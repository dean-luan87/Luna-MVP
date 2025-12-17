# decision_core/decision_core.py
from dataclasses import dataclass
from typing import Optional, Dict, Any, List

from core.flow_engine.planner import FlowPlanner, PlanningInput
from core.flow_engine.runtime import FlowRuntime
from core.query_engine.query_manager import QueryEngine, QueryType, PendingQuery
from task_chain.task_chain_manager import TaskChainManager, TaskStatus
from task_engine.tts import Utterance


@dataclass
class DecisionRequest:
    user_id: str
    utterance: str
    extra: Optional[Dict[str, Any]] = None


class SimpleIntentExtractor:
    """
    极简版意图识别：
    - 医院相关：go_hospital
    - 暂停：pause_task
    - 取消/不用：cancel_task
    - 继续：resume_task
    其余：generic_help
    """

    def extract(self, text: str) -> str:
        t = text.strip()
        if any(k in t for k in ["暂停", "先停", "先等等"]):
            return "pause_task"
        if any(k in t for k in ["不用", "不用去了", "算了", "取消"]):
            return "cancel_task"
        if any(k in t for k in ["继续", "接着来", "继续刚才"]):
            return "resume_task"
        if any(k in t for k in ["医院", "看病", "挂号"]):
            return "go_hospital"
        return "generic_help"


class SimpleSceneClassifier:
    """占位版场景识别：优先用 extra.scene_type，没有则 unknown。"""

    def classify(self, extra: Optional[Dict[str, Any]] = None) -> str:
        if not extra:
            return "unknown"
        return extra.get("scene_type", "unknown")


@dataclass
class Action:
    """Action 数据结构"""
    type: str
    payload: Dict[str, Any]


class DecisionCore:
    """
    v1.4.4 决策核心：
    - 先看用户是否在回答一个 PendingQuery
    - 再看是否是任务控制意图（暂停/取消/继续）
    - 否则视为新任务，进入 Planner + Runtime
    
    v1.4.6d Step 10: 增加 TTS_ROUTER_* actions 支持

    ==================================================================
    [v1.4.9 P0-1 FREEZE] Decision routing order & user-visible behavior

    Frozen routing order for `handle(req)`:
    1) PendingQuery reply path (QueryEngine)
    2) Task control intent path (pause/cancel/resume)
    3) New task path (Planner + Runtime)

    Frozen TTS integration:
    - All speech outputs initiated by DecisionCore MUST go through
      `task_engine.tts.router_facade.get_tts_router_facade()`.
    - `handle_action(Action)` supports only the frozen TTS_ROUTER_* types
      listed in that method (adding new action types is a behavior change).

    Any change that alters the above routing order or action mapping
    requires a new minor/major version.
    ==================================================================
    """

    def __init__(
        self,
        flow_planner: FlowPlanner,
        flow_runtime: FlowRuntime,
        query_engine: QueryEngine,
        task_manager: TaskChainManager,
        intent_extractor: Optional[SimpleIntentExtractor] = None,
        scene_classifier: Optional[SimpleSceneClassifier] = None,
    ) -> None:
        self._planner = flow_planner
        self._runtime = flow_runtime
        self._query = query_engine
        self._tasks = task_manager
        self._intent_extractor = intent_extractor or SimpleIntentExtractor()
        self._scene_classifier = scene_classifier or SimpleSceneClassifier()
        
        # Step 10: 初始化 TTS Router Facade
        from task_engine.tts.router_facade import get_tts_router_facade
        self.tts_router = get_tts_router_facade()

    # -------------------------------
    # 主入口
    # -------------------------------
    def handle(self, req: DecisionRequest) -> str:
        # 1. 是否在回答一个未完成问询
        pending = self._query.get_active_query(req.user_id)
        if pending:
            return self._handle_query_answer(req, pending)

        # 2. 识别意图
        intent = self._intent_extractor.extract(req.utterance)

        # 2.1 任务控制类
        if intent in ("pause_task", "cancel_task", "resume_task"):
            return self._handle_task_control(req, intent)

        # 3. 视为新任务
        scene_type = self._scene_classifier.classify(req.extra)

        planning_input = PlanningInput(
            user_id=req.user_id,
            intent=intent,
            scene_type=scene_type,
            raw_utterance=req.utterance,
            extra=req.extra or {},
        )

        instance = self._planner.plan(planning_input)
        if not instance:
            return "目前我还不能很好处理这个需求。"

        # 注册并执行任务
        self._tasks.register_task(instance)
        self._runtime.start(instance)

        # P5-5: 自动注入播报内容
        # Step 13: 使用统一入口
        from task_engine.tts.router_facade import get_tts_router_facade
        tts_router = get_tts_router_facade()
        task_name = instance.context.intent or "任务"
        tts_router.speak_task(
            f"好的，开始执行 {task_name}",
            meta={"stage": "decision_start_task"},
        )

        prompts = instance.context.data.get("prompts", [])
        if prompts:
            return prompts[0]
        return "好的，我会一步步协助你。"

    # -------------------------------
    # 处理用户对问询的回答
    # -------------------------------
    def _handle_query_answer(self, req: DecisionRequest, q: PendingQuery) -> str:
        text = req.utterance.strip()
        # 非严格版 yes/no 识别
        is_yes = any(k in text for k in ["是", "好", "继续", "要", "嗯", "对"])
        is_no = any(k in text for k in ["不", "不用", "算了", "先这样"])

        # ---- GOAL 澄清 ----
        if q.query_type == QueryType.GOAL:
            # 找到当前任务上下文，写入 slot
            record = self._tasks.get_active_task_for_user(req.user_id)
            if record and q.slot:
                self._query.save_answer(record.instance.context, q.slot, text)
            self._query.close_query(q)
            return "好的，我已经了解你的具体目标了。"

        # ---- CONTINUE 继续任务 ----
        if q.query_type == QueryType.CONTINUE:
            self._query.close_query(q)
            if is_yes and q.task_id:
                self._tasks.resume_task(q.task_id)
                return "好的，我们继续刚才的任务。"
            elif is_no and q.task_id:
                self._tasks.cancel_task(q.task_id)
                return "好的，我已经帮你停掉这个任务。"
            else:
                return "那我们先保持当前状态不变。"

        # ---- CANCEL 取消确认 ----
        if q.query_type == QueryType.CANCEL:
            self._query.close_query(q)
            if is_yes and q.task_id:
                self._tasks.cancel_task(q.task_id)
                return "这个任务已经取消。"
            else:
                return "好的，那我们暂时不取消。"

        # ---- NEXT：任务完成后下一步 ----
        if q.query_type == QueryType.NEXT:
            self._query.close_query(q)
            if is_yes:
                return "那你可以跟我说一下，接下来想做什么。"
            else:
                return "好的，这次我们就先到这里。"

        # 其它类型暂不处理
        self._query.close_query(q)
        return "好的。"

    # -------------------------------
    # 任务控制类意图（暂停/继续/取消）
    # -------------------------------
    def _handle_task_control(self, req: DecisionRequest, intent: str) -> str:
        record = self._tasks.get_active_task_for_user(req.user_id)
        if not record:
            return "你目前没有正在进行的任务。"

        # 暂停任务：直接暂停
        if intent == "pause_task":
            if record.status == TaskStatus.ACTIVE:
                self._tasks.pause_task(record.task_id)
                # P5-5: 自动注入播报内容
                # Step 13: 使用统一入口
                from task_engine.tts.router_facade import get_tts_router_facade
                tts_router = get_tts_router_facade()
                tts_router.speak_task(
                    "已暂停当前任务",
                    meta={"stage": "decision_pause_task"},
                )
                return "好的，我先帮你暂停当前任务。"
            return "当前任务本来就不是进行中的状态。"

        # 继续任务：直接恢复
        if intent == "resume_task":
            if record.status == TaskStatus.PAUSED:
                self._tasks.resume_task(record.task_id)
                # P5-5: 自动注入播报内容
                # Step 13: 使用统一入口
                from task_engine.tts.router_facade import get_tts_router_facade
                tts_router = get_tts_router_facade()
                tts_router.speak_task(
                    "继续执行任务",
                    meta={"stage": "decision_resume_task"},
                )
                return "好的，我们继续刚才的任务。"
            return "当前任务现在不是暂停状态，暂时不需要恢复。"

        # 取消任务：先发起一个 CANCEL_CONFIRM 问询
        if intent == "cancel_task":
            q = self._query.create_cancel_query(
                user_id=req.user_id,
                task_id=record.task_id,
                task_name="当前任务",
            )
            return q.message

        return "我不太确定你的意思。"

    # -------------------------------
    # Step 10: TTS Router Actions 处理
    # -------------------------------
    def handle_action(self, action: Action) -> None:
        """
        处理 Action（Step 10: TTS Router 接入）

        Args:
            action: Action 对象，包含 type 和 payload
        """
        # --------------------------------------------------------------
        # [v1.4.9 P0-1 FREEZE] TTS_ROUTER_* action surface (DO NOT CHANGE)
        #
        # Frozen action types and mappings:
        # - TTS_ROUTER_TURN     -> tts_router.route_turn(...)
        # - TTS_ROUTER_STRAIGHT -> tts_router.route_straight(...)
        # - TTS_ROUTER_OBSTACLE -> tts_router.route_obstacle_warning(...)
        # - TTS_ROUTER_GENERIC  -> tts_router.route_generic(...)
        # - TTS_ROUTER_SAFETY   -> tts_router.route_safety(...)
        #
        # Any new action type / change in mapping is a contract change.
        # --------------------------------------------------------------
        # --- TTS ROUTER ACTIONS ---
        if action.type == "TTS_ROUTER_TURN":
            self.tts_router.route_turn(
                direction=action.payload.get("direction", "左转"),
                distance=action.payload.get("distance")
            )
            return

        if action.type == "TTS_ROUTER_STRAIGHT":
            self.tts_router.route_straight(
                distance=action.payload.get("distance")
            )
            return

        if action.type == "TTS_ROUTER_OBSTACLE":
            self.tts_router.route_obstacle_warning(
                direction=action.payload.get("direction"),
                distance_m=action.payload.get("distance"),
                obstacle_type=action.payload.get("type")
            )
            return

        if action.type == "TTS_ROUTER_GENERIC":
            self.tts_router.route_generic(
                category=action.payload.get("category", "TASK"),
                text=action.payload.get("text", "")
            )
            return

        if action.type == "TTS_ROUTER_SAFETY":
            # Step 11: 安全播报，直接进入安全队列
            self.tts_router.route_safety(
                text=action.payload.get("text", ""),
                **action.payload.get("meta", {})
            )
            return

        # 其他 action 类型暂不处理
        pass

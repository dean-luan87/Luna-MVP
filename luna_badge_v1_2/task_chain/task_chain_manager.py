# task_chain/task_chain_manager.py
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from core.flow_engine.runtime import FlowRuntime
from core.flow_engine.flow_types import FlowInstance
from task_engine.ask import (
    AskIntegrationService,
    AskResultBinder,
    AskSchema,
)
from task_engine.task_execution_result import TaskExecutionResult
from task_engine.task_lifecycle_state import (
    TaskLifecycleState,
    TaskLifecyclePhase,
    TaskLifecycleStatus,
)
from task_engine.scene.scene_runtime import SceneRuntime
from task_engine.scene.scene_integration import SceneIntegrationService, SceneIntegrationResult
from task_engine.scene.scene_context import scene_context_manager


class TaskStatus:
    ACTIVE = "active"
    PAUSED = "paused"
    FINISHED = "finished"
    CANCELLED = "cancelled"
    FAILED = "failed"


@dataclass
class TaskRecord:
    task_id: str
    user_id: str
    status: str
    instance: FlowInstance
    parent_task_id: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


class TaskChainManager:
    def __init__(self, runtime: FlowRuntime, scene_service: Optional[SceneIntegrationService] = None) -> None:
        self._runtime = runtime
        self._tasks: Dict[str, TaskRecord] = {}
        # v1.4.6a: Ask 集成服务（封装 AskChainRuntime 的生命周期）
        self.ask_integration = AskIntegrationService()
        # 保存任务的 task_meta，用于延迟启动 Ask
        self._task_meta: Dict[str, Dict[str, Any]] = {}
        # v1.4.6a A-5-4-2: 任务生命周期状态
        self._lifecycle = TaskLifecycleState()
        # P5-3-D: Scene 融合
        self.scene_runtime = SceneRuntime()
        self.scene_service = scene_service  # 可选，如果为 None 则跳过场景更新
        self.last_scene_id: Optional[str] = None
        self.scene_trace: List[Dict[str, Any]] = []  # 场景轨迹记录

    @property
    def lifecycle(self) -> TaskLifecycleState:
        """对外暴露 lifecycle，只读引用。"""
        return self._lifecycle

    # --------------------------
    # 注册任务
    # --------------------------
    def register_task(
        self,
        instance: FlowInstance,
        task_meta: Optional[Dict[str, Any]] = None,
        scene_chain_meta: Optional[Dict[str, Any]] = None,
    ) -> TaskRecord:
        """
        注册任务。
        
        v1.4.6a: 如果 task_meta 包含 ask_schema，则标记需要启动 AskChain。
        v1.4.6a A-5-3: 实现 Scene → AskChain 的决策逻辑。
        
        决策优先级：
        1. task_meta.get("ask_required") == True
        2. scene_chain_meta.get("ask_required") == True
        3. ask_schema.has_required_slots() == True
        4. 否则不启动 AskChain
        
        Args:
            instance: 任务实例
            task_meta: 任务元数据，可能包含 ask_schema, ask_required
            scene_chain_meta: 场景链元数据，可能包含 ask_required
        """
        record = TaskRecord(
            task_id=instance.context.task_id,
            user_id=instance.context.user_id,
            status=TaskStatus.ACTIVE,
            instance=instance,
        )
        self._tasks[record.task_id] = record
        
        # v1.4.6a A-5-3: 决策是否需要 AskChain
        ask_schema: Optional[AskSchema] = None
        if task_meta:
            # 尝试从 task_meta 中解析 ask_schema
            ask_schema_dict = task_meta.get("ask_schema")
            if ask_schema_dict and isinstance(ask_schema_dict, dict):
                ask_schema = AskSchema.from_dict(ask_schema_dict)
            elif isinstance(ask_schema_dict, AskSchema):
                ask_schema = ask_schema_dict
            
            self._task_meta[record.task_id] = task_meta
        
        # 决策逻辑（按优先级）
        requires_ask = False
        if task_meta and task_meta.get("ask_required"):
            requires_ask = True
        elif scene_chain_meta and scene_chain_meta.get("ask_required"):
            requires_ask = True
        elif ask_schema and ask_schema.has_required_slots():
            requires_ask = True
        
        # 设置 phase 状态
        instance.context.data["phase"] = "ask" if requires_ask else "task"
        
        # v1.4.6a A-5-4-2: 初始化 lifecycle，但不改变任何执行行为
        self._lifecycle.mark(
            phase=TaskLifecyclePhase.ASK if requires_ask else TaskLifecyclePhase.TASK,
            status=TaskLifecycleStatus.ACTIVE,
            reason="task_registered",
            source="system",
            extra_meta={"task_id": record.task_id},
        )
        
        return record

    # --------------------------
    # 获取用户当前活跃任务
    # --------------------------
    def get_active_task_for_user(self, user_id: str) -> Optional[TaskRecord]:
        for record in self._tasks.values():
            if record.user_id == user_id and record.status in [TaskStatus.ACTIVE, TaskStatus.PAUSED]:
                return record
        return None

    # --------------------------
    # 状态更新
    # --------------------------
    def update_status(self, task_id: str, new_status: str) -> None:
        record = self._tasks.get(task_id)
        if not record:
            return
        record.status = new_status
        record.updated_at = time.time()

    # --------------------------
    # 暂停任务
    # --------------------------
    def pause_task(self, task_id: str) -> None:
        record = self._tasks.get(task_id)
        if not record or record.status != TaskStatus.ACTIVE:
            return
        self._runtime.pause(task_id)
        self.update_status(task_id, TaskStatus.PAUSED)
        # P5-5: 自动注入播报内容
        # Step 13: 使用统一入口
        from task_engine.tts.router_facade import get_tts_router_facade
        tts_router = get_tts_router_facade()
        tts_router.speak_task(
            "已暂停当前任务",
            meta={"stage": "task_pause", "task_id": task_id},
        )

    # --------------------------
    # 恢复任务
    # --------------------------
    def resume_task(self, task_id: str) -> None:
        record = self._tasks.get(task_id)
        if not record or record.status != TaskStatus.PAUSED:
            return
        self._runtime.resume(task_id)
        self.update_status(task_id, TaskStatus.ACTIVE)
        # P5-5: 自动注入播报内容
        # Step 13: 使用统一入口
        from task_engine.tts.router_facade import get_tts_router_facade
        tts_router = get_tts_router_facade()
        tts_router.speak_task(
            "继续执行任务",
            meta={"stage": "task_resume", "task_id": task_id},
        )

    # --------------------------
    # 取消任务
    # --------------------------
    def cancel_task(self, task_id: str) -> None:
        record = self._tasks.get(task_id)
        if not record:
            return
        record.instance.finished = True
        self.update_status(task_id, TaskStatus.CANCELLED)
        # P5-5: 自动注入播报内容
        # Step 13: 使用统一入口
        from task_engine.tts.router_facade import get_tts_router_facade
        tts_router = get_tts_router_facade()
        tts_router.speak_task(
            "任务已取消",
            meta={"stage": "task_cancel", "task_id": task_id},
        )

    # --------------------------
    # 任务结束
    # --------------------------
    def mark_finished(self, task_id: str) -> None:
        self.update_status(task_id, TaskStatus.FINISHED)

    # --------------------------
    # 插入子任务
    # --------------------------
    def insert_subtask(self, parent_task_id: str, instance: FlowInstance) -> None:
        parent_record = self._tasks.get(parent_task_id)
        # 如果父任务已注册，则暂停它
        if parent_record and parent_record.status == TaskStatus.ACTIVE:
            self.pause_task(parent_task_id)
        # 如果父任务在 runtime 中但未注册，直接暂停 runtime 中的实例
        elif not parent_record:
            parent_instance = self._runtime.get_instance(parent_task_id)
            if parent_instance and not parent_instance.paused:
                parent_instance.paused = True
        # 设置子任务的父任务ID（在注册前设置，确保实例本身也有这个属性）
        instance.parent_task_id = parent_task_id
        # 子任务注册
        child_record = self.register_task(instance)
        child_record.parent_task_id = parent_task_id
        # 启动子任务
        self._runtime.start(instance)

    # --------------------------
    # v1.4.4 扩展：切换任务
    # --------------------------
    def switch_task(self, old_task_id: str, new_instance: FlowInstance) -> TaskRecord:
        """
        切换任务：取消旧任务，创建新任务
        
        Args:
            old_task_id: 旧任务ID
            new_instance: 新任务实例
            
        Returns:
            新任务的 TaskRecord
        """
        # 1. 取消旧任务
        self.cancel_task(old_task_id)
        
        # 2. 注册新任务
        new_record = self.register_task(new_instance)
        
        # 3. 启动新任务
        self._runtime.start(new_instance)
        
        # P5-5: 自动注入播报内容
        # Step 13: 使用统一入口
        from task_engine.tts.router_facade import get_tts_router_facade
        tts_router = get_tts_router_facade()
        task_name = new_instance.context.intent or "新任务"
        tts_router.speak_task(
            f"已切换至 {task_name}",
            meta={"stage": "task_switch", "old_task_id": old_task_id, "new_task_id": new_record.task_id},
        )
        
        return new_record

    # --------------------------
    # v1.4.4 扩展：子任务结束 → 恢复父任务
    # --------------------------
    def restore_parent_after_child_finished(self, child_task_id: str) -> Optional[TaskRecord]:
        """
        子任务完成后恢复父任务
        
        Args:
            child_task_id: 子任务ID
            
        Returns:
            父任务的 TaskRecord，如果没有父任务则返回 None
        """
        child_record = self._tasks.get(child_task_id)
        if not child_record:
            return None
        
        # 标记子任务为完成
        self.mark_finished(child_task_id)
        
        # 如果有父任务，恢复它
        parent_task_id = child_record.parent_task_id
        if parent_task_id:
            parent_record = self._tasks.get(parent_task_id)
            if parent_record and parent_record.status == TaskStatus.PAUSED:
                self.resume_task(parent_task_id)
                return parent_record
        
        return None

    # --------------------------
    # v1.4.6a A-5-4-3: 声明式 Pause / Resume API（不改变执行逻辑）
    # --------------------------

    def pause_lifecycle(self, reason: str = "manual_pause") -> TaskLifecycleState:
        """
        用户显式请求暂停；Ultra 阶段：只改变生命周期 + 依赖层逻辑（A-5-4-4 已接管 handle_user_turn）。
        
        Args:
            reason: 暂停原因，默认为 "manual_pause"
            
        Returns:
            更新后的 TaskLifecycleState
        """
        if self._lifecycle.status == TaskLifecycleStatus.ACTIVE:
            self._lifecycle.mark(
                status=TaskLifecycleStatus.PAUSED,
                reason=reason,
                source="user",
            )
        return self._lifecycle

    def resume_lifecycle(self, reason: str = "manual_resume") -> TaskLifecycleState:
        """
        从暂停恢复为 ACTIVE；保持 Ask/Task 内部指针不变。
        
        Args:
            reason: 恢复原因，默认为 "manual_resume"
            
        Returns:
            更新后的 TaskLifecycleState
        """
        if self._lifecycle.status == TaskLifecycleStatus.PAUSED:
            self._lifecycle.mark(
                status=TaskLifecycleStatus.ACTIVE,
                reason=reason,
                source="user",
            )
        return self._lifecycle

    # --------------------------
    # v1.4.6a: Ask 系统集成（使用 AskIntegrationService + AskResultBinder）
    # --------------------------

    def _create_result_with_tts(self, scene_result: Optional[SceneIntegrationResult] = None, **kwargs) -> TaskExecutionResult:
        """
        创建 TaskExecutionResult 并自动从 tts_manager 收集 utterances。
        
        P5-2: 统一入口，确保所有返回的 TaskExecutionResult 都包含 TTS 输出。
        P5-3-D: 同时包含场景信息。
        
        Args:
            scene_result: 可选的场景集成结果
            **kwargs: TaskExecutionResult 的构造参数
            
        Returns:
            TaskExecutionResult: 包含 TTS utterances 和场景信息的结果
        """
        result = TaskExecutionResult(**kwargs)
        # 自动从 TtsManager 收集 utterances
        result.pop_utterances_from_tts_manager()
        
        # P5-3-D: 添加场景信息
        if scene_result:
            result.scene_snapshot = {
                "scene_id": scene_result.context.scene,
                "tag": scene_result.context.tag,
                "context_id": scene_result.context.scene or "",
            }
            result.scene_trace = self.scene_trace.copy()  # 拷贝一份
        else:
            # 如果没有场景结果，尝试从全局上下文获取
            current_ctx = scene_context_manager.get_current()
            if current_ctx:
                result.scene_snapshot = {
                    "scene_id": current_ctx.scene,
                    "tag": current_ctx.tag,
                    "context_id": current_ctx.scene or "",
                }
                result.scene_trace = self.scene_trace.copy()
        
        return result

    def handle_user_turn(self, user_text: str, now_ts: Optional[int] = None) -> TaskExecutionResult:
        """
        处理用户输入的主入口。
        
        v1.4.6a A-5-3: 统一返回 TaskExecutionResult，实现 AskChain → TaskChain 的自动接续。
        v1.4.6a A-5-4-4: 添加暂停硬拦截，暂停状态下不推进 Ask/Task。
        
        Args:
            user_text: 用户输入文本
            now_ts: 当前时间戳（秒级），如果为 None 则使用当前时间
            
        Returns:
            TaskExecutionResult: 统一的任务执行结果
        """
        if now_ts is None:
            now_ts = int(time.time())

        # === P5-3-D：Scene Fusion 入口 ===
        scene_result: Optional[SceneIntegrationResult] = None
        if self.scene_service:
            # 尝试从全局上下文获取场景信息（简化版，实际应该传入 OCR/objects 等）
            current_ctx = scene_context_manager.get_current()
            if current_ctx:
                # 使用现有上下文，不重新识别
                from task_engine.scene.scene_classifier import SceneGuess
                guess = SceneGuess(
                    scene=current_ctx.scene,
                    tag=current_ctx.tag,
                    confidence=current_ctx.confidence,
                )
                scene_result = SceneIntegrationResult(
                    context=current_ctx,
                    guess=guess,
                    pack_ref=current_ctx.pack_ref,
                    enter_voice=None,  # 不重新生成进入播报
                    hints=[],
                    exit_voice=None,
                )
            else:
                # 如果没有上下文，尝试识别场景（使用空输入）
                try:
                    scene_result = self.scene_service.ensure_scene_context(
                        ocr_text=None,
                        objects=None,
                        gps_hint=None,
                        history_tags=None,
                    )
                except Exception:
                    # 场景服务不可用，继续执行任务
                    pass
        
        # 处理场景进入/事件/退出
        if scene_result:
            # 1. 进入新场景
            if scene_result.context.scene != self.last_scene_id:
                if self.last_scene_id is not None:
                    # 上一个场景退出
                    from task_engine.tts import tts_manager
                    tts_manager.speak(
                        "场景已结束，准备进入下一任务。",
                        level="info",
                        channel="tts",
                        stage="scene_exit",
                        last_scene=self.last_scene_id,
                    )
                    # 记录退出事件
                    self.scene_trace.append({
                        "type": "exit",
                        "scene_id": self.last_scene_id,
                        "timestamp": now_ts,
                    })
                
                # 处理新场景进入
                enter_out = self.scene_runtime.handle_enter(scene_result)
                if enter_out.event_type:
                    self.scene_trace.append({
                        "type": "enter",
                        "scene_id": scene_result.context.scene,
                        "tag": scene_result.context.tag,
                        "timestamp": now_ts,
                    })
                self.last_scene_id = scene_result.context.scene

            # 2. 场景内部事件
            event_out = self.scene_runtime.handle_events(scene_result)
            if event_out.event_type == "event":
                self.scene_trace.append({
                    "type": "event",
                    "scene_id": scene_result.context.scene,
                    "tag": scene_result.context.tag,
                    "timestamp": now_ts,
                    "hints": event_out.hints,
                })

        # === A-5-4-4：用户暂停硬拦截（必须在最前面） ===
        if self._lifecycle.status == TaskLifecycleStatus.PAUSED:
            # 不调用 AskIntegration，不推进 TaskRuntime，原地返回"已暂停"
            # 查找当前活跃的任务 ID
            current_task_id = None
            for task_id, record in self._tasks.items():
                if record.status == TaskStatus.ACTIVE:
                    current_task_id = task_id
                    break
            
            # Ultra: 在 meta 中包含暂停统计信息
            pause_type = "user" if self._lifecycle.source == "user" else "system"
            return self._create_result_with_tts(
                scene_result=scene_result,
                ask_active=False,
                task_active=False,
                ask_output=None,
                task_output=None,
                task_finished=False,
                phase="idle",  # 暂停时暂时不区分 ask/task
                status=None,
                paused=True,
                pause_type=pause_type,
                meta={
                    "reason": self._lifecycle.reason,
                    "task_id": current_task_id,
                    "pause_count": self._lifecycle.pause_count,
                    "total_pause_duration": self._lifecycle.total_pause_duration,
                },
            )

        # 0. 如果没有 active Ask，检查是否有任务需要启动 Ask
        if not self.ask_integration.has_active:
            # 查找当前活跃的任务，检查是否需要启动 Ask
            for task_id, record in self._tasks.items():
                if record.status == TaskStatus.ACTIVE:
                    task_meta = self._task_meta.get(task_id)
                    if task_meta:
                        # 启动 Ask 并返回第一次 prompt
                        ask_result = self.ask_integration.maybe_start_for_task(
                            task_id=task_id,
                            task_meta=task_meta,
                            now_ts=now_ts,
                        )
                        if ask_result is not None:
                            # 有 Ask 前置 → 本轮只返回问询提示，不执行主任务
                            record.instance.context.data["phase"] = "ask"
                            # v1.4.6a A-5-4-2: 同步 lifecycle 状态（不改变行为）
                            self._lifecycle.mark(
                                phase=TaskLifecyclePhase.ASK,
                                status=TaskLifecycleStatus.ACTIVE,
                                reason="ask_started",
                                source="system",
                            )
                            return self._create_result_with_tts(
                                scene_result=scene_result,
                                ask_active=True,
                                task_active=False,
                                ask_output=ask_result.reply,
                                phase="ask",
                                paused=False,
                                pause_type=None,
                            )
                    break

        # 1. 若当前有 active Ask，则优先处理
        ask_result = self.ask_integration.step_if_active(
            user_message=user_text,
            now_ts=now_ts,
        )

        if ask_result is not None:
            # 1.1 Ask 还没结束 → 继续问，不执行主任务
            if not ask_result.done:
                # v1.4.6a A-5-4-2: 同步 lifecycle 状态（不改变行为）
                self._lifecycle.mark(
                    phase=TaskLifecyclePhase.ASK,
                    status=TaskLifecycleStatus.ACTIVE,
                    reason="ask_step",
                    source="system",
                )
                return self._create_result_with_tts(
                    scene_result=scene_result,
                    ask_active=True,
                    task_active=False,
                    ask_output=ask_result.reply,
                    phase="ask",
                    paused=False,
                    pause_type=None,
                )

            # 1.2 Ask 已结束（aborted）
            if ask_result.aborted:
                # 超限/失败等情况，这里直接终止任务
                if ask_result.task_id and ask_result.task_id in self._task_meta:
                    del self._task_meta[ask_result.task_id]
                if ask_result.task_id:
                    record = self._tasks.get(ask_result.task_id)
                    if record:
                        record.instance.context.data["phase"] = "task"
                # v1.4.6a A-5-4-2: 同步 lifecycle 状态（不改变行为）
                self._lifecycle.mark(
                    status=TaskLifecycleStatus.ABORTED,
                    reason="ask_aborted",
                    source="system",
                )
                return self._create_result_with_tts(
                    scene_result=scene_result,
                    ask_active=False,
                    task_active=False,
                    ask_output=ask_result.reply,
                    task_finished=True,
                    phase="task",
                    status="ask_failed",
                    paused=False,
                    pause_type=None,
                )

            # 1.3 正常完成：使用 AskResultBinder 将答案注入任务上下文，然后切换到 TaskChain
            if ask_result.task_id:
                record = self._tasks.get(ask_result.task_id)
                if record:
                    task_meta = self._task_meta.get(ask_result.task_id, {})
                    # 使用 AskResultBinder 进行绑定
                    AskResultBinder.bind(
                        answers=ask_result.answers,
                        task_meta=task_meta,
                        task_context=record.instance.context.data,
                    )
                    # A-5-3: Ask 完成 → 切换到 TaskChain 阶段
                    record.instance.context.data["phase"] = "task"
                    # 启动主任务链
                    self._runtime.start(record.instance)
                # 清除 task_meta，避免重复启动 Ask
                if ask_result.task_id in self._task_meta:
                    del self._task_meta[ask_result.task_id]
            
            # v1.4.6a A-5-4-2: 同步 lifecycle 状态（不改变行为）
            self._lifecycle.mark(
                phase=TaskLifecyclePhase.TASK,
                status=TaskLifecycleStatus.ACTIVE,
                reason="ask_completed_task_started",
                source="system",
            )
            
            return self._create_result_with_tts(
                scene_result=scene_result,
                ask_active=False,
                task_active=True,
                ask_output=ask_result.reply,
                task_output="ask_completed_and_task_started",
                phase="task",
                paused=False,
                pause_type=None,
            )

        # 2. 没有 active Ask → 执行主任务链
        # 查找当前活跃的任务
        active_record = None
        for task_id, record in self._tasks.items():
            if record.status == TaskStatus.ACTIVE:
                active_record = record
                break
        
        if active_record:
            # 检查任务是否已完成（检查 status 或 instance.finished）
            if active_record.status == TaskStatus.FINISHED or active_record.instance.finished:
                # v1.4.6a A-5-4-2: 同步 lifecycle 状态（不改变行为）
                self._lifecycle.mark(
                    status=TaskLifecycleStatus.FINISHED,
                    reason="task_completed",
                    source="system",
                )
                return self._create_result_with_tts(
                    scene_result=scene_result,
                    ask_active=False,
                    task_active=False,
                    task_finished=True,
                    phase="task",
                    paused=False,
                    pause_type=None,
                )
            
            # 任务正在执行中
            active_record.instance.context.data.setdefault("phase", "task")
            # v1.4.6a A-5-4-2: 同步 lifecycle 状态（不改变行为）
            self._lifecycle.mark(
                phase=TaskLifecyclePhase.TASK,
                status=TaskLifecycleStatus.ACTIVE,
                reason="task_running",
                source="system",
            )
            return self._create_result_with_tts(
                scene_result=scene_result,
                ask_active=False,
                task_active=True,
                task_output="task_running",
                phase="task",
                paused=False,
                pause_type=None,
            )
        
        # 没有活跃任务
        return self._create_result_with_tts(
            scene_result=scene_result,
            ask_active=False,
            task_active=False,
            phase="task",
            paused=False,
            pause_type=None,
        )

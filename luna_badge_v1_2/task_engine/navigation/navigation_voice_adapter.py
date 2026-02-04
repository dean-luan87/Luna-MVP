"""
NavigationVoiceAdapter: 导航语音适配器

负责把 Navigation / Speech 子系统产生的 speech_event
适配为一组 Utterance，由上层 Router 决定是否播报。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from task_engine.tts import Utterance
from task_engine.tts.tts_policy import (
    TTSCategory,
    make_utterance,
)


SpeechEvent = Union[str, Dict[str, Any]]


@dataclass
class NavigationVoiceAdapterConfig:
    """导航语音适配器配置"""
    default_language: str = "zh-CN"
    # 后面可以扩展：voice_profile, style 映射等


class NavigationVoiceAdapter:
    """
    负责把 Navigation / Speech 子系统产生的 speech_event
    适配为一组 Utterance，由上层 Router 决定是否播报。
    """

    def __init__(self, config: Optional[NavigationVoiceAdapterConfig] = None) -> None:
        self.config = config or NavigationVoiceAdapterConfig()

    # ---- 主入口 ----------------------------------------------------------

    def handle_speech_event(self, event: SpeechEvent) -> List[Utterance]:
        """
        接受 speech_event（str 或 dict），返回一组 Utterance。

        不直接调用 TTS，由调用方把结果交给 Router。

        Args:
            event: speech_event，可以是字符串或字典

        Returns:
            Utterance 列表
        """
        if event is None:
            return []

        # 向后兼容：字符串 → 视为普通导航播报
        if isinstance(event, str):
            text = event.strip()
            if not text:
                return []
            return [self._make_navigation_utterance(text=text, meta={"source": "raw_string"})]

        if not isinstance(event, dict):
            # 非预期格式，直接丢弃，避免报错
            return []

        # 标准 speech_event 结构：
        # {
        #   "speak": True,
        #   "decision": "STOP" / "LEFT" / "RIGHT" / "FORWARD" / ...,
        #   "text": "前方 3 米有障碍物，请减速",
        #   "style": "calm"/"alert",
        #   "priority": int,
        #   "interruptible": bool,
        #   "category": "navigation"
        # }

        if not event.get("speak", True):
            return []

        decision = (event.get("decision") or "").upper()
        text = event.get("text") or event.get("raw_text") or ""
        if not text:
            return []

        style = event.get("style") or "calm"

        # 允许 event 显式声明 category（安全 / 导航）
        explicit_cat = (event.get("category") or "").upper()

        # 1）先看决策类型（强语义）
        category = self._category_from_decision(decision)

        # 2）如果没有决策信息，再看显式 category / 文本关键词
        if category is None:
            if explicit_cat == "SAFETY":
                category = TTSCategory.SAFETY
            elif explicit_cat == "NAVIGATION":
                category = TTSCategory.NAVIGATION
            else:
                category = self._category_from_text(text) or TTSCategory.NAVIGATION

        if category == TTSCategory.SAFETY:
            return [self._make_safety_utterance(text, event, style)]
        else:
            return [self._make_navigation_utterance(text, event, style)]

    # ---- Category 推断 ---------------------------------------------------

    def _category_from_decision(self, decision: str) -> Optional[TTSCategory]:
        """根据决策类型推断类别"""
        # --------------------------------------------------------------
        # [1.4.X frozen] TURNING / STRAIGHT / WARNING → TTS 分类映射（禁止改语义）
        #
        # TURNING / STRAIGHT / WARNING 等“对用户可见”的语义类别，最终都
        # 会落在 SAFETY / NAVIGATION 两个播报类别上（影响优先级与节流）。
        #
        # Frozen mapping sets:
        # - SAFETY decisions:
        #   STOP, DANGER, OBSTACLE_FRONT, OBSTACLE, CLIFF, STAIRS_DOWN
        # - NAVIGATION decisions:
        #   LEFT, RIGHT, SLIGHT_LEFT, SLIGHT_RIGHT, FORWARD, KEEP_STRAIGHT,
        #   TURN_LEFT, TURN_RIGHT
        #
        # Changing these sets changes what the user hears first.
        # --------------------------------------------------------------
        if not decision:
            return None

        # 停止 / 危险一律走 SAFETY
        if decision in {
            "STOP",
            "DANGER",
            "OBSTACLE_FRONT",
            "OBSTACLE",
            "CLIFF",
            "STAIRS_DOWN",
        }:
            return TTSCategory.SAFETY

        # 转向 / 前进走 NAVIGATION
        if decision in {
            "LEFT",
            "RIGHT",
            "SLIGHT_LEFT",
            "SLIGHT_RIGHT",
            "FORWARD",
            "KEEP_STRAIGHT",
            "TURN_LEFT",
            "TURN_RIGHT",
        }:
            return TTSCategory.NAVIGATION

        return None

    def _category_from_text(self, text: str) -> Optional[TTSCategory]:
        """根据文本关键词推断类别"""
        # --------------------------------------------------------------
        # [1.4.X frozen] 文本关键词 → TTS 分类启发式（禁止改语义）
        #
        # This heuristic is used only when decision/category is not provided.
        # Frozen keyword lists (semantics): danger_keywords/nav_keywords.
        #
        # Any change here can reclassify speech output and alter scheduling.
        # --------------------------------------------------------------
        if not text:
            return None

        t = text.lower()

        danger_keywords = [
            "危险", "obstacle", "障碍", "台阶", "下坡", "跌落",
            "车", "机动车", "道路", "马路", "边缘",
        ]
        nav_keywords = [
            "左转", "右转", "直行", "前方", "米", "路口", "出口",
            "turn", "left", "right", "straight",
        ]

        if any(k in t for k in danger_keywords):
            return TTSCategory.SAFETY
        if any(k in t for k in nav_keywords):
            return TTSCategory.NAVIGATION

        return None

    # ---- Utterance 构造 --------------------------------------------------

    def _make_navigation_utterance(
        self,
        text: str,
        event: Optional[Dict[str, Any]] = None,
        style: str = "calm",
        meta: Optional[Dict[str, Any]] = None,
    ) -> Utterance:
        """构造导航类 Utterance"""
        extra_meta: Dict[str, Any] = {
            "source": "navigation",
            "style": style,
            "tts_category": "NAVIGATION",
            "lang": self.config.default_language,
        }
        if event:
            extra_meta["speech_event"] = event
        if meta:
            extra_meta.update(meta)

        return make_utterance(
            text=text,
            category=TTSCategory.NAVIGATION,
            meta=extra_meta,
        )

    def _make_safety_utterance(
        self,
        text: str,
        event: Optional[Dict[str, Any]] = None,
        style: str = "alert",
        meta: Optional[Dict[str, Any]] = None,
    ) -> Utterance:
        """构造安全类 Utterance"""
        extra_meta: Dict[str, Any] = {
            "source": "navigation",
            "style": style,
            "tts_category": "SAFETY",
            "lang": self.config.default_language,
        }
        if event:
            extra_meta["speech_event"] = event
        if meta:
            extra_meta.update(meta)

        return make_utterance(
            text=text,
            category=TTSCategory.SAFETY,
            meta=extra_meta,
        )


    # ====== 向后兼容：保留旧的语义化接口（但改为返回 Utterance 列表） ======
    # 这些方法现在返回 Utterance，由调用方决定是否通过 Router 播报

    def announce_route_planned(
        self,
        destination_name: str,
        *,
        eta_minutes: Optional[int] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> List[Utterance]:
        """路线规划完成时播报，用 TASK 类别。返回 Utterance 列表。"""
        if eta_minutes is not None:
            text = f"已为您规划到 {destination_name} 的路线，预计用时 {eta_minutes} 分钟。"
        else:
            text = f"已为您规划到 {destination_name} 的路线。"
        return [make_utterance(text, TTSCategory.TASK, meta=meta)]

    def announce_navigation_started(self, *, meta: Optional[Dict[str, Any]] = None) -> List[Utterance]:
        """导航正式开始时播报，用 TASK 类别。返回 Utterance 列表。"""
        return [make_utterance("导航已开始，请注意听取前方路况提示。", TTSCategory.TASK, meta=meta)]

    def announce_navigation_finished(self, *, meta: Optional[Dict[str, Any]] = None) -> List[Utterance]:
        """导航完全结束时播报，用 TASK 类别。返回 Utterance 列表。"""
        return [make_utterance("导航已结束。", TTSCategory.TASK, meta=meta)]

    def announce_turn(
        self,
        *,
        distance_m: Optional[int] = None,
        direction: str,
        meta: Optional[Dict[str, Any]] = None,
    ) -> List[Utterance]:
        """通用转向提示：向左/向右/调头等。返回 Utterance 列表。"""
        if distance_m is None:
            text = f"请{direction}。"
        else:
            text = f"前方 {distance_m} 米，请{direction}。"
        return [make_utterance(text, TTSCategory.NAVIGATION, meta=meta)]

    def announce_straight(
        self,
        *,
        distance_m: Optional[int] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> List[Utterance]:
        """直行提示，可选距离。返回 Utterance 列表。"""
        if distance_m is None:
            text = "请继续直行。"
        else:
            text = f"请继续直行约 {distance_m} 米。"
        return [make_utterance(text, TTSCategory.NAVIGATION, meta=meta)]

    def announce_reroute(
        self,
        *,
        reason: str = "偏离路线",
        meta: Optional[Dict[str, Any]] = None,
    ) -> List[Utterance]:
        """重新规划路线提示，用 NAVIGATION 类。返回 Utterance 列表。"""
        text = f"由于{reason}，我正在为您重新规划路线。"
        return [make_utterance(text, TTSCategory.NAVIGATION, meta=meta)]

    def announce_arrival(
        self,
        *,
        destination_name: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> List[Utterance]:
        """到达目的地提示，用 NAVIGATION 类。返回 Utterance 列表。"""
        if destination_name:
            text = f"已到达 {destination_name} 附近。"
        else:
            text = "您已到达目的地附近。"
        return [make_utterance(text, TTSCategory.NAVIGATION, meta=meta)]

    def announce_eta_update(
        self,
        *,
        eta_minutes: int,
        meta: Optional[Dict[str, Any]] = None,
    ) -> List[Utterance]:
        """ETA 更新提示，用 NAVIGATION 类。返回 Utterance 列表。"""
        text = f"预计还有 {eta_minutes} 分钟到达。"
        return [make_utterance(text, TTSCategory.NAVIGATION, meta=meta)]

    def announce_crowded_ahead(
        self,
        *,
        meta: Optional[Dict[str, Any]] = None,
    ) -> List[Utterance]:
        """人群拥挤提示，用 SAFETY 类。返回 Utterance 列表。"""
        text = "前方人多，请减速并注意避让。"
        return [make_utterance(text, TTSCategory.SAFETY, meta=meta)]

    def announce_complex_environment(
        self,
        *,
        meta: Optional[Dict[str, Any]] = None,
    ) -> List[Utterance]:
        """环境复杂提示，如地铁口、商场等。返回 Utterance 列表。"""
        text = "前方环境较复杂，请您放慢脚步，注意安全。"
        return [make_utterance(text, TTSCategory.SAFETY, meta=meta)]

    def announce_obstacle_warning(
        self,
        *,
        direction: Optional[str] = None,
        distance_m: Optional[int] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> List[Utterance]:
        """通用障碍物提示，用 SAFETY 类。返回 Utterance 列表。"""
        if direction and distance_m:
            text = f"{direction}方向约 {distance_m} 米处有障碍物，请注意避让。"
        elif direction:
            text = f"{direction}方向有障碍物，请注意避让。"
        else:
            text = "前方有障碍物，请注意避让。"
        return [make_utterance(text, TTSCategory.SAFETY, meta=meta)]

    def announce_red_light_wait(
        self,
        *,
        remain_seconds: Optional[int] = None,
        meta: Optional[Dict[str, Any]] = None,
    ) -> List[Utterance]:
        """红灯等待提示，用 SAFETY 类。返回 Utterance 列表。"""
        if remain_seconds is None:
            text = "当前为红灯，请在安全位置等待。"
        else:
            text = f"当前为红灯，请在安全位置等待，大约还需 {remain_seconds} 秒。"
        return [make_utterance(text, TTSCategory.SAFETY, meta=meta)]

    def announce_cross_with_caution(
        self,
        *,
        meta: Optional[Dict[str, Any]] = None,
    ) -> List[Utterance]:
        """绿灯可通行但建议谨慎时使用，用 SAFETY 类。返回 Utterance 列表。"""
        text = "现在可以通行，请注意观察来车，尽快通过。"
        return [make_utterance(text, TTSCategory.SAFETY, meta=meta)]


# 模块级单例（向后兼容）
navigation_voice = NavigationVoiceAdapter()

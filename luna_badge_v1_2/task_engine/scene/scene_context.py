from __future__ import annotations

"""
SceneContext: 场景运行时上下文封装。

职责：
- 持有当前场景识别结果（SceneGuess）；
- 绑定对应的 ScenePackRef（来自 SceneRegistry）；
- 记录与场景相关的运行参数（ocr_text / objects / gps_hint / history_tags 等）；
- 提供"场景是否变化"的判断方法；
- 作为 TaskEngine / DecisionCore 的统一场景入口。

注意：
- 不做 IO、不做模型推理；
- 不直接依赖 TaskChainManager，仅作为上游输入。
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from task_engine.scene.scene_classifier import SceneGuess
from task_engine.scene.scene_registry import ScenePackRef


@dataclass
class SceneContext:
    """
    场景运行时上下文。

    字段说明：
    - scene: 当前场景主类，例如 "subway" / "hospital"；
    - tag: 当前场景标签，例如 "静安寺站" / "虹口医院"；
    - confidence: 场景识别置信度；
    - pack_ref: 对应的场景包引用（可为 None）；
    - ocr_text: 最近一次用于识别场景的 OCR 文本；
    - objects: 最近一次用于识别场景的物体标签列表；
    - gps_hint: 与位置相关的文本提示；
    - history_tags: 与用户关联的历史场景标签（如常去"虹口医院"）；
    - metadata: 运行时附加信息（例如 environment / user_intent 等）；
    - last_updated_at: 最近一次更新上下文的时间。
    """

    scene: Optional[str] = None
    tag: Optional[str] = None
    confidence: float = 0.0

    pack_ref: Optional[ScenePackRef] = None

    ocr_text: Optional[str] = None
    objects: List[str] = field(default_factory=list)
    gps_hint: Optional[str] = None

    history_tags: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    last_updated_at: Optional[datetime] = None
    
    # P5-3: 记录已播报的提示 ID，避免重复播报
    spoken_flags: set = field(default_factory=set)

    # ---------- 构造与更新 ----------

    @classmethod
    def from_guess(
        cls,
        guess: SceneGuess,
        pack_ref: Optional[ScenePackRef] = None,
        *,
        ocr_text: Optional[str] = None,
        objects: Optional[List[str]] = None,
        gps_hint: Optional[str] = None,
        history_tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "SceneContext":
        """
        根据 SceneGuess + 可选的 ScenePackRef 构建一个新的 SceneContext。
        """
        now = datetime.utcnow()
        return cls(
            scene=guess.scene,
            tag=guess.tag,
            confidence=guess.confidence,
            pack_ref=pack_ref,
            ocr_text=ocr_text,
            objects=list(objects or []),
            gps_hint=gps_hint,
            history_tags=list(history_tags or []),
            metadata=dict(metadata or {}),
            last_updated_at=now,
        )

    def update_from_guess(
        self,
        guess: SceneGuess,
        pack_ref: Optional[ScenePackRef] = None,
        *,
        ocr_text: Optional[str] = None,
        objects: Optional[List[str]] = None,
        gps_hint: Optional[str] = None,
        append_history_tag: bool = True,
    ) -> None:
        """
        用新的 SceneGuess 更新当前上下文。

        - 若 append_history_tag=True 且 guess.tag 不为空，则追加至 history_tags（去重）；
        - 更新 last_updated_at。
        """
        self.scene = guess.scene
        self.tag = guess.tag
        self.confidence = guess.confidence
        self.pack_ref = pack_ref

        if ocr_text is not None:
            self.ocr_text = ocr_text

        if objects is not None:
            self.objects = list(objects)

        if gps_hint is not None:
            self.gps_hint = gps_hint

        if append_history_tag and guess.tag:
            if guess.tag not in self.history_tags:
                self.history_tags.append(guess.tag)

        self.last_updated_at = datetime.utcnow()

    # ---------- 场景变化判断 ----------

    def has_scene_changed(
        self,
        guess: SceneGuess,
        *,
        confidence_delta_threshold: float = 0.2,
    ) -> bool:
        """
        判断给定的 SceneGuess 是否与当前上下文"发生了场景级变化"。

        变化标准（任一满足即视为变化）：
        - scene 不同；
        - tag 不同；
        - 置信度变化幅度超过 confidence_delta_threshold。
        """
        # 任何一个为 None 的情况，直接当作变化
        if self.scene is None or guess.scene is None:
            return True

        if guess.scene != self.scene:
            return True

        if guess.tag != self.tag:
            return True

        if abs(guess.confidence - self.confidence) > float(confidence_delta_threshold):
            return True

        return False

    # ---------- 上下文附加能力 ----------

    def attach_environment(self, env: Dict[str, Any]) -> None:
        """
        附加或更新与环境相关的信息，例如：
        - 光照 / 噪声
        - 网络状态
        - 设备电量等
        """
        env_meta = self.metadata.get("environment", {})
        if not isinstance(env_meta, dict):
            env_meta = {}
        env_meta.update(env or {})
        self.metadata["environment"] = env_meta

    def attach_user_intent(self, intent: Dict[str, Any]) -> None:
        """
        附加或更新与用户意图相关的信息，例如：
        - 用户当前目标（去挂号 / 去洗手间等）
        - 上一次任务链执行类型
        """
        intent_meta = self.metadata.get("user_intent", {})
        if not isinstance(intent_meta, dict):
            intent_meta = {}
        intent_meta.update(intent or {})
        self.metadata["user_intent"] = intent_meta

    # ---------- 工具方法 ----------

    def to_dict(self) -> Dict[str, Any]:
        """
        方便日志与调试，将上下文转换为可序列化字典。

        注意：pack_ref 只保留其关键信息。
        """
        data = asdict(self)

        # pack_ref 无法直接 JSON 序列化，这里做简化处理
        ref = self.pack_ref
        if ref is not None:
            data["pack_ref"] = {
                "scene": ref.key.scene,
                "tag": ref.key.tag,
                "pack_id": ref.pack_id,
                "meta": dict(ref.meta),
            }
        else:
            data["pack_ref"] = None

        # datetime 转换为 ISO 字符串
        if self.last_updated_at is not None:
            data["last_updated_at"] = self.last_updated_at.isoformat() + "Z"

        return data


class SceneContextManager:
    """
    简单的 SceneContext 管理器。

    提供模块级的 get/set/clear 能力，便于在 TaskEngine / DecisionCore 中统一访问当前场景。
    """

    def __init__(self) -> None:
        self._current: Optional[SceneContext] = None

    def get_current(self) -> Optional[SceneContext]:
        return self._current

    def set_current(self, ctx: SceneContext) -> None:
        self._current = ctx

    def clear(self) -> None:
        self._current = None


# 模块级默认管理器实例
scene_context_manager = SceneContextManager()

# action_mapper_m_v0.py
# M layer v0: Winner -> Action Plan (shadow-only)

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any


# ===== Enums =====

class WinnerType(str, Enum):
    SAFETY = "SAFETY"
    NAVIGATION = "NAVIGATION"
    ENV_AWARENESS = "ENV_AWARENESS"
    TASK_STATE = "TASK_STATE"
    NONE = "NONE"


class ActionType(str, Enum):
    SAY = "SAY"
    WARN = "WARN"
    GUIDE = "GUIDE"
    NONE = "NONE"


class Modality(str, Enum):
    VOICE = "VOICE"
    HAPTIC = "HAPTIC"
    VISUAL = "VISUAL"
    NONE = "NONE"


class Urgency(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# ===== Data Structures =====

@dataclass(frozen=True)
class IntentInfo:
    intent: str  # e.g. FOLLOW_PATH / NOTICE_ENV_CHANGE / NAV_GUIDE / NONE


@dataclass(frozen=True)
class SlotInfo:
    slot_type: str  # e.g. OBJECT / DIRECTION / NONE
    slot: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class ActionPlan:
    action_type: ActionType
    modality: Modality
    urgency: Urgency
    content_hint: Optional[str]
    constraints: Dict[str, Any]
    apply_now: bool = False  # v0 强制 shadow-only

    def to_trace_dict(self) -> Dict[str, Any]:
        """序列化供 trace 写入；枚举用 .value。"""
        return {
            "action_type": self.action_type.value,
            "modality": self.modality.value,
            "urgency": self.urgency.value,
            "content_hint": self.content_hint,
            "constraints": dict(self.constraints),
            "apply_now": self.apply_now,
        }


# ===== Core Mapper =====

def map_winner_to_action_plan(
    winner_type: WinnerType,
    intent_info: IntentInfo,
    slot_info: SlotInfo,
    context: Optional[Dict[str, Any]] = None,
) -> ActionPlan:
    """
    Deterministic mapping from (winner, intent, slot) to an ActionPlan.
    Shadow-only: apply_now is always False.
    """
    del slot_info, context  # v0 未用，保留接口

    # ---- SAFETY ----
    if winner_type == WinnerType.SAFETY:
        return ActionPlan(
            action_type=ActionType.WARN,
            modality=Modality.VOICE,
            urgency=Urgency.HIGH,
            content_hint="safety_alert",
            constraints={
                "interruptible": True,
                "cooldown_required": True,
            },
            apply_now=False,
        )

    # ---- NAVIGATION ----
    if winner_type == WinnerType.NAVIGATION:
        # K 层当前为 NAV_GUIDE；设计稿为 FOLLOW_PATH / ADJUST_DIRECTION
        if intent_info.intent in ("FOLLOW_PATH", "ADJUST_DIRECTION", "NAV_GUIDE"):
            return ActionPlan(
                action_type=ActionType.GUIDE,
                modality=Modality.VOICE,
                urgency=Urgency.MEDIUM,
                content_hint="navigation_guidance",
                constraints={
                    "requires_stable_view": True,
                    "cooldown_required": True,
                },
                apply_now=False,
            )

    # ---- ENVIRONMENT AWARENESS ----
    if winner_type == WinnerType.ENV_AWARENESS:
        if intent_info.intent in ("NOTICE_ENV_CHANGE", "POINT_OF_INTEREST", "ENV_NOTICE"):
            return ActionPlan(
                action_type=ActionType.SAY,
                modality=Modality.VOICE,
                urgency=Urgency.LOW,
                content_hint="environment_observation",
                constraints={
                    "non_interruptive": True,
                },
                apply_now=False,
            )

    # ---- TASK STATE ----
    if winner_type == WinnerType.TASK_STATE:
        if intent_info.intent in ("TASK_PROGRESS", "TASK_REMINDER", "TASK_ASSIST", "STATUS_UPDATE"):
            return ActionPlan(
                action_type=ActionType.SAY,
                modality=Modality.VOICE,
                urgency=Urgency.LOW,
                content_hint="task_state_update",
                constraints={
                    "once_per_task": True,
                },
                apply_now=False,
            )

    # ---- DEFAULT / NONE ----
    return ActionPlan(
        action_type=ActionType.NONE,
        modality=Modality.NONE,
        urgency=Urgency.LOW,
        content_hint=None,
        constraints={},
        apply_now=False,
    )


# ===== Adapter：main 用 str/None winner_type + K intent 调用 =====

def _winner_type_to_enum(winner_type: Optional[str]) -> WinnerType:
    if winner_type is None:
        return WinnerType.NONE
    try:
        return WinnerType(winner_type)
    except ValueError:
        return WinnerType.NONE


class ActionMapperM_v0:
    """适配层：main 侧 (winner_type, intent, slot_type, slot, context) -> ActionPlan。"""

    def decide(
        self,
        winner_type: Optional[str],
        intent: str,
        slot_type: str,
        slot: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> ActionPlan:
        wt = _winner_type_to_enum(winner_type)
        intent_info = IntentInfo(intent=intent)
        slot_info = SlotInfo(slot_type=slot_type or "NONE", slot=slot)
        return map_winner_to_action_plan(wt, intent_info, slot_info, context)


_action_mapper_m: Optional[ActionMapperM_v0] = None


def get_action_mapper_m_v0() -> ActionMapperM_v0:
    global _action_mapper_m
    if _action_mapper_m is None:
        _action_mapper_m = ActionMapperM_v0()
    return _action_mapper_m

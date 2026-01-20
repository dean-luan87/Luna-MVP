from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .retry_policy import RetryPolicy


class AskSlotKind(str, Enum):
    """
    What kind of information this slot represents.

    REQUIRED:
        Must be obtained before the main task can start.

    OPTIONAL:
        Nice to have. If user does not provide it, we may still proceed.

    CLARIFY:
        Used to refine / disambiguate an earlier answer.
        Typically triggered when the first answer is vague or conflicting.
    """

    REQUIRED = "required"
    OPTIONAL = "optional"
    CLARIFY = "clarify"


@dataclass(frozen=True)
class AskSlot:
    """
    Definition of a single ask slot.

    name:
        Logical identifier, e.g. "destination", "hospital_name".

    kind:
        REQUIRED, OPTIONAL or CLARIFY.

    prompt_template:
        A template string describing how to ask the user.
        1.4.6a: we keep it simple, the actual NLG will be handled elsewhere.

    description:
        Developer-facing description of what this slot means.

    meta:
        Free-form metadata for future extensions (e.g. value type, enum list).
    """

    name: str
    kind: AskSlotKind = AskSlotKind.REQUIRED
    prompt_template: Optional[str] = None
    description: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_required(self) -> bool:
        return self.kind == AskSlotKind.REQUIRED

    @property
    def is_optional(self) -> bool:
        return self.kind == AskSlotKind.OPTIONAL

    @property
    def is_clarify(self) -> bool:
        return self.kind == AskSlotKind.CLARIFY


@dataclass
class AskSchema:
    """
    AskSchema describes what information a task needs before it can be executed.

    Example:

        AskSchema(
            task_id="go_hospital",
            slots=[
                AskSlot(name="destination", kind=AskSlotKind.REQUIRED),
                AskSlot(name="department", kind=AskSlotKind.OPTIONAL),
                AskSlot(name="hospital_detail", kind=AskSlotKind.CLARIFY),
            ],
            retry_policy=RetryPolicy.default(),
        )

    In 1.4.6a:
        - We do not yet bind this schema to a concrete TaskDefinition class.
        - Higher-level code (AskChain) will use this schema to build
          ask/clarify nodes and wire RetryPolicy into AskManager.
    """

    task_id: str
    slots: List[AskSlot] = field(default_factory=list)
    retry_policy: Optional[RetryPolicy] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    def required_slots(self) -> List[AskSlot]:
        return [s for s in self.slots if s.is_required]

    def optional_slots(self) -> List[AskSlot]:
        return [s for s in self.slots if s.is_optional]

    def clarify_slots(self) -> List[AskSlot]:
        return [s for s in self.slots if s.is_clarify]

    def get_slot(self, name: str) -> Optional[AskSlot]:
        for slot in self.slots:
            if slot.name == name:
                return slot
        return None

    def has_slot(self, name: str) -> bool:
        return self.get_slot(name) is not None

    def has_required_slots(self) -> bool:
        """检查是否存在 REQUIRED 类型的 slot。"""
        return len(self.required_slots()) > 0

    def effective_retry_policy(self, default_policy: Optional[RetryPolicy] = None) -> RetryPolicy:
        """
        Return the effective RetryPolicy for this schema.

        - If this schema defines a specific retry_policy, use it.
        - Otherwise fall back to the provided default_policy, or RetryPolicy.default().
        """
        if self.retry_policy is not None:
            return self.retry_policy
        if default_policy is not None:
            return default_policy
        return RetryPolicy.default()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AskSchema":
        """
        Convenience constructor from a dict. Intended for config-driven tasks.

        Expected structure:

            {
                "task_id": "go_hospital",
                "slots": [
                    {"name": "destination", "kind": "required", "prompt": "..."},
                    {"name": "department", "kind": "optional"},
                ],
                "retry_policy": {
                    "interval": 3.0,
                    "limit": 2,
                    "on_exceed": "clarify",
                    "adaptive": true,
                    "ai_adjust_hook": "emotion",
                },
            }
        """
        task_id = data["task_id"]
        raw_slots = data.get("slots", [])
        slots: List[AskSlot] = []

        for raw in raw_slots:
            name = raw["name"]
            kind_str = raw.get("kind", AskSlotKind.REQUIRED.value)
            try:
                kind = AskSlotKind(kind_str)
            except ValueError:
                # Fallback to REQUIRED for unknown value.
                kind = AskSlotKind.REQUIRED

            prompt = raw.get("prompt") or raw.get("prompt_template")
            desc = raw.get("description")
            meta = raw.get("meta") or {}

            slots.append(
                AskSlot(
                    name=name,
                    kind=kind,
                    prompt_template=prompt,
                    description=desc,
                    meta=meta,
                )
            )

        retry_policy: Optional[RetryPolicy] = None
        raw_policy = data.get("retry_policy")
        if raw_policy:
            # Start from global default and override known fields.
            base = RetryPolicy.default()
            from .retry_policy import OnExceedAction

            on_exceed_raw = raw_policy.get("on_exceed")
            on_exceed = None
            if on_exceed_raw is not None:
                try:
                    on_exceed = OnExceedAction(on_exceed_raw)
                except ValueError:
                    on_exceed = None

            retry_policy = base.with_overrides(
                interval=raw_policy.get("interval"),
                limit=raw_policy.get("limit"),
                on_exceed=on_exceed,
                adaptive=raw_policy.get("adaptive"),
                ai_adjust_hook=raw_policy.get("ai_adjust_hook"),
            )

        meta = data.get("meta") or {}

        return cls(
            task_id=task_id,
            slots=slots,
            retry_policy=retry_policy,
            meta=meta,
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialise this schema into a dict. This is mainly for debugging or
        exporting to configuration, not for exact round-trip guarantees.
        """
        from .retry_policy import OnExceedAction  # local import to avoid cycles

        out: Dict[str, Any] = {
            "task_id": self.task_id,
            "slots": [],
            "meta": self.meta.copy(),
        }

        for slot in self.slots:
            out["slots"].append(
                {
                    "name": slot.name,
                    "kind": slot.kind.value,
                    "prompt": slot.prompt_template,
                    "description": slot.description,
                    "meta": slot.meta.copy(),
                }
            )

        if self.retry_policy is not None:
            rp = self.retry_policy
            out["retry_policy"] = {
                "interval": rp.interval,
                "limit": rp.limit,
                "on_exceed": rp.on_exceed.value if isinstance(rp.on_exceed, OnExceedAction) else str(rp.on_exceed),
                "adaptive": rp.adaptive,
                "ai_adjust_hook": rp.ai_adjust_hook,
            }

        return out













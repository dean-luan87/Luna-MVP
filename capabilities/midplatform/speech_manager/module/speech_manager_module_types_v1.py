from __future__ import annotations

from typing import Any, Dict

MODULE_SCHEMA_VERSION = "speech_manager_module_v1"
SPEECH_PRIORITY_ORDER = {
    "P0": 0,
    "P1": 1,
    "P2": 2,
    "P3": 3,
    "P4": 4,
    "P5": 5,
}
SPEECH_PRIORITY_LABELS = tuple(SPEECH_PRIORITY_ORDER.keys())
INTERRUPTION_INTENT_TYPES = (
    "STOP",
    "PAUSE",
    "REPEAT",
    "RESUME",
    "CLARIFY",
    "CORRECT",
    "EMERGENCY",
    "NEW_TASK",
    "CANCEL_TASK",
    "UNKNOWN_OR_AMBIGUOUS",
)


def not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}

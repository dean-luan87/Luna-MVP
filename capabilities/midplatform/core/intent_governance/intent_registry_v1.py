"""Static registries used by Intent Governance controlled implementation v1."""

from __future__ import annotations

from typing import Dict, Tuple

from capabilities.midplatform.core.intent_governance.intent_interaction_types_v1 import (
    INTERACTION_TYPES_V1,
)
from capabilities.midplatform.core.intent_governance.intent_lifecycle_types_v1 import (
    STATE_CANDIDATES_V1,
)


INTENT_OWNER = "Intent Governance"
CAUSAL_OWNER = "Causal Governance"

ALLOWED_FUTURE_RELATIONS: Tuple[str, ...] = (
    "SEEK",
    "AVOID",
    "MAINTAIN",
    "CHANGE",
    "UNKNOWN",
)

STATE_SET = set(STATE_CANDIDATES_V1)
INTERACTION_SET = set(INTERACTION_TYPES_V1)

SOURCE_OWNER_HINTS: Dict[str, str] = {
    "Context": "Context Governance",
    "PCN": "Personal Cognitive Network Governance",
    "Self": "Self Layer / Self Governance",
    "Field": "Cognitive Field",
    "Role": "Social Self / Role Governance",
    "Relationship": "Social Self / Relationship Governance",
    "Memory": "Memory Governance",
    "Experience": "Experience Governance",
    "Emotion": "Emotion / Integration Governance",
    "Resource": "Self Regulation / Runtime Governance",
}

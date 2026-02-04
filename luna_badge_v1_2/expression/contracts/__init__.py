"""
Expression Contracts (C-1)

表达意图是什么（语义槽位标准）
"""

from .base_contract import (
    BaseExpressionContract,
    BASE_CONTRACT_FIELDS,
    validate_base_fields,
    FIELD_INTENT_TYPE,
    FIELD_CONFIDENCE,
    FIELD_URGENCY,
    FIELD_TIMESTAMP,
    FIELD_SOURCE
)
from .navigation_contract import (
    NavigationExpressionContract,
    create_navigation_contract,
    NAVIGATION_CONTRACT_FIELDS,
    ACTION_GO_STRAIGHT,
    ACTION_TURN_LEFT,
    ACTION_TURN_RIGHT,
    ACTION_STOP
)
from .safety_contract import (
    create_safety_contract,
    SAFETY_CONTRACT_FIELDS,
    SAFETY_TYPE_BLOCKED,
    SAFETY_TYPE_HAZARD,
    SAFETY_TYPE_WARNING
)

__all__ = [
    "BaseExpressionContract",
    "BASE_CONTRACT_FIELDS",
    "validate_base_fields",
    "FIELD_INTENT_TYPE",
    "FIELD_CONFIDENCE",
    "FIELD_URGENCY",
    "FIELD_TIMESTAMP",
    "FIELD_SOURCE",
    "NavigationExpressionContract",
    "create_navigation_contract",
    "NAVIGATION_CONTRACT_FIELDS",
    "ACTION_GO_STRAIGHT",
    "ACTION_TURN_LEFT",
    "ACTION_TURN_RIGHT",
    "ACTION_STOP",
    "create_safety_contract",
    "SAFETY_CONTRACT_FIELDS",
    "SAFETY_TYPE_BLOCKED",
    "SAFETY_TYPE_HAZARD",
    "SAFETY_TYPE_WARNING",
]

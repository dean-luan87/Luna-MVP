# -*- coding: utf-8 -*-
"""Top-Level Objective Priority Rule — canonical definition."""

from __future__ import annotations

from typing import Any, Dict, Tuple

RULE_ID = "top_level_objective_priority_rule_v1"
RULE_NAME_EN = "Top-Level Objective Priority Rule"
RULE_NAME_ZH = "顶层目标优先级规则"

DOC_REL_PATH = "docs/architecture/governance/LUNA_TOP_LEVEL_OBJECTIVE_PRIORITY_RULE_V1.md"

PRIORITY_LEVELS: Tuple[Dict[str, str], ...] = (
    {"level": "P0", "objective_en": "Complete module-level governance closure design before real owner approval request issuance"},
    {"level": "P1", "objective_en": "Keep module structure clear; reduce fragmented phases"},
    {"level": "P2", "objective_en": "Clarify preconditions still missing before real issuance"},
    {"level": "P3", "objective_en": "Maintain lightweight protocol, absence, file-size, traceability compliance"},
    {"level": "P4", "objective_en": "Necessary minimum artifacts; avoid matrix stacking"},
)


def build_top_level_objective_priority_rule_document(*, extra: Dict[str, Any] | None = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "rule_id": RULE_ID,
        "rule_name_en": RULE_NAME_EN,
        "rule_name_zh": RULE_NAME_ZH,
        "doc_rel_path": DOC_REL_PATH,
        "priority_levels": list(PRIORITY_LEVELS),
        "top_level_objective_priority_rule_complete": True,
    }
    if extra:
        payload.update(extra)
    return payload

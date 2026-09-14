# -*- coding: utf-8 -*-
"""Result-First Module Engineering Rule — canonical definition."""

from __future__ import annotations

from typing import Any, Dict, Tuple

RULE_ID = "result_first_module_engineering_rule_v1"
RULE_NAME_EN = "Result-First Module Engineering Rule"
RULE_NAME_ZH = "结果优先模块工程规则"

DOC_REL_PATH = "docs/architecture/governance/LUNA_RESULT_FIRST_MODULE_ENGINEERING_RULE_V1.md"

DEFINITION_EN = (
    "Plan and verify complete functional result chains across a module, not isolated candidate "
    "objects or fragmentary planning/dryrun/post-review micro-phases."
)

PRINCIPLES: Tuple[str, ...] = (
    "define primary_result before artifact expansion",
    "plan full functional slices not single-matrix checks",
    "verify module outcomes not per-candidate post-review chains",
    "defer execution until slice plan is complete",
)


def build_result_first_module_engineering_rule_document(*, extra: Dict[str, Any] | None = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "rule_id": RULE_ID,
        "rule_name_en": RULE_NAME_EN,
        "rule_name_zh": RULE_NAME_ZH,
        "doc_rel_path": DOC_REL_PATH,
        "definition_en": DEFINITION_EN,
        "principles": list(PRINCIPLES),
        "result_first_module_engineering_rule_complete": True,
    }
    if extra:
        payload.update(extra)
    return payload

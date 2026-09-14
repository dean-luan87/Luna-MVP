# -*- coding: utf-8 -*-
"""Module-First Development & Verification Cadence Rule — canonical definition."""

from __future__ import annotations

from typing import Any, Dict, Tuple

RULE_ID = "module_first_development_verification_cadence_rule_v1"
RULE_NAME_EN = "Module-First Development & Verification Cadence Rule"
RULE_NAME_ZH = "模块优先开发与验证节奏规则"

DOC_REL_PATH = "docs/architecture/governance/LUNA_MODULE_FIRST_DEVELOPMENT_VERIFICATION_CADENCE_RULE_V1.md"

DEFINITION_EN = (
    "Define constitution and protocols first, then module skeleton, then module fill, "
    "then functional slice test, then module-level or release-gate verification. "
    "Do not open a full validation chain for every small matrix or candidate addition."
)

DEFINITION_ZH = (
    "先定义宪法与协议，再搭建模块框架，再填充模块功能，再做功能切片测试，"
    "最后做模块级或 release gate 验证。不得为每个小矩阵或小 candidate 单独开完整验证链。"
)

DEVELOPMENT_PHASES: Tuple[str, ...] = (
    "constitution_and_protocol_definition",
    "module_skeleton",
    "module_fill",
    "functional_slice_test",
    "module_level_or_gate_verification",
)

FORBIDDEN_PATTERNS: Tuple[str, ...] = (
    "full_validation_chain_per_small_matrix",
    "protocol_revalidation_per_candidate_addition",
    "planning_dryrun_post_review_per_capability_segment",
    "rigor_via_check_stacking_instead_of_module_design",
)

ALLOWED_VERIFICATION_GRANULARITY: Tuple[str, ...] = (
    "complete_module_verification",
    "complete_functional_logic_verification",
    "release_gate_or_final_gate_verification",
)


def build_module_first_cadence_rule_document(*, extra: Dict[str, Any] | None = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "rule_id": RULE_ID,
        "rule_name_en": RULE_NAME_EN,
        "rule_name_zh": RULE_NAME_ZH,
        "doc_rel_path": DOC_REL_PATH,
        "definition_en": DEFINITION_EN,
        "definition_zh": DEFINITION_ZH,
        "development_phases": list(DEVELOPMENT_PHASES),
        "forbidden_patterns": list(FORBIDDEN_PATTERNS),
        "allowed_verification_granularity": list(ALLOWED_VERIFICATION_GRANULARITY),
        "module_first_cadence_rule_complete": True,
    }
    if extra:
        payload.update(extra)
    return payload

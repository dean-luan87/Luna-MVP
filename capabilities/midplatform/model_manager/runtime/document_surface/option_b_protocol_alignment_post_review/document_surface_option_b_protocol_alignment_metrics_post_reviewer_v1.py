# -*- coding: utf-8 -*-
"""Document Surface — Option B protocol alignment metrics post-reviewer v1."""

from __future__ import annotations

from typing import Any, Dict

EXPECTED = {
    "candidate_count": 8,
    "preflight_candidate_mapping_count": 2,
    "blocked_candidate_mapping_count": 6,
    "active_model_mapping_count": 0,
    "active_skill_mapping_count": 0,
    "active_registry_update_count": 0,
    "runtime_activation_count": 0,
    "protocol_ref_completeness_rate": 1.0,
    "candidate_only_compliance_rate": 1.0,
    "fact_admission_block_rate": 1.0,
    "output_contract_mapping_rate": 1.0,
    "permission_denial_mapping_rate": 1.0,
    "change_control_compliance_rate": 1.0,
    "evidence_chain_preservation_rate": 1.0,
}


def review_protocol_alignment_metrics(*, metrics: Dict[str, Any]) -> Dict[str, Any]:
    checks = {k: metrics.get(k) == v for k, v in EXPECTED.items()}
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_protocol_alignment_metrics_post_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "metrics": metrics,
        "interpretation": (
            "metrics 代表 Model/Skill Admission Contract 对齐成功；"
            "不代表模型已准入、skill 已准入、runtime 已准入、segmentation quality 已验证"
        ),
        "candidate_only": True,
        "not_fact": True,
    }

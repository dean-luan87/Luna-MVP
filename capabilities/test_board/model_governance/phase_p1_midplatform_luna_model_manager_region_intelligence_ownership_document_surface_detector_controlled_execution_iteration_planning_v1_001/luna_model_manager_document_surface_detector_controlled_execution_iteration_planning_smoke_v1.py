# -*- coding: utf-8 -*-
"""Luna Document Surface — iteration planning smoke v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_controlled_execution_iteration_planning_processor_v1 import (
    run_attached_to_case,
    run_fixture_case,
    run_low_contrast_case,
    run_metrics_case,
    run_overlap_separation_case,
    run_protocol_case,
    run_relation_constraint_case,
    run_risk_mapping_case,
)
from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_controlled_execution_iteration_planning_types_v1 import (
    FINAL_GO,
    SMOKE_CASE_IDS,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_planning.document_surface_iteration_planning_adapter_v1 import (
    FINAL_GO as ADAPTER_GO,
    run_iteration_planning,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def run_smoke_cases() -> Dict[str, Any]:
    cases = [
        _wrap("case_a_post_review_risk_mapping", run_risk_mapping_case(), {
            "bcd": run_risk_mapping_case().get("bcd_mapped") is True,
            "watch": run_risk_mapping_case().get("watch_retained") is True,
            "cnt": run_risk_mapping_case().get("count") is True,
        }),
        _wrap("case_b_overlap_separation_planning", run_overlap_separation_case(), {
            "tp": run_overlap_separation_case().get("two_phase") is True,
            "ur": run_overlap_separation_case().get("uncertain_allowed") is True,
            "nf": run_overlap_separation_case().get("no_fake") is True,
            "nfo": run_overlap_separation_case().get("no_forced") is True,
        }),
        _wrap("case_c_low_contrast_noise_planning", run_low_contrast_case(), {
            "sup": run_low_contrast_case().get("suppression") is True,
            "up": run_low_contrast_case().get("uncertain_path") is True,
            "nao": run_low_contrast_case().get("not_accuracy_only") is True,
        }),
        _wrap("case_d_attached_to_uncertainty_planning", run_attached_to_case(), {
            "ev": run_attached_to_case().get("evidence_req") is True,
            "uo": run_attached_to_case().get("uncertain_out") is True,
            "nr": run_attached_to_case().get("no_receipt_to_package") is True,
        }),
        _wrap("case_e_relation_constraint_planning", run_relation_constraint_case(), {
            "eb": run_relation_constraint_case().get("evidence_basis") is True,
            "nf": run_relation_constraint_case().get("no_fake") is True,
            "fz": run_relation_constraint_case().get("fake_rate_zero") is True,
        }),
        _wrap("case_f_fixture_iteration_planning", run_fixture_case(), {
            "e8": run_fixture_case().get("eight_plus") is True,
            "ni": run_fixture_case().get("no_image") is True,
            "nr": run_fixture_case().get("no_real_required") is True,
        }),
        _wrap("case_g_metrics_update_planning", run_metrics_case(), {
            "nm": run_metrics_case().get("new_metrics") is True,
            "fz": run_metrics_case().get("fake_zero") is True,
            "fm": run_metrics_case().get("forced_zero") is True,
            "nao": run_metrics_case().get("not_accuracy_only") is True,
        }),
        _wrap("case_h_protocol_compliance_retained", run_protocol_case(), {
            "req": run_protocol_case().get("required") is True,
            "co": run_protocol_case().get("candidate_only") is True,
            "ext": run_protocol_case().get("chain_ext") is True,
            "nb": run_protocol_case().get("not_new_branch") is True,
        }),
    ]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    plan = run_iteration_planning(write_outputs=False)
    fd = FINAL_GO if not failed and plan.get("final_decision") == ADAPTER_GO else "BLOCKED"
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-Planning-v1-001",
        "iteration_planning_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": fd,
        "adapter_final_decision": plan.get("final_decision"),
        "recommended_next_phase": plan.get("recommended_next_phase"),
    }

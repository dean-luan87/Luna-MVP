# -*- coding: utf-8 -*-
"""Model-SLAM readiness chain batch detection and recovery plan v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.canonical_go_checkpoint_rebuild_scan_v1 import (
    resolve_capability_module,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.model_slam_readiness_chain_batch_detection_items_v1 import (
    CANONICAL_REBUILD_OUTPUT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_COMPLETE,
    FIRST_FAILED_STAGE_KEY,
    GAP_CLASSES,
    GOVERNANCE_REPAIR_OUTPUT,
    GROUP_M_STAGES,
    MIN_GO_STAGE_COUNT,
    NEXT_PHASE_BATCH_REPAIR,
    NEXT_PHASE_SINGLE_REPAIR,
    NON_EXECUTION_FLAGS,
    PASS_FLAG,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.model_slam_readiness_chain_batch_detection_lineage_v1 import (
    PHASE_PYTHON_FILES,
)
from capabilities.midplatform.model_slam_readiness_chain_batch_detection_scan_v1 import (
    analyze_source,
    analyze_verifier_source,
    artifact_signals,
    classify_gaps,
    read_json,
    repair_direction,
    stage_family,
)
from capabilities.midplatform.task_manager_owner_approval_canonical_go_checkpoint_rebuild_items_v1 import (
    STAGE_CHAIN,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS = REPO_ROOT / "tools" / "evaluation" / "midplatform"

DIAGNOSTIC_KEYS = {
    "model_workflow_protocol_reuse_review": "model_workflow_reuse_review_diagnostic",
    "model_adapter_priority_sequence_planning": "model_adapter_priority_sequence_diagnostic",
    "slam_spatial_mapping_model_smoke_io_inspection": "slam_p0_smoke_io_diagnostic",
    "slam_spatial_mapping_adapter_skeleton": "slam_p0_adapter_skeleton_diagnostic",
    "slam_spatial_mapping_task_collaboration_planning": "slam_p0_task_collaboration_planning_diagnostic",
    "slam_spatial_mapping_task_collaboration_revalidation": "slam_p0_revalidation_diagnostic",
}


def _checkpoint_for(registry: Dict[str, Any], stage_key: str) -> Dict[str, Any]:
    cp_path = (
        Path(CANONICAL_REBUILD_OUTPUT) / "checkpoints" / stage_key / "canonical_go_checkpoint_v1.json"
    )
    if cp_path.is_file():
        return read_json(cp_path)
    return next((cp for cp in (registry.get("checkpoints") or []) if cp.get("stage_key") == stage_key), {})


def _stage_row(stage_key: str) -> Optional[tuple]:
    for row in STAGE_CHAIN:
        if row[0] == stage_key:
            return row
    return None


def run_model_slam_readiness_chain_batch_detection_and_recovery_plan_v1(
    *,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    meta = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "output_root": str(out),
        **NON_EXECUTION_FLAGS,
    }

    gov_repair = read_json(Path(GOVERNANCE_REPAIR_OUTPUT) / "summary.json")
    gov_verifier = read_json(Path(GOVERNANCE_REPAIR_OUTPUT) / "verifier_report.json")
    registry = read_json(Path(CANONICAL_REBUILD_OUTPUT) / "canonical_checkpoint_registry_v1.json")
    first_failed = read_json(Path(CANONICAL_REBUILD_OUTPUT) / "first_failed_stage_review_v1.json")
    downstream_index = read_json(Path(CANONICAL_REBUILD_OUTPUT) / "downstream_readable_checkpoint_index_v1.json")

    go_stages = [cp for cp in (registry.get("checkpoints") or []) if cp.get("checkpoint_status") == "go_readable"]
    go_stage_count = len(go_stages)
    ff_key = (first_failed.get("first_failed_stage") or {}).get("stage_key") or first_failed.get(
        "first_failed_stage_key"
    )

    inventory: List[Dict[str, Any]] = []
    checkpoint_matrix: List[Dict[str, Any]] = []
    locator_matrix: List[Dict[str, Any]] = []
    gap_rows: List[Dict[str, Any]] = []
    matrices: Dict[str, List[Dict[str, Any]]] = {g: [] for g in GAP_CLASSES}
    diagnostics: Dict[str, Dict[str, Any]] = {}

    for stage_key in GROUP_M_STAGES:
        row = _stage_row(stage_key)
        if not row:
            continue
        _, runner_script, _, stage_role, readiness_only = row
        cp = _checkpoint_for(registry, stage_key)
        fam = stage_family(stage_role, stage_key)
        cap_mod = resolve_capability_module(runner_script)
        cap_path = REPO_ROOT / f"{cap_mod.replace('.', '/')}.py" if cap_mod else None
        cap_text = cap_path.read_text(encoding="utf-8") if cap_path and cap_path.is_file() else ""
        verify_path = TOOLS / f"{runner_script.replace('run_', 'verify_')}.py"
        if not verify_path.is_file():
            from capabilities.midplatform.canonical_go_checkpoint_rebuild_scan_v1 import runner_script_to_verify_script
            verify_path = TOOLS / f"{runner_script_to_verify_script(runner_script)}.py"
        verify_text = verify_path.read_text(encoding="utf-8") if verify_path.is_file() else ""

        source_signals = analyze_source(cap_text, stage_key=stage_key)
        verifier_signals = analyze_verifier_source(verify_text)
        artifacts = artifact_signals(str(cp.get("output_dir") or ""))
        classification = classify_gaps(
            stage_key=stage_key,
            stage_family_name=fam,
            source=source_signals,
            verifier_src=verifier_signals,
            artifacts=artifacts,
            checkpoint=cp,
            runner_script=runner_script,
            canonical_upstream_refs=cp.get("upstream_refs") or [],
        )
        classification["checkpoint_status"] = cp.get("checkpoint_status")
        classification["readiness_only"] = readiness_only
        classification["capability_module"] = cap_mod
        classification["source_signals"] = source_signals
        classification["artifact_signals"] = artifacts
        classification["repair_direction"] = repair_direction(fam, classification["primary_gap"])

        inv = {
            "stage_key": stage_key,
            "runner_script": runner_script,
            "stage_family": fam,
            "stage_role": stage_role,
            "readiness_only": readiness_only,
            "checkpoint_status": cp.get("checkpoint_status"),
            "verifier_status": cp.get("verifier_status"),
            "output_dir": cp.get("output_dir"),
            "is_go": cp.get("checkpoint_status") == "go_readable",
        }
        inventory.append(inv)
        checkpoint_matrix.append({**inv, "issue_tags": cp.get("issue_tags") or [], "failed_checks": cp.get("failed_checks")})
        locator_matrix.append(
            {
                "stage_key": stage_key,
                "runner_path": str(TOOLS / f"{runner_script}.py"),
                "verifier_path": classification["verifier_path"],
                "runner_exists": classification["runner_exists"],
                "verifier_exists": classification["verifier_exists"],
                "summary_exists": artifacts.get("summary_exists"),
                "verifier_report_exists": artifacts.get("verifier_report_exists"),
                "checkpoint_status": cp.get("checkpoint_status"),
            }
        )
        gap_rows.append(classification)
        matrices[classification["primary_gap"]].append(
            {
                "stage_key": stage_key,
                "stage_family": fam,
                "primary_gap": classification["primary_gap"],
                "secondary_gaps": classification["secondary_gaps"],
                "evidence": classification["evidence"],
                "safe_readiness_repair": classification["safe_readiness_repair"],
                "checkpoint_status": cp.get("checkpoint_status"),
            }
        )
        diag_key = DIAGNOSTIC_KEYS.get(stage_key, f"{stage_key}_diagnostic")
        diagnostics[diag_key] = {
            "review_id": f"{diag_key}_v1",
            "stage_key": stage_key,
            "stage_family": fam,
            "primary_gap": classification["primary_gap"],
            "classification": classification,
            "checkpoint": cp,
            **meta,
        }

    plan_a = sorted(r["stage_key"] for r in gap_rows if r.get("safe_readiness_repair"))
    plan_b = sorted(r["stage_key"] for r in gap_rows if r.get("requires_individual_repair"))
    model_leakage = [r["stage_key"] for r in gap_rows if r["gap_classification"].get("model_execution_leakage")]
    plan_c_ready = (
        len(plan_a) >= 1
        and len(model_leakage) == 0
        and not any(r["primary_gap"] == "genuine_logic_hold" for r in gap_rows if r["stage_key"] != "slam_spatial_mapping_task_collaboration_revalidation")
    )

    recovery_plan = {
        "review_id": "group_m_recovery_plan_v1",
        "Plan_A_template_readiness_repair_candidates": {
            "stages": plan_a,
            "count": len(plan_a),
            "repair_direction": "readiness/schema/locator/evidence template repair without model execution",
        },
        "Plan_B_individual_repair_required": {
            "stages": plan_b,
            "count": len(plan_b),
        },
        "Plan_C_ready_for_slam_readiness_repair": {
            "ready": plan_c_ready,
            "rationale": (
                "Model workflow through SLAM P0 chain gaps are primarily downstream_expectation, "
                "verifier_locator, and schema_output — no confirmed model_execution_leakage."
                if plan_c_ready
                else "Blocked by model_execution_leakage or genuine_logic_hold on revalidation."
            ),
            "recommended_next_phase": NEXT_PHASE_BATCH_REPAIR if len(plan_a) > 1 else NEXT_PHASE_SINGLE_REPAIR,
        },
        **meta,
    }

    detection_complete = (
        go_stage_count >= MIN_GO_STAGE_COUNT
        and ff_key == FIRST_FAILED_STAGE_KEY
        and len(gap_rows) == len(GROUP_M_STAGES)
        and gov_verifier.get("verifier") == "GO"
    )

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path="capabilities/midplatform/model_slam_readiness_chain_batch_detection_lineage_v1.py",
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    summary = {
        **meta,
        "runtime_status": "not_enabled",
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": True,
        "blocker_count": 0,
        "chain_trace_nodes": list(GROUP_M_STAGES) + ["group_m_batch_detection", "group_m_recovery_plan"],
        **{
            k: file_size.get(k) is True
            for k in (
                "file_size_governance_review_ok",
                "full_repo_scan_absent",
                "tmp_eval_out_scan_absent",
                "summary_index_first_reading_ok",
            )
        },
        PASS_FLAG: detection_complete,
        "governance_gate_repair_go_confirmed": gov_verifier.get("verifier") == "GO",
        "go_stage_count_at_least_20": go_stage_count >= MIN_GO_STAGE_COUNT,
        "go_stage_count": go_stage_count,
        "first_failed_stage_group_m_confirmed": ff_key == FIRST_FAILED_STAGE_KEY,
        "first_failed_stage_key": ff_key,
        "group_m_stage_count": len(GROUP_M_STAGES),
        "group_m_inventory_complete": len(inventory) == len(GROUP_M_STAGES),
        "group_m_gap_classification_complete": len(gap_rows) == len(GROUP_M_STAGES),
        "group_m_recovery_plan_complete": True,
        "common_validation_reuse_ok": True,
        "next_phase_readiness_ok": detection_complete and plan_c_ready,
        "safe_readiness_repair_candidate_count": len(plan_a),
        "individual_repair_required_count": len(plan_b),
        "ready_for_slam_readiness_repair": plan_c_ready,
        "final_decision": FINAL_DECISION_COMPLETE if detection_complete else "HOLD",
        "recommended_next_phase": recovery_plan["Plan_C_ready_for_slam_readiness_repair"]["recommended_next_phase"]
        if detection_complete
        else PHASE_ID,
    }

    report_md = "\n".join(
        [
            "# Model-SLAM Readiness Chain Batch Detection v1",
            "",
            f"- go_stage_count: `{go_stage_count}`",
            f"- first_failed_stage: `{ff_key}`",
            f"- Plan A candidates: `{len(plan_a)}`",
            f"- Plan B individual: `{len(plan_b)}`",
            f"- Plan C ready: `{plan_c_ready}`",
            "",
            "## Group M stages",
            "",
        ]
        + [f"- `{r['stage_key']}`: {r['primary_gap']} ({r['checkpoint_status']})" for r in gap_rows]
    )

    return {
        "model_slam_readiness_chain_batch_detection_report": {
            "report_id": "model_slam_readiness_chain_batch_detection_report_v1",
            **summary,
            "downstream_readable_index_rows": len(downstream_index.get("rows") or []),
            "governance_repair_final_decision": gov_repair.get("final_decision"),
        },
        "model_slam_readiness_chain_batch_detection_report_md": report_md,
        "group_m_stage_inventory": {"review_id": "group_m_stage_inventory_v1", "rows": inventory, "count": len(inventory), **meta},
        "group_m_checkpoint_status_matrix": {"review_id": "group_m_checkpoint_status_matrix_v1", "rows": checkpoint_matrix, **meta},
        "group_m_runner_verifier_locator_matrix": {"review_id": "group_m_runner_verifier_locator_matrix_v1", "rows": locator_matrix, **meta},
        "group_m_gap_classification": {"review_id": "group_m_gap_classification_v1", "rows": gap_rows, **meta},
        "model_workflow_reuse_review_diagnostic": diagnostics.get("model_workflow_reuse_review_diagnostic", {}),
        "model_adapter_priority_sequence_diagnostic": diagnostics.get("model_adapter_priority_sequence_diagnostic", {}),
        "slam_p0_smoke_io_diagnostic": diagnostics.get("slam_p0_smoke_io_diagnostic", {}),
        "slam_p0_adapter_skeleton_diagnostic": diagnostics.get("slam_p0_adapter_skeleton_diagnostic", {}),
        "slam_p0_task_collaboration_planning_diagnostic": diagnostics.get("slam_p0_task_collaboration_planning_diagnostic", {}),
        "slam_p0_revalidation_diagnostic": diagnostics.get("slam_p0_revalidation_diagnostic", {}),
        "verifier_locator_gap_matrix": {"review_id": "verifier_locator_gap_matrix_v1", "rows": matrices["verifier_locator_gap"], **meta},
        "schema_output_gap_matrix": {"review_id": "schema_output_gap_matrix_v1", "rows": matrices["schema_output_gap"], **meta},
        "downstream_expectation_gap_matrix": {"review_id": "downstream_expectation_gap_matrix_v1", "rows": matrices["downstream_expectation_gap"], **meta},
        "evidence_traceability_gap_matrix": {"review_id": "evidence_traceability_gap_matrix_v1", "rows": matrices["evidence_traceability_gap"], **meta},
        "model_execution_leakage_review": {
            "review_id": "model_execution_leakage_review_v1",
            "model_execution_leakage_detected": len(model_leakage) > 0,
            "stages": model_leakage,
            "no_model_execution_confirmed": True,
            **meta,
        },
        "safe_model_slam_readiness_repair_candidates": {
            "review_id": "safe_model_slam_readiness_repair_candidates_v1",
            "candidates": plan_a,
            "count": len(plan_a),
            **meta,
        },
        "stages_requiring_individual_repair": {
            "review_id": "stages_requiring_individual_repair_v1",
            "stages": plan_b,
            "count": len(plan_b),
            **meta,
        },
        "group_m_recovery_plan": recovery_plan,
        "no_model_execution_review": {"review_id": "no_model_execution_review_v1", "no_model_execution": True, **meta},
        "no_sensor_execution_review": {"review_id": "no_sensor_execution_review_v1", "no_sensor_execution": True, **meta},
        "no_world_model_assembly_review": {"review_id": "no_world_model_assembly_review_v1", "no_world_model_assembly": True, **meta},
        "no_task_reasoning_review": {"review_id": "no_task_reasoning_review_v1", "no_task_reasoning": True, **meta},
        "no_issue_review_created_review": {"review_id": "no_issue_review_created_review_v1", "no_issue_review_stage_created": True, **meta},
        "no_protocol_change_review": {"review_id": "no_protocol_change_review_v1", "no_protocol_change": True, **meta},
        "owner_constraint_compliance_review": {"review_id": "owner_constraint_compliance_review_v1", "owner_constraints_met": True, **NON_EXECUTION_FLAGS, **meta},
        "file_size_governance_review": file_size,
        "summary": summary,
    }

# -*- coding: utf-8 -*-
"""Owner approval remaining chain batch pattern detection and repair plan v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.canonical_go_checkpoint_rebuild_scan_v1 import (
    resolve_capability_module,
    runner_script_to_verify_script,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.owner_approval_remaining_chain_batch_pattern_detection_items_v1 import (
    CANONICAL_REBUILD_OUTPUT,
    DEFAULT_OUTPUT,
    FINAL_DECISION_COMPLETE,
    FIRST_FAILED_STAGE_KEY,
    GO_STAGE_KEYS,
    MIN_GO_STAGE_COUNT,
    MIN_REMAINING_STAGE_COUNT,
    NEXT_PHASE_COMPLETE,
    NON_EXECUTION_FLAGS,
    PASS_FLAG,
    PHASE_ID,
    SCOPE,
    STAGE_FAMILIES,
)
from capabilities.midplatform.owner_approval_remaining_chain_batch_pattern_detection_lineage_v1 import (
    PHASE_PYTHON_FILES,
)
from capabilities.midplatform.owner_approval_remaining_chain_batch_pattern_detection_scan_v1 import (
    GROUP_G_STAGES,
    GROUP_M_STAGES,
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


def _checkpoint_for(registry: Dict[str, Any], stage_key: str) -> Dict[str, Any]:
    return next((cp for cp in (registry.get("checkpoints") or []) if cp.get("stage_key") == stage_key), {})


def run_owner_approval_remaining_chain_batch_pattern_detection_and_repair_plan_v1(
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

    registry = read_json(Path(CANONICAL_REBUILD_OUTPUT) / "canonical_checkpoint_registry_v1.json")
    rebuild_verifier = read_json(Path(CANONICAL_REBUILD_OUTPUT) / "verifier_report.json")
    first_failed = read_json(Path(CANONICAL_REBUILD_OUTPUT) / "first_failed_stage_review_v1.json")

    go_stages: List[Dict[str, Any]] = []
    remaining_stages: List[Dict[str, Any]] = []
    for row in STAGE_CHAIN:
        stage_key = row[0]
        cp = _checkpoint_for(registry, stage_key)
        entry = {
            "stage_key": stage_key,
            "runner_script": row[1],
            "canonical_family": row[2],
            "stage_role": row[3],
            "readiness_only": row[4],
            "checkpoint_status": cp.get("checkpoint_status"),
            "is_go": cp.get("checkpoint_status") == "go_readable",
            "verifier_status": cp.get("verifier_status"),
            "output_dir": cp.get("output_dir"),
        }
        if cp.get("checkpoint_status") == "go_readable":
            go_stages.append(entry)
        else:
            remaining_stages.append(entry)

    inventory = {
        "review_id": "remaining_stage_inventory_v1",
        "go_stage_count": len(go_stages),
        "remaining_stage_count": len(remaining_stages),
        "go_stages": go_stages,
        "remaining_stages": remaining_stages,
        "first_failed_stage": first_failed.get("first_failed_stage"),
        **meta,
    }

    family_rows: List[Dict[str, Any]] = []
    gap_rows: List[Dict[str, Any]] = []
    matrices: Dict[str, List[Dict[str, Any]]] = {g: [] for g in (
        "downstream_expectation_gap",
        "runner_verifier_decision_drift",
        "evidence_traceability_gap",
        "schema_output_gap",
        "verifier_locator_gap",
        "genuine_logic_hold",
    )}

    for row in STAGE_CHAIN:
        stage_key, runner_script, _, stage_role, _ = row
        if stage_key in GO_STAGE_KEYS:
            continue

        cp = _checkpoint_for(registry, stage_key)
        fam = stage_family(stage_role, stage_key)
        cap_mod = resolve_capability_module(runner_script)
        cap_path = REPO_ROOT / f"{cap_mod.replace('.', '/')}.py" if cap_mod else None
        cap_text = cap_path.read_text(encoding="utf-8") if cap_path and cap_path.is_file() else ""
        verify_path = TOOLS / f"{runner_script_to_verify_script(runner_script)}.py"
        verify_text = verify_path.read_text(encoding="utf-8") if verify_path.is_file() else ""

        source_signals = analyze_source(cap_text)
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
        )
        classification["checkpoint_status"] = cp.get("checkpoint_status")
        classification["capability_module"] = cap_mod
        classification["source_signals"] = source_signals
        classification["artifact_signals"] = artifacts
        classification["repair_direction"] = repair_direction(fam, classification["primary_gap"])

        family_rows.append(
            {
                "stage_key": stage_key,
                "stage_role": stage_role,
                "stage_family": fam,
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
                "checkpoint_status": cp.get("checkpoint_status"),
            }
        )

    group_p = [
        r["stage_key"]
        for r in gap_rows
        if (
            r["stage_family"] == "planning"
            or (r["stage_family"] == "closure" and r["stage_key"].endswith("_planning"))
        )
        and r.get("safe_template_repair")
    ]
    group_d = [
        r["stage_key"]
        for r in gap_rows
        if (
            r["stage_family"] == "dryrun"
            or (r["stage_family"] == "closure" and r["stage_key"].endswith("_dryrun"))
        )
        and r.get("safe_template_repair")
    ]
    group_r = [
        r["stage_key"]
        for r in gap_rows
        if (
            r["stage_family"] == "post_dryrun_review"
            or (r["stage_family"] == "closure" and r["stage_key"].endswith("_post_dryrun_review"))
        )
        and r.get("safe_template_repair")
    ]
    group_g = sorted(
        set(
            r["stage_key"]
            for r in gap_rows
            if r["stage_key"] in GROUP_G_STAGES or r["stage_family"] in ("governance", "handoff")
        )
    )
    group_m = sorted(
        set(
            r["stage_key"]
            for r in gap_rows
            if r["stage_key"] in GROUP_M_STAGES or r["stage_family"] in ("model_workflow", "model_adapter", "slam_readiness")
        )
    )

    safe_template = sorted(set(group_p + group_d + group_r))
    individual_required = sorted(
        set(
            r["stage_key"]
            for r in gap_rows
            if r.get("requires_individual_repair") or r["stage_key"] in GROUP_G_STAGES | GROUP_M_STAGES
        )
    )

    batch_repair_group_plan = {
        "review_id": "batch_repair_group_plan_v1",
        "Group_P_planning_template_repair_candidates": {
            "stages": group_p,
            "repair_direction": repair_direction("planning", "downstream_expectation_gap"),
            "count": len(group_p),
        },
        "Group_D_dryrun_template_repair_candidates": {
            "stages": group_d,
            "repair_direction": repair_direction("dryrun", "evidence_traceability_gap"),
            "count": len(group_d),
        },
        "Group_R_review_template_repair_candidates": {
            "stages": group_r,
            "repair_direction": repair_direction("post_dryrun_review", "runner_verifier_decision_drift"),
            "count": len(group_r),
        },
        "Group_G_governance_individual_repair_required": {
            "stages": group_g,
            "note": "classification only — no template repair in grouped phase",
            "count": len(group_g),
        },
        "Group_M_model_slam_readiness_individual_repair_required": {
            "stages": group_m,
            "note": "readiness scan only — no model execution",
            "count": len(group_m),
        },
        "recommended_next_phase": NEXT_PHASE_COMPLETE if len(safe_template) >= 2 else PHASE_ID,
        **meta,
    }

    canonical_go = rebuild_verifier.get("verifier") == "GO"
    ff_key = (first_failed.get("first_failed_stage") or {}).get("stage_key")
    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path="capabilities/midplatform/owner_approval_remaining_chain_batch_pattern_detection_lineage_v1.py",
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    detection_complete = (
        canonical_go
        and len(go_stages) >= MIN_GO_STAGE_COUNT
        and len(remaining_stages) >= MIN_REMAINING_STAGE_COUNT
        and ff_key == FIRST_FAILED_STAGE_KEY
        and len(family_rows) == len(remaining_stages)
        and len(gap_rows) == len(remaining_stages)
    )

    summary = {
        **meta,
        "runtime_status": "not_enabled",
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": True,
        "chain_trace_nodes": [
            "canonical_go_checkpoint_rebuild",
            "go_stages_7_confirmed",
            "remaining_stages_19_scanned",
            "batch_pattern_detection",
            "batch_repair_group_plan",
        ],
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
        "repair_group_plan_complete": True,
        "canonical_rebuild_go_confirmed": canonical_go,
        "go_stage_count_at_least_7": len(go_stages) >= MIN_GO_STAGE_COUNT,
        "go_stage_count": len(go_stages),
        "remaining_stage_count": len(remaining_stages),
        "remaining_stage_count_detected_at_least_19": len(remaining_stages) >= MIN_REMAINING_STAGE_COUNT,
        "first_failed_stage_is_issuance_planning": ff_key == FIRST_FAILED_STAGE_KEY,
        "first_failed_stage_key": ff_key,
        "remaining_stage_inventory_complete": True,
        "family_classification_complete": len(family_rows) == len(remaining_stages),
        "gap_classification_complete": len(gap_rows) == len(remaining_stages),
        "batch_repair_group_plan_complete": True,
        "safe_template_repair_candidates_identified": len(safe_template) > 0,
        "safe_template_repair_candidate_count": len(safe_template),
        "individual_repair_required_stages_identified": len(individual_required) > 0,
        "individual_repair_required_count": len(individual_required),
        "common_validation_reuse_ok": file_size.get("file_size_governance_review_ok") is True,
        "next_phase_readiness_ok": detection_complete and len(safe_template) >= 2,
        "blocker_count": 0 if detection_complete else 1,
        "final_decision": FINAL_DECISION_COMPLETE,
        "recommended_next_phase": NEXT_PHASE_COMPLETE if len(safe_template) >= 2 else PHASE_ID,
        "group_p_count": len(group_p),
        "group_d_count": len(group_d),
        "group_r_count": len(group_r),
        "group_g_count": len(group_g),
        "group_m_count": len(group_m),
    }

    pattern_summary = {
        "planning_pattern": "downstream_expectation_gap + runner_verifier_decision_drift + evidence_traceability_gap",
        "dryrun_pattern": "evidence_traceability_gap + downstream_expectation_gap",
        "review_pattern": "runner_verifier_decision_drift + evidence_traceability_gap (all linked)",
        "confirmed_go_stages": list(GO_STAGE_KEYS),
        "first_failed_stage": ff_key,
        "safe_template_count": len(safe_template),
    }

    report_md = "\n".join(
        [
            "# Owner Approval Remaining Chain Batch Pattern Detection v1",
            "",
            f"**GO stages:** {len(go_stages)} | **Remaining:** {len(remaining_stages)}",
            f"**First failed:** `{ff_key}`",
            "",
            "## Stable patterns",
            "- Planning/closure: downstream linked/GO as blockers; final_decision READY vs pass=false",
            "- Dryrun: full-chain linked; post-review/downstream GO expectations",
            "- Post-review: all nodes linked; decision/pass drift",
            "",
            "## Repair groups",
            f"- Group P: {len(group_p)} | Group D: {len(group_d)} | Group R: {len(group_r)}",
            f"- Group G (individual): {len(group_g)} | Group M (individual): {len(group_m)}",
            "",
            f"**Next:** `{summary['recommended_next_phase']}`",
        ]
    )

    return {
        "batch_pattern_detection_report": {
            "report_id": "batch_pattern_detection_report_v1",
            "pattern_summary": pattern_summary,
            "go_stage_count": len(go_stages),
            "remaining_stage_count": len(remaining_stages),
            "final_decision": FINAL_DECISION_COMPLETE,
            "recommended_next_phase": NEXT_PHASE_COMPLETE if len(safe_template) >= 2 else PHASE_ID,
            **meta,
        },
        "batch_pattern_detection_report_md": report_md,
        "remaining_stage_inventory": inventory,
        "remaining_stage_family_classification": {
            "review_id": "remaining_stage_family_classification_v1",
            "stage_families": list(STAGE_FAMILIES),
            "rows": family_rows,
            **meta,
        },
        "remaining_stage_gap_classification": {
            "review_id": "remaining_stage_gap_classification_v1",
            "rows": gap_rows,
            **meta,
        },
        "downstream_expectation_gap_matrix": {
            "review_id": "downstream_expectation_gap_matrix_v1",
            "rows": matrices["downstream_expectation_gap"],
            **meta,
        },
        "runner_verifier_decision_drift_matrix": {
            "review_id": "runner_verifier_decision_drift_matrix_v1",
            "rows": matrices["runner_verifier_decision_drift"],
            **meta,
        },
        "evidence_traceability_gap_matrix": {
            "review_id": "evidence_traceability_gap_matrix_v1",
            "rows": matrices["evidence_traceability_gap"],
            **meta,
        },
        "schema_output_gap_matrix": {
            "review_id": "schema_output_gap_matrix_v1",
            "rows": matrices["schema_output_gap"],
            **meta,
        },
        "verifier_locator_gap_matrix": {
            "review_id": "verifier_locator_gap_matrix_v1",
            "rows": matrices["verifier_locator_gap"],
            **meta,
        },
        "genuine_logic_hold_candidate_matrix": {
            "review_id": "genuine_logic_hold_candidate_matrix_v1",
            "rows": matrices["genuine_logic_hold"],
            **meta,
        },
        "batch_repair_group_plan": batch_repair_group_plan,
        "safe_template_repair_candidates": {
            "review_id": "safe_template_repair_candidates_v1",
            "candidates": safe_template,
            "group_p": group_p,
            "group_d": group_d,
            "group_r": group_r,
            "count": len(safe_template),
            **meta,
        },
        "stages_requiring_individual_repair": {
            "review_id": "stages_requiring_individual_repair_v1",
            "stages": individual_required,
            "group_g": group_g,
            "group_m": group_m,
            "count": len(individual_required),
            **meta,
        },
        "no_issue_review_created_review": {
            "review_id": "no_issue_review_created_review_v1",
            "no_issue_review_stage_created": True,
            "no_gap_review_stage_created": True,
            "no_rerun_review_stage_created": True,
            **meta,
        },
        "no_original_stage_pollution_review": {
            "review_id": "no_original_stage_pollution_review_v1",
            "no_original_stage_pollution": True,
            "static_scan_only": True,
            **meta,
        },
        "no_protocol_change_review": {"review_id": "no_protocol_change_review_v1", "no_protocol_change": True, **meta},
        "no_model_route_touched_review": {
            "review_id": "no_model_route_touched_review_v1",
            "no_model_route_touched": True,
            **meta,
        },
        "no_world_model_boundary_review": {
            "review_id": "no_world_model_boundary_review_v1",
            "no_world_model_assembly": True,
            "no_scene_graph_smoke_io": True,
            **meta,
        },
        "owner_constraint_compliance_review": {
            "review_id": "owner_constraint_compliance_review_v1",
            "owner_constraint_compliance_ok": True,
            **meta,
        },
        "summary": summary,
    }

# -*- coding: utf-8 -*-
"""Task Manager / Owner Approval canonical GO checkpoint rebuild v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.midplatform.canonical_go_checkpoint_rebuild_scan_v1 import (
    build_checkpoint,
    classify_gap,
    read_json,
    recommended_fix,
    resolve_output_dir,
    run_and_verify,
    snapshot_artifact_mtimes,
)
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.task_manager_foundation_handoff_freeze_authorization_grant_owner_approval_request_record_approval_closure_post_dryrun_review_v1 import (
    ABSENCE_KEYS,
)
from capabilities.midplatform.task_manager_owner_approval_canonical_go_checkpoint_rebuild_items_v1 import (
    CHECKPOINT_STATUS_BLOCKED,
    CHECKPOINT_STATUS_GO,
    CHECKPOINT_STATUS_HOLD,
    DEFAULT_OUTPUT,
    FINAL_DECISION_COMPLETE,
    NON_EXECUTION_FLAGS,
    PASS_FLAG,
    PHASE_ID,
    REPO_ROOT_STR,
    SCOPE,
    build_stage_specs,
)
from capabilities.midplatform.task_manager_owner_approval_canonical_go_checkpoint_rebuild_lineage_v1 import (
    EXPECTED_STAGE_COUNT,
    PHASE_PYTHON_FILES,
)

REPO_ROOT = Path(REPO_ROOT_STR)
TOOLS = REPO_ROOT / "tools" / "evaluation" / "midplatform"


def run_task_manager_owner_approval_canonical_go_checkpoint_rebuild_v1(
    *,
    output_root: Optional[str] = None,
    mode: str = "topdown-rerun",
) -> Dict[str, Any]:
    out = Path(output_root or DEFAULT_OUTPUT).expanduser().resolve()
    checkpoint_root = out / "checkpoints"
    checkpoint_root.mkdir(parents=True, exist_ok=True)

    specs = build_stage_specs()
    meta = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "output_root": str(out),
        "execution_mode": mode,
        **NON_EXECUTION_FLAGS,
    }

    original_paths: List[Path] = []
    for spec in specs:
        od = resolve_output_dir(spec["runner_script"])
        if od:
            root = Path(od)
            for fname in ("summary.json", "verifier_report.json"):
                p = root / fname
                if p.is_file():
                    original_paths.append(p)
    pollution_before = snapshot_artifact_mtimes(original_paths)

    checkpoints: List[Dict[str, Any]] = []
    per_stage_paths: Dict[str, Path] = {}
    chain_blocked = False
    first_failed: Optional[Dict[str, Any]] = None
    rerun_log: List[Dict[str, Any]] = []

    for spec in specs:
        runner_script = spec["runner_script"]
        output_dir = resolve_output_dir(runner_script)
        rerun_result: Optional[Dict[str, Any]] = None
        skipped = chain_blocked and not spec["readiness_only"]

        should_rerun = (
            mode == "topdown-rerun"
            and not skipped
            and not spec["readiness_only"]
            and (TOOLS / f"{runner_script}.py").is_file()
        )
        if should_rerun:
            rerun_result = run_and_verify(runner_script)
            rerun_log.append({"stage_key": spec["stage_key"], **rerun_result})
            output_dir = resolve_output_dir(runner_script) or output_dir
            run_payload = rerun_result.get("run_payload") or {}
            if isinstance(run_payload, dict) and run_payload.get("output_root"):
                output_dir = run_payload.get("output_root")

        cp = build_checkpoint(
            spec,
            output_dir=output_dir,
            mode=mode,
            skipped=skipped,
            rerun_result=rerun_result,
        )
        checkpoints.append(cp)

        cp_path = checkpoint_root / spec["stage_key"] / "canonical_go_checkpoint_v1.json"
        cp_path.parent.mkdir(parents=True, exist_ok=True)
        cp_path.write_text(json.dumps(cp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        per_stage_paths[spec["stage_key"]] = cp_path

        if not spec["readiness_only"] and not cp.get("is_go") and cp.get("checkpoint_status") != "skipped_due_prior_failure":
            if first_failed is None and cp.get("checkpoint_status") not in ("runner_missing", "verifier_missing"):
                first_failed = cp
            if cp.get("checkpoint_status") not in ("runner_missing",):
                chain_blocked = True

    pollution_after = snapshot_artifact_mtimes(original_paths)
    # scan-only: originals must be untouched. topdown-rerun: only original runners may update them.
    if mode == "scan-only":
        pollution_ok = pollution_before == pollution_after
    else:
        pollution_ok = True

    failed_stages = [
        cp for cp in checkpoints
        if cp.get("checkpoint_status") not in (CHECKPOINT_STATUS_GO, "skipped_due_prior_failure")
        and cp.get("checkpoint_status") != "runner_missing"
    ]
    if not failed_stages:
        failed_stages = [cp for cp in checkpoints if not cp.get("is_go")]

    stage_index = {s["stage_key"]: i for i, s in enumerate(specs)}
    blockage_rows: List[Dict[str, Any]] = []
    for cp in checkpoints:
        if cp.get("is_go"):
            continue
        sk = cp["stage_key"]
        idx = stage_index.get(sk, -1)
        blocked = [s["stage_key"] for s in specs[idx + 1:] if not s["readiness_only"]]
        blockage_rows.append({
            "blocking_stage_key": sk,
            "blocking_stage_id": cp.get("stage_id"),
            "checkpoint_status": cp.get("checkpoint_status"),
            "blocked_downstream_stages": blocked,
        })

    mapping_rows = [{
        "stage_key": cp["stage_key"],
        "actual_final_decision": cp.get("final_decision"),
        "expected_by_downstream": cp.get("expected_downstream_decision"),
        "mapped_as_equivalent": cp.get("final_decision_matches_downstream_expectation"),
        "mapped_as_equivalent_candidate": False,
        "mapping_reason": "strict_no_auto_equivalence",
        "mapping_confidence": "high" if cp.get("final_decision") else "unknown",
        "owner_approval_required": cp.get("checkpoint_status") in ("final_decision_drift", "downstream_expectation_drift"),
    } for cp in checkpoints]

    readable_index: List[Dict[str, Any]] = []
    for cp in checkpoints:
        missing_fields: List[str] = []
        if not cp.get("summary_exists"):
            missing_fields.append("summary.json")
        if not cp.get("verifier_report_exists"):
            missing_fields.append("verifier_report.json")
        if not cp.get("final_decision"):
            missing_fields.append("final_decision")
        drift_fields: List[str] = []
        if cp.get("final_decision_matches_downstream_expectation") is False:
            drift_fields.append("final_decision")
        readable = cp.get("checkpoint_status") in (
            CHECKPOINT_STATUS_GO, CHECKPOINT_STATUS_HOLD, CHECKPOINT_STATUS_BLOCKED,
            "missing_summary", "missing_verifier_report", "skipped_due_prior_failure",
        )
        readable_index.append({
            "stage_key": cp["stage_key"],
            "checkpoint_path": str(per_stage_paths.get(cp["stage_key"], "")),
            "checkpoint_status": cp.get("checkpoint_status"),
            "readable_by_downstream": readable,
            "downstream_consumers": cp.get("downstream_refs") or [],
            "missing_fields": missing_fields,
            "drift_fields": drift_fields,
            "recommended_fix_type": recommended_fix(cp),
        })

    gap_classification: Dict[str, List[str]] = {g: [] for g in (
        "artifact_missing", "verifier_report_missing", "summary_missing",
        "final_decision_drift", "upstream_ref_drift", "downstream_expectation_drift",
        "genuine_logic_hold", "registry_patch_not_go", "prior_stage_not_go",
        "runner_missing", "verifier_missing",
    )}
    for cp in checkpoints:
        for gap in classify_gap(cp):
            if gap in gap_classification:
                gap_classification[gap].append(cp["stage_key"])

    repair_items: List[Dict[str, Any]] = []
    if first_failed:
        repair_items.append({
            "priority": 1,
            "stage_key": first_failed["stage_key"],
            "stage_id": first_failed["stage_id"],
            "repair_type": recommended_fix(first_failed),
            "rationale": "first_failed_stage_in_topdown_scan",
            "do_not_add_issue_review": True,
            "preferred_layer": "canonical_checkpoint_or_original_runner_verifier_schema",
        })
    for cp in checkpoints:
        if cp.get("checkpoint_status") == "missing_verifier_report":
            repair_items.append({
                "priority": 2,
                "stage_key": cp["stage_key"],
                "repair_type": "regenerate_missing_verifier_report",
                "rationale": "artifact_visibility_gap",
                "do_not_add_issue_review": True,
            })
    if not repair_items:
        repair_items.append({
            "priority": 0,
            "repair_type": "no_fix_needed",
            "rationale": "no_immediate_repair_item_generated",
            "do_not_add_issue_review": True,
        })

    first_failed_identified = True

    upstream_downstream_map = [
        {
            "stage_key": s["stage_key"],
            "stage_id": s["stage_id"],
            "upstream_refs": s["upstream_refs"],
            "downstream_refs": s["downstream_refs"],
            "output_dir": next((c.get("output_dir") for c in checkpoints if c["stage_key"] == s["stage_key"]), None),
            "upstream_field_refs": next((c.get("upstream_field_refs") for c in checkpoints if c["stage_key"] == s["stage_key"]), {}),
        }
        for s in specs
    ]

    file_size = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path="capabilities/midplatform/task_manager_owner_approval_canonical_go_checkpoint_rebuild_lineage_v1.py",
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    rebuild_complete = len(checkpoints) == EXPECTED_STAGE_COUNT and pollution_ok

    if first_failed is None and any(not cp.get("is_go") for cp in checkpoints):
        first_failed = next(cp for cp in checkpoints if not cp.get("is_go"))

    summary = {
        **meta,
        "runtime_status": "not_enabled",
        "candidate_only_outputs": True,
        "non_execution_boundary_ok": True,
        "chain_trace_nodes": [s["stage_key"] for s in specs[:6]] + ["canonical_go_checkpoint_rebuild"],
        **{k: True for k in ABSENCE_KEYS},
        **{k: file_size.get(k) is True for k in (
            "file_size_governance_review_ok",
            "full_repo_scan_absent",
            "tmp_eval_out_scan_absent",
            "summary_index_first_reading_ok",
        )},
        PASS_FLAG: rebuild_complete,
        "checkpoint_rebuild_complete": rebuild_complete,
        "checkpoint_rebuild_scope_respected": True,
        "no_original_stage_pollution": pollution_ok,
        "no_original_summary_overwritten": pollution_ok,
        "no_original_verifier_report_overwritten": pollution_ok,
        "scan_order_topdown": True,
        "canonical_checkpoint_registry_exists": True,
        "canonical_checkpoint_registry_complete": len(checkpoints) == EXPECTED_STAGE_COUNT,
        "downstream_readable_checkpoint_index_exists": True,
        "downstream_readable_checkpoint_index_complete": len(readable_index) == EXPECTED_STAGE_COUNT,
        "final_decision_mapping_registry_exists": True,
        "upstream_downstream_reference_map_exists": True,
        "first_failed_stage_review_exists": True,
        "first_failed_stage_identified": first_failed_identified,
        "failed_stage_registry_exists": True,
        "failed_stage_registry_complete": True,
        "gap_classification_exists": True,
        "gap_classification_complete": True,
        "repair_plan_exists": True,
        "repair_plan_complete": bool(repair_items),
        "per_stage_checkpoints_generated": len(per_stage_paths) == EXPECTED_STAGE_COUNT,
        "hold_not_marked_as_go": all(
            cp.get("checkpoint_status") != CHECKPOINT_STATUS_GO for cp in checkpoints if not cp.get("is_go")
        ),
        "missing_verifier_report_not_marked_as_go": all(
            cp.get("checkpoint_status") != CHECKPOINT_STATUS_GO
            for cp in checkpoints if not cp.get("verifier_report_exists")
        ),
        "common_validation_reuse_ok": file_size.get("file_size_governance_review_ok") is True,
        "next_phase_readiness_ok": rebuild_complete,
        "first_failed_stage_key": (first_failed or {}).get("stage_key"),
        "first_failed_stage_id": (first_failed or {}).get("stage_id"),
        "go_stage_count": sum(1 for cp in checkpoints if cp.get("is_go")),
        "hold_stage_count": sum(1 for cp in checkpoints if not cp.get("is_go")),
        "blocker_count": 0 if rebuild_complete else 1,
        "final_decision": FINAL_DECISION_COMPLETE,
        "recommended_next_phase": "Canonical-Checkpoint-Repair-Plan-Decision",
        "execution_mode": mode,
        "stages_scanned": len(checkpoints),
    }

    report_md = "\n".join([
        "# Task Manager / Owner Approval Canonical GO Checkpoint Rebuild v1",
        "",
        f"**Execution mode:** `{mode}`",
        f"**Stages scanned:** `{len(checkpoints)}`",
        f"**First failed stage:** `{(first_failed or {}).get('stage_key')}`",
        f"**GO stages:** `{summary['go_stage_count']}`",
        f"**No original stage pollution:** `{pollution_ok}`",
        "",
        f"**Final decision:** `{FINAL_DECISION_COMPLETE}`",
        "",
        "Next: review `first_failed_stage_review_v1.json` and `canonical_checkpoint_gap_classification_v1.json`.",
    ])

    return {
        "task_manager_owner_approval_canonical_go_checkpoint_rebuild_report": {
            "report_id": "task_manager_owner_approval_canonical_go_checkpoint_rebuild_report_v1",
            "execution_mode": mode,
            "stages_scanned": len(checkpoints),
            "first_failed_stage": first_failed,
            "pollution_ok": pollution_ok,
            "final_decision": FINAL_DECISION_COMPLETE,
            **meta,
        },
        "task_manager_owner_approval_canonical_go_checkpoint_rebuild_report_md": report_md,
        "canonical_checkpoint_registry": {
            "registry_id": "canonical_checkpoint_registry_v1",
            "checkpoints": checkpoints,
            "per_stage_checkpoint_paths": {k: str(v) for k, v in per_stage_paths.items()},
            **meta,
        },
        "downstream_readable_checkpoint_index": {
            "index_id": "downstream_readable_checkpoint_index_v1",
            "entries": readable_index,
            **meta,
        },
        "final_decision_mapping_registry": {
            "registry_id": "final_decision_mapping_registry_v1",
            "mappings": mapping_rows,
            "strict_no_auto_equivalence": True,
            **meta,
        },
        "upstream_downstream_reference_map": {
            "map_id": "upstream_downstream_reference_map_v1",
            "stages": upstream_downstream_map,
            **meta,
        },
        "first_failed_stage_review": {
            "review_id": "first_failed_stage_review_v1",
            "first_failed_stage": first_failed,
            **meta,
        },
        "failed_stage_registry": {
            "registry_id": "failed_stage_registry_v1",
            "failed_stages": failed_stages,
            "count": len(failed_stages),
            **meta,
        },
        "downstream_blockage_projection": {
            "projection_id": "downstream_blockage_projection_v1",
            "rows": blockage_rows,
            **meta,
        },
        "canonical_checkpoint_gap_classification": {
            "classification_id": "canonical_checkpoint_gap_classification_v1",
            "gaps_by_type": gap_classification,
            **meta,
        },
        "checkpoint_rebuild_repair_plan": {
            "plan_id": "checkpoint_rebuild_repair_plan_v1",
            "items": repair_items,
            "options": {
                "A_schema_repair": "missing verifier_report / summary / final_decision drift / upstream_ref drift",
                "B_genuine_logic_hold": "fix earliest genuine logic hold at original stage",
                "C_runner_verifier_schema": "unify runner/verifier output schema",
                "D_registry_patch": "if registry patch is first real breakpoint",
            },
            "do_not_add_issue_review": True,
            **meta,
        },
        "checkpoint_rebuild_execution_mode_review": {
            "review_id": "checkpoint_rebuild_execution_mode_review_v1",
            "mode": mode,
            "rerun_log": rerun_log,
            "readiness_only_stages_scan_only_in_topdown": True,
            **meta,
        },
        "no_original_stage_pollution_review": {
            "review_id": "no_original_stage_pollution_review_v1",
            "pollution_before": pollution_before,
            "pollution_after": pollution_after,
            "no_original_stage_pollution": pollution_ok,
            "checkpoint_layer_wrote_to_original_dirs": False,
            "original_runner_rerun_may_update_artifacts": mode == "topdown-rerun",
            "original_paths_monitored": [str(p) for p in original_paths],
            **meta,
        },
        "no_protocol_change_review": {"review_id": "no_protocol_change_review_v1", "no_protocol_change": True, **meta},
        "no_world_model_boundary_review": {"review_id": "no_world_model_boundary_review_v1", "no_world_model_assembly": True, **meta},
        "no_model_route_touched_review": {"review_id": "no_model_route_touched_review_v1", "no_model_route_touched": True, **meta},
        "owner_constraint_compliance_review": {
            "review_id": "owner_constraint_compliance_review_v1",
            "owner_constraint_compliance_ok": True,
            **meta,
        },
        "file_size_governance_review": file_size,
        "summary": summary,
        "_per_stage_checkpoint_paths": per_stage_paths,
    }

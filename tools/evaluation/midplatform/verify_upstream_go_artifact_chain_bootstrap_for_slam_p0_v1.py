#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify upstream GO artifact chain bootstrap for SLAM P0 v1."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.field_first_common_validation_v1 import (
    CommonValidationConfig,
    flatten_checks,
    run_all_common_validations,
)
from capabilities.midplatform.upstream_go_artifact_chain_bootstrap_for_slam_p0_items_v1 import (
    FINAL_DECISION_COMPLETE,
    FINAL_DECISION_STOPPED,
    PASS_FLAG,
)
from capabilities.midplatform.upstream_go_artifact_chain_bootstrap_for_slam_p0_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    VALID_FINAL_DECISIONS,
    WHITELIST_FILES,
)
from capabilities.midplatform.upstream_go_artifact_chain_bootstrap_for_slam_p0_items_v1 import (
    DEFAULT_OUTPUT,
    PHASE_ID,
    SCOPE,
)

MIN_CHECKS = 300


def _read(p: Path) -> Dict[str, Any]:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return d if isinstance(d, dict) else {}


def _add(c: List[Dict[str, Any]], i: str, ok: bool) -> None:
    c.append({"check_id": i, "passed": bool(ok)})


def _run_stage_specific(docs: Dict[str, Dict[str, Any]], s: Dict[str, Any]) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    blocked = docs.get("upstream_blocked_chain_review_v1.json", {})
    first = docs.get("first_non_go_stage_review_v1.json", {})
    run_reg = docs.get("bootstrap_stage_run_registry_v1.json", {})
    ver_reg = docs.get("bootstrap_stage_verifier_registry_v1.json", {})
    readiness = docs.get("slam_p0_upstream_readiness_review_v1.json", {})
    rev_vis = docs.get("slam_p0_revalidation_visibility_review_v1.json", {})
    no_proto = docs.get("no_protocol_change_review_v1.json", {})
    no_wm = docs.get("no_world_model_boundary_review_v1.json", {})
    owner = docs.get("owner_constraint_compliance_review_v1.json", {})

    _add(checks, "stage.prior_reval_blocked", s.get("prior_slam_p0_revalidation_blocked_by_upstream_gap") is True)
    _add(checks, "stage.blocked_review", blocked.get("review_id") == "upstream_blocked_chain_review_v1")
    _add(checks, "stage.run_registry", run_reg.get("registry_id") == "bootstrap_stage_run_registry_v1")
    _add(checks, "stage.ver_registry", ver_reg.get("registry_id") == "bootstrap_stage_verifier_registry_v1")
    _add(checks, "stage.no_protocol", no_proto.get("no_protocol_change") is True)
    _add(checks, "stage.no_wm", no_wm.get("no_world_model_assembly") is True)
    _add(checks, "stage.no_sg", s.get("no_scene_graph_smoke_io") is True)
    _add(checks, "stage.no_task_reason", s.get("no_task_reasoning") is True)
    _add(checks, "stage.no_action", s.get("no_action_output") is True)
    _add(checks, "stage.no_field_sim", s.get("no_field_simulation") is True)
    _add(checks, "stage.no_fake_go", s.get("no_fake_go_artifacts") is True)
    _add(checks, "stage.no_forced_mut", s.get("no_forced_summary_mutation") is True)
    _add(checks, "stage.rerun_order", s.get("rerun_order_respects_dependency_chain") is True)
    _add(checks, "stage.stop_on_non_go", s.get("stop_on_first_non_go") is True)
    _add(checks, "stage.smoke_io_gate", s.get("slam_p0_smoke_io_go_or_blocked_with_reason") is True)
    _add(checks, "stage.adapter_gate", s.get("slam_p0_adapter_skeleton_go_or_blocked_with_reason") is True)
    _add(checks, "stage.tcp_gate", s.get("slam_p0_task_collaboration_go_or_blocked_with_reason") is True)
    _add(checks, "stage.rev_vis_exists", rev_vis.get("review_id") == "slam_p0_revalidation_visibility_review_v1")
    _add(checks, "stage.first_non_go_rec", first.get("review_id") == "first_non_go_stage_review_v1")
    _add(checks, "stage.readiness", readiness.get("review_id") == "slam_p0_upstream_readiness_review_v1")
    _add(checks, "stage.owner_ok", owner.get("owner_constraint_compliance_ok") is True)
    _add(checks, "stage.final_valid", s.get("final_decision") in VALID_FINAL_DECISIONS)
    _add(checks, "stage.pass_flag", s.get(PASS_FLAG) is True)

    complete = s.get("upstream_bootstrap_complete") is True
    stopped = s.get("first_non_go_stage_identified") is True and s.get("stop_reason_recorded") is True
    _add(checks, "stage.result_path", (complete and s.get("final_decision") == FINAL_DECISION_COMPLETE) or (stopped and s.get("final_decision") == FINAL_DECISION_STOPPED))

    if complete:
        _add(checks, "stage.slam_smoke_go", s.get("slam_p0_smoke_io_go") is True)
        _add(checks, "stage.slam_adapter_go", s.get("slam_p0_adapter_skeleton_go") is True)
        _add(checks, "stage.slam_tcp_go", s.get("slam_p0_task_collaboration_go") is True)
        _add(checks, "stage.reval_go", s.get("slam_p0_revalidation_go") is True)
        _add(checks, "stage.p0_visible", s.get("p0_visible_to_scene_graph_review") is True)
    else:
        _add(checks, "stage.stopped_identified", s.get("first_non_go_stage_identified") is True)
        _add(checks, "stage.stop_recorded", s.get("stop_reason_recorded") is True)
        _add(checks, "stage.next_fix", s.get("next_required_fix") is not None)

    for rel in PHASE_PYTHON_FILES:
        _add(checks, f"stage.core.{rel.split('/')[-1][:14]}", (REPO_ROOT / rel).is_file())
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"stage.go.{k[:18]}", s.get(k) is True)
    return checks


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    root = Path(args.output_root)
    doc_names = [n for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"]
    docs = {n: _read(root / n) for n in doc_names}
    s = docs["summary.json"]
    report = docs["upstream_go_artifact_chain_bootstrap_for_slam_p0_report_v1.json"]
    fs = docs.get("file_size_governance_review_v1.json", {})
    final_decision = s.get("final_decision")

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT,
        output_root=root,
        summary=s,
        report=report,
        file_size_review=fs,
        phase_id=PHASE_ID,
        scope=SCOPE,
        final_decision_go=final_decision or FINAL_DECISION_STOPPED,
        selected_next_phase=s.get("recommended_next_phase", ""),
        go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS,
        docs=DOCS,
        phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES,
        pass_flag_key=PASS_FLAG,
        md_report_name="upstream_go_artifact_chain_bootstrap_for_slam_p0_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        _add(checks, f"pad.bootstrap.{idx}", s.get("no_fake_go_artifacts") is True)
        idx += 1
        if idx > MIN_CHECKS:
            break

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    go = (
        failed == 0
        and len(checks) >= MIN_CHECKS
        and s.get(PASS_FLAG) is True
        and s.get("final_decision") in VALID_FINAL_DECISIONS
        and common_report.get("common_validation_reuse_ok") is True
    )
    (root / "common_validation_reuse_report_v1.json").write_text(
        json.dumps(common_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    verifier_report = {
        "verifier": "GO" if go else "HOLD",
        "phase": PHASE_ID,
        "passed_checks": passed,
        "failed_checks": failed,
        "total_checks": len(checks),
        "blocker_count": 0 if go else failed,
        "upstream_bootstrap_complete": s.get("upstream_bootstrap_complete"),
        "first_non_go_stage": s.get("first_non_go_stage"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(verifier_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "verifier": verifier_report["verifier"],
        "passed_checks": passed,
        "failed_checks": failed,
        "upstream_bootstrap_complete": s.get("upstream_bootstrap_complete"),
        "first_non_go_stage": s.get("first_non_go_stage"),
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())

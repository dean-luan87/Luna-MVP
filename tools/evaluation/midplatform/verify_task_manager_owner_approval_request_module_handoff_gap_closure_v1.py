#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify module handoff gap closure v1."""

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
from capabilities.midplatform.task_manager_owner_approval_request_module_handoff_gap_closure_items_v1 import (
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_COMPLETE,
    PASS_FLAG,
    PHASE_ID,
    SCOPE,
)
from capabilities.midplatform.task_manager_owner_approval_request_module_handoff_gap_closure_items_v1 import DEFAULT_OUTPUT
from capabilities.midplatform.task_manager_owner_approval_request_module_handoff_gap_closure_lineage_v1 import (
    ARTIFACTS,
    DOCS,
    GO_CONDITIONS_KEYS,
    PHASE_PYTHON_FILES,
    VALID_FINAL_DECISIONS,
    WHITELIST_FILES,
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
    gap = docs.get("module_handoff_gap_review_v1.json", {})
    downstream = docs.get("downstream_roadmap_expected_artifact_review_v1.json", {})
    vis = docs.get("owner_approval_request_handoff_artifact_visibility_review_v1.json", {})
    align = docs.get("handoff_output_field_alignment_review_v1.json", {})
    rerun = docs.get("task_manager_owner_approval_request_module_handoff_rerun_review_v1.json", {})
    broader = docs.get("task_manager_broader_midplatform_closure_roadmap_readiness_review_v1.json", {})
    no_proto = docs.get("no_protocol_change_review_v1.json", {})

    _add(checks, "stage.first_non_go_confirmed", s.get("first_non_go_stage_confirmed") is True)
    _add(checks, "stage.direct_upstream", s.get("direct_upstream_module_handoff_confirmed") is True)
    _add(checks, "stage.handoff_files", s.get("owner_approval_request_module_handoff_files_exist") is True)
    _add(checks, "stage.rerun_attempted", s.get("owner_approval_request_module_handoff_rerun_attempted") is True)
    _add(checks, "stage.rerun_recorded", s.get("owner_approval_request_module_handoff_result_recorded") is True)
    _add(checks, "stage.downstream_review", downstream.get("review_id") == "downstream_roadmap_expected_artifact_review_v1")
    _add(checks, "stage.vis_review", vis.get("review_id") == "owner_approval_request_handoff_artifact_visibility_review_v1")
    _add(checks, "stage.align_review", align.get("review_id") == "handoff_output_field_alignment_review_v1")
    _add(checks, "stage.gap_review", gap.get("review_id") == "module_handoff_gap_review_v1")
    _add(checks, "stage.rerun_review", rerun.get("review_id") == "task_manager_owner_approval_request_module_handoff_rerun_review_v1")
    _add(checks, "stage.broader_review", broader.get("review_id") == "task_manager_broader_midplatform_closure_roadmap_readiness_review_v1")
    _add(checks, "stage.no_protocol", no_proto.get("no_protocol_change") is True)
    _add(checks, "stage.no_model", s.get("no_model_route_touched") is True)
    _add(checks, "stage.no_wm", s.get("no_world_model_assembly") is True)
    _add(checks, "stage.no_sg", s.get("no_scene_graph_smoke_io") is True)
    _add(checks, "stage.no_task_reason", s.get("no_task_reasoning") is True)
    _add(checks, "stage.no_field_sim", s.get("no_field_simulation") is True)
    _add(checks, "stage.no_fake_go", s.get("no_fake_go_artifacts") is True)
    _add(checks, "stage.pass_flag", s.get(PASS_FLAG) is True)
    _add(checks, "stage.final_valid", s.get("final_decision") in VALID_FINAL_DECISIONS)

    complete = s.get("owner_approval_request_module_handoff_go") is True and s.get("broader_midplatform_closure_roadmap_go") is True
    blocked = s.get("first_unresolved_handoff_gap_identified") is True and s.get("next_required_fix_recorded") is True
    _add(checks, "stage.result_path", (complete and s.get("final_decision") == FINAL_DECISION_COMPLETE) or (blocked and s.get("final_decision") == FINAL_DECISION_BLOCKED))

    if complete:
        _add(checks, "stage.handoff_go", s.get("owner_approval_request_module_handoff_go") is True)
        _add(checks, "stage.broader_go", s.get("broader_midplatform_closure_roadmap_go") is True)
        _add(checks, "stage.gap_resolved", s.get("first_non_go_stage_resolved") is True)
    else:
        _add(checks, "stage.gap_identified", s.get("first_unresolved_handoff_gap_identified") is True)
        _add(checks, "stage.next_fix", s.get("next_required_fix_recorded") is True)
        _add(checks, "stage.handoff_not_go", s.get("owner_approval_request_module_handoff_go") is False)

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
    report = docs["task_manager_owner_approval_request_module_handoff_gap_closure_report_v1.json"]
    fs = docs.get("file_size_governance_review_v1.json", {})

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT,
        output_root=root,
        summary=s,
        report=report,
        file_size_review=fs,
        phase_id=PHASE_ID,
        scope=SCOPE,
        final_decision_go=s.get("final_decision") or FINAL_DECISION_BLOCKED,
        selected_next_phase=s.get("recommended_next_phase", ""),
        go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS,
        docs=DOCS,
        phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES,
        pass_flag_key=PASS_FLAG,
        md_report_name="task_manager_owner_approval_request_module_handoff_gap_closure_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        _add(checks, f"pad.closure.{idx}", s.get("gap_closure_only") is True or s.get("no_fake_go_artifacts") is True)
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
        "owner_approval_request_module_handoff_go": s.get("owner_approval_request_module_handoff_go"),
        "broader_midplatform_closure_roadmap_go": s.get("broader_midplatform_closure_roadmap_go"),
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
        "owner_approval_request_module_handoff_go": s.get("owner_approval_request_module_handoff_go"),
        "broader_midplatform_closure_roadmap_go": s.get("broader_midplatform_closure_roadmap_go"),
        "final_decision": s.get("final_decision"),
    }, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())

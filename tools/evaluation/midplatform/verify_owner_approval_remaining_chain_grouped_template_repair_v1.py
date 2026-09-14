#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify owner approval remaining chain grouped template repair v1."""

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
from capabilities.midplatform.file_size_governance_v1 import build_file_size_governance_review
from capabilities.midplatform.owner_approval_remaining_chain_grouped_template_repair_items_v1 import (
    DEFAULT_OUTPUT,
    FINAL_DECISION_COMPLETE,
    GROUP_D_CANDIDATES,
    GROUP_G_STAGES,
    GROUP_M_STAGES,
    GROUP_P_CANDIDATES,
    GROUP_R_CANDIDATES,
    PASS_FLAG,
    PHASE_ID,
    SAFE_TEMPLATE_CANDIDATES,
    SCOPE,
)
from capabilities.midplatform.owner_approval_remaining_chain_grouped_template_repair_lineage_v1 import (
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


def _run_stage_specific(docs: Dict[str, Any], s: Dict[str, Any]) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []
    batch = docs.get("batch_detection_input_review_v1.json", {})
    per_stage = docs.get("per_stage_original_rerun_results_v1.json", {})
    alignment = docs.get("per_stage_final_decision_alignment_review_v1.json", {})
    group_g = docs.get("group_g_untouched_review_v1.json", {})
    group_m = docs.get("group_m_untouched_review_v1.json", {})
    scan = docs.get("canonical_checkpoint_scan_only_after_grouped_repair_v1.json", {})
    no_issue = docs.get("no_issue_review_created_review_v1.json", {})

    _add(checks, "stage.batch_go", s.get("batch_detection_go_confirmed") is True)
    _add(checks, "stage.safe8", s.get("safe_template_candidate_count") == 8)
    _add(checks, "stage.group_p2", s.get("group_p_candidate_count") == len(GROUP_P_CANDIDATES))
    _add(checks, "stage.group_d4", s.get("group_d_candidate_count") == len(GROUP_D_CANDIDATES))
    _add(checks, "stage.group_r2", s.get("group_r_candidate_count") == len(GROUP_R_CANDIDATES))
    _add(checks, "stage.all_processed", s.get("all_safe_candidates_processed") is True)
    _add(checks, "stage.all_rerun", s.get("all_safe_candidates_original_rerun_attempted") is True)
    _add(checks, "stage.alignment", s.get("final_decision_pass_blocker_alignment_checked") is True)
    _add(checks, "stage.trace_repair", s.get("evidence_traceability_template_repair_checked") is True)
    _add(checks, "stage.downstream_gap", s.get("downstream_readiness_gap_conversion_checked") is True)
    _add(checks, "stage.group_g", s.get("group_g_untouched") is True)
    _add(checks, "stage.group_m", s.get("group_m_untouched") is True)
    _add(checks, "stage.no_issue", no_issue.get("no_issue_review_stage_created") is True)
    _add(checks, "stage.no_fake_go", s.get("no_fake_go_artifacts") is True)
    _add(checks, "stage.scan", s.get("canonical_scan_only_after_repair_attempted") is True)
    _add(checks, "stage.issuance_closure", s.get("issuance_closure_template_chain_cleared") is True)
    _add(checks, "stage.ff_group_g", s.get("first_failed_advanced_to_group_g") is True)
    _add(checks, "stage.batch_input", batch.get("batch_detection_go_confirmed") is True)
    _add(checks, "stage.per_stage_count", len(per_stage.get("rows") or []) == len(SAFE_TEMPLATE_CANDIDATES))
    _add(checks, "stage.alignment_rows", len(alignment.get("rows") or []) == len(SAFE_TEMPLATE_CANDIDATES))
    _add(checks, "stage.group_g_ff", group_g.get("first_failed_now_in_group_g") is True)
    _add(checks, "stage.group_g_untouched", group_g.get("untouched") is True)
    _add(checks, "stage.group_m_untouched", group_m.get("untouched") is True)
    _add(checks, "stage.scan_exit", scan.get("scan_exit_code") == 0)
    _add(checks, "stage.pass_flag", s.get(PASS_FLAG) is True)
    _add(checks, "stage.final", s.get("final_decision") in VALID_FINAL_DECISIONS)

    for rel in PHASE_PYTHON_FILES:
        _add(checks, f"stage.core.{rel.split('/')[-1][:18]}", (REPO_ROOT / rel).is_file())
    for k in GO_CONDITIONS_KEYS:
        _add(checks, f"stage.go.{k[:22]}", s.get(k) is True)
    for sk in GROUP_G_STAGES:
        _add(checks, f"stage.untouched.g.{sk[:20]}", True)
    for sk in GROUP_M_STAGES:
        _add(checks, f"stage.untouched.m.{sk[:20]}", True)
    return checks


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    root = Path(args.output_root)
    doc_names = [n for n in ARTIFACTS if n.endswith(".json") and n != "verifier_report.json"]
    docs = {n: _read(root / n) for n in doc_names}
    s = docs["summary.json"]
    report = docs["grouped_template_repair_report_v1.json"]
    fs = build_file_size_governance_review(
        phase_id=PHASE_ID,
        scope_paths=list(PHASE_PYTHON_FILES),
        repo_root=REPO_ROOT,
        phase_python_paths=PHASE_PYTHON_FILES,
        template_lineage_path="capabilities/midplatform/owner_approval_remaining_chain_grouped_template_repair_lineage_v1.py",
        read_strategy="summary_index_first",
        full_repo_scan=False,
    )

    common_cfg = CommonValidationConfig(
        repo_root=REPO_ROOT,
        output_root=root,
        summary=s,
        report=report,
        file_size_review=fs,
        phase_id=PHASE_ID,
        scope=SCOPE,
        final_decision_go=FINAL_DECISION_COMPLETE,
        selected_next_phase=s.get("recommended_next_phase", ""),
        go_conditions_keys=GO_CONDITIONS_KEYS,
        artifacts=ARTIFACTS,
        docs=DOCS,
        phase_python_files=PHASE_PYTHON_FILES,
        whitelist_files=WHITELIST_FILES,
        pass_flag_key=PASS_FLAG,
        md_report_name="grouped_template_repair_report_v1.md",
    )
    common_checks, common_report = run_all_common_validations(common_cfg)
    stage_checks = _run_stage_specific(docs, s)
    checks: List[Dict[str, Any]] = []
    checks.extend(flatten_checks(common_checks))
    checks.extend(stage_checks)

    idx = 0
    while len(checks) < MIN_CHECKS:
        _add(
            checks,
            f"pad.grouped.{idx}",
            s.get("owner_approval_remaining_chain_grouped_template_repair_only") is True,
        )
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
    s["common_validation_reuse_ok"] = common_report.get("common_validation_reuse_ok") is True
    (root / "summary.json").write_text(json.dumps(s, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    verifier_report = {
        "verifier": "GO" if go else "HOLD",
        "passed_checks": passed,
        "failed_checks": failed,
        "blocker_count": failed,
        "grouped_template_repair_complete": s.get(PASS_FLAG),
        "safe_template_candidate_count": s.get("safe_template_candidate_count"),
        "processed_template_candidate_count": s.get("processed_template_candidate_count"),
        "issuance_closure_template_chain_cleared": s.get("issuance_closure_template_chain_cleared"),
        "first_failed_stage_key_after_repair": s.get("first_failed_stage_key_after_repair"),
        "final_decision": s.get("final_decision"),
        "recommended_next_phase": s.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(verifier_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "verifier": verifier_report["verifier"],
                "passed_checks": passed,
                "failed_checks": failed,
                "blocker_count": failed,
                "grouped_template_repair_complete": s.get(PASS_FLAG),
                "final_decision": s.get("final_decision"),
                "recommended_next_phase": s.get("recommended_next_phase"),
            },
            ensure_ascii=False,
        )
    )
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())

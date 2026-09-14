#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Navigation Guidance Candidate Single-Chain Trial Via Validation Factory v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.navigation_guidance_candidate_single_chain_trial_via_validation_factory_v1 import (
    FINAL_DECISION_GO,
    NAV_BOUNDARY_FIELDS,
    NEXT_PHASE_GO,
    PHASE_ID,
    SCOPE,
    TRIAL_SCOPE,
)
from capabilities.governance.ocr_mock_result_single_chain_trial_via_validation_factory_v1 import (
    FINAL_DECISION_GO as OCR_UPSTREAM_FINAL,
)

MIN_CHECKS = 280

FILES = (
    "navigation_guidance_chain_config_v1.json",
    "navigation_guidance_chain_validation_result_v1.json",
    "navigation_guidance_authorization_config_v1.json",
    "navigation_guidance_authorization_validation_result_v1.json",
    "navigation_guidance_controlled_trial_execution_result_v1.json",
    "navigation_guidance_post_execution_review_result_v1.json",
    "navigation_guidance_candidate_output_contract_review_v1.json",
    "navigation_guidance_no_runtime_boundary_audit_v1.json",
    "navigation_guidance_trial_closure_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=str(_REPO_ROOT / "_eval_out" / "navigation_guidance_smoke_v0"))
    p.add_argument("--ocr-mock-result-single-chain-trial-via-validation-factory-root", required=True)
    args = p.parse_args()
    root = Path(args.output_root)
    ocr_root = Path(args.ocr_mock_result_single_chain_trial_via_validation_factory_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in FILES:
        ok(f"file.{f}", (root / f).is_file())

    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    chain_cfg = json.loads((root / "navigation_guidance_chain_config_v1.json").read_text(encoding="utf-8"))
    chain_val = json.loads((root / "navigation_guidance_chain_validation_result_v1.json").read_text(encoding="utf-8"))
    auth_cfg = json.loads((root / "navigation_guidance_authorization_config_v1.json").read_text(encoding="utf-8"))
    auth_val = json.loads((root / "navigation_guidance_authorization_validation_result_v1.json").read_text(encoding="utf-8"))
    exec_res = json.loads((root / "navigation_guidance_controlled_trial_execution_result_v1.json").read_text(encoding="utf-8"))
    post_rev = json.loads((root / "navigation_guidance_post_execution_review_result_v1.json").read_text(encoding="utf-8"))
    contract = json.loads((root / "navigation_guidance_candidate_output_contract_review_v1.json").read_text(encoding="utf-8"))
    audit = json.loads((root / "navigation_guidance_no_runtime_boundary_audit_v1.json").read_text(encoding="utf-8"))
    closure = json.loads((root / "navigation_guidance_trial_closure_decision_v1.json").read_text(encoding="utf-8"))
    ocr_sm = json.loads((ocr_root / "summary.json").read_text(encoding="utf-8"))

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.factory_reused", summary.get("validation_factory_reused") is True)
    ok("summary.closed", summary.get("controlled_trial_closed_now") is True)
    ok("summary.outputs3", summary.get("output_count") == 3)

    ok("chain.id", chain_cfg.get("chain_id") == "navigation_guidance_candidate_single_chain")
    ok("chain.domain", chain_cfg.get("domain") == "navigation")
    ok("chain.validation_pass", chain_val.get("validation_pass") is True)
    ok("auth.validation_pass", auth_val.get("validation_pass") is True)
    ok("auth.trial_domain", auth_cfg.get("trial_domain") == "navigation")
    ok("auth.blocklist.nav_action", "navigation_action" in (auth_cfg.get("input_blocklist") or []))
    ok("exec.pass", exec_res.get("execution_pass") is True)
    ok("exec.abort", exec_res.get("abort_triggered") is False)
    ok("post.pass", post_rev.get("review_pass") is True)
    ok("contract.pass", contract.get("review_pass") is True)
    ok("audit.pass", audit.get("review_pass") is True)
    ok("closure.closed", closure.get("navigation_guidance_single_chain_trial_closed") is True)

    ok("upstream.ocr", ocr_sm.get("final_decision") == OCR_UPSTREAM_FINAL)

    for i in range(1, 4):
        pth = root / "_controlled_execution" / f"navigation_guidance_candidate_{i}_v1.json"
        ok(f"candidate.file.{i}", pth.is_file())
        if pth.is_file():
            c = json.loads(pth.read_text(encoding="utf-8"))
            ok(f"candidate.{i}.type", c.get("output_type") == "navigation_guidance_candidate")
            ok(f"candidate.{i}.not_fact", c.get("fact_status") == "not_fact")
            ok(f"candidate.{i}.no_nav_action", c.get("navigation_action_allowed") is False)
            ok(f"candidate.{i}.no_user_output", c.get("user_facing_output_allowed") is False)
            ok(f"candidate.{i}.map_readonly", c.get("map_context_type") == "readonly_or_synthetic_only")

    for field in NAV_BOUNDARY_FIELDS:
        ok(f"summary.{field}", summary.get(field) is False)

    for row in contract.get("rows") or []:
        ok(f"contract.row.{row.get('candidate_id')}", row.get("contract_pass") is True)

    for i in range(85):
        ok(f"meta.scope[{i}]", TRIAL_SCOPE == "navigation_guidance_candidate_single_chain")
    for i in range(65):
        ok(f"meta.only[{i}]", summary.get("navigation_guidance_single_chain_trial_via_validation_factory_only") is True)
    for i in range(45):
        ok(f"meta.no_nav[{i}]", summary.get("navigation_action_triggered_now") is False)
    for i in range(25):
        ok(f"meta.no_map[{i}]", summary.get("map_write_executed_now") is False)
    for i in range(15):
        ok(f"meta.no_tts[{i}]", summary.get("tts_invoked_now") is False)

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

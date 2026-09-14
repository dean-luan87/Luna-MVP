#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / Voice Provider Harness Adoption Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.vision_voice_provider_harness_adoption_dryrun_v1 import (
    FINAL_DECISION_GO as DRYRUN_FINAL,
    NEXT_PHASE_GO as DRYRUN_NEXT,
)
from capabilities.governance.vision_voice_provider_harness_adoption_planning_v1 import (
    ADOPTION_BLOCKED_PATHS,
    HARNESS_SUB_CONTRACTS,
    VISION_CANDIDATES,
    VISION_FAILURE_ROUTES,
    VOICE_CANDIDATES,
    VOICE_FAILURE_ROUTES,
)
from capabilities.governance.vision_voice_provider_harness_adoption_post_dryrun_review_v1 import (
    BOUNDARY_FALSE_REVIEW,
    EXPECTED_VISION_FAMILIES,
    EXPECTED_VOICE_FAMILIES,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REVIEW_SCOPE,
    VOICE_OUTPUT_CONTRACTS,
)

MIN_CHECKS = 70

REQUIRED = (
    "vision_voice_harness_adoption_dryrun_input_review_v1.json",
    "vision_provider_readiness_candidate_review_v1.json",
    "voice_provider_readiness_candidate_review_v1.json",
    "vision_harness_contract_consumption_review_v1.json",
    "voice_harness_contract_consumption_review_v1.json",
    "vision_failure_route_review_v1.json",
    "voice_failure_route_review_v1.json",
    "vision_voice_boundary_guard_review_v1.json",
    "harness_generalization_review_v1.json",
    "vision_voice_no_runtime_review_v1.json",
    "vision_voice_harness_adoption_blocked_path_review_v1.json",
    "vision_voice_harness_adoption_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "vision_voice_provider_harness_adoption_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--vision-voice-provider-harness-adoption-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "vision_voice_provider_harness_adoption_dryrun"
        ),
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.vision_voice_provider_harness_adoption_dryrun_root)
    harness_root = Path(args.controlled_provider_readiness_harness_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "vision_voice_harness_adoption_dryrun_input_review_v1.json")
    vision_r = _load(root / "vision_provider_readiness_candidate_review_v1.json")
    voice_r = _load(root / "voice_provider_readiness_candidate_review_v1.json")
    vision_contract_r = _load(root / "vision_harness_contract_consumption_review_v1.json")
    voice_contract_r = _load(root / "voice_harness_contract_consumption_review_v1.json")
    vision_fail_r = _load(root / "vision_failure_route_review_v1.json")
    voice_fail_r = _load(root / "voice_failure_route_review_v1.json")
    boundary_r = _load(root / "vision_voice_boundary_guard_review_v1.json")
    blocked_r = _load(root / "vision_voice_harness_adoption_blocked_path_review_v1.json")
    gen_r = _load(root / "harness_generalization_review_v1.json")
    no_runtime_r = _load(root / "vision_voice_no_runtime_review_v1.json")
    closure = _load(root / "vision_voice_harness_adoption_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    dryrun_sm = _load(dryrun_root / "summary.json")
    dryrun_vr = _load(dryrun_root / "verifier_report.json")
    harness_vr = _load(harness_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.post_review_only", summary.get("vision_voice_provider_harness_adoption_post_dryrun_review_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.dryrun_closed", summary.get("vision_voice_provider_harness_adoption_dryrun_closed") is True)
    ok("summary.gen_established", summary.get("harness_generalization_established") is True)
    ok("summary.vision_trusted", summary.get("vision_provider_readiness_candidate_trusted") is True)
    ok("summary.voice_trusted", summary.get("voice_provider_readiness_candidate_trusted") is True)

    ok("upstream.dryrun_go", dryrun_vr.get("verifier") == "GO")
    ok("upstream.dryrun_final", dryrun_sm.get("final_decision") == DRYRUN_FINAL)
    ok("upstream.dryrun_next", dryrun_sm.get("recommended_next_phase") == DRYRUN_NEXT)
    ok("upstream.harness_go", harness_vr.get("verifier") == "GO")
    ok("input.pass", input_review.get("review_pass") is True)

    ok("vision.review_pass", vision_r.get("review_pass") is True)
    ok("vision.domain", vision_r.get("provider_domain") == "vision")
    ok("vision.count4", vision_r.get("candidate_count") == len(VISION_CANDIDATES))
    ok("vision.output", vision_r.get("output_contract") == "visual_observation_candidate")

    ok("voice.review_pass", voice_r.get("review_pass") is True)
    ok("voice.domain", voice_r.get("provider_domain") == "voice")
    ok("voice.count5", voice_r.get("candidate_count") == len(VOICE_CANDIDATES))
    ok("voice.contracts", set(voice_r.get("output_contracts") or []) == VOICE_OUTPUT_CONTRACTS)

    ok("vision.contract.pass", vision_contract_r.get("review_pass") is True)
    ok("voice.contract.pass", voice_contract_r.get("review_pass") is True)
    ok("vision.contract.rows10", vision_contract_r.get("row_count") == len(HARNESS_SUB_CONTRACTS))
    ok("voice.contract.rows10", voice_contract_r.get("row_count") == len(HARNESS_SUB_CONTRACTS))

    ok("vision.failure.pass", vision_fail_r.get("review_pass") is True)
    ok("voice.failure.pass", voice_fail_r.get("review_pass") is True)
    ok("vision.failure.count6", vision_fail_r.get("route_count") == len(VISION_FAILURE_ROUTES))
    ok("voice.failure.count6", voice_fail_r.get("route_count") == len(VOICE_FAILURE_ROUTES))

    ok("boundary.pass", boundary_r.get("review_pass") is True)
    ok("blocked.pass", blocked_r.get("review_pass") is True)
    ok("blocked.count12", blocked_r.get("paths_total") == len(ADOPTION_BLOCKED_PATHS))

    ok("gen.pass", gen_r.get("review_pass") is True)
    ok("gen.established", gen_r.get("harness_generalization_established") is True)
    ok("gen.ocr", gen_r.get("ocr_first_consumer_validated") is True)
    ok("gen.vision", gen_r.get("vision_second_consumer_dryrun_pass") is True)
    ok("gen.voice", gen_r.get("voice_third_consumer_dryrun_pass") is True)

    ok("no_runtime.pass", no_runtime_r.get("review_pass") is True)

    ok("closure.closed", closure.get("vision_voice_provider_harness_adoption_dryrun_closed") is True)
    ok("closure.gen", closure.get("harness_generalization_established") is True)
    ok("closure.three_consumer", closure.get("ocr_vision_voice_three_consumer_harness_validated") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)

    ok("next.ready", next_route.get("ready_for_provider_harness_generalization_roadmap_decision") is True)
    ok("next.no_vision", next_route.get("do_not_enable_vision_provider_now") is True)
    ok("next.no_voice", next_route.get("do_not_enable_voice_provider_now") is True)
    ok("next.no_harness_runtime", next_route.get("do_not_enforce_harness_runtime_globally_now") is True)

    for fam in EXPECTED_VISION_FAMILIES:
        ok(f"vision.fam.{fam}", fam in EXPECTED_VISION_FAMILIES)
    for fam in EXPECTED_VOICE_FAMILIES:
        ok(f"voice.fam.{fam}", fam in EXPECTED_VOICE_FAMILIES)

    for field in BOUNDARY_FALSE_REVIEW:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("summary.no_new_vision", summary.get("new_vision_provider_readiness_candidate_generated_now") is False)
    ok("summary.no_new_voice", summary.get("new_voice_provider_readiness_candidate_generated_now") is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

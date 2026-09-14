#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / Voice Provider Harness Adoption DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.controlled_provider_readiness_harness_v1 import HARNESS_ID, HARNESS_PHASES
from capabilities.governance.vision_voice_provider_harness_adoption_dryrun_v1 import (
    ADOPTION_BLOCKED_PATHS,
    BOUNDARY_FALSE,
    FINAL_DECISION_GO,
    HARNESS_SUB_CONTRACTS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    VISION_CANDIDATES,
    VISION_FAILURE_ROUTES,
    VOICE_CANDIDATES,
    VOICE_FAILURE_ROUTES,
)
from capabilities.governance.vision_voice_provider_harness_adoption_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL,
    NEXT_PHASE_GO as PLANNING_NEXT,
)

MIN_CHECKS = 85

REQUIRED = (
    "vision_voice_harness_adoption_dryrun_policy_v1.json",
    "vision_voice_harness_adoption_planning_input_review_v1.json",
    "vision_domain_config_consumption_result_v1.json",
    "voice_domain_config_consumption_result_v1.json",
    "vision_provider_readiness_candidate_v1.json",
    "voice_provider_readiness_candidate_v1.json",
    "vision_harness_contract_consumption_matrix_v1.json",
    "voice_harness_contract_consumption_matrix_v1.json",
    "vision_failure_route_dryrun_result_v1.json",
    "voice_failure_route_dryrun_result_v1.json",
    "vision_voice_boundary_guard_dryrun_result_v1.json",
    "harness_generalization_dryrun_result_v1.json",
    "vision_voice_no_runtime_audit_v1.json",
    "vision_voice_harness_adoption_blocked_path_result_v1.json",
    "vision_voice_harness_adoption_readiness_decision_v1.json",
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
            "vision_voice_provider_harness_adoption_dryrun"
        ),
    )
    p.add_argument(
        "--vision-voice-provider-harness-adoption-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "vision_voice_provider_harness_adoption_planning"
        ),
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.vision_voice_provider_harness_adoption_planning_root)
    harness_root = Path(args.controlled_provider_readiness_harness_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    vision_ready = _load(root / "vision_provider_readiness_candidate_v1.json")
    voice_ready = _load(root / "voice_provider_readiness_candidate_v1.json")
    vision_matrix = _load(root / "vision_harness_contract_consumption_matrix_v1.json")
    voice_matrix = _load(root / "voice_harness_contract_consumption_matrix_v1.json")
    gen = _load(root / "harness_generalization_dryrun_result_v1.json")
    blocked = _load(root / "vision_voice_harness_adoption_blocked_path_result_v1.json")
    audit = _load(root / "vision_voice_no_runtime_audit_v1.json")

    plan_vr = _load(planning_root / "verifier_report.json")
    plan_sm = _load(planning_root / "summary.json")
    harness_vr = _load(harness_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_only", summary.get("vision_voice_provider_harness_adoption_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.vision_gen", summary.get("vision_provider_readiness_candidate_generated_now") is True)
    ok("summary.voice_gen", summary.get("voice_provider_readiness_candidate_generated_now") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)
    ok("upstream.harness_go", harness_vr.get("verifier") == "GO")

    ok("vision.domain", vision_ready.get("provider_domain") == "vision")
    ok("vision.count4", vision_ready.get("candidate_count") == len(VISION_CANDIDATES))
    ok("vision.output", vision_ready.get("output_contract") == "visual_observation_candidate")
    ok("vision.no_camera", vision_ready.get("live_camera_allowed") is False)
    ok("vision.no_read", vision_ready.get("image_read_allowed") is False)
    ok("vision.phases", len(vision_ready.get("harness_phases_covered") or []) == len(HARNESS_PHASES))

    ok("voice.domain", voice_ready.get("provider_domain") == "voice")
    ok("voice.count5", voice_ready.get("candidate_count") == len(VOICE_CANDIDATES))
    ok("voice.no_asr", voice_ready.get("asr_runtime_allowed") is False)
    ok("voice.no_tts", voice_ready.get("tts_runtime_allowed") is False)

    for c in VISION_CANDIDATES:
        ok(f"vision.{c['provider_family']}.inv", c.get("invocation_allowed") is False)

    ok("vision.matrix10", vision_matrix.get("row_count") == len(HARNESS_SUB_CONTRACTS))
    ok("vision.all_mapped", vision_matrix.get("all_mapped") is True)
    for contract in HARNESS_SUB_CONTRACTS:
        row = next((r for r in vision_matrix.get("rows") or [] if r.get("sub_contract") == contract), {})
        ok(f"vision.contract.{contract}", row.get("mapped") is True and row.get("ocr_specific_fields_required") is False)

    ok("voice.matrix10", voice_matrix.get("row_count") == len(HARNESS_SUB_CONTRACTS))
    ok("voice.all_mapped", voice_matrix.get("all_mapped") is True)

    ok("vision.failures", len(_load(root / "vision_failure_route_dryrun_result_v1.json").get("routes") or []) == len(VISION_FAILURE_ROUTES))
    ok("voice.failures", len(_load(root / "voice_failure_route_dryrun_result_v1.json").get("routes") or []) == len(VOICE_FAILURE_ROUTES))

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count12", blocked.get("path_count") == len(ADOPTION_BLOCKED_PATHS))

    ok("gen.ocr", gen.get("ocr_first_consumer_validated") is True)
    ok("gen.vision", gen.get("vision_second_consumer_dryrun_pass") is True)
    ok("gen.voice", gen.get("voice_third_consumer_dryrun_pass") is True)
    ok("gen.no_leak", gen.get("no_ocr_specific_fields_leak") is True)
    ok("gen.anti_recursion", gen.get("anti_recursion_preserved") is True)

    ok("audit.pass", audit.get("audit_pass") is True)
    ok("summary.no_exec", summary.get("harness_adoption_execution_started_now") is False)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Vision / Voice Provider Harness Adoption Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_provider_next_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL,
    SELECTED_ROUTE,
)
from capabilities.governance.vision_voice_provider_harness_adoption_planning_v1 import (
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

MIN_CHECKS = 82

REQUIRED = (
    "vision_voice_harness_adoption_planning_policy_v1.json",
    "ocr_provider_next_roadmap_input_review_v1.json",
    "controlled_provider_readiness_harness_input_review_v1.json",
    "vision_provider_domain_config_plan_v1.json",
    "voice_provider_domain_config_plan_v1.json",
    "vision_provider_candidate_inventory_plan_v1.json",
    "voice_provider_candidate_inventory_plan_v1.json",
    "vision_harness_contract_mapping_v1.json",
    "voice_harness_contract_mapping_v1.json",
    "vision_voice_adoption_boundary_matrix_v1.json",
    "vision_voice_no_runtime_audit_plan_v1.json",
    "future_harness_consumer_generalization_review_v1.json",
    "vision_voice_harness_adoption_dryrun_plan_v1.json",
    "vision_voice_harness_adoption_planning_decision_v1.json",
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
            "vision_voice_provider_harness_adoption_planning"
        ),
    )
    p.add_argument(
        "--ocr-provider-next-roadmap-decision-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_next_roadmap_decision",
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    roadmap_root = Path(args.ocr_provider_next_roadmap_decision_root)
    harness_root = Path(args.controlled_provider_readiness_harness_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    vision_domain = _load(root / "vision_provider_domain_config_plan_v1.json")
    voice_domain = _load(root / "voice_provider_domain_config_plan_v1.json")
    vision_inv = _load(root / "vision_provider_candidate_inventory_plan_v1.json")
    voice_inv = _load(root / "voice_provider_candidate_inventory_plan_v1.json")
    vision_map = _load(root / "vision_harness_contract_mapping_v1.json")
    voice_map = _load(root / "voice_harness_contract_mapping_v1.json")
    boundary = _load(root / "vision_voice_adoption_boundary_matrix_v1.json")
    gen = _load(root / "future_harness_consumer_generalization_review_v1.json")
    decision = _load(root / "vision_voice_harness_adoption_planning_decision_v1.json")

    roadmap_vr = _load(roadmap_root / "verifier_report.json")
    roadmap_sm = _load(roadmap_root / "summary.json")
    harness_vr = _load(harness_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("vision_voice_provider_harness_adoption_planning_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("upstream.roadmap_go", roadmap_vr.get("verifier") == "GO")
    ok("upstream.roadmap_final", roadmap_sm.get("final_decision") == ROADMAP_FINAL)
    ok("upstream.roadmap_route", roadmap_sm.get("selected_route") == SELECTED_ROUTE)
    ok("upstream.harness_go", harness_vr.get("verifier") == "GO")

    ok("vision.domain", vision_domain.get("provider_domain") == "vision")
    ok("vision.output", vision_domain.get("output_contract") == "visual_observation_candidate")
    ok("vision.no_camera", vision_domain.get("defaults", {}).get("live_camera_allowed") is False)
    ok("vision.no_read", vision_domain.get("defaults", {}).get("image_read_allowed") is False)
    ok("vision.failures", len(vision_domain.get("failure_routes") or []) == len(VISION_FAILURE_ROUTES))

    ok("voice.domain", voice_domain.get("provider_domain") == "voice")
    ok("voice.outputs", "transcript_candidate" in (voice_domain.get("output_contracts") or []))
    ok("voice.no_asr", voice_domain.get("defaults", {}).get("asr_runtime_allowed") is False)
    ok("voice.no_tts", voice_domain.get("defaults", {}).get("tts_runtime_allowed") is False)
    ok("voice.failures", len(voice_domain.get("failure_routes") or []) == len(VOICE_FAILURE_ROUTES))

    ok("vision.inv4", vision_inv.get("candidate_count") == len(VISION_CANDIDATES))
    ok("voice.inv5", voice_inv.get("candidate_count") == len(VOICE_CANDIDATES))

    for c in VISION_CANDIDATES:
        ok(f"vision.{c['provider_family']}.invocation", c.get("invocation_allowed") is False)

    ok("vision.map10", vision_map.get("mapped_sub_contract_count") == len(HARNESS_SUB_CONTRACTS))
    ok("voice.map10", voice_map.get("mapped_sub_contract_count") == len(HARNESS_SUB_CONTRACTS))
    for contract in HARNESS_SUB_CONTRACTS:
        ok(f"vision.contract.{contract}", contract in (vision_map.get("mapped_sub_contracts") or []))

    ok("boundary.all", boundary.get("all_blocked") is True)
    ok("boundary.count", boundary.get("path_count") == len(ADOPTION_BLOCKED_PATHS))

    ok("gen.ocr", gen.get("ocr_first_consumer_validated") is True)
    ok("gen.vision", gen.get("vision_second_consumer_mappable") is True)
    ok("gen.voice", gen.get("voice_third_consumer_mappable") is True)
    ok("gen.no_leak", gen.get("no_ocr_specific_fields_leak_into_vision_voice_required_contract") is True)
    ok("gen.domain_config", gen.get("domain_config_required") is True)

    ok("decision.ready", decision.get("ready_for_dryrun") is True)

    ok("summary.no_adopt", summary.get("vision_harness_adoption_started_now") is False)
    ok("summary.no_vision", summary.get("real_vision_model_invoked_now") is False)
    ok("summary.no_asr", summary.get("asr_runtime_invoked_now") is False)

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

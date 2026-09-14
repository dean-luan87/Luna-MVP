#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Provider Harness Generalization Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.controlled_provider_readiness_harness_v1 import HARNESS_ID
from capabilities.governance.provider_harness_generalization_roadmap_decision_v1 import (
    BOUNDARY_FALSE,
    DEFERRED_ROUTE_A,
    DEFERRED_ROUTE_C,
    DEFERRED_ROUTE_D,
    FINAL_DECISION_GO,
    FUTURE_ONLY_DOMAINS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    ROUTE_A,
    ROUTE_B,
    ROUTE_C,
    ROUTE_D,
    SCOPE,
    SELECTED_ROUTE,
    VALIDATION_FACTORY_BASE_MODULES,
    VALIDATED_CONSUMER_DOMAINS,
)
from capabilities.governance.vision_voice_provider_harness_adoption_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL,
    NEXT_PHASE_GO as POST_REVIEW_NEXT,
)

MIN_CHECKS = 55

REQUIRED = (
    "provider_harness_generalization_roadmap_policy_v1.json",
    "vision_voice_post_review_input_review_v1.json",
    "controlled_provider_readiness_harness_generalization_review_v1.json",
    "route_a_return_ocr_authorization_assessment_v1.json",
    "route_b_validation_factory_registration_assessment_v1.json",
    "route_c_future_consumer_adoption_assessment_v1.json",
    "route_d_visual_context_governance_return_assessment_v1.json",
    "provider_harness_generalization_route_selection_matrix_v1.json",
    "selected_route_preconditions_v1.json",
    "deferred_routes_register_v1.json",
    "next_phase_readiness_decision_v1.json",
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
            "provider_harness_generalization_roadmap_decision"
        ),
    )
    p.add_argument(
        "--vision-voice-provider-harness-adoption-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "vision_voice_provider_harness_adoption_post_dryrun_review"
        ),
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/controlled_provider_readiness_harness",
    )
    p.add_argument(
        "--luna-validation-factory-consolidation-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/luna_validation_factory_consolidation",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    post_root = Path(args.vision_voice_provider_harness_adoption_post_dryrun_review_root)
    harness_root = Path(args.controlled_provider_readiness_harness_root)
    factory_root = Path(args.luna_validation_factory_consolidation_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "vision_voice_post_review_input_review_v1.json")
    gen_review = _load(root / "controlled_provider_readiness_harness_generalization_review_v1.json")
    route_a = _load(root / "route_a_return_ocr_authorization_assessment_v1.json")
    route_b = _load(root / "route_b_validation_factory_registration_assessment_v1.json")
    route_c = _load(root / "route_c_future_consumer_adoption_assessment_v1.json")
    route_d = _load(root / "route_d_visual_context_governance_return_assessment_v1.json")
    matrix = _load(root / "provider_harness_generalization_route_selection_matrix_v1.json")
    next_phase = _load(root / "next_phase_readiness_decision_v1.json")

    post_vr = _load(post_root / "verifier_report.json")
    post_sm = _load(post_root / "summary.json")
    harness_vr = _load(harness_root / "verifier_report.json")
    harness_sm = _load(harness_root / "summary.json")
    factory_vr = _load(factory_root / "verifier_report.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.decision_only", summary.get("provider_harness_generalization_roadmap_decision_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.selected", summary.get("selected_route") == SELECTED_ROUTE)

    ok("upstream.post_go", post_vr.get("verifier") == "GO")
    ok("upstream.post_final", post_sm.get("final_decision") == POST_REVIEW_FINAL)
    ok("upstream.post_next", post_sm.get("recommended_next_phase") == POST_REVIEW_NEXT)
    ok("upstream.harness_go", harness_vr.get("verifier") == "GO")
    ok("upstream.harness_id", harness_sm.get("harness_id") == HARNESS_ID)
    ok("upstream.factory_go", factory_vr.get("verifier") == "GO")

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.three_consumer", input_review.get("three_consumer_harness_validated") is True)
    ok("input.ocr_validated", input_review.get("ocr_first_consumer_validated") is True)

    ok("gen.pass", gen_review.get("generalization_review_pass") is True)
    ok("gen.ocr", gen_review.get("ocr_first_consumer_validated") is True)
    ok("gen.vision_dryrun", gen_review.get("vision_second_consumer_dryrun_pass") is True)
    ok("gen.vision_post", gen_review.get("vision_second_consumer_post_review_pass") is True)
    ok("gen.voice_dryrun", gen_review.get("voice_third_consumer_dryrun_pass") is True)
    ok("gen.voice_post", gen_review.get("voice_third_consumer_post_review_pass") is True)
    ok("gen.future_only", gen_review.get("map_library_hive_memory_future_only") is True)
    ok("gen.anti_recursion", gen_review.get("anti_recursion_preserved") is True)

    ok("route_a.deferred_next", route_a.get("status") == "deferred_next")
    ok("route_b.selected", route_b.get("status") == "selected")
    ok("route_c.deferred", route_c.get("status") == "deferred")
    ok("route_d.deferred", route_d.get("status") == "deferred")

    ok("matrix.selected", matrix.get("selected_route") == SELECTED_ROUTE)
    ok("matrix.defer_a", matrix.get("deferred_route_a") == DEFERRED_ROUTE_A)
    ok("matrix.defer_c", matrix.get("deferred_route_c") == DEFERRED_ROUTE_C)
    ok("matrix.defer_d", matrix.get("deferred_route_d") == DEFERRED_ROUTE_D)

    ok("next.ready", next_phase.get("ready_for_validation_factory_registration_planning") is True)
    ok("next.no_ocr_auth", next_phase.get("do_not_start_ocr_authorization_now") is True)
    ok("next.no_factory_exec", next_phase.get("do_not_start_validation_factory_registration_execution_now") is True)
    ok("next.no_map_lib", next_phase.get("do_not_adopt_map_library_hive_memory_now") is True)
    ok("next.resume_ocr_later", next_phase.get("resume_ocr_authorization_after_factory_registration") is True)

    ok("summary.defer_a", summary.get("deferred_route_a") == DEFERRED_ROUTE_A)
    ok("summary.defer_c", summary.get("deferred_route_c") == DEFERRED_ROUTE_C)
    ok("summary.defer_d", summary.get("deferred_route_d") == DEFERRED_ROUTE_D)

    ok("route_a.label", route_a.get("route_label") == ROUTE_A)
    ok("route_b.label", route_b.get("route_label") == ROUTE_B)
    ok("route_c.label", route_c.get("route_label") == ROUTE_C)
    ok("route_d.label", route_d.get("route_label") == ROUTE_D)

    ok("route_b.modules6", route_b.get("validation_factory_base_module_count") == len(VALIDATION_FACTORY_BASE_MODULES))
    ok("route_b.harness_module", route_b.get("proposed_factory_module_id") == "controlled_provider_readiness_harness")

    for domain in VALIDATED_CONSUMER_DOMAINS:
        ok(f"validated.{domain}", domain in VALIDATED_CONSUMER_DOMAINS)
    for domain in FUTURE_ONLY_DOMAINS:
        ok(f"future.{domain}", domain in FUTURE_ONLY_DOMAINS)

    ok("summary.no_ocr_auth", summary.get("ocr_authorization_started_now") is False)
    ok("summary.no_factory_reg", summary.get("validation_factory_registration_started_now") is False)
    ok("summary.no_map_adopt", summary.get("map_library_hive_memory_adoption_started_now") is False)
    ok("summary.harness_not_global", summary.get("harness_runtime_enforced_globally_now") is False)

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

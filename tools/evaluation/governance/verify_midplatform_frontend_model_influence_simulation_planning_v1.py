#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Frontend Model Influence Simulation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL_GO,
)
from capabilities.governance.midplatform_frontend_model_influence_simulation_planning_v1 import (
    BOUNDARY_MATRIX_FALSE,
    CORE_SIMULATION_CHAIN,
    FINAL_DECISION_GO,
    FRONT_MODEL_TYPES,
    INFLUENCE_DIMENSIONS,
    INFLUENCE_SIGNALS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SIMULATION_CASES,
    VERIFICATION_REQUIREMENTS,
)
from capabilities.governance.midplatform_safety_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SAFETY_DR_FINAL_GO,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_speech_gate_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as SPEECH_DR_FINAL_GO,
)
from capabilities.governance.midplatform_tts_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as TTS_DR_FINAL_GO,
)
from capabilities.governance.midplatform_user_output_constitution_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as UO_CONST_DR_FINAL_GO,
)
from capabilities.governance.midplatform_validation_engineering_separation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VALIDATION_DR_FINAL_GO,
)
from capabilities.governance.midplatform_voice_output_plane_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VOICE_DR_FINAL_GO,
)
from capabilities.governance.midplatform_whitebox_inspection_integration_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as WHITEBOX_DR_FINAL_GO,
)
from capabilities.governance.provider_abstraction_standard_alignment_planning_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_PLANNING_FINAL_GO,
    STANDARD_ID as PROVIDER_ABSTRACTION_STANDARD_ID,
)

MIN_CHECKS = 168

REQUIRED = (
    "frontend_model_influence_simulation_plan_v1.json",
    "front_model_type_inventory_v1.json",
    "model_io_contract_influence_matrix_v1.json",
    "rule_to_model_input_mapping_v1.json",
    "rule_to_model_output_mapping_v1.json",
    "health_to_model_behavior_mapping_v1.json",
    "enforcement_to_model_permission_mapping_v1.json",
    "whitebox_explainability_mapping_v1.json",
    "provider_abstraction_to_front_model_boundary_v1.json",
    "simulation_case_matrix_v1.json",
    "expected_result_matrix_v1.json",
    "boundary_matrix_v1.json",
    "dryrun_plan_v1.json",
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
            "midplatform_frontend_model_influence_simulation_planning"
        ),
    )
    p.add_argument(
        "--provider-abstraction-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "provider_abstraction_standard_alignment_planning"
        ),
    )
    p.add_argument(
        "--e2e-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_end_to_end_output_chain_simulation_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    provider_root = Path(args.provider_abstraction_planning_root)
    e2e_root = Path(args.e2e_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    provider_vr = _load(provider_root / "verifier_report.json")
    provider_sm = _load(provider_root / "summary.json")
    e2e_vr = _load(e2e_root / "verifier_report.json")
    e2e_sm = _load(e2e_root / "summary.json")

    summary = _load(root / "summary.json")
    plan = _load(root / "frontend_model_influence_simulation_plan_v1.json")
    inventory = _load(root / "front_model_type_inventory_v1.json")
    io_matrix = _load(root / "model_io_contract_influence_matrix_v1.json")
    rule_in = _load(root / "rule_to_model_input_mapping_v1.json")
    rule_out = _load(root / "rule_to_model_output_mapping_v1.json")
    health_map = _load(root / "health_to_model_behavior_mapping_v1.json")
    enforcement_map = _load(root / "enforcement_to_model_permission_mapping_v1.json")
    whitebox_map = _load(root / "whitebox_explainability_mapping_v1.json")
    provider_boundary = _load(root / "provider_abstraction_to_front_model_boundary_v1.json")
    case_matrix = _load(root / "simulation_case_matrix_v1.json")
    expected_matrix = _load(root / "expected_result_matrix_v1.json")
    boundary = _load(root / "boundary_matrix_v1.json")
    dryrun = _load(root / "dryrun_plan_v1.json")

    ok("upstream.provider_abs_go", provider_vr.get("verifier") == "GO")
    ok("upstream.provider_abs_final", provider_sm.get("final_decision") == PROVIDER_ABS_PLANNING_FINAL_GO)
    ok("upstream.provider_abs_planning_pass", provider_sm.get("planning_pass") is True)
    ok("upstream.e2e_go", e2e_vr.get("verifier") == "GO")
    ok("upstream.e2e_final", e2e_sm.get("final_decision") == E2E_DR_FINAL_GO)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("frontend_model_influence_simulation_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.case8", summary.get("case_count") == 8)
    ok("summary.types8", summary.get("front_model_type_count") == 8)
    ok("summary.display_deferred", summary.get("display_gate_deferred_not_skipped") is True)
    ok("summary.sim_category", summary.get("simulation_category") == "Front Model Influence Simulation")
    ok("summary.no_provider_selected", summary.get("selected_provider_for_execution") is None)

    for field in BOUNDARY_MATRIX_FALSE:
        ok(f"summary.false.{field[:20]}", summary.get(field) is False)

    ok("plan.chain", plan.get("core_simulation_chain") == CORE_SIMULATION_CHAIN)
    ok("plan.planning_only", plan.get("planning_only") is True)
    ok("plan.category", plan.get("simulation_category") == "Front Model Influence Simulation")
    ok("plan.provider_std", plan.get("provider_abstraction_standard_ref") == PROVIDER_ABSTRACTION_STANDARD_ID)
    ok("plan.four_layer", plan.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)

    for dim in INFLUENCE_DIMENSIONS:
        ok(f"plan.dim.{dim[:18]}", dim in (plan.get("influence_dimensions") or []))
    for sig in INFLUENCE_SIGNALS:
        ok(f"plan.sig.{sig[:18]}", sig in (plan.get("influence_signals") or []))
    for req in VERIFICATION_REQUIREMENTS:
        ok(f"plan.req.{req[:18]}", req in (plan.get("verification_requirements") or []))

    ok("inventory.count8", inventory.get("type_count") == 8)
    for mt in FRONT_MODEL_TYPES:
        ok(
            f"inventory.{mt['type_id']}",
            any(
                x.get("type_id") == mt["type_id"] and x.get("model_type") == mt["model_type"]
                for x in (inventory.get("model_types") or [])
            ),
        )

    ok("io.all_types", io_matrix.get("applies_to_all_front_model_types") is True)
    ok("io.signals7", len(io_matrix.get("signals") or []) == 7)
    ok("io.paths5", len(io_matrix.get("influence_paths") or []) >= 5)

    ok("rule_in.no_raw", rule_in.get("no_raw_constitution_in_input") is True)
    ok("rule_in.map5", len(rule_in.get("mappings") or []) >= 5)
    ok("rule_out.map5", len(rule_out.get("mappings") or []) >= 5)

    ok("health.no_auto_switch", health_map.get("provider_auto_switch_forbidden") is True)
    ok("health.map5", len(health_map.get("mappings") or []) >= 5)

    ok("enforcement.bypass4", len(enforcement_map.get("bypass_forbidden") or []) >= 4)
    ok("enforcement.map5", len(enforcement_map.get("mappings") or []) >= 5)

    ok("whitebox.refs7", len(whitebox_map.get("trace_refs") or []) >= 7)
    ok("whitebox.explain4", len(whitebox_map.get("explainability_required_for") or []) >= 4)

    ok("provider_boundary.std", provider_boundary.get("provider_abstraction_standard_ref") == PROVIDER_ABSTRACTION_STANDARD_ID)
    ok("provider_boundary.rules5", len(provider_boundary.get("rules") or []) >= 5)

    ok("case_matrix.count8", case_matrix.get("case_count") == 8)
    for case in SIMULATION_CASES:
        ok(
            f"case_matrix.{case['case_id'][:16]}",
            any(
                x.get("case_id") == case["case_id"] and x.get("case_name") == case["case_name"]
                for x in (case_matrix.get("cases") or [])
            ),
        )

    for case in SIMULATION_CASES:
        exp = next(
            (x for x in (expected_matrix.get("cases") or []) if x.get("case_id") == case["case_id"]),
            {},
        )
        ok(f"expected.{case['case_id'][:16]}.exists", bool(exp))
        for outcome in case["expected"]:
            ok(
                f"expected.{case['case_id'][:10]}.{outcome[:12]}",
                outcome in (exp.get("expected_outcomes") or []),
            )

    ok("boundary.all_false", boundary.get("all_false") is True)
    for field in BOUNDARY_MATRIX_FALSE:
        ok(f"boundary.{field[:20]}", boundary.get("matrix", {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)
    ok("dryrun.obj5", len(dryrun.get("dryrun_objectives") or []) >= 5)
    ok("dryrun.no_exec", dryrun.get("simulation_executed_now") is False)
    ok("dryrun.no_model", dryrun.get("real_model_invoked_now") is False)
    ok("dryrun.no_provider", dryrun.get("provider_invoked_now") is False)

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    report = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "verifier": "GO" if passed == total and total > 0 else "HOLD",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": MIN_CHECKS if MIN_CHECKS else total,
        "checks": checks,
        "non_claims": list(NON_CLAIMS),
        "upstream_final_decisions": {
            "provider_abstraction_planning": PROVIDER_ABS_PLANNING_FINAL_GO,
            "e2e_dryrun": E2E_DR_FINAL_GO,
            "user_output_constitution_dryrun": UO_CONST_DR_FINAL_GO,
            "safety_gate_dryrun": SAFETY_DR_FINAL_GO,
            "speech_gate_dryrun": SPEECH_DR_FINAL_GO,
            "voice_output_plane_dryrun": VOICE_DR_FINAL_GO,
            "tts_runtime_dryrun": TTS_DR_FINAL_GO,
            "validation_engineering_dryrun": VALIDATION_DR_FINAL_GO,
            "whitebox_dryrun": WHITEBOX_DR_FINAL_GO,
        },
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if report["verifier"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import ast
import json
from pathlib import Path

PHASE_DIR = Path(__file__).resolve().parent

REQUIRED_FILES = {
    "active_observation_control_gap_audit_v1.md",
    "existing_asset_inventory_v1.json",
    "active_observation_control_chain_v1.json",
    "active_observation_owner_matrix_v1.json",
    "provider_autonomy_boundary_v1.json",
    "evidence_sufficiency_boundary_v1.json",
    "historical_failure_regression_suite_v1.json",
    "maturity_gap_matrix_v1.json",
    "abcd_asset_classification_v1.json",
    "integration_handoff_gap_matrix_v1.json",
    "genuine_missing_capability_registry_v1.json",
    "deferred_outside_a_v1.json",
    "recommended_next_module_v1.json",
    "technical_debt_registry_v1.json",
    "phase_contract.json",
    "verify_active_observation_control_gap_audit_v1.py",
}
MATURITY_VALUES = {"COMPLETE", "COMPLETE_WITH_INTEGRATION_GAP", "PARTIAL", "SKELETON_ONLY", "PLANNING_ONLY", "LEGACY_ONLY", "MISSING", "DEFERRED_OUTSIDE_A"}
EXPECTED_NODES = {f"N{i:02d}" for i in range(1, 16)}
EXPECTED_QUESTIONS = {f"Q{i:02d}" for i in range(1, 21)}
EXPECTED_HANDOFFS = {f"H{i:02d}" for i in range(1, 15)}
EXPECTED_REGRESSIONS = {f"R{i:02d}" for i in range(1, 13)}


def _load(name: str):
    return json.loads((PHASE_DIR / name).read_text(encoding="utf-8"))


def _check(check_id: str, passed: bool, detail: str) -> dict:
    return {"check_id": check_id, "passed": bool(passed), "detail": detail}


def run_verification() -> dict:
    checks = []
    actual = {p.name for p in PHASE_DIR.iterdir() if p.is_file()}
    checks.append(_check("AOC01_exact_files", actual == REQUIRED_FILES, "Exact planning package file set."))

    parsed = {}
    parse_ok = True
    for name in sorted(REQUIRED_FILES):
        if name.endswith(".json"):
            try:
                parsed[name] = _load(name)
            except Exception:
                parse_ok = False
    checks.append(_check("AOC02_json_parse", parse_ok, "All JSON assets parse."))
    try:
        ast.parse((PHASE_DIR / "verify_active_observation_control_gap_audit_v1.py").read_text(encoding="utf-8"))
        ast_ok = True
    except (OSError, SyntaxError):
        ast_ok = False
    checks.append(_check("AOC03_verifier_ast", ast_ok, "Verifier parses as AST."))

    contract = parsed.get("phase_contract.json", {})
    checks.append(_check("AOC04_audit_only_contract", contract.get("audit_only") is True and contract.get("planning_only") is True and contract.get("implementation_change") is False and contract.get("runtime_execution") is False and contract.get("source_owner_mutation") is False and contract.get("emotion_engine_development") is False and contract.get("b_route_development") is False and contract.get("semantic_compression") is False, "Audit/planning-only boundaries are frozen."))
    checks.append(_check("AOC05_no_new_capability", contract.get("new_capabilities_directory_created") is False and not (PHASE_DIR.parents[2] / "capabilities/midplatform/core/active_observation_control").exists(), "No Active Observation Control implementation directory is created."))

    inventory = parsed.get("existing_asset_inventory_v1.json", {})
    classes = inventory.get("classifications", {})
    checks.append(_check("AOC06_abcd_inventory", all(classes.get(key) for key in ("A", "B", "C", "D")) and inventory.get("owner_decision") == "B_EXISTING_OWNER_REQUIRES_CONTROLLED_INTEGRATION", "A/B/C/D inventory and existing-owner decision exist."))

    chain = parsed.get("active_observation_control_chain_v1.json", {})
    nodes = chain.get("nodes", [])
    checks.append(_check("AOC07_chain_coverage", {n.get("node_id") for n in nodes} == EXPECTED_NODES and "Observation Demand != Observation Request" in chain.get("semantic_inequalities", []) and "Evidence Sufficiency != Model Confidence" in chain.get("semantic_inequalities", []), "Canonical control chain and inequalities are covered."))

    owner = parsed.get("active_observation_owner_matrix_v1.json", {})
    checks.append(_check("AOC08_owner_matrix", {r.get("question_id") for r in owner.get("rows", [])} == EXPECTED_QUESTIONS and len(owner.get("rows", [])) == 20, "All 20 ownership questions are explicitly assigned or registered as gaps."))

    autonomy = parsed.get("provider_autonomy_boundary_v1.json", {})
    checks.append(_check("AOC09_provider_autonomy", autonomy.get("provider_autonomy_allowed_by_default") is False and len(autonomy.get("forbidden_autonomous_triggers", [])) >= 6 and autonomy.get("safety_exception", {}).get("not_a_general_exception") is True, "Provider autonomy is false by default and safety exception is bounded."))

    sufficiency = parsed.get("evidence_sufficiency_boundary_v1.json", {})
    checks.append(_check("AOC10_sufficiency_boundary", sufficiency.get("inequality") == "Evidence Sufficiency != Model Confidence" and len(sufficiency.get("sufficiency_must_be_relative_to", [])) >= 7 and sufficiency.get("current_status") == "PARTIAL_GENUINE_P0_GAP", "Task-relative sufficiency boundary is explicit."))

    regressions = parsed.get("historical_failure_regression_suite_v1.json", {}).get("cases", [])
    checks.append(_check("AOC11_regression_baseline", {r.get("case_id") for r in regressions} == EXPECTED_REGRESSIONS and all(r.get("expected") for r in regressions), "R01-R12 product regression baseline is complete."))

    maturity = parsed.get("maturity_gap_matrix_v1.json", {}).get("rows", [])
    checks.append(_check("AOC12_maturity_matrix", {r.get("node_id") for r in maturity} == EXPECTED_NODES and all(r.get("maturity") in MATURITY_VALUES and r.get("evidence_refs") for r in maturity), "Every control-chain node has one maturity and evidence."))

    handoffs = parsed.get("integration_handoff_gap_matrix_v1.json", {}).get("handoffs", [])
    checks.append(_check("AOC13_handoff_matrix", {h.get("handoff_id") for h in handoffs} == EXPECTED_HANDOFFS and all(all(key in h for key in ("contract", "adapter", "controlled_handoff", "runtime_handoff", "trace_continuity", "authority_boundary", "status", "gap")) for h in handoffs), "Contract, adapter, controlled handoff, runtime handoff, trace and authority are separated."))

    gaps = parsed.get("genuine_missing_capability_registry_v1.json", {}).get("gaps", [])
    checks.append(_check("AOC14_genuine_gaps", any(g.get("severity") == "P0" for g in gaps) and all(g.get("gap_id") and g.get("recommended_module_or_extension") and g.get("stop_condition") for g in gaps), "Genuine P0/P1 gaps are registered without implementation."))

    deferred = parsed.get("deferred_outside_a_v1.json", {}).get("deferred_outside_a", [])
    deferred_names = {d.get("capability") for d in deferred}
    checks.append(_check("AOC15_deferred_boundary", {"Emotion Engine implementation", "Advanced Emotion Governance runtime", "Semantic compression", "B Route", "Cross-user transfer"}.issubset(deferred_names), "Emotion, semantic synthesis, B Route and transfer remain deferred."))

    recommendation = parsed.get("recommended_next_module_v1.json", {})
    checks.append(_check("AOC16_owner_reuse_recommendation", recommendation.get("new_canonical_owner_required") is False and recommendation.get("owner_decision") == "B_REUSE_EXISTING_FIELD_PERCEPTION_ORCHESTRATOR", "Next module reuses existing owner and avoids parallel owner."))

    debt = parsed.get("technical_debt_registry_v1.json", {}).get("debt_items", [])
    checks.append(_check("AOC17_verifier_debt", any(d.get("classification") == "NON_BLOCKING_VERIFIER_TRACEABILITY_DEBT" for d in debt), "Observation Gateway verifier traceability debt is registered only."))

    text = (PHASE_DIR / "active_observation_control_gap_audit_v1.md").read_text(encoding="utf-8")
    checks.append(_check("AOC18_report_answers", all(token in text for token in ("Provider Autonomy Principle", "Evidence Sufficiency", "R01-R12", "Genuine P0 gaps", "Emotion Engine", "B Route")), "Main audit includes required conclusions and boundaries."))

    passed = sum(1 for item in checks if item["passed"])
    return {
        "phase": "Phase-Luna-A-Route-Active-Observation-Control-Gap-Audit-v1-001",
        "checks": checks,
        "passed_check_count": passed,
        "failed_check_count": len(checks) - passed,
        "blocker_count": sum(1 for item in checks if not item["passed"]),
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }


if __name__ == "__main__":
    print(json.dumps(run_verification(), indent=2, ensure_ascii=False))

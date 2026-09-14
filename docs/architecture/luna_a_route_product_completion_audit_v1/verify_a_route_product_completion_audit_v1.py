from __future__ import annotations

import ast
import json
from pathlib import Path

PHASE_DIR = Path(__file__).resolve().parent
REQUIRED_FILES = {
    "a_route_product_completion_audit_v1.md",
    "a_route_product_completion_matrix_v1.json",
    "a_route_cognitive_brain_gap_matrix_v1.json",
    "a_route_handoff_matrix_v1.json",
    "a_route_product_loop_readiness_v1.json",
    "a_route_missing_capability_registry_v1.json",
    "a_route_deferred_outside_a_v1.json",
    "a_route_future_build_sequence_v1.json",
    "phase_contract.json",
    "verify_a_route_product_completion_audit_v1.py",
}
MATURITY = {"COMPLETE", "COMPLETE_WITH_INTEGRATION_GAP", "PARTIAL", "SKELETON_ONLY", "PLANNING_ONLY", "LEGACY_ONLY", "MISSING", "DEFERRED_OUTSIDE_A"}
DOMAINS = {f"A{i:02d}" for i in range(1, 33)}
LOOP_STEPS = {"Observe", "Understand", "Decide", "Act", "Observe Result", "Compare", "Learn/Experience", "Next Cycle"}
EXPECTED_FALSE = {"runtime_execution", "source_owner_mutation", "implementation_change", "emotion_engine_development", "b_route_development", "database_write", "vector_store_write", "embedding_execution", "model_call", "scheduler_execution", "task_mutation", "device_control", "self_mutation", "personality_mutation", "memory_mutation", "semantic_compression_execution", "cross_user_transfer", "real_side_effect"}


def load(name: str):
    return json.loads((PHASE_DIR / name).read_text(encoding="utf-8"))


def check(condition: bool, check_id: str, detail: str) -> dict:
    return {"check_id": check_id, "passed": bool(condition), "detail": detail}


def run_verification() -> dict:
    actual = {p.name for p in PHASE_DIR.iterdir() if p.is_file()}
    results = [check(actual == REQUIRED_FILES, "A01_exact_files", "Required audit package has exact file set.")]
    docs = {}
    parse_ok = True
    for name in sorted(REQUIRED_FILES):
        if name.endswith(".json"):
            try:
                docs[name] = load(name)
            except Exception:
                parse_ok = False
    results.append(check(parse_ok, "A02_json_parse", "All JSON audit assets parse."))
    try:
        ast.parse((PHASE_DIR / "verify_a_route_product_completion_audit_v1.py").read_text(encoding="utf-8"))
        ast_ok = True
    except SyntaxError:
        ast_ok = False
    results.append(check(ast_ok, "A03_verifier_ast", "Static verifier parses as Python AST."))

    contract = docs.get("phase_contract.json", {})
    flags = contract.get("boundary_flags", {})
    results.append(check(contract.get("execution_mode") == "READ_ONLY_AUDIT_AND_PLANNING_ONLY" and flags.get("audit_only") is True and flags.get("planning_only") is True and all(flags.get(k) is False for k in EXPECTED_FALSE), "A04_audit_contract", "Audit-only and implementation prohibitions are frozen."))
    repo_root = PHASE_DIR.parents[2]
    results.append(check(not (repo_root / "capabilities" / "midplatform" / "core" / "emotion_governance").exists(), "A05_no_emotion_implementation", "No Emotion Governance implementation directory was created."))

    matrix = docs.get("a_route_product_completion_matrix_v1.json", {}).get("domains", [])
    results.append(check({x.get("domain_id") for x in matrix} == DOMAINS and all(x.get("maturity") in MATURITY for x in matrix), "A06_domain_coverage", "All A01-A32 product domains have one valid maturity."))
    results.append(check(all(x.get("domain_name") and x.get("canonical_owner_or_module") and x.get("evidence_refs") for x in matrix), "A07_domain_evidence", "Every domain has owner and evidence references."))

    brain = docs.get("a_route_cognitive_brain_gap_matrix_v1.json", {}).get("mechanisms", [])
    required_brain = {"observation formation", "current-world representation", "relevance / attention", "hypothesis formation", "uncertainty", "contradiction", "expectation", "prediction", "intent continuity", "decision formation", "action consequence expectation", "result comparison", "error recognition", "correction", "experience formation", "learning admission", "self continuity", "personality influence", "cognitive-cycle continuity"}
    results.append(check(required_brain <= {x.get("mechanism") for x in brain} and all(x.get("status") in MATURITY for x in brain), "A08_brain_gap_coverage", "Cognitive brain mechanisms and maturity are recorded."))

    handoffs = docs.get("a_route_handoff_matrix_v1.json", {}).get("handoffs", [])
    results.append(check({x.get("handoff_id") for x in handoffs} == {f"H{i:02d}" for i in range(1, 19)} and all(all(k in x for k in ("producer", "consumer", "contract", "adapter", "controlled_handoff", "runtime_handoff", "trace_continuity", "authority_boundary", "status", "gap")) for x in handoffs), "A09_handoff_coverage", "All major adjacent handoffs distinguish contract, adapter, controlled, and runtime status."))

    loop = docs.get("a_route_product_loop_readiness_v1.json", {}).get("steps", [])
    results.append(check({x.get("step") for x in loop} == LOOP_STEPS and all(x.get("status") in {"READY", "PARTIAL", "BLOCKED", "NOT_REQUIRED"} for x in loop), "A10_loop_coverage", "Product loop readiness covers all required steps."))
    results.append(check(docs.get("a_route_product_loop_readiness_v1.json", {}).get("overall_status") == "BLOCKED", "A11_product_not_complete", "Audit records that A Route is not yet product-complete."))

    gaps = docs.get("a_route_missing_capability_registry_v1.json", {}).get("gaps", [])
    results.append(check(bool(gaps) and all(x.get("severity") in {"P0", "P1", "P2"} for x in gaps) and any(x.get("severity") == "P0" for x in gaps), "A12_genuine_gap_registry", "Genuine P0/P1/P2 gaps are registered."))
    deferred = docs.get("a_route_deferred_outside_a_v1.json", {}).get("deferred", [])
    deferred_names = {x.get("capability") for x in deferred}
    results.append(check({"Emotion Engine implementation", "Advanced Emotion Governance runtime", "B Route", "Advanced semantic compression", "Cross-user cognitive or emotion transfer"} <= deferred_names, "A13_deferred_boundary", "Emotion and B Route boundaries remain deferred."))
    sequence = docs.get("a_route_future_build_sequence_v1.json", {}).get("modules", [])
    results.append(check([x.get("order") for x in sequence] == list(range(1, 10)) and all(x.get("module") and x.get("exit_condition") for x in sequence), "A14_build_sequence", "Future sequence is module-level and ordered."))
    text = (PHASE_DIR / "a_route_product_completion_audit_v1.md").read_text(encoding="utf-8")
    results.append(check("A_ROUTE_PRODUCT_COMPLETE_V1" in text and "Emotion Engine implementation" in text and "not currently" in text, "A15_executive_conclusion", "Main audit answers completion and deferred-boundary questions."))
    passed = sum(1 for x in results if x["passed"])
    return {"phase": "Phase-Luna-A-Route-Product-Completion-Audit-v1-001", "checks": results, "passed_check_count": passed, "failed_check_count": len(results) - passed, "blocker_count": sum(1 for x in results if not x["passed"])}


if __name__ == "__main__":
    print(json.dumps(run_verification(), indent=2, ensure_ascii=False))

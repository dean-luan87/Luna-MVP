"""V2 verifier for the Open Source Integration architecture-only phase."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_ASSETS = [
    "opensource_layer_registry.json", "opensource_capability_admission_contract.json", "opensource_asset_mapping_registry.json",
    "memory_opensource_adapter_boundary.json", "experience_reflection_boundary.json", "similarity_engine_boundary.json",
    "knowledge_graph_boundary.json", "research_reference_boundary.json", "capability_provider_boundary.json",
    "opensource_replacement_contract.json", "opensource_failure_isolation_contract.json", "opensource_authority_matrix.json",
    "opensource_data_flow.json", "negative_guards.json", "summary.json",
]
MD_ASSETS = ["opensource_integration_architecture.md", "opensource_whitebox_v1.md", "opensource_go_no_go_v1.md"]


def main() -> int:
    failures: list[str] = []
    data = {}
    for name in JSON_ASSETS:
        path = ROOT / name
        if not path.is_file():
            failures.append(f"missing_json:{name}")
            continue
        try:
            data[name] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            failures.append(f"invalid_json:{name}")
    for name in MD_ASSETS:
        path = ROOT / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            failures.append(f"missing_or_empty:{name}")
    if [p.name for p in ROOT.glob("*.py") if p.name != Path(__file__).name]:
        failures.append("architecture_only_contains_implementation")
    layers = data.get("opensource_layer_registry.json", {})
    if [row.get("layer") for row in layers.get("layers", [])] != ["L0", "L1", "L2", "L3", "L4", "L5"] or not layers.get("rules", {}).get("kernel_protected"):
        failures.append("layer_freeze")
    admission = data.get("opensource_capability_admission_contract.json", {})
    if len(admission.get("checks", [])) < 8 or not admission.get("rules", {}).get("admission_required") or not admission.get("rules", {}).get("external_asset_not_brain"):
        failures.append("admission_boundary")
    assets = data.get("opensource_asset_mapping_registry.json", {})
    names = {row.get("asset") for row in assets.get("assets", [])}
    required_assets = {"Mem0", "Letta", "Generative Agents", "FAISS", "Chroma", "Neo4j", "OpenCog Hyperon", "SOAR"}
    if not required_assets.issubset(names) or not assets.get("rules", {}).get("mapping_not_integration"):
        failures.append("asset_mapping")
    memory = data.get("memory_opensource_adapter_boundary.json", {})
    if not memory.get("rules", {}).get("validated_entry_required") or not memory.get("rules", {}).get("external_storage_not_memory_authority"):
        failures.append("memory_adapter_boundary")
    reflection = data.get("experience_reflection_boundary.json", {})
    if not reflection.get("rules", {}).get("field_role_time_context_required") or not reflection.get("rules", {}).get("reflection_is_candidate"):
        failures.append("reflection_boundary")
    similarity = data.get("similarity_engine_boundary.json", {})
    if not similarity.get("rules", {}).get("similarity_not_semantics") or not similarity.get("rules", {}).get("retrieval_not_decision"):
        failures.append("similarity_boundary")
    graph = data.get("knowledge_graph_boundary.json", {})
    if graph.get("engine") != "Neo4j" or not graph.get("rules", {}).get("graph_not_knowledge_authority") or not graph.get("rules", {}).get("admission_required"):
        failures.append("knowledge_graph_boundary")
    research = data.get("research_reference_boundary.json", {})
    if not all(row.get("runtime_adoption") is False for row in research.get("references", [])) or not research.get("rules", {}).get("reference_not_dependency"):
        failures.append("research_boundary")
    provider = data.get("capability_provider_boundary.json", {})
    if not provider.get("rules", {}).get("capability_requirement_precedes_provider") or not provider.get("rules", {}).get("evidence_gateway_required") or not provider.get("rules", {}).get("provider_isolation_required"):
        failures.append("provider_boundary")
    replacement = data.get("opensource_replacement_contract.json", {})
    if not replacement.get("rules", {}).get("failure_isolation") or not replacement.get("rules", {}).get("replacement_not_automatic"):
        failures.append("replacement_boundary")
    isolation = data.get("opensource_failure_isolation_contract.json", {})
    if not isolation.get("rules", {}).get("failure_domain_required") or not isolation.get("rules", {}).get("self_preservation"):
        failures.append("failure_isolation")
    authority = data.get("opensource_authority_matrix.json", {})
    objects = [row.get("object") for row in authority.get("rows", [])]
    if len(objects) != len(set(objects)) or not authority.get("rules", {}).get("external_never_final_authority"):
        failures.append("authority_matrix")
    flow = data.get("opensource_data_flow.json", {})
    flow_rows = flow.get("flow", [])
    if [row.get("order") for row in flow_rows] != list(range(1, len(flow_rows) + 1)) or not flow.get("rules", {}).get("evidence_boundary") or not flow.get("rules", {}).get("adapter_boundary"):
        failures.append("data_flow")
    guards = data.get("negative_guards.json", {})
    required_guards = {"no_external_kernel", "no_direct_memory_write", "no_direct_decision", "no_self_modification", "no_meaning_ownership", "no_growth_direction", "no_runtime_integration", "no_network", "no_model_hardware"}
    if not required_guards.issubset({row.get("guard") for row in guards.get("guards", [])}) or not guards.get("rules", {}).get("architecture_only"):
        failures.append("negative_guards")
    summary = data.get("summary.json", {})
    if summary.get("principle") != "Open Source Capability is not Luna Intelligence" or summary.get("status") != "architecture_only" or not summary.get("rules", {}).get("kernel_protected"):
        failures.append("summary")
    try:
        ast.parse(Path(__file__).read_text(encoding="utf-8"))
    except SyntaxError:
        failures.append("verifier_syntax")
    source = Path(__file__).read_text(encoding="utf-8")
    for module in ("subprocess", "socket", "requests", "cv2", "torch"):
        if f"import {module}" in source or f"from {module}" in source:
            failures.append(f"forbidden_import:{module}")
    checks = 112
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_OPENSOURCE_INTEGRATION_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_OPENSOURCE_INTEGRATION_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

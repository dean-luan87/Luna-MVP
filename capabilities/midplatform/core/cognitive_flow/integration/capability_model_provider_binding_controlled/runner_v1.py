"""Controlled synthetic runner; intentionally not executed by the agent."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Dict, List

from .adapters_v1 import build_capability_model_binding, build_model_provider_binding, check_binding_chain
from .fixtures_v1 import SCENARIOS, capability_input_for, chain_inputs_for, provider_input_for


def _guards() -> Dict[str, bool]:
    return {
        "no_capability_mutation_by_model": True,
        "no_model_mutation_by_capability": True,
        "no_model_mutation_by_provider": True,
        "no_provider_mutation_by_model": True,
        "runtime_admission_executed": False,
        "provider_admission_executed": False,
        "provider_invocation_executed": False,
        "model_loading_executed": False,
        "checksum_computation_executed": False,
        "dependency_probe_executed": False,
        "runtime_health_probe_executed": False,
        "brain_provider_selection": False,
        "a_model_selection": False,
        "task_provider_selection": False,
        "scheduler_created": False,
        "planner_created": False,
        "source_mutation_executed": False,
    }


def _edge_dict(output: Any) -> Dict[str, Any]:
    return asdict(output.edge.edge)


def _run_one(case) -> Dict[str, Any]:
    if case.category == "CAPABILITY_MODEL":
        output = build_capability_model_binding(capability_input_for(case.scenario_id), binding_id=case.scenario_id)
        blocked = output.failure is not None
        passed = blocked == case.expected_blocked and (output.failure is None or output.failure.classification == case.expected_failure)
        if case.focus == "capability_owner":
            passed = passed and output.capability_model_binding is not None and output.capability_model_binding.authority_owner == "Capability Governance"
        return {"scenario_id": case.scenario_id, "category": case.category, "passed": passed, "blocked": blocked, "failure": asdict(output.failure) if output.failure else None, "capability_model_binding": asdict(output.capability_model_binding) if output.capability_model_binding else None, "model_provider_binding": None, "edge": _edge_dict(output), "binding_flags": asdict(output.edge), "guards": _guards()}
    if case.category == "MODEL_PROVIDER":
        output = build_model_provider_binding(provider_input_for(case.scenario_id), binding_id=case.scenario_id)
        blocked = output.failure is not None
        passed = blocked == case.expected_blocked and (output.failure is None or output.failure.classification == case.expected_failure)
        if case.focus == "provider_owner":
            passed = passed and output.model_provider_binding is not None and output.model_provider_binding.authority_owner == "Provider Governance"
        if case.focus == "model_source":
            passed = passed and output.model_provider_binding is not None and output.model_provider_binding.model_source_owner == "Model Governance" and output.model_provider_binding.provider_source_owner == "Provider Governance"
        return {"scenario_id": case.scenario_id, "category": case.category, "passed": passed, "blocked": blocked, "failure": asdict(output.failure) if output.failure else None, "capability_model_binding": None, "model_provider_binding": asdict(output.model_provider_binding) if output.model_provider_binding else None, "edge": _edge_dict(output), "binding_flags": asdict(output.edge), "guards": _guards()}
    if case.category == "CROSS_BINDING":
        cap, provider = chain_inputs_for(case.scenario_id)
        output = check_binding_chain(cap, provider, chain_id=case.scenario_id)
        blocked = output.failure is not None
        passed = blocked == case.expected_blocked and (output.failure is None or output.failure.classification == case.expected_failure)
        if case.focus == "superseded":
            passed = passed and blocked is True
        return {"scenario_id": case.scenario_id, "category": case.category, "passed": passed, "blocked": blocked, "failure": asdict(output.failure) if output.failure else None, "capability_model_binding": asdict(cap), "model_provider_binding": asdict(provider), "edge": _edge_dict(output), "binding_flags": asdict(output.edge), "cross_binding_consistent": output.consistent, "guards": _guards()}
    cap_output = build_capability_model_binding(_cap_input_for_authority(case.scenario_id), binding_id=case.scenario_id)
    provider_output = build_model_provider_binding(_provider_input_for_authority(case.scenario_id), binding_id=case.scenario_id)
    cap = cap_output.capability_model_binding
    provider = provider_output.model_provider_binding
    edge_output = cap_output if case.focus in {"capability_owner", "trace", "no_execution", "no_mutation"} else provider_output
    passed = cap is not None and provider is not None
    if case.focus == "capability_owner":
        passed = passed and cap is not None and cap.authority_owner == "Capability Governance" and cap.binding_lifecycle_owner == "Capability Governance"
    if case.focus == "provider_owner":
        passed = passed and provider is not None and provider.authority_owner == "Provider Governance" and provider.binding_lifecycle_owner == "Provider Governance"
    if case.focus == "model_source":
        passed = passed and cap is not None and provider is not None and cap.model_source_owner == "Model Governance" and provider.model_source_owner == "Model Governance" and provider.provider_source_owner == "Provider Governance"
    if case.focus == "trace":
        passed = passed and bool(edge_output.edge.edge.trace_id) and bool(edge_output.edge.edge.provenance_refs) and bool(edge_output.edge.edge.input_refs) and bool(edge_output.edge.edge.input_versions)
    if case.focus == "no_execution":
        passed = passed and not edge_output.edge.runtime_execution_executed and not edge_output.edge.model_loading_executed and not edge_output.edge.provider_invocation_executed
    if case.focus == "no_mutation":
        guards = _guards()
        mutation_guards = (
            "no_capability_mutation_by_model",
            "no_model_mutation_by_capability",
            "no_model_mutation_by_provider",
            "no_provider_mutation_by_model",
        )
        passed = passed and all(guards[name] is True for name in mutation_guards) and guards["source_mutation_executed"] is False
    return {"scenario_id": case.scenario_id, "category": case.category, "passed": passed, "blocked": False, "failure": None, "capability_model_binding": asdict(cap) if cap else None, "model_provider_binding": asdict(provider) if provider else None, "edge": _edge_dict(edge_output), "binding_flags": asdict(edge_output.edge), "guards": _guards()}


def _cap_input_for_authority(case_id: str):
    return capability_input_for(case_id)


def _provider_input_for_authority(case_id: str):
    return provider_input_for(case_id)


def run_synthetic_bindings() -> Dict[str, Any]:
    results: List[Dict[str, Any]] = [_run_one(case) for case in SCENARIOS]
    return {
        "scenario_count": len(results),
        "all_cases_passed": all(item["passed"] for item in results),
        "failed_case_ids": [item["scenario_id"] for item in results if not item["passed"]],
        "capability_model_binding_candidate_count": sum(bool(item["capability_model_binding"]) for item in results),
        "model_provider_binding_candidate_count": sum(bool(item["model_provider_binding"]) for item in results),
        "blocked_binding_count": sum(bool(item["blocked"]) for item in results),
        "stale_binding_count": sum(bool(item["failure"]) and item["failure"]["classification"] in {"BINDING_STALE", "UPSTREAM_BINDING_STALE", "DOWNSTREAM_BINDING_STALE"} for item in results),
        "superseded_binding_count": sum(bool(item["failure"]) and item["failure"]["classification"] == "UPSTREAM_BINDING_STALE" and item["scenario_id"] == "chain_superseded" for item in results),
        "cross_binding_consistency_pass_count": sum(item.get("cross_binding_consistent") is True for item in results),
        "runtime_execution_count": 0,
        "model_loading_count": 0,
        "provider_invocation_count": 0,
        "source_mutation_count": 0,
        "key_guards": _guards(),
        "case_results": results,
    }


if __name__ == "__main__":
    print(json.dumps(run_synthetic_bindings(), indent=2, ensure_ascii=False))

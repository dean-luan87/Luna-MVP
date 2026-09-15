"""Verifier for Provider Binding → Allocation → Execution Instance."""

from __future__ import annotations

import json
import argparse
from pathlib import Path
from typing import Any

from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import compute_unified_final_decision
from capabilities.evaluation.common.artifact_source_binding_v1 import (
    verify_binding,
)
from capabilities.evaluation.common.verification_trust_composition_v1 import (
    compose_verification_trust,
    legacy_provenance_status,
)

from .fixtures_v1 import build_provider_binding_runtime_allocation_execution_cases_v1


SUMMARY_PATH = Path("_eval_out/provider_binding_runtime_allocation_execution_instance_v1/runner_summary_v1.json")


def _check(checks: dict[str, bool], name: str, value: bool) -> None:
    checks[name] = bool(value)


def _cases(summary: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], tuple[str, ...]]:
    raw_cases = summary.get("cases")
    if not isinstance(raw_cases, list):
        return {}, ("cases_missing_or_wrong_type",)
    cases: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for index, item in enumerate(raw_cases):
        if not isinstance(item, dict):
            errors.append(f"case_{index}_wrong_type")
            continue
        case_id = item.get("case_id")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"case_{index}_identity_missing")
            continue
        if case_id in cases:
            errors.append(f"duplicate_case_id:{case_id}")
            continue
        cases[case_id] = item
    return cases, tuple(errors)


def _list(value: Any) -> list[dict[str, Any]]:
    return value if isinstance(value, list) else []


def verify(
    summary: dict[str, Any],
    *,
    binding_claim: dict[str, Any] | None = None,
    artifact_path: Path | None = None,
    repo_root: Path | None = None,
    binding_result: Any = None,
) -> dict[str, Any]:
    """Verify semantics and derive provenance only from raw binding inputs.

    ``binding_result`` is retained as an ignored compatibility keyword. A
    caller-supplied result, including one that claims trust, is never used as
    authority; callers must provide the raw claim and artifact path.
    """
    checks: dict[str, bool] = {}
    expected_cases = build_provider_binding_runtime_allocation_execution_cases_v1()
    actual, case_errors = _cases(summary)
    expected_ids = {case.case_id for case in expected_cases}
    _check(checks, "case_identity_valid", not case_errors and set(actual) == expected_ids)
    _check(checks, "required_cases_present", not case_errors and expected_ids <= set(actual))
    _check(checks, "controlled_marker", summary.get("source_mode") == "controlled_provider_binding_runtime_allocation_execution_instance")
    _check(checks, "governance_backbone_reused", summary.get("governance_backbone_reused") is True)
    _check(checks, "preflight_before_business_engine", summary.get("preflight_before_business_engine") is True)
    _check(checks, "provider_owner", summary.get("canonical_provider_binding_owner") == "Provider Governance")
    _check(checks, "allocation_owner", summary.get("canonical_runtime_allocation_owner") == "Runtime Executor")
    _check(checks, "execution_owner", summary.get("canonical_execution_instance_owner") == "Runtime Executor")
    _check(checks, "authoritative_records", summary.get("provider_binding_authoritative") is True and summary.get("runtime_allocation_authoritative") is True and summary.get("execution_instance_authoritative") is True)
    _check(checks, "synthetic_controlled", summary.get("synthetic_controlled_no_real_resource_effect") is True)
    _check(checks, "no_runtime", all(summary.get(field) is False for field in ("runtime_started", "provider_session_started", "provider_invocation", "model_invocation", "gateway_submission", "observation_produced", "evidence_produced")))
    _check(checks, "no_truth", summary.get("truth_declared") is False and summary.get("world_truth_declared") is False)

    for case in expected_cases:
        item = actual.get(case.case_id, {})
        preflight = item.get("governance_preflight") or {}
        binding = item.get("binding_decision") or {}
        allocation = item.get("allocation") or {}
        instance = item.get("execution_instance") or {}
        if case.profile is not None and not case.profile.governance_profiles:
            _check(checks, f"{case.case_id}:preflight_blocked", item.get("business_engine_executed") is False and preflight.get("status") == "GOVERNANCE_PREFLIGHT_BLOCKED")
            continue
        if case.expected_preflight_status == "GOVERNANCE_PREFLIGHT_BLOCKED":
            blocked = item.get("business_engine_executed") is False and preflight.get("status") == "GOVERNANCE_PREFLIGHT_BLOCKED"
            _check(checks, f"{case.case_id}:preflight_pass", blocked)
            _check(checks, f"{case.case_id}:binding_status", binding == {})
            decisions = _list(binding.get("decisions"))
            _check(checks, f"{case.case_id}:binding_count", len(decisions) == 0)
            _check(checks, f"{case.case_id}:bound_count", sum(1 for d in decisions if d.get("provider_bound") is True) == 0)
            _check(checks, f"{case.case_id}:allocation_status", allocation == {})
            records = _list(allocation.get("records"))
            _check(checks, f"{case.case_id}:allocation_count", len(records) == 0)
            _check(checks, f"{case.case_id}:allocated_count", sum(1 for r in records if r.get("allocation_status") == "ALLOCATED") == 0)
            _check(checks, f"{case.case_id}:instance_status", instance == {})
            instances = _list(instance.get("instances"))
            _check(checks, f"{case.case_id}:instance_count", len(instances) == 0)
            continue
        _check(checks, f"{case.case_id}:preflight_pass", preflight.get("status") == "PASS")
        _check(checks, f"{case.case_id}:binding_status", binding.get("formation_status", "NO_PROVIDER_BINDING_DECISION") == case.expected_binding_status)
        decisions = _list(binding.get("decisions"))
        _check(checks, f"{case.case_id}:binding_count", len(decisions) == case.expected_binding_count)
        _check(checks, f"{case.case_id}:bound_count", sum(1 for d in decisions if d.get("provider_bound") is True) == case.expected_bound_count)
        _check(checks, f"{case.case_id}:allocation_status", allocation.get("formation_status", "NO_RUNTIME_ALLOCATION_RECORD") == case.expected_allocation_status)
        records = _list(allocation.get("records"))
        _check(checks, f"{case.case_id}:allocation_count", len(records) == case.expected_allocation_count)
        _check(checks, f"{case.case_id}:allocated_count", sum(1 for r in records if r.get("allocation_status") == "ALLOCATED") == case.expected_allocated_count)
        _check(checks, f"{case.case_id}:instance_status", instance.get("formation_status", "NO_EXECUTION_INSTANCE") == case.expected_instance_status)
        instances = _list(instance.get("instances"))
        _check(checks, f"{case.case_id}:instance_count", len(instances) == case.expected_instance_count)

    single = actual.get("PROVIDER_ONLY_BINDING_BOUND", {})
    _check(checks, "provider_only_binding", all(d.get("source_model_ref") is None for d in _list((single.get("binding_decision") or {}).get("decisions"))))
    model = actual.get("MODEL_REF_CARRY_FORWARD_BINDING", {})
    _check(checks, "explicit_model_carry_forward", {d.get("source_model_ref") for d in _list((model.get("binding_decision") or {}).get("decisions"))} == {"model:controlled:explicit"})
    _check(checks, "no_model_inference", all(d.get("source_model_ref") is None for d in _list((actual.get("MODEL_NOT_INFERRED", {}).get("binding_decision") or {}).get("decisions"))))

    multiple = actual.get("MULTIPLE_PROVIDER_DISTINCT_BINDINGS", {})
    multiple_decisions = _list((multiple.get("binding_decision") or {}).get("decisions"))
    _check(checks, "multiple_provider_bindings_retained", len(multiple_decisions) == 2 and len({d.get("provider_ref") for d in multiple_decisions}) == 2)
    same_provider = actual.get("SAME_PROVIDER_MULTI_DEMAND", {})
    same_provider_decisions = _list((same_provider.get("binding_decision") or {}).get("decisions"))
    _check(checks, "same_provider_multi_demand_distinct", len(same_provider_decisions) == 2 and len({d.get("source_observation_demand_ref") for d in same_provider_decisions}) == 2 and len({d.get("binding_ref") for d in same_provider_decisions}) == 2)
    _check(checks, "execution_instance_unique", len({item.get("execution_instance_ref") for item in _list((multiple.get("execution_instance") or {}).get("instances"))}) == 2)

    resource = actual.get("RESOURCE_UNAVAILABLE", {})
    _check(checks, "resource_unavailable_no_active_allocation", all(r.get("allocation_status") != "ALLOCATED" for r in _list((resource.get("allocation") or {}).get("records"))))
    released = actual.get("ALLOCATION_RELEASED", {})
    _check(checks, "allocation_release_recorded", all(r.get("allocation_status") == "RELEASED" for r in _list((released.get("allocation") or {}).get("records"))))
    denied = actual.get("ALLOCATION_DENIED", {})
    _check(checks, "allocation_denied_recorded", all(r.get("allocation_status") == "DENIED" and r.get("failure_owner_ref") == "Resource Governance" for r in _list((denied.get("allocation") or {}).get("records"))))
    failed = actual.get("ALLOCATION_FAILED", {})
    _check(checks, "allocation_failed_recorded", all(r.get("allocation_status") == "FAILED" and r.get("failure_owner_ref") == "Resource Governance" for r in _list((failed.get("allocation") or {}).get("records"))))
    _check(checks, "grant_is_hard_prerequisite", all(not any(d.get("decision") == "GRANTED" for d in _list((item.get("grant") or {}).get("decisions"))) and (item.get("binding_decision") or {}) == {} and (item.get("allocation") or {}) == {} for item in (actual.get("DENIED_GRANT_BLOCKS_ALLOCATION", {}), actual.get("EXPIRED_GRANT_BLOCKS_ALLOCATION", {}), actual.get("REVOKED_GRANT_BLOCKS_ALLOCATION", {}), actual.get("STALE_GRANT_BLOCKS_ALLOCATION", {}))))
    _check(checks, "grant_rechecked_before_instance", (actual.get("GRANT_RECHECK_BEFORE_INSTANCE", {}).get("execution_instance") or {}).get("formation_status") == "INVALID_INPUT")
    _check(checks, "binding_revoke_blocks_instance", (actual.get("BINDING_REVOKED_BEFORE_INSTANCE", {}).get("execution_instance") or {}).get("instances", []) == [])
    _check(checks, "allocation_required_before_instance", (actual.get("ALLOCATION_REQUIRED_BEFORE_INSTANCE", {}).get("execution_instance") or {}) == {})

    for case_id in ("SCENARIO12_SIGNAGE", "SCENARIO12_HUMAN_FLOW", "SCENARIO12_INDEPENDENT_BINDING_PATHS"):
        _check(checks, f"{case_id}:abstract_provider", not any(token in json.dumps(actual.get(case_id, {})).lower() for token in ("ocr", "vlm", "yolo", "slam", "camera")))
    scenario = actual.get("SCENARIO12_INDEPENDENT_BINDING_PATHS", {})
    _check(checks, "scenario12_independent_execution_paths", len(_list((scenario.get("execution_instance") or {}).get("instances"))) == 2)

    _check(checks, "all_binding_decisions_authoritative", all(d.get("authoritative") is True and d.get("owner_ref") == "Provider Governance" and d.get("authority_ref") == "authority:provider-binding-decision" for item in actual.values() for d in _list((item.get("binding_decision") or {}).get("decisions"))))
    _check(checks, "all_allocations_authoritative_synthetic", all(r.get("authoritative") is True and r.get("synthetic") is True and r.get("controlled") is True and r.get("no_real_resource_effect") is True for item in actual.values() for r in _list((item.get("allocation") or {}).get("records"))))
    _check(checks, "all_instances_authoritative_created_not_started", all(i.get("authoritative") is True and i.get("execution_started") is False and i.get("provider_session_started") is False and i.get("provider_invoked") is False and i.get("model_invoked") is False and i.get("gateway_submission") is False for item in actual.values() for i in _list((item.get("execution_instance") or {}).get("instances"))))
    _check(checks, "no_resource_identity_selection", all(not any(value.startswith(("gpu:", "worker:", "pid:")) for value in r.get("resource_identity_refs", [])) for item in actual.values() for r in _list((item.get("allocation") or {}).get("records"))))
    _check(checks, "lineage_preserved", all(d.get("source_binding_candidate_ref") and d.get("source_runtime_grant_ref") and d.get("lineage_refs") for item in actual.values() for d in _list((item.get("binding_decision") or {}).get("decisions")) if d.get("provider_bound")) and all(i.get("source_allocation_ref") and i.get("source_runtime_grant_ref") and i.get("source_provider_binding_ref") and i.get("lineage_refs") for item in actual.values() for i in _list((item.get("execution_instance") or {}).get("instances"))))
    _check(checks, "allocation_requires_granted_fresh", all(r.get("source_runtime_grant_ref") and r.get("allocation_status") in {"ALLOCATED", "DENIED", "FAILED", "RELEASED"} for item in actual.values() for r in _list((item.get("allocation") or {}).get("records"))))
    _check(checks, "upstream_snapshots_unchanged", all(item.get("target_request_snapshot_before") == item.get("target_request_snapshot_after") for item in actual.values()))
    deterministic = actual.get("DETERMINISTIC_REPLAY", {})
    _check(checks, "deterministic_replay", deterministic.get("deterministic_replay") == deterministic.get("execution_instance"))
    _check(checks, "malformed_input_fails_closed", (actual.get("MALFORMED_INPUT_FAIL_CLOSED", {}).get("target_preparation") or {}).get("formation_status") == "INVALID_INPUT" and (actual.get("MALFORMED_INPUT_FAIL_CLOSED", {}).get("binding_decision") or {}) == {})
    _check(checks, "authority_responsibility_governed", all((item.get("governance_preflight") or {}).get("status") == "PASS" for item in actual.values() if item.get("business_engine_executed") is True))
    _check(checks, "no_authority_without_responsibility", (actual.get("AUTHORITY_WITHOUT_RESPONSIBILITY_BLOCKED", {}).get("governance_preflight") or {}).get("status") == "GOVERNANCE_PREFLIGHT_BLOCKED")
    _check(checks, "no_applicable_rules_fail_closed", (actual.get("NO_APPLICABLE_RULES_FAIL_CLOSED", {}).get("governance_preflight") or {}).get("status") == "GOVERNANCE_PREFLIGHT_BLOCKED")

    functional = all(checks.values())
    governance_preflight = "PASS" if all((item.get("governance_preflight") or {}).get("status") == "PASS" or item.get("business_engine_executed") is False for item in actual.values()) else "GOVERNANCE_PREFLIGHT_BLOCKED"
    governance_postflight = "PASS" if all((item.get("governance_postflight") or {}).get("status") == "PASS" for item in actual.values() if item.get("business_engine_executed") is True) else "GOVERNANCE_POSTFLIGHT_BLOCKED"
    contract_failures = tuple(name for name, passed in checks.items() if not passed)
    cognitive = "PASS" if functional else "FAIL"
    operational = "PASS" if functional else "FAIL"
    binding_result = None
    if binding_claim is not None and artifact_path is not None:
        binding_result = verify_binding(
            binding_claim,
            repo_root=repo_root or Path(__file__).resolve().parents[4],
            artifact_path=artifact_path,
        )
    trust = compose_verification_trust(semantic_passed=functional, binding_result=binding_result)
    provenance_trusted = trust.trusted_current_evidence
    trusted_functional = trust.trusted_current_evidence
    provenance_status = legacy_provenance_status(trust)
    trusted_failures = contract_failures if functional else contract_failures
    if not provenance_trusted:
        trusted_failures = (*trusted_failures, "provenance_binding")
    final_decision = compute_unified_final_decision(functional_checks_passed=trusted_functional, contract_failures=trusted_failures, governance_preflight=governance_preflight, governance_postflight=governance_postflight, cognitive_logic_result=cognitive, operational_result=operational)
    return {
        "check_count": len(checks), "passed_count": sum(1 for passed in checks.values() if passed),
        "failed_checks": [name for name, passed in checks.items() if not passed], "all_checks_passed": functional,
        "contract_failures": list(contract_failures), "governance_preflight": governance_preflight,
        "governance_postflight": governance_postflight, "cognitive_logic_result": cognitive,
        "operational_result": operational, "final_decision": final_decision,
        "status": "VERIFIED_ARTIFACT_RESULT",
        "provenance_status": provenance_status,
        "trust_state": trust.state,
        "trusted_current_evidence": trusted_functional,
        "controlled_scope_passed": functional,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=SUMMARY_PATH)
    parser.add_argument("--binding", type=Path)
    args = parser.parse_args()
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    binding_claim = None
    if args.binding is not None:
        binding_claim = json.loads(args.binding.read_text(encoding="utf-8"))
    result = verify(
        summary,
        binding_claim=binding_claim,
        artifact_path=args.summary if binding_claim is not None else None,
        repo_root=Path(__file__).resolve().parents[4],
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["final_decision"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())

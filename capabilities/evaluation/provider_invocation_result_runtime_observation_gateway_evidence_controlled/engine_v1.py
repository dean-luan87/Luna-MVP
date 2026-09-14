"""Controlled execution-result to Runtime Observation/Gateway/Evidence engine."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass, replace
from typing import Any

from capabilities.evaluation.provider_binding_runtime_allocation_execution_instance_controlled.fixtures_v1 import (
    build_provider_binding_runtime_allocation_execution_cases_v1,
)
from capabilities.evaluation.provider_session_controlled_invocation_multiscenario_sandbox.engine_v1 import (
    _source_chain,
)
from capabilities.evaluation.provider_session_controlled_invocation_multiscenario_sandbox.fixtures_v1 import (
    SessionCaseV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)
from capabilities.midplatform.core.observation_runtime_ingress.adapters_v1 import (
    build_gateway_request,
)
from capabilities.midplatform.core.observation_runtime_ingress.types_v1 import (
    RuntimeObservationIngressCaseV1,
)
from capabilities.midplatform.core.provider_runtime_to_observation_ingress.provider_invocation_result_adapter_v1 import (
    form_runtime_observation_from_invocation_result,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_session_invocation_v1 import (
    ProviderInvocationInputV1,
    ProviderRuntimeSessionInputV1,
    ProviderInvocationResultV1,
    create_provider_runtime_session,
    start_controlled_provider_invocation,
)
from capabilities.midplatform.protocol_manager.module.governance_verification_backbone_v1 import (
    CORE_GOVERNANCE_RULE_REGISTRY_V1,
    resolve_applicable_governance_set,
    run_governance_postflight,
    run_governance_preflight,
)

from .fixtures_v1 import (
    CONTEXT,
    EVALUATION_MARKER,
    PHASE,
    IntegrationCaseV1,
    build_provider_invocation_observation_evidence_cases_v1,
    valid_authority_records,
    valid_profile,
)


def _json_safe(value: Any) -> Any:
    if is_dataclass(value):
        return _json_safe(asdict(value))
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    return value


def _gateway_case(case: IntegrationCaseV1, observation: Any, index: int) -> Any:
    if observation is None:
        return None
    current = observation
    if case.gateway_malformed_observation:
        current = replace(current, capability_ref="")
    if case.gateway_lineage_mismatch:
        current = replace(current, execution_instance_ref="execution:other")
    if case.gateway_unknown_provider:
        current = replace(current, provider_ref="")
    return RuntimeObservationIngressCaseV1(
        case_id=f"{case.case_id}:{index}",
        title="controlled invocation result ingress",
        observation=current,
        context_ref=CONTEXT[0],
        pcn_ref=f"pcn:controlled:{case.case_id.lower()}:{index}",
        intent_ref=f"intent:controlled:{case.case_id.lower()}:{index}",
        role_refs=("role:controlled-evaluation",),
        task_refs=(),
        goal_refs=(),
        concern_refs=(),
        information_need_refs=(),
        field_refs=(),
        relation_refs=(),
        required_information_refs=(),
        available_information_refs=(),
        synthetic_only=True,
        controlled_integration_only=True,
        candidate_only=True,
    )


def _lifecycle_artifact(
    observations: list[Any],
    gateways: list[Any],
    evidence: list[Any],
    truth_attempt: bool,
) -> dict[str, Any]:
    return {
        "candidate_only": True,
        "read_only": True,
        "truth_declared": truth_attempt,
        "world_truth_declared": truth_attempt,
        "runtime_started": False,
        "execution_instance_created": False,
        "provider_session_started": False,
        "resource_allocated": False,
        "runtime_observation_created": bool(observations),
        "gateway_submission": False,
        "evidence_created": bool(evidence),
        "authoritative_effects": False,
        "mutation_effects": False,
        "gateway_admitted": any(item.admission_state == "ADMITTED_OBSERVATION" for item in gateways),
    }


class ProviderInvocationObservationGatewayEvidenceEvaluationEngineV1:
    def run(self) -> dict[str, Any]:
        profile = valid_profile()
        source_cases = {
            item.case_id: item
            for item in build_provider_binding_runtime_allocation_execution_cases_v1()
        }
        results = []
        for case in build_provider_invocation_observation_evidence_cases_v1():
            records = case.authority_records or valid_authority_records()
            applicable = resolve_applicable_governance_set(profile, CORE_GOVERNANCE_RULE_REGISTRY_V1)
            preflight = run_governance_preflight(
                profile,
                CORE_GOVERNANCE_RULE_REGISTRY_V1,
                records,
                tuple(profile.protocol_refs),
            )
            source_ids = case.source_case_ids or (case.source_case_id,)
            source_chains: list[dict[str, Any]] = []
            sessions: list[Any] = []
            invocation_results: list[ProviderInvocationResultV1] = []
            formation_results: list[Any] = []
            observations: list[Any] = []
            gateways: list[Any] = []
            evidence: list[Any] = []
            if preflight.status == "PASS":
                for index, source_id in enumerate(source_ids, start=1):
                    source_case = source_cases[source_id]
                    session_case = SessionCaseV1(
                        case_id=f"{case.case_id.lower()}:{index}",
                        source_case_id=source_id,
                    )
                    source = _source_chain(session_case, source_case)
                    source_chains.append(source)
                    binding = source["binding_decisions"].decisions[0]
                    grant = source["grant"].decisions[0]
                    allocation = source["allocation"].records[0]
                    instance = source["instances"].instances[0]
                    session_result = create_provider_runtime_session(
                        ProviderRuntimeSessionInputV1(
                            session_request_ref=f"session:{case.case_id.lower()}:{index}",
                            execution_instance=instance,
                            provider_binding=binding,
                            runtime_grant=grant,
                            runtime_allocation=allocation,
                            trace_ref=f"trace:session:{case.case_id.lower()}:{index}",
                            provenance_refs=(f"provenance:session:{case.case_id.lower()}:{index}",),
                        )
                    )
                    if session_result.session is None:
                        continue
                    sessions.append(session_result.session)
                    if not case.invoke:
                        continue
                    invocation_result = start_controlled_provider_invocation(
                        ProviderInvocationInputV1(
                            invocation_request_ref=f"invocation:{case.case_id.lower()}:{index}",
                            session=session_result.session,
                            execution_instance=instance,
                            provider_binding=binding,
                            runtime_grant=grant,
                            runtime_allocation=allocation,
                            outcome=case.outcome,
                            trace_ref=f"trace:invocation:{case.case_id.lower()}:{index}",
                            provenance_refs=(f"provenance:invocation:{case.case_id.lower()}:{index}",),
                        )
                    )
                    if case.malformed_invocation_result:
                        invocation_result = replace(invocation_result, invocation=None)
                    invocation_results.append(invocation_result)
                    formation = form_runtime_observation_from_invocation_result(invocation_result)
                    formation_results.append(formation)
                    if formation.observation is None:
                        continue
                    observation_case = _gateway_case(case, formation.observation, index)
                    if observation_case is None:
                        continue
                    gateway_request = build_gateway_request(observation_case)
                    if case.gateway_lineage_mismatch:
                        gateway_request = replace(
                            gateway_request,
                            execution_identity_ref=f"execution:gateway-mismatch:{case.case_id.lower()}:{index}",
                        )
                    if case.gateway_unknown_provider:
                        gateway_request = replace(gateway_request, missing_provider=True)
                    if case.duplicate_observation:
                        gateway_request = replace(gateway_request, duplicate_observation=True)
                    gateway = ObservationGatewayEngineV1().run_case(gateway_request)
                    gateways.append(gateway)
                    if case.replay:
                        gateways.append(ObservationGatewayEngineV1().run_case(gateway_request))
                    if gateway.admission_state == "ADMITTED_OBSERVATION":
                        evidence.extend(gateway.evidence)
                    observations.append(formation.observation) if gateway.admission_state == "ADMITTED_OBSERVATION" else None
            artifact = _lifecycle_artifact(observations, gateways, evidence, case.truth_attempt)
            postflight = (
                run_governance_postflight(profile, artifact)
                if preflight.status == "PASS"
                else None
            )
            first_formation = formation_results[0] if formation_results else None
            first_gateway = gateways[0] if gateways else None
            results.append(
                {
                    "case_id": case.case_id,
                    "expected": _json_safe(case),
                    "applicable_governance": _json_safe(applicable),
                    "governance_preflight": _json_safe(preflight),
                    "governance_postflight": _json_safe(postflight),
                    "business_engine_executed": preflight.status == "PASS",
                    "source_chains": _json_safe(source_chains),
                    "sessions": _json_safe(sessions),
                    "invocation_results": _json_safe(invocation_results),
                    "observation_formation": _json_safe(first_formation),
                    "observation_formations": _json_safe(formation_results),
                    "runtime_observation": _json_safe(first_formation.observation if first_formation else None),
                    "gateways": _json_safe(gateways),
                    "gateway": _json_safe(first_gateway),
                    "evidence": _json_safe(evidence),
                    "observation_count": len(observations),
                    "evidence_count": len(evidence),
                    "lifecycle_artifact": artifact,
                }
            )
        return {
            "phase": PHASE,
            "source_mode": EVALUATION_MARKER,
            "governance_backbone_reused": True,
            "canonical_observation_owner": "Provider Runtime Observation Integration",
            "canonical_gateway_owner": "Observation Gateway Governance",
            "canonical_evidence_owner": "Observation Gateway Governance",
            "adapter_semantic_authority": False,
            "synthetic_only": True,
            "controlled": True,
            "no_real_provider_effect": True,
            "no_real_model_effect": True,
            "network_called": False,
            "subprocess_started": False,
            "thread_started": False,
            "socket_used": False,
            "provider_invoked": False,
            "model_invoked": False,
            "runtime_observation_created": True,
            "gateway_submission": False,
            "evidence_created": True,
            "truth_declared": False,
            "world_truth_declared": False,
            "evidence_sufficiency_decided": False,
            "current_world_mutated": False,
            "field_mutated": False,
            "context_mutated": False,
            "memory_mutated": False,
            "experience_mutated": False,
            "cases": results,
            "controlled_case_count": len(results),
            "status": "READY_FOR_USER_VERIFICATION",
        }


__all__ = ["ProviderInvocationObservationGatewayEvidenceEvaluationEngineV1"]

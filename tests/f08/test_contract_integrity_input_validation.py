"""Adversarial F-08 contract-boundary tests.

These tests exercise rejection at owner boundaries and preserve the distinction
between invalid structure and semantic uncertainty.  They are intentionally
not run by the implementation agent; the user terminal owns execution.
"""

from dataclasses import fields as dataclass_fields, replace
from pathlib import Path

import pytest

from capabilities.evaluation.full_end_to_end_cognitive_logic_conformance_regression.fixtures_v1 import (
    build_request_v1,
    build_replay_inputs_v1,
    get_contrast_specs_v1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_static_validators_v1 import (
    validate_request_shape,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_engine_v1 import (
    CognitiveStateFormationEngineV1,
)
from capabilities.midplatform.core.context_foundation.context_foundation_static_validators_v1 import (
    validate_projection_reference_complete,
)
from capabilities.midplatform.core.context_foundation.context_projection_types_v1 import (
    ProjectionReferenceV1,
)
from capabilities.midplatform.core.evidence_to_field_event_adapter_v1 import (
    form_field_event_candidate_from_evidence,
)
from capabilities.midplatform.core.field_event_admission_api_v1 import admit_field_event
from capabilities.midplatform.core.field_event_admission_types_v1 import AdmissionPolicyV1
from capabilities.midplatform.core.field_state_read_model.module.field_state_read_model_query_validator_v1 import (
    validate_query_v1,
)
from capabilities.midplatform.core.field_state_read_model.module.field_state_read_model_projection_builder_v1 import (
    validate_state_candidate_v1,
)
from capabilities.midplatform.core.field_state_reducer.module.field_state_reducer_module_input_adapter_v1 import (
    adapt_module_input_v1,
)
from capabilities.midplatform.core.field_state_reducer.module.field_state_reducer_module_types_v1 import (
    FieldStateReducerModuleRequestV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_static_validators_v1 import (
    validate_ingress_request_shape,
)
from capabilities.midplatform.core.execution_mode_v1 import ControlledReplayInputV1
from capabilities.midplatform.core.runtime_executor.runtime_allocation_preparation_candidate_v1 import (
    RuntimeAllocationPreparationInputV1,
    form_runtime_allocation_preparation_candidates,
)
from capabilities.midplatform.core.task_manager.module.task_manager_module_input_adapter_v1 import (
    adapt_task_manager_input_v1,
)
from capabilities.midplatform.provider_runtime_governance.provider_binding_runtime_preparation_v1 import (
    ProviderBindingRuntimePreparationInputV1,
    form_provider_binding_runtime_preparation_candidates,
)


def _valid_event() -> dict:
    return {
        "event_id": "event:f08",
        "event_type": "observation",
        "field_ref": "field:f08",
        "occurred_at": "2026-09-16T00:00:00Z",
        "observed_at": "2026-09-16T00:00:01Z",
        "received_at": "2026-09-16T00:00:02Z",
        "source_chain": ("Observation Gateway",),
        "evidence_refs": ("evidence:f08",),
        "provenance_refs": ("provenance:f08",),
        "payload": {"opaque": True},
        "trace_ref": "trace:f08",
    }


def _valid_task() -> dict:
    return {
        "task_request_id": "task:f08",
        "task_type": "atomic",
        "task_goal": "verify contract",
        "requester_ref": "requester:f08",
        "priority": "normal",
        "context_snapshot": {},
        "dependency_refs": (),
        "resource_constraints": {},
        "permission_snapshot": {"governance_ref": "governance:f08"},
        "capability_requirements": (),
        "deadline_or_timeout": "",
        "interruption_policy": {},
        "recovery_policy": {},
        "version_snapshots": {},
        "trace_ref": "trace:f08",
    }


def test_gateway_rejects_string_and_bytes_ref_collections_before_formation():
    request, _ = build_replay_inputs_v1(get_contrast_specs_v1()[0])
    for malformed in ("evidence:scalar", b"evidence:bytes"):
        result = ObservationGatewayEngineV1().run_case(replace(request, evidence_refs=malformed))
        assert result.admission_state == "REJECTED"
        assert result.ingress is None
        assert any(error.code == "INVALID_INPUT_SHAPE" for error in result.errors)


def test_valid_gateway_request_remains_on_canonical_path():
    request, _ = build_replay_inputs_v1(get_contrast_specs_v1()[0])
    result = ObservationGatewayEngineV1().run_case(request)
    assert result.ingress is not None
    assert result.errors == ()


def test_p10g_t01_gateway_replay_validator_matches_canonical_contract():
    request, _ = build_replay_inputs_v1(get_contrast_specs_v1()[0])
    assert request.replay_input is not None
    canonical_fields = {item.name for item in dataclass_fields(ControlledReplayInputV1)}
    assert "inherited_information_refs" not in canonical_fields
    assert validate_ingress_request_shape(request) == ()
    assert ObservationGatewayEngineV1().run_case(request).admission_state == "ADMITTED_OBSERVATION"
    validator_source = Path(
        "capabilities/midplatform/core/observation_gateway/observation_gateway_static_validators_v1.py"
    ).read_text()
    replay_validation_source = validator_source.split("replay = request.replay_input", 1)[1]
    assert '"inherited_information_refs"' not in replay_validation_source


def test_evidence_bridge_rejects_mixed_provenance_members():
    evidence = {
        "evidence_id": "evidence:f08",
        "source_provider": "provider:f08",
        "source_capability": "capability:f08",
        "raw_output_ref": "raw:f08",
        "source_temporal_ref": "time:f08",
        "trace_ref": "trace:f08",
        "provenance_refs": ["provenance:ok", 7],
        "candidate_only": True,
        "fact_declared": False,
    }
    result = form_field_event_candidate_from_evidence(
        evidence,
        field_ref="field:f08",
        context_ref="context:f08",
        occurred_at="2026-09-16T00:00:00Z",
        observed_at="2026-09-16T00:00:01Z",
        received_at="2026-09-16T00:00:02Z",
    )
    assert result.event_candidate is None
    assert "invalid_member_type:provenance_refs" in result.validation_errors


@pytest.mark.parametrize("mutation", [
    {"event_id": 7},
    {"evidence_refs": ["evidence:ok", 7]},
    {"source_chain": ["source:ok", object()]},
])
def test_field_event_admission_rejects_malformed_structure(mutation):
    event = _valid_event()
    event.update(mutation)
    result = admit_field_event(event, AdmissionPolicyV1("2026-09-16T00:01:00Z"))
    assert result.admission_status == "rejected_event"
    assert result.reducer_eligible is False


def test_valid_field_event_admission_remains_admissible():
    result = admit_field_event(
        _valid_event(), AdmissionPolicyV1("2026-09-16T00:01:00Z")
    )
    assert result.admission_status == "admitted_event"
    assert result.reducer_eligible is True


def test_reducer_rejects_bad_event_member_and_snapshot_shape():
    base = dict(
        reducer_request_id="request:f08",
        reducer_run_id="run:f08",
        field_id="field:f08",
        requested_state_type="field_state",
        admitted_events=(7,),
        existing_state_snapshot={},
        temporal_snapshot={},
        policy_registry_snapshot={"v": "1"},
        evaluation_contract_snapshot={"v": "1"},
        selection_contract_snapshot={"v": "1"},
        reduction_contract_snapshot={"v": "1"},
        conflict_snapshot={},
        overlay_snapshot={},
        owner_correction_snapshot={},
        provenance_snapshot={},
        version_snapshots={
            key: "1" for key in (
                "policy_registry_version", "eligibility_matrix_version",
                "precedence_matrix_version", "composition_contract_version",
                "replay_contract_version", "evaluation_contract_version",
                "reduction_contract_version",
            )
        },
    )
    adapted, _, reasons = adapt_module_input_v1(FieldStateReducerModuleRequestV1(**base))
    assert adapted is None
    assert "admitted_events_members_must_be_mapping" in reasons

    base["admitted_events"] = ({"event_id": "event:f08"},)
    base["existing_state_snapshot"] = 7
    adapted, _, reasons = adapt_module_input_v1(FieldStateReducerModuleRequestV1(**base))
    assert adapted is None
    assert "existing_state_snapshot_must_be_mapping" in reasons


def test_read_model_rejects_scalarification_of_query_fields():
    query = {
        "query_id": 7,
        "requester_ref": "requester:f08",
        "query_scope": "FIELD_STATE",
        "field_state_ref": "state:f08",
        "snapshot_ref": None,
        "task_ref": None,
        "scene_ref": None,
        "object_ref": None,
        "temporal_scope": None,
        "required_fields": ["state", 9],
        "trace_ref": "trace:f08",
        "replay_key": "replay:f08",
        "metadata": {},
    }
    valid, reasons, normalized = validate_query_v1(query)
    assert valid is False
    assert "missing_query_id" in reasons
    assert "required_fields_member_type_invalid" in reasons
    assert normalized == {}


def test_read_model_rejects_malformed_projection_members():
    valid, reasons, normalized = validate_state_candidate_v1(
        query={"field_state_ref": "state:f08", "trace_ref": "trace:f08", "replay_key": "replay:f08"},
        state_candidate={
            "source_state_ref": "state:f08",
            "state_version": "v1",
            "state_payload": {},
            "available_fields": ["field:f08", 7],
            "provenance_refs": ["provenance:f08"],
            "temporal_status": "unknown",
            "trace_ref": "trace:f08",
            "replay_key": "replay:f08",
        },
    )
    assert valid is False
    assert "invalid_available_fields_member_type" in reasons


def test_p10g_t02_read_model_temporal_status_wrong_scalar_rejected():
    valid, reasons, _ = validate_state_candidate_v1(
        query={"field_state_ref": "state:f08", "trace_ref": "trace:f08", "replay_key": "replay:f08"},
        state_candidate={
            "source_state_ref": "state:f08", "state_version": "v1", "state_payload": {},
            "available_fields": (), "provenance_refs": (), "temporal_status": 7,
            "trace_ref": "trace:f08", "replay_key": "replay:f08",
        },
    )
    assert valid is False
    assert "invalid_temporal_status_type" in reasons


def test_p10g_t03_read_model_source_state_ref_wrong_scalar_rejected():
    valid, reasons, _ = validate_state_candidate_v1(
        query={"field_state_ref": "state:f08", "trace_ref": "trace:f08", "replay_key": "replay:f08"},
        state_candidate={
            "source_state_ref": 7, "state_version": "v1", "state_payload": {},
            "available_fields": (), "provenance_refs": (), "temporal_status": "unknown",
            "trace_ref": "trace:f08", "replay_key": "replay:f08",
        },
    )
    assert valid is False
    assert "invalid_source_state_ref_type" in reasons


def test_p10g_t04_read_model_state_version_wrong_scalar_rejected():
    valid, reasons, _ = validate_state_candidate_v1(
        query={"field_state_ref": "state:f08", "trace_ref": "trace:f08", "replay_key": "replay:f08"},
        state_candidate={
            "source_state_ref": "state:f08", "state_version": 7, "state_payload": {},
            "available_fields": (), "provenance_refs": (), "temporal_status": "unknown",
            "trace_ref": "trace:f08", "replay_key": "replay:f08",
        },
    )
    assert valid is False
    assert "invalid_state_version_type" in reasons


def test_p10g_t05_read_model_valid_projection_preserved():
    valid, reasons, normalized = validate_state_candidate_v1(
        query={"field_state_ref": "state:f08", "trace_ref": "trace:f08", "replay_key": "replay:f08"},
        state_candidate={
            "source_state_ref": "state:f08", "state_version": "v1", "state_payload": {"state": "ready"},
            "available_fields": ("state",), "provenance_refs": ("provenance:f08",),
            "temporal_status": "active", "trace_ref": "trace:f08", "replay_key": "replay:f08",
        },
    )
    assert valid is True
    assert reasons == ()
    assert normalized["source_state_ref"] == "state:f08"
    assert normalized["state_version"] == "v1"


def test_context_validator_rejects_wrong_scalar_projection_shape():
    projection = ProjectionReferenceV1(
        source_owner="Field State System",
        projection_id="projection:f08",
        projection_version="v1",
        timestamp=7,
        validity="valid",
        confidence=None,
        unknown_state="unknown",
        provenance=("provenance:f08",),
        projection_kind="field",
        trace_reference="trace:f08",
    )
    result = validate_projection_reference_complete(projection)
    assert result.valid is False
    assert "timestamp_invalid_type" in result.issues


def test_cognitive_rejects_string_expansion_before_unknown_reasoning():
    request = build_request_v1(get_contrast_specs_v1()[0])
    malformed = replace(request, evidence_refs="evidence:scalar")
    with pytest.raises(ValueError, match="cognitive_state_input_invalid"):
        CognitiveStateFormationEngineV1().run_case(malformed)


def test_valid_cognitive_input_and_semantic_unknown_remain_structurally_valid():
    request = build_request_v1(get_contrast_specs_v1()[0])
    from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_static_validators_v1 import validate_input_contract
    assert validate_input_contract(request) == ()
    assert validate_input_contract(replace(request, semantic_reference_values=())) == ()
    assert validate_input_contract(replace(request, requirement_establishment_status="NOT_ESTABLISHED")) == ()


def test_task_wrong_context_mapping_is_rejected_not_defaulted_as_absence():
    raw = _valid_task()
    raw["context_snapshot"] = 7
    result = adapt_task_manager_input_v1(raw)
    assert result["adapted_input_ok"] is False
    assert "context_snapshot_invalid_field_type" in result["rejection_reasons"]


def test_explicit_optional_context_absence_remains_valid():
    raw = _valid_task()
    raw["context_snapshot"] = None
    result = adapt_task_manager_input_v1(raw)
    assert result["adapted_input_ok"] is True


def test_p10g_t06_task_dependency_string_rejected():
    raw = _valid_task()
    raw["dependency_refs"] = "dependency:1"
    result = adapt_task_manager_input_v1(raw)
    assert result["adapted_input_ok"] is False
    assert "dependency_refs_invalid_field_type" in result["rejection_reasons"]


def test_p10g_t07_task_dependency_bytes_rejected():
    raw = _valid_task()
    raw["dependency_refs"] = b"dependency:1"
    result = adapt_task_manager_input_v1(raw)
    assert result["adapted_input_ok"] is False
    assert "dependency_refs_invalid_field_type" in result["rejection_reasons"]


def test_p10g_t08_task_dependency_mixed_tuple_rejected():
    raw = _valid_task()
    raw["dependency_refs"] = ("dependency:1", 7)
    result = adapt_task_manager_input_v1(raw)
    assert result["adapted_input_ok"] is False
    assert "dependency_refs_invalid_member_type" in result["rejection_reasons"]


def test_p10g_t09_task_valid_dependency_tuple_preserved():
    raw = _valid_task()
    raw["dependency_refs"] = ("dependency:1", "dependency:2")
    result = adapt_task_manager_input_v1(raw)
    assert result["adapted_input_ok"] is True
    assert result["dependency_refs"] == ("dependency:1", "dependency:2")


@pytest.mark.parametrize("dependency_refs", [None, ()])
def test_p10g_t10_task_optional_dependency_absence_preserved(dependency_refs):
    raw = _valid_task()
    raw["dependency_refs"] = dependency_refs
    result = adapt_task_manager_input_v1(raw)
    assert result["adapted_input_ok"] is True
    assert result["dependency_refs"] == ()


def test_runtime_and_provider_preparation_reject_string_ref_expansion():
    runtime = RuntimeAllocationPreparationInputV1(
        preparation_ref="prep:f08",
        parent_cognitive_problem_ref="problem:f08",
        source_state_ref="state:f08",
        context_refs="ctx:1",
        trace_ref="trace:f08",
    )
    runtime_result = form_runtime_allocation_preparation_candidates(runtime)
    assert runtime_result.formation_status == "INVALID_INPUT"
    assert "context_refs_must_contain_strings" in runtime_result.validation_errors

    provider = ProviderBindingRuntimePreparationInputV1(
        preparation_ref="prep:f08",
        parent_cognitive_problem_ref="problem:f08",
        source_state_ref="state:f08",
        context_refs="ctx:1",
        trace_ref="trace:f08",
    )
    provider_result = form_provider_binding_runtime_preparation_candidates(provider)
    assert provider_result.formation_status == "INVALID_INPUT"
    assert "context_refs_must_contain_strings" in provider_result.validation_errors


def test_valid_empty_runtime_preparation_remains_a_valid_no_candidate_result():
    request = RuntimeAllocationPreparationInputV1(
        preparation_ref="prep:f08",
        parent_cognitive_problem_ref="problem:f08",
        source_state_ref="state:f08",
        trace_ref="trace:f08",
    )
    result = form_runtime_allocation_preparation_candidates(request)
    assert result.formation_status == "NO_RUNTIME_ALLOCATION_PREPARATION_CANDIDATE"
    assert result.validation_errors == ()


def test_aroute_rejects_malformed_transport_refs():
    _, route = build_replay_inputs_v1(get_contrast_specs_v1()[0])
    malformed = replace(route, ingress=replace(route.ingress, field_refs="field:scalar"))
    assert "ingress.field_refs_must_contain_strings" in validate_request_shape(malformed)


def test_decision_and_action_are_typed_internal_boundaries():
    decision = Path("capabilities/midplatform/core/decision_governance/decision_governance_engine_v1.py")
    action = Path("capabilities/midplatform/core/action_governance/action_governance_engine_v1.py")
    assert "DecisionGovernanceInputV1" in decision.read_text()
    assert "ActionGovernanceInputV1" in action.read_text()


def test_malformed_input_cannot_replace_f05_or_f07_authority_roots():
    gateway = Path("capabilities/midplatform/core/observation_gateway/observation_gateway_engine_v1.py").read_text()
    runtime = Path("capabilities/midplatform/core/runtime_executor/runtime_allocation_execution_instance_v1.py").read_text()
    assert "ObservationGatewayAdmissionRuntimeStateV1" in gateway
    assert "query_active_authorization_for_grant" in runtime

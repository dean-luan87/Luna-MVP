from __future__ import annotations

from copy import deepcopy
import inspect
from dataclasses import asdict, replace

from capabilities.midplatform.core.cognitive_flow.integration.brain_cognitive_loop_closure_assimilation_controlled.brain_cognitive_loop_closure_assimilation_engine_v1 import (
    build_brain_closure_run_v1,
    run_brain_cognitive_case_v1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    EvidenceReferenceBindingV1,
    ObservationGatewayAdmissionRuntimeStateV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.brain_cognitive_loop_closure_assimilation_controlled import (
    brain_cognitive_loop_closure_assimilation_engine_v1 as brain_engine,
)
from capabilities.midplatform.core.cognitive_flow.integration.cognitive_result_to_decision_governance_controlled_handoff import (
    engine_v1 as handoff_engine,
)
from capabilities.midplatform.core.cognitive_flow.integration.cognitive_result_to_decision_governance_controlled_handoff.engine_v1 import (
    _decision_result,
    build_cognitive_decision_handoff_candidate_v1,
    build_decision_handoff_run_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.cognitive_result_to_decision_governance_controlled_handoff.cognitive_result_to_decision_governance_handoff_types_v1 import (
    CognitiveDecisionHandoffCandidateV1,
)


def _typed_case_and_proof() -> tuple[dict, object]:
    typed_case = run_brain_cognitive_case_v1('CASE_A_SUFFICIENT_STOP', 'f05-test')
    case = asdict(typed_case)
    case['gateway_results'] = typed_case.gateway_results
    case['gateway_execution_identity_ref'] = typed_case.cognitive_proofs[-1].gateway_execution_identity_ref
    case['gateway_admission_queries'] = typed_case.gateway_admission_queries
    return case, typed_case.cognitive_proofs[-1]


def _source_case_and_proof() -> tuple[dict, dict]:
    case, proof = _typed_case_and_proof()
    proof_data = asdict(proof)
    proof_data['canonical_gateway_admission_result'] = proof.canonical_gateway_admission_result
    proof_data['evidence_binding'] = proof.evidence_binding
    return case, proof_data


def _candidate(proof: dict) -> tuple[object, tuple[str, ...]]:
    case, _ = _source_case_and_proof()
    return build_cognitive_decision_handoff_candidate_v1(case, proof)


def _proof_without_binding() -> dict:
    _, proof = _source_case_and_proof()
    mutated = deepcopy(proof)
    mutated.pop('evidence_binding', None)
    return mutated


def test_t1_canonical_gateway_evidence_is_allowed() -> None:
    summary = build_decision_handoff_run_v1('f05-t1')
    case = next(item for item in summary['cases'] if item['case_id'] == 'CASE_A_SUFFICIENT_STOP')
    gateway_refs = tuple(case['traceability']['evidence_refs'])
    assert tuple(case['decision_handoff']['evidence_refs']) == gateway_refs
    assert case['decision_governance_consumed'] is True


def test_t2_provenance_only_binding_is_rejected() -> None:
    proof = _proof_without_binding()
    proof['evidence_binding'] = {
        'evidence_refs': ['provenance:only'],
        'owner_ref': 'Observation Gateway Governance',
        'binding_kind': 'PROVENANCE',
        'candidate_only': True,
    }
    handoff, errors = _candidate(proof)
    assert handoff is None
    assert errors


def test_t3_current_world_only_binding_is_rejected() -> None:
    proof = _proof_without_binding()
    proof['evidence_binding'] = {
        'evidence_refs': ['current-world:only'],
        'owner_ref': 'Observation Gateway Governance',
        'binding_kind': 'CURRENT_WORLD',
        'candidate_only': True,
    }
    assert _candidate(proof)[0] is None


def test_t4_hypothesis_only_binding_is_rejected() -> None:
    proof = _proof_without_binding()
    proof['evidence_binding'] = {
        'evidence_refs': ['hypothesis:only'],
        'owner_ref': 'Observation Gateway Governance',
        'binding_kind': 'HYPOTHESIS',
        'candidate_only': True,
    }
    assert _candidate(proof)[0] is None


def test_t5_mixed_ingress_cannot_become_evidence() -> None:
    case, proof = _typed_case_and_proof()
    proof = replace(proof, ingress_refs=('gateway-admission:x', 'current-world:x', 'provenance:x'))
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case, proof)
    assert errors == ()
    assert handoff is not None
    assert tuple(handoff.evidence_refs) == proof.evidence_binding.evidence_refs
    assert 'current-world:x' not in handoff.evidence_refs
    assert 'provenance:x' not in handoff.evidence_refs


def test_t6_forged_evidence_like_ingress_is_rejected_without_binding() -> None:
    proof = _proof_without_binding()
    proof['ingress_refs'] = ('evidence:forged',)
    handoff, errors = _candidate(proof)
    assert handoff is None
    assert errors


def test_t7_valid_identity_with_wrong_semantic_binding_is_rejected() -> None:
    proof = _proof_without_binding()
    proof['evidence_binding'] = {
        'evidence_refs': ['evidence:identity'],
        'owner_ref': 'Observation Gateway Governance',
        'binding_kind': 'CURRENT_WORLD',
        'candidate_only': True,
    }
    assert _candidate(proof)[0] is None


def test_t8_empty_evidence_binding_is_rejected() -> None:
    proof = _proof_without_binding()
    proof['evidence_binding'] = {
        'evidence_refs': [],
        'owner_ref': 'Observation Gateway Governance',
        'binding_kind': 'ADMITTED_EVIDENCE',
        'candidate_only': True,
    }
    assert _candidate(proof)[0] is None


def test_t9_duplicate_evidence_refs_are_rejected_deterministically() -> None:
    proof = _proof_without_binding()
    proof['evidence_binding'] = {
        'evidence_refs': ['evidence:duplicate', 'evidence:duplicate'],
        'owner_ref': 'Observation Gateway Governance',
        'binding_kind': 'ADMITTED_EVIDENCE',
        'candidate_only': True,
    }
    handoff, errors = _candidate(proof)
    assert handoff is None
    assert errors


def test_t10_unknown_namespace_without_canonical_binding_is_rejected() -> None:
    proof = _proof_without_binding()
    proof['ingress_refs'] = ('opaque:unknown',)
    assert _candidate(proof)[0] is None


def test_t11_valid_sufficiency_and_stop_do_not_override_invalid_evidence() -> None:
    proof = _proof_without_binding()
    proof['evidence_binding'] = {
        'evidence_refs': ['provenance:invalid'],
        'owner_ref': 'Other Governance',
        'binding_kind': 'ADMITTED_EVIDENCE',
        'candidate_only': True,
    }
    assert _candidate(proof)[0] is None


def test_t12_complete_cognitive_proof_reaches_candidate_only_decision() -> None:
    summary = build_decision_handoff_run_v1('f05-t12')
    case = next(item for item in summary['cases'] if item['case_id'] == 'CASE_A_SUFFICIENT_STOP')
    assert case['decision_governance_consumed'] is True
    assert case['decision']['output']['decision_output'] is False
    assert case['decision']['output']['candidate_only'] is True


def test_t13_provenance_is_preserved_separately_from_evidence() -> None:
    summary = build_decision_handoff_run_v1('f05-t13')
    case = next(item for item in summary['cases'] if item['case_id'] == 'CASE_A_SUFFICIENT_STOP')
    handoff = case['decision_handoff']
    assert handoff['evidence_refs']
    assert handoff['provenance_refs']
    assert set(handoff['evidence_refs']) != set(handoff['provenance_refs'])
    assert handoff['evidence_owner_ref'] == 'Observation Gateway Governance'


def test_t14_adapter_does_not_assign_evidence_to_generic_ingress() -> None:
    case, proof = _typed_case_and_proof()
    proof = replace(proof, ingress_refs=('gateway-admission:generic', 'relation:generic'))
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case, proof)
    assert errors == ()
    assert handoff is not None
    assert handoff.evidence_refs != proof.ingress_refs


def test_t15_decision_boundary_rejects_unbound_handoff() -> None:
    case, proof = _typed_case_and_proof()
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case, proof)
    assert errors == ()
    assert handoff is not None
    invalid = handoff.__class__(
        **{
            **handoff.__dict__,
            'evidence_owner_ref': '',
            'evidence_binding_kind': '',
        }
    )
    result = _decision_result(invalid)
    assert result['decision_governance_consumed'] is False
    assert result['all_checks_passed'] is False


def test_t16_typed_gateway_binding_survives_handoff() -> None:
    case, proof = _typed_case_and_proof()
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case, proof)
    assert errors == ()
    assert handoff is not None
    binding = proof.evidence_binding
    assert handoff.evidence_binding_kind == binding.binding_kind
    assert handoff.evidence_owner_ref == binding.owner_ref
    assert handoff.evidence_refs == binding.evidence_refs


def _forged_binding(proof: dict, refs: tuple[str, ...], **overrides: object) -> dict:
    binding = {
        'gateway_admission_ref': proof['gateway_admission_ref'],
        'evidence_refs': list(refs),
        'owner_ref': 'Observation Gateway Governance',
        'binding_kind': 'ADMITTED_EVIDENCE',
        'candidate_only': True,
    }
    binding.update(overrides)
    return binding


def test_t17_correct_metadata_does_not_admit_provenance_ref() -> None:
    case, proof = _typed_case_and_proof()
    forged = EvidenceReferenceBindingV1(
        gateway_admission_ref=proof.gateway_admission_ref,
        evidence_refs=('provenance:forged',),
    )
    assert build_cognitive_decision_handoff_candidate_v1(
        case, replace(proof, evidence_binding=forged)
    )[0] is None


def test_t18_correct_metadata_does_not_admit_current_world_ref() -> None:
    proof = _proof_without_binding()
    proof['evidence_binding'] = _forged_binding(proof, ('current-world:forged',))
    assert _candidate(proof)[0] is None


def test_t19_correct_metadata_does_not_admit_hypothesis_ref() -> None:
    proof = _proof_without_binding()
    proof['evidence_binding'] = _forged_binding(proof, ('hypothesis:forged',))
    assert _candidate(proof)[0] is None


def test_t20_correct_metadata_does_not_admit_unknown_ref() -> None:
    proof = _proof_without_binding()
    proof['evidence_binding'] = _forged_binding(proof, ('opaque:unknown',))
    assert _candidate(proof)[0] is None


def test_t21_correct_metadata_does_not_admit_forged_evidence_like_ref() -> None:
    proof = _proof_without_binding()
    proof['evidence_binding'] = _forged_binding(proof, ('evidence:forged',))
    assert _candidate(proof)[0] is None


def test_t22_gateway_a_rejects_binding_for_gateway_b() -> None:
    proof = _proof_without_binding()
    proof['evidence_binding'] = _forged_binding(
        proof,
        tuple(proof['admitted_evidence_refs']),
        gateway_admission_ref='gateway-admission:other:v1',
    )
    assert _candidate(proof)[0] is None


def test_t23_gateway_admission_set_substitution_is_rejected() -> None:
    proof = _proof_without_binding()
    proof['evidence_binding'] = _forged_binding(proof, ('evidence:substituted',))
    assert _candidate(proof)[0] is None


def test_t24_genuine_gateway_binding_is_transported_unchanged() -> None:
    case = run_brain_cognitive_case_v1('CASE_A_SUFFICIENT_STOP', 'f05-t24')
    gateway = case.gateway_results[0].replay_admission
    proof = case.cognitive_proofs[-1]
    assert gateway is not None
    assert proof.evidence_binding is gateway.evidence_binding
    assert proof.evidence_binding.gateway_admission_ref == gateway.gateway_admission_ref
    assert proof.evidence_binding.evidence_refs == gateway.evidence_refs


def test_t25_a_route_consumes_gateway_binding_identity() -> None:
    case = run_brain_cognitive_case_v1('CASE_A_SUFFICIENT_STOP', 'f05-t25')
    gateway = case.gateway_results[0].replay_admission
    route = case.route_results[0]
    assert gateway is not None
    assert route.cognitive_execution is not None
    assert route.cognitive_execution.evidence_binding is gateway.evidence_binding


def test_t26_brain_closure_preserves_evidence_refs_without_reconstruction() -> None:
    case = run_brain_cognitive_case_v1('CASE_A_SUFFICIENT_STOP', 'f05-t26')
    proof = case.cognitive_proofs[-1]
    assert case.closure_record is not None
    assert case.closure_record.evidence_refs == proof.evidence_binding.evidence_refs


def test_t27_handoff_rejects_arbitrary_mapping_with_expected_metadata() -> None:
    proof = _proof_without_binding()
    proof['evidence_binding'] = _forged_binding(proof, ('provenance:arbitrary',))
    assert _candidate(proof)[0] is None


def test_t28_decision_remains_candidate_only_after_valid_binding() -> None:
    summary = build_decision_handoff_run_v1('f05-t28')
    case = next(item for item in summary['cases'] if item['case_id'] == 'CASE_A_SUFFICIENT_STOP')
    assert case['decision']['output']['candidate_only'] is True
    assert case['decision']['output']['decision_output'] is False


def test_t29_canonical_gateway_admission_result_is_required_and_preserved() -> None:
    case, proof = _typed_case_and_proof()
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case, proof)
    canonical = case['gateway_results'][0].replay_admission
    assert errors == ()
    assert handoff is not None
    assert handoff.canonical_gateway_admission_result is canonical


def test_t30_value_equivalent_admission_clone_is_not_authoritative() -> None:
    case, proof = _typed_case_and_proof()
    canonical = case['gateway_results'][0].replay_admission
    clone = replace(canonical)
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(
        case, replace(proof, canonical_gateway_admission_result=clone)
    )
    assert handoff is None
    assert errors == ('decision_handoff_rejects_noncanonical_gateway_admission_result',)


def test_t31_self_consistent_fake_admission_and_binding_are_rejected() -> None:
    case, proof = _typed_case_and_proof()
    canonical = case['gateway_results'][0].replay_admission
    fake_admission = replace(
        canonical,
        gateway_admission_ref='gateway-admission:fake',
        evidence_refs=('provenance:fake',),
    )
    fake_binding = EvidenceReferenceBindingV1(
        gateway_admission_ref='gateway-admission:fake',
        evidence_refs=('provenance:fake',),
    )
    forged = replace(
        proof,
        canonical_gateway_admission_result=fake_admission,
        gateway_admission_ref='gateway-admission:fake',
        admitted_evidence_refs=('provenance:fake',),
        evidence_binding=fake_binding,
    )
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case, forged)
    assert handoff is None
    assert errors


def test_t32_copied_gateway_fields_without_parent_result_are_rejected() -> None:
    case, proof = _typed_case_and_proof()
    copied = replace(proof, canonical_gateway_admission_result=None)
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case, copied)
    assert handoff is None
    assert errors == ('decision_handoff_requires_canonical_gateway_admission_result',)


def test_t33_canonical_result_rejects_substituted_derived_evidence_refs() -> None:
    case, proof = _typed_case_and_proof()
    substituted = ('evidence:substituted',)
    binding = EvidenceReferenceBindingV1(
        gateway_admission_ref=proof.gateway_admission_ref,
        evidence_refs=substituted,
    )
    forged = replace(proof, evidence_binding=binding, admitted_evidence_refs=substituted)
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case, forged)
    assert handoff is None
    assert errors == ('decision_handoff_evidence_binding_set_mismatch',)


def test_t34_canonical_result_rejects_substituted_admission_ref() -> None:
    case, proof = _typed_case_and_proof()
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(
        case, replace(proof, gateway_admission_ref='gateway-admission:substituted')
    )
    assert handoff is None
    assert errors == ('decision_handoff_evidence_binding_admission_mismatch',)


def test_t35_a_route_proof_retains_the_gateway_admission_object() -> None:
    typed_case = run_brain_cognitive_case_v1('CASE_A_SUFFICIENT_STOP', 'f05-t35')
    gateway = typed_case.gateway_results[0].replay_admission
    proof = typed_case.cognitive_proofs[-1]
    assert gateway is not None
    assert proof.canonical_gateway_admission_result is gateway


def test_t36_brain_closure_uses_the_preserved_gateway_admission_result() -> None:
    typed_case = run_brain_cognitive_case_v1('CASE_A_SUFFICIENT_STOP', 'f05-t36')
    gateway = typed_case.gateway_results[0].replay_admission
    proof = typed_case.cognitive_proofs[-1]
    assert gateway is not None
    assert typed_case.closure_record is not None
    assert proof.canonical_gateway_admission_result is gateway
    assert typed_case.closure_record.evidence_refs == gateway.evidence_refs


def test_t37_handoff_does_not_infer_authority_from_matching_projections() -> None:
    case, proof = _typed_case_and_proof()
    copied = replace(proof, canonical_gateway_admission_result=None)
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case, copied)
    assert handoff is None
    assert errors == ('decision_handoff_requires_canonical_gateway_admission_result',)


def test_t38_controlled_replay_forms_a_new_gateway_admission_result() -> None:
    case_a = run_brain_cognitive_case_v1('CASE_A_SUFFICIENT_STOP', 'f05-t38-a')
    case_b = run_brain_cognitive_case_v1('CASE_A_SUFFICIENT_STOP', 'f05-t38-b')
    admission_a = case_a.gateway_results[0].replay_admission
    admission_b = case_b.gateway_results[0].replay_admission
    assert admission_a is not None
    assert admission_b is not None
    assert admission_a is not admission_b
    assert admission_a.gateway_admission_ref != admission_b.gateway_admission_ref


def test_t39_execution_mode_carrier_alone_cannot_create_evidence_authority() -> None:
    case, proof = _typed_case_and_proof()
    carrier_only_case = dict(case)
    carrier_only_case['gateway_results'] = ()
    carrier_only_case['gateway_admission_queries'] = ()
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(
        carrier_only_case, proof
    )
    assert handoff is None
    assert errors


def test_t40_decision_remains_candidate_only_and_gateway_decoupled() -> None:
    summary = build_decision_handoff_run_v1('f05-t40')
    case = next(item for item in summary['cases'] if item['case_id'] == 'CASE_A_SUFFICIENT_STOP')
    assert case['decision']['output']['candidate_only'] is True
    assert case['decision']['output']['decision_output'] is False
    assert 'gateway_admission_ref' not in case['decision']['request']


def test_t41_genuine_gateway_governed_admission_is_accepted() -> None:
    case, proof = _typed_case_and_proof()
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case, proof)
    assert errors == ()
    assert handoff is not None
    record = case['gateway_admission_queries'][-1].lookup(
        case['gateway_execution_identity_ref'], proof.gateway_admission_ref
    )
    assert record is not None
    assert record.evidence_refs == proof.admitted_evidence_refs


def test_t42_caller_created_gateway_dto_without_state_is_rejected() -> None:
    case, proof = _typed_case_and_proof()
    forged = replace(
        proof,
        canonical_gateway_admission_result=replace(
            proof.canonical_gateway_admission_result,
            gateway_admission_ref='gateway-admission:caller',
            evidence_refs=('provenance:caller',),
        ),
    )
    case['gateway_admission_queries'] = ()
    assert build_cognitive_decision_handoff_candidate_v1(case, forged)[0] is None


def test_t43_caller_created_dto_binding_and_proof_are_rejected() -> None:
    case, proof = _typed_case_and_proof()
    fake_admission = replace(
        proof.canonical_gateway_admission_result,
        gateway_admission_ref='gateway-admission:caller',
        evidence_refs=('provenance:caller',),
    )
    fake_binding = EvidenceReferenceBindingV1(
        gateway_admission_ref='gateway-admission:caller',
        evidence_refs=('provenance:caller',),
    )
    forged = replace(
        proof,
        canonical_gateway_admission_result=fake_admission,
        evidence_binding=fake_binding,
        gateway_admission_ref='gateway-admission:caller',
        admitted_evidence_refs=('provenance:caller',),
    )
    case['gateway_admission_queries'] = ()
    assert build_cognitive_decision_handoff_candidate_v1(case, forged)[0] is None


def test_t44_fake_runtime_state_dto_has_no_authority() -> None:
    case, proof = _typed_case_and_proof()
    forged = proof
    case['gateway_admission_queries'] = (object(),)
    assert build_cognitive_decision_handoff_candidate_v1(case, forged)[0] is None


def test_t45_value_copy_of_runtime_state_has_no_authority() -> None:
    case, proof = _typed_case_and_proof()
    case['gateway_admission_queries'] = (object(),)
    assert build_cognitive_decision_handoff_candidate_v1(case, proof)[0] is None


def test_t46_genuine_gateway_dto_without_canonical_state_is_rejected() -> None:
    case, proof = _typed_case_and_proof()
    case['gateway_admission_queries'] = ()
    assert build_cognitive_decision_handoff_candidate_v1(case, proof)[0] is None


def test_t47_genuine_state_with_substituted_evidence_set_is_rejected() -> None:
    case, proof = _typed_case_and_proof()
    substituted = replace(
        proof.canonical_gateway_admission_result,
        evidence_refs=('evidence:substituted',),
    )
    forged = replace(proof, canonical_gateway_admission_result=substituted)
    assert build_cognitive_decision_handoff_candidate_v1(case, forged)[0] is None


def test_t48_genuine_state_with_substituted_admission_ref_is_rejected() -> None:
    case, proof = _typed_case_and_proof()
    substituted = replace(
        proof.canonical_gateway_admission_result,
        gateway_admission_ref='gateway-admission:substituted',
    )
    forged = replace(
        proof,
        canonical_gateway_admission_result=substituted,
        gateway_admission_ref='gateway-admission:substituted',
    )
    assert build_cognitive_decision_handoff_candidate_v1(case, forged)[0] is None


def test_t49_admission_from_execution_a_cannot_authorize_execution_b() -> None:
    case_a, proof_a = _typed_case_and_proof()
    case_b_typed = run_brain_cognitive_case_v1('CASE_A_SUFFICIENT_STOP', 'f05-t49-b')
    case_b = asdict(case_b_typed)
    case_b['gateway_results'] = case_b_typed.gateway_results
    case_b['gateway_execution_identity_ref'] = case_b_typed.cognitive_proofs[-1].gateway_execution_identity_ref
    case_b['gateway_admission_queries'] = case_b_typed.gateway_admission_queries
    assert build_cognitive_decision_handoff_candidate_v1(case_b, proof_a)[0] is None


def test_t50_aroute_cannot_register_gateway_admission_state() -> None:
    state = ObservationGatewayAdmissionRuntimeStateV1()
    assert not hasattr(state, 'record_admission')
    assert '_record_admission' not in inspect.getsource(ARouteOrchestrationEngineV1)


def test_t51_brain_cannot_register_gateway_admission_state() -> None:
    assert '_record_admission' not in inspect.getsource(brain_engine)


def test_t52_handoff_cannot_register_or_repair_gateway_state() -> None:
    source = inspect.getsource(handoff_engine)
    assert '_record_admission' not in source
    assert 'ObservationGatewayEngineV1(' not in source


def test_t53_decision_remains_gateway_state_decoupled() -> None:
    summary = build_decision_handoff_run_v1('f05-t53')
    case = next(item for item in summary['cases'] if item['case_id'] == 'CASE_A_SUFFICIENT_STOP')
    assert case['decision']['output']['candidate_only'] is True
    assert 'gateway_admission_runtime_state' not in case['decision']['request']


def test_t54_serialized_old_admission_record_cannot_restore_authority() -> None:
    case, proof = _typed_case_and_proof()
    case['gateway_admission_queries'] = ()
    assert build_cognitive_decision_handoff_candidate_v1(case, proof)[0] is None


def test_t55_controlled_replay_creates_a_new_gateway_state_transition() -> None:
    case_a = run_brain_cognitive_case_v1('CASE_A_SUFFICIENT_STOP', 'f05-t55-a')
    case_b = run_brain_cognitive_case_v1('CASE_A_SUFFICIENT_STOP', 'f05-t55-b')
    proof_a = case_a.cognitive_proofs[-1]
    proof_b = case_b.cognitive_proofs[-1]
    state_a = case_a.gateway_admission_queries[-1]
    state_b = case_b.gateway_admission_queries[-1]
    assert state_a is not state_b
    assert state_a.lookup(
        proof_a.gateway_execution_identity_ref, proof_a.gateway_admission_ref
    ) is not None
    assert state_b.lookup(
        proof_b.gateway_execution_identity_ref, proof_b.gateway_admission_ref
    ) is not None
    assert proof_a.gateway_admission_ref != proof_b.gateway_admission_ref


def test_t56_evaluation_cannot_fabricate_gateway_admission_state() -> None:
    from capabilities.evaluation.full_end_to_end_cognitive_logic_conformance_regression import runner_v1, verifier_v1
    assert '_record_admission(' not in inspect.getsource(runner_v1)
    assert '_record_admission(' not in inspect.getsource(verifier_v1)


def test_t57_binding_alone_cannot_establish_admission() -> None:
    case, proof = _typed_case_and_proof()
    case['gateway_admission_queries'] = ()
    assert build_cognitive_decision_handoff_candidate_v1(case, proof)[0] is None


def test_t58_self_consistent_dto_package_without_state_is_rejected() -> None:
    case, proof = _typed_case_and_proof()
    fake_admission = replace(
        proof.canonical_gateway_admission_result,
        gateway_admission_ref='gateway-admission:self-consistent',
        evidence_refs=('provenance:self-consistent',),
    )
    forged = replace(
        proof,
        canonical_gateway_admission_result=fake_admission,
        gateway_admission_ref='gateway-admission:self-consistent',
        admitted_evidence_refs=('provenance:self-consistent',),
    )
    case['gateway_admission_queries'] = ()
    assert build_cognitive_decision_handoff_candidate_v1(case, forged)[0] is None


def test_t59_canonical_state_rejects_mismatching_descriptive_projection() -> None:
    case, proof = _typed_case_and_proof()
    mismatched_binding = EvidenceReferenceBindingV1(
        gateway_admission_ref=proof.gateway_admission_ref,
        evidence_refs=('evidence:mismatch',),
    )
    forged = replace(proof, evidence_binding=mismatched_binding)
    assert build_cognitive_decision_handoff_candidate_v1(case, forged)[0] is None


def test_t60_canonical_state_and_matching_projections_are_accepted() -> None:
    case, proof = _typed_case_and_proof()
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case, proof)
    assert errors == ()
    assert handoff is not None
    assert handoff.evidence_refs == proof.admitted_evidence_refs

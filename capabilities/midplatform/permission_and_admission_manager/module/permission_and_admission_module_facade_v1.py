from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_admission_decision_builder_v1 import (
    build_permission_admission_decision_candidate_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_admission_eligibility_resolver_v1 import (
    resolve_permission_admission_eligibility_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_diagnostics_v1 import (
    build_permission_and_admission_diagnostics_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_input_adapter_v1 import (
    adapt_permission_and_admission_input_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_module_output_builder_v1 import (
    build_permission_and_admission_module_output_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_request_classifier_v1 import (
    build_permission_and_admission_request_classification_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_resource_resolver_v1 import (
    build_permission_and_admission_resource_candidate_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_subject_resolver_v1 import (
    build_permission_and_admission_subject_candidate_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_trace_replay_v1 import (
    build_permission_and_admission_trace_replay_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_authority_boundary_checker_v1 import (
    build_permission_authority_boundary_check_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_conflict_checker_v1 import (
    build_permission_conflict_check_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_consent_checker_v1 import (
    build_permission_consent_check_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_evidence_provenance_validator_v1 import (
    build_permission_evidence_provenance_validation_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_ownership_checker_v1 import (
    build_permission_ownership_check_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_policy_registry_adapter_v1 import (
    build_permission_policy_lookup_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_revocation_checker_v1 import (
    build_permission_revocation_check_v1,
)
from capabilities.midplatform.permission_and_admission_manager.module.permission_risk_checker_v1 import (
    build_permission_risk_check_v1,
)


def run_permission_and_admission_manager_module_v1(
    payload: Mapping[str, Any],
) -> Dict[str, Any]:
    input_candidate = adapt_permission_and_admission_input_v1(payload)
    subject_candidate = build_permission_and_admission_subject_candidate_v1(
        input_candidate
    )
    resource_candidate = build_permission_and_admission_resource_candidate_v1(
        input_candidate
    )
    request_classification = build_permission_and_admission_request_classification_v1(
        input_candidate
    )
    policy_lookup = build_permission_policy_lookup_v1(
        input_candidate, request_classification
    )
    evidence_validation = build_permission_evidence_provenance_validation_v1(
        input_candidate, policy_lookup
    )
    consent_check = build_permission_consent_check_v1(input_candidate, policy_lookup)
    ownership_check = build_permission_ownership_check_v1(
        input_candidate, policy_lookup
    )
    authority_check = build_permission_authority_boundary_check_v1(
        input_candidate, policy_lookup
    )
    risk_check = build_permission_risk_check_v1(input_candidate)
    conflict_check = build_permission_conflict_check_v1(input_candidate)
    revocation_check = build_permission_revocation_check_v1(input_candidate)

    eligibility = resolve_permission_admission_eligibility_v1(
        input_candidate,
        subject_candidate,
        resource_candidate,
        request_classification,
        policy_lookup,
        evidence_validation,
        consent_check,
        ownership_check,
        authority_check,
        risk_check,
        conflict_check,
        revocation_check,
    )
    decision_candidate = build_permission_admission_decision_candidate_v1(
        input_candidate, eligibility
    )
    diagnostics = build_permission_and_admission_diagnostics_v1(
        input_candidate,
        eligibility,
        evidence_validation,
        consent_check,
        ownership_check,
        authority_check,
        risk_check,
        conflict_check,
        revocation_check,
    )
    trace_replay = build_permission_and_admission_trace_replay_v1(
        input_candidate, eligibility
    )
    output = build_permission_and_admission_module_output_v1(
        input_candidate,
        eligibility,
        decision_candidate,
        diagnostics,
        trace_replay,
    )

    output.update(
        {
            "input_candidate": input_candidate,
            "subject_candidate": subject_candidate,
            "resource_candidate": resource_candidate,
            "request_classification": request_classification,
            "policy_lookup": policy_lookup,
            "evidence_validation": evidence_validation,
            "consent_check": consent_check,
            "ownership_check": ownership_check,
            "authority_check": authority_check,
            "risk_check": risk_check,
            "conflict_check": conflict_check,
            "revocation_check": revocation_check,
            "eligibility": eligibility,
            "trace_replay": trace_replay,
            "unhandled_exception": False,
        }
    )
    return output

"""Child-runner manifest for the consolidated canonical-flow regression."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


PHASE = "Phase-Luna-Canonical-Flow-Consolidated-Regression-v1-001"


@dataclass(frozen=True)
class ChildModuleSpecV1:
    module_id: str
    phase: str
    runner_module: str
    verifier_module: str
    expected_scenario_count: int
    required_checks: Tuple[str, ...]
    authority_domains: Tuple[str, ...]
    input_output_boundary: str
    runtime_allowance: str
    required_negative_guards: Tuple[str, ...]


CHILD_MODULES = (
    ChildModuleSpecV1(
        module_id="SOURCE_STATE_OUTCOME_RETURN",
        phase="Phase-Luna-Canonical-Flow-Source-State-And-Outcome-Return-Controlled-Implementation-v1-001",
        runner_module="capabilities.midplatform.core.cognitive_flow.integration.canonical_source_state_outcome_return_controlled.runner_v1",
        verifier_module="capabilities.midplatform.core.cognitive_flow.integration.canonical_source_state_outcome_return_controlled.verifier_v1",
        expected_scenario_count=30,
        required_checks=(
            "source_state_handoff_boundary_ok", "current_world_candidate_boundary_ok",
            "field_event_candidate_boundary_ok", "provider_result_evidence_separation_ok",
            "action_result_reality_separation_ok", "outcome_brain_boundary_ok",
            "brain_adjudication_not_executed", "version_lineage_ok", "invalidation_boundary_ok",
            "trace_provenance_ok", "authority_responsibility_ok", "no_source_mutation",
            "no_world_truth", "no_runtime_execution", "negative_guards_ok", "source_set_ok",
            "documentation_set_ok",
        ),
        authority_domains=("Field", "Current World", "Evidence", "Outcome Evaluation", "Brain Governance"),
        input_output_boundary="Provider/Action Result → Evidence/Source-State candidates and Brain input candidate",
        runtime_allowance="synthetic adapters only",
        required_negative_guards=("source_mutation_count=0", "brain_mutation_count=0", "runtime_execution_count=0"),
    ),
    ChildModuleSpecV1(
        module_id="CAPABILITY_MODEL_PROVIDER_BINDING",
        phase="Phase-Luna-Capability-Model-Provider-Binding-Controlled-Implementation-v1-001",
        runner_module="capabilities.midplatform.core.cognitive_flow.integration.capability_model_provider_binding_controlled.runner_v1",
        verifier_module="capabilities.midplatform.core.cognitive_flow.integration.capability_model_provider_binding_controlled.verifier_v1",
        expected_scenario_count=34,
        required_checks=(
            "capability_model_binding_boundary_ok", "model_provider_binding_boundary_ok",
            "capability_binding_owner_ok", "provider_binding_owner_ok", "model_source_owner_preserved",
            "shared_declaration_no_dual_mutation_ok", "binding_not_runtime_admission_ok",
            "binding_not_provider_admission_ok", "cross_binding_consistency_ok", "version_lineage_ok",
            "invalidation_ok", "trace_provenance_ok", "authority_responsibility_ok",
            "no_runtime_execution", "no_model_loading", "no_provider_invocation", "negative_guards_ok",
            "source_set_ok", "documentation_set_ok",
        ),
        authority_domains=("Capability Governance", "Model Governance", "Provider Governance"),
        input_output_boundary="Capability/Model and Model/Provider declarations → candidate bindings",
        runtime_allowance="declaration validation only",
        required_negative_guards=("runtime_execution_count=0", "model_loading_count=0", "provider_invocation_count=0", "source_mutation_count=0"),
    ),
    ChildModuleSpecV1(
        module_id="EXECUTION_HANDOFF_ADAPTERS",
        phase="Phase-Luna-Canonical-Flow-Execution-Handoff-Adapters-Controlled-Implementation-v1-001",
        runner_module="capabilities.midplatform.core.cognitive_flow.integration.canonical_execution_handoff_adapters_controlled.runner_v1",
        verifier_module="capabilities.midplatform.core.cognitive_flow.integration.canonical_execution_handoff_adapters_controlled.verifier_v1",
        expected_scenario_count=48,
        required_checks=(
            "a_attention_boundary_ok", "attention_need_authority_ok", "runtime_observation_boundary_ok",
            "executable_candidate_required", "runtime_block_not_observation_ready", "decision_action_boundary_ok",
            "task_action_boundary_ok", "single_action_admission_owner_ok", "action_result_task_boundary_ok",
            "action_result_a_boundary_ok", "task_completion_not_direct_result_ok", "a_sufficiency_not_direct_result_ok",
            "version_lineage_ok", "invalidation_ok", "trace_provenance_ok", "authority_responsibility_ok",
            "no_source_mutation", "no_world_truth", "no_runtime_execution", "no_observation_execution",
            "no_action_execution", "no_provider_invocation", "negative_guards_ok", "source_set_ok",
            "documentation_set_ok",
        ),
        authority_domains=("A", "Attention", "Observation", "Decision Governance", "Task", "Action Governance"),
        input_output_boundary="Cognitive Requirement/Executable Capability/Decision/Task/Action Result → governed handoff candidates",
        runtime_allowance="synthetic handoff adapters only",
        required_negative_guards=("source_mutation_count=0", "runtime_execution_count=0", "observation_execution_count=0", "action_execution_count=0", "provider_invocation_count=0"),
    ),
)


DOCUMENT_FILES = (
    "README.md", "regression_scope_v1.md", "child_module_manifest_v1.md",
    "cross_module_invariants_v1.md", "reference_version_continuity_v1.md",
    "authority_responsibility_regression_v1.md", "failure_return_regression_v1.md",
    "legacy_bypass_audit_v1.md", "whitebox_observability_surface_v1.md",
    "scenario_mapping_v1.json", "change_manifest.md",
)

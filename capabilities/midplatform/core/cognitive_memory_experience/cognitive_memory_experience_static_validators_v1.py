"""Static validators for controlled implementation v1."""

from __future__ import annotations

from dataclasses import asdict

from capabilities.midplatform.core.cognitive_memory_experience.cognitive_memory_experience_registry_v1 import (
    ADMISSION_STATES,
    MEMORY_TYPES,
    NEGATIVE_GUARDS,
    SENSITIVITY_LEVELS,
)
from capabilities.midplatform.core.cognitive_memory_experience.memory_io_types_v1 import (
    CognitiveMemoryExperienceOutputV1,
    NegativeGuardStatusV1,
)


def validate_output_contract(output: CognitiveMemoryExperienceOutputV1) -> bool:
    exp = output.experience_candidate
    mem = output.memory_candidate
    adm = output.admission_decision_candidate
    handoff = output.persistence_handoff_candidate
    return (
        output.synthetic_only is True
        and output.candidate_only is True
        and output.runtime_execution is False
        and output.source_owner_mutation is False
        and exp.candidate_only is True
        and exp.fact_admitted is False
        and exp.persisted is False
        and mem.candidate_only is True
        and mem.persisted is False
        and mem.fact_admitted is False
        and mem.automatic_consolidation is False
        and mem.memory_type in MEMORY_TYPES
        and mem.privacy_sensitivity_level in SENSITIVITY_LEVELS
        and adm.admission_state in ADMISSION_STATES
        and handoff.persistence_executed is False
        and handoff.database_write is False
        and handoff.vector_store_write is False
        and (
            output.retrieval_candidate is None
            or (
                output.retrieval_candidate.candidate_only is True
                and output.retrieval_candidate.context_mutation is False
                and output.retrieval_candidate.field_mutation is False
                and output.retrieval_candidate.current_world_truth_declaration is False
            )
        )
        and (
            output.learning_evidence_candidate is None
            or (
                output.learning_evidence_candidate.learning_execution is False
                and output.learning_evidence_candidate.parameter_mutation is False
                and output.learning_evidence_candidate.genome_activation is False
            )
        )
        and (
            output.self_personality_evidence_candidate is None
            or (
                output.self_personality_evidence_candidate.personality_mutation is False
                and output.self_personality_evidence_candidate.self_model_mutation
                is False
                and output.self_personality_evidence_candidate.identity_mutation
                is False
                and output.self_personality_evidence_candidate.automatic_trait_change
                is False
            )
        )
        and output.trace is not None
        and output.provenance is not None
        and output.negative_guard_status is not None
        and validate_negative_guards(output.negative_guard_status)
    )


def validate_negative_guards(guard: NegativeGuardStatusV1) -> bool:
    return asdict(guard) == NEGATIVE_GUARDS

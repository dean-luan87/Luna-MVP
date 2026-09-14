"""Static validators for controlled implementation v1."""

from __future__ import annotations

from dataclasses import asdict

from capabilities.midplatform.core.cognitive_learning.cognitive_learning_io_types_v1 import (
    CognitiveLearningOutputV1,
    NegativeGuardStatusV1,
)
from capabilities.midplatform.core.cognitive_learning.cognitive_learning_registry_v1 import (
    ADMISSION_STATES,
    GENERALIZATION_LEVELS,
    LEARNING_KINDS,
    NEGATIVE_GUARDS,
    SENSITIVITY_LEVELS,
)


def validate_output_contract(output: CognitiveLearningOutputV1) -> bool:
    evidence = output.learning_evidence_candidate
    learning = output.learning_candidate
    update = output.parameter_update_candidate
    decision = output.admission_decision_candidate
    generalization = output.generalization_assessment
    return (
        output.synthetic_only is True
        and output.candidate_only is True
        and output.runtime_training is False
        and output.source_owner_mutation is False
        and evidence.candidate_only is True
        and evidence.fact_admitted is False
        and learning.learning_kind in LEARNING_KINDS
        and learning.candidate_only is True
        and learning.truth_declared is False
        and learning.generalization_level_candidate in GENERALIZATION_LEVELS
        and update.activation_allowed is False
        and update.persistence_allowed is False
        and update.genome_activation_allowed is False
        and update.source_owner_mutation is False
        and decision.admission_state in ADMISSION_STATES
        and generalization.generalization_level_candidate in GENERALIZATION_LEVELS
        and (output.trace is not None)
        and (output.provenance is not None)
        and (output.negative_guard_status is not None)
        and validate_negative_guards(output.negative_guard_status)
    )


def validate_negative_guards(guard: NegativeGuardStatusV1) -> bool:
    return asdict(guard) == NEGATIVE_GUARDS


def validate_sensitivity_level(level: str) -> bool:
    return level in SENSITIVITY_LEVELS

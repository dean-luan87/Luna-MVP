"""Static registry for the controlled working-envelope bridge."""

PHASE = "Phase-Luna-A-Working-Envelope-And-Cognitive-Requirement-Bridge-Controlled-Implementation-v1-001"
ROLE_A = "A_REASONING_ROLE"
OBSERVATION_OWNER = "Observation Gateway Governance"
CAPABILITY_SCOPE_OWNER = "Capability Registry / Capability Governance"
CAPABILITY_RESOLUTION_OWNER = "Capability Registry / Capability Governance / Universal Slot Resolution Surface"

IMPACT_DISPOSITIONS = (
    "NO_MATERIAL_IMPACT",
    "REASSESS_CURRENT_NEED",
    "REASSESS_HYPOTHESIS",
    "REASSESS_SUFFICIENCY",
    "REPLAN",
    "PAUSE",
    "WAIT",
    "REQUEST_NEW_EVIDENCE",
)

SUPPORTED_REQUESTS = {
    "OBJECT_DETECTION": {
        "problem_class": "object_presence",
        "operation": "DETECT_OBJECT",
        "input_contract": "image_evidence",
        "output_contract": "object_candidate",
        "requirement_type": "OBJECT_DETECTION",
    },
    "TEXT_RECOGNITION": {
        "problem_class": "text_content",
        "operation": "READ_TEXT",
        "input_contract": "image_evidence",
        "output_contract": "text_candidate",
        "requirement_type": "TEXT_READ",
    },
    "SPATIAL_RELATION": {
        "problem_class": "spatial_structure",
        "operation": "PROVIDE_SPATIAL_STRUCTURE",
        "input_contract": "pose_candidate",
        "output_contract": "spatial_map_candidate",
        "requirement_type": "SPATIAL_MAP",
    },
}

NEGATIVE_GUARDS = {
    "candidate_only": True,
    "synthetic_only": True,
    "brain_runtime": False,
    "semantic_module_runtime": False,
    "experience_filter_runtime": False,
    "provider_invocation": False,
    "model_inference": False,
    "yolo": False,
    "ocr_runtime": False,
    "camera": False,
    "action_execution": False,
    "learning": False,
    "memory_mutation": False,
    "experience_mutation": False,
    "scheduler": False,
    "loop_manager": False,
    "loop_planner": False,
    "working_envelope_authoritative_duplication": False,
    "task_need_authority": False,
    "task_capability_selection": False,
    "observation_need_authority": False,
    "observation_sufficiency_authority": False,
    "capability_goal_authority": False,
    "capability_need_authority": False,
    "loop_requirement_creation": False,
    "loop_capability_selection": False,
    "loop_observation_request": False,
    "loop_evidence_judgment": False,
    "a_provider_selection": False,
    "brain_provider_selection": False,
    "experience_world_truth": False,
    "experience_direct_need_selection": False,
}


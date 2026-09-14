# -*- coding: utf-8 -*-
"""Document Surface — Option B Model/Skill Admission Contract mapping v1."""

from __future__ import annotations

from typing import Any, Dict, List

PRIMARY_CONTRACT = "LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1"

REFERENCED_PROTOCOLS: List[Dict[str, Any]] = [
    {"protocol_ref": PRIMARY_CONTRACT, "layer": "L1 Midplatform Protocols", "role": "model_skill_admission_authority"},
    {"protocol_ref": "Runtime Boundary Contract", "layer": "L1", "role": "runtime_activation_boundary"},
    {"protocol_ref": "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1", "layer": "L1", "role": "candidate_fact_admission"},
    {"protocol_ref": "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1", "layer": "L1", "role": "evidence_chain"},
    {"protocol_ref": "Model Manager Admission / Registry", "layer": "Model Manager Protocol", "role": "registry_governance"},
    {"protocol_ref": "Change Control / Review / Freeze", "layer": "Governance", "role": "phase_governance"},
    {"protocol_ref": "Permission / Admission Contract", "layer": "L1", "role": "permission_gates"},
    {"protocol_ref": "Input / Output Symmetry Contract", "layer": "L1", "role": "io_symmetry"},
]


def build_model_skill_admission_contract_mapping() -> Dict[str, Any]:
    return {
        "mapping_id": "option_b_model_skill_admission_contract_mapping_v1",
        "primary_contract": PRIMARY_CONTRACT,
        "option_b_scope": "document_surface_detector_v1_segmentation_candidate_route",
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "referenced_protocols": REFERENCED_PROTOCOLS,
        "option_b_status_under_contract": {
            "model_candidate_route": True,
            "skill_candidate_route": True,
            "model_admitted": False,
            "skill_admitted": False,
            "runtime_admitted": False,
            "active_model": False,
            "active_skill": False,
            "model_skill_admission_required": True,
        },
        "local_admission_mounted": True,
        "local_admission_replaces_contract": False,
        "candidate_only": True,
        "not_fact": True,
    }

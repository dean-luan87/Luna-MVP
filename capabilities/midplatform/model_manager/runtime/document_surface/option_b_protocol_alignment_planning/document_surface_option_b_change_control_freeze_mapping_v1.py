# -*- coding: utf-8 -*-
"""Document Surface — Option B change control / freeze protocol mapping v1."""

from __future__ import annotations

from typing import Any, Dict, List

ADJUSTED_PIPELINE = [
    "OptionB Candidate Route",
    "OptionB Dependency / Model Candidate Admission",
    "Model / Skill Admission Protocol Alignment",
    "OptionB Preflight Planning",
    "OptionB Controlled Execution Planning",
]

COMPLETED_PHASES = [
    "OptionB Candidate Route DryRun",
    "OptionB Candidate Route Post-Review",
    "OptionB Dependency And Model Candidate Admission Planning",
    "OptionB Dependency And Model Candidate Admission DryRun",
    "OptionB Dependency And Model Candidate Admission Post-Review",
]

PENDING_PHASES = [
    "OptionB Model-Skill Admission Protocol Alignment DryRun",
    "OptionB Model-Skill Admission Protocol Alignment Post-Review",
    "OptionB Preflight Planning",
]


def build_change_control_freeze_mapping() -> Dict[str, Any]:
    return {
        "mapping_id": "option_b_change_control_freeze_mapping_v1",
        "change_control_contract": "Change Control / Review / Freeze",
        "boundary_status": "frozen",
        "adjusted_pipeline": ADJUSTED_PIPELINE,
        "completed_phases": COMPLETED_PHASES,
        "current_phase": "OptionB Model-Skill Admission Protocol Alignment Planning",
        "pending_phases": PENDING_PHASES,
        "phase_pattern_required": ["Planning", "DryRun", "Post-Review"],
        "skip_to_execution_forbidden": True,
        "skip_protocol_alignment_forbidden": True,
        "candidate_only": True,
        "not_fact": True,
    }

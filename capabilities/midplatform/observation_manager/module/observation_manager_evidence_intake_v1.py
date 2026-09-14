from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    not_fact,
)


def build_observation_evidence_intake_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    vision_evidence_refs = tuple(input_candidate.get("vision_evidence_refs") or ())
    ocr_evidence_refs = tuple(input_candidate.get("ocr_evidence_refs") or ())
    source_constraints = dict(input_candidate.get("source_constraints") or {})

    evidence_conflicted = bool(source_constraints.get("conflicting_evidence", False))
    evidence_sufficient_hint = bool(source_constraints.get("evidence_sufficient", True))

    return {
        "schema_version": "observation_manager_evidence_intake_v1",
        "vision_evidence_refs": vision_evidence_refs,
        "ocr_evidence_refs": ocr_evidence_refs,
        "vision_evidence_present": bool(vision_evidence_refs),
        "ocr_evidence_present": bool(ocr_evidence_refs),
        "evidence_conflicted": evidence_conflicted,
        "evidence_sufficient_hint": evidence_sufficient_hint,
        **not_fact(),
    }

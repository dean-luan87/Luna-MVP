from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    not_fact,
)


def build_observation_admission_handoff_candidate_v1(
    input_candidate: Mapping[str, Any],
    observation_candidate: Mapping[str, Any],
    trace_ref: str,
) -> Dict[str, Any]:
    return {
        "schema_version": "observation_manager_admission_handoff_candidate_v1",
        "request_id": f"admission_handoff_{input_candidate.get('observation_request_id')}",
        "request_type": "evidence_admission",
        "subject_ref": (input_candidate.get("task_context") or {}).get("subject_ref")
        or "observation_pipeline",
        "resource_ref": observation_candidate.get("candidate_id"),
        "source_ref": input_candidate.get("observation_request_id"),
        "owner_ref": (input_candidate.get("permission_context") or {}).get("owner_ref")
        or "observation_manager",
        "consent_ref": (input_candidate.get("permission_context") or {}).get(
            "consent_ref"
        ),
        "evidence_refs": list(observation_candidate.get("vision_evidence_refs") or ())
        + list(observation_candidate.get("ocr_evidence_refs") or ()),
        "provenance_refs": [trace_ref],
        "requested_authority": "admission_candidate",
        "requested_operation": "evaluate",
        "policy_snapshot": (input_candidate.get("permission_context") or {}).get(
            "policy_snapshot"
        )
        or {},
        "version_snapshot": input_candidate.get("version_snapshot") or {},
        "temporal_snapshot": input_candidate.get("temporal_snapshot") or {},
        "risk_context": (input_candidate.get("permission_context") or {}).get(
            "risk_context"
        )
        or {},
        "trace_ref": trace_ref,
        "candidate_only": True,
        **not_fact(),
    }

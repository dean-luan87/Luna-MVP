from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.ocr_manager.module.ocr_manager_crossmodal_consistency_v1 import (
    build_ocr_manager_crossmodal_consistency_v1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_diagnostics_v1 import (
    build_ocr_manager_diagnostics_v1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_enhancement_candidate_v1 import (
    build_ocr_manager_enhancement_candidates_v1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_engine_capability_adapter_v1 import (
    build_ocr_manager_engine_capability_adapter_v1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_evidence_envelope_builder_v1 import (
    build_ocr_manager_evidence_envelope_v1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_human_correction_adapter_v1 import (
    build_ocr_manager_human_correction_candidates_v1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_layout_analysis_v1 import (
    build_ocr_manager_layout_candidates_v1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_module_input_adapter_v1 import (
    adapt_ocr_manager_input_v1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_module_output_builder_v1 import (
    build_ocr_manager_result_summary_v1,
    decide_ocr_manager_module_status_v1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_raw_evidence_adapter_v1 import (
    build_ocr_manager_raw_evidence_v1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_reading_order_v1 import (
    build_ocr_manager_reading_order_candidates_v1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_region_attribution_v1 import (
    build_ocr_manager_region_attribution_v1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_request_governance_v1 import (
    run_ocr_manager_request_governance_v1,
)
from capabilities.midplatform.ocr_manager.module.ocr_manager_trace_replay_v1 import (
    build_ocr_manager_trace_replay_v1,
)


def _build_text_blocks(
    raw_evidence: tuple[Mapping[str, Any], ...],
) -> tuple[Dict[str, Any], ...]:
    return tuple(
        {
            "block_id": f"text_block_{index}",
            "text": item.get("normalized_text_candidate") or item.get("raw_text"),
            "line_refs": (item.get("line_ref"),),
            "region_ref": item.get("region_ref"),
            "confidence": item.get("confidence"),
        }
        for index, item in enumerate(raw_evidence)
    )


def run_ocr_manager_module_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    input_candidate = adapt_ocr_manager_input_v1(payload)
    governance = run_ocr_manager_request_governance_v1(input_candidate)
    engine_capability = build_ocr_manager_engine_capability_adapter_v1(
        input_candidate, governance
    )
    raw_evidence = build_ocr_manager_raw_evidence_v1(input_candidate, engine_capability)
    region_attribution_candidates = build_ocr_manager_region_attribution_v1(
        raw_evidence, input_candidate
    )
    layout_candidates = build_ocr_manager_layout_candidates_v1(
        raw_evidence, region_attribution_candidates
    )
    reading_order_candidates = build_ocr_manager_reading_order_candidates_v1(
        raw_evidence
    )
    enhancement_candidates = build_ocr_manager_enhancement_candidates_v1(raw_evidence)
    crossmodal_consistency_candidates = build_ocr_manager_crossmodal_consistency_v1(
        raw_evidence, input_candidate
    )
    correction_candidates = build_ocr_manager_human_correction_candidates_v1(
        input_candidate, raw_evidence
    )

    trace_seed = build_ocr_manager_trace_replay_v1(
        request_id=str(input_candidate.get("request_id") or "none"),
        source_refs=(
            str(input_candidate.get("source_ref") or ""),
            str(input_candidate.get("frame_ref") or ""),
        ),
        engine_snapshot=(engine_capability.get("selected_engine") or {}),
        ocr_contract_version="ocr_request_v0",
        enhancement_version="ocr_enhancement_candidate_v1",
        correction_refs=tuple(
            str(item.get("correction_id") or "") for item in correction_candidates
        ),
        input_payload={
            "request_id": input_candidate.get("request_id"),
            "request_type": input_candidate.get("request_type"),
            "source_ref": input_candidate.get("source_ref"),
            "frame_ref": input_candidate.get("frame_ref"),
            "task_ocr_request": input_candidate.get("task_ocr_request"),
        },
        result_summary={
            "raw_evidence_count": len(raw_evidence),
            "enhancement_count": len(enhancement_candidates),
            "correction_count": len(correction_candidates),
        },
    )

    evidence_envelope = build_ocr_manager_evidence_envelope_v1(
        request_id=str(input_candidate.get("request_id") or "none"),
        source_ref=str(input_candidate.get("source_ref") or ""),
        raw_evidence=raw_evidence,
        layout_candidates=layout_candidates,
        reading_order_candidates=reading_order_candidates,
        region_attribution_candidates=region_attribution_candidates,
        enhancement_candidates=enhancement_candidates,
        correction_candidates=correction_candidates,
        crossmodal_consistency_candidates=crossmodal_consistency_candidates,
        trace_ref=str(trace_seed["trace_ref"]),
        replay_key=str(trace_seed["replay_key"]),
    )

    crossmodal_conflict = any(
        str(item.get("status") or "") == "conflict_candidate"
        for item in crossmodal_consistency_candidates
    )
    module_status = decide_ocr_manager_module_status_v1(
        input_valid=bool(input_candidate.get("input_valid")),
        governance_admitted=bool(governance.get("admitted")),
        engine_ready=str(
            (
                (engine_capability.get("selected_engine") or {}).get("engine_readiness")
                or ""
            )
        )
        not in {"unavailable", ""},
        raw_evidence_count=len(raw_evidence),
        reading_order_ambiguous=any(
            bool(item.get("ambiguous_order")) for item in reading_order_candidates
        ),
        layout_available=len(layout_candidates) > 0,
        enhancement_count=len(enhancement_candidates),
        correction_count=len(correction_candidates),
        crossmodal_conflict=crossmodal_conflict,
        envelope_ready=bool(
            evidence_envelope.get("candidate_only")
            and evidence_envelope.get("not_fact")
        ),
    )

    diagnostics = build_ocr_manager_diagnostics_v1(
        module_status=module_status,
        governance=governance,
        engine_capability=engine_capability,
        region_attribution_candidates=region_attribution_candidates,
        layout_candidates=layout_candidates,
        reading_order_candidates=reading_order_candidates,
        enhancement_candidates=enhancement_candidates,
        correction_candidates=correction_candidates,
        crossmodal_consistency_candidates=crossmodal_consistency_candidates,
        rejection_reasons=tuple(governance.get("rejection_reasons") or ()),
    )

    result_summary = build_ocr_manager_result_summary_v1(
        request_id=str(input_candidate.get("request_id") or "none"),
        module_status=module_status,
        raw_evidence=raw_evidence,
        envelope=evidence_envelope,
    )
    trace_replay = build_ocr_manager_trace_replay_v1(
        request_id=str(input_candidate.get("request_id") or "none"),
        source_refs=(
            str(input_candidate.get("source_ref") or ""),
            str(input_candidate.get("frame_ref") or ""),
        ),
        engine_snapshot=(engine_capability.get("selected_engine") or {}),
        ocr_contract_version="ocr_request_v0",
        enhancement_version="ocr_enhancement_candidate_v1",
        correction_refs=tuple(
            str(item.get("correction_id") or "") for item in correction_candidates
        ),
        input_payload={
            "request_id": input_candidate.get("request_id"),
            "request_type": input_candidate.get("request_type"),
            "source_ref": input_candidate.get("source_ref"),
            "frame_ref": input_candidate.get("frame_ref"),
            "synthetic": input_candidate.get("synthetic_integration_fixture"),
        },
        result_summary=result_summary,
    )

    evidence_envelope = {
        **evidence_envelope,
        "trace_ref": trace_replay["trace_ref"],
        "replay_key": trace_replay["replay_key"],
    }

    return {
        "module_status": module_status,
        "input_candidate": input_candidate,
        "governance": governance,
        "engine_capability_candidate": engine_capability,
        "raw_evidence": raw_evidence,
        "text_blocks": _build_text_blocks(raw_evidence),
        "region_attribution_candidates": region_attribution_candidates,
        "layout_candidates": layout_candidates,
        "reading_order_candidates": reading_order_candidates,
        "enhancement_candidates": enhancement_candidates,
        "correction_candidates": correction_candidates,
        "crossmodal_consistency_candidates": crossmodal_consistency_candidates,
        "evidence_envelope": evidence_envelope,
        "diagnostics": diagnostics,
        "trace_ref": trace_replay["trace_ref"],
        "replay_key": trace_replay["replay_key"],
        "fact_admission_executed": False,
        "state_mutation_executed": False,
        "action_execution_executed": False,
        "navigation_decision_executed": False,
        "speech_output_executed": False,
        "database_write_executed": False,
        "provider_recall_executed": False,
        "external_lookup_executed": False,
        "model_training_executed": False,
        "production_runtime_executed": False,
    }

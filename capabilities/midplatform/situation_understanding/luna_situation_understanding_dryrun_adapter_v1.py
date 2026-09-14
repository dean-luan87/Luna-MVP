# -*- coding: utf-8
"""Luna Situation Understanding — dry-run adapter v1 (job/envelope → situation input)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.situation_understanding.luna_situation_understanding_processor_v1 import (
    build_situation_understanding_candidate,
)
from capabilities.midplatform.situation_understanding.luna_situation_understanding_types_v1 import (
    POLICY_REF,
)

CASE_LIBRARY: Dict[str, Dict[str, Any]] = {
    "shopfront_sign_case": {
        "case_id": "shopfront_sign_case",
        "case_type": "shopfront_sign",
        "similarity_score": 0.9,
        "matched_clues": ["large_text_density", "storefront_layout"],
        "candidate_only": True,
        "not_fact": True,
    },
    "subway_platform_case": {
        "case_id": "subway_platform_case",
        "case_type": "subway_platform",
        "similarity_score": 0.88,
        "matched_clues": ["direction_sign_text_density", "public_transport_hint"],
        "candidate_only": True,
        "not_fact": True,
    },
    "street_crossing_case": {
        "case_id": "street_crossing_case",
        "case_type": "street_crossing",
        "similarity_score": 0.85,
        "matched_clues": ["crosswalk_hint", "vehicle_hint"],
        "candidate_only": True,
        "not_fact": True,
    },
    "corridor_case": {
        "case_id": "corridor_case",
        "case_type": "corridor",
        "similarity_score": 0.84,
        "matched_clues": ["corridor_lines", "indoor_path"],
        "candidate_only": True,
        "not_fact": True,
    },
    "unknown_scene_case": {
        "case_id": "unknown_scene_case",
        "case_type": "unknown_scene",
        "similarity_score": 0.3,
        "matched_clues": [],
        "candidate_only": True,
        "not_fact": True,
    },
    "teacher_accepted_shopfront_case": {
        "case_id": "teacher_accepted_shopfront_case",
        "case_type": "shopfront_sign",
        "similarity_score": 0.87,
        "matched_clues": ["teacher_label_accepted"],
        "candidate_only": True,
        "not_fact": True,
    },
}

FILENAME_CASE_MAP = {
    "ocr_real_image_shop_sign": "shopfront_sign_case",
    "shop_sign": "shopfront_sign_case",
    "subway_direction_sign_jiahuihu": "subway_platform_case",
    "street_crossing": "street_crossing_case",
    "corridor": "corridor_case",
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _evidence(
    eid: str,
    source: str,
    etype: str,
    value: str,
    conf: float = 0.75,
    trace_ref: str = "",
) -> Dict[str, Any]:
    return {
        "evidence_id": eid,
        "source": source,
        "evidence_type": etype,
        "value": value,
        "confidence": conf,
        "source_trace_ref": trace_ref or eid,
        "candidate_only": True,
        "not_fact": True,
    }


def extract_frame_context(job_envelope: Dict[str, Any]) -> Dict[str, Any]:
    manifest = job_envelope.get("asset_manifest", {})
    job_id = job_envelope.get("job_id", "")
    file_name = manifest.get("file_name") or manifest.get("local_file_name", "")
    return {
        "frame_id": f"frame_{job_id or file_name}",
        "image_id": manifest.get("asset_id", f"img_{file_name}"),
        "file_name": file_name,
        "timestamp": job_envelope.get("created_at", job_envelope.get("updated_at", "")),
        "source": job_envelope.get("source", "replay"),
        "job_id_optional": job_id,
        "environment_ref_optional": job_envelope.get("environment_ref_optional", ""),
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": [{"stage": "job_envelope", "ref": job_id}],
    }


def extract_runner_scene_hint_as_evidence(job_envelope: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Runner scene_hint → visual_evidence_candidate only, never scene owner."""
    runner = job_envelope.get("runner_result", {})
    scene_cand = runner.get("scene_profile_candidate", {})
    hint = (
        job_envelope.get("runner_scene_hint_optional")
        or scene_cand.get("scene_type_candidate")
        or runner.get("scene_type_candidate")
    )
    if not hint:
        return None
    eid = _uid("ev_runner_scene")
    return _evidence(
        eid,
        "runner_scene_hint",
        "scene_hint",
        hint,
        conf=float(scene_cand.get("confidence", 0.55)),
        trace_ref=job_envelope.get("job_id", eid),
    )


def extract_visual_evidence_candidates(job_envelope: Dict[str, Any]) -> List[Dict[str, Any]]:
    evidence: List[Dict[str, Any]] = []
    frame = extract_frame_context(job_envelope)
    file_name = frame.get("file_name", "").lower()
    runner = job_envelope.get("runner_result", {})
    job_id = job_envelope.get("job_id", "")

    runner_ev = extract_runner_scene_hint_as_evidence(job_envelope)
    if runner_ev:
        evidence.append(runner_ev)

    if "shop_sign" in file_name or "shopfront" in file_name:
        evidence.extend([
            _evidence(_uid("ev_fn"), "metadata", "text_density", "large_text_density", 0.85, job_id),
            _evidence(_uid("ev_fn2"), "metadata", "scene_hint", "storefront_layout", 0.82, job_id),
            _evidence(_uid("ev_fn3"), "metadata", "region", "logo_region", 0.78, job_id),
        ])
    if "subway" in file_name or "jiahuihu" in file_name:
        evidence.extend([
            _evidence(_uid("ev_sub1"), "metadata", "scene_hint", "platform_screen_door", 0.84, job_id),
            _evidence(_uid("ev_sub2"), "text_detector", "text_density", "direction_sign_text_density", 0.86, job_id),
            _evidence(_uid("ev_sub3"), "metadata", "scene_hint", "public_transport_hint", 0.8, job_id),
        ])
    if "street_crossing" in file_name or "crosswalk" in file_name:
        evidence.extend([
            _evidence(_uid("ev_st1"), "detection", "scene_hint", "crosswalk_hint", 0.83, job_id),
            _evidence(_uid("ev_st2"), "detection", "object_hint", "vehicle_hint", 0.8, job_id),
            _evidence(_uid("ev_st3"), "detection", "object_hint", "person_hint", 0.78, job_id),
            _evidence(_uid("ev_st4"), "metadata", "spatial_hint", "open_road", 0.76, job_id),
        ])
    if "corridor" in file_name:
        evidence.extend([
            _evidence(_uid("ev_co1"), "metadata", "spatial_hint", "corridor_lines", 0.82, job_id),
            _evidence(_uid("ev_co2"), "depth", "spatial_hint", "indoor_path", 0.8, job_id),
            _evidence(_uid("ev_co3"), "sam", "spatial_hint", "spatial_boundary", 0.78, job_id),
        ])

    prompt_policy = runner.get("segmentation_prompt_policy", {})
    prompt_set_id = (
        job_envelope.get("prompt_set_id_optional")
        or prompt_policy.get("prompt_set_id", "")
    )
    if prompt_set_id:
        evidence.append(_evidence(
            _uid("ev_ps"), "sam", "scene_hint", f"prompt_set:{prompt_set_id}", 0.7, job_id,
        ))
        if "generic" in prompt_set_id:
            evidence.append(_evidence(
                _uid("ev_gen"), "sam", "region", "generic_sam_regions", 0.65, job_id,
            ))

    for i, pr in enumerate(runner.get("prompt_results", [])[:5]):
        pid = pr.get("prompt_id", f"region_{i}")
        evidence.append(_evidence(
            _uid(f"ev_sam_{i}"),
            "sam",
            "region",
            pid if "generic" in pid else f"sam_region:{pid}",
            float(pr.get("score", 0.7)),
            job_id,
        ))
        if pr.get("ocr_route_candidate") is False:
            evidence.append(_evidence(
                _uid(f"ev_ocr_false_{i}"),
                "metadata",
                "user_signal",
                "ocr_route_candidate_false",
                0.9,
                job_id,
            ))

    for rec in job_envelope.get("observation_attention_records_optional", []):
        hint = rec.get("attention_hint") or rec.get("target_type", "")
        if hint:
            evidence.append(_evidence(
                _uid("ev_attn"), "metadata", "user_signal", f"attention:{hint}", 0.72, job_id,
            ))

    for hc in job_envelope.get("human_correction_hints_optional", []):
        evidence.append(_evidence(
            _uid("ev_hc"),
            "human_correction",
            "user_signal",
            hc.get("correction_text", "human_correction"),
            0.8,
            job_id,
        ))

    for extra in job_envelope.get("dryrun_extra_evidence", []):
        evidence.append(extra)

    return evidence


def attach_case_refs(job_envelope: Dict[str, Any]) -> List[Dict[str, Any]]:
    refs: List[Dict[str, Any]] = []
    explicit = job_envelope.get("situation_case_refs_optional", [])
    if explicit:
        for ref in explicit:
            cid = ref if isinstance(ref, str) else ref.get("case_id", "")
            if cid in CASE_LIBRARY:
                refs.append(dict(CASE_LIBRARY[cid]))
            elif isinstance(ref, dict):
                refs.append(ref)
        return refs

    frame = extract_frame_context(job_envelope)
    file_name = frame.get("file_name", "").lower()
    for key, case_id in FILENAME_CASE_MAP.items():
        if key in file_name:
            refs.append(dict(CASE_LIBRARY[case_id]))
            break

    case_key = job_envelope.get("dryrun_case_ref_key")
    if case_key and case_key in CASE_LIBRARY:
        refs.append(dict(CASE_LIBRARY[case_key]))

    return refs


def build_input_from_job_envelope(job_envelope: Dict[str, Any]) -> Dict[str, Any]:
    goal = job_envelope.get("user_goal_candidate_optional", {})
    return {
        "frame_context": extract_frame_context(job_envelope),
        "user_goal_candidate": {
            "goal_text_optional": goal.get("goal_text_optional", ""),
            "goal_type": goal.get("goal_type", "unknown"),
            "confidence": goal.get("confidence", 0.2),
            "source": goal.get("source", "unknown"),
            "candidate_only": True,
            "not_fact": True,
        },
        "visual_evidence_candidates": extract_visual_evidence_candidates(job_envelope),
        "situation_case_refs": attach_case_refs(job_envelope),
        "environment_memory_candidates": job_envelope.get("environment_memory_candidates_optional", []),
        "human_correction_signals": job_envelope.get("human_correction_signals_optional", []),
        "available_capabilities": job_envelope.get("available_capabilities_optional", [
            {"capability_id": "cap_ocr", "capability_type": "ocr", "availability": "available"},
            {"capability_id": "cap_slam", "capability_type": "slam", "availability": "available"},
            {"capability_id": "cap_depth", "capability_type": "depth", "availability": "available"},
            {"capability_id": "cap_detection", "capability_type": "detection", "availability": "available"},
            {"capability_id": "cap_tracking", "capability_type": "tracking", "availability": "available"},
            {"capability_id": "cap_vlm", "capability_type": "vlm", "availability": "available"},
        ]),
        "candidate_only": True,
        "not_fact": True,
        "trace_refs": [{"stage": "dryrun_adapter", "ref": job_envelope.get("job_id", "")}],
    }


def build_situation_input_for_dryrun(job_envelope: Dict[str, Any]) -> Dict[str, Any]:
    return build_input_from_job_envelope(job_envelope)


def _model_need_summary(candidate: Dict[str, Any]) -> Dict[str, List[str]]:
    hints = candidate.get("model_need_hints", {})
    return {
        "likely_needed": [h["capability_type"] for h in hints.get("likely_needed", [])],
        "optional": [h["capability_type"] for h in hints.get("optional", [])],
        "not_needed": [h["capability_type"] for h in hints.get("not_needed", [])],
    }


def run_situation_understanding_dryrun(job_envelope: Dict[str, Any]) -> Dict[str, Any]:
    """Full dry-run: envelope → input → candidate + traces. No runner execution."""
    situation_input = build_situation_input_for_dryrun(job_envelope)
    candidate = build_situation_understanding_candidate(situation_input)

    runner_ev = extract_runner_scene_hint_as_evidence(job_envelope)
    scene = candidate.get("scene_profile_candidate", {})
    scene["owned_by"] = "situation_understanding_layer"

    conflict_traces = [
        t for t in scene.get("trace_refs", [])
        if t.get("stage") in ("runner_scene_hint_conflict", "runner_scene_hint_received")
    ]
    conflict_traces.extend(candidate.get("trace_refs", []))

    scene_resolution_trace = {
        "scene_type": scene.get("scene_type"),
        "owned_by": "situation_understanding_layer",
        "runner_scene_hint": runner_ev.get("value") if runner_ev else None,
        "conflict_traces": conflict_traces,
        "policy_refs": [POLICY_REF, "scene_profile_owned_by_situation_layer"],
        "candidate_only": True,
        "not_fact": True,
    }

    return {
        "job_id": job_envelope.get("job_id", ""),
        "situation_understanding_input": situation_input,
        "situation_understanding_candidate": candidate,
        "scene_resolution_trace": scene_resolution_trace,
        "runner_scene_hint_evidence_record": runner_ev,
        "conflict_trace_optional": conflict_traces if conflict_traces else None,
        "model_need_hint_summary": _model_need_summary(candidate),
        "no_runner_invocation_assertion": True,
        "no_fact_write_assertion": True,
        "dryrun_only": True,
        "no_real_model_execution": True,
    }

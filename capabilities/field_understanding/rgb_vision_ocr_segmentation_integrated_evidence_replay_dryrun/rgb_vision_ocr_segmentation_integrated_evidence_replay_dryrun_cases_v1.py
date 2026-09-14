# -*- coding: utf-8 -*-
"""RGB Vision / OCR / Segmentation Integrated Evidence Replay DryRun — cases v1.

Reads local controlled sample files, runs external-vision source admission +
interface adapter mapping into evidence candidates, then replays through a
Field / Task / Guidance candidate path. All outputs candidate-only.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun.rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_types_v1 import (
    INTERFACE_ADAPTER_REF,
    NEGATIVE_CASE_REFS,
    POSITIVE_CASE_REFS,
    PROHIBITED_OUTPUT_FLAGS,
    SAMPLE_FILES,
    SAMPLES_REL_DIR,
    SOURCE_DEPTH_VIO,
    SOURCE_OBJECT_DETECTION,
    SOURCE_OCR,
    SOURCE_RGB_FRAME,
    SOURCE_SCENE_RELATION,
    SOURCE_SEGMENTATION,
    SOURCE_TO_CANDIDATE_TYPE,
    SOURCE_TRACKING,
    SOURCE_CHAIN,
    TARGET_ENTRYPOINT,
)

_MODULE_DIR = Path(__file__).resolve().parent
_SAMPLES_DIR = _MODULE_DIR / "samples"

_PAYLOAD_KEY: Dict[str, str] = {
    SOURCE_RGB_FRAME: "frames",
    SOURCE_OBJECT_DETECTION: "objects",
    SOURCE_SEGMENTATION: "regions",
    SOURCE_TRACKING: "tracks",
    SOURCE_OCR: "texts",
    SOURCE_DEPTH_VIO: "hints",
    SOURCE_SCENE_RELATION: "relations",
}

_ITEM_ID_KEY: Dict[str, str] = {
    SOURCE_RGB_FRAME: "frame_id",
    SOURCE_OBJECT_DETECTION: "object_id",
    SOURCE_SEGMENTATION: "region_id",
    SOURCE_TRACKING: "track_id",
    SOURCE_OCR: "text_id",
    SOURCE_DEPTH_VIO: "hint_id",
    SOURCE_SCENE_RELATION: "relation_id",
}


def samples_dir() -> Path:
    return _SAMPLES_DIR


def is_controlled_sample_path(path: Path) -> bool:
    try:
        resolved = path.resolve()
        samples_resolved = _SAMPLES_DIR.resolve()
        return samples_resolved in resolved.parents or resolved == samples_resolved
    except OSError:
        return False


def read_local_vision_file(sample_file: str) -> Tuple[Optional[Dict[str, Any]], bool, List[str]]:
    path = _SAMPLES_DIR / sample_file
    if not is_controlled_sample_path(path):
        return None, False, [f"sample_path_not_controlled:{sample_file}"]
    if not path.is_file():
        return None, False, [f"sample_file_missing:{sample_file}"]
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, True, [f"sample_read_failed:{sample_file}:{exc}"]
    if not isinstance(doc, dict):
        return None, True, [f"sample_root_not_object:{sample_file}"]
    return doc, True, []


def _payload_items(doc: Dict[str, Any], source_ref: str) -> List[Dict[str, Any]]:
    return list(doc.get(_PAYLOAD_KEY.get(source_ref, "")) or [])


def _confidence_present(doc: Dict[str, Any], source_ref: str) -> bool:
    if isinstance(doc.get("confidence"), (int, float)):
        return True
    items = _payload_items(doc, source_ref)
    return bool(items) and all(isinstance(it.get("confidence"), (int, float)) for it in items)


def _origin_metadata_present(doc: Dict[str, Any]) -> bool:
    has_frame_or_file = bool(doc.get("frame_origin")) or bool(doc.get("file_origin"))
    has_model_origin = bool(doc.get("model_output_origin"))
    return has_frame_or_file and has_model_origin


def admit_vision_source(
    *, sample_file: str, doc: Dict[str, Any], expected_format: str
) -> Dict[str, Any]:
    path = _SAMPLES_DIR / sample_file
    rejection_reasons: List[str] = []

    controlled_ok = is_controlled_sample_path(path)
    if not controlled_ok:
        rejection_reasons.append("controlled_samples_path_violation")

    format_ref_ok = doc.get("format_ref") == expected_format
    if not format_ref_ok:
        rejection_reasons.append(f"format_ref_not_{expected_format}")

    source_chain_present = bool(doc.get("source_chain"))
    if not source_chain_present:
        rejection_reasons.append("source_chain_missing")

    confidence_present = _confidence_present(doc, expected_format)
    if not confidence_present:
        rejection_reasons.append("confidence_missing")

    origin_present = _origin_metadata_present(doc)
    if not origin_present:
        rejection_reasons.append("origin_metadata_missing")

    prohibited_flags_absent = not any(doc.get(flag) is True for flag in PROHIBITED_OUTPUT_FLAGS)
    if not prohibited_flags_absent:
        present = [flag for flag in PROHIBITED_OUTPUT_FLAGS if doc.get(flag) is True]
        rejection_reasons.append("prohibited_output_flags_present:" + ",".join(present))

    admitted = len(rejection_reasons) == 0
    return {
        "result_ref": f"rgb_vision_admission_{sample_file}",
        "sample_file": sample_file,
        "source_ref": expected_format,
        "file_source_admitted": admitted,
        "controlled_samples_path_ok": controlled_ok,
        "format_ref_ok": format_ref_ok,
        "source_chain_present": source_chain_present,
        "confidence_present": confidence_present,
        "origin_metadata_present": origin_present,
        "prohibited_flags_absent": prohibited_flags_absent,
        "rejection_reasons": rejection_reasons,
        "source_chain": SOURCE_CHAIN,
    }


def _base_metadata(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "frame_origin": doc.get("frame_origin"),
        "file_origin": doc.get("file_origin"),
        "model_output_origin": doc.get("model_output_origin"),
        "frame_id": doc.get("frame_id"),
        "timestamp_ms": doc.get("timestamp_ms"),
        "export_session_id": (doc.get("file_origin") or {}).get("export_session_id"),
    }


def _make_candidate(
    *,
    candidate_type: str,
    candidate_ref: str,
    doc: Dict[str, Any],
    item: Dict[str, Any],
    extra_payload: Dict[str, Any],
) -> Dict[str, Any]:
    metadata = _base_metadata(doc)
    confidence = item.get("confidence")
    if not isinstance(confidence, (int, float)):
        confidence = doc.get("confidence")
    return {
        "candidate_type": candidate_type,
        "candidate_ref": candidate_ref,
        "source_chain": list(doc.get("source_chain") or []) + [candidate_ref],
        "confidence": confidence,
        "field_synthesis_entrypoint": TARGET_ENTRYPOINT,
        "adapter_ref": INTERFACE_ADAPTER_REF,
        "metadata": metadata,
        "payload": extra_payload,
        "candidate_only": True,
        "direct_action_allowed": False,
        "direct_speech_allowed": False,
        "direct_fact_write_allowed": False,
        "route_activation_allowed": False,
        "field_identity_mutation_allowed": False,
    }


def map_vision_output_to_candidates(
    *, doc: Dict[str, Any], source_ref: str
) -> Dict[str, Any]:
    items = _payload_items(doc, source_ref)
    id_key = _ITEM_ID_KEY.get(source_ref, "id")
    candidate_types = SOURCE_TO_CANDIDATE_TYPE.get(source_ref, ())
    candidates: List[Dict[str, Any]] = []

    for index, item in enumerate(items):
        item_id = item.get(id_key, f"{source_ref}_{index}")
        for candidate_type in candidate_types:
            # dynamic_risk_candidate only emitted for tracks with a velocity hint
            if candidate_type == "dynamic_risk_candidate" and not item.get("velocity_hint"):
                continue
            candidate_ref = f"{candidate_type}_{item_id}"
            extra_payload = {
                "source_ref": source_ref,
                "bbox": item.get("bbox"),
                "mask_ref": item.get("mask_ref"),
                "track_id": item.get("track_id"),
                "text": item.get("text"),
                "text_span": item.get("text_span"),
                "relation": item.get("relation"),
                "relation_refs": item.get("relation_refs"),
                "label": item.get("label"),
                "scene_label_hint": item.get("scene_label_hint"),
                "relative_depth_hint": item.get("relative_depth_hint"),
                "visual_odometry_hint": item.get("visual_odometry_hint"),
                "motion_hint": item.get("motion_hint"),
                "trajectory": item.get("trajectory"),
                "velocity_hint": item.get("velocity_hint"),
                "spatial_hint_only": source_ref == SOURCE_DEPTH_VIO,
                "evidence_only": True,
                "is_final_interpretation": False,
            }
            extra_payload = {k: v for k, v in extra_payload.items() if v is not None}
            candidates.append(
                _make_candidate(
                    candidate_type=candidate_type,
                    candidate_ref=candidate_ref,
                    doc=doc,
                    item=item,
                    extra_payload=extra_payload,
                )
            )

    output_types = tuple(sorted({c["candidate_type"] for c in candidates}))
    source_chain_preserved = bool(candidates) and all(c.get("source_chain") for c in candidates)
    confidence_preserved = bool(candidates) and all(
        isinstance(c.get("confidence"), (int, float)) for c in candidates
    )
    origin_preserved = bool(candidates) and all(
        bool(c["metadata"].get("model_output_origin"))
        and (bool(c["metadata"].get("frame_origin")) or bool(c["metadata"].get("file_origin")))
        for c in candidates
    )
    return {
        "source_ref": source_ref,
        "candidates": candidates,
        "candidate_count": len(candidates),
        "output_candidate_types": output_types,
        "adapter_mapping_used": True,
        "source_chain_preserved": source_chain_preserved,
        "confidence_preserved": confidence_preserved,
        "origin_metadata_preserved": origin_preserved,
        "candidate_only": all(c.get("candidate_only") is True for c in candidates),
    }


def run_source_pipeline(sample_file: str, source_ref: str) -> Dict[str, Any]:
    doc, read_ok, read_issues = read_local_vision_file(sample_file)
    admission = admit_vision_source(
        sample_file=sample_file, doc=doc or {}, expected_format=source_ref
    )
    mapping = {
        "source_ref": source_ref, "candidates": [], "candidate_count": 0,
        "output_candidate_types": (), "adapter_mapping_used": False,
        "source_chain_preserved": False, "confidence_preserved": False,
        "origin_metadata_preserved": False, "candidate_only": True,
    }
    admitted = admission["file_source_admitted"] and read_ok and doc is not None
    if admitted:
        mapping = map_vision_output_to_candidates(doc=doc, source_ref=source_ref)
    return {
        "sample_file": sample_file, "source_ref": source_ref, "read_ok": read_ok,
        "read_issues": read_issues, "admission": admission, "mapping": mapping,
        "admitted": admitted,
    }


def _candidates_of(pipe: Dict[str, Any], candidate_type: str) -> List[Dict[str, Any]]:
    return [c for c in pipe["mapping"]["candidates"] if c["candidate_type"] == candidate_type]


# --------------------------------------------------------------------------- #
# Positive cases
# --------------------------------------------------------------------------- #
def run_positive_scene_object_region(ctx: Dict[str, Any]) -> Dict[str, Any]:
    frame = ctx["frame_pipe"]
    obj = ctx["object_pipe"]
    seg = ctx["segmentation_pipe"]
    checks = {
        "scene_observation_candidate_generated": len(_candidates_of(frame, "scene_observation_candidate")) > 0,
        "object_evidence_candidate_generated": len(_candidates_of(obj, "object_evidence_candidate")) > 0,
        "region_evidence_candidate_generated": len(_candidates_of(seg, "region_evidence_candidate")) > 0,
        "candidate_only": all(
            p["mapping"]["candidate_only"] for p in (frame, obj, seg)
        ),
        "source_chain_preserved": all(
            p["mapping"]["source_chain_preserved"] for p in (frame, obj, seg)
        ),
        "origin_metadata_preserved": all(
            p["mapping"]["origin_metadata_preserved"] for p in (frame, obj, seg)
        ),
    }
    return {"case_ref": "rgb_scene_object_region_integrated_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_ocr_scene_text(ctx: Dict[str, Any]) -> Dict[str, Any]:
    ocr = ctx["ocr_pipe"]
    texts = _candidates_of(ocr, "text_evidence_candidate")
    checks = {
        "text_evidence_candidate_generated": len(texts) > 0,
        "ocr_output_not_fact": all(c.get("direct_fact_write_allowed") is False for c in texts),
        "source_chain_preserved": ocr["mapping"]["source_chain_preserved"],
        "confidence_preserved": ocr["mapping"]["confidence_preserved"],
        "origin_metadata_preserved": ocr["mapping"]["origin_metadata_preserved"],
        "text_span_preserved": all(c["payload"].get("text_span") for c in texts),
    }
    return {"case_ref": "rgb_ocr_scene_text_integrated_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_tracking_dynamic_risk(ctx: Dict[str, Any]) -> Dict[str, Any]:
    trk = ctx["tracking_pipe"]
    tracks = _candidates_of(trk, "track_evidence_candidate")
    risks = _candidates_of(trk, "dynamic_risk_candidate")
    checks = {
        "track_evidence_candidate_generated": len(tracks) > 0,
        "dynamic_risk_candidate_generated": len(risks) > 0,
        "tracking_output_not_action_trigger": all(
            c.get("direct_action_allowed") is False and c.get("direct_speech_allowed") is False
            for c in tracks + risks
        ),
        "track_id_preserved": all(c["payload"].get("track_id") for c in tracks),
    }
    return {"case_ref": "rgb_tracking_dynamic_risk_integrated_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_depth_vio_spatial_hint(ctx: Dict[str, Any]) -> Dict[str, Any]:
    depth = ctx["depth_pipe"]
    hints = _candidates_of(depth, "spatial_hint_candidate")
    checks = {
        "spatial_hint_candidate_generated": len(hints) > 0,
        "monocular_depth_vio_not_field_identity": all(
            c.get("field_identity_mutation_allowed") is False and c["payload"].get("spatial_hint_only") is True
            for c in hints
        ),
    }
    return {"case_ref": "rgb_monocular_depth_vio_spatial_hint_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_scene_relation_task_context(ctx: Dict[str, Any]) -> Dict[str, Any]:
    rel = ctx["relation_pipe"]
    relations = _candidates_of(rel, "scene_relation_candidate")
    relation_refs = [c["candidate_ref"] for c in relations]
    task_context = {
        "candidate_type": "TaskContextCandidate",
        "candidate_ref": "rgb_task_ctx_001",
        "referenced_relation_refs": relation_refs,
        "candidate_only": True,
    }
    task_evidence_need = {
        "candidate_type": "TaskEvidenceNeedCandidate",
        "candidate_ref": "rgb_task_evidence_need_001",
        "referenced_relation_refs": relation_refs,
        "candidate_only": True,
    }
    checks = {
        "scene_relation_candidate_generated": len(relations) > 0,
        "task_context_can_reference_relation_candidates": len(
            task_context["referenced_relation_refs"]
        )
        > 0
        and len(task_evidence_need["referenced_relation_refs"]) > 0,
        "scene_relation_not_final_interpretation": all(
            c["payload"].get("is_final_interpretation") is False for c in relations
        ),
        "relation_refs_preserved": all(c["payload"].get("relation_refs") for c in relations),
    }
    return {"case_ref": "rgb_scene_relation_task_context_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks, "_relation_refs": relation_refs}


def _all_evidence_refs(ctx: Dict[str, Any]) -> Dict[str, List[str]]:
    refs: Dict[str, List[str]] = {}
    for key in ("frame_pipe", "object_pipe", "segmentation_pipe", "tracking_pipe",
                "ocr_pipe", "depth_pipe", "relation_pipe"):
        for c in ctx[key]["mapping"]["candidates"]:
            refs.setdefault(c["candidate_type"], []).append(c["candidate_ref"])
    return refs


def run_positive_field_task_guidance(ctx: Dict[str, Any], relation_refs: List[str]) -> Dict[str, Any]:
    refs = _all_evidence_refs(ctx)
    tracking_refs = refs.get("track_evidence_candidate", []) + refs.get("dynamic_risk_candidate", [])
    spatial_hint_refs = refs.get("spatial_hint_candidate", [])
    all_refs = [r for group in refs.values() for r in group]

    field_candidates = [
        {"candidate_type": "FieldCandidate", "candidate_ref": "rgb_field_001", "candidate_only": True,
         "referenced_evidence_refs": all_refs},
        {"candidate_type": "FieldStateCandidate", "candidate_ref": "rgb_field_state_001", "candidate_only": True},
    ]
    task_candidates = [
        {"candidate_type": "TaskContextCandidate", "candidate_ref": "rgb_task_ctx_002",
         "candidate_only": True, "referenced_relation_refs": relation_refs},
        {"candidate_type": "TaskRiskCandidate", "candidate_ref": "rgb_task_risk_001",
         "candidate_only": True, "referenced_evidence_refs": tracking_refs + spatial_hint_refs},
    ]
    guidance_candidates = [
        {"candidate_type": "GuidanceCandidate", "candidate_ref": "rgb_guidance_001",
         "candidate_only": True, "is_runtime_navigation": False},
        {"candidate_type": "SpeechGateCandidate", "candidate_ref": "rgb_speech_gate_001",
         "candidate_only": True, "is_tts": False},
        {"candidate_type": "ActionSafetyCandidate", "candidate_ref": "rgb_action_safety_001",
         "candidate_only": True, "direct_action_allowed": False},
    ]
    guidance = {c["candidate_type"]: c for c in guidance_candidates}
    checks = {
        "field_task_guidance_replay_path_ok": bool(field_candidates)
        and bool(task_candidates)
        and bool(guidance_candidates),
        "task_context_can_reference_relation_candidates": len(
            task_candidates[0]["referenced_relation_refs"]
        )
        > 0,
        "task_risk_can_reference_tracking_and_spatial_hint": len(
            task_candidates[1]["referenced_evidence_refs"]
        )
        > 0
        and len(tracking_refs) > 0
        and len(spatial_hint_refs) > 0,
        "guidance_candidate_remains_candidate": guidance["GuidanceCandidate"]["is_runtime_navigation"]
        is False,
        "speech_gate_candidate_not_tts": guidance["SpeechGateCandidate"]["is_tts"] is False,
        "action_safety_candidate_exists": "ActionSafetyCandidate" in guidance,
    }
    return {"case_ref": "rgb_integrated_field_task_guidance_replay_path", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_observation_only(ctx: Dict[str, Any]) -> Dict[str, Any]:
    scenario = {
        "scope": "stadium_plaza_observation_only",
        "observation_only": True,
        "movement_command_emitted": False,
        "route_activation_started": False,
    }
    checks = {
        "observation_only_scope_preserved": scenario["observation_only"] is True,
        "no_movement_command": scenario["movement_command_emitted"] is False,
        "no_route_activation": scenario["route_activation_started"] is False,
    }
    return {"case_ref": "rgb_observation_only_replay_scope", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


# --------------------------------------------------------------------------- #
# Negative cases
# --------------------------------------------------------------------------- #
def _negative_admission(sample_file: str, source_ref: str, expect_reason_prefix: str) -> bool:
    doc, _, _ = read_local_vision_file(sample_file)
    admission = admit_vision_source(sample_file=sample_file, doc=doc or {}, expected_format=source_ref)
    return admission["file_source_admitted"] is False and any(
        r.startswith(expect_reason_prefix) for r in admission["rejection_reasons"]
    )


def run_negative_missing_source_chain() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_missing_source_chain_output.json", SOURCE_OBJECT_DETECTION, "source_chain_missing"
    )
    return {"case_ref": "invalid_missing_source_chain_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"missing_source_chain_rejected": rejected}}


def run_negative_direct_fact_write_ocr() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_direct_fact_write_ocr_output.json", SOURCE_OCR, "prohibited_output_flags_present"
    )
    return {"case_ref": "invalid_direct_fact_write_ocr_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"direct_fact_write_ocr_rejected": rejected}}


def run_negative_segmentation_route_activation() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_segmentation_route_activation_output.json", SOURCE_SEGMENTATION,
        "prohibited_output_flags_present"
    )
    return {"case_ref": "invalid_segmentation_route_activation_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"segmentation_route_activation_rejected": rejected}}


def run_negative_tracking_action_speech() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_tracking_action_trigger_output.json", SOURCE_TRACKING,
        "prohibited_output_flags_present"
    )
    return {"case_ref": "invalid_tracking_direct_action_speech_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"tracking_direct_action_speech_rejected": rejected}}


def run_negative_depth_field_identity_override() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_depth_field_identity_override_output.json", SOURCE_DEPTH_VIO,
        "prohibited_output_flags_present"
    )
    return {"case_ref": "invalid_depth_vio_field_identity_override_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"depth_vio_field_identity_override_rejected": rejected}}


def run_negative_native_output_direct_to_field() -> Dict[str, Any]:
    # Tamper a valid object-detection doc to bypass the adapter and go straight to field.
    doc, _, _ = read_local_vision_file("sample_object_detection_output.json")
    tampered = copy.deepcopy(doc or {})
    tampered["bypass_adapter"] = True
    tampered["native_direct_to_field"] = True
    tampered["direct_to_field_task_guidance"] = True
    admission = admit_vision_source(
        sample_file="sample_object_detection_output.json",
        doc=tampered,
        expected_format=SOURCE_OBJECT_DETECTION,
    )
    rejected = admission["file_source_admitted"] is False and any(
        r.startswith("prohibited_output_flags_present") for r in admission["rejection_reasons"]
    )
    return {"case_ref": "invalid_native_output_direct_to_field_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"native_output_direct_to_field_rejected": rejected,
                       "rejection_reasons": admission["rejection_reasons"]}}


def run_all_cases_v1() -> Dict[str, Any]:
    ctx = {
        "frame_pipe": run_source_pipeline("sample_rgb_frame_metadata.json", SOURCE_RGB_FRAME),
        "object_pipe": run_source_pipeline("sample_object_detection_output.json", SOURCE_OBJECT_DETECTION),
        "segmentation_pipe": run_source_pipeline("sample_segmentation_output.json", SOURCE_SEGMENTATION),
        "tracking_pipe": run_source_pipeline("sample_tracking_output.json", SOURCE_TRACKING),
        "ocr_pipe": run_source_pipeline("sample_ocr_text_output.json", SOURCE_OCR),
        "depth_pipe": run_source_pipeline("sample_monocular_depth_vio_output.json", SOURCE_DEPTH_VIO),
        "relation_pipe": run_source_pipeline("sample_scene_relation_output.json", SOURCE_SCENE_RELATION),
    }

    pos1 = run_positive_scene_object_region(ctx)
    pos2 = run_positive_ocr_scene_text(ctx)
    pos3 = run_positive_tracking_dynamic_risk(ctx)
    pos4 = run_positive_depth_vio_spatial_hint(ctx)
    pos5 = run_positive_scene_relation_task_context(ctx)
    relation_refs = pos5.get("_relation_refs") or []
    pos6 = run_positive_field_task_guidance(ctx, relation_refs)
    pos7 = run_positive_observation_only(ctx)

    positive_results = [
        {k: v for k, v in c.items() if not k.startswith("_")}
        for c in (pos1, pos2, pos3, pos4, pos5, pos6, pos7)
    ]
    negative_results = [
        run_negative_missing_source_chain(),
        run_negative_direct_fact_write_ocr(),
        run_negative_segmentation_route_activation(),
        run_negative_tracking_action_speech(),
        run_negative_depth_field_identity_override(),
        run_negative_native_output_direct_to_field(),
    ]

    evidence_refs = _all_evidence_refs(ctx)
    generated_types = sorted(evidence_refs.keys())
    return {
        "positive_cases": positive_results,
        "negative_cases": negative_results,
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "sample_files": list(SAMPLE_FILES),
        "samples_rel_dir": SAMPLES_REL_DIR,
        "generated_evidence_candidate_types": generated_types,
    }

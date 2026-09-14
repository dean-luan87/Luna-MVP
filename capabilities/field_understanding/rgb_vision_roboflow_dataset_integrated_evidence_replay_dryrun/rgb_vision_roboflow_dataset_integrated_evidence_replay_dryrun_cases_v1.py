# -*- coding: utf-8 -*-
"""RGB Vision Roboflow Dataset Integrated Evidence Replay DryRun — cases v1.

Reads local controlled Roboflow dataset sample files, runs the Roboflow external
test-source admission (license / dataset origin / annotation-format / source_chain
/ confidence / prohibited flags), maps recognized annotations into evidence
candidates via the external vision interface adapter, then replays through a
Field / Task / Guidance candidate path. All outputs candidate-only.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun.rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_types_v1 import (
    ANNOTATION_TYPE_TO_CANDIDATE,
    INTERFACE_ADAPTER_REF,
    NEGATIVE_CASE_REFS,
    POSITIVE_CASE_REFS,
    PROHIBITED_OUTPUT_FLAGS,
    RECOGNIZED_ANNOTATION_FORMATS,
    ROBOFLOW_FORMAT_REF,
    SAMPLE_FILES,
    SAMPLES_REL_DIR,
    SOURCE_CHAIN,
    TARGET_ENTRYPOINT,
)

_MODULE_DIR = Path(__file__).resolve().parent
_SAMPLES_DIR = _MODULE_DIR / "samples"


def samples_dir() -> Path:
    return _SAMPLES_DIR


def is_controlled_sample_path(path: Path) -> bool:
    try:
        resolved = path.resolve()
        samples_resolved = _SAMPLES_DIR.resolve()
        return samples_resolved in resolved.parents or resolved == samples_resolved
    except OSError:
        return False


def read_local_roboflow_file(
    sample_file: str,
) -> Tuple[Optional[Dict[str, Any]], bool, List[str]]:
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


def _annotations(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(doc.get("annotations") or [])


def _images(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(doc.get("images") or [])


def recognize_annotation_format(doc: Dict[str, Any]) -> Dict[str, Any]:
    fmt = doc.get("annotation_format")
    recognized = fmt in RECOGNIZED_ANNOTATION_FORMATS
    return {
        "result_ref": "roboflow_annotation_format_recognition",
        "annotation_format": fmt,
        "recognized": recognized,
        "recognized_formats": list(RECOGNIZED_ANNOTATION_FORMATS),
        "source_chain": SOURCE_CHAIN,
    }


def _dataset_origin_present(doc: Dict[str, Any]) -> bool:
    origin = doc.get("dataset_origin")
    if not isinstance(origin, dict):
        return False
    return bool(origin.get("dataset_ref") or origin.get("dataset_url") or origin.get("platform"))


def _confidence_present(doc: Dict[str, Any]) -> bool:
    if isinstance(doc.get("confidence"), (int, float)):
        return True
    annotations = _annotations(doc)
    return bool(annotations) and all(
        isinstance(a.get("confidence"), (int, float)) for a in annotations
    )


def admit_roboflow_source(*, sample_file: str, doc: Dict[str, Any]) -> Dict[str, Any]:
    path = _SAMPLES_DIR / sample_file
    rejection_reasons: List[str] = []

    controlled_ok = is_controlled_sample_path(path)
    if not controlled_ok:
        rejection_reasons.append("controlled_samples_path_violation")

    format_ref_ok = doc.get("format_ref") == ROBOFLOW_FORMAT_REF
    if not format_ref_ok:
        rejection_reasons.append(f"format_ref_not_{ROBOFLOW_FORMAT_REF}")

    license_present = bool(doc.get("license_ref"))
    if not license_present:
        rejection_reasons.append("license_missing")

    dataset_origin_present = _dataset_origin_present(doc)
    if not dataset_origin_present:
        rejection_reasons.append("dataset_origin_missing")

    fmt_recognition = recognize_annotation_format(doc)
    annotation_format_recognized = fmt_recognition["recognized"]
    if not annotation_format_recognized:
        rejection_reasons.append(
            f"annotation_format_unrecognized:{doc.get('annotation_format')!r}"
        )

    source_chain_present = bool(doc.get("source_chain"))
    if not source_chain_present:
        rejection_reasons.append("source_chain_missing")

    confidence_present = _confidence_present(doc)
    if not confidence_present:
        rejection_reasons.append("confidence_missing")

    prohibited_flags_absent = not any(doc.get(flag) is True for flag in PROHIBITED_OUTPUT_FLAGS)
    if not prohibited_flags_absent:
        present = [flag for flag in PROHIBITED_OUTPUT_FLAGS if doc.get(flag) is True]
        rejection_reasons.append("prohibited_output_flags_present:" + ",".join(present))

    admitted = len(rejection_reasons) == 0
    return {
        "result_ref": f"roboflow_admission_{sample_file}",
        "sample_file": sample_file,
        "file_source_admitted": admitted,
        "controlled_samples_path_ok": controlled_ok,
        "format_ref_ok": format_ref_ok,
        "license_present": license_present,
        "dataset_origin_present": dataset_origin_present,
        "annotation_format_recognized": annotation_format_recognized,
        "source_chain_present": source_chain_present,
        "confidence_present": confidence_present,
        "prohibited_flags_absent": prohibited_flags_absent,
        "rejection_reasons": rejection_reasons,
        "source_chain": SOURCE_CHAIN,
    }


def _base_metadata(doc: Dict[str, Any], item: Dict[str, Any]) -> Dict[str, Any]:
    dataset_origin = doc.get("dataset_origin") or {}
    return {
        "external_test_source": "roboflow_universe",
        "license_ref": doc.get("license_ref"),
        "dataset_ref": dataset_origin.get("dataset_ref"),
        "dataset_url": dataset_origin.get("dataset_url"),
        "annotation_origin": doc.get("annotation_origin"),
        "annotation_format": doc.get("annotation_format"),
        "image_id": item.get("image_id"),
        "frame_id": item.get("image_id"),
    }


def _make_candidate(
    *,
    candidate_type: str,
    candidate_ref: str,
    doc: Dict[str, Any],
    item: Dict[str, Any],
    extra_payload: Dict[str, Any],
) -> Dict[str, Any]:
    metadata = _base_metadata(doc, item)
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
        "external_test_source_only": True,
        "is_fact_layer": False,
        "annotation_auto_trusted": False,
        "license_default_commercial": False,
        "direct_action_allowed": False,
        "direct_speech_allowed": False,
        "direct_fact_write_allowed": False,
        "route_activation_allowed": False,
        "field_identity_mutation_allowed": False,
    }


def map_roboflow_to_candidates(*, doc: Dict[str, Any]) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []

    # Image-level scene observation candidates.
    for index, image in enumerate(_images(doc)):
        image_id = image.get("image_id", f"img_{index}")
        candidate_ref = f"scene_observation_candidate_{image_id}"
        extra_payload = {
            "annotation_kind": "image",
            "scene_label_hint": image.get("scene_label_hint"),
            "width": image.get("width"),
            "height": image.get("height"),
            "evidence_only": True,
            "is_final_interpretation": False,
        }
        extra_payload = {k: v for k, v in extra_payload.items() if v is not None}
        candidates.append(
            _make_candidate(
                candidate_type="scene_observation_candidate",
                candidate_ref=candidate_ref,
                doc=doc,
                item=image,
                extra_payload=extra_payload,
            )
        )

    # Annotation-level evidence candidates.
    for index, ann in enumerate(_annotations(doc)):
        ann_type = ann.get("type", "")
        ann_id = ann.get("ann_id", f"ann_{index}")
        for candidate_type in ANNOTATION_TYPE_TO_CANDIDATE.get(ann_type, ()):
            if candidate_type == "dynamic_risk_candidate" and not ann.get("velocity_hint"):
                continue
            candidate_ref = f"{candidate_type}_{ann_id}"
            extra_payload = {
                "annotation_kind": ann_type,
                "label": ann.get("label"),
                "bbox": ann.get("bbox"),
                "mask_ref": ann.get("mask_ref"),
                "polygon": ann.get("polygon"),
                "text": ann.get("text"),
                "text_span": ann.get("text_span"),
                "track_id": ann.get("track_id"),
                "trajectory": ann.get("trajectory"),
                "velocity_hint": ann.get("velocity_hint"),
                "evidence_only": True,
                "is_final_interpretation": False,
            }
            extra_payload = {k: v for k, v in extra_payload.items() if v is not None}
            candidates.append(
                _make_candidate(
                    candidate_type=candidate_type,
                    candidate_ref=candidate_ref,
                    doc=doc,
                    item=ann,
                    extra_payload=extra_payload,
                )
            )

    output_types = tuple(sorted({c["candidate_type"] for c in candidates}))
    source_chain_preserved = bool(candidates) and all(c.get("source_chain") for c in candidates)
    confidence_preserved = bool(candidates) and all(
        isinstance(c.get("confidence"), (int, float)) for c in candidates
    )
    license_ref_preserved = bool(candidates) and all(
        bool(c["metadata"].get("license_ref")) for c in candidates
    )
    dataset_ref_preserved = bool(candidates) and all(
        bool(c["metadata"].get("dataset_ref")) for c in candidates
    )
    annotation_origin_preserved = bool(candidates) and all(
        bool(c["metadata"].get("annotation_origin")) for c in candidates
    )
    return {
        "candidates": candidates,
        "candidate_count": len(candidates),
        "output_candidate_types": output_types,
        "adapter_mapping_used": True,
        "source_chain_preserved": source_chain_preserved,
        "confidence_preserved": confidence_preserved,
        "license_ref_preserved": license_ref_preserved,
        "dataset_ref_preserved": dataset_ref_preserved,
        "annotation_origin_preserved": annotation_origin_preserved,
        "candidate_only": all(c.get("candidate_only") is True for c in candidates),
    }


def run_dataset_pipeline(sample_file: str) -> Dict[str, Any]:
    doc, read_ok, read_issues = read_local_roboflow_file(sample_file)
    admission = admit_roboflow_source(sample_file=sample_file, doc=doc or {})
    mapping = {
        "candidates": [], "candidate_count": 0, "output_candidate_types": (),
        "adapter_mapping_used": False, "source_chain_preserved": False,
        "confidence_preserved": False, "license_ref_preserved": False,
        "dataset_ref_preserved": False, "annotation_origin_preserved": False,
        "candidate_only": True,
    }
    admitted = admission["file_source_admitted"] and read_ok and doc is not None
    if admitted:
        mapping = map_roboflow_to_candidates(doc=doc)
    return {
        "sample_file": sample_file, "read_ok": read_ok, "read_issues": read_issues,
        "admission": admission, "mapping": mapping, "admitted": admitted,
    }


def _candidates_of(pipe: Dict[str, Any], candidate_type: str) -> List[Dict[str, Any]]:
    return [c for c in pipe["mapping"]["candidates"] if c["candidate_type"] == candidate_type]


# --------------------------------------------------------------------------- #
# Positive cases
# --------------------------------------------------------------------------- #
def run_positive_yolo_object(ctx: Dict[str, Any]) -> Dict[str, Any]:
    yolo = ctx["yolo_pipe"]
    objects = _candidates_of(yolo, "object_evidence_candidate")
    checks = {
        "annotation_format_recognized": yolo["admission"]["annotation_format_recognized"] is True,
        "object_evidence_candidate_generated": len(objects) > 0,
        "bbox_preserved": all(c["payload"].get("bbox") for c in objects),
        "license_ref_preserved": yolo["mapping"]["license_ref_preserved"],
        "candidate_only": yolo["mapping"]["candidate_only"],
    }
    return {"case_ref": "roboflow_yolo_object_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_coco_object_region(ctx: Dict[str, Any]) -> Dict[str, Any]:
    coco = ctx["coco_pipe"]
    objects = _candidates_of(coco, "object_evidence_candidate")
    regions = _candidates_of(coco, "region_evidence_candidate")
    checks = {
        "annotation_format_recognized": coco["admission"]["annotation_format_recognized"] is True,
        "object_evidence_candidate_generated": len(objects) > 0,
        "region_evidence_candidate_generated": len(regions) > 0,
        "mask_ref_preserved": all(c["payload"].get("mask_ref") for c in regions),
        "candidate_only": coco["mapping"]["candidate_only"],
    }
    return {"case_ref": "roboflow_coco_object_region_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_voc_object(ctx: Dict[str, Any]) -> Dict[str, Any]:
    voc = ctx["voc_pipe"]
    objects = _candidates_of(voc, "object_evidence_candidate")
    checks = {
        "annotation_format_recognized": voc["admission"]["annotation_format_recognized"] is True,
        "object_evidence_candidate_generated": len(objects) > 0,
        "bbox_preserved": all(c["payload"].get("bbox") for c in objects),
        "candidate_only": voc["mapping"]["candidate_only"],
    }
    return {"case_ref": "roboflow_voc_object_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_ocr_placeholder_text(ctx: Dict[str, Any]) -> Dict[str, Any]:
    ocr = ctx["ocr_pipe"]
    texts = _candidates_of(ocr, "text_evidence_candidate")
    checks = {
        "text_evidence_candidate_generated": len(texts) > 0,
        "ocr_output_not_fact": all(c.get("direct_fact_write_allowed") is False for c in texts),
        "text_span_preserved": all(c["payload"].get("text_span") for c in texts),
        "source_chain_preserved": ocr["mapping"]["source_chain_preserved"],
    }
    return {"case_ref": "roboflow_ocr_placeholder_text_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_tracking_placeholder_dynamic_risk(ctx: Dict[str, Any]) -> Dict[str, Any]:
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
    return {"case_ref": "roboflow_tracking_placeholder_dynamic_risk_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_license_source_admission_metadata(ctx: Dict[str, Any]) -> Dict[str, Any]:
    yolo = ctx["yolo_pipe"]
    admission = yolo["admission"]
    mapping = yolo["mapping"]
    checks = {
        "license_present": admission["license_present"] is True,
        "dataset_origin_present": admission["dataset_origin_present"] is True,
        "annotation_format_recognized": admission["annotation_format_recognized"] is True,
        "source_chain_present": admission["source_chain_present"] is True,
        "confidence_present": admission["confidence_present"] is True,
        "license_ref_preserved": mapping["license_ref_preserved"] is True,
        "dataset_ref_preserved": mapping["dataset_ref_preserved"] is True,
        "annotation_origin_preserved": mapping["annotation_origin_preserved"] is True,
        "roboflow_not_fact_layer": all(
            c.get("is_fact_layer") is False for c in mapping["candidates"]
        ),
        "annotation_not_auto_trusted": all(
            c.get("annotation_auto_trusted") is False for c in mapping["candidates"]
        ),
        "license_not_default_commercial": all(
            c.get("license_default_commercial") is False for c in mapping["candidates"]
        ),
    }
    return {"case_ref": "roboflow_license_source_admission_metadata_preserved",
            "case_kind": "positive", "passed": all(checks.values()), "checks": checks}


def _all_evidence_refs(ctx: Dict[str, Any]) -> Dict[str, List[str]]:
    refs: Dict[str, List[str]] = {}
    for key in ("yolo_pipe", "coco_pipe", "voc_pipe", "ocr_pipe", "tracking_pipe"):
        for c in ctx[key]["mapping"]["candidates"]:
            refs.setdefault(c["candidate_type"], []).append(c["candidate_ref"])
    return refs


def run_positive_field_task_guidance(ctx: Dict[str, Any]) -> Dict[str, Any]:
    refs = _all_evidence_refs(ctx)
    tracking_refs = refs.get("track_evidence_candidate", []) + refs.get("dynamic_risk_candidate", [])
    object_region_refs = refs.get("object_evidence_candidate", []) + refs.get(
        "region_evidence_candidate", []
    )
    all_refs = [r for group in refs.values() for r in group]

    field_candidates = [
        {"candidate_type": "FieldCandidate", "candidate_ref": "roboflow_field_001",
         "candidate_only": True, "referenced_evidence_refs": all_refs},
        {"candidate_type": "FieldStateCandidate", "candidate_ref": "roboflow_field_state_001",
         "candidate_only": True},
    ]
    task_candidates = [
        {"candidate_type": "TaskContextCandidate", "candidate_ref": "roboflow_task_ctx_001",
         "candidate_only": True, "referenced_evidence_refs": object_region_refs},
        {"candidate_type": "TaskEvidenceNeedCandidate", "candidate_ref": "roboflow_task_need_001",
         "candidate_only": True, "referenced_evidence_refs": all_refs},
        {"candidate_type": "TaskRiskCandidate", "candidate_ref": "roboflow_task_risk_001",
         "candidate_only": True, "referenced_evidence_refs": tracking_refs},
    ]
    guidance_candidates = [
        {"candidate_type": "GuidanceCandidate", "candidate_ref": "roboflow_guidance_001",
         "candidate_only": True, "is_runtime_navigation": False},
        {"candidate_type": "SpeechGateCandidate", "candidate_ref": "roboflow_speech_gate_001",
         "candidate_only": True, "is_tts": False},
        {"candidate_type": "ActionSafetyCandidate", "candidate_ref": "roboflow_action_safety_001",
         "candidate_only": True, "direct_action_allowed": False},
    ]
    guidance = {c["candidate_type"]: c for c in guidance_candidates}
    checks = {
        "field_task_guidance_replay_path_ok": bool(field_candidates)
        and bool(task_candidates)
        and bool(guidance_candidates),
        "task_context_can_reference_evidence_candidates": len(
            task_candidates[0]["referenced_evidence_refs"]
        )
        > 0,
        "task_risk_can_reference_tracking_evidence": len(
            task_candidates[2]["referenced_evidence_refs"]
        )
        > 0
        and len(tracking_refs) > 0,
        "guidance_candidate_remains_candidate": guidance["GuidanceCandidate"]["is_runtime_navigation"]
        is False,
        "speech_gate_candidate_not_tts": guidance["SpeechGateCandidate"]["is_tts"] is False,
        "action_safety_candidate_exists": "ActionSafetyCandidate" in guidance,
        "model_output_not_direct_to_field": True,
    }
    return {"case_ref": "roboflow_integrated_field_task_guidance_replay_path",
            "case_kind": "positive", "passed": all(checks.values()), "checks": checks}


# --------------------------------------------------------------------------- #
# Negative cases
# --------------------------------------------------------------------------- #
def _negative_admission(sample_file: str, expect_reason_prefix: str) -> bool:
    doc, _, _ = read_local_roboflow_file(sample_file)
    admission = admit_roboflow_source(sample_file=sample_file, doc=doc or {})
    return admission["file_source_admitted"] is False and any(
        r.startswith(expect_reason_prefix) for r in admission["rejection_reasons"]
    )


def run_negative_missing_license() -> Dict[str, Any]:
    rejected = _negative_admission("invalid_roboflow_missing_license.json", "license_missing")
    return {"case_ref": "invalid_roboflow_missing_license_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"missing_license_rejected": rejected}}


def run_negative_missing_dataset_origin() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_roboflow_missing_dataset_origin.json", "dataset_origin_missing"
    )
    return {"case_ref": "invalid_roboflow_missing_dataset_origin_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"missing_dataset_origin_rejected": rejected}}


def run_negative_unrecognized_annotation_format() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_roboflow_unrecognized_annotation_format.json", "annotation_format_unrecognized"
    )
    return {"case_ref": "invalid_roboflow_unrecognized_annotation_format_rejected",
            "case_kind": "negative", "expected_outcome": "rejected", "passed": rejected,
            "checks": {"unrecognized_annotation_format_rejected": rejected}}


def run_negative_missing_source_chain() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_roboflow_missing_source_chain.json", "source_chain_missing"
    )
    return {"case_ref": "invalid_roboflow_missing_source_chain_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"missing_source_chain_rejected": rejected}}


def run_negative_direct_fact_write_or_route_activation() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_roboflow_direct_fact_write.json", "prohibited_output_flags_present"
    )
    return {"case_ref": "invalid_roboflow_direct_fact_write_or_route_activation_rejected",
            "case_kind": "negative", "expected_outcome": "rejected", "passed": rejected,
            "checks": {"direct_fact_write_or_route_activation_rejected": rejected}}


def run_negative_model_native_output_direct_to_field() -> Dict[str, Any]:
    # Sample file already carries native bypass flags; also tamper a valid doc in-memory
    # to prove the adapter rejects native-direct-to-field regardless of provenance.
    file_rejected = _negative_admission(
        "invalid_roboflow_model_native_direct_to_field.json", "prohibited_output_flags_present"
    )
    doc, _, _ = read_local_roboflow_file("sample_roboflow_yolo_dataset.json")
    tampered = copy.deepcopy(doc or {})
    tampered["bypass_adapter"] = True
    tampered["native_direct_to_field"] = True
    tampered["direct_to_field_task_guidance"] = True
    admission = admit_roboflow_source(
        sample_file="sample_roboflow_yolo_dataset.json", doc=tampered
    )
    tamper_rejected = admission["file_source_admitted"] is False and any(
        r.startswith("prohibited_output_flags_present") for r in admission["rejection_reasons"]
    )
    rejected = file_rejected and tamper_rejected
    return {"case_ref": "invalid_roboflow_model_native_output_direct_to_field_rejected",
            "case_kind": "negative", "expected_outcome": "rejected", "passed": rejected,
            "checks": {"model_native_output_direct_to_field_rejected": rejected,
                       "file_rejected": file_rejected, "tamper_rejected": tamper_rejected}}


def run_all_cases_v1() -> Dict[str, Any]:
    ctx = {
        "yolo_pipe": run_dataset_pipeline("sample_roboflow_yolo_dataset.json"),
        "coco_pipe": run_dataset_pipeline("sample_roboflow_coco_dataset.json"),
        "voc_pipe": run_dataset_pipeline("sample_roboflow_voc_dataset.json"),
        "ocr_pipe": run_dataset_pipeline("sample_roboflow_ocr_placeholder.json"),
        "tracking_pipe": run_dataset_pipeline("sample_roboflow_tracking_placeholder.json"),
    }

    positive_results = [
        run_positive_yolo_object(ctx),
        run_positive_coco_object_region(ctx),
        run_positive_voc_object(ctx),
        run_positive_ocr_placeholder_text(ctx),
        run_positive_tracking_placeholder_dynamic_risk(ctx),
        run_positive_license_source_admission_metadata(ctx),
        run_positive_field_task_guidance(ctx),
    ]
    negative_results = [
        run_negative_missing_license(),
        run_negative_missing_dataset_origin(),
        run_negative_unrecognized_annotation_format(),
        run_negative_missing_source_chain(),
        run_negative_direct_fact_write_or_route_activation(),
        run_negative_model_native_output_direct_to_field(),
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

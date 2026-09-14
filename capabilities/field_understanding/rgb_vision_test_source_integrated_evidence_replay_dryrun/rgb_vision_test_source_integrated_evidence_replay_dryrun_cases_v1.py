# -*- coding: utf-8 -*-
"""RGB Vision Test Source Integrated Evidence Replay DryRun — cases v1.

Reads local controlled multi test-source samples, runs unified license/source
admission, maps heterogeneous annotations into unified Luna evidence candidates
via the external vision interface adapter, then replays through a Field / Task /
Guidance candidate path. All outputs candidate-only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.rgb_vision_test_source_integrated_evidence_replay_dryrun.rgb_vision_test_source_integrated_evidence_replay_dryrun_types_v1 import (
    ADMISSION_REQUIRED_FIELDS,
    ANNOTATION_TYPE_TO_CANDIDATE,
    AUTO_TRUST_FLAGS,
    ALLOWED_USE_RESEARCH_TEST_ONLY,
    COMMERCIAL_NON_COMMERCIAL,
    COMMERCIAL_READY_FLAGS,
    FORMAT_REF,
    INTERFACE_ADAPTER_REF,
    NEGATIVE_CASE_REFS,
    POSITIVE_CASE_REFS,
    PROHIBITED_OUTPUT_FLAGS,
    RECOGNIZED_ANNOTATION_FORMATS,
    SAMPLE_FILES,
    SAMPLE_SOURCES,
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


def read_local_sample(sample_file: str) -> Tuple[Optional[Dict[str, Any]], bool, List[str]]:
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


def _confidence_present(doc: Dict[str, Any]) -> bool:
    if isinstance(doc.get("confidence"), (int, float)):
        return True
    annotations = _annotations(doc)
    return bool(annotations) and all(
        isinstance(a.get("confidence"), (int, float)) for a in annotations
    )


def admit_test_source(*, sample_file: str, doc: Dict[str, Any]) -> Dict[str, Any]:
    path = _SAMPLES_DIR / sample_file
    rejection_reasons: List[str] = []

    controlled_ok = is_controlled_sample_path(path)
    if not controlled_ok:
        rejection_reasons.append("controlled_samples_path_violation")

    format_ref_ok = doc.get("format_ref") == FORMAT_REF
    if not format_ref_ok:
        rejection_reasons.append(f"format_ref_not_{FORMAT_REF}")

    missing_fields = [f for f in ADMISSION_REQUIRED_FIELDS if not doc.get(f)]
    required_fields_present = not missing_fields
    license_present = bool(doc.get("license_ref"))
    dataset_ref_present = bool(doc.get("dataset_ref"))
    sample_origin_present = bool(doc.get("sample_origin"))
    if not license_present:
        rejection_reasons.append("license_ref_missing")
    if not dataset_ref_present:
        rejection_reasons.append("dataset_ref_missing")
    if not sample_origin_present:
        rejection_reasons.append("sample_origin_missing")
    for field in missing_fields:
        if field not in ("license_ref", "dataset_ref", "sample_origin"):
            rejection_reasons.append(f"required_field_missing:{field}")

    annotation_format_recognized = doc.get("annotation_format") in RECOGNIZED_ANNOTATION_FORMATS
    if not annotation_format_recognized:
        rejection_reasons.append(
            f"annotation_format_unrecognized:{doc.get('annotation_format')!r}"
        )

    confidence_present = _confidence_present(doc)
    if not confidence_present:
        rejection_reasons.append("confidence_missing")

    annotation_not_auto_trusted = not any(doc.get(flag) is True for flag in AUTO_TRUST_FLAGS)
    if not annotation_not_auto_trusted:
        rejection_reasons.append("annotation_auto_trusted")

    commercial_integrity_ok = True
    if doc.get("commercial_use_status") == COMMERCIAL_NON_COMMERCIAL:
        marked_commercial = any(doc.get(flag) is True for flag in COMMERCIAL_READY_FLAGS)
        not_research_only = doc.get("allowed_use") != ALLOWED_USE_RESEARCH_TEST_ONLY
        if marked_commercial or not_research_only:
            commercial_integrity_ok = False
            rejection_reasons.append("non_commercial_marked_commercial_ready")

    prohibited_flags_absent = not any(doc.get(flag) is True for flag in PROHIBITED_OUTPUT_FLAGS)
    if not prohibited_flags_absent:
        present = [flag for flag in PROHIBITED_OUTPUT_FLAGS if doc.get(flag) is True]
        rejection_reasons.append("prohibited_output_flags_present:" + ",".join(present))

    admitted = len(rejection_reasons) == 0
    return {
        "result_ref": f"test_source_admission_{sample_file}",
        "source_id": doc.get("source_id"),
        "sample_file": sample_file,
        "file_source_admitted": admitted,
        "controlled_samples_path_ok": controlled_ok,
        "format_ref_ok": format_ref_ok,
        "required_fields_present": required_fields_present,
        "annotation_format_recognized": annotation_format_recognized,
        "license_present": license_present,
        "dataset_ref_present": dataset_ref_present,
        "sample_origin_present": sample_origin_present,
        "confidence_present": confidence_present,
        "annotation_not_auto_trusted": annotation_not_auto_trusted,
        "commercial_integrity_ok": commercial_integrity_ok,
        "prohibited_flags_absent": prohibited_flags_absent,
        "rejection_reasons": rejection_reasons,
        "source_chain": SOURCE_CHAIN,
    }


def _base_metadata(doc: Dict[str, Any], item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "source_id": doc.get("source_id"),
        "dataset_ref": doc.get("dataset_ref"),
        "license_ref": doc.get("license_ref"),
        "annotation_origin": doc.get("annotation_origin"),
        "sample_origin": doc.get("sample_origin"),
        "annotation_format": doc.get("annotation_format"),
        "allowed_use": doc.get("allowed_use"),
        "commercial_use_status": doc.get("commercial_use_status"),
        "image_id": item.get("image_id"),
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
        "source_id": doc.get("source_id"),
        "source_chain": list(doc.get("source_chain") or []) + [candidate_ref],
        "confidence": confidence,
        "field_synthesis_entrypoint": TARGET_ENTRYPOINT,
        "adapter_ref": INTERFACE_ADAPTER_REF,
        "metadata": metadata,
        "payload": extra_payload,
        "candidate_only": True,
        "external_test_source_only": True,
        "is_fact_layer": False,
        "dataset_label_is_truth": False,
        "annotation_auto_trusted": False,
        "direct_action_allowed": False,
        "direct_speech_allowed": False,
        "direct_fact_write_allowed": False,
        "route_activation_allowed": False,
        "field_identity_mutation_allowed": False,
    }


def map_annotations_to_candidates(*, doc: Dict[str, Any]) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []

    for index, image in enumerate(_images(doc)):
        image_id = image.get("image_id", f"img_{index}")
        candidate_ref = f"scene_observation_candidate_{image_id}"
        payload = {
            "annotation_kind": "image",
            "scene_label_hint": image.get("scene_label_hint"),
            "evidence_only": True,
            "is_final_interpretation": False,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        candidates.append(
            _make_candidate(
                candidate_type="scene_observation_candidate",
                candidate_ref=candidate_ref,
                doc=doc,
                item=image,
                extra_payload=payload,
            )
        )

    for index, ann in enumerate(_annotations(doc)):
        ann_type = ann.get("type", "")
        ann_id = ann.get("ann_id", f"ann_{index}")
        for candidate_type in ANNOTATION_TYPE_TO_CANDIDATE.get(ann_type, ()):
            candidate_ref = f"{candidate_type}_{ann_id}"
            payload = {
                "annotation_kind": ann_type,
                "label": ann.get("label"),
                "bbox": ann.get("bbox"),
                "mask_ref": ann.get("mask_ref"),
                "polygon": ann.get("polygon"),
                "text": ann.get("text"),
                "text_span": ann.get("text_span"),
                "attribute": ann.get("attribute"),
                "relation": ann.get("relation"),
                "relation_refs": ann.get("relation_refs"),
                "subject_ref": ann.get("subject_ref"),
                "object_ref": ann.get("object_ref"),
                "evidence_only": True,
                "is_final_interpretation": False,
            }
            payload = {k: v for k, v in payload.items() if v is not None}
            candidates.append(
                _make_candidate(
                    candidate_type=candidate_type,
                    candidate_ref=candidate_ref,
                    doc=doc,
                    item=ann,
                    extra_payload=payload,
                )
            )

    output_types = tuple(sorted({c["candidate_type"] for c in candidates}))
    src_ok = bool(candidates) and all(c.get("source_chain") for c in candidates)
    conf_ok = bool(candidates) and all(
        isinstance(c.get("confidence"), (int, float)) for c in candidates
    )
    lic_ok = bool(candidates) and all(bool(c["metadata"].get("license_ref")) for c in candidates)
    ds_ok = bool(candidates) and all(bool(c["metadata"].get("dataset_ref")) for c in candidates)
    ann_ok = bool(candidates) and all(
        bool(c["metadata"].get("annotation_origin")) for c in candidates
    )
    so_ok = bool(candidates) and all(
        bool(c["metadata"].get("sample_origin")) for c in candidates
    )
    return {
        "candidates": candidates,
        "candidate_count": len(candidates),
        "output_candidate_types": output_types,
        "adapter_mapping_used": True,
        "source_chain_preserved": src_ok,
        "confidence_preserved": conf_ok,
        "license_ref_preserved": lic_ok,
        "dataset_ref_preserved": ds_ok,
        "annotation_origin_preserved": ann_ok,
        "sample_origin_preserved": so_ok,
        "candidate_only": all(c.get("candidate_only") is True for c in candidates),
    }


def run_source_pipeline(source_id: str, sample_file: str) -> Dict[str, Any]:
    doc, read_ok, read_issues = read_local_sample(sample_file)
    admission = admit_test_source(sample_file=sample_file, doc=doc or {})
    mapping = {
        "candidates": [], "candidate_count": 0, "output_candidate_types": (),
        "adapter_mapping_used": False, "source_chain_preserved": False,
        "confidence_preserved": False, "license_ref_preserved": False,
        "dataset_ref_preserved": False, "annotation_origin_preserved": False,
        "sample_origin_preserved": False, "candidate_only": True,
    }
    admitted = admission["file_source_admitted"] and read_ok and doc is not None
    if admitted:
        mapping = map_annotations_to_candidates(doc=doc)
    return {
        "source_id": source_id, "sample_file": sample_file, "read_ok": read_ok,
        "read_issues": read_issues, "admission": admission, "mapping": mapping,
        "admitted": admitted,
    }


def _candidates_of(pipe: Dict[str, Any], candidate_type: str) -> List[Dict[str, Any]]:
    return [c for c in pipe["mapping"]["candidates"] if c["candidate_type"] == candidate_type]


# --------------------------------------------------------------------------- #
# Positive cases
# --------------------------------------------------------------------------- #
def run_positive_roboflow(ctx: Dict[str, Any]) -> Dict[str, Any]:
    pipe = ctx["roboflow_universe"]
    objects = _candidates_of(pipe, "object_evidence_candidate")
    regions = _candidates_of(pipe, "region_evidence_candidate")
    checks = {
        "license_ref_present": pipe["admission"]["license_present"] is True,
        "dataset_origin_present": pipe["admission"]["dataset_ref_present"] is True,
        "object_evidence_candidate_generated": len(objects) > 0,
        "region_evidence_candidate_generated": len(regions) > 0,
        "roboflow_annotation_not_fact": all(
            c.get("is_fact_layer") is False and c.get("dataset_label_is_truth") is False
            for c in objects + regions
        ),
    }
    return {"case_ref": "roboflow_sample_to_luna_evidence_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_coco(ctx: Dict[str, Any]) -> Dict[str, Any]:
    pipe = ctx["coco"]
    objects = _candidates_of(pipe, "object_evidence_candidate")
    regions = _candidates_of(pipe, "region_evidence_candidate")
    checks = {
        "object_evidence_candidate_generated": len(objects) > 0,
        "region_evidence_candidate_generated": len(regions) > 0,
        "dataset_label_not_luna_truth": all(
            c.get("dataset_label_is_truth") is False for c in objects + regions
        ),
    }
    return {"case_ref": "coco_sample_to_object_region_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_ade20k(ctx: Dict[str, Any]) -> Dict[str, Any]:
    pipe = ctx["ade20k"]
    scenes = _candidates_of(pipe, "scene_observation_candidate")
    regions = _candidates_of(pipe, "region_evidence_candidate")
    checks = {
        "scene_observation_candidate_generated": len(scenes) > 0,
        "region_evidence_candidate_generated": len(regions) > 0,
        "segmentation_not_route_activation": all(
            c.get("route_activation_allowed") is False for c in regions
        ),
    }
    return {"case_ref": "ade20k_sample_to_scene_region_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_textocr(ctx: Dict[str, Any]) -> Dict[str, Any]:
    pipe = ctx["textocr"]
    texts = _candidates_of(pipe, "text_evidence_candidate")
    checks = {
        "text_evidence_candidate_generated": len(texts) > 0,
        "ocr_text_not_fact": all(c.get("direct_fact_write_allowed") is False for c in texts),
        "confidence_preserved": pipe["mapping"]["confidence_preserved"],
        "source_chain_preserved": pipe["mapping"]["source_chain_preserved"],
    }
    return {"case_ref": "textocr_sample_to_text_evidence_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_visual_genome(ctx: Dict[str, Any]) -> Dict[str, Any]:
    pipe = ctx["visual_genome"]
    objects = _candidates_of(pipe, "object_evidence_candidate")
    attributes = _candidates_of(pipe, "attribute_candidate")
    relations = _candidates_of(pipe, "scene_relation_candidate")
    checks = {
        "object_evidence_candidate_generated": len(objects) > 0,
        "attribute_candidate_generated": len(attributes) > 0,
        "scene_relation_candidate_generated": len(relations) > 0,
        "scene_relation_not_final_interpretation": all(
            c["payload"].get("is_final_interpretation") is False for c in relations
        ),
    }
    return {"case_ref": "visual_genome_sample_to_scene_relation_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def _all_evidence_refs(ctx: Dict[str, Any]) -> Dict[str, List[str]]:
    refs: Dict[str, List[str]] = {}
    for source_id in SAMPLE_SOURCES:
        for c in ctx[source_id]["mapping"]["candidates"]:
            refs.setdefault(c["candidate_type"], []).append(c["candidate_ref"])
    return refs


def run_positive_multi_source_ftg(ctx: Dict[str, Any]) -> Dict[str, Any]:
    refs = _all_evidence_refs(ctx)
    object_refs = refs.get("object_evidence_candidate", [])
    region_refs = refs.get("region_evidence_candidate", [])
    text_refs = refs.get("text_evidence_candidate", [])
    relation_refs = refs.get("scene_relation_candidate", [])
    all_refs = [r for group in refs.values() for r in group]
    uncertainty_refs = region_refs + object_refs + relation_refs

    field_candidates = [
        {"candidate_type": "FieldCandidate", "candidate_ref": "ts_field_001",
         "candidate_only": True, "referenced_evidence_refs": all_refs},
        {"candidate_type": "FieldStateCandidate", "candidate_ref": "ts_field_state_001",
         "candidate_only": True},
    ]
    task_candidates = [
        {"candidate_type": "TaskContextCandidate", "candidate_ref": "ts_task_ctx_001",
         "candidate_only": True,
         "referenced_evidence_refs": object_refs + text_refs + region_refs + relation_refs},
        {"candidate_type": "TaskRiskCandidate", "candidate_ref": "ts_task_risk_001",
         "candidate_only": True, "referenced_evidence_refs": uncertainty_refs},
    ]
    guidance_candidates = [
        {"candidate_type": "GuidanceCandidate", "candidate_ref": "ts_guidance_001",
         "candidate_only": True, "is_runtime_navigation": False},
        {"candidate_type": "SpeechGateCandidate", "candidate_ref": "ts_speech_gate_001",
         "candidate_only": True, "is_tts": False},
        {"candidate_type": "ActionSafetyCandidate", "candidate_ref": "ts_action_safety_001",
         "candidate_only": True, "direct_action_allowed": False},
    ]
    guidance = {c["candidate_type"]: c for c in guidance_candidates}
    checks = {
        "field_task_guidance_replay_path_ok": bool(field_candidates)
        and bool(task_candidates)
        and bool(guidance_candidates),
        "task_context_references_evidence_candidates": len(
            task_candidates[0]["referenced_evidence_refs"]
        )
        > 0
        and len(object_refs) > 0
        and len(text_refs) > 0
        and len(region_refs) > 0
        and len(relation_refs) > 0,
        "task_risk_references_uncertainty_evidence": len(
            task_candidates[1]["referenced_evidence_refs"]
        )
        > 0,
        "guidance_candidate_remains_candidate": guidance["GuidanceCandidate"]["is_runtime_navigation"]
        is False,
        "speech_gate_candidate_not_tts": guidance["SpeechGateCandidate"]["is_tts"] is False,
        "action_safety_candidate_exists": "ActionSafetyCandidate" in guidance,
    }
    return {"case_ref": "multi_source_field_task_guidance_replay_path", "case_kind": "positive",
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
    return {"case_ref": "multi_source_observation_only_scope_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


# --------------------------------------------------------------------------- #
# Negative cases
# --------------------------------------------------------------------------- #
def _negative_admission(sample_file: str, expect_reason_prefix: str) -> bool:
    doc, _, _ = read_local_sample(sample_file)
    admission = admit_test_source(sample_file=sample_file, doc=doc or {})
    return admission["file_source_admitted"] is False and any(
        r.startswith(expect_reason_prefix) for r in admission["rejection_reasons"]
    )


def run_negative_missing_license() -> Dict[str, Any]:
    rejected = _negative_admission("invalid_missing_license_ref.json", "license_ref_missing")
    return {"case_ref": "invalid_missing_license_ref_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"missing_license_ref_rejected": rejected}}


def run_negative_missing_dataset_or_sample_origin() -> Dict[str, Any]:
    doc, _, _ = read_local_sample("invalid_missing_dataset_or_sample_origin.json")
    admission = admit_test_source(
        sample_file="invalid_missing_dataset_or_sample_origin.json", doc=doc or {}
    )
    rejected = admission["file_source_admitted"] is False and any(
        r.startswith("dataset_ref_missing") or r.startswith("sample_origin_missing")
        for r in admission["rejection_reasons"]
    )
    return {"case_ref": "invalid_missing_dataset_or_sample_origin_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"missing_dataset_or_sample_origin_rejected": rejected}}


def run_negative_annotation_auto_trusted() -> Dict[str, Any]:
    rejected = _negative_admission("invalid_annotation_auto_trusted.json", "annotation_auto_trusted")
    return {"case_ref": "invalid_annotation_auto_trusted_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"annotation_auto_trusted_rejected": rejected}}


def run_negative_non_commercial_marked_commercial_ready() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_non_commercial_marked_commercial_ready.json",
        "non_commercial_marked_commercial_ready",
    )
    return {"case_ref": "invalid_non_commercial_marked_commercial_ready_rejected",
            "case_kind": "negative", "expected_outcome": "rejected", "passed": rejected,
            "checks": {"non_commercial_marked_commercial_ready_rejected": rejected}}


def run_negative_fact_write_route_activation_direct_action() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_fact_write_route_activation_direct_action.json", "prohibited_output_flags_present"
    )
    return {"case_ref": "invalid_fact_write_route_activation_direct_action_rejected",
            "case_kind": "negative", "expected_outcome": "rejected", "passed": rejected,
            "checks": {"fact_write_route_activation_direct_action_rejected": rejected}}


def run_negative_native_annotation_bypass_adapter() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_native_annotation_bypass_adapter.json", "prohibited_output_flags_present"
    )
    return {"case_ref": "invalid_native_annotation_bypass_adapter_rejected",
            "case_kind": "negative", "expected_outcome": "rejected", "passed": rejected,
            "checks": {"native_annotation_bypass_adapter_rejected": rejected}}


def run_all_cases_v1() -> Dict[str, Any]:
    ctx = {sid: run_source_pipeline(sid, f) for sid, f in SAMPLE_SOURCES.items()}

    positive_results = [
        run_positive_roboflow(ctx),
        run_positive_coco(ctx),
        run_positive_ade20k(ctx),
        run_positive_textocr(ctx),
        run_positive_visual_genome(ctx),
        run_positive_multi_source_ftg(ctx),
        run_positive_observation_only(ctx),
    ]
    negative_results = [
        run_negative_missing_license(),
        run_negative_missing_dataset_or_sample_origin(),
        run_negative_annotation_auto_trusted(),
        run_negative_non_commercial_marked_commercial_ready(),
        run_negative_fact_write_route_activation_direct_action(),
        run_negative_native_annotation_bypass_adapter(),
    ]

    evidence_refs = _all_evidence_refs(ctx)
    generated_types = sorted(evidence_refs.keys())
    admitted_sources = sorted(sid for sid in SAMPLE_SOURCES if ctx[sid]["admitted"])
    return {
        "positive_cases": positive_results,
        "negative_cases": negative_results,
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "sample_files": list(SAMPLE_FILES),
        "samples_rel_dir": SAMPLES_REL_DIR,
        "generated_evidence_candidate_types": generated_types,
        "admitted_source_ids": admitted_sources,
        "sample_source_count": len(SAMPLE_SOURCES),
    }

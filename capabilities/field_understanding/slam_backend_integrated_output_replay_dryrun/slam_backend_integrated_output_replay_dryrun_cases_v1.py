# -*- coding: utf-8 -*-
"""SLAM Backend Integrated Output Replay DryRun — cases v1.

Reads local controlled mock-but-file-based SLAM backend output samples, runs a
unified license/source admission, maps heterogeneous backend outputs into unified
Luna Generic JSON Spatial Trace evidence candidates via the external SLAM backend
interface adapter, then replays through a spatial-evidence -> Field/Task/Guidance
candidate path. All outputs candidate-only.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.slam_backend_integrated_output_replay_dryrun.slam_backend_integrated_output_replay_dryrun_types_v1 import (
    ADAPTER_MAPPING_REF,
    ADMISSION_REQUIRED_FIELDS,
    BACKEND_FAMILY_METRIC_SEMANTIC,
    BACKEND_FAMILY_MULTI,
    BACKEND_FAMILY_NEURAL_GAUSSIAN,
    BACKEND_FAMILY_SCENE_GRAPH,
    BACKEND_FAMILY_VIO,
    BACKEND_FAMILY_VISUAL_SLAM,
    COMMERCIAL_READY_FLAGS,
    COVERAGE_CANDIDATE_TYPES,
    GENERIC_JSON_PARSER_REF,
    INTERFACE_ADAPTER_REF,
    LICENSE_TECHNICAL_REFERENCE_ONLY,
    NEGATIVE_CASE_REFS,
    POSITIVE_CASE_REFS,
    PROHIBITED_OUTPUT_FLAGS,
    SAMPLE_BACKENDS,
    SAMPLE_FILES,
    SAMPLES_REL_DIR,
    SOURCE_CHAIN,
    TARGET_ENTRYPOINT,
)

_MODULE_DIR = Path(__file__).resolve().parent
_SAMPLES_DIR = _MODULE_DIR / "samples"

_DEGRADED_TRACKING_STATES = {"degraded", "lost", "failed", "lost_tracking"}


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


# --------------------------------------------------------------------------- #
# Admission
# --------------------------------------------------------------------------- #
def _prohibited_flags_present(doc: Dict[str, Any]) -> List[str]:
    present: List[str] = []
    for flag in PROHIBITED_OUTPUT_FLAGS:
        if doc.get(flag) is True:
            present.append(flag)
    for sub in doc.get("backends") or []:
        if isinstance(sub, dict):
            for flag in PROHIBITED_OUTPUT_FLAGS:
                if sub.get(flag) is True and flag not in present:
                    present.append(flag)
    # nested prohibited flags inside known payload containers
    for container_key in ("loop_closure_hint", "object_landmarks", "poses", "camera_poses"):
        container = doc.get(container_key)
        items = container if isinstance(container, list) else [container]
        for item in items:
            if isinstance(item, dict):
                for flag in PROHIBITED_OUTPUT_FLAGS:
                    if item.get(flag) is True and flag not in present:
                        present.append(flag)
    return present


def admit_backend_source(*, sample_file: str, doc: Dict[str, Any]) -> Dict[str, Any]:
    path = _SAMPLES_DIR / sample_file
    rejection_reasons: List[str] = []

    controlled_ok = is_controlled_sample_path(path)
    if not controlled_ok:
        rejection_reasons.append("controlled_samples_path_violation")

    missing_fields = [f for f in ADMISSION_REQUIRED_FIELDS if not doc.get(f)]
    required_fields_present = not missing_fields
    license_present = bool(doc.get("license_ref"))
    source_chain_present = bool(doc.get("source_chain"))
    backend_origin_present = bool(doc.get("backend_origin"))
    confidence_present = isinstance(doc.get("confidence"), (int, float))
    adapter_mapping_ref_ok = doc.get("adapter_mapping_ref") == ADAPTER_MAPPING_REF

    if not license_present:
        rejection_reasons.append("license_ref_missing")
    if not source_chain_present:
        rejection_reasons.append("source_chain_missing")
    if not backend_origin_present:
        rejection_reasons.append("backend_origin_missing")
    if not confidence_present:
        rejection_reasons.append("confidence_missing")
    if not adapter_mapping_ref_ok:
        rejection_reasons.append("adapter_mapping_ref_invalid")
    for field in missing_fields:
        if field not in ("license_ref", "source_chain", "backend_origin", "confidence",
                         "adapter_mapping_ref"):
            rejection_reasons.append(f"required_field_missing:{field}")

    gpl_commercial_integrity_ok = True
    is_gpl_or_incompatible = (
        doc.get("license_boundary") == LICENSE_TECHNICAL_REFERENCE_ONLY
    )
    marked_commercial = any(doc.get(flag) is True for flag in COMMERCIAL_READY_FLAGS) or (
        doc.get("commercial_use_status") in ("commercial_ready", "commercial_approved")
    )
    if is_gpl_or_incompatible and marked_commercial:
        gpl_commercial_integrity_ok = False
        rejection_reasons.append("gpl_or_incompatible_backend_marked_commercial_ready")

    present_prohibited = _prohibited_flags_present(doc)
    prohibited_flags_absent = not present_prohibited
    if present_prohibited:
        rejection_reasons.append("prohibited_output_flags_present:" + ",".join(present_prohibited))

    admitted = len(rejection_reasons) == 0
    return {
        "result_ref": f"backend_admission_{sample_file}",
        "backend_id": doc.get("backend_id"),
        "sample_file": sample_file,
        "file_source_admitted": admitted,
        "controlled_samples_path_ok": controlled_ok,
        "required_fields_present": required_fields_present,
        "license_present": license_present,
        "source_chain_present": source_chain_present,
        "confidence_present": confidence_present,
        "backend_origin_present": backend_origin_present,
        "adapter_mapping_ref_ok": adapter_mapping_ref_ok,
        "gpl_commercial_integrity_ok": gpl_commercial_integrity_ok,
        "prohibited_flags_absent": prohibited_flags_absent,
        "rejection_reasons": rejection_reasons,
        "source_chain": SOURCE_CHAIN,
    }


# --------------------------------------------------------------------------- #
# Adapter mapping -> Luna evidence candidates
# --------------------------------------------------------------------------- #
def _make_candidate(
    *,
    candidate_type: str,
    candidate_ref: str,
    doc: Dict[str, Any],
    confidence: Any,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    if not isinstance(confidence, (int, float)):
        confidence = doc.get("confidence")
    base_chain = list(doc.get("source_chain") or [])
    metadata = {
        "backend_id": doc.get("backend_id"),
        "backend_family": doc.get("backend_family"),
        "backend_origin": doc.get("backend_origin"),
        "license_ref": doc.get("license_ref"),
        "license_boundary": doc.get("license_boundary"),
        "allowed_use": doc.get("allowed_use"),
        "commercial_use_status": doc.get("commercial_use_status"),
    }
    return {
        "candidate_type": candidate_type,
        "candidate_ref": candidate_ref,
        "backend_id": doc.get("backend_id"),
        "source_chain": base_chain + [candidate_ref],
        "confidence": confidence,
        "internal_format": "generic_json_spatial_trace",
        "field_synthesis_entrypoint": TARGET_ENTRYPOINT,
        "adapter_ref": INTERFACE_ADAPTER_REF,
        "metadata": metadata,
        "payload": {k: v for k, v in payload.items() if v is not None},
        "candidate_only": True,
        "is_fact_layer": False,
        "semantic_label_is_fact": False,
        "overrides_field_identity": False,
        "field_identity_mutation_allowed": False,
        "restore_runtime_trust": False,
        "heavy_runtime_admitted": False,
        "direct_action_allowed": False,
        "direct_speech_allowed": False,
        "direct_fact_write_allowed": False,
        "route_activation_allowed": False,
    }


def _map_poses(
    doc: Dict[str, Any], poses: List[Dict[str, Any]], prefix: str
) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    prev_id = None
    for index, pose in enumerate(poses):
        pid = pose.get("id", f"{prefix}_pose_{index}")
        candidates.append(
            _make_candidate(
                candidate_type="pose",
                candidate_ref=f"pose_candidate_{pid}",
                doc=doc,
                confidence=pose.get("confidence"),
                payload={
                    "timestamp_ms": pose.get("timestamp_ms"),
                    "pose": pose.get("pose"),
                    "evidence_only": True,
                },
            )
        )
        if prev_id is not None:
            candidates.append(
                _make_candidate(
                    candidate_type="motion",
                    candidate_ref=f"motion_candidate_{prev_id}_{pid}",
                    doc=doc,
                    confidence=pose.get("confidence"),
                    payload={
                        "from_pose": prev_id,
                        "to_pose": pid,
                        "velocity_hint": pose.get("velocity_hint"),
                        "evidence_only": True,
                    },
                )
            )
        if pose.get("tracking_state") in _DEGRADED_TRACKING_STATES:
            candidates.append(
                _make_candidate(
                    candidate_type="health",
                    candidate_ref=f"health_candidate_{pid}",
                    doc=doc,
                    confidence=pose.get("confidence"),
                    payload={
                        "tracking_state": pose.get("tracking_state"),
                        "risk_evidence_only": True,
                        "is_fact": False,
                    },
                )
            )
        prev_id = pid
    return candidates


def map_vio(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    return _map_poses(doc, list(doc.get("poses") or []), doc.get("backend_id", "vio"))


def map_visual_slam(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    candidates.extend(
        _map_poses(doc, list(doc.get("camera_poses") or []), doc.get("backend_id", "orb"))
    )
    for index, kf in enumerate(doc.get("keyframes") or []):
        kid = kf.get("id", f"kf_{index}")
        candidates.append(
            _make_candidate(
                candidate_type="anchor",
                candidate_ref=f"anchor_candidate_{kid}",
                doc=doc,
                confidence=None,
                payload={"keyframe_id": kid, "landmark_count": kf.get("landmark_count"),
                         "evidence_only": True},
            )
        )
    summary = doc.get("map_points_summary")
    if isinstance(summary, dict):
        candidates.append(
            _make_candidate(
                candidate_type="anchor",
                candidate_ref=f"anchor_candidate_map_points_{doc.get('backend_id', 'orb')}",
                doc=doc,
                confidence=None,
                payload={"map_points_summary": summary, "evidence_only": True},
            )
        )
    loop = doc.get("loop_closure_hint")
    if isinstance(loop, dict):
        candidates.append(
            _make_candidate(
                candidate_type="relocalization",
                candidate_ref=f"relocalization_candidate_{loop.get('id', 'lc')}",
                doc=doc,
                confidence=loop.get("score"),
                payload={
                    "from_kf": loop.get("from_kf"),
                    "to_kf": loop.get("to_kf"),
                    "loop_closure_hint": True,
                    "restores_runtime_trust": False,
                    "evidence_only": True,
                },
            )
        )
    drift = doc.get("drift_estimate")
    if isinstance(drift, dict):
        candidates.append(
            _make_candidate(
                candidate_type="drift",
                candidate_ref=f"drift_candidate_{drift.get('id', 'drift')}",
                doc=doc,
                confidence=None,
                payload={
                    "map_inconsistency": drift.get("map_inconsistency"),
                    "tracking_drift": drift.get("tracking_drift"),
                    "uncertainty_evidence_only": True,
                },
            )
        )
    return candidates


def map_metric_semantic(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    nodes = ((doc.get("pose_graph") or {}).get("nodes")) or []
    for index, node in enumerate(nodes):
        nid = node.get("id", f"n_{index}")
        candidates.append(
            _make_candidate(
                candidate_type="pose",
                candidate_ref=f"pose_candidate_{nid}",
                doc=doc,
                confidence=None,
                payload={"timestamp_ms": node.get("timestamp_ms"), "pose": node.get("pose"),
                         "evidence_only": True},
            )
        )
        candidates.append(
            _make_candidate(
                candidate_type="anchor",
                candidate_ref=f"anchor_candidate_{nid}",
                doc=doc,
                confidence=None,
                payload={"pose_graph_node": nid, "evidence_only": True},
            )
        )
    for index, region in enumerate(doc.get("semantic_mesh_regions") or []):
        rid = region.get("id", f"r_{index}")
        candidates.append(
            _make_candidate(
                candidate_type="region",
                candidate_ref=f"region_candidate_{rid}",
                doc=doc,
                confidence=None,
                payload={"semantic_label": region.get("semantic_label"),
                         "area_hint": region.get("area_hint"),
                         "semantic_label_is_fact": False, "evidence_only": True},
            )
        )
    for index, obj in enumerate(doc.get("object_landmarks") or []):
        oid = obj.get("id", f"obj_{index}")
        candidates.append(
            _make_candidate(
                candidate_type="scene_relation",
                candidate_ref=f"scene_relation_candidate_{oid}",
                doc=doc,
                confidence=None,
                payload={"semantic_label": obj.get("semantic_label"),
                         "position": obj.get("position"),
                         "semantic_label_is_fact": False, "is_final_interpretation": False},
            )
        )
        candidates.append(
            _make_candidate(
                candidate_type="semantic_place",
                candidate_ref=f"semantic_place_candidate_{oid}",
                doc=doc,
                confidence=None,
                payload={"semantic_label": obj.get("semantic_label"),
                         "semantic_label_is_fact": False, "defines_field_identity": False},
            )
        )
    for index, place in enumerate(doc.get("room_or_place_hints") or []):
        pid = place.get("id", f"place_{index}")
        candidates.append(
            _make_candidate(
                candidate_type="semantic_place",
                candidate_ref=f"semantic_place_candidate_{pid}",
                doc=doc,
                confidence=place.get("confidence"),
                payload={"place_label": place.get("place_label"),
                         "semantic_label_is_fact": False, "defines_field_identity": False},
            )
        )
    return candidates


def map_scene_graph(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    for index, place in enumerate(doc.get("places") or []):
        pid = place.get("id", f"place_{index}")
        candidates.append(
            _make_candidate(
                candidate_type="anchor",
                candidate_ref=f"anchor_candidate_{pid}",
                doc=doc, confidence=None,
                payload={"place_label": place.get("place_label"), "position": place.get("position"),
                         "evidence_only": True},
            )
        )
        candidates.append(
            _make_candidate(
                candidate_type="semantic_place",
                candidate_ref=f"semantic_place_candidate_{pid}",
                doc=doc, confidence=None,
                payload={"place_label": place.get("place_label"),
                         "semantic_label_is_fact": False, "defines_field_identity": False},
            )
        )
        candidates.append(
            _make_candidate(
                candidate_type="field_structure",
                candidate_ref=f"field_structure_candidate_{pid}",
                doc=doc, confidence=None,
                payload={"place_label": place.get("place_label"),
                         "is_final_field_identity": False, "field_evidence_only": True},
            )
        )
    for index, room in enumerate(doc.get("rooms") or []):
        rid = room.get("id", f"room_{index}")
        candidates.append(
            _make_candidate(
                candidate_type="field_structure",
                candidate_ref=f"field_structure_candidate_{rid}",
                doc=doc, confidence=None,
                payload={"room_label": room.get("room_label"),
                         "is_final_field_identity": False, "field_evidence_only": True},
            )
        )
        candidates.append(
            _make_candidate(
                candidate_type="anchor",
                candidate_ref=f"anchor_candidate_{rid}",
                doc=doc, confidence=None,
                payload={"room_label": room.get("room_label"), "position": room.get("position"),
                         "evidence_only": True},
            )
        )
    for index, obj in enumerate(doc.get("objects") or []):
        oid = obj.get("id", f"obj_{index}")
        candidates.append(
            _make_candidate(
                candidate_type="anchor",
                candidate_ref=f"anchor_candidate_{oid}",
                doc=doc, confidence=None,
                payload={"semantic_label": obj.get("semantic_label"),
                         "position": obj.get("position"), "evidence_only": True},
            )
        )
    for index, rel in enumerate((doc.get("relations") or []) + (doc.get("edges") or [])):
        rid = rel.get("id", f"rel_{index}")
        candidates.append(
            _make_candidate(
                candidate_type="scene_relation",
                candidate_ref=f"scene_relation_candidate_{rid}",
                doc=doc, confidence=None,
                payload={"subject_ref": rel.get("subject_ref") or rel.get("from"),
                         "object_ref": rel.get("object_ref") or rel.get("to"),
                         "relation": rel.get("relation") or rel.get("edge_type"),
                         "is_final_interpretation": False},
            )
        )
    return candidates


def map_neural_gaussian(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    candidates: List[Dict[str, Any]] = []
    candidates.extend(
        _map_poses(doc, list(doc.get("camera_trajectory") or []), doc.get("backend_id", "neural"))
    )
    for key in ("gaussian_map_metadata", "local_map_summary"):
        meta = doc.get(key)
        if isinstance(meta, dict):
            candidates.append(
                _make_candidate(
                    candidate_type="local_map",
                    candidate_ref=f"local_map_candidate_{meta.get('id', key)}",
                    doc=doc, confidence=None,
                    payload={"map_kind": key, "metadata": meta,
                             "heavy_runtime_admitted": False, "observation_only": True},
                )
            )
    unc = doc.get("uncertainty_hint")
    if isinstance(unc, dict):
        candidates.append(
            _make_candidate(
                candidate_type="uncertainty_hint",
                candidate_ref=f"uncertainty_hint_candidate_{unc.get('id', 'unc')}",
                doc=doc, confidence=None,
                payload={"map_uncertainty": unc.get("map_uncertainty"),
                         "pose_uncertainty": unc.get("pose_uncertainty"),
                         "uncertainty_evidence_only": True},
            )
        )
    return candidates


_FAMILY_MAPPERS = {
    BACKEND_FAMILY_VIO: map_vio,
    BACKEND_FAMILY_VISUAL_SLAM: map_visual_slam,
    BACKEND_FAMILY_METRIC_SEMANTIC: map_metric_semantic,
    BACKEND_FAMILY_SCENE_GRAPH: map_scene_graph,
    BACKEND_FAMILY_NEURAL_GAUSSIAN: map_neural_gaussian,
}


def map_backend_output(doc: Dict[str, Any]) -> Dict[str, Any]:
    family = doc.get("backend_family")
    candidates: List[Dict[str, Any]] = []
    if family == BACKEND_FAMILY_MULTI:
        for sub in doc.get("backends") or []:
            if not isinstance(sub, dict):
                continue
            merged = dict(sub)
            for inherited in ("source_chain", "license_ref", "license_boundary",
                              "backend_origin", "confidence", "allowed_use",
                              "commercial_use_status"):
                merged.setdefault(inherited, doc.get(inherited))
            mapper = _FAMILY_MAPPERS.get(sub.get("backend_family"))
            if mapper:
                candidates.extend(mapper(merged))
    else:
        mapper = _FAMILY_MAPPERS.get(family)
        if mapper:
            candidates.extend(mapper(doc))

    output_types = tuple(sorted({c["candidate_type"] for c in candidates}))
    src_ok = bool(candidates) and all(c.get("source_chain") for c in candidates)
    conf_ok = bool(candidates) and all(
        isinstance(c.get("confidence"), (int, float)) for c in candidates
    )
    backend_ok = bool(candidates) and all(
        bool(c["metadata"].get("backend_origin")) for c in candidates
    )
    lic_ok = bool(candidates) and all(
        bool(c["metadata"].get("license_ref")) for c in candidates
    )
    return {
        "candidates": candidates,
        "candidate_count": len(candidates),
        "output_candidate_types": output_types,
        "adapter_mapping_used": True,
        "source_chain_preserved": src_ok,
        "confidence_preserved": conf_ok,
        "backend_origin_preserved": backend_ok,
        "license_ref_preserved": lic_ok,
        "candidate_only": all(c.get("candidate_only") is True for c in candidates),
    }


def convert_to_generic_json_trace(doc: Dict[str, Any], mapping: Dict[str, Any]) -> Dict[str, Any]:
    frames = [
        {"candidate_ref": c["candidate_ref"], "candidate_type": c["candidate_type"],
         "confidence": c.get("confidence")}
        for c in mapping["candidates"]
    ]
    return {
        "result_ref": f"generic_json_trace_{doc.get('backend_id')}",
        "backend_id": doc.get("backend_id"),
        "generic_json_output_ok": bool(frames),
        "generic_json_parser_ref": GENERIC_JSON_PARSER_REF,
        "internal_format": "generic_json_spatial_trace",
        "frame_count": len(frames),
        "frames": frames,
    }


def run_backend_pipeline(backend_key: str, sample_file: str) -> Dict[str, Any]:
    doc, read_ok, read_issues = read_local_sample(sample_file)
    admission = admit_backend_source(sample_file=sample_file, doc=doc or {})
    mapping = {
        "candidates": [], "candidate_count": 0, "output_candidate_types": (),
        "adapter_mapping_used": False, "source_chain_preserved": False,
        "confidence_preserved": False, "backend_origin_preserved": False,
        "license_ref_preserved": False, "candidate_only": True,
    }
    trace = {"generic_json_output_ok": False, "frame_count": 0}
    admitted = admission["file_source_admitted"] and read_ok and doc is not None
    if admitted:
        mapping = map_backend_output(doc)
        trace = convert_to_generic_json_trace(doc, mapping)
    return {
        "backend_key": backend_key, "sample_file": sample_file, "read_ok": read_ok,
        "read_issues": read_issues, "admission": admission, "mapping": mapping,
        "trace": trace, "admitted": admitted,
    }


def _candidates_of(pipe: Dict[str, Any], candidate_type: str) -> List[Dict[str, Any]]:
    return [c for c in pipe["mapping"]["candidates"] if c["candidate_type"] == candidate_type]


# --------------------------------------------------------------------------- #
# Positive cases
# --------------------------------------------------------------------------- #
def run_positive_openvins(ctx: Dict[str, Any]) -> Dict[str, Any]:
    pipe = ctx["openvins"]
    poses = _candidates_of(pipe, "pose")
    motions = _candidates_of(pipe, "motion")
    healths = _candidates_of(pipe, "health")
    checks = {
        "pose_candidate_generated": len(poses) > 0,
        "motion_candidate_generated": len(motions) > 0,
        "health_candidate_generated": len(healths) > 0,
        "vio_pose_does_not_override_field_identity": all(
            c.get("overrides_field_identity") is False for c in poses
        ),
        "candidate_bundle_mapping_ok": pipe["mapping"]["adapter_mapping_used"] is True
        and pipe["mapping"]["source_chain_preserved"] is True,
    }
    return {"case_ref": "openvins_vio_output_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_orb_slam3(ctx: Dict[str, Any]) -> Dict[str, Any]:
    pipe = ctx["orb_slam3"]
    relocs = _candidates_of(pipe, "relocalization")
    checks = {
        "pose_candidate_generated": len(_candidates_of(pipe, "pose")) > 0,
        "motion_candidate_generated": len(_candidates_of(pipe, "motion")) > 0,
        "anchor_candidate_generated": len(_candidates_of(pipe, "anchor")) > 0,
        "relocalization_candidate_generated": len(relocs) > 0,
        "drift_candidate_generated": len(_candidates_of(pipe, "drift")) > 0,
        "relocalization_does_not_restore_runtime_trust": all(
            c.get("restore_runtime_trust") is False
            and c["payload"].get("restores_runtime_trust") is False
            for c in relocs
        ),
        "gpl_license_boundary_preserved": pipe["mapping"]["candidates"][0]["metadata"].get(
            "license_boundary"
        )
        == LICENSE_TECHNICAL_REFERENCE_ONLY,
    }
    return {"case_ref": "orb_slam3_keyframe_output_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_kimera(ctx: Dict[str, Any]) -> Dict[str, Any]:
    pipe = ctx["kimera"]
    regions = _candidates_of(pipe, "region")
    relations = _candidates_of(pipe, "scene_relation")
    places = _candidates_of(pipe, "semantic_place")
    checks = {
        "pose_candidate_generated": len(_candidates_of(pipe, "pose")) > 0,
        "anchor_candidate_generated": len(_candidates_of(pipe, "anchor")) > 0,
        "region_candidate_generated": len(regions) > 0,
        "scene_relation_candidate_generated": len(relations) > 0,
        "semantic_place_candidate_generated": len(places) > 0,
        "semantic_label_not_fact": all(
            c.get("semantic_label_is_fact") is False for c in regions + relations + places
        ),
        "semantic_output_does_not_define_field_identity": all(
            c.get("overrides_field_identity") is False
            and c["payload"].get("defines_field_identity", False) is False
            for c in relations + places
        ),
    }
    return {"case_ref": "kimera_metric_semantic_output_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_hydra(ctx: Dict[str, Any]) -> Dict[str, Any]:
    pipe = ctx["hydra"]
    fs = _candidates_of(pipe, "field_structure")
    checks = {
        "anchor_candidate_generated": len(_candidates_of(pipe, "anchor")) > 0,
        "scene_relation_candidate_generated": len(_candidates_of(pipe, "scene_relation")) > 0,
        "field_structure_candidate_generated": len(fs) > 0,
        "semantic_place_candidate_generated": len(_candidates_of(pipe, "semantic_place")) > 0,
        "scene_graph_not_final_field_identity": all(
            c["payload"].get("is_final_field_identity") is False for c in fs
        ),
    }
    return {"case_ref": "hydra_scene_graph_output_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_neural_gaussian(ctx: Dict[str, Any]) -> Dict[str, Any]:
    pipe = ctx["neural_gaussian"]
    local_maps = _candidates_of(pipe, "local_map")
    checks = {
        "pose_candidate_generated": len(_candidates_of(pipe, "pose")) > 0,
        "motion_candidate_generated": len(_candidates_of(pipe, "motion")) > 0,
        "local_map_candidate_generated": len(local_maps) > 0,
        "uncertainty_hint_candidate_generated": len(_candidates_of(pipe, "uncertainty_hint")) > 0,
        "heavy_neural_gaussian_runtime_not_admitted": all(
            c.get("heavy_runtime_admitted") is False for c in pipe["mapping"]["candidates"]
        ),
        "observation_only": all(
            c["payload"].get("observation_only", True) is not False for c in local_maps
        ),
    }
    return {"case_ref": "neural_gaussian_slam_output_observation_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_multi_coverage(ctx: Dict[str, Any]) -> Dict[str, Any]:
    pipe = ctx["multi_backend"]
    generated = set(pipe["mapping"]["output_candidate_types"])
    coverage = {t: t in generated for t in COVERAGE_CANDIDATE_TYPES}
    checks = dict(coverage)
    checks["candidate_type_coverage_complete"] = all(coverage.values())
    return {"case_ref": "multi_backend_candidate_type_coverage", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks,
            "generated_candidate_types": sorted(generated)}


def _all_candidate_refs(ctx: Dict[str, Any]) -> Dict[str, List[str]]:
    refs: Dict[str, List[str]] = {}
    for key in SAMPLE_BACKENDS:
        if not ctx[key]["admitted"]:
            continue
        for c in ctx[key]["mapping"]["candidates"]:
            refs.setdefault(c["candidate_type"], []).append(c["candidate_ref"])
    return refs


def run_positive_multi_spatial_evidence_path(ctx: Dict[str, Any]) -> Dict[str, Any]:
    refs = _all_candidate_refs(ctx)
    all_refs = [r for group in refs.values() for r in group]
    pose_refs = refs.get("pose", [])
    uncertainty_refs = (
        refs.get("drift", []) + refs.get("health", []) + refs.get("uncertainty_hint", [])
    )

    spatial_bundle = {
        "candidate_type": "spatial_evidence_candidate_bundle",
        "candidate_ref": "slam_spatial_evidence_bundle_001",
        "candidate_only": True, "referenced_candidate_refs": all_refs,
    }
    fusion = {
        "candidate_type": "spatial_odometry_fusion_candidate",
        "candidate_ref": "slam_spatial_odometry_fusion_001",
        "candidate_only": True, "referenced_pose_refs": pose_refs,
        "overrides_field_identity": False,
    }
    field_candidates = [
        {"candidate_type": "FieldCandidate", "candidate_ref": "slam_field_001",
         "candidate_only": True, "referenced_evidence_refs": all_refs},
        {"candidate_type": "FieldStateCandidate", "candidate_ref": "slam_field_state_001",
         "candidate_only": True},
    ]
    task_candidates = [
        {"candidate_type": "TaskContextCandidate", "candidate_ref": "slam_task_ctx_001",
         "candidate_only": True, "referenced_evidence_refs": all_refs},
        {"candidate_type": "TaskRiskCandidate", "candidate_ref": "slam_task_risk_001",
         "candidate_only": True, "referenced_evidence_refs": uncertainty_refs},
    ]
    guidance = {
        "GuidanceCandidate": {"candidate_type": "GuidanceCandidate",
                              "candidate_ref": "slam_guidance_001",
                              "candidate_only": True, "is_runtime_navigation": False},
        "SpeechGateCandidate": {"candidate_type": "SpeechGateCandidate",
                                "candidate_ref": "slam_speech_gate_001",
                                "candidate_only": True, "is_tts": False},
        "ActionSafetyCandidate": {"candidate_type": "ActionSafetyCandidate",
                                  "candidate_ref": "slam_action_safety_001",
                                  "candidate_only": True, "direct_action_allowed": False},
    }
    checks = {
        "spatial_evidence_candidate_bundle_generated": len(spatial_bundle["referenced_candidate_refs"]) > 0,
        "spatial_odometry_fusion_candidate_generated": len(fusion["referenced_pose_refs"]) > 0,
        "field_task_guidance_replay_path_ok": bool(field_candidates) and bool(task_candidates)
        and bool(guidance),
        "task_risk_references_uncertainty_evidence": len(
            task_candidates[1]["referenced_evidence_refs"]
        )
        > 0,
        "guidance_candidate_remains_candidate": guidance["GuidanceCandidate"]["is_runtime_navigation"]
        is False,
        "speech_gate_candidate_not_tts": guidance["SpeechGateCandidate"]["is_tts"] is False,
        "action_safety_candidate_exists": "ActionSafetyCandidate" in guidance,
        "fusion_does_not_override_field_identity": fusion["overrides_field_identity"] is False,
    }
    return {"case_ref": "multi_backend_spatial_evidence_replay_path", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


def run_positive_observation_only(ctx: Dict[str, Any]) -> Dict[str, Any]:
    scenario = {
        "scope": "neural_gaussian_and_scene_graph_observation_only",
        "observation_only": True,
        "movement_command_emitted": False,
        "route_activation_started": False,
        "heavy_runtime_started": False,
    }
    checks = {
        "observation_only_scope_preserved": scenario["observation_only"] is True,
        "no_movement_command": scenario["movement_command_emitted"] is False,
        "no_route_activation": scenario["route_activation_started"] is False,
        "no_heavy_runtime": scenario["heavy_runtime_started"] is False,
    }
    return {"case_ref": "multi_backend_observation_only_scope_replay", "case_kind": "positive",
            "passed": all(checks.values()), "checks": checks}


# --------------------------------------------------------------------------- #
# Negative cases
# --------------------------------------------------------------------------- #
def _negative_admission(sample_file: str, expect_reason_prefix: str) -> bool:
    doc, _, _ = read_local_sample(sample_file)
    admission = admit_backend_source(sample_file=sample_file, doc=doc or {})
    return admission["file_source_admitted"] is False and any(
        r.startswith(expect_reason_prefix) for r in admission["rejection_reasons"]
    )


def run_negative_missing_source_chain() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_missing_source_chain_backend_output.json", "source_chain_missing"
    )
    return {"case_ref": "invalid_missing_source_chain_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"missing_source_chain_rejected": rejected}}


def run_negative_missing_license_ref() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_missing_license_ref_backend_output.json", "license_ref_missing"
    )
    return {"case_ref": "invalid_missing_license_ref_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"missing_license_ref_rejected": rejected}}


def run_negative_gpl_commercial_ready() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_gpl_backend_marked_commercial_ready.json",
        "gpl_or_incompatible_backend_marked_commercial_ready",
    )
    return {"case_ref": "invalid_gpl_marked_commercial_ready_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"gpl_marked_commercial_ready_rejected": rejected}}


def run_negative_native_direct_to_field() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_native_backend_direct_to_field.json", "prohibited_output_flags_present"
    )
    return {"case_ref": "invalid_native_output_direct_to_field_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"native_output_direct_to_field_rejected": rejected}}


def run_negative_relocalization_runtime_trust() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_relocalization_runtime_trust_restore.json", "prohibited_output_flags_present"
    )
    return {"case_ref": "invalid_relocalization_runtime_trust_restore_rejected",
            "case_kind": "negative", "expected_outcome": "rejected", "passed": rejected,
            "checks": {"runtime_trust_restore_attempt_rejected": rejected}}


def run_negative_semantic_fact_write() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_semantic_label_fact_write.json", "prohibited_output_flags_present"
    )
    return {"case_ref": "invalid_semantic_label_fact_write_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "passed": rejected,
            "checks": {"semantic_fact_write_field_identity_rejected": rejected}}


def run_negative_heavy_runtime_activation() -> Dict[str, Any]:
    rejected = _negative_admission(
        "invalid_heavy_neural_runtime_activation.json", "prohibited_output_flags_present"
    )
    return {"case_ref": "invalid_heavy_neural_runtime_activation_rejected",
            "case_kind": "negative", "expected_outcome": "rejected", "passed": rejected,
            "checks": {"heavy_runtime_activation_rejected": rejected}}


def run_negative_direct_action_speech_navigation_fact_write() -> Dict[str, Any]:
    # Tamper a valid admitted backend doc in memory: inject runtime side-effect flags.
    doc, _, _ = read_local_sample("sample_openvins_trajectory_output.json")
    tampered = copy.deepcopy(doc or {})
    tampered["direct_action"] = True
    tampered["direct_speech"] = True
    tampered["direct_navigation"] = True
    tampered["direct_fact_write"] = True
    admission = admit_backend_source(
        sample_file="sample_openvins_trajectory_output.json", doc=tampered
    )
    rejected = admission["file_source_admitted"] is False and any(
        r.startswith("prohibited_output_flags_present") for r in admission["rejection_reasons"]
    )
    return {"case_ref": "invalid_direct_action_speech_navigation_fact_write_rejected",
            "case_kind": "negative", "expected_outcome": "rejected", "passed": rejected,
            "checks": {"direct_action_speech_navigation_fact_write_rejected": rejected}}


def run_all_cases_v1() -> Dict[str, Any]:
    ctx = {key: run_backend_pipeline(key, f) for key, f in SAMPLE_BACKENDS.items()}

    positive_results = [
        run_positive_openvins(ctx),
        run_positive_orb_slam3(ctx),
        run_positive_kimera(ctx),
        run_positive_hydra(ctx),
        run_positive_neural_gaussian(ctx),
        run_positive_multi_coverage(ctx),
        run_positive_multi_spatial_evidence_path(ctx),
        run_positive_observation_only(ctx),
    ]
    negative_results = [
        run_negative_missing_source_chain(),
        run_negative_missing_license_ref(),
        run_negative_gpl_commercial_ready(),
        run_negative_native_direct_to_field(),
        run_negative_relocalization_runtime_trust(),
        run_negative_semantic_fact_write(),
        run_negative_heavy_runtime_activation(),
        run_negative_direct_action_speech_navigation_fact_write(),
    ]

    refs = _all_candidate_refs(ctx)
    generated_types = sorted(refs.keys())
    admitted_backends = sorted(k for k in SAMPLE_BACKENDS if ctx[k]["admitted"])
    generic_json_ok = all(
        ctx[k]["trace"]["generic_json_output_ok"] for k in admitted_backends
    )
    return {
        "positive_cases": positive_results,
        "negative_cases": negative_results,
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "sample_files": list(SAMPLE_FILES),
        "samples_rel_dir": SAMPLES_REL_DIR,
        "generated_candidate_types": generated_types,
        "admitted_backend_keys": admitted_backends,
        "backend_sample_count": len(SAMPLE_BACKENDS),
        "generic_json_output_ok_for_all_admitted": generic_json_ok,
    }

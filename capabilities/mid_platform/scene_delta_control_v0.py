from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Optional, Tuple


def _sha_short(s: str, n: int = 16) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:n]


def _as_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return float(default)


def _as_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return int(default)


def build_scene_delta_input_v0(
    *,
    delta_input_id: str,
    input_type: str,
    source_evidence_id: str,
    frame_id: str,
    timestamp_ms: int,
    source_frame_window_id: str,
    observed_at: Dict[str, Any],
    observed_where: Dict[str, Any],
    source_attribution: Dict[str, Any],
    content_signature: Dict[str, Any],
    content_payload_ref: str,
    confidence: Dict[str, Any],
    spatiotemporal_delta_anchor_ref: Optional[str] = None,
    candidate_only: bool = True,
    allows_execute_now: bool = False,
) -> Dict[str, Any]:
    return {
        "delta_input_id": delta_input_id,
        "input_type": input_type,
        "source_evidence_id": source_evidence_id,
        "frame_id": frame_id,
        "timestamp_ms": int(timestamp_ms),
        "source_frame_window_id": source_frame_window_id,
        "spatiotemporal_anchor": {"observed_at": observed_at, "observed_where": observed_where},
        "spatiotemporal_delta_anchor_ref": spatiotemporal_delta_anchor_ref,
        "source_attribution": source_attribution,
        "content_signature": content_signature,
        "content_payload_ref": content_payload_ref,
        "confidence": confidence,
        "candidate_only": bool(candidate_only),
        "allows_execute_now": bool(allows_execute_now),
    }


def build_spatiotemporal_delta_anchor_v0(
    *,
    spatiotemporal_anchor_id: str,
    anchor_type: str,
    observed_at: Dict[str, Any],
    observed_where: Dict[str, Any],
    region_bbox: Optional[List[float]] = None,
    visual_landmark_ref: Optional[str] = None,
    carrier_signature_hint: Optional[str] = None,
    content_signature_hint: Optional[str] = None,
) -> Dict[str, Any]:
    place_hint = str((observed_where or {}).get("place_hint") or "unknown")
    geo = (observed_where or {}).get("geo_location") or {}
    lat = geo.get("lat")
    lng = geo.get("lng")
    bbox = region_bbox or [0.0, 0.0, 1.0, 1.0]
    spatial_signature = _sha_short(f"{place_hint}:{lat}:{lng}:{bbox}:{visual_landmark_ref}")
    carrier_signature = _sha_short(f"carrier:{anchor_type}:{carrier_signature_hint or visual_landmark_ref or 'unknown'}")
    layout_signature = _sha_short(f"layout:{anchor_type}:{bbox}")
    content_signature = _sha_short(f"content:{content_signature_hint or 'unknown'}")

    ts = _as_int((observed_at or {}).get("timestamp_ms"), 0)
    return {
        "spatiotemporal_anchor_id": spatiotemporal_anchor_id,
        "anchor_type": anchor_type,
        "spatial_scope": {
            "geo_location": geo if isinstance(geo, dict) else {"lat": None, "lng": None, "accuracy_m": None},
            "place_hint": place_hint,
            "visual_landmark_ref": visual_landmark_ref,
            "relative_position": (observed_where or {}).get("relative_position")
            if isinstance((observed_where or {}).get("relative_position"), dict)
            else {"direction_hint": None, "distance_estimate_m": None},
            "region_bbox": bbox,
            "spatial_confidence": 0.0,
        },
        "temporal_scope": {
            "first_seen_at": ts,
            "last_seen_at": ts,
            "observation_window_id": None,
            "seen_count": 1,
        },
        "anchor_signature": {
            "spatial_signature": spatial_signature,
            "carrier_signature": carrier_signature,
            "layout_signature": layout_signature,
            "content_signature": content_signature,
        },
        "stability_profile": {
            "position_stability": "unknown",
            "content_stability": "unknown",
            "expected_update_frequency": "unknown",
        },
    }


def build_scene_processed_state_v0(
    *,
    state_id: str,
    state_scope: str,
    source_evidence_refs: List[str],
    last_processed_at: int,
    last_seen_at: int,
    seen_count: int,
    signatures: Dict[str, Any],
    last_delta_decision: str,
    last_output_refs: Dict[str, Any],
    ttl_policy: str,
    expires_at: Optional[int],
    requires_revalidation: bool = True,
    spatiotemporal_delta_anchor_ref: Optional[str] = None,
    compression_record_ref: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "state_id": state_id,
        "state_scope": state_scope,
        "source_evidence_refs": source_evidence_refs,
        "last_processed_at": int(last_processed_at),
        "last_seen_at": int(last_seen_at),
        "seen_count": int(seen_count),
        "spatiotemporal_delta_anchor_ref": spatiotemporal_delta_anchor_ref,
        "compression_record_ref": compression_record_ref,
        "signatures": signatures,
        "last_delta_decision": last_delta_decision,
        "last_output_refs": last_output_refs,
        "ttl_policy": ttl_policy,
        "expires_at": expires_at,
        "requires_revalidation": bool(requires_revalidation),
    }


def match_previous_scene_state_v0(
    *,
    delta_input: Dict[str, Any],
    previous_state: Optional[Dict[str, Any]],
) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    if not isinstance(previous_state, dict):
        return None, None
    # Simplest v0: if anchor refs match, treat as matched. Otherwise no match.
    cur_anchor = delta_input.get("spatiotemporal_delta_anchor_ref")
    prev_anchor = previous_state.get("spatiotemporal_delta_anchor_ref")
    if cur_anchor and prev_anchor and str(cur_anchor) == str(prev_anchor):
        return str(previous_state.get("state_id") or "unknown_state"), previous_state
    return None, None


def compare_scene_signatures_v0(
    *,
    delta_input: Dict[str, Any],
    previous_state: Optional[Dict[str, Any]],
    spatial_shift_threshold: float = 0.10,
) -> Dict[str, Any]:
    cur_sig = delta_input.get("content_signature") or {}
    prev_sig = (previous_state or {}).get("signatures") or {}

    # content can be explicitly marked missing (e.g., poster board now blank)
    cur_marked_missing = bool(cur_sig.get("marked_missing") or False)
    cur_content = None if cur_marked_missing else (cur_sig.get("text_signature") or cur_sig.get("content_signature"))
    prev_content = prev_sig.get("text_signature") or prev_sig.get("content_signature")

    cur_spatial = cur_sig.get("crop_signature") or cur_sig.get("spatial_signature")
    prev_spatial = prev_sig.get("crop_signature") or prev_sig.get("spatial_signature")

    content_same = (cur_content is not None and prev_content is not None and str(cur_content) == str(prev_content))
    spatial_same = (cur_spatial is not None and prev_spatial is not None and str(cur_spatial) == str(prev_spatial))

    # v0: no real bbox math; spatial_shift_ratio is placeholder 0.0 when same, else 1.0
    spatial_shift_ratio = 0.0 if spatial_same else 1.0

    if content_same and spatial_shift_ratio <= spatial_shift_threshold:
        result = "exact_match"
    elif content_same:
        result = "near_match"
    else:
        result = "changed"

    return {
        "comparison_result": result,
        "content_same": bool(content_same),
        "spatial_same": bool(spatial_same),
        "spatial_shift_ratio": float(spatial_shift_ratio),
        "which_signature_changed": {
            "content_signature_changed": not content_same,
            "spatial_signature_changed": not spatial_same,
        },
        "previous_content_ref": prev_content,
        "current_content_ref": cur_content,
        "current_marked_missing": bool(cur_marked_missing),
    }


def build_repeated_evidence_compression_v0(
    *,
    compression_record_id: str,
    anchor_ref: str,
    canonical_evidence_ref: str,
    duplicate_evidence_refs: List[str],
    first_seen_at: int,
    last_seen_at: int,
    content_signature: Optional[str],
    spatial_signature: Optional[str],
    compression_method: str = "canonical_ref",
) -> Dict[str, Any]:
    return {
        "compression_record_id": compression_record_id,
        "compression_scope": "individual_local",
        "anchor_ref": anchor_ref,
        "canonical_evidence_ref": canonical_evidence_ref,
        "duplicate_evidence_refs": duplicate_evidence_refs,
        "duplicate_count": int(len(duplicate_evidence_refs)),
        "first_seen_at": int(first_seen_at),
        "last_seen_at": int(last_seen_at),
        "content_signature": content_signature,
        "spatial_signature": spatial_signature,
        "compression_method": compression_method,
        "storage_policy": {
            "retain_full_first_observation": True,
            "retain_full_last_observation": True,
            "retain_delta_only_for_duplicates": True,
            "retain_sample_frames": "first_last_or_periodic",
            "raw_evidence_cold_storage": True,
        },
        "usage": {
            "reuse_previous_result": True,
            "skip_reprocessing": True,
            "available_for_world_change_analysis": True,
        },
        # Explicit boundary flags (skeleton audit)
        "hive_upload_invoked": False,
        "world_model_write_invoked": False,
    }


def decide_scene_delta_v0(
    *,
    delta_input: Dict[str, Any],
    previous_state: Optional[Dict[str, Any]],
    comparison: Dict[str, Any],
    task_context_changed: bool = False,
    low_confidence: bool = False,
    is_duplicate_in_window: bool = False,
) -> Dict[str, Any]:
    # Hard blockers (definition-only guardrails)
    hard_blocker: Optional[str] = None

    sta = (delta_input.get("spatiotemporal_anchor") or {})
    observed_at = (sta.get("observed_at") if isinstance(sta, dict) else None) or {}
    observed_where = (sta.get("observed_where") if isinstance(sta, dict) else None) or {}
    anchor_ref = delta_input.get("spatiotemporal_delta_anchor_ref")

    # missing anchor inputs: either anchor_ref missing or observed_at/where missing timestamp/spatial_anchor_type
    if not anchor_ref or "timestamp_ms" not in observed_at or "spatial_anchor_type" not in observed_where:
        hard_blocker = "missing_spatiotemporal_anchor"

    cur_sig = delta_input.get("content_signature") or {}
    cur_marked_missing = bool(cur_sig.get("marked_missing") or False) if isinstance(cur_sig, dict) else False
    # missing signature inputs is a hard blocker UNLESS this is an explicit "content removed" observation
    sig_present = isinstance(cur_sig, dict) and any(cur_sig.get(k) is not None for k in ("text_signature", "object_signature", "crop_signature", "content_signature", "spatial_signature"))
    if not sig_present and not cur_marked_missing:
        hard_blocker = hard_blocker or "missing_signature_inputs"

    now = _as_int(delta_input.get("timestamp_ms"), 0)
    expires_at = _as_int((previous_state or {}).get("expires_at"), 0) if previous_state else 0
    ttl_expired = bool(previous_state and expires_at and now > expires_at)

    delta_status = "uncertain"
    delta_action = "hold_uncertain"
    decision_reason = "default_hold_uncertain"

    if hard_blocker:
        delta_status = "uncertain"
        delta_action = "block"
        decision_reason = f"hard_blocker:{hard_blocker}"
    elif low_confidence:
        delta_status = "uncertain"
        delta_action = "hold_uncertain"
        decision_reason = "low_confidence_hold"
    elif ttl_expired:
        delta_status = "expired"
        delta_action = "expire_and_reprocess"
        decision_reason = "ttl_expired"
    elif task_context_changed:
        delta_status = "task_context_changed"
        delta_action = "full_reprocess" if comparison.get("comparison_result") == "changed" else "partial_update"
        decision_reason = "task_context_changed_reeval"
    else:
        cmp_res = str(comparison.get("comparison_result") or "unstable")
        prev_content_ref = comparison.get("previous_content_ref")
        cur_content_ref = comparison.get("current_content_ref")
        # Explicit content lifecycle branching (same anchor implied by match_previous_state_v0)
        if previous_state and cur_marked_missing and prev_content_ref:
            delta_status = "content_removed"
            delta_action = "partial_update"
            decision_reason = "explicit_marked_missing_content_removed"
        elif previous_state and prev_content_ref and cur_content_ref and str(prev_content_ref) != str(cur_content_ref):
            delta_status = "content_replaced"
            delta_action = "full_reprocess"
            decision_reason = "content_replaced_same_anchor"
        elif (not previous_state or not prev_content_ref) and cur_content_ref:
            delta_status = "new_content_same_place"
            delta_action = "full_reprocess"
            decision_reason = "new_content_same_place_no_previous_content"
        if is_duplicate_in_window:
            delta_status = "duplicate"
            delta_action = "ignore_duplicate"
            decision_reason = "duplicate_in_window"
        elif cmp_res == "exact_match":
            delta_status = "same_content_same_place"
            delta_action = "reuse_previous"
            decision_reason = "exact_match_reuse"
        elif cmp_res == "near_match":
            delta_status = "same_content_same_place"
            delta_action = "partial_update"
            decision_reason = "near_match_partial_update"
        elif cmp_res == "changed":
            # fallback when explicit branches above did not apply
            if delta_status == "uncertain":
                delta_status = "new_content_same_place"
                delta_action = "full_reprocess"
                decision_reason = "content_changed_same_anchor"
        else:
            delta_status = "uncertain"
            delta_action = "hold_uncertain"
            decision_reason = "unstable_hold"

    matched_ref = str((previous_state or {}).get("state_id")) if isinstance(previous_state, dict) else None
    which_changed = comparison.get("which_signature_changed") if isinstance(comparison, dict) else None

    return {
        "delta_decision_id": f"scene_delta_decision_{_sha_short(str(delta_input.get('delta_input_id')))}",
        "delta_input_id": delta_input.get("delta_input_id"),
        "matched_previous_state_ref": matched_ref,
        "delta_status": delta_status,
        "delta_action": delta_action,
        "change_summary": {
            "text_changed": bool((which_changed or {}).get("content_signature_changed")) if isinstance(which_changed, dict) else False,
            "object_changed": False,
            "layout_changed": False,
            "spatial_shift_ratio": float(comparison.get("spatial_shift_ratio") or 0.0) if isinstance(comparison, dict) else 0.0,
            "confidence_delta": 0.0,
            "task_context_changed": bool(task_context_changed),
            "validity_changed": bool(ttl_expired),
            "previous_content_ref": comparison.get("previous_content_ref"),
            "current_content_ref": comparison.get("current_content_ref"),
        },
        "decision_reason": decision_reason,
        "allowed_to_downstream_candidate": delta_action in ("full_reprocess", "partial_update"),
        "requires_revalidation": delta_action in ("expire_and_reprocess",) or delta_status in ("expired", "contradicted", "content_removed"),
        "hard_blocker": hard_blocker,
        "trace_ref": "scene_delta_trace.jsonl",
        "whitebox_ref": "scene_delta_whitebox.jsonl",
        # Explicit boundary flags (skeleton audit)
        "runtime_invoked": False,
        "hive_upload_invoked": False,
        "world_model_write_invoked": False,
        "navigation_action": None,
        "real_tts_invoked": False,
    }


def run_scene_delta_control_v0(
    *,
    sample_id: str,
    current_input: Dict[str, Any],
    previous_state: Optional[Dict[str, Any]],
    task_context_changed: bool = False,
    is_duplicate_in_window: bool = False,
) -> Dict[str, Any]:
    """
    Offline skeleton orchestration:
    - build anchor (if not provided)
    - match previous state
    - compare signatures
    - decide delta
    - build compression record (if duplicate or reused)
    - build updated processed state
    - generate trace/replay/whitebox rows
    """
    # Extract required pieces from sample current_input
    input_type = str(current_input.get("input_type") or "ocr_evidence")
    source_evidence_id = str(current_input.get("source_evidence_id") or f"evidence_{sample_id}")
    frame_id = str(current_input.get("frame_id") or sample_id)
    timestamp_ms = _as_int(current_input.get("timestamp_ms"), 0)

    observed_at = current_input.get("observed_at") if isinstance(current_input.get("observed_at"), dict) else {"timestamp_ms": timestamp_ms, "time_source": "sample", "date_confidence": "unknown"}
    observed_where = current_input.get("observed_where") if isinstance(current_input.get("observed_where"), dict) else {"place_hint": "unknown", "spatial_anchor_type": "unknown", "geo_location": {"lat": None, "lng": None, "accuracy_m": None}, "relative_position": {"distance_estimate_m": None, "direction_hint": None}}

    content = current_input.get("content") if isinstance(current_input.get("content"), dict) else {}
    content_signature = {
        "text_signature": content.get("content_signature") or content.get("text_signature"),
        "layout_signature": content.get("layout_signature"),
        "crop_signature": content.get("crop_signature"),
        "content_signature": content.get("content_signature"),
        "spatial_signature": content.get("crop_signature"),
        "marked_missing": bool(content.get("marked_missing") or False),
    }
    conf = current_input.get("confidence") if isinstance(current_input.get("confidence"), dict) else {"source_confidence": 0.0, "modality_confidence": 0.0, "trust_score": 0.0}
    low_confidence = _as_float(conf.get("modality_confidence"), 0.0) > 0 and _as_float(conf.get("modality_confidence"), 0.0) < 0.35

    source_attribution = current_input.get("source_attribution") if isinstance(current_input.get("source_attribution"), dict) else {"source": "sample", "provider_id": None, "pipeline_stage": "scene_delta", "notes": None}
    payload_ref = str(current_input.get("content_payload_ref") or f"payload_ref:{source_evidence_id}")
    window_id = str(current_input.get("source_frame_window_id") or "window_000")

    # Anchor (skeleton): based on provided anchor_id or derived
    anchor_id = str(current_input.get("spatiotemporal_anchor_id") or f"sta_{_sha_short(str(current_input.get('anchor_key') or observed_where.get('place_hint') or 'unknown'))}")
    anchor = build_spatiotemporal_delta_anchor_v0(
        spatiotemporal_anchor_id=anchor_id,
        anchor_type=str(current_input.get("anchor_type") or "unknown"),
        observed_at=observed_at,
        observed_where=observed_where,
        region_bbox=current_input.get("region_bbox") if isinstance(current_input.get("region_bbox"), list) else None,
        visual_landmark_ref=current_input.get("visual_landmark_ref"),
        carrier_signature_hint=str(current_input.get("carrier_signature_hint") or ""),
        content_signature_hint=str(content.get("content_signature") or ""),
    )

    delta_input = build_scene_delta_input_v0(
        delta_input_id=str(current_input.get("delta_input_id") or f"scene_delta_input_{_sha_short(sample_id)}"),
        input_type=input_type,
        source_evidence_id=source_evidence_id,
        frame_id=frame_id,
        timestamp_ms=timestamp_ms,
        source_frame_window_id=window_id,
        observed_at=observed_at,
        observed_where=observed_where,
        source_attribution=source_attribution,
        content_signature=content_signature,
        content_payload_ref=payload_ref,
        confidence=conf,
        spatiotemporal_delta_anchor_ref=anchor_id,
        candidate_only=True,
        allows_execute_now=False,
    )

    matched_state_ref, matched_state = match_previous_scene_state_v0(delta_input=delta_input, previous_state=previous_state)
    comparison = compare_scene_signatures_v0(delta_input=delta_input, previous_state=matched_state)

    decision = decide_scene_delta_v0(
        delta_input=delta_input,
        previous_state=matched_state,
        comparison=comparison,
        task_context_changed=bool(task_context_changed),
        low_confidence=bool(low_confidence),
        is_duplicate_in_window=bool(is_duplicate_in_window),
    )

    # Compression (skeleton): generate record for duplicates or reuse_previous decisions
    compression_record: Optional[Dict[str, Any]] = None
    if decision.get("delta_action") in ("reuse_previous", "ignore_duplicate"):
        compression_record = build_repeated_evidence_compression_v0(
            compression_record_id=f"compress_{_sha_short(sample_id)}",
            anchor_ref=anchor_id,
            canonical_evidence_ref=str((matched_state or {}).get("source_evidence_refs", [source_evidence_id])[0] if isinstance(matched_state, dict) else source_evidence_id),
            duplicate_evidence_refs=[source_evidence_id],
            first_seen_at=_as_int((matched_state or {}).get("last_processed_at"), timestamp_ms) if isinstance(matched_state, dict) else timestamp_ms,
            last_seen_at=timestamp_ms,
            content_signature=str(content_signature.get("content_signature") or content_signature.get("text_signature") or ""),
            spatial_signature=str(content_signature.get("crop_signature") or ""),
            compression_method="canonical_ref",
        )

    # Updated processed state (skeleton)
    new_state = build_scene_processed_state_v0(
        state_id=str((matched_state or {}).get("state_id") or f"scene_state_{_sha_short(anchor_id)}"),
        state_scope=str((matched_state or {}).get("state_scope") or "frame_window"),
        source_evidence_refs=list(((matched_state or {}).get("source_evidence_refs") or []) + [source_evidence_id]) if isinstance(matched_state, dict) else [source_evidence_id],
        last_processed_at=timestamp_ms,
        last_seen_at=timestamp_ms,
        seen_count=int(((matched_state or {}).get("seen_count") or 0) + 1) if isinstance(matched_state, dict) else 1,
        signatures={
            "text_signature": content_signature.get("text_signature"),
            "layout_signature": content_signature.get("layout_signature"),
            "crop_signature": content_signature.get("crop_signature"),
            "spatial_signature": content_signature.get("crop_signature"),
            "content_signature": content_signature.get("content_signature"),
        },
        last_delta_decision=str(decision.get("delta_action")),
        last_output_refs=(matched_state or {}).get("last_output_refs") if isinstance(matched_state, dict) else {"text_candidate_ref": None, "world_context_ref": None, "ambient_candidate_ref": None, "filter_result_ref": None},
        ttl_policy=str((matched_state or {}).get("ttl_policy") or str(current_input.get("ttl_policy") or "short_ttl")),
        expires_at=(matched_state or {}).get("expires_at") if isinstance(matched_state, dict) else current_input.get("expires_at"),
        requires_revalidation=True,
        spatiotemporal_delta_anchor_ref=anchor_id,
        compression_record_ref=(compression_record or {}).get("compression_record_id") if compression_record else None,
    )

    # Trace / replay / whitebox rows
    trace_row = {
        "event_type": "trace",
        "sample_id": sample_id,
        "delta_input_id": delta_input.get("delta_input_id"),
        "spatiotemporal_anchor_id": anchor_id,
        "anchor_type": anchor.get("anchor_type"),
        "spatial_signature": (anchor.get("anchor_signature") or {}).get("spatial_signature"),
        "content_signature": str(content_signature.get("content_signature") or content_signature.get("text_signature") or ""),
        "signature_comparison_result": comparison.get("comparison_result"),
        "delta_status": decision.get("delta_status"),
        "delta_action": decision.get("delta_action"),
        "compression_record_id": (compression_record or {}).get("compression_record_id"),
        "duplicate_count": (compression_record or {}).get("duplicate_count"),
        "storage_level": "individual_local",
        "world_change_candidate_created": decision.get("delta_status") in ("carrier_removed", "carrier_added", "content_replaced", "content_removed"),
        "world_model_write_invoked": False,
        "hive_upload_invoked": False,
        "navigation_action": None,
        "real_tts_invoked": False,
    }

    replay_row = {
        "event_type": "replay",
        "sample_id": sample_id,
        "current_input_ref": delta_input.get("delta_input_id"),
        "previous_state_ref": matched_state_ref,
        "signature_inputs_ref": {"current": content_signature, "previous": (matched_state or {}).get("signatures") if isinstance(matched_state, dict) else None},
        "thresholds_ref": {"spatial_shift_threshold": 0.10},
        "delta_decision_ref": decision.get("delta_decision_id"),
        "compression_record_ref": (compression_record or {}).get("compression_record_id"),
        "canonical_evidence_ref": (compression_record or {}).get("canonical_evidence_ref"),
        "duplicate_evidence_refs": (compression_record or {}).get("duplicate_evidence_refs"),
        "compression_method": (compression_record or {}).get("compression_method"),
        "retained_sample_refs": "first_last_or_periodic" if compression_record else None,
        "previous_content_ref": comparison.get("previous_content_ref"),
        "current_content_ref": comparison.get("current_content_ref"),
    }

    whitebox_row = {
        "event_type": "whitebox",
        "sample_id": sample_id,
        "why_reused": "exact_match" if decision.get("delta_action") == "reuse_previous" else None,
        "why_ignored": "duplicate" if decision.get("delta_action") == "ignore_duplicate" else None,
        "why_full_reprocess": "content_changed" if decision.get("delta_action") == "full_reprocess" else None,
        "why_held_uncertain": "low_confidence_or_missing_inputs" if decision.get("delta_action") == "hold_uncertain" else None,
        "why_blocked": decision.get("decision_reason") if decision.get("delta_action") == "block" else None,
        "why_compressed": "reuse_or_duplicate" if compression_record else None,
        "which_signature_changed": comparison.get("which_signature_changed"),
        "why_same_anchor": "anchor_ref_match" if matched_state_ref else None,
    }

    return {
        "scene_delta_input": delta_input,
        "previous_state": previous_state,
        "matched_previous_state_ref": matched_state_ref,
        "spatiotemporal_delta_anchor": anchor,
        "signature_comparison": comparison,
        "scene_delta_decision": decision,
        "repeated_evidence_compression_record": compression_record,
        "scene_processed_state": new_state,
        "trace_row": trace_row,
        "replay_row": replay_row,
        "whitebox_row": whitebox_row,
    }


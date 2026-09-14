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


def build_world_context_trust_v0(
    *,
    source_confidence: float,
    ocr_confidence: Optional[float] = None,
    yolo_confidence: Optional[float] = None,
    cross_validation_status: str = "single_source",
    fraud_risk_status: str = "unknown",
) -> Dict[str, Any]:
    # Skeleton trust_score aggregation (contract-only)
    base = float(max(0.0, min(1.0, source_confidence)))
    if ocr_confidence is not None:
        base = float(max(base, max(0.0, min(1.0, float(ocr_confidence))) * 0.8))
    trust_score = float(max(0.0, min(1.0, base)))
    return {
        "source_confidence": float(source_confidence),
        "ocr_confidence": float(ocr_confidence) if ocr_confidence is not None else None,
        "yolo_confidence": float(yolo_confidence) if yolo_confidence is not None else None,
        "cross_validation_status": cross_validation_status,
        "trust_score": trust_score,
        "fraud_risk_status": fraud_risk_status,
    }


def build_world_context_lifecycle_v0(
    *,
    evidence_status: str,
    ttl_policy: str,
    now_ms: int,
    expires_at: Optional[int] = None,
    requires_revalidation: bool = True,
    last_seen_at: Optional[int] = None,
    seen_count: int = 1,
) -> Dict[str, Any]:
    return {
        "evidence_status": evidence_status,
        "ttl_policy": ttl_policy,
        "expires_at": expires_at,
        "requires_revalidation": bool(requires_revalidation),
        "last_seen_at": int(last_seen_at if last_seen_at is not None else now_ms),
        "seen_count": int(seen_count),
    }


def build_world_model_policy_v0(
    *,
    write_policy: str,
    task_planning_impact: str = "none",
    shareable_to_hive: bool = False,
    requires_user_confirmation: bool = False,
) -> Dict[str, Any]:
    return {
        "write_policy": write_policy,
        "task_planning_impact": task_planning_impact,
        "shareable_to_hive": bool(shareable_to_hive),
        "requires_user_confirmation": bool(requires_user_confirmation),
    }


def build_world_context_evidence_candidate_v0(
    *,
    evidence_type: str,
    source_modalities: List[str],
    source_evidence_refs: List[str],
    observed_at: Dict[str, Any],
    observed_where: Dict[str, Any],
    observed_where_source: str,
    spatial_anchor_confidence: float,
    anchor_status: str,
    content: Dict[str, Any],
    trust: Dict[str, Any],
    lifecycle: Dict[str, Any],
    world_model_policy: Dict[str, Any],
    source_reference_chain: List[Dict[str, Any]],
    source_layers: List[str],
    missing_source_refs: List[Dict[str, Any]],
    source_ref_integrity_status: str,
    trace_ref: str,
    replay_ref: str,
    whitebox_ref: str,
    seq: int,
) -> Dict[str, Any]:
    return {
        "world_context_evidence_id": f"world_ctx_{seq:04d}",
        "candidate_only": True,
        "evidence_type": evidence_type,
        "source_modalities": source_modalities,
        "source_evidence_refs": source_evidence_refs,
        "observed_at": observed_at,
        "observed_where": observed_where,
        "observed_where_source": observed_where_source,
        "spatial_anchor_confidence": float(spatial_anchor_confidence),
        "anchor_status": anchor_status,
        "content": content,
        "trust": trust,
        "lifecycle": lifecycle,
        "world_model_policy": world_model_policy,
        "source_reference_chain": source_reference_chain,
        "source_layers": source_layers,
        "missing_source_refs": missing_source_refs,
        "source_ref_integrity_status": source_ref_integrity_status,
        "governance": {
            "world_model_write_invoked": False,
            "hive_upload_invoked": False,
            "navigation_action": None,
            "real_tts_invoked": False,
            "recommendation_invoked": False,
        },
        "trace_ref": trace_ref,
        "replay_ref": replay_ref,
        "whitebox_ref": whitebox_ref,
    }


def _ref(level: str, ref_id: Optional[str], ref_type: str) -> Dict[str, Any]:
    return {"level": level, "ref_id": ref_id, "ref_type": ref_type}


def _integrity_status(source_evidence_refs: List[str], missing_source_refs: List[Dict[str, Any]]) -> str:
    if not source_evidence_refs:
        return "broken"
    if missing_source_refs:
        return "partial"
    return "complete"


def _sensing_modalities_only(mods: List[str]) -> List[str]:
    allow = {"ocr", "yolo", "map", "gps", "visual_symbol", "user_feedback"}
    return [m for m in mods if m in allow]


def map_scene_delta_decision_to_world_context_status_v0(delta_status: str) -> Tuple[str, bool]:
    """
    Returns (lifecycle.evidence_status, requires_revalidation).
    """
    s = str(delta_status or "unknown")
    if s in ("expired", "content_removed"):
        return "expired_candidate", True
    if s in ("contradicted", "content_contradicted"):
        return "contradicted_candidate", True
    if s in ("duplicate",):
        return "candidate", False
    if s in ("uncertain",):
        return "uncertain_candidate", True
    if s in ("content_replaced", "new_content_same_place", "carrier_added", "carrier_removed", "carrier_changed"):
        return "active_candidate", True
    if s in ("same_content_same_place", "unchanged"):
        return "active_candidate", False
    return "candidate", True


def _infer_observed_at_where_from_midplatform_evidence(ev: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    ts = _as_int(ev.get("timestamp_ms"), 0)
    observed_at = {"timestamp_ms": ts, "time_source": "midplatform_clock", "date_confidence": "system_confirmed", "observation_window_id": None}
    observed_where = {
        "geo_location": {"lat": None, "lng": None, "accuracy_m": None},
        "place_hint": "unknown",
        "spatial_anchor_type": "unknown",
        "relative_position": {"distance_estimate_m": None, "direction_hint": None},
        "spatiotemporal_anchor_ref": None,
        "crop_region": None,
        "image_ref": ev.get("frame_id") or ev.get("source_evidence_id"),
    }
    return observed_at, observed_where


def _infer_observed_at_where_from_scene_delta_trace(trace: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    # SceneDelta skeleton doesn't carry full observed_where; keep placeholder but bind anchor_ref if present.
    observed_at = {"timestamp_ms": 0, "time_source": "midplatform_clock", "date_confidence": "system_confirmed", "observation_window_id": None}
    anchor_type = str(trace.get("anchor_type") or "unknown")
    spatial_anchor_type = "unknown"
    if anchor_type in ("poster_board", "notice_board", "signboard", "screen"):
        spatial_anchor_type = "visual_landmark"
    observed_where = {
        "geo_location": {"lat": None, "lng": None, "accuracy_m": None},
        "place_hint": "unknown",
        "spatial_anchor_type": spatial_anchor_type,
        "relative_position": {"distance_estimate_m": None, "direction_hint": None},
        "spatiotemporal_anchor_ref": trace.get("spatiotemporal_anchor_id"),
        "spatial_scope": "scene_local",
        "anchor_type": anchor_type,
        "spatial_signature": trace.get("spatial_signature"),
    }
    return observed_at, observed_where


def _map_midplatform_class_to_evidence_type_and_policy(visual_cls: str) -> Tuple[str, str, str]:
    """
    Returns (evidence_type, write_policy, ttl_policy).
    """
    c = str(visual_cls or "unknown")
    if c == "world_context_text":
        return "text_context", "scene_local_candidate", "scene_local_ttl"
    if c in ("commercial_context_text", "promotional_text"):
        return "commercial_activity", "low_priority_candidate", "short_ttl"
    if c in ("advertisement_like_text", "ambient_context_text", "experience_enrichment_text"):
        return "ambient_context", "low_priority_candidate", "short_ttl"
    if c in (
        "uncertain_relevance_text",
        "illegible_text",
        "blurred_text",
        "scribble_or_graffiti_text",
        "decorative_or_stylized_text",
        "fragmented_text",
        "non_actionable_text",
        "meaning_uncertain_text",
        "irrelevant_or_noise_text",
    ):
        return "unknown", "no_write", "no_persistent_write"
    return "unknown", "no_write", "no_persistent_write"


def map_midplatform_candidate_to_world_context_v0(
    *,
    evidence_input: Dict[str, Any],
    filter_result: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    allowed_world = bool(filter_result.get("allowed_for_world_context_candidate"))
    allowed_ambient = bool(filter_result.get("allowed_for_ambient_context_candidate"))
    if not (allowed_world or allowed_ambient):
        return None

    visual_cls = str(filter_result.get("visual_text_relevance_class") or "unknown")
    evidence_type, write_policy, ttl_policy = _map_midplatform_class_to_evidence_type_and_policy(visual_cls)
    if write_policy == "no_write":
        # still allow generating uncertain candidates in skeleton, but keep them no_write and candidate-only
        pass

    observed_at, observed_where = _infer_observed_at_where_from_midplatform_evidence(evidence_input)
    raw_text_candidates = evidence_input.get("raw_text_candidates") or []
    if isinstance(raw_text_candidates, list):
        sorted_lines = sorted(
            [c for c in raw_text_candidates if isinstance(c, dict)],
            key=lambda c: _as_int(c.get("line_order"), 0),
        )
        raw_text = "\n".join([str(c.get("text") or "").strip() for c in sorted_lines if str(c.get("text") or "").strip()])
        confs = [_as_float(c.get("confidence"), 0.0) for c in sorted_lines if c.get("confidence") is not None]
        ocr_conf = float(sum(confs) / max(1, len(confs))) if confs else None
        ts_from_lines = [_as_int(c.get("timestamp_ms"), 0) for c in sorted_lines if c.get("timestamp_ms") is not None]
        now_ms = max(ts_from_lines) if ts_from_lines else _as_int(evidence_input.get("timestamp_ms"), 0)
    else:
        raw_text = ""
        ocr_conf = None
        now_ms = _as_int(evidence_input.get("timestamp_ms"), 0)

    # observed_where crop region from OCR bboxes (union)
    bboxes = []
    for c in raw_text_candidates if isinstance(raw_text_candidates, list) else []:
        if isinstance(c, dict) and isinstance(c.get("bbox"), list) and len(c.get("bbox")) == 4:
            bboxes.append(c.get("bbox"))
    if bboxes:
        xs1 = [float(b[0]) for b in bboxes]
        ys1 = [float(b[1]) for b in bboxes]
        xs2 = [float(b[2]) for b in bboxes]
        ys2 = [float(b[3]) for b in bboxes]
        observed_where["crop_region"] = [min(xs1), min(ys1), max(xs2), max(ys2)]

    evidence_status = "candidate"
    requires_revalidation = True
    if visual_cls == "world_context_text":
        evidence_status = "active_candidate"
        requires_revalidation = True
    elif visual_cls in ("commercial_context_text", "promotional_text", "advertisement_like_text"):
        evidence_status = "active_candidate"
        requires_revalidation = True
    elif visual_cls in ("uncertain_relevance_text", "illegible_text", "blurred_text", "fragmented_text", "meaning_uncertain_text"):
        evidence_status = "uncertain_candidate"
        requires_revalidation = True
    elif visual_cls == "duplicate":
        evidence_status = "candidate"
        requires_revalidation = False

    trust = build_world_context_trust_v0(
        source_confidence=float(ocr_conf if ocr_conf is not None else 0.0),
        ocr_confidence=ocr_conf,
        yolo_confidence=None,
        cross_validation_status="single_source",
        fraud_risk_status="unknown",
    )
    lifecycle = build_world_context_lifecycle_v0(
        evidence_status=evidence_status,
        ttl_policy=ttl_policy,
        now_ms=now_ms,
        expires_at=None,
        requires_revalidation=requires_revalidation,
        last_seen_at=now_ms,
        seen_count=1,
    )
    world_policy = build_world_model_policy_v0(
        write_policy=write_policy,
        task_planning_impact="none",
        shareable_to_hive=False,
        requires_user_confirmation=False,
    )
    content = {
        "text": raw_text if raw_text else None,
        "entity_type": evidence_type,
        "entity_name": None,
        "details": raw_text if raw_text else None,
        "raw_content_ref": str(evidence_input.get("evidence_id") or ""),
    }

    # Source ref chain (honest, no fabrication)
    missing_source_refs: List[Dict[str, Any]] = []
    if not evidence_input.get("evidence_id"):
        missing_source_refs.append({"level": "midplatform_evidence", "expected_ref_type": "MidPlatformOCREvidenceInput"})

    chain = [
        _ref("midplatform_evidence", str(evidence_input.get("evidence_id") or None), "MidPlatformOCREvidenceInput"),
    ]
    # OCR raw candidates are optional
    text_ids = [str(c.get("text_id")) for c in raw_text_candidates if isinstance(c, dict) and c.get("text_id")]
    if text_ids:
        chain.append(_ref("ocr", text_ids[0], "OCRRawTextCandidate"))
    else:
        missing_source_refs.append({"level": "ocr", "expected_ref_type": "OCRRawTextCandidate"})

    return {
        "evidence_type": evidence_type,
        "source_modalities": ["ocr"],
        "source_evidence_refs": [str(evidence_input.get("evidence_id") or "")] if evidence_input.get("evidence_id") else [],
        "observed_at": observed_at,
        "observed_where": observed_where,
        "observed_where_source": "midplatform_ocr_evidence",
        "spatial_anchor_confidence": 0.3,
        "anchor_status": "missing_or_unresolved",
        "content": content,
        "trust": trust,
        "lifecycle": lifecycle,
        "world_model_policy": world_policy,
        "source_reference_chain": chain,
        "source_layers": ["sensing", "bridge", "midplatform", "world_context_candidate"],
        "missing_source_refs": missing_source_refs,
        "visual_text_relevance_class": visual_cls,
    }


def _build_commercial_activity_candidate_v0(*, world_ctx_id: str, text: str, observed_at: Dict[str, Any], observed_where: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "commercial_activity_evidence_id": f"commercial_{_sha_short(world_ctx_id)}",
        "source_world_context_evidence_id": world_ctx_id,
        "store_name": None,
        "activity_text": text,
        "discount_or_promotion": True,
        "valid_time_text": None,
        "observed_at": observed_at,
        "observed_where": observed_where,
        "expiry_policy": "short_ttl",
        "requires_revalidation": True,
        "allowed_for_experience_enrichment": True,
        "allowed_for_primary_task_decision": False,
        "navigation_action": None,
        "fraud_risk_status": "unknown",
    }


def _build_world_change_event_candidate_v0(
    *,
    delta_decision: Dict[str, Any],
    anchor_ref: Optional[str],
    seq: int,
) -> Dict[str, Any]:
    change_type = str(delta_decision.get("delta_status") or "unknown")
    return {
        "world_change_event_id": f"world_change_{seq:04d}",
        "source_delta_decision_id": str(delta_decision.get("delta_decision_id") or ""),
        "change_type": change_type,
        "spatiotemporal_anchor_ref": anchor_ref,
        "previous_state_ref": delta_decision.get("matched_previous_state_ref"),
        "current_state_ref": None,
        "confidence": 0.0,
        "impact_on_navigation": "none",
        "impact_on_recommendation": "none",
        "candidate_only": True,
        "requires_revalidation": True,
        "world_model_write_invoked": False,
    }


def run_world_context_evidence_candidate_v0(
    *,
    input_type: str,
    midplatform_root: Optional[str] = None,
    scene_delta_root: Optional[str] = None,
    sample_matrix: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Offline skeleton:
    - From midplatform root: map filter_results + evidence_inputs -> WorldContextEvidence candidates
    - From scene_delta root: map delta decisions -> WorldChangeEvent candidates (+ WorldContextEvidence wrappers)
    - From sample_matrix: directly treat samples as already normalized intermediate objects.
    """
    world_candidates: List[Dict[str, Any]] = []
    commercial_candidates: List[Dict[str, Any]] = []
    world_change_candidates: List[Dict[str, Any]] = []
    trust_lifecycle_records: List[Dict[str, Any]] = []

    trace_rows: List[Dict[str, Any]] = []
    replay_rows: List[Dict[str, Any]] = []
    whitebox_rows: List[Dict[str, Any]] = []

    trace_ref = "world_context_evidence_trace.jsonl"
    replay_ref = "world_context_evidence_replay.jsonl"
    whitebox_ref = "world_context_evidence_whitebox.jsonl"

    if input_type == "midplatform_ocr_bridge_root":
        if not midplatform_root:
            raise SystemExit("missing_midplatform_root")
        import os, json  # local import to keep module pure

        def rj(fn: str) -> Any:
            p = os.path.join(midplatform_root, fn)
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)

        evidence_inputs = rj("midplatform_ocr_evidence_inputs.json")
        filter_results = rj("filter_results.json")

        # Align by index (skeleton guarantee)
        for i, (ev, fr) in enumerate(zip(evidence_inputs, filter_results)):
            mapped = map_midplatform_candidate_to_world_context_v0(evidence_input=ev, filter_result=fr)
            if not mapped:
                continue
            wc = build_world_context_evidence_candidate_v0(
                evidence_type=mapped["evidence_type"],
                source_modalities=_sensing_modalities_only(mapped["source_modalities"]),
                source_evidence_refs=mapped["source_evidence_refs"],
                observed_at=mapped["observed_at"],
                observed_where=mapped["observed_where"],
                observed_where_source=mapped["observed_where_source"],
                spatial_anchor_confidence=mapped["spatial_anchor_confidence"],
                anchor_status=mapped["anchor_status"],
                content=mapped["content"],
                trust=mapped["trust"],
                lifecycle=mapped["lifecycle"],
                world_model_policy=mapped["world_model_policy"],
                source_reference_chain=[_ref("world_context_candidate", None, "WorldContextEvidenceCandidate")] + list(mapped["source_reference_chain"]),
                source_layers=list(mapped["source_layers"]),
                missing_source_refs=list(mapped["missing_source_refs"]),
                source_ref_integrity_status=_integrity_status(mapped["source_evidence_refs"], list(mapped["missing_source_refs"])),
                trace_ref=trace_ref,
                replay_ref=replay_ref,
                whitebox_ref=whitebox_ref,
                seq=len(world_candidates) + 1,
            )
            if isinstance(wc.get("source_reference_chain"), list) and wc["source_reference_chain"]:
                if isinstance(wc["source_reference_chain"][0], dict):
                    wc["source_reference_chain"][0]["ref_id"] = wc["world_context_evidence_id"]
            world_candidates.append(wc)

            if mapped.get("evidence_type") == "commercial_activity" and (mapped.get("content") or {}).get("text"):
                commercial_candidates.append(
                    _build_commercial_activity_candidate_v0(
                        world_ctx_id=wc["world_context_evidence_id"],
                        text=str((mapped["content"] or {}).get("text") or ""),
                        observed_at=mapped["observed_at"],
                        observed_where=mapped["observed_where"],
                    )
                )

            trust_lifecycle_records.append({"world_context_evidence_id": wc["world_context_evidence_id"], "trust": wc["trust"], "lifecycle": wc["lifecycle"]})

            trace_rows.append(
                {
                    "event_type": "trace",
                    "source_input_type": "midplatform_ocr_bridge_root",
                    "source_evidence_refs": wc["source_evidence_refs"],
                    "evidence_type": wc["evidence_type"],
                    "trust_score": wc["trust"]["trust_score"],
                    "lifecycle_status": wc["lifecycle"]["evidence_status"],
                    "world_model_policy": wc["world_model_policy"]["write_policy"],
                    "governance": wc["governance"],
                }
            )
            replay_rows.append({"event_type": "replay", "source_payload_refs": wc["source_evidence_refs"], "mapping_rule_refs": {"visual_text_relevance_class": mapped.get("visual_text_relevance_class")}})
            whitebox_rows.append({"event_type": "whitebox", "why_candidate_created": "mapped_from_midplatform_filter", "why_no_write": wc["world_model_policy"]["write_policy"] == "no_write"})

    elif input_type == "scene_delta_root":
        if not scene_delta_root:
            raise SystemExit("missing_scene_delta_root")
        import os, json

        def rj(fn: str) -> Any:
            p = os.path.join(scene_delta_root, fn)
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)

        decisions = rj("scene_delta_decisions.json")
        # Also read trace for anchor refs and content signatures
        trace_rows_in = []
        trace_path = os.path.join(scene_delta_root, "scene_delta_trace.jsonl")
        with open(trace_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    trace_rows_in.append(json.loads(line))
                except Exception:
                    continue

        for i, d in enumerate(decisions):
            t = trace_rows_in[i] if i < len(trace_rows_in) and isinstance(trace_rows_in[i], dict) else {}
            delta_status = str(d.get("delta_status") or "")
            lifecycle_status, requires_revalidation = map_scene_delta_decision_to_world_context_status_v0(delta_status)
            observed_at, observed_where = _infer_observed_at_where_from_scene_delta_trace(t)
            now_ms = 0
            trust = build_world_context_trust_v0(source_confidence=0.0, cross_validation_status="single_source")
            lifecycle = build_world_context_lifecycle_v0(
                evidence_status=lifecycle_status,
                ttl_policy="scene_local_ttl",
                now_ms=now_ms,
                expires_at=None,
                requires_revalidation=requires_revalidation,
                last_seen_at=now_ms,
                seen_count=1,
            )
            world_policy = build_world_model_policy_v0(write_policy="no_write", task_planning_impact="none", shareable_to_hive=False)
            content = {
                "text": None,
                "entity_type": "world_change",
                "entity_name": None,
                "details": f"scene_delta:{delta_status}",
                "raw_content_ref": str(d.get("delta_decision_id") or ""),
            }
            missing_source_refs: List[Dict[str, Any]] = []
            if not d.get("delta_decision_id"):
                missing_source_refs.append({"level": "scene_delta", "expected_ref_type": "SceneDeltaDecision"})
            if not observed_where.get("spatiotemporal_anchor_ref"):
                missing_source_refs.append({"level": "scene_delta_anchor", "expected_ref_type": "SpatiotemporalDeltaAnchor"})

            anchor_status = "present" if observed_where.get("spatiotemporal_anchor_ref") else "missing_or_unresolved"
            observed_where_source = "scene_delta_anchor" if observed_where.get("spatiotemporal_anchor_ref") else "fallback_unknown"
            spatial_anchor_confidence = 0.8 if observed_where.get("spatiotemporal_anchor_ref") else 0.0

            source_evidence_refs = [str(d.get("delta_decision_id"))] if d.get("delta_decision_id") else []
            chain = [
                _ref("scene_delta", str(d.get("delta_decision_id") or None), "SceneDeltaDecision"),
                _ref("scene_delta_anchor", str(observed_where.get("spatiotemporal_anchor_ref") or None), "SpatiotemporalDeltaAnchor"),
            ]

            wc = build_world_context_evidence_candidate_v0(
                evidence_type="world_change",
                source_modalities=[],
                source_evidence_refs=source_evidence_refs,
                observed_at=observed_at,
                observed_where=observed_where,
                observed_where_source=observed_where_source,
                spatial_anchor_confidence=spatial_anchor_confidence,
                anchor_status=anchor_status,
                content=content,
                trust=trust,
                lifecycle=lifecycle,
                world_model_policy=world_policy,
                source_reference_chain=[_ref("world_context_candidate", None, "WorldContextEvidenceCandidate")] + chain,
                source_layers=["scene_delta", "world_context_candidate"],
                missing_source_refs=missing_source_refs,
                source_ref_integrity_status=_integrity_status(source_evidence_refs, missing_source_refs),
                trace_ref=trace_ref,
                replay_ref=replay_ref,
                whitebox_ref=whitebox_ref,
                seq=len(world_candidates) + 1,
            )
            if isinstance(wc.get("source_reference_chain"), list) and wc["source_reference_chain"]:
                if isinstance(wc["source_reference_chain"][0], dict):
                    wc["source_reference_chain"][0]["ref_id"] = wc["world_context_evidence_id"]
            world_candidates.append(wc)
            trust_lifecycle_records.append({"world_context_evidence_id": wc["world_context_evidence_id"], "trust": wc["trust"], "lifecycle": wc["lifecycle"]})

            if delta_status in ("new_content_same_place", "content_replaced", "content_removed", "expired", "carrier_added", "carrier_removed", "contradicted"):
                world_change_candidates.append(_build_world_change_event_candidate_v0(delta_decision=d, anchor_ref=t.get("spatiotemporal_anchor_id"), seq=len(world_change_candidates) + 1))

            trace_rows.append(
                {
                    "event_type": "trace",
                    "source_input_type": "scene_delta_root",
                    "source_evidence_refs": wc["source_evidence_refs"],
                    "evidence_type": wc["evidence_type"],
                    "lifecycle_status": wc["lifecycle"]["evidence_status"],
                    "governance": wc["governance"],
                }
            )
            replay_rows.append({"event_type": "replay", "source_payload_refs": wc["source_evidence_refs"], "world_change_event_refs": [w["world_change_event_id"] for w in world_change_candidates[-1:]]})
            whitebox_rows.append({"event_type": "whitebox", "why_world_change_candidate": delta_status})

    elif input_type == "sample_matrix":
        if not isinstance(sample_matrix, dict):
            raise SystemExit("missing_sample_matrix")
        samples = sample_matrix.get("samples") or []
        if not isinstance(samples, list):
            raise SystemExit("sample_matrix_missing_samples")
        for s in samples:
            if not isinstance(s, dict):
                continue
            now_ms = _as_int(s.get("timestamp_ms"), 0)
            observed_at = {"timestamp_ms": now_ms, "time_source": "midplatform_clock", "date_confidence": "system_confirmed", "observation_window_id": None}
            observed_where = {
                "geo_location": {"lat": None, "lng": None, "accuracy_m": None},
                "place_hint": str(s.get("place_hint") or "unknown"),
                "spatial_anchor_type": str(s.get("spatial_anchor_type") or "unknown"),
                "relative_position": {"distance_estimate_m": None, "direction_hint": None},
                "spatiotemporal_anchor_ref": s.get("spatiotemporal_anchor_ref"),
            }
            content = s.get("content") if isinstance(s.get("content"), dict) else {}
            trust = build_world_context_trust_v0(source_confidence=_as_float(s.get("source_confidence"), 0.0), cross_validation_status="single_source")
            lifecycle = build_world_context_lifecycle_v0(
                evidence_status=str(s.get("evidence_status") or "candidate"),
                ttl_policy=str(s.get("ttl_policy") or "short_ttl"),
                now_ms=now_ms,
                expires_at=None,
                requires_revalidation=bool(s.get("requires_revalidation") if s.get("requires_revalidation") is not None else True),
                last_seen_at=now_ms,
                seen_count=1,
            )
            world_policy = build_world_model_policy_v0(write_policy=str(s.get("write_policy") or "no_write"))
            wc = build_world_context_evidence_candidate_v0(
                evidence_type=str(s.get("evidence_type") or "unknown"),
                source_modalities=_sensing_modalities_only(list(s.get("source_modalities") or [])),
                source_evidence_refs=list(s.get("source_evidence_refs") or []),
                observed_at=observed_at,
                observed_where=observed_where,
                observed_where_source=str(s.get("observed_where_source") or ("scene_delta_anchor" if observed_where.get("spatiotemporal_anchor_ref") else "fallback_unknown")),
                spatial_anchor_confidence=float(s.get("spatial_anchor_confidence") or (0.8 if observed_where.get("spatiotemporal_anchor_ref") else 0.0)),
                anchor_status=str(s.get("anchor_status") or ("present" if observed_where.get("spatiotemporal_anchor_ref") else "missing_or_unresolved")),
                content=content,
                trust=trust,
                lifecycle=lifecycle,
                world_model_policy=world_policy,
                source_reference_chain=[_ref("world_context_candidate", None, "WorldContextEvidenceCandidate")],
                source_layers=list(s.get("source_layers") or ["world_context_candidate"]),
                missing_source_refs=list(s.get("missing_source_refs") or ([] if (s.get("source_evidence_refs") or []) else [{"level": "unknown", "expected_ref_type": "UpstreamEvidence"}])),
                source_ref_integrity_status=str(s.get("source_ref_integrity_status") or _integrity_status(list(s.get("source_evidence_refs") or []), list(s.get("missing_source_refs") or []))),
                trace_ref=trace_ref,
                replay_ref=replay_ref,
                whitebox_ref=whitebox_ref,
                seq=len(world_candidates) + 1,
            )
            if isinstance(wc.get("source_reference_chain"), list) and wc["source_reference_chain"]:
                if isinstance(wc["source_reference_chain"][0], dict):
                    wc["source_reference_chain"][0]["ref_id"] = wc["world_context_evidence_id"]
            world_candidates.append(wc)

            trust_lifecycle_records.append({"world_context_evidence_id": wc["world_context_evidence_id"], "trust": wc["trust"], "lifecycle": wc["lifecycle"]})

            if wc.get("evidence_type") == "commercial_activity" and isinstance(content, dict) and content.get("text"):
                commercial_candidates.append(
                    _build_commercial_activity_candidate_v0(
                        world_ctx_id=wc["world_context_evidence_id"],
                        text=str(content.get("text") or ""),
                        observed_at=observed_at,
                        observed_where=observed_where,
                    )
                )

            if wc.get("evidence_type") == "world_change":
                details = ""
                if isinstance(content, dict):
                    details = str(content.get("details") or "")
                change_type = None
                if details.startswith("scene_delta:"):
                    change_type = details.split("scene_delta:", 1)[1].strip()
                if change_type:
                    world_change_candidates.append(
                        {
                            "world_change_event_id": f"world_change_{len(world_change_candidates) + 1:04d}",
                            "source_delta_decision_id": str((wc.get("source_evidence_refs") or [""])[0]),
                            "change_type": change_type,
                            "spatiotemporal_anchor_ref": observed_where.get("spatiotemporal_anchor_ref"),
                            "previous_state_ref": None,
                            "current_state_ref": None,
                            "confidence": 0.0,
                            "impact_on_navigation": "none",
                            "impact_on_recommendation": "none",
                            "candidate_only": True,
                            "requires_revalidation": True,
                            "world_model_write_invoked": False
                        }
                    )
        # minimal trace rows
        for wc in world_candidates:
            trace_rows.append({"event_type": "trace", "source_input_type": "sample_matrix", "source_evidence_refs": wc["source_evidence_refs"], "governance": wc["governance"]})
            replay_rows.append({"event_type": "replay", "source_payload_refs": wc["source_evidence_refs"]})
            whitebox_rows.append({"event_type": "whitebox", "why_candidate_created": "sample_matrix"})

    else:
        raise SystemExit("unsupported_input_type")

    return {
        "world_context_evidence_candidates": world_candidates,
        "commercial_activity_evidence_candidates": commercial_candidates,
        "world_change_event_candidates": world_change_candidates,
        "trust_and_lifecycle_records": trust_lifecycle_records,
        "trace_rows": trace_rows,
        "replay_rows": replay_rows,
        "whitebox_rows": whitebox_rows,
    }


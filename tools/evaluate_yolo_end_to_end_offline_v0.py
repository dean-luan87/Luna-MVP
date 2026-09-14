#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelPerception-010
YOLO Shadow End-to-End Offline Evaluation v0 (offline).

Reads five roots:
  FieldBatch -> YOLO Perception Replacement -> YOLO SceneTask Bridge -> YOLO Fusion Bridge -> YOLO Output Bridge
and generates:
- yolo_e2e_offline_evaluation_summary.json
- per_sample_yolo_chain_results.json
- yolo_chain_trace_consistency.json
- evaluation_notes.md

Hard boundaries:
- offline only; candidate-only; no real TTS; no forbidden semantics
- do not claim real navigation capability validation
"""

from __future__ import annotations

import argparse
import json
import os
import time
from typing import Any, Dict, List, Optional, Set


def _now_ms() -> int:
    return int(time.time() * 1000)


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def _write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _rate(n: int, d: int) -> float:
    return float(n) / float(d) if d else 0.0


def _has_nonempty_list(x: Any) -> bool:
    return isinstance(x, list) and len(x) > 0


def _resolve_root(p: str, repo_root: str) -> str:
    if not p:
        return p
    if os.path.isabs(p) and os.path.exists(p):
        return p
    if not os.path.isabs(p):
        cand_repo = os.path.join(repo_root, p)
        if os.path.exists(cand_repo):
            return cand_repo
        cand_ws = os.path.join("/Users/luanlei/Desktop/Luna-Workspace-Min", p)
        if os.path.exists(cand_ws):
            return cand_ws
    return p


def _schema_ok_perception(sample: Dict[str, Any]) -> bool:
    # Replacement tool stores 5 signals + signal_presence
    sigs = sample.get("signals")
    pres = sample.get("signal_presence")
    if not isinstance(sigs, dict) or not isinstance(pres, dict):
        return False
    required = [
        "object_stability_signal",
        "ocr_navigation_signal",
        "spatial_passability_signal",
        "dynamic_event_signal",
        "risk_field_signal",
    ]
    if not all(k in sigs for k in required):
        return False
    required_pres = [
        "object_stability_signal_present",
        "ocr_navigation_signal_present",
        "spatial_passability_signal_present",
        "dynamic_event_signal_present",
        "risk_field_signal_present",
    ]
    if not all(k in pres for k in required_pres):
        return False
    return True


def _schema_ok_scene_task(sample: Dict[str, Any]) -> bool:
    ss = sample.get("scene_state")
    cands = sample.get("task_candidates")
    if not isinstance(ss, dict) or not isinstance(cands, list):
        return False
    for k in ("scene_id", "scene_type", "scene_confidence", "scene_phase", "active_task_id", "task_status"):
        if k not in ss:
            return False
    for c in cands:
        if not isinstance(c, dict):
            return False
        if c.get("allows_execute_now") is not False:
            return False
    return True


def _schema_ok_fusion(sample: Dict[str, Any]) -> bool:
    fc = sample.get("fusion_decision_candidate")
    if not isinstance(fc, dict):
        return False
    for k in ("fusion_candidate_id", "fusion_candidate_type", "allows_execute_now", "source_attribution", "reason_codes"):
        if k not in fc:
            return False
    if fc.get("allows_execute_now") is not False:
        return False
    return True


def _schema_ok_output(sample: Dict[str, Any]) -> bool:
    oc = sample.get("navigation_output_candidate")
    if not isinstance(oc, dict):
        return False
    for k in (
        "output_candidate_id",
        "source_fusion_candidate_id",
        "source_type",
        "output_type",
        "priority",
        "message_template_id",
        "message_text_candidate",
        "generated_at_ms",
        "expires_at_ms",
        "validity_window_ms",
        "reason_codes",
        "allows_execute_now",
        "real_tts_invoked",
    ):
        if k not in oc:
            return False
    if oc.get("allows_execute_now") is not False:
        return False
    if oc.get("real_tts_invoked") is not False:
        return False
    if int(oc.get("expires_at_ms")) <= int(oc.get("generated_at_ms")):
        return False
    if (int(oc.get("expires_at_ms")) - int(oc.get("generated_at_ms"))) != int(oc.get("validity_window_ms")):
        return False
    return True


def _yolo_source_preserved_all_stages(pe: Optional[Dict[str, Any]], st: Optional[Dict[str, Any]], fu: Optional[Dict[str, Any]], oo: Optional[Dict[str, Any]]) -> bool:
    """
    Minimal traceability definition for v0:
    - perception has yolo_invoked/detection_count/detected_classes
    - fusion candidate has source_attribution.yolo_source with these fields (propagated from 008)
    - output candidate has source_attribution.yolo_source with these fields (propagated from 009)
    """
    if not pe or not fu or not oo:
        return False
    pe_ok = (pe.get("yolo_invoked") is True) and ("detection_count" in pe) and ("detected_classes" in pe)
    fu_fc = (fu.get("fusion_decision_candidate") or {}) if isinstance(fu.get("fusion_decision_candidate"), dict) else {}
    fu_ys = (fu_fc.get("source_attribution") or {}).get("yolo_source") if isinstance(fu_fc.get("source_attribution"), dict) else None
    fu_ok = isinstance(fu_ys, dict) and ("yolo_invoked" in fu_ys) and ("detection_count" in fu_ys) and ("detected_classes" in fu_ys)
    oo_oc = (oo.get("navigation_output_candidate") or {}) if isinstance(oo.get("navigation_output_candidate"), dict) else {}
    oo_ys = (oo_oc.get("source_attribution") or {}).get("yolo_source") if isinstance(oo_oc.get("source_attribution"), dict) else None
    oo_ok = isinstance(oo_ys, dict) and ("yolo_invoked" in oo_ys) and ("detection_count" in oo_ys) and ("detected_classes" in oo_ys)
    # SceneTask stage currently carries yolo_invoked/detection_count/detected_classes at wrapper level, but we don't require deep attribution there.
    st_ok = True if st else False
    return bool(pe_ok and st_ok and fu_ok and oo_ok)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--field-batch-root", required=True)
    ap.add_argument("--yolo-perception-root", required=True)
    ap.add_argument("--yolo-scene-task-root", required=True)
    ap.add_argument("--yolo-fusion-root", required=True)
    ap.add_argument("--yolo-output-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    args.field_batch_root = _resolve_root(args.field_batch_root, repo_root=repo_root)
    args.yolo_perception_root = _resolve_root(args.yolo_perception_root, repo_root=repo_root)
    args.yolo_scene_task_root = _resolve_root(args.yolo_scene_task_root, repo_root=repo_root)
    args.yolo_fusion_root = _resolve_root(args.yolo_fusion_root, repo_root=repo_root)
    args.yolo_output_root = _resolve_root(args.yolo_output_root, repo_root=repo_root)

    out_root = args.output_root
    if os.path.exists(out_root) and (not os.path.isdir(out_root) or os.listdir(out_root)):
        raise SystemExit("output_root_must_be_empty_dir_or_nonexistent")
    os.makedirs(out_root, exist_ok=True)

    # FieldBatch sample_matrix
    fb_sm = _read_json(os.path.join(args.field_batch_root, "sample_matrix.json"))
    fb_samples = fb_sm.get("samples") or []
    if not isinstance(fb_samples, list) or not fb_samples:
        raise SystemExit("field_batch_sample_matrix_missing_or_empty")
    fb_by_id = {str(s.get("sample_id")): s for s in fb_samples if isinstance(s, dict) and s.get("sample_id")}

    # YOLO perception replacement
    pe_summary = _read_json(os.path.join(args.yolo_perception_root, "yolo_perception_replacement_summary.json"))
    pe_samples = _read_json(os.path.join(args.yolo_perception_root, "per_sample_yolo_perception_replacement_results.json")).get("samples") or []
    pe_by_id = {str(s.get("sample_id")): s for s in pe_samples if isinstance(s, dict) and s.get("sample_id")}

    # YOLO SceneTask bridge
    st_summary = _read_json(os.path.join(args.yolo_scene_task_root, "yolo_scene_task_bridge_summary.json"))
    st_samples = _read_json(os.path.join(args.yolo_scene_task_root, "per_sample_yolo_scene_task_results.json")).get("samples") or []
    st_by_id = {str(s.get("sample_id")): s for s in st_samples if isinstance(s, dict) and s.get("sample_id")}

    # YOLO Fusion bridge
    fu_summary = _read_json(os.path.join(args.yolo_fusion_root, "yolo_fusion_bridge_summary.json"))
    fu_samples = _read_json(os.path.join(args.yolo_fusion_root, "per_sample_yolo_fusion_results.json")).get("samples") or []
    fu_by_id = {str(s.get("sample_id")): s for s in fu_samples if isinstance(s, dict) and s.get("sample_id")}

    # YOLO Output bridge
    out_summary = _read_json(os.path.join(args.yolo_output_root, "yolo_output_bridge_summary.json"))
    out_samples = _read_json(os.path.join(args.yolo_output_root, "per_sample_yolo_output_results.json")).get("samples") or []
    out_by_id = {str(s.get("sample_id")): s for s in out_samples if isinstance(s, dict) and s.get("sample_id")}

    sample_ids: List[str] = sorted(set(fb_by_id.keys()))
    n = len(sample_ids)

    per_sample_results: List[Dict[str, Any]] = []

    chain_complete = 0
    stage_complete = {"perception": 0, "scene_task": 0, "fusion": 0, "output": 0}
    schema_valid = {"perception": 0, "scene_task": 0, "fusion": 0, "output": 0}

    yolo_invoked = 0
    detection_available = 0
    yolo_source_preserved_all = 0
    source_attr_all = 0

    allows_exec_false_all = 0
    candidate_only_integrity = 0
    real_tts_false = 0

    leakage_totals = {
        "execute_leakage_count_total": 0,
        "default_on_leakage_count_total": 0,
        "release_retry_reopen_leakage_count_total": 0,
        "side_effects_expansion_count_total": 0,
        "forced_navigation_action_count_total": 0,
        "forbidden_output_semantic_count_total": 0,
    }

    evidence_boundary_ok = {
        "evidence_type_preserved_all_stages": 0,
        "controlled_live_stream_false_all_stages": 0,
        "phone_local_capture_true_all_stages": 0,
        "pending_real_sidewalk_run_true": 0,
    }

    reason_codes_present = 0
    hard_blockers_total = 0

    for sid in sample_ids:
        fb = fb_by_id.get(sid) or {}
        pe = pe_by_id.get(sid)
        st = st_by_id.get(sid)
        fu = fu_by_id.get(sid)
        oo = out_by_id.get(sid)

        bundle_archive_go = bool(fb.get("bundle_validator_recommendation") == "go" and fb.get("archive_validator_recommendation") == "go")

        perception_present = pe is not None
        scene_task_present = st is not None
        fusion_present = fu is not None
        output_present = oo is not None

        if perception_present:
            stage_complete["perception"] += 1
        if scene_task_present:
            stage_complete["scene_task"] += 1
        if fusion_present:
            stage_complete["fusion"] += 1
        if output_present:
            stage_complete["output"] += 1

        perception_schema_ok = _schema_ok_perception(pe) if pe else False
        scene_task_schema_ok = _schema_ok_scene_task(st) if st else False
        fusion_schema_ok = _schema_ok_fusion(fu) if fu else False
        output_schema_ok = _schema_ok_output(oo) if oo else False

        if perception_schema_ok:
            schema_valid["perception"] += 1
        if scene_task_schema_ok:
            schema_valid["scene_task"] += 1
        if fusion_schema_ok:
            schema_valid["fusion"] += 1
        if output_schema_ok:
            schema_valid["output"] += 1

        if pe and pe.get("yolo_invoked") is True:
            yolo_invoked += 1
        if pe and int(pe.get("detection_count") or 0) > 0:
            detection_available += 1

        src_ok = _yolo_source_preserved_all_stages(pe, st, fu, oo)
        if src_ok:
            yolo_source_preserved_all += 1

        # source attribution present all stages (best-effort: fusion+output must have it, scene_task wrapper has it, perception has it implicitly)
        sa_ok = bool(
            (fu or {}).get("source_attribution") is not None
            and (oo or {}).get("source_attribution") is not None
            and isinstance((fu or {}).get("source_attribution"), dict)
            and isinstance((oo or {}).get("source_attribution"), dict)
        )
        if sa_ok:
            source_attr_all += 1

        # allows_execute_now must be false in scene_task candidates, fusion candidate, output candidate
        st_allows_ok = True
        if st and isinstance(st.get("task_candidates"), list):
            st_allows_ok = all((isinstance(c, dict) and c.get("allows_execute_now") is False) for c in st.get("task_candidates"))
        fu_allows_ok = bool((fu or {}).get("fusion_decision_candidate", {}).get("allows_execute_now") is False) if fu else False
        oo_allows_ok = bool((oo or {}).get("navigation_output_candidate", {}).get("allows_execute_now") is False) if oo else False
        if st_allows_ok and fu_allows_ok and oo_allows_ok:
            allows_exec_false_all += 1

        # candidate_only flags exist in wrappers (SceneTask/Fusion/Output)
        cand_only = bool((st or {}).get("candidate_only") is True and (fu or {}).get("candidate_only") is True and (oo or {}).get("candidate_only") is True)
        if cand_only:
            candidate_only_integrity += 1

        # no real TTS
        tts_ok = bool((oo or {}).get("real_tts_invoked") is False and (oo or {}).get("navigation_output_candidate", {}).get("real_tts_invoked") is False) if oo else False
        if tts_ok:
            real_tts_false += 1

        # leakage totals from wrapper fields
        if pe and isinstance(pe.get("metrics"), dict):
            m = pe["metrics"]
            leakage_totals["execute_leakage_count_total"] += int(m.get("execute_leakage_count") or 0)
            leakage_totals["default_on_leakage_count_total"] += int(m.get("default_on_leakage_count") or 0)
            leakage_totals["side_effects_expansion_count_total"] += int(m.get("side_effects_expansion_count") or 0)
        if st:
            leakage_totals["execute_leakage_count_total"] += int(st.get("direct_execute_leakage_count") or 0)
            leakage_totals["release_retry_reopen_leakage_count_total"] += int(st.get("release_retry_reopen_leakage_count") or 0)
            leakage_totals["default_on_leakage_count_total"] += int(st.get("default_on_leakage_count") or 0)
            leakage_totals["forced_navigation_action_count_total"] += int(st.get("forced_navigation_action_count") or 0)
        if fu:
            leakage_totals["execute_leakage_count_total"] += int(fu.get("direct_execute_leakage_count") or 0)
            leakage_totals["release_retry_reopen_leakage_count_total"] += int(fu.get("release_retry_reopen_leakage_count") or 0)
            leakage_totals["default_on_leakage_count_total"] += int(fu.get("default_on_leakage_count") or 0)
            leakage_totals["side_effects_expansion_count_total"] += int(fu.get("side_effects_expansion_count") or 0)
            leakage_totals["forced_navigation_action_count_total"] += int(fu.get("forced_navigation_action_count") or 0)
        if oo:
            leakage_totals["execute_leakage_count_total"] += int(oo.get("direct_execute_leakage_count") or 0)
            leakage_totals["release_retry_reopen_leakage_count_total"] += int(oo.get("release_retry_reopen_leakage_count") or 0)
            leakage_totals["default_on_leakage_count_total"] += int(oo.get("default_on_leakage_count") or 0)
            leakage_totals["side_effects_expansion_count_total"] += int(oo.get("side_effects_expansion_count") or 0)
            leakage_totals["forbidden_output_semantic_count_total"] += int(oo.get("forbidden_output_semantic_count") or 0)
            leakage_totals["forced_navigation_action_count_total"] += int(oo.get("forced_navigation_action_count") or 0)

        # Evidence boundary checks
        evidence_ok = bool(
            (pe or {}).get("evidence_type") == "phone_local_controlled_capture"
            and (st or {}).get("evidence_type_preserved") is True
            and (fu or {}).get("evidence_type_preserved") is True
            and (oo or {}).get("evidence_type_preserved") is True
        )
        cls_ok = bool(
            (pe or {}).get("controlled_live_stream") is False
            and (st or {}).get("controlled_live_stream_false") is True
            and (fu or {}).get("controlled_live_stream_false") is True
            and (oo or {}).get("controlled_live_stream_false") is True
        )
        plc_ok = bool(
            (pe or {}).get("phone_local_capture") is True
            and (st or {}).get("phone_local_capture_true") is True
            and (fu or {}).get("phone_local_capture_true") is True
            and (oo or {}).get("phone_local_capture_true") is True
        )
        pending_ok = bool((pe or {}).get("pending_real_sidewalk_run") is True)

        if evidence_ok:
            evidence_boundary_ok["evidence_type_preserved_all_stages"] += 1
        if cls_ok:
            evidence_boundary_ok["controlled_live_stream_false_all_stages"] += 1
        if plc_ok:
            evidence_boundary_ok["phone_local_capture_true_all_stages"] += 1
        if pending_ok:
            evidence_boundary_ok["pending_real_sidewalk_run_true"] += 1

        if _has_nonempty_list((pe or {}).get("reason_codes")) and _has_nonempty_list((st or {}).get("reason_codes")) and _has_nonempty_list((fu or {}).get("reason_codes")) and _has_nonempty_list((oo or {}).get("reason_codes")):
            reason_codes_present += 1

        hard_blockers: List[str] = []
        soft_followups: List[str] = []

        if not bundle_archive_go:
            hard_blockers.append("field_batch_not_go")
        if not perception_present:
            hard_blockers.append("perception_missing")
        if not scene_task_present:
            hard_blockers.append("scene_task_missing")
        if not fusion_present:
            hard_blockers.append("fusion_missing")
        if not output_present:
            hard_blockers.append("output_missing")

        if perception_present and not perception_schema_ok:
            hard_blockers.append("perception_schema_invalid")
        if scene_task_present and not scene_task_schema_ok:
            hard_blockers.append("scene_task_schema_invalid")
        if fusion_present and not fusion_schema_ok:
            hard_blockers.append("fusion_schema_invalid")
        if output_present and not output_schema_ok:
            hard_blockers.append("output_schema_invalid")

        if not src_ok:
            hard_blockers.append("yolo_detection_source_not_preserved_all_stages")
        if not sa_ok:
            hard_blockers.append("source_attribution_not_present_all_stages")

        if not (st_allows_ok and fu_allows_ok and oo_allows_ok):
            hard_blockers.append("allows_execute_now_not_false_all_stages")
        if not tts_ok:
            hard_blockers.append("real_tts_invoked_not_false")

        if not evidence_ok:
            hard_blockers.append("evidence_type_not_preserved_all_stages")
        if not cls_ok:
            hard_blockers.append("controlled_live_stream_not_false_all_stages")
        if not plc_ok:
            hard_blockers.append("phone_local_capture_not_true_all_stages")
        if not pending_ok:
            hard_blockers.append("pending_real_sidewalk_run_not_true")

        chain_ok = bool(bundle_archive_go and perception_present and scene_task_present and fusion_present and output_present)
        if chain_ok:
            chain_complete += 1

        if hard_blockers:
            hard_blockers_total += len(hard_blockers)

        per_sample_results.append(
            {
                "sample_id": sid,
                "archive_root": fb.get("archive_root"),
                "source_video_path": fb.get("source_video_path"),
                "yolo_invoked": (pe or {}).get("yolo_invoked"),
                "detection_count": (pe or {}).get("detection_count"),
                "detected_classes": (pe or {}).get("detected_classes"),
                "bundle_archive_go": bundle_archive_go,
                "perception_result_present": perception_present,
                "scene_task_result_present": scene_task_present,
                "fusion_result_present": fusion_present,
                "output_result_present": output_present,
                "perception_runtime_mode": (pe or {}).get("perception_runtime_mode"),
                "scene_task_runtime_mode": st_summary.get("scene_task_runtime_mode"),
                "fusion_runtime_mode": fu_summary.get("fusion_runtime_mode"),
                "output_runtime_mode": out_summary.get("output_runtime_mode"),
                "perception_schema_ok": perception_schema_ok,
                "scene_task_schema_ok": scene_task_schema_ok,
                "fusion_schema_ok": fusion_schema_ok,
                "output_schema_ok": output_schema_ok,
                "yolo_detection_source_preserved_all_stages": src_ok,
                "source_attribution_present_all_stages": sa_ok,
                "allows_execute_now_false_all_stages": bool(st_allows_ok and fu_allows_ok and oo_allows_ok),
                "real_tts_invoked_false": tts_ok,
                "candidate_only_integrity": cand_only,
                "evidence_type_preserved_all_stages": evidence_ok,
                "controlled_live_stream_false_all_stages": cls_ok,
                "phone_local_capture_true_all_stages": plc_ok,
                "pending_real_sidewalk_run_true": pending_ok,
                "reason_codes_present": _has_nonempty_list((pe or {}).get("reason_codes")) and _has_nonempty_list((st or {}).get("reason_codes")) and _has_nonempty_list((fu or {}).get("reason_codes")) and _has_nonempty_list((oo or {}).get("reason_codes")),
                "hard_blockers": hard_blockers,
                "soft_followups": soft_followups,
            }
        )

    # Trace consistency report: sample_id set equality across stages
    stage_sets = {
        "field_batch_sample_ids": sorted(fb_by_id.keys()),
        "yolo_perception_sample_ids": sorted(pe_by_id.keys()),
        "yolo_scene_task_sample_ids": sorted(st_by_id.keys()),
        "yolo_fusion_sample_ids": sorted(fu_by_id.keys()),
        "yolo_output_sample_ids": sorted(out_by_id.keys()),
    }
    common: Set[str] = set(stage_sets["field_batch_sample_ids"])
    for k in ("yolo_perception_sample_ids", "yolo_scene_task_sample_ids", "yolo_fusion_sample_ids", "yolo_output_sample_ids"):
        common &= set(stage_sets[k])
    consistency = {
        "tool": "evaluate_yolo_end_to_end_offline_v0",
        "phase": "Phase-ModelPerception-010",
        "generated_at_ms": _now_ms(),
        "stage_sample_id_sets": stage_sets,
        "common_sample_ids": sorted(common),
        "all_stages_same_set": all(
            set(stage_sets["field_batch_sample_ids"]) == set(stage_sets[k])
            for k in ("yolo_perception_sample_ids", "yolo_scene_task_sample_ids", "yolo_fusion_sample_ids", "yolo_output_sample_ids")
        ),
    }

    hard_blockers: List[str] = []
    leakage_sum = sum(int(v) for v in leakage_totals.values())
    if chain_complete != n:
        hard_blockers.append("chain_incomplete")
    if hard_blockers_total != 0:
        hard_blockers.append("per_sample_hard_blockers_present")
    if leakage_sum != 0:
        hard_blockers.append("leakage_detected")
    if yolo_source_preserved_all != n:
        hard_blockers.append("yolo_detection_source_not_preserved_all_stages")
    if source_attr_all != n:
        hard_blockers.append("source_attribution_not_present_all_stages")
    if evidence_boundary_ok["evidence_type_preserved_all_stages"] != n:
        hard_blockers.append("evidence_type_not_preserved_all_stages")
    if evidence_boundary_ok["controlled_live_stream_false_all_stages"] != n:
        hard_blockers.append("controlled_live_stream_not_false_all_stages")
    if evidence_boundary_ok["phone_local_capture_true_all_stages"] != n:
        hard_blockers.append("phone_local_capture_not_true_all_stages")
    if evidence_boundary_ok["pending_real_sidewalk_run_true"] != n:
        hard_blockers.append("pending_real_sidewalk_run_not_true")

    recommendation = "go" if not hard_blockers else "no_go"

    summary = {
        "tool": "evaluate_yolo_end_to_end_offline_v0",
        "phase": "Phase-ModelPerception-010",
        "generated_at_ms": _now_ms(),
        "inputs": {
            "field_batch_root": args.field_batch_root,
            "yolo_perception_root": args.yolo_perception_root,
            "yolo_scene_task_root": args.yolo_scene_task_root,
            "yolo_fusion_root": args.yolo_fusion_root,
            "yolo_output_root": args.yolo_output_root,
        },
        "metrics": {
            "chain_completeness": {
                "sample_chain_complete_rate": _rate(chain_complete, n),
                "yolo_perception_stage_complete_rate": _rate(stage_complete["perception"], n),
                "yolo_scene_task_stage_complete_rate": _rate(stage_complete["scene_task"], n),
                "yolo_fusion_stage_complete_rate": _rate(stage_complete["fusion"], n),
                "yolo_output_stage_complete_rate": _rate(stage_complete["output"], n),
            },
            "schema_integrity": {
                "yolo_perception_schema_valid_rate": _rate(schema_valid["perception"], n),
                "yolo_scene_task_schema_valid_rate": _rate(schema_valid["scene_task"], n),
                "yolo_fusion_schema_valid_rate": _rate(schema_valid["fusion"], n),
                "yolo_output_schema_valid_rate": _rate(schema_valid["output"], n),
            },
            "yolo_source_traceability": {
                "yolo_invoked_rate": _rate(yolo_invoked, n),
                "detection_available_rate": _rate(detection_available, n),
                "yolo_detection_source_preserved_all_stages_rate": _rate(yolo_source_preserved_all, n),
                "source_attribution_present_all_stages_rate": _rate(source_attr_all, n),
            },
            "candidate_only_no_tts_integrity": {
                "allows_execute_now_false_all_stages_rate": _rate(allows_exec_false_all, n),
                "candidate_only_integrity_rate": _rate(candidate_only_integrity, n),
                "real_tts_invoked_false_rate": _rate(real_tts_false, n),
            },
            "safety_boundary": dict(leakage_totals),
            "evidence_boundary": {
                "evidence_type_preserved_all_stages_rate": _rate(evidence_boundary_ok["evidence_type_preserved_all_stages"], n),
                "controlled_live_stream_false_all_stages_rate": _rate(evidence_boundary_ok["controlled_live_stream_false_all_stages"], n),
                "phone_local_capture_true_all_stages_rate": _rate(evidence_boundary_ok["phone_local_capture_true_all_stages"], n),
                "pending_real_sidewalk_run_true_rate": _rate(evidence_boundary_ok["pending_real_sidewalk_run_true"], n),
            },
            "observability": {
                "per_sample_chain_result_ready_rate": 1.0,
                "chain_trace_consistency_ready_rate": 1.0,
                "reason_codes_present_rate": _rate(reason_codes_present, n),
            },
        },
        "recommendation": recommendation,
        "hard_blockers": hard_blockers,
        "soft_followups": ["yolo_shadow_chain_is_candidate_only_not_navigation_validation"],
        "constraints": {
            "controlled_live_stream": False,
            "full_controlled_trial": False,
            "default_path_enabled": False,
            "execution_authority": False,
            "navigation_action_execution": False,
            "real_tts_emission": False,
            "option_expanded": False,
        },
        "outputs": {
            "yolo_e2e_offline_evaluation_summary_json": "yolo_e2e_offline_evaluation_summary.json",
            "per_sample_yolo_chain_results_json": "per_sample_yolo_chain_results.json",
            "yolo_chain_trace_consistency_json": "yolo_chain_trace_consistency.json",
            "evaluation_notes_md": "evaluation_notes.md",
        },
    }

    _write_json(os.path.join(out_root, "yolo_e2e_offline_evaluation_summary.json"), summary)
    _write_json(os.path.join(out_root, "per_sample_yolo_chain_results.json"), {"samples": per_sample_results})
    _write_json(os.path.join(out_root, "yolo_chain_trace_consistency.json"), consistency)
    _write_text(
        os.path.join(out_root, "evaluation_notes.md"),
        "\n".join(
            [
                "# YOLO End-to-End Offline Evaluation (v0)",
                "",
                "- reminder: offline only; candidate-only; no real TTS; no execute/default-on/release/retry/reopen",
                "- do not claim real navigation capability validation",
                "",
            ]
        )
        + "\n",
    )

    print(
        json.dumps(
            {"output_root": out_root, "summary_path": os.path.join(out_root, "yolo_e2e_offline_evaluation_summary.json"), "recommendation": recommendation},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict
from typing import Any, Dict, List

REQUIRED_PROPOSAL_KEYS = {
    "proposal_id",
    "proposal_source",
    "source_detection_id",
    "frame_id",
    "timestamp_ms",
    "image_ref",
    "crop_region",
    "original_bbox",
    "padded_crop_region",
    "source_object",
    "ocr_trigger_type",
    "crop_signature",
    "delta_control_deferred",
}

REQUIRED_RESULT_KEYS = {
    "bridge_result_id",
    "frame_id",
    "timestamp_ms",
    "proposal_id",
    "source_detection_id",
    "ocr_source_policy_id",
    "ocr_provider_selected",
    "fallback_used",
    "fallback_reason",
    "crop_region",
    "raw_text_candidates",
    "raw_text_joined",
    "raw_text_segments",
    "length_policy_applied",
    "reading_direction_candidate",
    "line_order_status",
    "source_attribution",
    "candidate_only",
    "semantic_interpretation_enabled",
    "allows_execute_now",
    "downstream_invocation_count",
    "real_tts_invoked",
    "trace_ref",
    "replay_ref",
    "whitebox_ref",
    "hard_blockers",
    "soft_followups",
    "crop_signature",
    "source_frame_window_id",
    "delta_control_deferred",
}


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _case(name: str, ok: bool, details: Any) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def _valid_candidate_list(cands: Any) -> bool:
    if not isinstance(cands, list):
        return False
    for c in cands:
        if not isinstance(c, dict):
            return False
        if "text" not in c and "normalized_text" not in c:
            return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    root = os.path.abspath(args.output_root)
    summary_p = os.path.join(root, "yolo_ocr_bridge_summary.json")
    per_sample_p = os.path.join(root, "per_sample_yolo_ocr_bridge_results.json")
    proposals_p = os.path.join(root, "ocr_crop_proposals.json")
    trace_p = os.path.join(root, "yolo_ocr_bridge_trace.jsonl")
    replay_p = os.path.join(root, "yolo_ocr_bridge_replay.jsonl")
    whitebox_p = os.path.join(root, "yolo_ocr_bridge_whitebox.jsonl")

    results: List[Dict[str, Any]] = []

    # A
    sample_readable = os.path.isfile(per_sample_p)
    results.append(_case("A_input_samples_readable", sample_readable, per_sample_p))
    if not sample_readable:
        report = {"verdict": "NO_GO", "hard_blockers": ["input_samples_unreadable"], "results": results}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2

    per_sample = _read_json(per_sample_p)
    proposals = _read_json(proposals_p) if os.path.isfile(proposals_p) else []
    summary = _read_json(summary_p) if os.path.isfile(summary_p) else {}

    # B proposal schema
    prop_ok = isinstance(proposals, list) and all(REQUIRED_PROPOSAL_KEYS.issubset(set(p.keys())) for p in proposals if isinstance(p, dict))
    results.append(_case("B_proposal_schema_valid", prop_ok, {"proposal_count": len(proposals)}))

    # C crop clamped
    clamp_ok = True
    clamp_bad = 0
    for p in proposals:
        if not isinstance(p, dict):
            clamp_ok = False
            clamp_bad += 1
            continue
        w = int(p.get("image_width") or 0)
        h = int(p.get("image_height") or 0)
        cr = p.get("crop_region") or {}
        x1, y1, x2, y2 = int(cr.get("x1", -1)), int(cr.get("y1", -1)), int(cr.get("x2", -1)), int(cr.get("y2", -1))
        if not (0 <= x1 < x2 <= w and 0 <= y1 < y2 <= h):
            clamp_ok = False
            clamp_bad += 1
    results.append(_case("C_crop_region_clamped", clamp_ok, {"bad": clamp_bad}))

    # D original bbox preserved
    ob_ok = all(isinstance(p.get("original_bbox"), list) and len(p.get("original_bbox")) == 4 for p in proposals if isinstance(p, dict))
    results.append(_case("D_original_bbox_preserved", ob_ok, {}))

    # E max proposals per frame <=3
    per_frame = defaultdict(int)
    for p in proposals:
        if isinstance(p, dict):
            per_frame[str(p.get("frame_id") or "")] += 1
    e_ok = all(v <= 3 for v in per_frame.values())
    results.append(_case("E_max_proposals_per_frame", e_ok, dict(per_frame)))

    # flatten bridge results
    bridge_results: List[Dict[str, Any]] = []
    for s in per_sample if isinstance(per_sample, list) else []:
        if not isinstance(s, dict):
            continue
        b = (s.get("bridge") or {}).get("bridge_results") if isinstance(s.get("bridge"), dict) else []
        if isinstance(b, list):
            bridge_results.extend([x for x in b if isinstance(x, dict)])

    # F policy used
    f_ok = bool(bridge_results) and all(str(r.get("ocr_source_policy_id") or "") == str(summary.get("ocr_source_policy_id") or "") for r in bridge_results)
    results.append(_case("F_ocr_source_policy_used", f_ok, {"policy": summary.get("ocr_source_policy_id")}))

    # G/H attribution present
    g_ok = all(isinstance((r.get("source_attribution") or {}).get("yolo_source"), dict) for r in bridge_results)
    h_ok = all(isinstance((r.get("source_attribution") or {}).get("ocr_source"), dict) for r in bridge_results)
    results.append(_case("G_yolo_attribution_present", g_ok, {}))
    results.append(_case("H_ocr_attribution_present", h_ok, {}))

    # I raw candidates valid or honest
    i_ok = True
    for r in bridge_results:
        cands = r.get("raw_text_candidates")
        if not _valid_candidate_list(cands):
            i_ok = False
            break
        if not cands:
            blockers = r.get("hard_blockers") or []
            follows = r.get("soft_followups") or []
            if not blockers and not any(str(x).startswith("no_text_detected") for x in follows):
                i_ok = False
                break
    results.append(_case("I_raw_text_schema_or_honest_empty", i_ok, {"result_count": len(bridge_results)}))

    # J-M-N
    results.append(_case("J_candidate_only_true", all(r.get("candidate_only") is True for r in bridge_results), {}))
    results.append(_case("K_semantic_disabled", all(r.get("semantic_interpretation_enabled") is False for r in bridge_results), {}))
    results.append(_case("L_allows_execute_false", all(r.get("allows_execute_now") is False for r in bridge_results), {}))
    results.append(_case("M_real_tts_false", all(r.get("real_tts_invoked") is False for r in bridge_results), {}))
    results.append(_case("N_downstream_count_zero", all(int(r.get("downstream_invocation_count") or 0) == 0 for r in bridge_results), {}))

    # O files present
    o_ok = all(os.path.isfile(p) and os.path.getsize(p) > 0 for p in (trace_p, replay_p, whitebox_p))
    results.append(_case("O_trace_replay_whitebox_present", o_ok, {"trace": trace_p, "replay": replay_p, "whitebox": whitebox_p}))

    # P delta placeholders
    p_ok = True
    for r in bridge_results:
        if "crop_signature" not in r or "source_frame_window_id" not in r or r.get("delta_control_deferred") is not True:
            p_ok = False
            break
        if "text_signature" not in r or "layout_signature" not in r or "previous_result_ref" not in r:
            p_ok = False
            break
    results.append(_case("P_delta_placeholder_present", p_ok, {}))

    # Q no downstream invocation markers
    q_ok = True
    for r in bridge_results:
        if r.get("downstream_invocation_count") not in (0, 0.0):
            q_ok = False
            break
    results.append(_case("Q_no_scenetask_fusion_output_invocation", q_ok, {}))

    all_ok = all(r["ok"] for r in results)
    report = {
        "verifier": "verify_yolo_ocr_offline_bridge_v0",
        "verdict": "GO" if all_ok else "NO_GO",
        "results": results,
        "hard_blockers": [] if all_ok else [r["case"] for r in results if not r["ok"]],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-006 — Evaluate OCR capability boundary dataset v0 (Evaluation Tools).

v0 supports provider=rapidocr only (evaluation-only). No PaddleOCR trial in this phase.

Outputs:
- ocr_capability_boundary_eval_summary.json
- ocr_capability_boundary_sample_matrix.json
- ocr_content_type_performance_report.json
- ocr_quality_perturbation_report.json
- ocr_expected_routing_report.json
- ocr_failure_mode_report.json
- ocr_provider_boundary_map.json
- ocr_capability_boundary_map.json
- ocr_false_text_risk_report.json
- ocr_eligibility_accuracy_report.json
- ocr_recommended_routing_policy_draft.json
- ocr_boundary_quality_vs_accuracy_report.json
- ocr_capability_boundary_trace.jsonl
- ocr_capability_boundary_replay.jsonl
- boundary_eval_notes.md
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.evaluation.ocr.ocr_capability_boundary_router_policy_v0 import build_routing_policy_draft_v0  # noqa: E402
from capabilities.evaluation.ocr.ocr_eval_metrics_v0 import (  # noqa: E402
    compute_cer_v0,
    compute_chinese_char_recall_v0,
    compute_garbled_score_v0,
    normalize_ocr_text_for_eval_v0,
)
from capabilities.evaluation.ocr.ocr_input_image_quality_gate_v0 import assess_ocr_input_image_quality_v0  # noqa: E402
from capabilities.model_ocr.rapidocr_adapter_v0 import RapidOCRAdapterV0  # noqa: E402


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _load_manifest(dataset_root: Path) -> List[Dict[str, Any]]:
    p = dataset_root / "boundary_case_manifest.jsonl"
    if not p.is_file():
        raise SystemExit(f"ERROR: missing boundary_case_manifest.jsonl: {p}")
    rows: List[Dict[str, Any]] = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        rows.append(json.loads(ln))
    return rows


def _quality_fail_reason(q: Dict[str, Any]) -> str:
    gate = str(q.get("image_quality_gate") or "NO_GO")
    if gate == "NO_GO":
        return "input_quality_fail"
    if gate == "CONDITIONAL_GO":
        return "input_quality_risk"
    return "input_quality_ok"


def _failure_mode(pred: str, cer: float, garbled_score: float, pred_empty: bool) -> str:
    if pred_empty:
        return "empty_output"
    if garbled_score >= 0.35:
        return "garbled_output"
    if cer >= 0.35:
        return "high_cer"
    if cer >= 0.15:
        return "medium_cer"
    return "ok"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-root", required=True)
    ap.add_argument("--provider", default="rapidocr", choices=["rapidocr"])
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--limit", type=int, default=0, help="0=no limit")
    args = ap.parse_args()

    dataset_root = _require_abs(args.dataset_root, "--dataset-root")
    out_root = _require_abs(args.output_root, "--output-root")
    out_root.mkdir(parents=True, exist_ok=True)

    rows = _load_manifest(dataset_root)
    if int(args.limit) > 0:
        rows = rows[: int(args.limit)]

    # Routing policy draft (evaluation-only)
    _write_json(out_root / "ocr_recommended_routing_policy_draft.json", build_routing_policy_draft_v0())

    # Provider init
    adapter = RapidOCRAdapterV0()
    ok, err = adapter.is_available()
    if not ok:
        raise SystemExit(f"ERROR: RapidOCR unavailable: {err}")

    trace = out_root / "ocr_capability_boundary_trace.jsonl"
    replay = out_root / "ocr_capability_boundary_replay.jsonl"
    if trace.exists():
        trace.unlink()
    if replay.exists():
        replay.unlink()

    _append_jsonl(trace, {"type": "ocr_capability_boundary_trace_v0", "ts": _now_iso(), "event": "start", "count": len(rows)})

    per: List[Dict[str, Any]] = []
    t0 = time.perf_counter()
    for r in rows:
        cid = str(r.get("case_id") or "")
        sid = cid
        img = str(r.get("image_path") or "")
        truth = str(r.get("ground_truth_text") or "")
        content_type = str(r.get("content_type") or "unknown")
        gen_status = str(r.get("generation_status") or "generated")
        expected_route = str(r.get("expected_ocr_route") or "manual_review")

        # OCR-004 gate (reuse evaluation capability)
        q = assess_ocr_input_image_quality_v0(image_path=img)

        pred = ""
        provider_fail = False
        hard_blockers = []
        if gen_status != "generated":
            provider_fail = False
            hard_blockers = ["manual_sample_required"]
        else:
            env = adapter.recognize_image(image_path=img, frame_id=sid, timestamp_ms=int(time.time() * 1000))
            provider_fail = bool(env.get("provider_status") in ("not_available", "failed")) or bool(env.get("hard_blockers"))
            hard_blockers = env.get("hard_blockers") or []
            pred = str(env.get("raw_text_joined") or "")

        pred_norm = normalize_ocr_text_for_eval_v0(pred)
        pred_empty = not bool(pred_norm)
        cer_d = compute_cer_v0(pred, truth) if truth else {"cer": None, "edit_distance": None, "pred_len": len(pred_norm), "truth_len": 0}
        cer_v = float(cer_d["cer"]) if cer_d.get("cer") is not None else None
        zh_d = compute_chinese_char_recall_v0(pred, truth) if truth else {"chinese_char_recall": None, "truth_chinese_count": 0, "hit_chinese_count": 0}
        gar_d = compute_garbled_score_v0(pred)

        fm = _failure_mode(pred, cer=float(cer_v or 0.0), garbled_score=float(gar_d["garbled_score"]), pred_empty=pred_empty) if truth else "no_ground_truth"
        qf = _quality_fail_reason(q)

        row = {
            "case_id": cid,
            "sample_id": cid,
            "content_type": content_type,
            "generation_status": gen_status,
            "expected_ocr_route": expected_route,
            "image_path": img,
            "ground_truth_text": truth,
            "pred_text": pred,
            "pred_empty": pred_empty,
            "provider": "rapidocr_onnxruntime_v0",
            "provider_fail": provider_fail,
            "hard_blockers": hard_blockers,
            **({"cer": cer_v, "edit_distance": cer_d.get("edit_distance")} if truth else {"cer": None, "edit_distance": None}),
            **zh_d,
            **gar_d,
            "failure_mode": fm,
            "input_quality_gate": q.get("image_quality_gate"),
            "input_quality_reason": q.get("reason"),
            "input_quality_scale_action": q.get("scale_action"),
            "quality_vs_accuracy_bucket": qf,
            "quality_metrics": {
                "blur_score": q.get("blur_score"),
                "contrast_score": q.get("contrast_score"),
                "brightness_status": q.get("brightness_status"),
                "text_scale_status": q.get("text_scale_status"),
                "text_area_ratio": q.get("text_area_ratio"),
                "skew_angle_deg": q.get("skew_angle_deg"),
            },
        }
        per.append(row)
        _append_jsonl(trace, {"type": "ocr_capability_boundary_trace_v0", "ts": _now_iso(), "event": "case_done", "case_id": cid, "content_type": content_type, "failure_mode": fm})

    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    # Reports
    def _avg(xs: List[float]) -> Optional[float]:
        return (sum(xs) / max(1, len(xs))) if xs else None

    # content type performance
    ct_map: Dict[str, Dict[str, Any]] = {}
    for r in per:
        ct = str(r.get("content_type") or "unknown")
        ct_map.setdefault(ct, {"count": 0, "cer": [], "recall": [], "empty": 0, "garbled": [], "provider_fail": 0})
        ct_map[ct]["count"] += 1
        if r.get("cer") is not None:
            ct_map[ct]["cer"].append(float(r["cer"]))
        if r.get("chinese_char_recall") is not None:
            ct_map[ct]["recall"].append(float(r["chinese_char_recall"]))
        if bool(r.get("pred_empty")):
            ct_map[ct]["empty"] += 1
        ct_map[ct]["garbled"].append(float(r.get("garbled_score") or 0.0))
        if bool(r.get("provider_fail")):
            ct_map[ct]["provider_fail"] += 1

    ct_report = {}
    for ct, d in ct_map.items():
        ct_report[ct] = {
            "count": d["count"],
            "avg_cer": _avg(d["cer"]),
            "avg_chinese_recall": _avg(d["recall"]),
            "empty_output_rate": float(d["empty"]) / float(max(1, d["count"])),
            "avg_garbled_score": _avg(d["garbled"]),
            "provider_fail_rate": float(d["provider_fail"]) / float(max(1, d["count"])),
        }

    # perturbation report (lightweight): group by blur/contrast/brightness/size_scale
    pert: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        prof = r.get("quality_profile") or {}
        key = f"size={prof.get('size_scale')}|blur={prof.get('blur')}|contrast={prof.get('contrast')}|brightness={prof.get('brightness')}|skew={prof.get('skew_angle')}|comp={prof.get('compression')}"
        pert.setdefault(key, {"count": 0, "cer": [], "empty": 0})
    # align per list to manifest order by case_id
    per_by_id = {str(x.get("case_id") or ""): x for x in per}
    for r in rows:
        cid = str(r.get("case_id") or "")
        prof = r.get("quality_profile") or {}
        key = f"size={prof.get('size_scale')}|blur={prof.get('blur')}|contrast={prof.get('contrast')}|brightness={prof.get('brightness')}|skew={prof.get('skew_angle')}|comp={prof.get('compression')}"
        d = pert[key]
        d["count"] += 1
        rr = per_by_id.get(cid) or {}
        if rr.get("cer") is not None:
            d["cer"].append(float(rr["cer"]))
        if bool(rr.get("pred_empty")):
            d["empty"] += 1
    pert_report = {k: {"count": v["count"], "avg_cer": _avg(v["cer"]), "empty_rate": float(v["empty"]) / float(max(1, v["count"]))} for k, v in pert.items()}

    # expected routing report (counts only in v0)
    routing_counts: Dict[str, int] = {}
    for r in rows:
        routing_counts[str(r.get("expected_ocr_route") or "unknown")] = int(routing_counts.get(str(r.get("expected_ocr_route") or "unknown"), 0) + 1)

    # failure mode report
    fm_counts: Dict[str, int] = {}
    for r in per:
        fm_counts[str(r.get("failure_mode") or "unknown")] = int(fm_counts.get(str(r.get("failure_mode") or "unknown"), 0) + 1)

    # boundary map (evaluation-only summary)
    boundary_map = {
        "provider": "rapidocr_onnxruntime_v0",
        "content_type_performance": ct_report,
        "notes": "Evaluation-only boundary map; does not change runtime routing.",
    }

    # --- OCR eligibility domain (A/B/C) + distortion prevention rules ---
    # Heuristic A/B/C classification by content_type + quality + observed false-text risk.
    eligible_types = {"zh_plain_text", "en_plain_text", "digits", "mixed_zh_en_digit", "multi_line_text"}
    conditional_types = {"document_text", "product_label", "signboard", "low_quality_text", "zh_traditional_text"}
    non_ocr_types = {"decorative_graphic_non_text", "symbols_and_punctuation", "artistic_text", "stylized_digits", "icon_text_mix", "multi_panel_layout", "vertical_text", "handwritten_style"}

    distortion_prevention_rules = [
        "non_ocr_content_types must not be forced into fact text output",
        "low_quality/unreadable inputs must not be surfaced as confident facts",
        "symbol/glyph candidates must not be concatenated into raw_text",
        "reading_order_uncertain must not produce a single global text as fact",
        "multi_panel layouts must not concatenate across panels without layout grouping",
        "conditional domain outputs must carry uncertainty + preprocess/routing hints",
    ]

    # False Text Risk: for non-ocr content types, how often OCR produced non-empty text.
    non_rows = [r for r in per if str(r.get("content_type") or "") in non_ocr_types and str(r.get("generation_status") or "") == "generated"]
    non_nonempty = [r for r in non_rows if not bool(r.get("pred_empty"))]
    false_text_risk = {
        "definition": "For non_ocr content types (generated only), rate of non-empty OCR output (risk of confident wrong text).",
        "non_ocr_case_count": len(non_rows),
        "non_ocr_nonempty_output_count": len(non_nonempty),
        "false_text_risk_rate": float(len(non_nonempty)) / float(max(1, len(non_rows))) if non_rows else None,
        "examples": [
            {
                "case_id": r.get("case_id"),
                "content_type": r.get("content_type"),
                "pred_text": normalize_ocr_text_for_eval_v0(str(r.get("pred_text") or ""))[:120],
                "input_quality_gate": r.get("input_quality_gate"),
            }
            for r in non_nonempty[:25]
        ],
        "notes": "OCR failure is acceptable; false confident text in non-ocr domain is not.",
    }

    # Eligibility Accuracy (v0 proxy): expected_ocr_route vs observed behavior.
    # - If expected is reject/manual/symbol/glyph/layout, then non-empty OCR output is counted as risky (unless no_ground_truth placeholder).
    # - If expected is rapidocr_primary, then empty_output/high_cer/garbled is counted as miss.
    eligible_rows = [r for r in per if str(r.get("generation_status") or "") == "generated"]
    correct = 0
    incorrect = 0
    details: Dict[str, int] = {"expected_rapidocr_primary_fail": 0, "expected_non_ocr_but_text_emitted": 0}
    for r in eligible_rows:
        exp = str(r.get("expected_ocr_route") or "")
        fm = str(r.get("failure_mode") or "")
        pred_empty = bool(r.get("pred_empty"))
        emitted_text = not pred_empty
        ct = str(r.get("content_type") or "")
        # expected rapidocr: should not be empty/garbled/high cer
        if exp == "rapidocr_primary":
            if fm in ("ok", "medium_cer") and emitted_text:
                correct += 1
            else:
                incorrect += 1
                details["expected_rapidocr_primary_fail"] += 1
        # expected non-ocr branches: emitting text is risky (proxy for eligibility misrouting)
        elif exp in ("visual_symbol_branch", "visual_glyph_branch", "reject_low_quality", "manual_review"):
            if not emitted_text:
                correct += 1
            else:
                incorrect += 1
                details["expected_non_ocr_but_text_emitted"] += 1
        else:
            # layout branch: allow either, but prefer not emitting global text without layout evidence in v0
            # treat as correct (neutral) for merge-only v0
            correct += 1

    eligibility_accuracy = {
        "definition": "Proxy accuracy of eligibility/routing expectations vs observed OCR emission & quality (evaluation-only).",
        "evaluated_case_count": len(eligible_rows),
        "correct_count": correct,
        "incorrect_count": incorrect,
        "eligibility_accuracy": float(correct) / float(max(1, correct + incorrect)),
        "details": details,
        "notes": "This is a proxy metric in v0 (no real router). Used to quantify false-text risk & misrouting pressure.",
    }

    capability_boundary_map = {
        "phase": "Phase-EvaluationTools-OCR-006",
        "provider": "rapidocr_onnxruntime_v0",
        "ocr_eligible_content_types": sorted(list(eligible_types)),
        "conditional_ocr_content_types": sorted(list(conditional_types)),
        "non_ocr_content_types": sorted(list(non_ocr_types)),
        "routing_policy_draft_ref": "ocr_recommended_routing_policy_draft.json",
        "distortion_prevention_rules": distortion_prevention_rules,
        "false_text_risk": {k: false_text_risk[k] for k in ("non_ocr_case_count", "false_text_risk_rate")},
        "eligibility_accuracy": {k: eligibility_accuracy[k] for k in ("evaluated_case_count", "eligibility_accuracy")},
        "notes": "Evaluation-only boundary map; must be manually reviewed before any mainline reference.",
    }

    # quality vs accuracy report (gate bucket)
    qva_counts: Dict[str, int] = {}
    for r in per:
        qva_counts[str(r.get("quality_vs_accuracy_bucket") or "unknown")] = int(qva_counts.get(str(r.get("quality_vs_accuracy_bucket") or "unknown"), 0) + 1)
    qva = {"bucket_counts": qva_counts, "notes": "input_quality_ok/risk/fail vs OCR outputs"}

    summary = {
        "phase": "Phase-EvaluationTools-OCR-006",
        "tool": "evaluate_ocr_capability_boundary_v0",
        "ts": _now_iso(),
        "dataset_root": str(dataset_root),
        "output_root": str(out_root),
        "provider": "rapidocr_onnxruntime_v0",
        "case_count": len(per),
        "elapsed_ms": round(elapsed_ms, 3),
        "hard_audit": {
            "runtime_integration": False,
            "whitebox_integration": False,
            "mainline_side_effect": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
            "tts_invoked": False,
            "qwen_invoked": False,
        },
    }

    _write_json(out_root / "ocr_capability_boundary_eval_summary.json", summary)
    _write_json(out_root / "ocr_capability_boundary_sample_matrix.json", per)
    _write_json(out_root / "ocr_content_type_performance_report.json", ct_report)
    _write_json(out_root / "ocr_quality_perturbation_report.json", pert_report)
    _write_json(out_root / "ocr_expected_routing_report.json", {"expected_routing_counts": routing_counts})
    _write_json(out_root / "ocr_failure_mode_report.json", {"failure_mode_counts": fm_counts})
    _write_json(out_root / "ocr_provider_boundary_map.json", boundary_map)
    _write_json(out_root / "ocr_capability_boundary_map.json", capability_boundary_map)
    _write_json(out_root / "ocr_false_text_risk_report.json", false_text_risk)
    _write_json(out_root / "ocr_eligibility_accuracy_report.json", eligibility_accuracy)
    _write_json(out_root / "ocr_boundary_quality_vs_accuracy_report.json", qva)

    _append_jsonl(replay, {"type": "ocr_capability_boundary_replay_v0", "ts": _now_iso(), "hint": "Review content_type and perturbation reports."})

    notes = "\n".join(
        [
            "# OCR capability boundary eval v0 (Evaluation Tools)",
            "",
            f"- **dataset_root:** `{summary['dataset_root']}`",
            f"- **output_root:** `{summary['output_root']}`",
            f"- **provider:** `{summary['provider']}`",
            f"- **case_count:** `{summary['case_count']}`",
            "",
            "## Boundary",
            "",
            "- Evaluation-only; no runtime/whitebox integration; no mainline side effects.",
            "- This phase does not run PaddleOCR trials.",
            "",
        ]
    )
    (out_root / "boundary_eval_notes.md").write_text(notes + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out_root), "case_count": len(per)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import shutil
import sys
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _now_stamp() -> str:
    return _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _merge_bridge_results_from_per_sample(per_sample: Any) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if not isinstance(per_sample, list):
        return out
    for s in per_sample:
        if not isinstance(s, dict):
            continue
        bridge = s.get("bridge")
        if not isinstance(bridge, dict):
            continue
        brs = bridge.get("bridge_results")
        if isinstance(brs, list):
            out.extend([x for x in brs if isinstance(x, dict)])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--yolo-roots",
        required=True,
        help="Comma-separated YOLO offline output roots (evidence roots).",
    )
    ap.add_argument("--output-root", default=None, help="Expansion output root (default: logs/yolo_ocr_bridge_evidence_expansion_005_<timestamp>).")
    ap.add_argument("--ocr-source-policy", default="ocr_default_offline_raw_text_source_policy_v0")

    # Targets (user provided constraints)
    ap.add_argument("--target-parsed-samples", type=int, default=3)
    ap.add_argument("--target-parsed-detections", type=int, default=5)
    ap.add_argument("--target-proposal-count", type=int, default=3)
    ap.add_argument("--target-bridge-result-count", type=int, default=3)

    # Evidence generation tuning
    ap.add_argument("--max-bridge-samples", type=int, default=6, help="Upper bound for evaluate tool samples per root-run attempt.")
    ap.add_argument("--max-detections-per-frame", type=int, default=3)
    ap.add_argument("--min-ocr-worthy-detections", type=int, default=0, help="Optional parse gating per root (audit only).")
    args = ap.parse_args()

    roots = [r.strip() for r in str(args.yolo_roots).split(",") if r.strip()]
    if not roots:
        raise SystemExit("yolo_roots_empty")

    if args.output_root:
        out_root = os.path.abspath(args.output_root)
    else:
        out_root = os.path.abspath(os.path.join("logs", f"yolo_ocr_bridge_evidence_expansion_005_{_now_stamp()}"))
    os.makedirs(out_root, exist_ok=True)

    # Use evaluate tool's built-in multi-root aggregation (do not change bridge schema).
    # We keep everything inside out_root so existing evidence-run verifier can run.
    eval_cmd = [
        sys.executable,
        os.path.join(REPO_ROOT, "tools", "evaluate_yolo_ocr_offline_bridge_v0.py"),
        "--yolo-root",
        ",".join(roots),
        "--output-root",
        out_root,
        "--ocr-source-policy",
        args.ocr_source_policy,
        "--max-bridge-samples",
        str(int(args.max_bridge_samples)),
        "--max-detections-per-frame",
        str(int(args.max_detections_per_frame)),
        "--min-ocr-worthy-detections",
        str(int(args.min_ocr_worthy_detections)),
    ]

    # Use subprocess so this tool remains self-contained.
    import subprocess

    proc = subprocess.run(eval_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    rc = proc.returncode
    if rc != 0:
        # Still write notes for honest failure.
        with open(os.path.join(out_root, "expansion_notes.md"), "w", encoding="utf-8") as nf:
            nf.write(
                "\n".join(
                    [
                        "# YOLO × OCR Evidence Expansion Notes v0",
                        "",
                        "- evaluate_yolo_ocr_offline_bridge_v0 failed",
                        f"- returncode: {rc}",
                        f"- stderr_head: {(proc.stderr or '').strip()[:500]}",
                    ]
                )
            )
        return 2

    # Load generated outputs.
    parse_report_p = os.path.join(out_root, "yolo_root_parse_report.json")
    per_sample_p = os.path.join(out_root, "per_sample_yolo_ocr_bridge_results.json")
    proposals_p = os.path.join(out_root, "ocr_crop_proposals.json")
    summary_p = os.path.join(out_root, "yolo_ocr_bridge_summary.json")

    parse_report = _read_json(parse_report_p) if os.path.isfile(parse_report_p) else {}
    per_sample = _read_json(per_sample_p) if os.path.isfile(per_sample_p) else []
    proposals = _read_json(proposals_p) if os.path.isfile(proposals_p) else []
    summary = _read_json(summary_p) if os.path.isfile(summary_p) else {}

    root_parse_matrix = parse_report.get("root_parse_matrix") or []
    parsed_sample_count = int(parse_report.get("parsed_sample_count") or 0)
    parsed_detection_count = int(parse_report.get("parsed_detection_count") or 0)
    ocr_worthy_detection_count = int(parse_report.get("ocr_worthy_detection_count") or 0)

    # Selected roots are those that produced any parsed detections.
    selected_roots: List[str] = []
    for row in root_parse_matrix:
        if int(row.get("parsed_detection_count") or 0) > 0 and row.get("yolo_root") not in selected_roots:
            selected_roots.append(row.get("yolo_root"))

    bridge_results = _merge_bridge_results_from_per_sample(per_sample)

    # Class coverage from kept proposals.
    class_coverage: Dict[str, int] = defaultdict(int)
    if isinstance(proposals, list):
        for p in proposals:
            if not isinstance(p, dict):
                continue
            so = p.get("source_object") or {}
            cls = str(so.get("class_name") or "").strip()
            if cls:
                class_coverage[cls] += 1

    example_ocr_classes = ["sign", "screen", "storefront", "board", "label"]
    covered_classes = sorted([c for c in class_coverage.keys() if c in set(example_ocr_classes)])

    proposals_count = len(proposals) if isinstance(proposals, list) else 0
    bridge_results_count = len(bridge_results)

    meets_targets = (
        parsed_sample_count >= int(args.target_parsed_samples)
        and parsed_detection_count >= int(args.target_parsed_detections)
        and proposals_count >= int(args.target_proposal_count)
        and bridge_results_count >= int(args.target_bridge_result_count)
    )

    # Honest insufficient logic:
    any_root_produced_det = any(int(row.get("parsed_detection_count") or 0) > 0 for row in root_parse_matrix if isinstance(row, dict))
    if meets_targets:
        verdict_recommendation = "GO"
    else:
        verdict_recommendation = "CONDITIONAL_GO" if any_root_produced_det else "NO_GO"

    evidence_expansion_summary = {
        "phase": "Phase-ModelOCR-YOLO-Bridge-005",
        "tool": "run_yolo_ocr_bridge_evidence_expansion_v0.py",
        "timestamp": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "targets": {
            "parsed_sample_count": int(args.target_parsed_samples),
            "parsed_detection_count": int(args.target_parsed_detections),
            "proposal_generated_count": int(args.target_proposal_count),
            "bridge_result_generated_count": int(args.target_bridge_result_count),
        },
        "final_counts": {
            "parsed_sample_count": parsed_sample_count,
            "parsed_detection_count": parsed_detection_count,
            "ocr_worthy_detection_count": ocr_worthy_detection_count,
            "proposal_generated_count": proposals_count,
            "bridge_result_generated_count": bridge_results_count,
        },
        "selected_roots": selected_roots,
        "root_parse_matrix_size": len(root_parse_matrix) if isinstance(root_parse_matrix, list) else 0,
        "ocr_provider_selected_set": summary.get("ocr_provider_selected_set"),
        "fallback_used_count": summary.get("fallback_used_count"),
        "class_coverage": dict(class_coverage),
        "covered_example_ocr_classes": covered_classes,
        "meets_targets": meets_targets,
        "verdict_recommendation": verdict_recommendation,
        "honest_insufficient_reason": "insufficient_real_ocr_worthy_detections" if not meets_targets and any_root_produced_det else ("no_root_parsed_detections" if not meets_targets else None),
    }

    _write_json(os.path.join(out_root, "evidence_expansion_summary.json"), evidence_expansion_summary)
    _write_json(os.path.join(out_root, "root_parse_matrix.json"), root_parse_matrix)
    _write_json(os.path.join(out_root, "selected_roots.json"), selected_roots)
    _write_json(os.path.join(out_root, "expanded_bridge_results.json"), bridge_results)
    _write_json(os.path.join(out_root, "expanded_ocr_crop_proposals.json"), proposals)

    # Expand notes.
    with open(os.path.join(out_root, "expansion_notes.md"), "w", encoding="utf-8") as nf:
        nf.write(
            "\n".join(
                [
                    "# YOLO × OCR Evidence Expansion Notes v0",
                    "",
                    f"- attempted_yolo_roots: {roots}",
                    f"- selected_roots: {selected_roots}",
                    "",
                    "## final counts",
                    f"- parsed_sample_count: {parsed_sample_count}",
                    f"- parsed_detection_count: {parsed_detection_count}",
                    f"- proposal_generated_count: {proposals_count}",
                    f"- bridge_result_generated_count: {bridge_results_count}",
                    "",
                    "## covered example classes",
                    f"- {covered_classes}",
                    "",
                    "## honest insufficient",
                    f"- {evidence_expansion_summary.get('honest_insufficient_reason')}",
                ]
            )
        )

    # Ensure trace/replay/whitebox are present already (generated by evaluate tool).
    # Also keep standard artifacts for base verifier:
    # yolo_ocr_bridge_summary.json, yolo_root_parse_report.json, per_sample_yolo_ocr_bridge_results.json, ocr_crop_proposals.json
    _write_json(os.path.join(out_root, "verification_result.json"), {"note": "run verify_yolo_ocr_bridge_evidence_expansion_v0.py for final verdict"})

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


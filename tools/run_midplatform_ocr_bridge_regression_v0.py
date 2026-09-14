#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in __import__("sys").path:
    __import__("sys").path.insert(0, REPO_ROOT)


def _resolve(p: str) -> str:
    return p if os.path.isabs(p) else os.path.abspath(os.path.join(REPO_ROOT, p))


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _read_jsonl_count(path: str) -> int:
    if not os.path.isfile(path):
        return 0
    c = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                c += 1
    return c


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _scan_for_forbidden_nonnull(obj: Any, forbidden_keys: List[str]) -> Dict[str, int]:
    counts = {k: 0 for k in forbidden_keys}

    def rec(x: Any) -> None:
        if isinstance(x, dict):
            for k, v in x.items():
                if isinstance(k, str) and k in forbidden_keys and v is not None:
                    counts[k] += 1
                rec(v)
        elif isinstance(x, list):
            for it in x:
                rec(it)

    rec(obj)
    return counts


def _required_files() -> List[str]:
    return [
        "midplatform_ocr_bridge_summary.json",
        "midplatform_ocr_evidence_inputs.json",
        "scene_delta_control_results.json",
        "filter_results.json",
        "midplatform_text_extraction_candidates.json",
        "world_context_evidence_candidates.json",
        "ambient_context_candidates.json",
        "midplatform_ocr_bridge_trace.jsonl",
        "midplatform_ocr_bridge_replay.jsonl",
        "midplatform_ocr_bridge_whitebox.jsonl",
        "evaluation_notes.md",
    ]


def _root_probe(root: str) -> Dict[str, Any]:
    root_abs = _resolve(root)
    info: Dict[str, Any] = {
        "root": root,
        "root_abs": root_abs,
        "readable": os.path.isdir(root_abs),
        "required_files_missing": [],
        "verification_result_present": False,
        "verification_verdict": None,
        "summary": None,
        "counts": {},
        "boundary_scan": {},
        "trace_replay_whitebox": {},
        "notes": [],
    }
    if not info["readable"]:
        info["notes"].append("root_not_readable")
        return info

    missing = [f for f in _required_files() if not os.path.isfile(os.path.join(root_abs, f))]
    info["required_files_missing"] = missing

    vr_path = os.path.join(root_abs, "verification_result.json")
    if os.path.isfile(vr_path):
        info["verification_result_present"] = True
        try:
            vr = _read_json(vr_path)
            info["verification_verdict"] = vr.get("verdict")
        except Exception:
            info["verification_verdict"] = "unreadable"
            info["notes"].append("verification_result_unreadable")

    # Load primary outputs (best-effort; regression should be honest)
    def load_json_opt(fn: str) -> Any:
        p = os.path.join(root_abs, fn)
        if not os.path.isfile(p):
            return None
        try:
            return _read_json(p)
        except Exception:
            info["notes"].append(f"unreadable_json:{fn}")
            return None

    summary = load_json_opt("midplatform_ocr_bridge_summary.json")
    evidence_inputs = load_json_opt("midplatform_ocr_evidence_inputs.json")
    delta_results = load_json_opt("scene_delta_control_results.json")
    filter_results = load_json_opt("filter_results.json")
    text_candidates = load_json_opt("midplatform_text_extraction_candidates.json")
    world_candidates = load_json_opt("world_context_evidence_candidates.json")
    ambient_candidates = load_json_opt("ambient_context_candidates.json")

    info["summary"] = summary if isinstance(summary, dict) else None

    info["counts"] = {
        "evidence_inputs": len(evidence_inputs) if isinstance(evidence_inputs, list) else None,
        "delta_results": len(delta_results) if isinstance(delta_results, list) else None,
        "filter_results": len(filter_results) if isinstance(filter_results, list) else None,
        "text_candidates": len(text_candidates) if isinstance(text_candidates, list) else None,
        "world_candidates": len(world_candidates) if isinstance(world_candidates, list) else None,
        "ambient_candidates": len(ambient_candidates) if isinstance(ambient_candidates, list) else None,
    }

    # Trace/replay/whitebox line counts (must be non-empty)
    trace_count = _read_jsonl_count(os.path.join(root_abs, "midplatform_ocr_bridge_trace.jsonl"))
    replay_count = _read_jsonl_count(os.path.join(root_abs, "midplatform_ocr_bridge_replay.jsonl"))
    whitebox_count = _read_jsonl_count(os.path.join(root_abs, "midplatform_ocr_bridge_whitebox.jsonl"))
    info["trace_replay_whitebox"] = {"trace": trace_count, "replay": replay_count, "whitebox": whitebox_count}

    # Boundary scan: forbid semantic_summary / navigation_action anywhere
    forbidden = ["semantic_summary", "navigation_action"]
    boundary_obj: Dict[str, Any] = {
        "evidence_inputs": evidence_inputs,
        "text_candidates": text_candidates,
        "world_candidates": world_candidates,
        "ambient_candidates": ambient_candidates,
        "filter_results": filter_results,
        "summary": summary,
    }
    info["boundary_scan"] = _scan_for_forbidden_nonnull(boundary_obj, forbidden)

    # Low-value uncertainty fields presence (best-effort; only counts keys)
    low_value_keys = [
        "readability_status",
        "meaning_status",
        "requires_better_frame",
        "uncertainty_reason",
        "allowed_for_user_requested_readout",
    ]
    lv_present: Dict[str, int] = {k: 0 for k in low_value_keys}
    if isinstance(filter_results, list):
        for fr in filter_results:
            if not isinstance(fr, dict):
                continue
            for k in low_value_keys:
                if k in fr and fr.get(k) is not None:
                    lv_present[k] += 1
    info["counts"]["low_value_fields_nonnull_in_filter_results"] = lv_present

    # Blocked evidence retention check (count blocked with missing retained_evidence_ref)
    retained_missing = 0
    blocked_total = 0
    if isinstance(filter_results, list):
        for fr in filter_results:
            if not isinstance(fr, dict):
                continue
            if fr.get("block_applied"):
                blocked_total += 1
                if not fr.get("retained_evidence_ref"):
                    retained_missing += 1
    info["counts"]["blocked_total"] = blocked_total
    info["counts"]["blocked_missing_retained_evidence_ref"] = retained_missing

    return info


def _matrix_from_probes(probes: List[Dict[str, Any]]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for p in probes:
        rows.append(
            {
                "root": p.get("root"),
                "readable": p.get("readable"),
                "verification_verdict": p.get("verification_verdict"),
                "missing_required_files_count": len(p.get("required_files_missing") or []),
                "evidence_inputs": (p.get("counts") or {}).get("evidence_inputs"),
                "delta_results": (p.get("counts") or {}).get("delta_results"),
                "filter_results": (p.get("counts") or {}).get("filter_results"),
                "text_candidates": (p.get("counts") or {}).get("text_candidates"),
                "world_candidates": (p.get("counts") or {}).get("world_candidates"),
                "ambient_candidates": (p.get("counts") or {}).get("ambient_candidates"),
                "trace_lines": (p.get("trace_replay_whitebox") or {}).get("trace"),
                "replay_lines": (p.get("trace_replay_whitebox") or {}).get("replay"),
                "whitebox_lines": (p.get("trace_replay_whitebox") or {}).get("whitebox"),
                "forbidden_nonnull": p.get("boundary_scan"),
                "blocked_total": (p.get("counts") or {}).get("blocked_total"),
                "blocked_missing_retained_evidence_ref": (p.get("counts") or {}).get("blocked_missing_retained_evidence_ref"),
                "low_value_fields_nonnull_in_filter_results": (p.get("counts") or {}).get("low_value_fields_nonnull_in_filter_results"),
            }
        )
    return {"rows": rows}


def _boundary_summary(probes: List[Dict[str, Any]]) -> Dict[str, Any]:
    forbidden_keys = ["semantic_summary", "navigation_action"]
    totals = {k: 0 for k in forbidden_keys}
    for p in probes:
        scan = p.get("boundary_scan") or {}
        for k in forbidden_keys:
            totals[k] += int(scan.get(k) or 0)
    return {"forbidden_nonnull_totals": totals}


def _trw_summary(probes: List[Dict[str, Any]]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for p in probes:
        trw = p.get("trace_replay_whitebox") or {}
        rows.append({"root": p.get("root"), "trace": trw.get("trace"), "replay": trw.get("replay"), "whitebox": trw.get("whitebox")})
    return {"rows": rows}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", nargs="+", required=True, help="Multiple Bridge-002/002-Fix output roots (read-only).")
    ap.add_argument("--output-root", required=True, help="Where to write regression aggregate outputs.")
    args = ap.parse_args()

    roots = [str(r) for r in args.roots]
    out_root = _resolve(args.output_root)
    os.makedirs(out_root, exist_ok=True)

    probes: List[Dict[str, Any]] = []
    hard_blockers: List[str] = []
    for r in roots:
        p = _root_probe(r)
        probes.append(p)
        if not p.get("readable"):
            hard_blockers.append(f"root_not_readable:{r}")
        missing = p.get("required_files_missing") or []
        if missing:
            hard_blockers.append(f"missing_required_files:{r}:{len(missing)}")

    matrix = _matrix_from_probes(probes)
    boundary = _boundary_summary(probes)
    trw = _trw_summary(probes)

    # Candidate matrix: presence only (counts can fluctuate; closure allows it)
    candidate_rows: List[Dict[str, Any]] = []
    for p in probes:
        c = p.get("counts") or {}
        candidate_rows.append(
            {
                "root": p.get("root"),
                "text_candidates": c.get("text_candidates"),
                "world_candidates": c.get("world_candidates"),
                "ambient_candidates": c.get("ambient_candidates"),
                "allowed_fluctuation": True,
            }
        )
    candidate_matrix = {"rows": candidate_rows}

    input_root_matrix = {
        "roots": roots,
        "root_count": len(roots),
        "generated_at_ms": int(time.time() * 1000),
        "notes": ["read_only_regression", "counts_allowed_to_fluctuate", "boundary_must_not_fluctuate"],
    }

    summary = {
        "phase": "Phase-ModelOCR-MidPlatform-Bridge-003",
        "tool": "run_midplatform_ocr_bridge_regression_v0.py",
        "roots": roots,
        "root_count": len(roots),
        "hard_blockers": hard_blockers,
        "verdict_hint": "GO" if not hard_blockers else "NO_GO",
        "boundary_forbidden_nonnull_totals": boundary.get("forbidden_nonnull_totals"),
        "trace_replay_whitebox_all_nonempty": all((p.get("trace_replay_whitebox") or {}).get(k, 0) > 0 for p in probes for k in ("trace", "replay", "whitebox")),
    }

    _write_json(os.path.join(out_root, "midplatform_ocr_bridge_regression_summary.json"), summary)
    _write_json(os.path.join(out_root, "midplatform_ocr_bridge_regression_matrix.json"), matrix)
    _write_json(os.path.join(out_root, "midplatform_ocr_bridge_input_root_matrix.json"), input_root_matrix)
    _write_json(os.path.join(out_root, "midplatform_ocr_bridge_candidate_matrix.json"), candidate_matrix)
    _write_json(os.path.join(out_root, "midplatform_ocr_bridge_boundary_summary.json"), boundary)
    _write_json(os.path.join(out_root, "midplatform_ocr_bridge_trace_replay_whitebox_summary.json"), trw)

    # Markdown notes
    notes_lines: List[str] = []
    notes_lines.append("# MidPlatform OCR Bridge Regression Notes (Phase-ModelOCR-MidPlatform-Bridge-003)\n")
    notes_lines.append(f"- generated_at_ms: {input_root_matrix['generated_at_ms']}\n")
    notes_lines.append(f"- roots: {len(roots)}\n")
    if hard_blockers:
        notes_lines.append("## Hard blockers\n")
        for hb in hard_blockers:
            notes_lines.append(f"- {hb}\n")
    else:
        notes_lines.append("## Hard blockers\n- none\n")
    notes_lines.append("\n## Boundary forbidden non-null totals\n")
    for k, v in (boundary.get("forbidden_nonnull_totals") or {}).items():
        notes_lines.append(f"- {k}: {v}\n")
    with open(os.path.join(out_root, "regression_notes.md"), "w", encoding="utf-8") as f:
        f.write("".join(notes_lines))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-012-Fix — Batch OCR raw_text (RapidOCR mainline).

Default sample scope: ocr_1 … ocr_12 only (regex on basename).
Excludes: ocr_stage2_*, *_metadata*, hidden files, non-images.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

INCLUDE_REGEX_STR = r"^ocr_([1-9]|1[0-2])\.(png|jpg|jpeg|webp)$"
INCLUDE_RE = re.compile(INCLUDE_REGEX_STR, re.IGNORECASE)

EXPECTED_COUNT = 12
EXPECTED_INDICES = list(range(1, 13))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute")
    return pp.resolve()


def _run(cmd: List[str]) -> int:
    import subprocess

    return subprocess.run(cmd, check=False).returncode


def _ocr_index_from_name(name: str) -> Optional[int]:
    m = INCLUDE_RE.match(name)
    if not m:
        return None
    return int(m.group(1))


def _classify_directory(
    sample_dir: Path,
) -> Tuple[Dict[int, Path], List[Dict[str, str]], bool]:
    """
    Returns:
      unique_by_index: at most one path per index 1..12
      excluded: list of {path, reason}
      has_duplicate_index: True if two files mapped to same ocr_N
    """
    excluded: List[Dict[str, str]] = []
    buckets: Dict[int, List[Path]] = {i: [] for i in EXPECTED_INDICES}

    for p in sorted(sample_dir.iterdir(), key=lambda x: x.name):
        name = p.name
        if not p.is_file():
            excluded.append({"path": name, "reason": "not_a_file"})
            continue
        if name.startswith("."):
            excluded.append({"path": name, "reason": "hidden_file"})
            continue
        nlow = name.lower()
        if "metadata" in nlow:
            excluded.append({"path": name, "reason": "metadata_pattern"})
            continue
        if name.startswith("ocr_stage2"):
            excluded.append({"path": name, "reason": "ocr_stage2_excluded"})
            continue
        idx = _ocr_index_from_name(name)
        if idx is None:
            if nlow.endswith((".png", ".jpg", ".jpeg", ".webp")):
                excluded.append({"path": name, "reason": "not_oc_1_to_12_regex"})
            else:
                excluded.append({"path": name, "reason": "unsupported_extension"})
            continue
        buckets[idx].append(p)

    has_duplicate_index = False
    unique_by_index: Dict[int, Path] = {}
    for idx in EXPECTED_INDICES:
        lst = sorted(buckets[idx], key=lambda x: x.name)
        if len(lst) > 1:
            has_duplicate_index = True
            unique_by_index[idx] = lst[0]
            for extra in lst[1:]:
                excluded.append({"path": extra.name, "reason": f"duplicate_ocr_index_{idx}"})
        elif len(lst) == 1:
            unique_by_index[idx] = lst[0]

    return unique_by_index, excluded, has_duplicate_index


def _compute_batch_verdict(
    *,
    actual_count: int,
    expected_full: bool,
    duplicate_index: bool,
    rows: List[Dict[str, Any]],
) -> Tuple[str, List[str]]:
    blockers: List[str] = []
    if duplicate_index:
        blockers.append("duplicate_ocr_index")
    if actual_count != EXPECTED_COUNT or not expected_full:
        blockers.append("sample_count_not_12")
        return ("NO_GO", blockers)

    providers_ok = all("rapidocr" in str(r.get("provider_selected") or "").lower() for r in rows)
    macos_pick = any("macos_vision" in str(r.get("provider_selected") or "").lower() for r in rows)
    if macos_pick:
        return ("NO_GO", blockers + ["macos_vision_selected"])
    if not providers_ok:
        return ("NO_GO", blockers + ["non_rapidocr_provider"])

    for r in rows:
        wp = Path(str(r.get("trial_output_root") or "")) / "ocr_stage2_controlled_provider_whitebox.jsonl"
        if not wp.is_file():
            continue
        try:
            line = wp.read_text(encoding="utf-8").strip().splitlines()[-1]
            wb = json.loads(line)
            ha = wb.get("hard_audit") or {}
            if ha.get("network_request_invoked"):
                return ("NO_GO", blockers + ["network_request"])
            if ha.get("semantic_interpretation_enabled"):
                return ("NO_GO", blockers + ["semantic_enabled"])
            if ha.get("midplatform_invoked"):
                return ("NO_GO", blockers + ["midplatform"])
        except Exception:
            continue

    any_empty = any(int(r.get("raw_text_len") or -1) <= 0 for r in rows)
    any_not_go = any(r.get("post_trial_recommendation") != "GO_next_window" for r in rows)
    if any_empty or any_not_go:
        return ("CONDITIONAL_GO", [])

    return ("GO", [])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample-dir", required=True)
    ap.add_argument(
        "--sample-glob",
        default=None,
        help="Optional pre-filter glob; inclusion still enforced by ocr_[1-9]|1[0-2] regex.",
    )
    ap.add_argument("--provider", default="rapidocr", help="ignored")
    ap.add_argument("--static-config-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    sample_dir = _require_abs(args.sample_dir, "--sample-dir")
    out_root = _require_abs(args.output_root, "--output-root")
    static_root = _require_abs(args.static_config_root, "--static-config-root")
    out_root.mkdir(parents=True, exist_ok=True)

    unique_by_index, excluded_records, duplicate_index = _classify_directory(sample_dir)

    if args.sample_glob:
        globs = {p.resolve() for p in sample_dir.glob(args.sample_glob) if p.is_file()}
        for idx in list(unique_by_index.keys()):
            if unique_by_index[idx].resolve() not in globs:
                excluded_records.append({"path": unique_by_index[idx].name, "reason": "filtered_out_by_sample_glob"})
                del unique_by_index[idx]

    ordered_paths: List[Path] = [unique_by_index[i] for i in EXPECTED_INDICES if i in unique_by_index]
    actual_count = len(ordered_paths)
    missing_indices = [i for i in EXPECTED_INDICES if i not in unique_by_index]
    expected_full = len(missing_indices) == 0 and actual_count == EXPECTED_COUNT

    included_samples = [unique_by_index[i].name for i in EXPECTED_INDICES if i in unique_by_index]

    sample_filter: Dict[str, Any] = {
        "include_regex": INCLUDE_REGEX_STR,
        "excluded_patterns": ["ocr_stage2_*", "*metadata*", "hidden_files", "outside_ocr_1_to_12"],
        "expected_count": EXPECTED_COUNT,
        "actual_count": actual_count,
        "missing_indices": missing_indices,
        "optional_sample_glob": args.sample_glob,
    }

    per_dir = out_root / "per_sample"
    per_dir.mkdir(parents=True, exist_ok=True)

    rows: List[Dict[str, Any]] = []
    py = sys.executable
    tool_prepare = str(Path(REPO_ROOT) / "tools" / "prepare_ocr_stage2_provider_approval_gate_v0.py")
    tool_run = str(Path(REPO_ROOT) / "tools" / "run_ocr_stage2_controlled_provider_trial_v0.py")

    for img in ordered_paths:
        stem = img.stem
        sha_short = ""
        try:
            import hashlib

            h = hashlib.sha256()
            with open(img, "rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    h.update(chunk)
            sha_short = h.hexdigest()[:12]
        except Exception:
            sha_short = "unknown"

        d010 = per_dir / f"010_{stem}_{sha_short}"
        d011 = per_dir / f"011_{stem}_{sha_short}"
        d010.mkdir(parents=True, exist_ok=True)
        d011.mkdir(parents=True, exist_ok=True)

        rc0 = _run(
            [
                py,
                tool_prepare,
                "--static-config-root",
                str(static_root),
                "--input-image",
                str(img.resolve()),
                "--output-root",
                str(d010),
            ]
        )
        rc1 = _run(
            [
                py,
                tool_run,
                "--approval-root",
                str(d010),
                "--output-root",
                str(d011),
            ]
        )

        raw_len = -1
        provider = ""
        rec = ""
        hard_audit: Dict[str, Any] = {}
        try:
            cand_p = d011 / "ocr_stage2_raw_text_candidate.json"
            if cand_p.is_file():
                c = json.loads(cand_p.read_text(encoding="utf-8"))
                raw_len = len(str(c.get("raw_text") or "").strip())
            sel_p = d011 / "ocr_stage2_provider_selection.json"
            if sel_p.is_file():
                s = json.loads(sel_p.read_text(encoding="utf-8"))
                provider = str(s.get("provider_selected") or "")
            post_p = d011 / "ocr_stage2_post_trial_report.json"
            if post_p.is_file():
                pr = json.loads(post_p.read_text(encoding="utf-8"))
                rec = str(pr.get("post_trial_recommendation") or "")
            wp = d011 / "ocr_stage2_controlled_provider_whitebox.jsonl"
            if wp.is_file() and wp.read_text(encoding="utf-8").strip():
                lines = wp.read_text(encoding="utf-8").strip().splitlines()
                wb = json.loads(lines[-1])
                hard_audit = wb.get("hard_audit") or {}
        except Exception:
            pass

        rows.append(
            {
                "image": img.name,
                "ocr_index": _ocr_index_from_name(img.name),
                "sha256_prefix": sha_short,
                "prepare_rc": rc0,
                "trial_rc": rc1,
                "provider_selected": provider,
                "raw_text_len": raw_len,
                "post_trial_recommendation": rec,
                "approval_root": str(d010),
                "trial_output_root": str(d011),
                "hard_audit": hard_audit,
            }
        )

    fieldnames = [
        "image",
        "ocr_index",
        "sha256_prefix",
        "prepare_rc",
        "trial_rc",
        "provider_selected",
        "raw_text_len",
        "post_trial_recommendation",
        "approval_root",
        "trial_output_root",
    ]
    tsv_path = out_root / "batch_report.tsv"
    with tsv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    batch_verdict, verdict_blockers = _compute_batch_verdict(
        actual_count=actual_count,
        expected_full=expected_full,
        duplicate_index=duplicate_index,
        rows=rows,
    )

    summary = {
        "phase": "Phase-Mainline-GuardedTrial-012-Fix",
        "sample_dir": str(sample_dir),
        "included_samples": included_samples,
        "excluded_samples": excluded_records,
        "sample_filter": sample_filter,
        "batch_verdict": batch_verdict,
        "batch_verdict_blockers": verdict_blockers,
        "count": len(rows),
        "rapidocr_rows": sum(1 for r in rows if "rapidocr" in str(r.get("provider_selected") or "").lower()),
        "non_empty_text": sum(1 for r in rows if int(r.get("raw_text_len") or -1) > 0),
        "go_next": sum(1 for r in rows if r.get("post_trial_recommendation") == "GO_next_window"),
        "conditional_go_repeat": sum(1 for r in rows if r.get("post_trial_recommendation") == "CONDITIONAL_GO_repeat"),
        "no_go_rollback": sum(1 for r in rows if r.get("post_trial_recommendation") == "NO_GO_rollback_and_fix"),
    }
    (out_root / "batch_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    ha_batch = {
        "network_request_invoked": any((r.get("hard_audit") or {}).get("network_request_invoked") for r in rows),
        "semantic_interpretation_enabled": any((r.get("hard_audit") or {}).get("semantic_interpretation_enabled") for r in rows),
        "midplatform_invoked": any((r.get("hard_audit") or {}).get("midplatform_invoked") for r in rows),
        "scene_delta_invoked": any((r.get("hard_audit") or {}).get("scene_delta_invoked") for r in rows),
        "world_context_invoked": any((r.get("hard_audit") or {}).get("world_context_invoked") for r in rows),
        "qwen_invoked": any((r.get("hard_audit") or {}).get("qwen_invoked") for r in rows),
        "real_tts_invoked": any((r.get("hard_audit") or {}).get("real_tts_invoked") for r in rows),
        "playback_invoked": any((r.get("hard_audit") or {}).get("playback_invoked") for r in rows),
        "downstream_invocation_count_max": max(
            ((r.get("hard_audit") or {}).get("downstream_invocation_count") or 0) for r in rows
        )
        if rows
        else 0,
        "navigation_action_all_null": all((r.get("hard_audit") or {}).get("navigation_action") in (None, "null") for r in rows),
        "world_write_invoked": any((r.get("hard_audit") or {}).get("world_write_invoked") for r in rows),
        "hive_upload_invoked": any((r.get("hard_audit") or {}).get("hive_upload_invoked") for r in rows),
    }

    tid = f"batch_012_fix_{out_root.name}"
    for fname, payload in (
        ("ocr_stage2_batch_rapidocr_trace.jsonl", {"type": "batch_trace", "ts": tid, "batch_verdict": batch_verdict}),
        ("ocr_stage2_batch_rapidocr_replay.jsonl", {"type": "batch_replay", "ts": tid, "sample_filter": sample_filter}),
        ("ocr_stage2_batch_rapidocr_whitebox.jsonl", {"type": "batch_whitebox", "ts": tid, "hard_audit_batch": ha_batch}),
    ):
        (out_root / fname).write_text(json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "output_root": str(out_root), "batch_report": str(tsv_path), "summary": summary}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

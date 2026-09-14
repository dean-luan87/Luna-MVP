#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Failed-Sample-Isolation-001 — Verifier for failed-sample isolation outputs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--isolation-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.isolation_root, "--isolation-root")
    blockers: List[str] = []

    required = (
        "paddleocr_failed_sample_isolation_summary.json",
        "paddleocr_failed_sample_matrix.json",
        "paddleocr_failed_sample_image_probe_report.json",
        "paddleocr_failed_sample_variant_results.json",
        "paddleocr_failed_sample_raw_shape_report.json",
        "paddleocr_failed_sample_crash_classification.json",
        "paddleocr_failed_sample_audit_report.json",
        "paddleocr_failed_sample_notes.md",
    )
    for name in required:
        if not (root / name).is_file():
            blockers.append(f"missing:{name}")

    sum_p = root / "paddleocr_failed_sample_isolation_summary.json"
    summary: Dict[str, Any] = _read_json(sum_p) if sum_p.is_file() else {}
    failed: List[str] = [str(x) for x in summary.get("failed_sample_ids") or [] if x]
    if not failed:
        blockers.append("empty_failed_sample_ids")

    aud_p = root / "paddleocr_failed_sample_audit_report.json"
    if aud_p.is_file():
        aud = _read_json(aud_p)
        for k in (
            "network_request_invoked",
            "model_cache_modified",
            "ocr_routing_changed",
            "rapidocr_replaced",
            "runtime_integration",
            "whitebox_integration",
            "midplatform_invoked",
            "world_model_written",
            "midplatform_semantics_written",
            "mainline_touched",
        ):
            if aud.get(k) is True:
                blockers.append(f"audit_true:{k}")

    probe_p = root / "paddleocr_failed_sample_image_probe_report.json"
    probes: Dict[str, Any] = {}
    if probe_p.is_file():
        doc = _read_json(probe_p)
        probes = doc.get("probes") if isinstance(doc.get("probes"), dict) else {}

    for sid in failed:
        pr = probes.get(sid)
        if not isinstance(pr, dict):
            blockers.append(f"probe_missing:{sid}")
            continue
        if pr.get("file_exists") is True and pr.get("width") is None and not pr.get("probe_error"):
            blockers.append(f"probe_no_dimensions:{sid}")
        if pr.get("file_exists") is not True and not pr.get("probe_error"):
            blockers.append(f"probe_incomplete:{sid}")

    vr_p = root / "paddleocr_failed_sample_variant_results.json"
    rows: List[Dict[str, Any]] = []
    if vr_p.is_file():
        doc = _read_json(vr_p)
        rows = doc.get("rows") if isinstance(doc.get("rows"), list) else []

    bs1 = Path(str(summary.get("input_bs1_rerun_root") or ""))
    crash_sids: Set[str] = set()
    sig_sids: Set[str] = set()
    if bs1.is_dir():
        cp = bs1 / "paddleocr_labeled_set_batch_crash_report.json"
        if cp.is_file():
            crash = _read_json(cp)
            for e in crash.get("crash_entries") or []:
                if not isinstance(e, dict):
                    continue
                sid = str(e.get("last_sample_id") or "")
                if sid:
                    crash_sids.add(sid)
                if e.get("signal") == 11 or e.get("exit_code") == -11:
                    sig_sids.add(sid)

    required_variants = ("original", "downscale_max_2048", "downscale_max_1600")
    for sid in failed:
        if sid not in sig_sids:
            continue
        for vn in required_variants:
            hit = [r for r in rows if isinstance(r, dict) and r.get("sample_id") == sid and r.get("variant") == vn]
            if not hit:
                blockers.append(f"missing_variant_row:{sid}:{vn}")
                continue
            h = hit[0]
            if h.get("exit_code") is None and not h.get("build_error"):
                blockers.append(f"variant_no_outcome:{sid}:{vn}")

    raw_p = root / "paddleocr_failed_sample_raw_shape_report.json"
    if not raw_p.is_file() or not isinstance((_read_json(raw_p) if raw_p.is_file() else {}).get("adapter_rules"), list):
        blockers.append("raw_shape_adapter_rules_missing")

    cc_p = root / "paddleocr_failed_sample_crash_classification.json"
    if cc_p.is_file():
        cc = _read_json(cc_p)
        by = cc.get("by_sample_id") if isinstance(cc.get("by_sample_id"), dict) else {}
        for sid in failed:
            if sid not in by:
                blockers.append(f"classification_missing_sample:{sid}")
    else:
        blockers.append("missing_crash_classification")

    post_012 = None
    if raw_p.is_file():
        rs = _read_json(raw_p)
        post_012 = rs.get("labeled_012_post_fix_subprocess")

    if "labeled_012" in failed:
        if not isinstance(post_012, dict):
            blockers.append("labeled_012_post_fix_missing")
        elif post_012.get("exit_code") != 0:
            blockers.append("labeled_012_post_fix_not_exit_0")

    verdict: str
    if blockers:
        hard_prefixes = (
            "missing:",
            "empty_failed_sample_ids",
            "audit_true:",
            "missing_variant_row:",
            "variant_no_outcome:",
            "raw_shape_adapter_rules_missing",
            "missing_crash_classification",
            "classification_missing_sample:",
            "labeled_012_post_fix_missing",
            "probe_missing:",
            "probe_no_dimensions:",
            "probe_incomplete:",
        )
        if any(b.startswith(hard_prefixes) for b in blockers):
            verdict = "NO_GO"
        else:
            verdict = "CONDITIONAL_GO"
    else:
        verdict = "GO"

    rep = {
        "schema": "paddleocr_failed_sample_isolation_verifier_report_v0",
        "phase": "Phase-PaddleOCR-Failed-Sample-Isolation-001",
        "isolation_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "paddleocr_failed_sample_isolation_verifier_report.json", rep)
    print(json.dumps({"isolation_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

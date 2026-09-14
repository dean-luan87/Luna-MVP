#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001 — Batch subprocess isolation + merge + crash audit.

Evaluation-only: does not change routing, MidPlatform, or RapidOCR default. Invokes existing labeled-set runner per batch in a fresh subprocess.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import statistics
import subprocess
import sys
import time
import traceback
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _exit_code_to_signal(rc: int) -> Optional[int]:
    if rc is None:
        return None
    if rc < 0:
        return -int(rc)
    return None


def _chunks(xs: List[Any], n: int) -> List[List[Any]]:
    out: List[List[Any]] = []
    for i in range(0, len(xs), n):
        out.append(xs[i : i + n])
    return out


def _cer(gt: str, hyp: str) -> float:
    def _ed(a: str, b: str) -> int:
        a = a or ""
        b = b or ""
        if len(a) < len(b):
            a, b = b, a
        la, lb = len(a), len(b)
        prev = list(range(lb + 1))
        for i in range(1, la + 1):
            cur = [i] + [0] * lb
            ca = a[i - 1]
            for j in range(1, lb + 1):
                cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (0 if ca == b[j - 1] else 1))
            prev = cur
        return prev[lb]

    gt = (gt or "").strip()
    hyp = (hyp or "").strip()
    if not gt and not hyp:
        return 0.0
    d = _ed(gt, hyp)
    return d / max(len(gt), len(hyp), 1)


def _merge_from_batches(
    full_samples: List[Dict[str, Any]],
    batch_dirs: Dict[int, Path],
    batch_ok: Dict[int, bool],
) -> Tuple[
    List[Dict[str, Any]],
    List[Dict[str, Any]],
    List[Dict[str, Any]],
    List[Dict[str, Any]],
    List[str],
]:
    """Build merged rows aligned to full_samples order; missing batches -> placeholders + missing_ids."""
    by_id: Dict[str, Tuple[int, Path]] = {}
    for bi, root in batch_dirs.items():
        if not batch_ok.get(bi):
            continue
        sm_p = root / "paddleocr_labeled_set_sample_matrix.json"
        if not sm_p.is_file():
            continue
        sm = _read_json(sm_p)
        rows = sm.get("rows") if isinstance(sm.get("rows"), list) else []
        for r in rows:
            if isinstance(r, dict) and r.get("sample_id"):
                by_id[str(r["sample_id"])] = (bi, root)

    merged_matrix: List[Dict[str, Any]] = []
    merged_raw: List[Dict[str, Any]] = []
    merged_norm: List[Dict[str, Any]] = []
    merged_ev: List[Dict[str, Any]] = []
    missing: List[str] = []

    for spec in full_samples:
        sid = str(spec.get("id") or "")
        if sid not in by_id:
            missing.append(sid)
            merged_matrix.append(
                {
                    "sample_id": sid,
                    "category": spec.get("category"),
                    "image_path": spec.get("image_path"),
                    "ok": False,
                    "predict_duration_ms": None,
                    "call_method": None,
                    "fallback_reason": None,
                    "error": "missing_from_successful_batches",
                }
            )
            merged_raw.append({"sample_id": sid, "image_path": spec.get("image_path"), "raw": None})
            merged_norm.append(
                {
                    "sample_id": sid,
                    "category": spec.get("category"),
                    "text_joined": "",
                    "text_items": [],
                    "error": "missing_from_successful_batches",
                }
            )
            merged_ev.append(
                {
                    "sample_id": sid,
                    "category": spec.get("category"),
                    "text_item_count": 0,
                    "text_joined": "",
                    "field_fidelity": {},
                    "reading_order_mismatch": False,
                }
            )
            continue
        _bi, root = by_id[sid]
        sm = _read_json(root / "paddleocr_labeled_set_sample_matrix.json")
        raw_j = _read_json(root / "paddleocr_labeled_set_raw_results.json")
        nm_j = _read_json(root / "paddleocr_labeled_set_normalized_results.json")
        ev_j = _read_json(root / "paddleocr_labeled_set_evidence_results.json")
        row_map = {str(r.get("sample_id")): r for r in (sm.get("rows") or []) if isinstance(r, dict)}
        raw_map = {str(r.get("sample_id")): r for r in (raw_j.get("results") or []) if isinstance(r, dict)}
        nm_map = {str(r.get("sample_id")): r for r in (nm_j.get("results") or []) if isinstance(r, dict)}
        ev_map = {str(r.get("sample_id")): r for r in (ev_j.get("results") or []) if isinstance(r, dict)}
        merged_matrix.append(dict(row_map.get(sid, {})))
        merged_raw.append(dict(raw_map.get(sid, {})))
        merged_norm.append(dict(nm_map.get(sid, {})))
        merged_ev.append(dict(ev_map.get(sid, {})))

    return merged_matrix, merged_raw, merged_norm, merged_ev, missing


def _build_merged_quality(
    full_samples: List[Dict[str, Any]],
    merged_matrix: List[Dict[str, Any]],
    merged_norm: List[Dict[str, Any]],
    merged_ev: List[Dict[str, Any]],
) -> Dict[str, Any]:
    n = len(full_samples)
    with_gt = sum(
        1
        for s in full_samples
        if s.get("ground_truth_text") is not None and str(s.get("ground_truth_text") or "").strip() != ""
    )
    gt_cov = round(with_gt / n, 4) if n else 0.0
    per_sample: List[Dict[str, Any]] = []
    for i, spec in enumerate(full_samples):
        norm = merged_norm[i] if i < len(merged_norm) else {}
        row = merged_matrix[i] if i < len(merged_matrix) else {}
        joined = str(norm.get("text_joined") or "").strip()
        gt = spec.get("ground_truth_text")
        gt_s = str(gt).strip() if gt is not None else ""
        evaluated = bool(spec.get("include_in_accuracy", True)) and bool(gt_s)
        exact = bool(evaluated and gt_s == joined) if row.get("ok") else None
        cer_v = round(_cer(gt_s, joined), 4) if evaluated and row.get("ok") else None
        per_sample.append(
            {
                "sample_id": spec.get("id"),
                "category": spec.get("category"),
                "exact_match": exact,
                "cer": cer_v,
                "evaluated": evaluated,
            }
        )
    eval_rows = [m for m in per_sample if m.get("evaluated")]
    exact_match_rate = round(sum(1 for m in eval_rows if m.get("exact_match")) / len(eval_rows), 4) if eval_rows else None
    char_error_rate_mean = (
        round(statistics.mean([float(m["cer"]) for m in eval_rows if m.get("cer") is not None]), 4)
        if eval_rows and any(m.get("cer") is not None for m in eval_rows)
        else None
    )
    cer_by_cat: Dict[str, List[float]] = defaultdict(list)
    for m in eval_rows:
        if m.get("cer") is not None:
            cer_by_cat[str(m.get("category") or "")].append(float(m["cer"]))
    char_error_rate_by_category = {k: round(statistics.mean(v), 4) for k, v in sorted(cer_by_cat.items()) if v}

    false_text_n = sum(1 for s in full_samples if s.get("false_text_suspected"))
    ro_n = len(
        {
            i
            for i, s in enumerate(full_samples)
            if s.get("reading_order_issue_suspected")
            or (i < len(merged_ev) and merged_ev[i].get("reading_order_mismatch"))
        }
    )
    mr_n = sum(1 for s in full_samples if s.get("multi_region_mix_suspected"))

    return {
        "schema": "paddleocr_labeled_set_quality_metrics_v0",
        "phase": "Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001",
        "merge_source": "batch_outputs_concatenated",
        "sample_count": n,
        "ground_truth_coverage": gt_cov,
        "exact_match_rate": exact_match_rate,
        "char_error_rate_mean": char_error_rate_mean,
        "char_error_rate_by_category": char_error_rate_by_category,
        "false_text_suspected_count": false_text_n,
        "reading_order_issue_suspected_count": ro_n,
        "multi_region_mix_suspected_count": mr_n,
        "production_quality_deemed_pass": False,
        "evaluation_interpretation": "batch_recovery_merge_evaluation_only_not_production_gate",
    }


def _merged_runtime(batch_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    peaks = [r.get("memory_peak_mb") for r in batch_results if r.get("memory_peak_mb") is not None]
    durs = [r.get("batch_duration_ms") for r in batch_results if r.get("batch_duration_ms") is not None]
    return {
        "schema": "paddleocr_labeled_set_batch_merged_runtime_metrics_v0",
        "phase": "Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001",
        "memory_peak_mb_max_across_batches": max(peaks) if peaks else None,
        "batch_duration_ms_sum": round(sum(float(x) for x in durs), 2) if durs else None,
        "memory_peak_by_batch": [
            {"batch_index": r.get("batch_index"), "memory_peak_mb": r.get("memory_peak_mb")} for r in batch_results
        ],
    }


def _merged_audit(batch_results: List[Dict[str, Any]], batch_dirs: Dict[int, Path], batch_ok: Dict[int, bool]) -> Dict[str, Any]:
    agg = {
        "schema": "paddleocr_labeled_set_batch_audit_report_v0",
        "phase": "Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001",
        "network_request_invoked": False,
        "model_cache_modified": False,
        "ocr_routing_changed": False,
        "rapidocr_replaced": False,
        "runtime_integration": False,
        "whitebox_integration": False,
        "midplatform_invoked": False,
        "world_model_written": False,
        "midplatform_semantics_written": False,
        "mainline_touched": False,
    }
    for bi, ok in batch_ok.items():
        if not ok:
            continue
        p = batch_dirs.get(bi)
        if p is None:
            continue
        aud_p = p / "paddleocr_labeled_set_audit_report.json"
        if not aud_p.is_file():
            continue
        aud = _read_json(aud_p)
        for k in list(agg.keys()):
            if k in ("schema", "phase"):
                continue
            if aud.get(k) is True:
                agg[k] = True
    return agg


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--materialize-root", required=True)
    ap.add_argument("--pinned-manifest", required=True)
    ap.add_argument("--labeled-set-manifest", required=True, help="Full labeled set manifest (e.g. 20 samples)")
    ap.add_argument("--output-root", default="", help="Batch recovery root; default under ~/LunaRuntime/logs/evaluation/")
    ap.add_argument("--batch-size", type=int, default=5, help="Samples per subprocess batch (try 1, 5, 10)")
    ap.add_argument("--resume", action="store_true", help="Skip batches already completed with exit_code=0")
    ap.add_argument("--batch-timeout-sec", type=int, default=7200, help="Subprocess wall timeout per batch")
    ap.add_argument("--no-use-angle-cls", action="store_true")
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    mat_root = _require_abs(args.materialize_root, "--materialize-root")
    pinned_path = _require_abs(args.pinned_manifest, "--pinned-manifest")
    manifest_path = _require_abs(args.labeled_set_manifest, "--labeled-set-manifest")

    if args.output_root.strip():
        out_root = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out_root = (
            Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_labeled_set_batch_recovery_001_{stamp}"
        ).resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    mat_sum_p = mat_root / "paddleocr_manifest_v1_cache_materialize_summary.json"
    if not mat_sum_p.is_file():
        raise SystemExit(f"ERROR: missing {mat_sum_p}")
    mat_sum = _read_json(mat_sum_p)
    if mat_sum.get("materialize_verdict") != "GO":
        raise SystemExit(f"ERROR: materialize_verdict must be GO, got {mat_sum.get('materialize_verdict')}")

    doc = _read_json(manifest_path)
    if str(doc.get("schema_version") or "") != "paddleocr_labeled_set_manifest_v0":
        raise SystemExit("ERROR: schema_version must be paddleocr_labeled_set_manifest_v0")
    rows = doc.get("samples") if isinstance(doc.get("samples"), list) else []
    if not rows:
        raise SystemExit("ERROR: samples empty")
    if len(rows) > 50:
        raise SystemExit("ERROR: at most 50 samples for labeled set")

    full_samples: List[Dict[str, Any]] = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise SystemExit(f"ERROR: samples[{i}] must be object")
        sid = str(row.get("id") or "").strip()
        ip = str(row.get("image_path") or "").strip()
        cat = str(row.get("category") or "").strip()
        if not sid or not ip or not cat:
            raise SystemExit(f"ERROR: samples[{i}] missing id, image_path, or category")
        img_p = _require_abs(ip, f"samples[{i}].image_path")
        if not img_p.is_file():
            raise SystemExit(f"ERROR: image not readable: {img_p}")
        full_samples.append(
            {
                "id": sid,
                "image_path": str(img_p),
                "category": cat,
                "ground_truth_text": row.get("ground_truth_text"),
                "ground_truth_items": row.get("ground_truth_items") if isinstance(row.get("ground_truth_items"), list) else [],
                "include_in_accuracy": bool(row.get("include_in_accuracy", True)),
                "expected_risks": row.get("expected_risks") if isinstance(row.get("expected_risks"), list) else [],
                "notes": str(row.get("notes") or ""),
                "false_text_suspected": bool(row.get("false_text_suspected", False)),
                "reading_order_issue_suspected": bool(row.get("reading_order_issue_suspected", False)),
                "multi_region_mix_suspected": bool(row.get("multi_region_mix_suspected", False)),
            }
        )

    bs = int(args.batch_size)
    if bs < 1 or bs > 50:
        raise SystemExit("ERROR: batch-size must be 1..50")

    batches_samples = _chunks(full_samples, bs)
    batch_count = len(batches_samples)
    runner = repo / "tools/evaluation/ocr/run_paddleocr_labeled_set_evaluation_v0.py"
    if not runner.is_file():
        raise SystemExit(f"ERROR: missing runner {runner}")

    resume_path = out_root / "paddleocr_labeled_set_batch_resume_state.json"
    resume: Dict[str, Any] = {}
    if args.resume and resume_path.is_file():
        resume = _read_json(resume_path)
    completed: set[int] = set()
    for x in resume.get("completed_batches", []):
        try:
            completed.add(int(x))
        except (TypeError, ValueError):
            continue

    plan_batches: List[Dict[str, Any]] = []
    batch_dirs: Dict[int, Path] = {}
    batch_results: List[Dict[str, Any]] = []
    crash_entries: List[Dict[str, Any]] = []

    for bi, chunk in enumerate(batches_samples):
        bdir = out_root / "batches" / f"batch_{bi:03d}"
        bdir.mkdir(parents=True, exist_ok=True)
        slice_doc = {"schema_version": "paddleocr_labeled_set_manifest_v0", "samples": chunk}
        slice_path = bdir / "manifest_slice.json"
        slice_path.write_text(json.dumps(slice_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        eval_out = bdir
        batch_dirs[bi] = eval_out

        last_sid = str(chunk[-1]["id"]) if chunk else ""
        plan_batches.append(
            {
                "batch_index": bi,
                "sample_ids": [str(s["id"]) for s in chunk],
                "manifest_slice_path": str(slice_path),
                "output_root": str(eval_out),
                "last_sample_id": last_sid,
            }
        )

        if args.resume and bi in completed:
            sum_p = eval_out / "paddleocr_labeled_set_summary.json"
            if sum_p.is_file():
                try:
                    sm = _read_json(sum_p)
                    if sm.get("labeled_set_verdict") != "NO_GO":
                        batch_results.append(
                            {
                                "batch_index": bi,
                                "exit_code": 0,
                                "signal": None,
                                "skipped_resume": True,
                                "batch_duration_ms": 0.0,
                                "last_sample_id": last_sid,
                                "memory_peak_mb": None,
                                "stderr_tail": "",
                            }
                        )
                        rt_p = eval_out / "paddleocr_labeled_set_runtime_metrics.json"
                        if rt_p.is_file():
                            try:
                                batch_results[-1]["memory_peak_mb"] = _read_json(rt_p).get("memory_peak_mb")
                            except Exception:
                                pass
                        continue
                except Exception:
                    pass

        cmd = [
            sys.executable,
            str(runner),
            "--repo-root",
            str(repo),
            "--materialize-root",
            str(mat_root),
            "--pinned-manifest",
            str(pinned_path),
            "--labeled-set-manifest",
            str(slice_path.resolve()),
            "--output-root",
            str(eval_out.resolve()),
        ]
        if args.no_use_angle_cls:
            cmd.append("--no-use-angle-cls")

        t0 = time.perf_counter()
        stderr_tail = ""
        exit_code = 1
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(repo),
                capture_output=True,
                text=True,
                timeout=int(args.batch_timeout_sec),
            )
            exit_code = int(proc.returncode or 0)
            err = proc.stderr or ""
            stderr_tail = err[-8000:] if err else ""
        except subprocess.TimeoutExpired as e:
            exit_code = 124
            stderr_tail = (e.stderr or "")[-8000:] if isinstance(e.stderr, str) else ""
        except Exception as e:
            exit_code = 1
            stderr_tail = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"[-8000:]

        dt_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        sig = _exit_code_to_signal(exit_code)

        mem_peak = None
        rt_p = eval_out / "paddleocr_labeled_set_runtime_metrics.json"
        if rt_p.is_file():
            try:
                mem_peak = _read_json(rt_p).get("memory_peak_mb")
            except Exception:
                mem_peak = None

        row = {
            "batch_index": bi,
            "exit_code": exit_code,
            "signal": sig,
            "skipped_resume": False,
            "batch_duration_ms": dt_ms,
            "last_sample_id": last_sid,
            "memory_peak_mb": mem_peak,
            "stderr_tail": stderr_tail,
        }
        batch_results.append(row)

        if exit_code != 0 or sig is not None:
            crash_entries.append(
                {
                    "batch_index": bi,
                    "exit_code": exit_code,
                    "signal": sig,
                    "last_sample_id": last_sid,
                    "crash_sample_candidates": [str(s["id"]) for s in chunk],
                    "stderr_tail": stderr_tail,
                }
            )
        if exit_code == 0 and sig is None:
            completed.add(bi)

        resume_state = {
            "schema": "paddleocr_labeled_set_batch_resume_state_v0",
            "phase": "Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001",
            "completed_batches": sorted(completed),
            "last_batch_attempted": bi,
            "updated_at_utc": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        }
        _write_json(resume_path, resume_state)

    batch_ok = {int(r["batch_index"]): (r.get("exit_code") == 0 and r.get("signal") is None) for r in batch_results}
    merged_matrix, merged_raw, merged_norm, merged_ev, missing_ids = _merge_from_batches(full_samples, batch_dirs, batch_ok)
    merged_quality = _build_merged_quality(full_samples, merged_matrix, merged_norm, merged_ev)
    merged_runtime = _merged_runtime(batch_results)
    merged_audit = _merged_audit(batch_results, batch_dirs, batch_ok)

    n_full = len(full_samples)
    with_gt = sum(
        1
        for s in full_samples
        if s.get("ground_truth_text") is not None and str(s.get("ground_truth_text") or "").strip() != ""
    )
    gt_cov_full = round(with_gt / n_full, 4) if n_full else 0.0

    completed_batch_count = sum(1 for r in batch_results if r.get("exit_code") == 0 and r.get("signal") is None)
    failed_batch_count = batch_count - completed_batch_count
    merged_present = n_full - len(missing_ids)

    merged_gt_cov = float(merged_quality.get("ground_truth_coverage") or 0.0)
    predict_all_ok = all(r.get("ok") for r in merged_matrix) if merged_matrix else False

    recovery_verdict = "CONDITIONAL_GO"
    audit_bad = any(
        merged_audit.get(k) is True
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
        )
    )
    if audit_bad:
        recovery_verdict = "NO_GO"
    elif (
        completed_batch_count == batch_count
        and failed_batch_count == 0
        and merged_present == n_full
        and n_full >= 20
        and merged_gt_cov >= 0.8
        and not crash_entries
        and predict_all_ok
    ):
        recovery_verdict = "GO"
    elif not plan_batches:
        recovery_verdict = "NO_GO"
    elif crash_entries and all("exit_code" in e for e in crash_entries):
        recovery_verdict = "CONDITIONAL_GO"
    else:
        recovery_verdict = "CONDITIONAL_GO"

    plan_obj = {
        "schema": "paddleocr_labeled_set_batch_plan_v0",
        "phase": "Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001",
        "batch_size": bs,
        "batch_count": batch_count,
        "full_manifest": str(manifest_path),
        "batches": plan_batches,
    }
    _write_json(out_root / "paddleocr_labeled_set_batch_plan.json", plan_obj)
    _write_json(
        out_root / "paddleocr_labeled_set_batch_results_matrix.json",
        {"schema": "paddleocr_labeled_set_batch_results_matrix_v0", "rows": batch_results},
    )
    _write_json(out_root / "paddleocr_labeled_set_batch_crash_report.json", {"crash_entries": crash_entries})
    _write_json(out_root / "paddleocr_labeled_set_batch_merged_quality_metrics.json", merged_quality)
    _write_json(out_root / "paddleocr_labeled_set_batch_merged_runtime_metrics.json", merged_runtime)
    _write_json(out_root / "paddleocr_labeled_set_batch_audit_report.json", merged_audit)

    _write_json(
        out_root / "paddleocr_labeled_set_batch_recovery_summary.json",
        {
            "schema": "paddleocr_labeled_set_batch_recovery_summary_v0",
            "phase": "Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001",
            "batch_recovery_verdict": recovery_verdict,
            "repo_root": str(repo),
            "materialize_root": str(mat_root),
            "pinned_manifest": str(pinned_path),
            "labeled_set_manifest": str(manifest_path),
            "output_root": str(out_root),
            "batch_size": bs,
            "batch_count": batch_count,
            "completed_batch_count": completed_batch_count,
            "failed_batch_count": failed_batch_count,
            "merged_sample_count_present": merged_present,
            "merged_sample_count_expected": n_full,
            "missing_sample_ids": missing_ids,
            "ground_truth_coverage_manifest": gt_cov_full,
            "crash_sample_count": sum(len(e.get("crash_sample_candidates") or []) for e in crash_entries),
        },
    )

    notes = "\n".join(
        [
            "# PaddleOCR Labeled Set Batch Recovery v0",
            "",
            f"- **batch_recovery_verdict**: `{recovery_verdict}`",
            f"- **output_root**: `{out_root}`",
            f"- **batch_size**: `{bs}`",
            f"- **batches**: {batch_count} (completed={completed_batch_count}, failed={failed_batch_count})",
            "",
            "- Subprocess per batch isolates SIGSEGV to a single child; inspect `batch_crash_report` + per-batch `stderr_tail`.",
            "- **GO** requires all batches exit 0, merged coverage of all manifest ids, n≥20, GT coverage≥0.8, empty crash report, clean merged audit.",
            "",
        ]
    )
    (out_root / "paddleocr_labeled_set_batch_recovery_notes.md").write_text(notes, encoding="utf-8")

    print(
        json.dumps(
            {
                "batch_recovery_output_root": str(out_root),
                "batch_recovery_verdict": recovery_verdict,
                "batch_count": batch_count,
                "completed_batch_count": completed_batch_count,
                "failed_batch_count": failed_batch_count,
            },
            ensure_ascii=False,
        )
    )
    return 0 if recovery_verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

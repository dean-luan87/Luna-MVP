#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Evaluation-Benchmark-001 — Small-sample quality + runtime benchmark (evaluation-only).

Reuses current API adapter normalization paths; max 20 images; no routing / RapidOCR / MidPlatform.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import statistics
import sys
import time
import traceback
import urllib.request
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

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


def _load_adapter_contract_module() -> Any:
    p = Path(__file__).resolve().parent / "paddleocr_current_api_adapter_contract_v0.py"
    spec = importlib.util.spec_from_file_location("paddleocr_adapter_contract_v0", p)
    if spec is None or spec.loader is None:
        raise SystemExit("ERROR: cannot load paddleocr_current_api_adapter_contract_v0.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _install_network_probe(flag_holder: Dict[str, bool]) -> Callable[..., Any]:
    orig_urlopen = urllib.request.urlopen

    def wrapped_urlopen(*a: Any, **kw: Any) -> Any:
        flag_holder["network_request_invoked"] = True
        return orig_urlopen(*a, **kw)

    urllib.request.urlopen = wrapped_urlopen  # type: ignore[assignment]
    return orig_urlopen


def _restore_urlopen(orig: Callable[..., Any]) -> None:
    urllib.request.urlopen = orig  # type: ignore[assignment]


def _edit_distance(a: str, b: str) -> int:
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
            cur[j] = min(
                prev[j] + 1,
                cur[j - 1] + 1,
                prev[j - 1] + (0 if ca == b[j - 1] else 1),
            )
        prev = cur
    return prev[lb]


def _cer(gt: str, hyp: str) -> float:
    gt = (gt or "").strip()
    hyp = (hyp or "").strip()
    if not gt and not hyp:
        return 0.0
    d = _edit_distance(gt, hyp)
    return d / max(len(gt), len(hyp), 1)


def _percentile(sorted_vals: List[float], q: float) -> Optional[float]:
    if not sorted_vals:
        return None
    xs = sorted(sorted_vals)
    n = len(xs)
    if n == 1:
        return round(xs[0], 3)
    idx = (n - 1) * q
    lo = int(idx)
    hi = min(lo + 1, n - 1)
    w = idx - lo
    return round(xs[lo] * (1 - w) + xs[hi] * w, 3)


def _try_memory_mb() -> Tuple[Optional[float], str]:
    try:
        import psutil  # type: ignore[import-untyped]

        p = psutil.Process()
        rss = p.memory_info().rss / (1024 * 1024)
        return round(float(rss), 2), "psutil.Process().memory_info().rss_mb_snapshot"
    except Exception:
        return None, "psutil_unavailable_or_error"


def _device_info(paddle_mod: Any, init_kwargs: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "use_gpu_kw": bool(init_kwargs.get("use_gpu")),
        "device_kw": str(init_kwargs.get("device") or ""),
    }
    try:
        import paddle

        fn = getattr(paddle.device, "is_compiled_with_cuda", None)
        out["paddle_compiled_with_cuda"] = bool(fn()) if callable(fn) else False
    except Exception as e:
        out["paddle_device_probe_error"] = str(e)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--materialize-root", required=True)
    ap.add_argument("--pinned-manifest", required=True)
    ap.add_argument("--sample-manifest", required=True)
    ap.add_argument("--output-root", default="")
    ap.add_argument("--no-use-angle-cls", action="store_true")
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    mat_root = _require_abs(args.materialize_root, "--materialize-root")
    pinned_path = _require_abs(args.pinned_manifest, "--pinned-manifest")
    sample_manifest_path = _require_abs(args.sample_manifest, "--sample-manifest")

    if args.output_root.strip():
        out_root = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out_root = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_evaluation_benchmark_001_{stamp}").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    mat_sum_p = mat_root / "paddleocr_manifest_v1_cache_materialize_summary.json"
    if not mat_sum_p.is_file():
        raise SystemExit(f"ERROR: missing {mat_sum_p}")
    mat_sum = json.loads(mat_sum_p.read_text(encoding="utf-8"))
    if mat_sum.get("materialize_verdict") != "GO":
        raise SystemExit(f"ERROR: materialize_verdict must be GO, got {mat_sum.get('materialize_verdict')}")

    sm = json.loads(sample_manifest_path.read_text(encoding="utf-8"))
    if str(sm.get("schema_version") or "") != "paddleocr_benchmark_sample_manifest_v0":
        raise SystemExit("ERROR: sample manifest schema_version must be paddleocr_benchmark_sample_manifest_v0")
    samples_in = sm.get("samples") if isinstance(sm.get("samples"), list) else []
    if len(samples_in) == 0:
        raise SystemExit("ERROR: samples must be non-empty")
    if len(samples_in) > 20:
        raise SystemExit(f"ERROR: at most 20 samples allowed, got {len(samples_in)}")

    samples: List[Dict[str, Any]] = []
    for i, row in enumerate(samples_in):
        if not isinstance(row, dict):
            raise SystemExit(f"ERROR: samples[{i}] must be object")
        sid = str(row.get("id") or "").strip()
        ip = str(row.get("image_path") or "").strip()
        cat = str(row.get("category") or "uncategorized").strip()
        if not sid or not ip:
            raise SystemExit(f"ERROR: samples[{i}] missing id or image_path")
        img_p = _require_abs(ip, f"samples[{i}].image_path")
        if not img_p.is_file():
            raise SystemExit(f"ERROR: image not readable: {img_p}")
        samples.append(
            {
                "id": sid,
                "image_path": str(img_p),
                "category": cat,
                "ground_truth_text": row.get("ground_truth_text"),
                "include_in_accuracy": bool(row.get("include_in_accuracy")),
                "expected_notes": str(row.get("expected_notes") or ""),
                "false_text_suspected": bool(row.get("false_text_suspected", False)),
                "reading_order_issue_suspected": bool(row.get("reading_order_issue_suspected", False)),
                "multi_region_mix_suspected": bool(row.get("multi_region_mix_suspected", False)),
            }
        )

    ad = _load_adapter_contract_module()
    pinned = json.loads(pinned_path.read_text(encoding="utf-8"))
    resolved = pinned.get("resolved_model_refs") or {}
    det_path = (resolved.get("det") or {}).get("resolved_path")
    rec_path = (resolved.get("rec") or {}).get("resolved_path")
    cls_path = (resolved.get("cls") or {}).get("resolved_path")
    use_angle_cls = not bool(args.no_use_angle_cls)
    lang = "ch"
    langs = pinned.get("language")
    if isinstance(langs, list) and langs:
        lang = "ch" if "zh" in langs or "mixed" in langs else str(langs[0])
    device = str(pinned.get("device") or "cpu")
    model_dirs = [Path(str(det_path)), Path(str(rec_path)), Path(str(cls_path))] if det_path and rec_path and cls_path else []

    pre_hashes = ad._hash_model_trees(model_dirs)  # type: ignore[attr-defined]

    errors: List[Dict[str, Any]] = []
    raw_results: List[Dict[str, Any]] = []
    normalized_results: List[Dict[str, Any]] = []
    evidence_results: List[Dict[str, Any]] = []
    sample_matrix: List[Dict[str, Any]] = []
    predict_durations: List[float] = []
    constructor_duration_ms: Optional[float] = None
    paddle = None
    constructor_ok = False
    device_info: Dict[str, Any] = {}
    mem_before_ctor, _ = _try_memory_mb()

    net_flag: Dict[str, bool] = {"network_request_invoked": False}
    orig_open = _install_network_probe(net_flag)
    return_code = 2
    try:
        try:
            from paddleocr import PaddleOCR
            import inspect

            t0c = time.perf_counter()
            sig = inspect.signature(PaddleOCR.__init__)
            param_names = [k for k in sig.parameters.keys() if k != "self"]
            cand_kw = {
                "det_dir": det_path,
                "rec_dir": rec_path,
                "cls_dir": cls_path,
                "use_angle_cls": use_angle_cls,
                "lang": lang,
                "use_gpu": device.lower() in ("gpu", "cuda"),
                "device": device,
            }
            init_kwargs = ad._filter_init_kwargs({k: True for k in param_names}, cand_kw)  # type: ignore[attr-defined]
            paddle = PaddleOCR(**init_kwargs)
            constructor_duration_ms = round((time.perf_counter() - t0c) * 1000.0, 2)
            constructor_ok = True
            device_info = _device_info(paddle, init_kwargs)
        except Exception as e:
            constructor_ok = False
            errors.append({"phase": "constructor", "error": f"{type(e).__name__}: {e}", "traceback": traceback.format_exc()})
            device_info = {"error": str(e)}

        mem_after_ctor, _ = _try_memory_mb()

        for si, spec in enumerate(samples):
            img = Path(spec["image_path"])
            row_m: Dict[str, Any] = {
                "sample_id": spec["id"],
                "category": spec["category"],
                "image_path": str(img),
                "ok": False,
                "predict_duration_ms": None,
                "call_method": None,
                "fallback_reason": None,
                "error": None,
            }
            raw_entry: Dict[str, Any] = {"sample_id": spec["id"], "image_path": str(img), "raw": None}
            norm_entry: Dict[str, Any] = {}
            ev_entry: Dict[str, Any] = {
                "sample_id": spec["id"],
                "image_path": str(img),
                "text_item_count": 0,
                "text_joined": "",
                "field_fidelity": {},
            }

            if paddle is None:
                row_m["error"] = "paddle_not_constructed"
                errors.append({"phase": "predict", "sample_id": spec["id"], "error": row_m["error"]})
                sample_matrix.append(row_m)
                raw_results.append(raw_entry)
                n0 = ad.normalize_current_api_result(  # type: ignore[attr-defined]
                    None,
                    image_path=str(img),
                    duration_ms=0.0,
                    call_method="none",
                    error=row_m["error"],
                )
                n0["sample_id"] = spec["id"]
                n0["category"] = spec["category"]
                normalized_results.append(n0)
                evidence_results.append(ev_entry)
                continue

            t0 = time.perf_counter()
            try:
                raw, method, fb = ad._invoke_predict_or_ocr(paddle, img, use_angle_cls)  # type: ignore[attr-defined]
                dt = (time.perf_counter() - t0) * 1000.0
                predict_durations.append(dt)
                row_m["predict_duration_ms"] = round(dt, 2)
                row_m["call_method"] = method
                row_m["fallback_reason"] = fb
                row_m["ok"] = True
                raw_json = ad._to_jsonable(raw)  # type: ignore[attr-defined]
                raw_entry["raw"] = raw_json
                norm = ad.normalize_current_api_result(  # type: ignore[attr-defined]
                    raw,
                    image_path=str(img),
                    duration_ms=dt,
                    call_method=method,
                    error=None,
                )
                norm["sample_id"] = spec["id"]
                norm["category"] = spec["category"]
                norm_entry = norm
                items = norm.get("text_items") if isinstance(norm.get("text_items"), list) else []
                joined = str(norm.get("text_joined") or "")
                polys = sum(1 for it in items if isinstance(it, dict) and it.get("polygon") is not None)
                ev_entry["text_item_count"] = len(items)
                ev_entry["text_joined"] = joined
                ev_entry["field_fidelity"] = {
                    "text_joined_present": bool(joined.strip()),
                    "scores_present": any(isinstance(it, dict) and it.get("score") is not None for it in items),
                    "polygons_present_ratio": round(polys / max(len(items), 1), 4),
                }
            except Exception as e:
                dt = (time.perf_counter() - t0) * 1000.0
                predict_durations.append(dt)
                row_m["predict_duration_ms"] = round(dt, 2)
                row_m["ok"] = False
                row_m["error"] = f"{type(e).__name__}: {e}"
                errors.append(
                    {"phase": "predict", "sample_id": spec["id"], "error": row_m["error"], "traceback": traceback.format_exc()}
                )
                norm_entry = ad.normalize_current_api_result(  # type: ignore[attr-defined]
                    None,
                    image_path=str(img),
                    duration_ms=dt,
                    call_method="none",
                    error=row_m["error"],
                )
                norm_entry["sample_id"] = spec["id"]
                norm_entry["category"] = spec["category"]
                items = norm_entry.get("text_items") if isinstance(norm_entry.get("text_items"), list) else []
                joined = str(norm_entry.get("text_joined") or "")
                polys = sum(1 for it in items if isinstance(it, dict) and it.get("polygon") is not None)
                ev_entry["text_item_count"] = len(items)
                ev_entry["text_joined"] = joined
                ev_entry["field_fidelity"] = {
                    "text_joined_present": bool(joined.strip()),
                    "scores_present": any(isinstance(it, dict) and it.get("score") is not None for it in items),
                    "polygons_present_ratio": round(polys / max(len(items), 1), 4),
                }
            sample_matrix.append(row_m)
            raw_results.append(raw_entry)
            normalized_results.append(norm_entry)
            evidence_results.append(ev_entry)

        post_hashes = ad._hash_model_trees(model_dirs)  # type: ignore[attr-defined]
        model_cache_modified = not (pre_hashes == post_hashes and bool(pre_hashes))

        mem_after_run, mem_note2 = _try_memory_mb()
        memory_peak_mb = None
        if mem_before_ctor is not None or mem_after_ctor is not None or mem_after_run is not None:
            memory_peak_mb = max(x for x in (mem_before_ctor, mem_after_ctor, mem_after_run) if x is not None)

        raw_loss = 0
        for i, spec in enumerate(samples):
            raw_obj = raw_results[i].get("raw") if i < len(raw_results) else None
            norm = normalized_results[i] if i < len(normalized_results) else {}
            joined = str(norm.get("text_joined") or "").strip()
            has_raw_text = ad._raw_contains_rec_texts(raw_obj) if raw_obj is not None else False  # type: ignore[attr-defined]
            if has_raw_text and not joined:
                raw_loss += 1

        gt_eval: List[Dict[str, Any]] = []
        for i, spec in enumerate(samples):
            if not spec.get("include_in_accuracy"):
                continue
            gt = spec.get("ground_truth_text")
            if gt is None or str(gt).strip() == "":
                continue
            norm = normalized_results[i] if i < len(normalized_results) else {}
            hyp = str(norm.get("text_joined") or "")
            ex = str(gt).strip() == hyp.strip()
            gt_eval.append(
                {
                    "sample_id": spec["id"],
                    "exact_match": ex,
                    "cer": round(_cer(str(gt), hyp), 4),
                }
            )

        exact_match_count = sum(1 for x in gt_eval if x.get("exact_match"))
        n_gt = len(gt_eval)
        exact_match_rate = round(exact_match_count / n_gt, 4) if n_gt else None
        cer_mean = round(statistics.mean([float(x["cer"]) for x in gt_eval]), 4) if gt_eval else None

        category_summary: Dict[str, int] = {}
        for spec in samples:
            category_summary[spec["category"]] = category_summary.get(spec["category"], 0) + 1

        empty_result_count = 0
        for i, r in enumerate(sample_matrix):
            if not r.get("ok"):
                continue
            norm = normalized_results[i] if i < len(normalized_results) else {}
            if not str(norm.get("text_joined") or "").strip():
                empty_result_count += 1

        text_item_total = sum(len(n.get("text_items") or []) if isinstance(n, dict) else 0 for n in normalized_results)

        quality_metrics = {
            "schema": "paddleocr_benchmark_quality_metrics_v0",
            "phase": "Phase-PaddleOCR-Evaluation-Benchmark-001",
            "exact_match_count": exact_match_count,
            "exact_match_rate": exact_match_rate,
            "char_error_rate_mean_on_gt": cer_mean,
            "ground_truth_evaluated_count": n_gt,
            "text_item_count_total": text_item_total,
            "empty_result_count": empty_result_count,
            "false_text_suspected_count": sum(1 for s in samples if s.get("false_text_suspected")),
            "reading_order_issue_suspected_count": sum(1 for s in samples if s.get("reading_order_issue_suspected")),
            "multi_region_mix_suspected_count": sum(1 for s in samples if s.get("multi_region_mix_suspected")),
            "category_summary": category_summary,
            "raw_to_normalized_loss_count": raw_loss,
            "accuracy_interpretation": "computed" if n_gt else "not_applicable_no_ground_truth",
            "accuracy_pass_claimed": False,
        }

        pred_ok = [float(x) for x in predict_durations]
        runtime_metrics = {
            "schema": "paddleocr_benchmark_runtime_metrics_v0",
            "phase": "Phase-PaddleOCR-Evaluation-Benchmark-001",
            "constructor_duration_ms": constructor_duration_ms,
            "predict_duration_ms_by_sample": [round(float(x), 3) for x in predict_durations],
            "predict_duration_ms_avg": round(statistics.mean(pred_ok), 3) if pred_ok else None,
            "predict_duration_ms_p50": _percentile(pred_ok, 0.50),
            "predict_duration_ms_p90": _percentile(pred_ok, 0.90),
            "predict_duration_ms_p95": _percentile(pred_ok, 0.95),
            "error_count": sum(1 for r in sample_matrix if not r.get("ok")),
            "timeout_count": 0,
            "memory_peak_mb": memory_peak_mb,
            "memory_measurement_method": mem_note2,
            "device_info": device_info,
        }

        audit = {
            "schema": "paddleocr_benchmark_audit_report_v0",
            "phase": "Phase-PaddleOCR-Evaluation-Benchmark-001",
            "network_request_invoked": bool(net_flag["network_request_invoked"]),
            "model_cache_modified": bool(model_cache_modified),
            "ocr_routing_changed": False,
            "rapidocr_replaced": False,
            "runtime_integration": False,
            "whitebox_integration": False,
            "midplatform_invoked": False,
            "world_model_written": False,
            "midplatform_semantics_written": False,
            "mainline_touched": False,
            "sample_count": len(samples),
        }

        verdict = "NO_GO"
        if not constructor_ok:
            verdict = "NO_GO"
        elif audit["network_request_invoked"] or audit["model_cache_modified"]:
            verdict = "NO_GO"
        elif any(not r.get("ok") for r in sample_matrix):
            verdict = "CONDITIONAL_GO"
        else:
            verdict = "GO"

        summary = {
            "schema": "paddleocr_benchmark_summary_v0",
            "phase": "Phase-PaddleOCR-Evaluation-Benchmark-001",
            "benchmark_verdict": verdict,
            "repo_root": str(repo),
            "materialize_root": str(mat_root),
            "pinned_manifest": str(pinned_path),
            "sample_manifest": str(sample_manifest_path),
            "output_root": str(out_root),
            "sample_count": len(samples),
            "constructor_ok": constructor_ok,
            "audit": audit,
            "errors": errors,
        }

        _write_json(out_root / "paddleocr_benchmark_summary.json", summary)
        _write_json(out_root / "paddleocr_benchmark_sample_matrix.json", {"rows": sample_matrix, "samples_spec": samples})
        _write_json(out_root / "paddleocr_benchmark_raw_results.json", {"results": raw_results})
        _write_json(out_root / "paddleocr_benchmark_normalized_results.json", {"results": normalized_results})
        _write_json(out_root / "paddleocr_benchmark_evidence_results.json", {"results": evidence_results})
        _write_json(out_root / "paddleocr_benchmark_quality_metrics.json", quality_metrics)
        _write_json(out_root / "paddleocr_benchmark_runtime_metrics.json", runtime_metrics)
        _write_json(
            out_root / "paddleocr_benchmark_error_report.json",
            {"errors": errors, "sample_failures": [r for r in sample_matrix if not r.get("ok")]},
        )
        _write_json(out_root / "paddleocr_benchmark_audit_report.json", audit)

        notes = "\n".join(
            [
                "# PaddleOCR Evaluation Benchmark v0",
                "",
                f"- **benchmark_verdict**: `{verdict}`",
                f"- **output_root**: `{out_root}`",
                "",
                "- Max 20 samples; no model download; no cache mutation; no routing.",
                "",
            ]
        )
        (out_root / "paddleocr_benchmark_notes.md").write_text(notes, encoding="utf-8")

        print(json.dumps({"benchmark_output_root": str(out_root), "benchmark_verdict": verdict}, ensure_ascii=False))
        return_code = 0 if verdict != "NO_GO" else 2
    finally:
        _restore_urlopen(orig_open)

    return return_code


if __name__ == "__main__":
    raise SystemExit(main())

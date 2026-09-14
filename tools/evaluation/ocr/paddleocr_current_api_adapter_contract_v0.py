#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-API-Adapter-Contract-001 — Evaluation-only PaddleOCR current API adapter contract.

Maps pinned manifest → constructor kwargs, prefers predict(), normalizes outputs to minimal OCR evidence.
No mainline, no routing, no RapidOCR replacement, no MidPlatform.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
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


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _hash_model_trees(model_dirs: List[Path]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for root in model_dirs:
        if not root.is_dir():
            continue
        for p in sorted(root.rglob("*")):
            if p.is_file():
                out[str(p.resolve())] = _sha256_file(p)
    return out


def _install_network_probe(flag_holder: Dict[str, bool]) -> Callable[..., Any]:
    orig_urlopen = urllib.request.urlopen

    def wrapped_urlopen(*a: Any, **kw: Any) -> Any:
        flag_holder["network_request_invoked"] = True
        return orig_urlopen(*a, **kw)

    urllib.request.urlopen = wrapped_urlopen  # type: ignore[assignment]
    return orig_urlopen


def _restore_urlopen(orig: Callable[..., Any]) -> None:
    urllib.request.urlopen = orig  # type: ignore[assignment]


def _filter_init_kwargs(sig_params: Dict[str, Any], candidate: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if "det_model_dir" in sig_params and candidate.get("det_dir"):
        out["det_model_dir"] = candidate["det_dir"]
    if "rec_model_dir" in sig_params and candidate.get("rec_dir"):
        out["rec_model_dir"] = candidate["rec_dir"]
    if "cls_model_dir" in sig_params and candidate.get("cls_dir"):
        out["cls_model_dir"] = candidate["cls_dir"]
    if "text_detection_model_dir" in sig_params and candidate.get("det_dir"):
        out["text_detection_model_dir"] = candidate["det_dir"]
    if "text_recognition_model_dir" in sig_params and candidate.get("rec_dir"):
        out["text_recognition_model_dir"] = candidate["rec_dir"]
    if "textline_orientation_model_dir" in sig_params and candidate.get("cls_dir"):
        out["textline_orientation_model_dir"] = candidate["cls_dir"]
    if "use_textline_orientation" in sig_params and "use_angle_cls" in candidate:
        out["use_textline_orientation"] = bool(candidate["use_angle_cls"])
    if "use_doc_orientation_classify" in sig_params:
        out["use_doc_orientation_classify"] = False
    if "use_doc_unwarping" in sig_params:
        out["use_doc_unwarping"] = False
    if "show_log" in sig_params:
        out["show_log"] = False
    if "use_angle_cls" in sig_params and "use_angle_cls" in candidate:
        out["use_angle_cls"] = bool(candidate["use_angle_cls"])
    if "lang" in sig_params and candidate.get("lang"):
        out["lang"] = candidate["lang"]
    if "use_gpu" in sig_params:
        out["use_gpu"] = bool(candidate.get("use_gpu", False))
    if "device" in sig_params and candidate.get("device"):
        out["device"] = candidate["device"]
    return out


def _to_jsonable(x: Any, depth: int = 0) -> Any:
    if depth > 30:
        return "<max_depth>"
    if x is None or isinstance(x, (bool, int, float, str)):
        return x
    if isinstance(x, (list, tuple)):
        return [_to_jsonable(v, depth + 1) for v in x[:500]]
    if isinstance(x, dict):
        return {str(k): _to_jsonable(v, depth + 1) for k, v in list(x.items())[:200]}
    mod = type(x).__module__
    if mod == "numpy" and hasattr(x, "tolist"):
        try:
            return x.tolist()
        except Exception:
            return repr(x)[:400]
    if hasattr(x, "detach") and callable(x.detach):  # torch tensor sketch
        try:
            return x.detach().cpu().numpy().tolist()  # type: ignore[no-any-return]
        except Exception:
            return repr(x)[:400]
    return repr(x)[:400]


def _poly_to_list(poly: Any) -> Optional[List[Any]]:
    if poly is None:
        return None
    if hasattr(poly, "tolist"):
        try:
            return poly.tolist()  # type: ignore[no-any-return]
        except Exception:
            pass
    if isinstance(poly, (list, tuple)):
        return list(poly)
    return None


def _raw_contains_rec_texts(raw: Any) -> bool:
    """True if raw (dict, list, or nested mix) contains non-empty rec_texts lists."""
    if isinstance(raw, dict):
        rt = raw.get("rec_texts")
        if isinstance(rt, list) and any(isinstance(t, str) and t.strip() for t in rt):
            return True
        for v in raw.values():
            if _raw_contains_rec_texts(v):
                return True
        return False
    if isinstance(raw, list):
        for item in raw:
            if _raw_contains_rec_texts(item):
                return True
        return False
    return False


def normalize_current_api_result(
    raw: Any,
    *,
    image_path: str,
    duration_ms: float,
    call_method: str,
    error: Any,
) -> Dict[str, Any]:
    text_items: List[Dict[str, Any]] = []
    boxes: List[Any] = []
    scores: List[Any] = []

    blocks: List[Dict[str, Any]] = []
    if isinstance(raw, list):
        for b in raw:
            if isinstance(b, dict):
                blocks.append(b)
    elif isinstance(raw, dict):
        blocks.append(raw)

    for block in blocks:
        texts = block.get("rec_texts")
        if not isinstance(texts, list):
            continue
        sc = block.get("rec_scores") if isinstance(block.get("rec_scores"), list) else []
        polys = block.get("rec_polys")
        if not isinstance(polys, list):
            polys = block.get("dt_polys") if isinstance(block.get("dt_polys"), list) else []
        for i, t in enumerate(texts):
            if not isinstance(t, str):
                continue
            score = sc[i] if i < len(sc) else None
            poly = polys[i] if i < len(polys) else None
            box = _poly_to_list(poly)
            text_items.append({"index": i, "text": t, "score": score, "polygon": box})
            if score is not None:
                scores.append(score)
            if box is not None:
                boxes.append(box)

    text_joined = " ".join(x["text"] for x in text_items if x.get("text"))
    return {
        "schema": "paddleocr_api_adapter_normalized_result_v0",
        "phase": "Phase-PaddleOCR-API-Adapter-Contract-001",
        "provider": "paddleocr",
        "api_family": "current_api",
        "call_method": call_method,
        "image_path": image_path,
        "text_items": text_items,
        "text_joined": text_joined,
        "boxes": boxes if boxes else None,
        "scores": scores if scores else None,
        "duration_ms": round(duration_ms, 2),
        "error": error,
    }


def _invoke_predict_or_ocr(paddle: Any, img_path: Path, use_angle_cls: bool) -> Tuple[Any, str, Optional[str]]:
    fallback_reason: Optional[str] = None
    pred = getattr(paddle, "predict", None)
    if callable(pred):
        try:
            raw = pred(str(img_path))
            return raw, "predict", None
        except TypeError:
            try:
                raw = pred(input=str(img_path))
                return raw, "predict", None
            except Exception as e:
                fallback_reason = f"predict_typeerror:{type(e).__name__}:{e}"
        except Exception as e:
            fallback_reason = f"predict_failed:{type(e).__name__}:{e}"
    else:
        fallback_reason = "predict_not_callable"

    try:
        raw = paddle.ocr(str(img_path), cls=use_angle_cls)
    except TypeError:
        raw = paddle.ocr(str(img_path))
    return raw, "ocr_fallback", fallback_reason or "ocr_fallback_default"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--materialize-root", required=True)
    ap.add_argument("--pinned-manifest", required=True)
    ap.add_argument("--trial-root", default="", help="Optional prior controlled trial root for provenance.")
    ap.add_argument("--output-root", default="")
    ap.add_argument("--constructor-only", action="store_true")
    ap.add_argument("--no-use-angle-cls", action="store_true")
    ap.add_argument("--image", action="append", default=[])
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    mat_root = _require_abs(args.materialize_root, "--materialize-root")
    pinned_path = _require_abs(args.pinned_manifest, "--pinned-manifest")
    trial_root = _require_abs(args.trial_root, "--trial-root") if args.trial_root.strip() else None

    if args.output_root.strip():
        out_root = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out_root = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_api_adapter_contract_001_{stamp}").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    mat_sum_p = mat_root / "paddleocr_manifest_v1_cache_materialize_summary.json"
    if not mat_sum_p.is_file():
        raise SystemExit(f"ERROR: missing {mat_sum_p}")
    mat_sum = json.loads(mat_sum_p.read_text(encoding="utf-8"))
    if mat_sum.get("materialize_verdict") != "GO":
        raise SystemExit(f"ERROR: materialize_verdict must be GO, got {mat_sum.get('materialize_verdict')}")

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
    model_dirs = [Path(det_path), Path(rec_path), Path(cls_path)] if det_path and rec_path and cls_path else []

    net_flag: Dict[str, bool] = {"network_request_invoked": False}
    orig_open = _install_network_probe(net_flag)
    try:
        return _run_body(
            args=args,
            repo=repo,
            mat_root=mat_root,
            pinned_path=pinned_path,
            trial_root=trial_root,
            out_root=out_root,
            mat_sum=mat_sum,
            pinned=pinned,
            det_path=det_path,
            rec_path=rec_path,
            cls_path=cls_path,
            use_angle_cls=use_angle_cls,
            lang=lang,
            device=device,
            model_dirs=model_dirs,
            net_flag=net_flag,
        )
    finally:
        _restore_urlopen(orig_open)


def _run_body(
    *,
    args: argparse.Namespace,
    repo: Path,
    mat_root: Path,
    pinned_path: Path,
    trial_root: Optional[Path],
    out_root: Path,
    mat_sum: Dict[str, Any],
    pinned: Dict[str, Any],
    det_path: Any,
    rec_path: Any,
    cls_path: Any,
    use_angle_cls: bool,
    lang: str,
    device: str,
    model_dirs: List[Path],
    net_flag: Dict[str, bool],
) -> int:
    errors: List[Dict[str, Any]] = []
    constructor_report: Dict[str, Any] = {
        "schema": "paddleocr_api_adapter_constructor_report_v0",
        "phase": "Phase-PaddleOCR-API-Adapter-Contract-001",
        "paddleocr_import_ok": False,
        "constructor_ok": False,
        "constructor_exception": None,
        "constructor_traceback": None,
        "init_kwargs_effective": {},
        "init_signature_parameter_names": [],
        "use_angle_cls_requested": use_angle_cls,
        "det_path": det_path,
        "rec_path": rec_path,
        "cls_path": cls_path,
        "cls_compatibility_note": (
            "cls directory may be PP-LCNet_x1_0_textline_ori; not equivalent to classic ch_ppocr_mobile_v2.0_cls."
        ),
    }

    pre_hashes: Dict[str, str] = {}
    post_hashes: Dict[str, str] = {}
    try:
        pre_hashes = _hash_model_trees(model_dirs)
    except Exception as e:
        errors.append({"phase": "pre_hash", "error": str(e)})

    paddle = None
    try:
        from paddleocr import PaddleOCR
        import inspect

        constructor_report["paddleocr_import_ok"] = True
        sig = inspect.signature(PaddleOCR.__init__)
        param_names = [k for k in sig.parameters.keys() if k != "self"]
        constructor_report["init_signature_parameter_names"] = param_names
        cand_kw = {
            "det_dir": det_path,
            "rec_dir": rec_path,
            "cls_dir": cls_path,
            "use_angle_cls": use_angle_cls,
            "lang": lang,
            "use_gpu": device.lower() in ("gpu", "cuda"),
            "device": device,
        }
        init_kwargs = _filter_init_kwargs({k: True for k in param_names}, cand_kw)
        constructor_report["init_kwargs_effective"] = init_kwargs
        paddle = PaddleOCR(**init_kwargs)
        constructor_report["constructor_ok"] = True
    except Exception as e:
        constructor_report["constructor_ok"] = False
        constructor_report["constructor_exception"] = f"{type(e).__name__}: {e}"
        constructor_report["constructor_traceback"] = traceback.format_exc()
        errors.append({"phase": "constructor", "error": constructor_report["constructor_exception"]})

    images = [_require_abs(p, f"--image[{i}]") for i, p in enumerate(args.image)]
    if len(images) > 3:
        errors.append({"phase": "args", "error": f"too_many_images:{len(images)}"})

    call_rows: List[Dict[str, Any]] = []
    normalized_results: List[Dict[str, Any]] = []
    raw_bundle: List[Dict[str, Any]] = []

    too_many = any("too_many_images" in str(e.get("error", "")) for e in errors)

    if paddle is not None and not args.constructor_only and images and not too_many:
        for img in images[:3]:
            t0 = time.perf_counter()
            row: Dict[str, Any] = {
                "image": str(img),
                "call_method": None,
                "fallback_reason": None,
                "duration_ms": None,
                "ok": False,
                "error": None,
            }
            try:
                raw, method, fb = _invoke_predict_or_ocr(paddle, img, use_angle_cls)
                dt = (time.perf_counter() - t0) * 1000.0
                row["call_method"] = method
                row["fallback_reason"] = fb
                row["duration_ms"] = round(dt, 2)
                row["ok"] = True
                raw_json = _to_jsonable(raw)
                raw_bundle.append({"image": str(img), "raw": raw_json})
                norm = normalize_current_api_result(
                    raw,
                    image_path=str(img),
                    duration_ms=dt,
                    call_method=method,
                    error=None,
                )
                norm["fallback_reason"] = fb
                normalized_results.append(norm)
            except Exception as e:
                row["error"] = f"{type(e).__name__}: {e}"
                row["traceback"] = traceback.format_exc()
                errors.append({"phase": "inference", "image": str(img), "error": row["error"]})
                normalized_results.append(
                    normalize_current_api_result(
                        None,
                        image_path=str(img),
                        duration_ms=(time.perf_counter() - t0) * 1000.0,
                        call_method="none",
                        error=row["error"],
                    )
                )
            call_rows.append(row)

    try:
        post_hashes = _hash_model_trees(model_dirs)
    except Exception as e:
        errors.append({"phase": "post_hash", "error": str(e)})

    model_cache_unchanged = pre_hashes == post_hashes and bool(pre_hashes)
    audit = {
        "schema": "paddleocr_api_adapter_audit_report_v0",
        "phase": "Phase-PaddleOCR-API-Adapter-Contract-001",
        "network_request_invoked": bool(net_flag["network_request_invoked"]),
        "ocr_routing_changed": False,
        "rapidocr_replaced": False,
        "runtime_integration": False,
        "whitebox_integration": False,
        "midplatform_invoked": False,
        "mainline_touched": False,
        "model_cache_modified": not model_cache_unchanged,
        "sample_count": len(images[:3]),
        "constructor_only": bool(args.constructor_only),
    }

    adapter_verdict = "NO_GO"
    if too_many:
        adapter_verdict = "NO_GO"
    elif not constructor_report["constructor_ok"]:
        adapter_verdict = "NO_GO"
    elif args.constructor_only or not images:
        adapter_verdict = "CONDITIONAL_GO"
    else:
        adapter_verdict = "GO"
        for i, img in enumerate(images[:3]):
            raw_entry = raw_bundle[i] if i < len(raw_bundle) else {}
            raw_obj = raw_entry.get("raw") if isinstance(raw_entry, dict) else None
            raw_has = _raw_contains_rec_texts(raw_obj) if raw_obj is not None else False
            norm = normalized_results[i] if i < len(normalized_results) else {}
            joined = (norm.get("text_joined") or "").strip()
            if raw_has and not joined:
                adapter_verdict = "CONDITIONAL_GO"
                errors.append(
                    {
                        "phase": "normalization",
                        "image": str(img),
                        "error": "raw_has_rec_texts_but_normalized_empty",
                    }
                )
                break
        for row in call_rows:
            if not row.get("ok"):
                adapter_verdict = "NO_GO"

    if audit["network_request_invoked"] or audit["model_cache_modified"]:
        adapter_verdict = "NO_GO"

    summary = {
        "schema": "paddleocr_api_adapter_contract_summary_v0",
        "phase": "Phase-PaddleOCR-API-Adapter-Contract-001",
        "adapter_contract_verdict": adapter_verdict,
        "repo_root": str(repo),
        "materialize_root": str(mat_root),
        "trial_root": str(trial_root) if trial_root else None,
        "pinned_manifest": str(pinned_path),
        "output_root": str(out_root),
        "constructor_only": bool(args.constructor_only),
        "audit": audit,
        "errors": errors,
    }

    _write_json(out_root / "paddleocr_api_adapter_constructor_report.json", constructor_report)
    _write_json(
        out_root / "paddleocr_api_adapter_call_report.json",
        {"schema": "paddleocr_api_adapter_call_report_v0", "calls": call_rows},
    )
    _write_json(out_root / "paddleocr_api_adapter_raw_result.json", {"results": raw_bundle})
    _write_json(out_root / "paddleocr_api_adapter_normalized_result.json", {"results": normalized_results})
    _write_json(out_root / "paddleocr_api_adapter_error_report.json", {"errors": errors})
    _write_json(out_root / "paddleocr_api_adapter_audit_report.json", audit)
    _write_json(out_root / "paddleocr_api_adapter_contract_summary.json", summary)

    notes = "\n".join(
        [
            "# PaddleOCR API Adapter Contract v0",
            "",
            f"- **adapter_contract_verdict**: `{adapter_verdict}`",
            f"- **output_root**: `{out_root}`",
            "",
            "- Normalization targets `rec_texts` / `rec_scores` / `rec_polys` on current_api dict blocks.",
            "- `predict` preferred; `ocr` as controlled fallback.",
            "",
        ]
    )
    (out_root / "paddleocr_api_adapter_notes.md").write_text(notes, encoding="utf-8")

    print(json.dumps({"adapter_output_root": str(out_root), "adapter_contract_verdict": adapter_verdict}, ensure_ascii=False))
    return 0 if adapter_verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

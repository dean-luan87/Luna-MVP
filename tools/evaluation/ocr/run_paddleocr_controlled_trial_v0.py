#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Controlled-Trial-001 — Offline controlled constructor + minimal OCR trial.

Independent evaluation phase: may instantiate PaddleOCR and run ocr() on <=3 local images.
Does not change mainline routing, RapidOCR, or MidPlatform.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import sys
import time
import traceback
import urllib.request
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

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


def _install_network_probe(flag_holder: Dict[str, bool]) -> Tuple[Callable[..., Any], Callable[..., Any]]:
    orig_urlopen = urllib.request.urlopen

    def wrapped_urlopen(*a: Any, **kw: Any) -> Any:
        flag_holder["network_request_invoked"] = True
        return orig_urlopen(*a, **kw)

    urllib.request.urlopen = wrapped_urlopen  # type: ignore[assignment]
    return orig_urlopen, wrapped_urlopen


def _restore_urlopen(orig: Callable[..., Any]) -> None:
    urllib.request.urlopen = orig  # type: ignore[assignment]


def _filter_init_kwargs(sig_params: Dict[str, Any], candidate: Dict[str, Any]) -> Dict[str, Any]:
    """Map manifest paths to PaddleOCR __init__ names when present (legacy + current API)."""
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


def _normalize_ocr_item(raw: Any) -> Any:
    """Best-effort JSON-serializable minimal view."""
    if raw is None:
        return None
    if isinstance(raw, (str, int, float, bool)):
        return raw
    if isinstance(raw, (list, tuple)):
        return [_normalize_ocr_item(x) for x in raw[:200]]
    if isinstance(raw, dict):
        return {str(k): _normalize_ocr_item(v) for k, v in list(raw.items())[:50]}
    return repr(raw)[:500]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--materialize-root", required=True)
    ap.add_argument("--pinned-manifest", required=True)
    ap.add_argument("--output-root", default="", help="Absolute output root; default under ~/LunaRuntime/logs/evaluation/")
    ap.add_argument("--constructor-only", action="store_true")
    ap.add_argument(
        "--no-use-angle-cls",
        action="store_true",
        help="Force use_angle_cls=false when supported (default: use_angle_cls=true).",
    )
    ap.add_argument("--image", action="append", default=[], help="Absolute path to test image; repeat up to 3 times.")
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    mat_root = _require_abs(args.materialize_root, "--materialize-root")
    pinned_path = _require_abs(args.pinned_manifest, "--pinned-manifest")

    if args.output_root.strip():
        out_root = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out_root = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_controlled_trial_001_{stamp}").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    mat_sum_p = mat_root / "paddleocr_manifest_v1_cache_materialize_summary.json"
    if not mat_sum_p.is_file():
        raise SystemExit(f"ERROR: materialize summary missing: {mat_sum_p}")
    mat_sum = json.loads(mat_sum_p.read_text(encoding="utf-8"))

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
    orig_open, _ = _install_network_probe(net_flag)
    try:
        return _main_body(
            args=args,
            repo=repo,
            mat_root=mat_root,
            pinned_path=pinned_path,
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


def _main_body(
    *,
    args: argparse.Namespace,
    repo: Path,
    mat_root: Path,
    pinned_path: Path,
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
    if mat_sum.get("materialize_verdict") != "GO":
        errors.append(
            {
                "phase": "preflight",
                "error": f"materialize_verdict_not_go:{mat_sum.get('materialize_verdict')}",
            }
        )

    constructor_report: Dict[str, Any] = {
        "schema": "paddleocr_controlled_trial_constructor_report_v0",
        "phase": "Phase-PaddleOCR-Controlled-Trial-001",
        "paddleocr_import_ok": False,
        "constructor_invoked": False,
        "constructor_ok": False,
        "constructor_exception": None,
        "constructor_traceback": None,
        "init_kwargs_effective": {},
        "init_signature_parameter_names": [],
        "use_angle_cls_requested": use_angle_cls,
        "cls_path": cls_path,
        "cls_compatibility_note": (
            "Pinned cls tree may be PP-LCNet_x1_0_textline_ori (PaddleX textline orientation), "
            "not necessarily classic ch_ppocr_mobile_v2.0_cls angle classifier; runtime compatibility is trial-owned."
        ),
        "det_path": det_path,
        "rec_path": rec_path,
        "device": device,
        "lang": lang,
    }

    ocr_raw: List[Dict[str, Any]] = []
    ocr_norm: List[Dict[str, Any]] = []
    pre_hashes: Dict[str, str] = {}
    post_hashes: Dict[str, str] = {}

    try:
        pre_hashes = _hash_model_trees(model_dirs)
    except Exception as e:
        errors.append({"phase": "pre_hash_model_trees", "error": f"{type(e).__name__}: {e}"})

    paddle = None
    if mat_sum.get("materialize_verdict") != "GO":
        constructor_report["constructor_exception"] = "skipped:materialize_verdict_not_go"
    else:
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

            constructor_report["constructor_invoked"] = True
            paddle = PaddleOCR(**init_kwargs)
            constructor_report["constructor_ok"] = True
        except Exception as e:
            constructor_report["constructor_ok"] = False
            constructor_report["constructor_exception"] = f"{type(e).__name__}: {e}"
            constructor_report["constructor_traceback"] = traceback.format_exc()
            errors.append({"phase": "constructor", "error": constructor_report["constructor_exception"]})

    trial_verdict = "NO_GO"
    if constructor_report["constructor_ok"]:
        trial_verdict = "CONDITIONAL_GO" if args.constructor_only else "GO"
    else:
        trial_verdict = "NO_GO"

    images = [_require_abs(p, f"--image[{i}]") for i, p in enumerate(args.image)]
    if len(images) > 3:
        errors.append({"phase": "args", "error": f"too_many_images:{len(images)}"})
        trial_verdict = "NO_GO"

    if not args.constructor_only:
        if not constructor_report["constructor_ok"]:
            trial_verdict = "NO_GO"
            errors.append({"phase": "ocr_skipped", "error": "constructor_failed"})
        elif not images:
            trial_verdict = "CONDITIONAL_GO"
            errors.append({"phase": "ocr", "error": "no_images_provided_for_ocr_layer"})
        elif paddle is not None:
            for img in images:
                t0 = time.perf_counter()
                entry: Dict[str, Any] = {"image": str(img), "ok": False, "duration_ms": None, "raw_error": None}
                try:
                    try:
                        raw = paddle.ocr(str(img), cls=use_angle_cls)
                    except TypeError:
                        raw = paddle.ocr(str(img))
                    dt = (time.perf_counter() - t0) * 1000.0
                    entry["ok"] = True
                    entry["duration_ms"] = round(dt, 2)
                    entry["raw"] = _normalize_ocr_item(raw)
                    ocr_raw.append(entry)
                    ocr_norm.append(
                        {
                            "image": str(img),
                            "duration_ms": entry["duration_ms"],
                            "text_joined": _extract_joined_text(raw),
                        }
                    )
                except Exception as e:
                    entry["raw_error"] = f"{type(e).__name__}: {e}"
                    entry["traceback"] = traceback.format_exc()
                    errors.append({"phase": "ocr", "image": str(img), "error": entry["raw_error"]})
                    ocr_raw.append(entry)
                    trial_verdict = "CONDITIONAL_GO"

    try:
        post_hashes = _hash_model_trees(model_dirs)
    except Exception as e:
        errors.append({"phase": "post_hash_model_trees", "error": f"{type(e).__name__}: {e}"})

    model_cache_unchanged = pre_hashes == post_hashes and bool(pre_hashes)

    audit = {
        "schema": "paddleocr_controlled_trial_audit_report_v0",
        "phase": "Phase-PaddleOCR-Controlled-Trial-001",
        "network_request_invoked": bool(net_flag["network_request_invoked"]),
        "ocr_routing_changed": False,
        "rapidocr_replaced": False,
        "runtime_integration": False,
        "whitebox_integration": False,
        "midplatform_invoked": False,
        "mainline_touched": False,
        "model_cache_modified": not model_cache_unchanged,
        "sample_count": len(images),
        "constructor_only": bool(args.constructor_only),
    }

    if audit["network_request_invoked"]:
        trial_verdict = "NO_GO"
    if audit["model_cache_modified"]:
        trial_verdict = "NO_GO"
        errors.append({"phase": "integrity", "error": "model_cache_sha_changed_during_trial"})

    if (
        not args.constructor_only
        and constructor_report["constructor_ok"]
        and images
        and ocr_raw
        and all(e.get("ok") for e in ocr_raw)
    ):
        trial_verdict = "GO"

    summary = {
        "schema": "paddleocr_controlled_trial_summary_v0",
        "phase": "Phase-PaddleOCR-Controlled-Trial-001",
        "trial_verdict": trial_verdict,
        "repo_root": str(repo),
        "materialize_root": str(mat_root),
        "pinned_manifest": str(pinned_path),
        "output_root": str(out_root),
        "materialize_verdict_from_input": mat_sum.get("materialize_verdict"),
        "pinning_complete": pinned.get("pinning_complete"),
        "missing_ref_count": pinned.get("missing_ref_count", 0),
        "sha256_entry_count": len(pinned.get("sha256_by_file") or {}),
        "constructor_only": bool(args.constructor_only),
        "audit": audit,
        "errors": errors,
    }

    _write_json(out_root / "paddleocr_controlled_trial_constructor_report.json", constructor_report)
    _write_json(out_root / "paddleocr_controlled_trial_ocr_results_raw.json", {"results": ocr_raw})
    _write_json(out_root / "paddleocr_controlled_trial_ocr_results_normalized.json", {"results": ocr_norm})
    _write_json(out_root / "paddleocr_controlled_trial_error_report.json", {"errors": errors})
    _write_json(out_root / "paddleocr_controlled_trial_audit_report.json", audit)
    _write_json(out_root / "paddleocr_controlled_trial_summary.json", summary)

    notes = [
        "# PaddleOCR Controlled Trial v0",
        "",
        f"- **trial_verdict**: `{trial_verdict}`",
        f"- **materialize_root**: `{mat_root}`",
        f"- **output_root**: `{out_root}`",
        "",
        "## Conservative note (cls)",
        "",
        constructor_report.get("cls_compatibility_note", ""),
        "",
        "## Boundary",
        "",
        "- Not mainline integration; not provider switch; not MidPlatform semantics.",
    ]
    (out_root / "paddleocr_controlled_trial_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")

    print(json.dumps({"trial_output_root": str(out_root), "trial_verdict": trial_verdict}, ensure_ascii=False))
    return 0 if trial_verdict != "NO_GO" else 2


def _extract_joined_text(raw: Any) -> str:
    parts: List[str] = []
    try:
        if isinstance(raw, list):
            for page in raw:
                if page is None:
                    continue
                if isinstance(page, list):
                    for line in page:
                        if isinstance(line, (list, tuple)) and line:
                            cell = line[0]
                            if isinstance(cell, str):
                                parts.append(cell)
                            elif isinstance(cell, (list, tuple)) and cell and isinstance(cell[0], str):
                                parts.append(cell[0])
    except Exception:
        pass
    return " ".join(parts)[:4000]


if __name__ == "__main__":
    raise SystemExit(main())

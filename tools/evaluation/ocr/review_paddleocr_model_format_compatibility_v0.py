#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-ModelFormat-001 — Read-only PaddleOCR model format vs Luna manifest compatibility review.

No model download. No PaddleOCR(). No OCR inference. No routing / mainline changes.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import inspect
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _installed_version_report() -> Dict[str, Any]:
    ver: Optional[str] = None
    dist_error: Optional[str] = None
    try:
        from importlib.metadata import version as md_version

        ver = md_version("paddleocr")
    except Exception as e:
        dist_error = f"{type(e).__name__}: {e}"
    pkg_file: Optional[str] = None
    pkg_ok, import_err = False, None
    try:
        import paddleocr as po

        pkg_ok = True
        pkg_file = getattr(po, "__file__", None)
        if ver is None:
            ver = getattr(po, "__version__", None)
    except Exception as e:
        import_err = f"{type(e).__name__}: {e}"
    return {
        "schema": "paddleocr_installed_version_report_v0",
        "phase": "Phase-PaddleOCR-ModelFormat-001",
        "paddleocr_distribution_version": ver,
        "paddleocr_package_import_ok": pkg_ok,
        "paddleocr_package_file": pkg_file,
        "importlib_metadata_error": dist_error,
        "import_error": import_err,
        "policy": "read_only_no_download_no_constructor_no_inference",
    }


def _api_signature_report() -> Dict[str, Any]:
    report: Dict[str, Any] = {
        "schema": "paddleocr_api_signature_report_v0",
        "phase": "Phase-PaddleOCR-ModelFormat-001",
        "paddleocr_class_import_ok": False,
        "paddleocr_class_fqn": "paddleocr.paddleocr.PaddleOCR",
        "init_parameters": {},
        "init_docstring_excerpt": None,
        "init_signature_error": None,
        "policy": "inspect_only_PaddleOCR_class_not_instantiated",
    }
    try:
        from paddleocr import PaddleOCR

        report["paddleocr_class_import_ok"] = True
        try:
            sig = inspect.signature(PaddleOCR.__init__)
            report["init_parameters"] = {
                k: {"kind": str(v.kind), "default": repr(v.default) if v.default is not inspect.Parameter.empty else None}
                for k, v in sig.parameters.items()
                if k != "self"
            }
        except Exception as e:
            report["init_signature_error"] = f"{type(e).__name__}: {e}"
        doc = inspect.getdoc(PaddleOCR) or ""
        excerpt = doc.strip().splitlines()[0] if doc.strip() else None
        if len(doc) > 400:
            doc = doc[:400] + "…"
        report["init_docstring_excerpt"] = excerpt
        report["class_docstring_trimmed"] = doc or None
    except Exception as e:
        report["paddleocr_class_import_error"] = f"{type(e).__name__}: {e}"
    return report


def _load_manifest_expected(repo: Path, rel: str) -> List[Dict[str, Any]]:
    p = repo / rel
    if not p.is_file():
        return []
    doc = json.loads(p.read_text(encoding="utf-8"))
    raw = doc.get("expected_files") or []
    return [x for x in raw if isinstance(x, dict)]


def _keyword_scan_pkg(pkg_root: Optional[Path], keywords: Tuple[str, ...], max_files: int = 120) -> List[Dict[str, Any]]:
    hits: List[Dict[str, Any]] = []
    if not pkg_root or not pkg_root.is_dir():
        return hits
    root = pkg_root
    n = 0
    for py in root.rglob("*.py"):
        if n >= max_files:
            break
        n += 1
        try:
            text = py.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lower = text.lower()
        found = [k for k in keywords if k.lower() in lower]
        if found:
            hits.append({"path": str(py), "keyword_hits": found})
    return hits


def _manifest_format_compatibility_matrix(
    repo: Path,
    manifest_rel: str,
    version_rep: Dict[str, Any],
    api_rep: Dict[str, Any],
) -> Dict[str, Any]:
    expected = _load_manifest_expected(repo, manifest_rel)
    manifest_paths = [str(e.get("relative_path") or "") for e in expected]
    init_params = api_rep.get("init_parameters") or {}
    param_names = list(init_params.keys())

    rows: List[Dict[str, Any]] = [
        {
            "dimension": "luna_manifest_v0",
            "detail": "Expected six files under repo-relative paths: det/rec/cls each with inference.pdmodel + inference.pdiparams (Paddle Inference static graph naming).",
            "alignment_vs_installed_api": "partial",
            "notes": "Typical PaddleOCR __init__ accepts det_model_dir / rec_model_dir / cls_model_dir pointing at directories; those dirs often contain inference.pdmodel + inference.pdiparams for PP-OCRv3/v4 style releases.",
        },
        {
            "dimension": "ppocrv5_format_risk",
            "detail": "Community reports: some PP-OCRv5 official bundles may not expose legacy .pdmodel/.pdiparams pairs; formats may include ONNX or other Paddle packaging.",
            "alignment_vs_installed_api": "unknown_requires_manual_confirmation",
            "notes": "Do not assume PP-OCRv5 download satisfies Luna manifest v0 without file-level verification.",
        },
        {
            "dimension": "installed_paddleocr_api_surface",
            "detail": f"PaddleOCR.__init__ parameter names observed: {', '.join(param_names) if param_names else '(none — import or inspect failed)'}",
            "alignment_vs_installed_api": "n/a",
            "notes": "This row is static introspection only; it does not validate weight files on disk.",
        },
        {
            "dimension": "version_pin",
            "detail": f"Distribution/import version: {version_rep.get('paddleocr_distribution_version')!s}",
            "alignment_vs_installed_api": "n/a",
            "notes": "Pin this string in downstream evaluation docs once format route is chosen.",
        },
    ]

    return {
        "schema": "paddleocr_manifest_format_compatibility_matrix_v0",
        "phase": "Phase-PaddleOCR-ModelFormat-001",
        "model_files_manifest_relative": manifest_rel,
        "expected_relative_paths": [p for p in manifest_paths if p],
        "rows": rows,
        "read_only_source_scan_note": "Optional keyword scan of installed paddleocr *.py is heuristic only.",
    }


def _route_options() -> Dict[str, Any]:
    return {
        "schema": "paddleocr_model_format_route_options_v0",
        "phase": "Phase-PaddleOCR-ModelFormat-001",
        "routes": [
            {
                "id": "A",
                "title": "Legacy Paddle Inference six-file layout",
                "summary": "Keep current Luna manifest; acquire det/rec/cls folders each containing inference.pdmodel + inference.pdiparams compatible with PaddleOCR det_model_dir/rec_model_dir/cls_model_dir.",
                "pros": ["Hash-pin friendly", "Aligns with existing Weights-001/002/003 tooling"],
                "cons": ["PP-OCRv5 official bundles may not ship this layout"],
            },
            {
                "id": "B",
                "title": "New-format PaddleOCR model dir / upstream download route",
                "summary": "Adapt manifest + prepare/snapshot tooling to the format PaddleOCR actually loads for PP-OCRv5 (e.g. ONNX or new Paddle save format), and document __init__ parameters accordingly.",
                "pros": ["Matches upstream evolution"],
                "cons": ["Requires manifest v1 + adapter changes + new pin strategy"],
            },
            {
                "id": "C",
                "title": "Evaluation candidate downgrade to PP-OCRv4 / PP-OCRv3 inference packs",
                "summary": "Keep legacy manifest for evaluation-only Paddle path; pin PP-OCRv4/v3 inference trees that are known to expose .pdmodel/.pdiparams pairs.",
                "pros": ["Fast path to CONDITIONAL_GO → GO on weights tooling without fighting v5 packaging"],
                "cons": ["Not PP-OCRv5 headline capability"],
            },
        ],
    }


def _constraints_template() -> Dict[str, Any]:
    return {
        "network_download_invoked": False,
        "paddleocr_constructor_invoked": False,
        "paddleocr_inference_invoked": False,
        "ocr_routing_changed": False,
        "rapidocr_replaced": False,
        "runtime_integration": False,
        "whitebox_integration": False,
        "mainline_side_effect": False,
        "midplatform_invoked": False,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument(
        "--model-files-manifest",
        default="configs/models/ocr/paddleocr_ppocrv5_model_files_manifest_v0.json",
        help="Repo-relative manifest describing expected weight files.",
    )
    ap.add_argument("--output-root", default="")
    ap.add_argument("--keyword-scan-max-files", type=int, default=120)
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_model_format_review_001_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    version_rep = _installed_version_report()
    api_rep = _api_signature_report()
    matrix = _manifest_format_compatibility_matrix(repo, args.model_files_manifest.strip(), version_rep, api_rep)
    routes = _route_options()

    pkg_file = version_rep.get("paddleocr_package_file")
    pkg_root = Path(pkg_file).resolve().parent if isinstance(pkg_file, str) and pkg_file else None
    keywords = ("inference.pdmodel", "inference.pdiparams", "onnx", "pdmodel", "pir", "paddle_infer")
    scan_hits = _keyword_scan_pkg(pkg_root, keywords, max_files=max(1, args.keyword_scan_max_files))
    matrix["installed_package_keyword_scan"] = {
        "pkg_root": str(pkg_root) if pkg_root else None,
        "max_files_scanned_cap": args.keyword_scan_max_files,
        "hits_sample": scan_hits[:40],
        "hit_count": len(scan_hits),
    }

    _write_json(out / "paddleocr_installed_version_report.json", version_rep)
    _write_json(out / "paddleocr_api_signature_report.json", api_rep)
    _write_json(out / "paddleocr_manifest_format_compatibility_matrix.json", matrix)
    _write_json(out / "paddleocr_model_format_route_options.json", routes)

    api_ok = bool(api_rep.get("paddleocr_class_import_ok")) and bool(api_rep.get("init_parameters"))
    ver_ok = bool(version_rep.get("paddleocr_package_import_ok")) or bool(version_rep.get("paddleocr_distribution_version"))
    review_verdict = "GO" if api_ok and ver_ok else "CONDITIONAL_GO"

    summary = {
        "schema": "paddleocr_model_format_review_summary_v0",
        "phase": "Phase-PaddleOCR-ModelFormat-001",
        "repo_root": str(repo),
        "output_root": str(out),
        "model_files_manifest_relative": args.model_files_manifest.strip(),
        "review_verdict": review_verdict,
        "review_posture": "GO_static_introspection_ok"
        if review_verdict == "GO"
        else "CONDITIONAL_GO_partial_or_missing_paddleocr_install",
        "frozen_inputs": {
            "paddleocr_readiness_001": "GO (prior phase; not re-run here)",
            "paddleocr_weights_003": "CONDITIONAL_GO (prior fact: no local inference.pdmodel/pdiparams pairs found)",
            "manifest_expectation": "Legacy Paddle Inference six-file tree per paddleocr_ppocrv5_model_files_manifest_v0.json",
        },
        "constraints": _constraints_template(),
        "artifacts": {
            "paddleocr_model_format_review_summary.json": str(out / "paddleocr_model_format_review_summary.json"),
            "paddleocr_installed_version_report.json": str(out / "paddleocr_installed_version_report.json"),
            "paddleocr_api_signature_report.json": str(out / "paddleocr_api_signature_report.json"),
            "paddleocr_manifest_format_compatibility_matrix.json": str(out / "paddleocr_manifest_format_compatibility_matrix.json"),
            "paddleocr_model_format_route_options.json": str(out / "paddleocr_model_format_route_options.json"),
            "paddleocr_model_format_review_notes.md": str(out / "paddleocr_model_format_review_notes.md"),
        },
    }
    _write_json(out / "paddleocr_model_format_review_summary.json", summary)

    notes = out / "paddleocr_model_format_review_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# PaddleOCR Model Format Compatibility Review v0（Phase-PaddleOCR-ModelFormat-001）",
                "",
                f"- **output_root**: `{out}`",
                "",
                "## 边界",
                "",
                "- **不**下载模型、**不** `PaddleOCR()`、**不** OCR 推理、**不**改 OCR routing / 主线 / 白盒 / MidPlatform。",
                "",
                "## 冻结事实（输入）",
                "",
                "- Weights-003 本地发现链：**未发现**成对 `inference.pdmodel` / `inference.pdiparams`；`missing_count = 6`；completion **CONDITIONAL_GO**。",
                "- 当前 Luna manifest v0：**旧式** Paddle Inference 六文件结构。",
                "",
                "## 本工具产出",
                "",
                "- 已安装 **paddleocr** 版本信息（distribution / import）。",
                "- **`PaddleOCR.__init__` 签名**（仅 `inspect`，不实例化）。",
                "- **manifest vs 格式风险** 兼容性矩阵 + **A/B/C 路线选项** JSON。",
                "- 可选：对 site-packages 内 `paddleocr` 的 `*.py` 做**只读**关键字抽样扫描（启发式，非证明）。",
                "",
                f"- **review_verdict**: `{review_verdict}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "review_verdict": review_verdict}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

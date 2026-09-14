#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-ManifestV1-Design-001 — Manifest v1 design review (read-only).

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
from typing import Any, Dict, List

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


def _constraints() -> Dict[str, Any]:
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


def _paddleocr_init_params() -> Dict[str, Any]:
    out: Dict[str, Any] = {"import_ok": False, "init_parameters": {}, "error": None}
    try:
        from paddleocr import PaddleOCR

        out["import_ok"] = True
        sig = inspect.signature(PaddleOCR.__init__)
        out["init_parameters"] = {k: str(v) for k, v in sig.parameters.items() if k != "self"}
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {e}"
    return out


def _field_matrix(example: Dict[str, Any], init_params: Dict[str, Any]) -> Dict[str, Any]:
    init_keys = list((init_params.get("init_parameters") or {}).keys())
    rows: List[Dict[str, Any]] = [
        {
            "v1_field": "provider_id",
            "purpose": "Stable evaluation / adapter routing id",
            "maps_to_paddleocr_init": [],
            "placeholder": False,
        },
        {
            "v1_field": "model_format",
            "purpose": "paddleocr_current_api vs paddle_inference_legacy",
            "maps_to_paddleocr_init": [],
            "placeholder": False,
        },
        {
            "v1_field": "model_root",
            "purpose": "Offline cache root (repo-relative or abs evaluation-only)",
            "maps_to_paddleocr_init": ["implicit_prefix_for_det_rec_cls_dirs"],
            "placeholder": "<PLACEHOLDER" in str(example.get("model_root") or ""),
        },
        {
            "v1_field": "det_model_ref",
            "purpose": "Detection model directory or name under model_root",
            "maps_to_paddleocr_init": ["det_model_dir"] if "det_model_dir" in init_keys else ["det_model_dir?"],
            "placeholder": "<PLACEHOLDER" in str(example.get("det_model_ref") or ""),
        },
        {
            "v1_field": "rec_model_ref",
            "purpose": "Recognition model directory or name",
            "maps_to_paddleocr_init": ["rec_model_dir"] if "rec_model_dir" in init_keys else ["rec_model_dir?"],
            "placeholder": "<PLACEHOLDER" in str(example.get("rec_model_ref") or ""),
        },
        {
            "v1_field": "cls_model_ref",
            "purpose": "Angle classifier model directory or name",
            "maps_to_paddleocr_init": ["cls_model_dir"] if "cls_model_dir" in init_keys else ["cls_model_dir?"],
            "placeholder": "<PLACEHOLDER" in str(example.get("cls_model_ref") or ""),
        },
        {
            "v1_field": "offline_cache_required",
            "purpose": "Evaluation must be reproducible without network",
            "maps_to_paddleocr_init": [],
            "placeholder": False,
        },
        {
            "v1_field": "network_required",
            "purpose": "Whether provider expects HTTPS model fetch",
            "maps_to_paddleocr_init": [],
            "placeholder": False,
        },
        {
            "v1_field": "sha256_required",
            "purpose": "Pin weights for A/B and regression",
            "maps_to_paddleocr_init": [],
            "placeholder": False,
        },
        {
            "v1_field": "legacy_manifest_ref",
            "purpose": "Pointer to v0 readiness manifest (dual-track)",
            "maps_to_paddleocr_init": [],
            "placeholder": False,
        },
    ]
    return {
        "schema": "paddleocr_manifest_v1_field_matrix_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-Design-001",
        "paddleocr_init_parameter_names_observed": init_keys,
        "rows": rows,
    }


def _legacy_matrix(repo: Path, example: Dict[str, Any]) -> Dict[str, Any]:
    leg = str(example.get("legacy_manifest_ref") or "").strip()
    leg_mf = str(example.get("legacy_model_files_manifest_ref") or "").strip()
    v0_ready: Dict[str, Any] = {}
    v0_files: Dict[str, Any] = {}
    if leg and (repo / leg).is_file():
        v0_ready = json.loads((repo / leg).read_text(encoding="utf-8"))
    if leg_mf and (repo / leg_mf).is_file():
        v0_files = json.loads((repo / leg_mf).read_text(encoding="utf-8"))
    return {
        "schema": "paddleocr_legacy_manifest_compatibility_matrix_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-Design-001",
        "legacy_readiness_relative": leg or None,
        "legacy_model_files_relative": leg_mf or None,
        "v0_readiness_keys_sample": sorted(v0_ready.keys()) if v0_ready else [],
        "v0_expected_file_count": len(v0_files.get("expected_files") or []) if v0_files else 0,
        "rows": [
            {
                "topic": "det/rec/cls paths",
                "v0": "det_model_dir / rec_model_dir / cls_model_dir in readiness manifest",
                "v1": "model_root + det_model_ref / rec_model_ref / cls_model_ref (composable to *_model_dir)",
            },
            {
                "topic": "weight file shape",
                "v0": "Six-file paddle_inference_legacy (inference.pdmodel + inference.pdiparams)",
                "v1": "model_format discriminant; current_api may omit legacy filenames",
            },
            {
                "topic": "weights tooling",
                "v0": "run_paddleocr_weights_snapshot_v0 binds to paddleocr_ppocrv5_model_files_manifest_v0",
                "v1": "New snapshot/prepare schema in a later phase (not in Design-001)",
            },
        ],
    }


def _route_matrix() -> Dict[str, Any]:
    return {
        "schema": "paddleocr_manifest_route_decision_matrix_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-Design-001",
        "design_bias_note": "Product preference: align manifest v1 with current PaddleOCR API / ecosystem (ModelFormat route B) while keeping legacy manifest as optional route.",
        "rows": [
            {
                "route_id": "A",
                "manifest_model_format": "paddle_inference_legacy",
                "summary": "Keep v0 six-file expectation; use legacy_manifest_ref as primary.",
                "weights_tooling": "Existing Weights-001/002/003",
            },
            {
                "route_id": "B",
                "manifest_model_format": "paddleocr_current_api",
                "summary": "v1 primary; model_root + refs map to PaddleOCR.__init__ dirs; new pin tooling later.",
                "weights_tooling": "New v1 snapshot phase (TBD)",
            },
            {
                "route_id": "C",
                "manifest_model_format": "paddle_inference_legacy",
                "summary": "PP-OCRv4/v3 legacy inference packs as evaluation candidate; v1 model_version pin.",
                "weights_tooling": "Legacy tooling with updated manifest paths in later phase",
            },
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument(
        "--v1-example-relative",
        default="configs/models/ocr/paddleocr_current_api_model_manifest_v1.example.json",
    )
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    ex_path = repo / args.v1_example_relative.strip()
    if not ex_path.is_file():
        raise SystemExit(f"ERROR: v1 example not found: {ex_path}")

    example = json.loads(ex_path.read_text(encoding="utf-8"))
    init_rep = _paddleocr_init_params()
    field_m = _field_matrix(example, init_rep)
    leg_m = _legacy_matrix(repo, example)
    route_m = _route_matrix()

    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_manifest_v1_design_001_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    api_partial = not init_rep.get("import_ok") or not init_rep.get("init_parameters")
    leg_rel = str(example.get("legacy_manifest_ref") or "").strip()
    legacy_ok = bool(leg_rel) and (repo / leg_rel).is_file()
    review_verdict = "CONDITIONAL_GO" if (api_partial or not legacy_ok) else "GO"

    summary = {
        "schema": "paddleocr_manifest_v1_design_summary_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-Design-001",
        "scope": "manifest_v1_design_review_only",
        "repo_root": str(repo),
        "output_root": str(out),
        "v1_example_relative": args.v1_example_relative.strip(),
        "review_verdict": review_verdict,
        "review_posture": "GO_design_artifacts_complete"
        if review_verdict == "GO"
        else "CONDITIONAL_GO_api_or_legacy_path_partial",
        "frozen_facts": {
            "paddleocr_readiness_001": "GO",
            "paddleocr_weights_003": "CONDITIONAL_GO",
            "paddleocr_model_format_001": "GO",
        },
        "constraints": _constraints(),
        "artifacts": {
            "paddleocr_manifest_v1_design_summary.json": str(out / "paddleocr_manifest_v1_design_summary.json"),
            "paddleocr_manifest_v1_field_matrix.json": str(out / "paddleocr_manifest_v1_field_matrix.json"),
            "paddleocr_legacy_manifest_compatibility_matrix.json": str(
                out / "paddleocr_legacy_manifest_compatibility_matrix.json"
            ),
            "paddleocr_manifest_route_decision_matrix.json": str(out / "paddleocr_manifest_route_decision_matrix.json"),
            "paddleocr_manifest_v1_notes.md": str(out / "paddleocr_manifest_v1_notes.md"),
        },
    }

    _write_json(out / "paddleocr_manifest_v1_field_matrix.json", field_m)
    _write_json(out / "paddleocr_legacy_manifest_compatibility_matrix.json", leg_m)
    _write_json(out / "paddleocr_manifest_route_decision_matrix.json", route_m)
    _write_json(out / "paddleocr_manifest_v1_design_summary.json", summary)

    notes = out / "paddleocr_manifest_v1_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# PaddleOCR Manifest v1 Design Notes（Phase-PaddleOCR-ManifestV1-Design-001）",
                "",
                f"- **output_root**: `{out}`",
                "",
                "## 边界",
                "",
                "- **不**下载、**不** `PaddleOCR()`、**不**推理、**不**改 routing、**不**替换 RapidOCR。",
                "",
                f"- **review_verdict**: `{review_verdict}`",
                "",
                "## v1 example",
                "",
                f"- `{args.v1_example_relative.strip()}`",
                "",
                "## Adapter v1（设计）",
                "",
                "- 见 `docs/architecture/evaluation/LUNA_EVALUATION_OCR_PADDLEOCR_ADAPTER_CONTRACT_V1_DESIGN_V0.md`。",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "review_verdict": review_verdict}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-ManifestV1-CachePrepare-001 — Offline cache prepare plan (no download, no PaddleOCR(), no OCR).

Emits concrete manifest candidate + acquisition plan + directory matrix; does not pin sha256 or claim pinning complete.
"""

from __future__ import annotations

import argparse
import datetime as _dt
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
        "scene_delta_invoked": False,
        "world_context_evidence_invoked": False,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument(
        "--manifest",
        default="configs/models/ocr/paddleocr_current_api_model_manifest_v1.example.json",
        help="Repo-relative v1 example manifest.",
    )
    ap.add_argument(
        "--model-root",
        required=True,
        help="Absolute recommended offline model cache root (e.g. ~/LunaRuntime/models/ocr/paddleocr_current_api_v1).",
    )
    ap.add_argument(
        "--det-ref",
        default="det",
        help="Relative directory name under model_root for detection model cache.",
    )
    ap.add_argument("--rec-ref", default="rec")
    ap.add_argument("--cls-ref", default="cls")
    ap.add_argument(
        "--layout-alias-note",
        default="PP-OCRv5_server_det / PP-OCRv5_server_rec / PP-OCRv5_mobile_cls",
        help="Human note for alternate official directory naming (not applied as paths unless you pass custom --det-ref etc.).",
    )
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    model_root = _require_abs(args.model_root, "--model-root")
    man_path = repo / args.manifest.strip()
    if not man_path.is_file():
        raise SystemExit(f"ERROR: manifest not found: {man_path}")

    example = json.loads(man_path.read_text(encoding="utf-8"))

    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_manifest_v1_cache_prepare_001_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    url_template_repo_rel = "configs/models/ocr/paddleocr_current_api_model_download_urls_v1.example.json"
    url_template_abs = repo / url_template_repo_rel
    if not url_template_abs.is_file():
        raise SystemExit(f"ERROR: URL template must exist in repo: {url_template_abs}")

    det_r, rec_r, cls_r = args.det_ref.strip(), args.rec_ref.strip(), args.cls_ref.strip()
    try:
        source_rel = str(man_path.relative_to(repo))
    except ValueError:
        source_rel = str(man_path)
    candidate: Dict[str, Any] = {
        "schema": "paddleocr_current_api_model_manifest_v1",
        "phase": "Phase-PaddleOCR-ManifestV1-CachePrepare-001",
        "source_example_manifest": source_rel,
        "provider_id": example.get("provider_id") or "paddleocr_current_api_v1",
        "provider_family": example.get("provider_family") or "paddleocr",
        "model_format": "paddleocr_current_api",
        "model_version": "PP-OCRv5",
        "language": example.get("language") or ["zh", "en", "mixed"],
        "model_root": str(model_root),
        "det_model_ref": det_r,
        "rec_model_ref": rec_r,
        "cls_model_ref": cls_r,
        "offline_cache_required": True,
        "network_required": False,
        "download_authorized": False,
        "sha256_required": True,
        "runtime_default_enabled": False,
        "mainline_provider": False,
        "evaluation_candidate": True,
        "legacy_manifest_ref": example.get("legacy_manifest_ref")
        or "configs/models/ocr/paddleocr_evaluation_readiness_manifest_v0.json",
        "legacy_model_files_manifest_ref": example.get("legacy_model_files_manifest_ref")
        or "configs/models/ocr/paddleocr_ppocrv5_model_files_manifest_v0.json",
        "adapter_contract_ref": example.get("adapter_contract_ref")
        or "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PADDLEOCR_ADAPTER_CONTRACT_V1_DESIGN_V0.md",
        "device": example.get("device") or "cpu",
        "route_options": {
            "layout_flat": {"det": det_r, "rec": rec_r, "cls": cls_r},
            "layout_named_servers_note": args.layout_alias_note,
            "note": "If official bundles use PP-OCRv5_* folder names, set --det-ref/--rec-ref/--cls-ref accordingly and re-run this tool.",
        },
        "pinning_complete": False,
        "sha256_by_file": {},
        "notes": "Concrete candidate from CachePrepare-001. Replace model_version and paths after verifying official layout. Do not treat as pinned until run_paddleocr_manifest_v1_snapshot_v0 reports pinning_complete=true.",
    }

    expected_dirs = [
        {"role": "model_root", "path": str(model_root), "purpose": "Offline cache root"},
        {"role": "det", "path": str(model_root / det_r), "purpose": "Detection model directory"},
        {"role": "rec", "path": str(model_root / rec_r), "purpose": "Recognition model directory"},
        {"role": "cls", "path": str(model_root / cls_r), "purpose": "Angle classifier directory"},
    ]
    matrix = {
        "schema": "paddleocr_manifest_v1_expected_directory_matrix_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-CachePrepare-001",
        "rows": expected_dirs,
    }

    manual_steps: List[str] = [
        f"mkdir -p \"{model_root / det_r}\" \"{model_root / rec_r}\" \"{model_root / cls_r}\"",
        f"# Copy official det model files into: {model_root / det_r}",
        f"# Copy official rec model files into: {model_root / rec_r}",
        f"# Copy official cls model files into: {model_root / cls_r}",
        "# Then re-run: run_paddleocr_manifest_v1_snapshot_v0.py with --manifest pointing to this candidate (or a repo copy after review).",
    ]

    acquisition = {
        "schema": "paddleocr_manifest_v1_cache_acquisition_plan_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-CachePrepare-001",
        "target_model_root": str(model_root),
        "required_refs": {"det_model_ref": det_r, "rec_model_ref": rec_r, "cls_model_ref": cls_r},
        "expected_directories": [r["path"] for r in expected_dirs if r["role"] != "model_root"] + [str(model_root)],
        "manual_copy_instructions": manual_steps,
        "authorized_download_required": False,
        "download_completed": False,
        "pinning_complete": False,
        "download_url_manifest_template_ref": url_template_repo_rel,
        "constraints": _constraints(),
    }

    summary = {
        "schema": "paddleocr_manifest_v1_cache_prepare_summary_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-CachePrepare-001",
        "prepare_verdict": "GO",
        "prepare_posture": "GO_concrete_candidate_and_plans_emitted",
        "repo_root": str(repo),
        "output_root": str(out),
        "input_example_manifest": str(man_path),
        "recommended_model_root": str(model_root),
        "human_confirmation_note": "Official PaddleOCR current API directory names may differ; adjust refs before snapshot GO.",
        "constraints": _constraints(),
        "artifacts": {
            "paddleocr_manifest_v1_cache_prepare_summary.json": str(out / "paddleocr_manifest_v1_cache_prepare_summary.json"),
            "paddleocr_current_api_model_manifest_v1.candidate.json": str(out / "paddleocr_current_api_model_manifest_v1.candidate.json"),
            "paddleocr_manifest_v1_cache_acquisition_plan.json": str(out / "paddleocr_manifest_v1_cache_acquisition_plan.json"),
            "paddleocr_manifest_v1_expected_directory_matrix.json": str(out / "paddleocr_manifest_v1_expected_directory_matrix.json"),
            "paddleocr_manifest_v1_manual_copy_instructions.md": str(out / "paddleocr_manifest_v1_manual_copy_instructions.md"),
            "paddleocr_manifest_v1_cache_prepare_notes.md": str(out / "paddleocr_manifest_v1_cache_prepare_notes.md"),
        },
    }

    _write_json(out / "paddleocr_manifest_v1_cache_prepare_summary.json", summary)
    _write_json(out / "paddleocr_current_api_model_manifest_v1.candidate.json", candidate)
    _write_json(out / "paddleocr_manifest_v1_cache_acquisition_plan.json", acquisition)
    _write_json(out / "paddleocr_manifest_v1_expected_directory_matrix.json", matrix)

    (out / "paddleocr_manifest_v1_manual_copy_instructions.md").write_text(
        "\n".join(
            [
                "# PaddleOCR manifest v1 — manual cache acquisition",
                "",
                "## Target layout (flat)",
                "",
                f"- **model_root**: `{model_root}`",
                f"- **det**: `{model_root / det_r}`",
                f"- **rec**: `{model_root / rec_r}`",
                f"- **cls**: `{model_root / cls_r}`",
                "",
                "## Commands (shell)",
                "",
                "```bash",
                manual_steps[0],
                "```",
                "",
                "## Alternate naming (reference only)",
                "",
                f"- {args.layout_alias_note}",
                "",
                "## After files exist",
                "",
                "- Run `run_paddleocr_manifest_v1_snapshot_v0.py` with `--manifest` pointing to `paddleocr_current_api_model_manifest_v1.candidate.json` (copy to repo if desired) and `--cache-root` if needed.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    (out / "paddleocr_manifest_v1_cache_prepare_notes.md").write_text(
        "\n".join(
            [
                "# PaddleOCR Manifest v1 Cache Prepare v0",
                "",
                f"- **output_root**: `{out}`",
                "",
                "## 边界",
                "",
                "- **不**下载、**不** `PaddleOCR()`、**不** OCR、**不**改 routing。",
                "- **不**声明 `pinning_complete` / **不**写 fake sha256。",
                "",
                "- **URL 模板**（仓库内）：`" + url_template_repo_rel + "`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "prepare_verdict": summary["prepare_verdict"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

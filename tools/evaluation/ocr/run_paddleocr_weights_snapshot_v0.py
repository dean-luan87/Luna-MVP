#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Weights-001 — Local weight file snapshot + SHA256 pin (no download, no PaddleOCR(), no inference).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

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


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument("--readiness-manifest", default="configs/models/ocr/paddleocr_evaluation_readiness_manifest_v0.json")
    ap.add_argument("--model-files-manifest", default="configs/models/ocr/paddleocr_ppocrv5_model_files_manifest_v0.json")
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_weights_snapshot_001_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    rm_rel = args.readiness_manifest.strip()
    mf_rel = args.model_files_manifest.strip()
    rm_path = repo / rm_rel
    mf_path = repo / mf_rel
    if not rm_path.is_file():
        raise SystemExit(f"ERROR: missing readiness manifest: {rm_path}")
    if not mf_path.is_file():
        raise SystemExit(f"ERROR: missing model files manifest: {mf_path}")

    readiness = json.loads(rm_path.read_text(encoding="utf-8"))
    files_doc = json.loads(mf_path.read_text(encoding="utf-8"))
    expected = files_doc.get("expected_files") or []
    if not isinstance(expected, list):
        raise SystemExit("ERROR: expected_files must be a list")

    existence_rows: List[Dict[str, Any]] = []
    sha_rows: List[Dict[str, Any]] = []
    missing: List[Dict[str, Any]] = []
    weights_sha256: Dict[str, str] = {}
    weights_size: Dict[str, int] = {}

    for ent in expected:
        if not isinstance(ent, dict):
            continue
        rel = str(ent.get("relative_path") or "").strip()
        role = str(ent.get("role") or "")
        abs_path = (repo / rel).resolve() if rel else repo
        exists = abs_path.is_file()
        size_b: Optional[int] = abs_path.stat().st_size if exists else None
        sha_val: Optional[str] = _sha256_file(abs_path) if exists else None
        if exists and sha_val:
            weights_sha256[rel] = sha_val
            weights_size[rel] = int(size_b or 0)

        row_ex = {
            "role": role,
            "relative_path": rel,
            "absolute_path": str(abs_path),
            "exists": exists,
            "size_bytes": size_b,
        }
        existence_rows.append(row_ex)
        sha_rows.append({**row_ex, "sha256": sha_val})
        if not exists:
            missing.append({"role": role, "relative_path": rel, "absolute_path": str(abs_path), "reason": "file_not_found"})

    roles_found = {str(e.get("role") or "") for e in expected if isinstance(e, dict)}
    det_rec_cls_ok = {"det", "rec", "cls"}.issubset(roles_found)
    all_exist = len(missing) == 0
    all_sha = all(r.get("sha256") for r in sha_rows if r.get("exists"))

    pinned_files = []
    for ent in expected:
        if not isinstance(ent, dict):
            continue
        rel = str(ent.get("relative_path") or "").strip()
        apath = (repo / rel).resolve() if rel else None
        ex = apath.is_file() if apath else False
        pinned_files.append(
            {
                "role": ent.get("role"),
                "relative_path": rel,
                "sha256": weights_sha256.get(rel) if ex else None,
                "size_bytes": weights_size.get(rel) if ex else None,
            }
        )

    def _rel_to_repo(p: Path) -> str:
        try:
            return str(p.relative_to(repo))
        except ValueError:
            return str(p)

    pinned_candidate = {
        **readiness,
        "pin_phase": "Phase-PaddleOCR-Weights-001",
        "source_readiness_manifest_path": _rel_to_repo(rm_path),
        "source_model_files_manifest_path": _rel_to_repo(mf_path),
        "weights_snapshot_all_files_present": all_exist,
        "weights_sha256": weights_sha256,
        "weights_file_size_bytes": weights_size,
        "expected_files_pinned": pinned_files,
        "network_required": False,
        "runtime_default_enabled": False,
        "mainline_provider": False,
    }

    summary = {
        "phase": "Phase-PaddleOCR-Weights-001",
        "repo_root": str(repo),
        "output_root": str(out),
        "readiness_manifest": str(rm_path),
        "model_files_manifest": str(mf_path),
        "det_rec_cls_roles_present": det_rec_cls_ok,
        "all_planned_files_exist": all_exist,
        "all_sha256_computed_for_existing": all_sha,
        "missing_file_count": len(missing),
        "readiness_posture": "GO" if all_exist and all_sha else "CONDITIONAL_GO_weights_missing_or_incomplete",
        "verdict": "GO" if all_exist and all_sha else "CONDITIONAL_GO",
        "constraints": {
            "paddleocr_constructor_invoked": False,
            "paddleocr_inference_invoked": False,
            "network_download_invoked": False,
            "rapidocr_replaced": False,
            "ocr_routing_changed": False,
            "runtime_integration": False,
            "whitebox_integration": False,
            "mainline_side_effect": False,
            "midplatform_invoked": False,
        },
    }

    _write_json(out / "paddleocr_weights_snapshot_summary.json", summary)
    _write_json(out / "paddleocr_model_file_existence_matrix.json", {"rows": existence_rows})
    _write_json(out / "paddleocr_model_sha256_matrix.json", {"rows": sha_rows})
    _write_json(out / "paddleocr_model_missing_files_report.json", {"missing": missing, "complete": len(missing) == 0})
    _write_json(out / "paddleocr_pinned_model_manifest_candidate.json", pinned_candidate)

    notes = out / "paddleocr_weights_snapshot_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# PaddleOCR Weights Snapshot (Weights-001)",
                "",
                f"- **repo_root**: `{repo}`",
                f"- **output_root**: `{out}`",
                "",
                "- **No network download** in this tool; missing files are listed only.",
                "- **No PaddleOCR()** and **no OCR inference**.",
                "",
                f"- **all_planned_files_exist**: `{all_exist}`",
                f"- **verdict**: `{summary['verdict']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "verdict": summary["verdict"], "missing_count": len(missing)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

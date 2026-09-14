#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-ManifestV1-Snapshot-001 — v1 manifest model cache snapshot (no download, no PaddleOCR(), no OCR).

Scans resolved det/rec/cls refs under repo and optional cache-root; SHA256 for existing files only.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import sys
import uuid
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


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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


def _is_placeholder(s: Any) -> bool:
    t = str(s or "").strip()
    return not t or "<PLACEHOLDER" in t


REQUIRED_KEYS = (
    "provider_id",
    "provider_family",
    "model_format",
    "model_version",
    "language",
    "model_root",
    "det_model_ref",
    "rec_model_ref",
    "cls_model_ref",
    "offline_cache_required",
    "network_required",
    "download_authorized",
    "sha256_required",
    "runtime_default_enabled",
    "mainline_provider",
    "evaluation_candidate",
    "legacy_manifest_ref",
    "adapter_contract_ref",
)


def _validate_manifest_policy(m: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errs: List[str] = []
    for k in REQUIRED_KEYS:
        if k not in m:
            errs.append(f"missing_key:{k}")
    if m.get("runtime_default_enabled") is not False:
        errs.append("policy_runtime_default_enabled_must_be_false")
    if m.get("mainline_provider") is not False:
        errs.append("policy_mainline_provider_must_be_false")
    if m.get("network_required") is not False:
        errs.append("policy_network_required_must_be_false")
    if m.get("download_authorized") is not False:
        errs.append("policy_download_authorized_must_be_false")
    if m.get("evaluation_candidate") is not True:
        errs.append("policy_evaluation_candidate_must_be_true")
    return len(errs) == 0, errs


def _build_candidates(repo: Path, model_root: str, ref: str, cache_root: Optional[Path]) -> List[Path]:
    out: List[Path] = []
    r = str(ref or "").strip()
    if not r or _is_placeholder(r):
        return out
    p = Path(r)
    if p.is_absolute():
        out.append(p.resolve())
        return out
    mr_s = str(model_root or "").strip()
    if not _is_placeholder(mr_s):
        mrp = Path(mr_s)
        if mrp.is_absolute():
            out.append((mrp / r).resolve())
        else:
            out.append((repo / mr_s / r).resolve())
    out.append((repo / r).resolve())
    if cache_root is not None:
        cr = cache_root.resolve()
        out.append((cr / r).resolve())
        if not _is_placeholder(mr_s):
            leaf = Path(mr_s).name
            if leaf and not _is_placeholder(leaf):
                out.append((cr / leaf / r).resolve())
    seen = set()
    uniq: List[Path] = []
    for x in out:
        sx = str(x)
        if sx not in seen:
            seen.add(sx)
            uniq.append(x)
    return uniq


def _resolve_role_path(
    repo: Path,
    model_root: str,
    ref: str,
    cache_root: Optional[Path],
) -> Tuple[List[str], Optional[Path]]:
    cands = _build_candidates(repo, model_root, ref, cache_root)
    labels = [str(p) for p in cands]
    for p in cands:
        if p.exists():
            return labels, p
    return labels, None


def _collect_dir_hashes(root: Path, max_files: int) -> Tuple[Dict[str, str], int, bool, str]:
    """Returns (sha256_by_rel_path, file_count, cap_hit, note)."""
    files: List[Path] = []
    for p in sorted(root.rglob("*")):
        if p.is_file():
            files.append(p)
    cap_hit = len(files) > max_files
    to_hash = files[:max_files]
    sha_map: Dict[str, str] = {}
    for fp in to_hash:
        rel = str(fp.relative_to(root))
        sha_map[rel] = _sha256_file(fp)
    note = ""
    if cap_hit:
        note = f"sha256_truncated_cap_{max_files}"
    return sha_map, len(files), cap_hit, note


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument(
        "--manifest",
        default="configs/models/ocr/paddleocr_current_api_model_manifest_v1.example.json",
        help="Repo-relative or absolute path to v1 manifest JSON.",
    )
    ap.add_argument("--cache-root", default="", help="Optional absolute cache root to probe in addition to repo.")
    ap.add_argument("--output-root", default="")
    ap.add_argument("--max-files-per-ref-dir", type=int, default=512)
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    man_rel = args.manifest.strip()
    man_path = repo / man_rel if not Path(man_rel).is_absolute() else Path(man_rel).resolve()
    if not man_path.is_file():
        raise SystemExit(f"ERROR: manifest not found: {man_path}")

    cache_root: Optional[Path] = None
    if args.cache_root.strip():
        cache_root = _require_abs(args.cache_root, "--cache-root")

    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_manifest_v1_snapshot_001_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    manifest = json.loads(man_path.read_text(encoding="utf-8"))
    policy_ok, policy_errs = _validate_manifest_policy(manifest)

    field_rows: List[Dict[str, Any]] = []
    for k in REQUIRED_KEYS:
        field_rows.append({"field": k, "present": k in manifest, "value_type": type(manifest.get(k)).__name__})

    if not policy_ok:
        summary = {
            "phase": "Phase-PaddleOCR-ManifestV1-Snapshot-001",
            "verdict": "NO_GO",
            "policy_validation_errors": policy_errs,
            "manifest_path": str(man_path),
            "output_root": str(out),
            "constraints": _constraints(),
        }
        _write_json(out / "paddleocr_manifest_v1_snapshot_summary.json", summary)
        _write_json(out / "paddleocr_manifest_v1_field_matrix.json", {"rows": field_rows, "policy_ok": False})
        _write_json(out / "paddleocr_manifest_v1_model_cache_matrix.json", {"rows": []})
        _write_json(out / "paddleocr_manifest_v1_sha256_matrix.json", {"files": []})
        _write_json(out / "paddleocr_manifest_v1_missing_cache_report.json", {"missing": [], "reason": "manifest_policy_failed"})
        _write_json(
            out / "paddleocr_manifest_v1_pinned_manifest_candidate.json",
            {
                "pinning_complete": False,
                "verdict": "NO_GO",
                "missing_refs": [],
                "runtime_default_enabled": False,
                "mainline_provider": False,
                "network_required": False,
                "download_authorized": False,
                "policy_validation_errors": policy_errs,
            },
        )
        (out / "paddleocr_manifest_v1_snapshot_notes.md").write_text(
            "# Manifest v1 snapshot\n\n**NO_GO**: manifest policy validation failed.\n", encoding="utf-8"
        )
        print(json.dumps({"output_root": str(out), "verdict": "NO_GO"}, ensure_ascii=False))
        return 2

    model_root = str(manifest.get("model_root") or "")
    roles = ("det", "rec", "cls")
    ref_keys = {"det": "det_model_ref", "rec": "rec_model_ref", "cls": "cls_model_ref"}

    cache_rows: List[Dict[str, Any]] = []
    sha_files: List[Dict[str, Any]] = []
    missing: List[Dict[str, Any]] = []
    resolved_refs: Dict[str, Any] = {}
    sha256_by_file: Dict[str, str] = {}

    for role in roles:
        rk = ref_keys[role]
        ref = str(manifest.get(rk) or "")
        labels, chosen = _resolve_role_path(repo, model_root, ref, cache_root)
        resolved_refs[role] = {
            "ref_key": rk,
            "ref_value": ref,
            "resolved_candidates": labels,
            "resolved_path": str(chosen) if chosen else None,
            "exists": chosen is not None and chosen.exists(),
        }
        row: Dict[str, Any] = {
            "role": role,
            "ref_key": rk,
            "ref_value": ref,
            "placeholder_ref": _is_placeholder(ref),
            "resolved_candidates": labels,
            "resolved_path": str(chosen) if chosen else None,
            "exists": bool(chosen and chosen.exists()),
            "is_file": chosen.is_file() if chosen and chosen.exists() else False,
            "is_dir": chosen.is_dir() if chosen and chosen.exists() else False,
            "file_count": 0,
            "sha256_note": "",
        }
        if _is_placeholder(ref):
            missing.append({"role": role, "ref_key": rk, "reason": "placeholder_ref", "candidates": labels})
        elif chosen is None or not chosen.exists():
            missing.append({"role": role, "ref_key": rk, "reason": "path_not_found", "candidates": labels})
        elif chosen.is_file():
            sha = _sha256_file(chosen)
            sha256_by_file[str(chosen)] = sha
            sha_files.append({"role": role, "path": str(chosen), "sha256": sha, "kind": "file"})
            row["file_count"] = 1
        elif chosen.is_dir():
            sub, n_files, cap_hit, note = _collect_dir_hashes(chosen, max_files=max(1, args.max_files_per_ref_dir))
            row["file_count"] = n_files
            row["sha256_note"] = note
            for rel, h in sorted(sub.items()):
                key = f"{chosen}:{rel}"
                sha256_by_file[key] = h
                sha_files.append({"role": role, "path": str(chosen / rel), "sha256": h, "kind": "dir_member", "relative": rel})
            if n_files == 0:
                missing.append({"role": role, "ref_key": rk, "reason": "empty_directory", "path": str(chosen)})
            if cap_hit:
                missing.append({"role": role, "ref_key": rk, "reason": "sha256_cap_incomplete", "path": str(chosen)})
        cache_rows.append(row)

    mr_labels, mr_chosen = _resolve_role_path(repo, "", model_root, cache_root)
    model_root_row = {
        "field": "model_root",
        "value": model_root,
        "placeholder": _is_placeholder(model_root),
        "resolved_candidates": mr_labels,
        "resolved_path": str(mr_chosen) if mr_chosen else None,
        "exists": mr_chosen is not None and mr_chosen.exists(),
        "is_dir": mr_chosen.is_dir() if mr_chosen and mr_chosen.exists() else False,
    }

    missing_refs = [m for m in missing if m.get("reason") in ("placeholder_ref", "path_not_found", "empty_directory")]
    cap_incomplete = any(m.get("reason") == "sha256_cap_incomplete" for m in missing)
    three_ok = (
        len(cache_rows) == 3
        and all(not r.get("placeholder_ref") for r in cache_rows)
        and all(r.get("exists") and r.get("file_count", 0) > 0 for r in cache_rows)
    )
    pinning_complete = bool(three_ok and not missing_refs and not cap_incomplete)

    verdict = "GO" if pinning_complete else "CONDITIONAL_GO"

    summary = {
        "phase": "Phase-PaddleOCR-ManifestV1-Snapshot-001",
        "verdict": verdict,
        "manifest_path": str(man_path),
        "manifest_repo_relative": man_rel if not Path(man_rel).is_absolute() else None,
        "cache_root": str(cache_root) if cache_root else None,
        "output_root": str(out),
        "snapshot_id": str(uuid.uuid4()),
        "snapshot_time": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "model_root_probe": model_root_row,
        "missing_ref_count": len(missing_refs),
        "pinning_complete": pinning_complete,
        "constraints": _constraints(),
    }
    pinned = {
        **manifest,
        "snapshot_id": summary["snapshot_id"],
        "snapshot_time": summary["snapshot_time"],
        "snapshot_phase": "Phase-PaddleOCR-ManifestV1-Snapshot-001",
        "resolved_model_refs": resolved_refs,
        "model_cache_exists": three_ok,
        "sha256_by_file": sha256_by_file,
        "missing_refs": missing_refs,
        "missing_cache_events": missing,
        "pinning_complete": pinning_complete,
        "snapshot_verdict": verdict,
        "runtime_default_enabled": manifest.get("runtime_default_enabled"),
        "mainline_provider": manifest.get("mainline_provider"),
    }

    _write_json(out / "paddleocr_manifest_v1_snapshot_summary.json", summary)
    _write_json(
        out / "paddleocr_manifest_v1_field_matrix.json",
        {"schema": "paddleocr_manifest_v1_field_matrix_snapshot_v0", "phase": summary["phase"], "rows": field_rows, "policy_ok": True},
    )
    _write_json(
        out / "paddleocr_manifest_v1_model_cache_matrix.json",
        {"schema": "paddleocr_manifest_v1_model_cache_matrix_v0", "phase": summary["phase"], "rows": cache_rows},
    )
    _write_json(
        out / "paddleocr_manifest_v1_sha256_matrix.json",
        {"schema": "paddleocr_manifest_v1_sha256_matrix_v0", "phase": summary["phase"], "files": sha_files},
    )
    _write_json(
        out / "paddleocr_manifest_v1_missing_cache_report.json",
        {"schema": "paddleocr_manifest_v1_missing_cache_report_v0", "phase": summary["phase"], "missing": missing},
    )
    _write_json(out / "paddleocr_manifest_v1_pinned_manifest_candidate.json", pinned)

    notes = out / "paddleocr_manifest_v1_snapshot_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# PaddleOCR Manifest v1 Model Cache Snapshot v0",
                "",
                f"- **output_root**: `{out}`",
                f"- **manifest**: `{man_path}`",
                f"- **cache_root**: `{cache_root or '(none)'}`",
                "",
                "## 边界",
                "",
                "- **不**下载、**不** `PaddleOCR()`、**不** OCR、**不**改 routing。",
                "",
                f"- **verdict**: `{verdict}`",
                f"- **pinning_complete**: `{pinning_complete}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_root": str(out), "verdict": verdict, "pinning_complete": pinning_complete}, ensure_ascii=False))
    return 0 if verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelOCR-003-Fix
PaddleOCR pinned-local weights preparation v0.

Hard boundaries:
- Does not run OCR inference (no images, no benchmark)
- Default: no auto-download; only copies from an explicit source root
- Never fabricates weights/hashes
- Does not connect to runtime / downstream chains

This tool:
- Locates det/rec/cls model directories under a provided --source-root (or explicit overrides)
- Copies them into the repo standard paths under --target-root (models/ocr/paddleocr_ppocrv5/{det,rec,cls})
- Generates file-level sha256/size manifest: models/ocr/paddleocr_ppocrv5/model_files_manifest_v0.json
- Updates OCR manifest (configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json) to pinned_local or pinned_partial

Directory weights hashing policy:
- Record sha256+size per file (file-level manifest)
- Record an aggregate digest of the manifest lines in OCR manifest under directory_hash_summary
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import shutil
import sys
import tarfile
import zipfile
from typing import Any, Dict, List, Optional, Tuple


REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    if not isinstance(obj, dict):
        raise ValueError("json_root_not_dict")
    return obj


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _sha256_file(path: str) -> Tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            size += len(chunk)
            h.update(chunk)
    return h.hexdigest(), size


def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _resolve_repo_rel(path: str) -> str:
    ap = os.path.abspath(path)
    if ap.startswith(REPO_ROOT):
        return os.path.relpath(ap, REPO_ROOT)
    return ap


def _is_in_dir(child: str, parent: str) -> bool:
    c = os.path.abspath(child)
    p = os.path.abspath(parent)
    return c == p or c.startswith(p + os.sep)


def _folder_has_paddle_infer_assets(files) -> bool:
    names = set(files)
    if "inference.pdiparams" not in names:
        return False
    if "inference.pdmodel" in names:
        return True
    if "inference.json" in names:
        return True
    return False


def _has_paddle_infer_files(d: str) -> bool:
    """
    True if a directory (or any subdirectory) contains a valid Paddle inference pair
    in the same folder: (inference.pdmodel|inference.json) + inference.pdiparams.
    """
    if not os.path.isdir(d):
        return False
    for root, _dirs, files in os.walk(d):
        if _folder_has_paddle_infer_assets(files):
            return True
    return False


def _first_infer_subdir(d: str) -> Optional[str]:
    """Return the first directory path that directly contains the inference pair."""
    if not os.path.isdir(d):
        return None
    for root, _dirs, files in os.walk(d):
        if _folder_has_paddle_infer_assets(files):
            return root
    return None


def _walk_find_infer_dirs(source_root: str) -> List[str]:
    out: List[str] = []
    for root, dirs, files in os.walk(source_root):
        # prune very deep vendor dirs by simple heuristics
        bn = os.path.basename(root).lower()
        if bn in (".git", "__pycache__", "node_modules"):
            dirs[:] = []
            continue
        if _folder_has_paddle_infer_assets(files):
            out.append(root)
    return out


def _classify_role_from_path(p: str) -> Optional[str]:
    lp = p.lower().replace("\\", "/")
    parts = [x for x in lp.split("/") if x]
    for role in ("det", "rec", "cls"):
        if role in parts:
            return role
    # fallback heuristic: substring match
    if "det" in lp:
        return "det"
    if "rec" in lp:
        return "rec"
    if "cls" in lp or "angle" in lp:
        return "cls"
    return None


def _select_single(cands: List[str], role: str) -> str:
    if not cands:
        raise SystemExit(f"source_missing_role:{role}")
    if len(cands) != 1:
        raise SystemExit(f"source_ambiguous_role:{role} candidates={len(cands)}")
    return cands[0]


def _copy_tree(src_dir: str, dst_dir: str, *, clean_target: bool) -> None:
    if not os.path.isdir(src_dir):
        raise SystemExit("source_not_a_dir")
    os.makedirs(dst_dir, exist_ok=True)
    if clean_target:
        for name in os.listdir(dst_dir):
            p = os.path.join(dst_dir, name)
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)
    # copy2 preserves mtime; we still hash afterwards.
    for root, dirs, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        out_root = dst_dir if rel == "." else os.path.join(dst_dir, rel)
        os.makedirs(out_root, exist_ok=True)
        for fn in files:
            sp = os.path.join(root, fn)
            dp = os.path.join(out_root, fn)
            shutil.copy2(sp, dp)


def _build_file_manifest(
    *,
    target_root: str,
    det_dir: str,
    rec_dir: str,
    cls_dir: Optional[str],
    source_notes: str,
    role_provenance: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    files: List[Dict[str, Any]] = []
    total = 0
    rpmap = role_provenance or {}

    def _add_dir(role: str, d: str) -> None:
        nonlocal total
        prov = (rpmap.get(role) or source_notes or "").strip() or None
        for root, dirs, fns in os.walk(d):
            dirs.sort()
            fns.sort()
            for fn in fns:
                ap = os.path.join(root, fn)
                if not os.path.isfile(ap):
                    continue
                sha, sz = _sha256_file(ap)
                total += int(sz)
                rp = os.path.relpath(ap, REPO_ROOT)
                if not _is_in_dir(ap, REPO_ROOT):
                    raise SystemExit("target_file_escape_repo_root")
                files.append(
                    {
                        "relative_path": rp,
                        "sha256": sha,
                        "file_size_bytes": int(sz),
                        "role": role,
                        "source_url_or_cache": prov,
                        "created_at": _now_iso(),
                    }
                )

    _add_dir("det", det_dir)
    _add_dir("rec", rec_dir)
    if cls_dir and os.path.isdir(cls_dir):
        _add_dir("cls", cls_dir)

    files.sort(key=lambda r: (str(r.get("role") or ""), str(r.get("relative_path") or "")))
    norm_lines = [f"{r.get('sha256')}\t{r.get('file_size_bytes')}\t{r.get('role')}\t{r.get('relative_path')}" for r in files]
    agg = _sha256_text("\n".join(norm_lines) + "\n")

    return {
        "manifest_version": "v0",
        "target_root": os.path.relpath(os.path.abspath(target_root), REPO_ROOT) if _is_in_dir(target_root, REPO_ROOT) else os.path.abspath(target_root),
        "generated_at": _now_iso(),
        "provenance": {
            "global_notes": source_notes or None,
            "per_role": {k: v for k, v in (role_provenance or {}).items() if v},
        },
        "hash_summary": {"algorithm": "sha256_of_manifest_lines_v0", "sha256": agg, "file_count": len(files), "total_file_size_bytes": int(total)},
        "files": files,
    }


def _extract_if_archive(path: str, dest_dir: str) -> str:
    """
    If path is a .zip / .tar / .tar.gz, extract to dest_dir and return dest_dir.
    Otherwise return the parent directory of path (for single-file drops).
    """
    os.makedirs(dest_dir, exist_ok=True)
    lower = path.lower()
    if lower.endswith(".zip"):
        with zipfile.ZipFile(path, "r") as z:
            z.extractall(dest_dir)
        return dest_dir
    if lower.endswith(".tar.gz") or lower.endswith(".tgz") or lower.endswith(".tar"):
        with tarfile.open(path, "r:*") as t:
            t.extractall(dest_dir)
        return dest_dir
    return os.path.dirname(os.path.abspath(path))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--source-root",
        default=None,
        help="Root to search for inference dirs, or anchor for relative det/rec/cls paths (default: repo root if all sources absolute)",
    )
    ap.add_argument("--target-root", default="models/ocr/paddleocr_ppocrv5", help="Repo target root for pinned weights")
    ap.add_argument("--manifest", default="configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json", help="OCR manifest to update")
    ap.add_argument("--model-files-manifest", default="models/ocr/paddleocr_ppocrv5/model_files_manifest_v0.json", help="File-level weights manifest output path")
    ap.add_argument("--det-source-dir", default=None, help="Explicit det dir (absolute or relative to --source-root)")
    ap.add_argument("--rec-source-dir", default=None, help="Explicit rec dir (absolute or relative to --source-root)")
    ap.add_argument("--cls-source-dir", default=None, help="Explicit cls dir (absolute or relative to --source-root). If omitted, auto-detect; may be optional.")
    ap.add_argument("--cls-optional", action="store_true", help="Allow missing cls assets (pinned_partial)")
    ap.add_argument("--clean-target", action="store_true", help="Clean target det/rec/cls dirs before copying")
    ap.add_argument("--source-notes", default="", help="Provenance notes (URL/cache path/version); recorded into manifests")
    ap.add_argument("--det-source-url", default="", help="Optional: URL provenance for det files (recorded in manifest per-role)")
    ap.add_argument("--rec-source-url", default="", help="Optional: URL provenance for rec files")
    ap.add_argument("--cls-source-url", default="", help="Optional: URL provenance for cls files")
    ap.add_argument(
        "--allow-download",
        default="false",
        choices=["true", "false"],
        help="Reserved: pinned preparation never downloads; use acquire tool first",
    )
    args = ap.parse_args()

    if str(args.allow_download).lower() == "true":
        raise SystemExit("prepare_tool_does_not_download_use_acquire_then_prepare")

    src_root_arg = args.source_root
    if src_root_arg:
        src_root = os.path.abspath(os.path.expanduser(str(src_root_arg)))
        if not os.path.isdir(src_root):
            raise SystemExit("source_root_not_found_or_not_dir")
    else:
        src_root = REPO_ROOT

    role_prov = {}
    if str(args.det_source_url or "").strip():
        role_prov["det"] = str(args.det_source_url).strip()
    if str(args.rec_source_url or "").strip():
        role_prov["rec"] = str(args.rec_source_url).strip()
    if str(args.cls_source_url or "").strip():
        role_prov["cls"] = str(args.cls_source_url).strip()

    target_root_abs = os.path.abspath(os.path.join(REPO_ROOT, str(args.target_root))) if not os.path.isabs(str(args.target_root)) else os.path.abspath(str(args.target_root))
    if not _is_in_dir(target_root_abs, REPO_ROOT):
        raise SystemExit("target_root_must_be_inside_repo")

    det_target = os.path.join(target_root_abs, "det")
    rec_target = os.path.join(target_root_abs, "rec")
    cls_target = os.path.join(target_root_abs, "cls")

    # Resolve explicit sources or auto-detect
    def _resolve_src_dir(p: Optional[str]) -> Optional[str]:
        if not p:
            return None
        pp = os.path.expanduser(str(p))
        if os.path.isabs(pp):
            return os.path.abspath(pp)
        return os.path.abspath(os.path.join(src_root, pp))

    det_src = _resolve_src_dir(args.det_source_dir)
    rec_src = _resolve_src_dir(args.rec_source_dir)
    cls_src = _resolve_src_dir(args.cls_source_dir)

    infer_dirs = _walk_find_infer_dirs(src_root) if (not det_src or not rec_src or (not cls_src and not args.cls_optional)) else []

    if not det_src:
        det_cands = [d for d in infer_dirs if _classify_role_from_path(d) == "det"]
        det_src = _select_single(det_cands, "det")
    if not rec_src:
        rec_cands = [d for d in infer_dirs if _classify_role_from_path(d) == "rec"]
        rec_src = _select_single(rec_cands, "rec")
    if not cls_src and not args.cls_optional:
        cls_cands = [d for d in infer_dirs if _classify_role_from_path(d) == "cls"]
        cls_src = _select_single(cls_cands, "cls")

    # Validate infer files in selected dirs (best-effort; do not guess)
    if not det_src:
        raise SystemExit("det_source_missing")
    det_infer = _first_infer_subdir(det_src)
    if not det_infer:
        raise SystemExit("det_source_dir_invalid_or_missing_inference_files")
    if not rec_src:
        raise SystemExit("rec_source_missing")
    rec_infer = _first_infer_subdir(rec_src)
    if not rec_infer:
        raise SystemExit("rec_source_dir_invalid_or_missing_inference_files")

    cls_infer: Optional[str] = None
    if cls_src:
        cls_infer = _first_infer_subdir(cls_src)
        if not cls_infer:
            if args.cls_optional:
                cls_src = None
                cls_infer = None
            else:
                raise SystemExit("cls_source_dir_invalid_or_missing_inference_files")

    # Copy into repo standard paths
    _copy_tree(det_infer, det_target, clean_target=bool(args.clean_target))
    _copy_tree(rec_infer, rec_target, clean_target=bool(args.clean_target))
    if cls_infer:
        _copy_tree(cls_infer, cls_target, clean_target=bool(args.clean_target))
    else:
        os.makedirs(cls_target, exist_ok=True)

    # Generate file-level manifest (repo-relative paths)
    mf_obj = _build_file_manifest(
        target_root=target_root_abs,
        det_dir=det_target,
        rec_dir=rec_target,
        cls_dir=cls_target if cls_infer else None,
        source_notes=str(args.source_notes or "").strip(),
        role_provenance=role_prov if role_prov else None,
    )
    mf_path_abs = os.path.abspath(os.path.join(REPO_ROOT, str(args.model_files_manifest))) if not os.path.isabs(str(args.model_files_manifest)) else os.path.abspath(str(args.model_files_manifest))
    if not _is_in_dir(mf_path_abs, REPO_ROOT):
        raise SystemExit("model_files_manifest_must_be_inside_repo")
    _write_json(mf_path_abs, mf_obj)

    # Update OCR manifest
    manifest_path_abs = os.path.abspath(os.path.join(REPO_ROOT, str(args.manifest))) if not os.path.isabs(str(args.manifest)) else os.path.abspath(str(args.manifest))
    man = _read_json(manifest_path_abs)

    man["weights_paths"] = man.get("weights_paths") if isinstance(man.get("weights_paths"), dict) else {}
    man["weights_paths"]["det_model_path"] = _resolve_repo_rel(det_target)
    man["weights_paths"]["rec_model_path"] = _resolve_repo_rel(rec_target)
    man["weights_paths"]["cls_model_path"] = _resolve_repo_rel(cls_target)
    if "tokenizer_path" not in man["weights_paths"]:
        man["weights_paths"]["tokenizer_path"] = None

    man["model_files_manifest_path"] = _resolve_repo_rel(mf_path_abs)
    man["directory_hash_summary"] = mf_obj.get("hash_summary")

    man["weights_policy"] = man.get("weights_policy") if isinstance(man.get("weights_policy"), dict) else {}
    man["weights_policy"]["cls_optional"] = bool(args.cls_optional)

    # Do not fake single-file hashes for directories; keep dicts but do not fabricate.
    if not isinstance(man.get("weights_sha256"), dict):
        man["weights_sha256"] = {}
    if not isinstance(man.get("weights_file_size_bytes"), dict):
        man["weights_file_size_bytes"] = {}

    man["weights_source"] = "pinned_local" if (not args.cls_optional or cls_infer) else "pinned_partial"
    if bool(args.cls_optional) and not cls_infer:
        man["weights_source"] = "pinned_partial"

    man["verification_status"] = "partial"
    man["verified_at"] = None
    man["notes"] = (man.get("notes") or "").strip()
    if str(args.source_notes or "").strip():
        extra = f"paddleocr_weights_source:{str(args.source_notes).strip()}"
        man["notes"] = (man["notes"] + " | " + extra).strip(" |")

    _write_json(manifest_path_abs, man)

    out = {
        "phase": "Phase-ModelOCR-003-Fix",
        "tool": "prepare_paddleocr_pinned_weights_v0.py",
        "source_root": src_root,
        "det_source_dir": det_infer,
        "rec_source_dir": rec_infer,
        "cls_source_dir": cls_infer,
        "target_root": _resolve_repo_rel(target_root_abs),
        "model_files_manifest_path": _resolve_repo_rel(mf_path_abs),
        "directory_hash_summary": mf_obj.get("hash_summary"),
        "manifest_updated": _resolve_repo_rel(manifest_path_abs),
        "weights_source_set_to": man.get("weights_source"),
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelOCR-003-Fix-003
PaddleOCR Alternative Weight Source Acquisition v0.

Hard boundaries:
- Default: does NOT download
- Only --allow-download true performs network fetches
- Never runs OCR inference (no ocr.ocr / no recognition on images)
- Does not mark runtime ready; pinned state is produced by prepare + readiness only
- Must pin to Luna-Models/ocr/paddleocr_ppocrv5/ via prepare (or equivalent), not "use at runtime download"

Source types:
- local_dir: use existing directory (or explicit --det-path/--rec-path/--cls-path)
- manual_url: download --det-url / --rec-url / optional --cls-url
- gitee: same as manual_url (full URL to artifact; no magic host)
- huggingface: --hf-det-repo / --hf-rec-repo / optional --hf-cls-repo (requires huggingface_hub) OR full resolve URLs in --det-url
- official: scan default caches + optional init-only (PaddleOCR) when --allow-download true
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import platform
from collections import defaultdict
import subprocess
import sys
import tarfile
import zipfile
from typing import Any, Dict, List, Optional, Set, Tuple
from urllib.request import Request, urlopen


REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _sha256_file(path: str) -> Tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with open(path, "rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            size += len(b)
            h.update(b)
    return h.hexdigest(), size


def _import_version(dist_name: str) -> Optional[str]:
    try:
        from importlib import metadata as _md

        return _md.version(dist_name)
    except Exception:
        return None


def _check_import(mod: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {"module": mod, "import_ok": False, "version": None, "error": None, "file": None}
    try:
        m = __import__(mod)
        out["import_ok"] = True
        out["file"] = getattr(m, "__file__", None)
    except Exception as e:
        out["error"] = repr(e)
        return out

    if mod == "paddleocr":
        out["version"] = _import_version("paddleocr") or getattr(m, "__version__", None)
    elif mod == "paddle":
        out["version"] = getattr(m, "__version__", None) or _import_version("paddlepaddle")
    elif mod == "cv2":
        out["version"] = getattr(m, "__version__", None) or _import_version("opencv-python")
    elif mod == "PIL":
        out["version"] = _import_version("Pillow")
    return out


def _folder_has_paddle_infer_assets(files: List[str]) -> bool:
    """
    Legacy Paddle inference dir: inference.pdmodel + inference.pdiparams.
    PP-OCRv5 HF exports often ship inference.json (program) + inference.pdiparams instead.
    """
    names = set(files)
    if "inference.pdiparams" not in names:
        return False
    if "inference.pdmodel" in names:
        return True
    if "inference.json" in names:
        return True
    return False


def _first_infer_subdir(root: str) -> Optional[str]:
    for dirpath, _dirs, files in os.walk(root):
        if _folder_has_paddle_infer_assets(files):
            return dirpath
    return None


def _walk_find_infer_dirs(source_root: str) -> List[str]:
    out: List[str] = []
    for root, dirs, files in os.walk(source_root):
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
    if "det" in lp:
        return "det"
    if "rec" in lp:
        return "rec"
    if "cls" in lp or "angle" in lp:
        return "cls"
    return None


def _pick_single_role(cands: List[str], role: str) -> Tuple[Optional[str], str]:
    cands = [c for c in cands if c]
    if not cands:
        return None, f"missing:{role}"
    if len(cands) == 1:
        return cands[0], "ok"

    def _score(x: str) -> Tuple[int, int]:
        lp = x.lower().replace("\\", "/")
        tail = lp.split("/")[-1]
        tail_bonus = 0 if tail in (role, f"{role}_model", f"{role}model") else 1
        return (tail_bonus, len(lp))

    cands_sorted = sorted(cands, key=_score)
    return cands_sorted[0], f"ambiguous:{role} candidates={len(cands)}"


def _default_cache_roots() -> List[str]:
    h = os.path.expanduser("~")
    roots = [
        os.path.join(h, ".paddleocr"),
        os.path.join(h, ".cache", "paddleocr"),
        os.path.join(h, ".cache", "paddle", "ocr"),
        os.path.join(h, ".cache", "paddle"),
        os.path.join(h, ".paddle"),
        os.path.join(h, ".cache"),
    ]
    out: List[str] = []
    for r in roots:
        r = os.path.abspath(r)
        if r not in out:
            out.append(r)
    return out


def _scan_caches(roots: List[str]) -> Dict[str, Any]:
    found_dirs: List[str] = []
    scanned: List[Dict[str, Any]] = []
    for r in roots:
        if not os.path.exists(r) or not os.path.isdir(r):
            scanned.append({"root": r, "exists": False, "infer_dirs": 0})
            continue
        dirs = _walk_find_infer_dirs(r)
        scanned.append({"root": r, "exists": True, "infer_dirs": len(dirs)})
        found_dirs.extend(dirs)
    uniq: List[str] = []
    seen = set()
    for d in found_dirs:
        ad = os.path.abspath(d)
        if ad not in seen:
            seen.add(ad)
            uniq.append(ad)
    return {"scanned_roots": scanned, "infer_dirs": uniq, "infer_dir_count": len(uniq)}


def _download_url(url: str, dest_path: str) -> Dict[str, Any]:
    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
    req = Request(url, headers={"User-Agent": "Luna-PaddleOCR-Acquire/0"})
    with urlopen(req, timeout=600) as resp:
        data = resp.read()
    with open(dest_path, "wb") as f:
        f.write(data)
    sha, sz = _sha256_file(dest_path)
    return {"source_url": url, "path": dest_path, "sha256": sha, "file_size_bytes": int(sz)}


def _extract_if_archive(path: str, dest_dir: str) -> str:
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


def _attempt_init_only(model_profile: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {"attempted": False, "ok": False, "error": None, "profile": model_profile, "paddleocr_init": {}}
    try:
        from paddleocr import PaddleOCR  # type: ignore

        out["attempted"] = True
        lang = "ch" if "zh" in model_profile or "ch" in model_profile else "en"
        use_angle_cls = True
        ocr = PaddleOCR(lang=lang, use_angle_cls=use_angle_cls)
        out["paddleocr_init"] = {
            "lang": lang,
            "use_angle_cls": use_angle_cls,
            "det_model_dir": getattr(ocr, "det_model_dir", None),
            "rec_model_dir": getattr(ocr, "rec_model_dir", None),
            "cls_model_dir": getattr(ocr, "cls_model_dir", None),
        }
        out["ok"] = True
        return out
    except Exception as e:
        out["error"] = repr(e)
        return out


def _hf_download_inference_repo(repo_id: str, out_dir: str, downloads: List[Dict[str, Any]]) -> str:
    """
    PP-OCR / Paddle HF repos may place weights under a subdirectory. List remote files and
    pick the first folder that contains a valid Paddle inference pair:
    - legacy: inference.pdmodel + inference.pdiparams, or
    - PP-OCRv5-style (common on HF): inference.json + inference.pdiparams.
    Then download core files plus optional inference.yml / config.json when present.
    """
    try:
        from huggingface_hub import HfApi, hf_hub_download, list_repo_files  # type: ignore
    except Exception as e:
        raise RuntimeError(f"huggingface_hub_required:{repr(e)}") from e

    os.makedirs(out_dir, exist_ok=True)
    try:
        remote_files = list(list_repo_files(repo_id=repo_id))  # type: ignore[misc]
    except TypeError:
        remote_files = list(list_repo_files(repo_id))  # type: ignore[misc]
    except Exception:
        remote_files = list(HfApi().list_repo_files(repo_id=repo_id))

    remote_set: Set[str] = {str(f).replace("\\", "/").strip() for f in remote_files}
    by_dir: Dict[str, Set[str]] = defaultdict(set)
    for f in remote_files:
        fn_norm = str(f).replace("\\", "/").strip()
        if not fn_norm or fn_norm.endswith("/"):
            continue
        d_part, base = os.path.split(fn_norm)
        d_key = d_part.strip("/")
        by_dir[d_key].add(base)

    # d_key == "" means repo root; must not use `if not pick_prefix` (that rejects root).
    pick_prefix = ""
    pick_kind: Optional[str] = None  # "pdmodel" | "json"
    for d_key in sorted(by_dir.keys()):
        names = by_dir[d_key]
        if "inference.pdiparams" not in names:
            continue
        if "inference.pdmodel" in names:
            pick_prefix, pick_kind = d_key, "pdmodel"
            break
        if "inference.json" in names:
            pick_prefix, pick_kind = d_key, "json"
            break

    if pick_kind is None:
        raise RuntimeError(f"hf_repo_no_paddle_infer_pair:{repo_id}")

    def _rel(name: str) -> str:
        if pick_prefix == "":
            return name
        return f"{pick_prefix}/{name}"

    if pick_kind == "pdmodel":
        core_files = [_rel("inference.pdmodel"), _rel("inference.pdiparams")]
    else:
        core_files = [_rel("inference.json"), _rel("inference.pdiparams")]

    for cf in core_files:
        if cf not in remote_set:
            raise RuntimeError(f"hf_repo_infer_pair_inconsistent:{repo_id} missing={cf}")

    optional_names = ("inference.yml", "inference.pdiparams.info", "config.json")
    optional = [_rel(n) for n in optional_names if n in by_dir[pick_prefix] and _rel(n) in remote_set]
    to_fetch = core_files + optional
    core_set = set(core_files)

    for fn in to_fetch:
        try:
            p = hf_hub_download(repo_id=repo_id, filename=fn, local_dir=out_dir)
            sha, sz = _sha256_file(p)
            enc_fn = fn.replace("\\", "/")
            downloads.append(
                {
                    "source_type": "huggingface",
                    "repo_id": repo_id,
                    "filename": fn,
                    "resolved_path": p,
                    "source_url": f"https://huggingface.co/{repo_id}/resolve/main/{enc_fn}",
                    "sha256": sha,
                    "file_size_bytes": int(sz),
                }
            )
        except Exception as e:
            if fn in core_set:
                raise RuntimeError(f"hf_hub_download_failed:{repo_id}:{fn}:{e!r}") from e

    infer_root = _first_infer_subdir(out_dir)
    if not infer_root:
        raise RuntimeError(f"hf_repo_missing_inference_pair_after_download:{repo_id}")
    return infer_root


def _run_prepare(
    *,
    source_root: str,
    det_dir: str,
    rec_dir: str,
    cls_dir: Optional[str],
    cls_optional: bool,
    source_notes: str,
    det_url: str,
    rec_url: str,
    cls_url: str,
    target_root: str,
    manifest: str,
    model_files_manifest: str,
    clean_target: bool,
) -> Dict[str, Any]:
    prepare_py = os.path.join(REPO_ROOT, "tools", "prepare_paddleocr_pinned_weights_v0.py")
    cmd: List[str] = [
        sys.executable,
        prepare_py,
        "--source-root",
        source_root,
        "--det-source-dir",
        det_dir,
        "--rec-source-dir",
        rec_dir,
        "--target-root",
        target_root,
        "--manifest",
        manifest,
        "--model-files-manifest",
        model_files_manifest,
        "--source-notes",
        source_notes,
        "--allow-download",
        "false",
    ]
    if det_url:
        cmd += ["--det-source-url", det_url]
    if rec_url:
        cmd += ["--rec-source-url", rec_url]
    if cls_url:
        cmd += ["--cls-source-url", cls_url]
    if cls_optional:
        cmd.append("--cls-optional")
    if clean_target:
        cmd.append("--clean-target")
    if cls_dir:
        cmd += ["--cls-source-dir", cls_dir]

    p = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    out: Dict[str, Any] = {"cmd": cmd, "returncode": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}
    return out


def _run_readiness(manifest: str, out_dir: str) -> Dict[str, Any]:
    check_py = os.path.join(REPO_ROOT, "tools", "check_ocr_model_readiness_v0.py")
    cmd = [sys.executable, check_py, "--manifest", manifest, "--out-dir", out_dir]
    p = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    return {"cmd": cmd, "returncode": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--source-type",
        required=True,
        choices=["official", "huggingface", "gitee", "manual_url", "local_dir"],
        help="Acquisition strategy",
    )
    ap.add_argument("--model-profile", default="ppocrv5_zh_en_lightweight", help="Logging only (official/init)")
    ap.add_argument("--allow-download", default="false", choices=["true", "false"])
    ap.add_argument("--source-root", default=None, help="Local directory root (local_dir / post-download staging anchor)")
    ap.add_argument("--det-url", default=None, help="URL to det archive or file")
    ap.add_argument("--rec-url", default=None, help="URL to rec archive or file")
    ap.add_argument("--cls-url", default=None, help="URL to cls archive or file (optional)")
    ap.add_argument("--det-path", default=None, help="Local filesystem path to det tree (contains inference files)")
    ap.add_argument("--rec-path", default=None, help="Local filesystem path to rec tree")
    ap.add_argument("--cls-path", default=None, help="Local filesystem path to cls tree")
    ap.add_argument("--hf-det-repo", default=None, help="e.g. PaddlePaddle/PP-OCRv5_mobile_det")
    ap.add_argument("--hf-rec-repo", default=None, help="e.g. PaddlePaddle/PP-OCRv5_mobile_rec")
    ap.add_argument("--hf-cls-repo", default=None, help="optional cls repo id")
    ap.add_argument("--cls-optional", action="store_true", help="Allow missing cls (pinned_partial)")
    ap.add_argument("--source-notes", default="", help="Human provenance string recorded into manifests")
    ap.add_argument("--cache-root", action="append", default=[], help="Extra cache roots to scan (official)")
    ap.add_argument("--output", required=True, help="Acquisition JSON log path")
    ap.add_argument("--staging-dir", default=None, help="Optional staging directory for downloads (default: logs/...)")
    ap.add_argument("--invoke-prepare", default="true", choices=["true", "false"])
    ap.add_argument("--run-readiness", default="true", choices=["true", "false"])
    ap.add_argument("--target-root", default=None, help="External OCR root (default: LUNA_MODELS_ROOT/ocr/paddleocr_ppocrv5)")
    ap.add_argument("--manifest", default="configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json")
    ap.add_argument("--model-files-manifest", default="configs/models/ocr/paddleocr_ppocrv5_model_files_manifest_v0.json")
    ap.add_argument("--clean-target", action="store_true")
    args = ap.parse_args()

    if not args.target_root:
        sys.path.insert(0, REPO_ROOT)
        from capabilities.model_paths_v1 import resolve_model_path

        args.target_root = str(resolve_model_path("ocr/paddleocr_ppocrv5"))

    allow_download = str(args.allow_download).lower() == "true"
    invoke_prepare = str(args.invoke_prepare).lower() == "true"
    run_readiness = str(args.run_readiness).lower() == "true"

    ts = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    staging = args.staging_dir
    if not staging:
        staging = os.path.join(REPO_ROOT, "logs", f"paddleocr_acquire_staging_{ts}")
    staging = os.path.abspath(os.path.expanduser(staging))
    os.makedirs(staging, exist_ok=True)

    downloads: List[Dict[str, Any]] = []
    det_dir: Optional[str] = None
    rec_dir: Optional[str] = None
    cls_dir: Optional[str] = None
    det_url_prov = (args.det_url or "").strip()
    rec_url_prov = (args.rec_url or "").strip()
    cls_url_prov = (args.cls_url or "").strip()

    report: Dict[str, Any] = {
        "phase": "Phase-ModelOCR-003-Fix-003",
        "tool": "acquire_paddleocr_weights_v0.py",
        "timestamp": _now_iso(),
        "platform": {"system": platform.system(), "platform": platform.platform(), "python": sys.version},
        "inputs": {
            "source_type": args.source_type,
            "allow_download": allow_download,
            "source_root": args.source_root,
            "det_url": args.det_url,
            "rec_url": args.rec_url,
            "cls_url": args.cls_url,
            "det_path": args.det_path,
            "rec_path": args.rec_path,
            "cls_path": args.cls_path,
            "hf_det_repo": args.hf_det_repo,
            "hf_rec_repo": args.hf_rec_repo,
            "hf_cls_repo": args.hf_cls_repo,
            "cls_optional": bool(args.cls_optional),
            "source_notes": args.source_notes,
            "staging_dir": os.path.relpath(staging, REPO_ROOT) if staging.startswith(REPO_ROOT) else staging,
        },
        "dependency_check": [
            _check_import("paddleocr"),
            _check_import("paddle"),
            _check_import("cv2"),
            _check_import("numpy"),
            _check_import("PIL"),
        ],
        "downloads": downloads,
        "discovered": {"det_dir": None, "rec_dir": None, "cls_dir": None},
        "prepare": None,
        "readiness": None,
        "hard_blockers": [],
        "soft_followups": [],
    }

    st = str(args.source_type)

    # --- Acquire by source-type ---
    if st == "local_dir":
        root = args.source_root or args.det_path or args.rec_path
        if not root:
            report["hard_blockers"].append("local_dir_requires_source_root_or_paths")
        else:
            root_abs = os.path.abspath(os.path.expanduser(str(root)))
            if args.det_path:
                det_dir = os.path.abspath(os.path.expanduser(str(args.det_path)))
            if args.rec_path:
                rec_dir = os.path.abspath(os.path.expanduser(str(args.rec_path)))
            if args.cls_path:
                cls_dir = os.path.abspath(os.path.expanduser(str(args.cls_path)))
            if not det_dir or not rec_dir:
                scan_root = root_abs
                infer_dirs = _walk_find_infer_dirs(scan_root)
                det_cands = [d for d in infer_dirs if _classify_role_from_path(d) == "det"]
                rec_cands = [d for d in infer_dirs if _classify_role_from_path(d) == "rec"]
                cls_cands = [d for d in infer_dirs if _classify_role_from_path(d) == "cls"]
                if not det_dir:
                    det_dir, _n = _pick_single_role(det_cands, "det")
                if not rec_dir:
                    rec_dir, _n = _pick_single_role(rec_cands, "rec")
                if not cls_dir and not args.cls_optional:
                    cls_dir, _n = _pick_single_role(cls_cands, "cls")

    elif st in ("manual_url", "gitee"):
        if not allow_download:
            report["hard_blockers"].append("manual_url_requires_allow_download_true")
        else:
            if not args.det_url or not args.rec_url:
                report["hard_blockers"].append("manual_url_requires_det_and_rec_url")
            else:

                def _infer_from_downloaded(role: str, url: str, dest_file: str) -> Optional[str]:
                    lower = dest_file.lower()
                    if lower.endswith((".zip", ".tar.gz", ".tgz", ".tar")):
                        ext_dir = os.path.join(staging, f"{role}_extracted")
                        os.makedirs(ext_dir, exist_ok=True)
                        _extract_if_archive(dest_file, ext_dir)
                        return _first_infer_subdir(ext_dir)
                    return _first_infer_subdir(os.path.dirname(dest_file))

                for role, url in [("det", args.det_url), ("rec", args.rec_url)]:
                    dest = os.path.join(staging, role, os.path.basename(url.split("?")[0]))
                    rec = _download_url(url, dest)
                    downloads.append({**rec, "role": role, "source_type": st})
                    infer_root = _infer_from_downloaded(role, url, dest)
                    if role == "det":
                        det_dir = infer_root
                    else:
                        rec_dir = infer_root
                if args.cls_url:
                    dest = os.path.join(staging, "cls", os.path.basename(args.cls_url.split("?")[0]))
                    recd = _download_url(args.cls_url, dest)
                    downloads.append({**recd, "role": "cls", "source_type": st})
                    cls_dir = _infer_from_downloaded("cls", args.cls_url, dest)

    elif st == "huggingface":
        if not allow_download:
            report["hard_blockers"].append("huggingface_requires_allow_download_true")
        else:
            if args.hf_det_repo and args.hf_rec_repo:
                try:
                    det_dir = _hf_download_inference_repo(str(args.hf_det_repo), os.path.join(staging, "hf_det"), downloads)
                    rec_dir = _hf_download_inference_repo(str(args.hf_rec_repo), os.path.join(staging, "hf_rec"), downloads)
                    det_url_prov = det_url_prov or f"hf://{args.hf_det_repo}"
                    rec_url_prov = rec_url_prov or f"hf://{args.hf_rec_repo}"
                    if args.hf_cls_repo:
                        cls_dir = _hf_download_inference_repo(str(args.hf_cls_repo), os.path.join(staging, "hf_cls"), downloads)
                        cls_url_prov = cls_url_prov or f"hf://{args.hf_cls_repo}"
                except RuntimeError as e:
                    report["hard_blockers"].append(f"hf_acquire_failed:{e}")
            elif args.det_url and args.rec_url and args.det_url.startswith("http") and args.rec_url.startswith("http"):

                def _infer_from_downloaded_hf(role: str, dest_file: str) -> Optional[str]:
                    lower = dest_file.lower()
                    if lower.endswith((".zip", ".tar.gz", ".tgz", ".tar")):
                        ext_dir = os.path.join(staging, f"{role}_extracted")
                        os.makedirs(ext_dir, exist_ok=True)
                        _extract_if_archive(dest_file, ext_dir)
                        return _first_infer_subdir(ext_dir)
                    return _first_infer_subdir(os.path.dirname(dest_file))

                for role, url in [("det", args.det_url), ("rec", args.rec_url)]:
                    dest = os.path.join(staging, role, os.path.basename(url.split("?")[0]))
                    rec = _download_url(url, dest)
                    downloads.append({**rec, "role": role, "source_type": "huggingface_url"})
                    infer_root = _infer_from_downloaded_hf(role, dest)
                    if role == "det":
                        det_dir = infer_root
                    else:
                        rec_dir = infer_root
                if args.cls_url:
                    dest = os.path.join(staging, "cls", os.path.basename(args.cls_url.split("?")[0]))
                    recd = _download_url(args.cls_url, dest)
                    downloads.append({**recd, "role": "cls", "source_type": "huggingface_url"})
                    cls_dir = _infer_from_downloaded_hf("cls", dest)
            else:
                report["hard_blockers"].append("huggingface_requires_repos_or_http_urls")

    elif st == "official":
        roots = _default_cache_roots() + [os.path.abspath(os.path.expanduser(x)) for x in (args.cache_root or [])]
        scan = _scan_caches(roots)
        report["cache_scan"] = scan
        infer_dirs = list(scan.get("infer_dirs") or [])
        det_cands = [d for d in infer_dirs if _classify_role_from_path(d) == "det"]
        rec_cands = [d for d in infer_dirs if _classify_role_from_path(d) == "rec"]
        cls_cands = [d for d in infer_dirs if _classify_role_from_path(d) == "cls"]
        det_dir, _ = _pick_single_role(det_cands, "det")
        rec_dir, _ = _pick_single_role(rec_cands, "rec")
        cls_dir, _ = _pick_single_role(cls_cands, "cls")
        if allow_download:
            report["init_only"] = _attempt_init_only(str(args.model_profile))
            scan2 = _scan_caches(roots)
            report["cache_scan_after_init"] = scan2
            infer_dirs2 = list(scan2.get("infer_dirs") or [])
            det_cands2 = [d for d in infer_dirs2 if _classify_role_from_path(d) == "det"]
            rec_cands2 = [d for d in infer_dirs2 if _classify_role_from_path(d) == "rec"]
            cls_cands2 = [d for d in infer_dirs2 if _classify_role_from_path(d) == "cls"]
            d2, _ = _pick_single_role(det_cands2, "det")
            r2, _ = _pick_single_role(rec_cands2, "rec")
            c2, _ = _pick_single_role(cls_cands2, "cls")
            det_dir = d2 or det_dir
            rec_dir = r2 or rec_dir
            cls_dir = c2 or cls_dir
        else:
            report["init_only"] = {"attempted": False, "error": "allow_download_false"}

    # Validate inference presence
    if det_dir and not _first_infer_subdir(det_dir):
        report["hard_blockers"].append("det_inference_pair_not_found")
        det_dir = None
    if rec_dir and not _first_infer_subdir(rec_dir):
        report["hard_blockers"].append("rec_inference_pair_not_found")
        rec_dir = None
    if cls_dir and not _first_infer_subdir(cls_dir):
        if args.cls_optional:
            report["soft_followups"].append("cls_inference_pair_not_found_treated_as_optional")
            cls_dir = None
        else:
            report["hard_blockers"].append("cls_inference_pair_not_found")

    if not det_dir or not rec_dir:
        report["hard_blockers"].append("missing_required_det_or_rec")

    if not args.cls_optional and not cls_dir:
        report["hard_blockers"].append("missing_cls_and_cls_optional_false")

    report["discovered"]["det_dir"] = det_dir
    report["discovered"]["rec_dir"] = rec_dir
    report["discovered"]["cls_dir"] = cls_dir

    notes = str(args.source_notes or "").strip()
    if not notes:
        notes = f"source_type={st};staging={os.path.relpath(staging, REPO_ROOT) if staging.startswith(REPO_ROOT) else staging}"

    prepare_out = None
    readiness_out = None
    hb = [x for x in report["hard_blockers"]]
    if invoke_prepare and det_dir and rec_dir and len(hb) == 0:
        anchor = args.source_root or staging
        anchor_abs = os.path.abspath(os.path.expanduser(str(anchor)))
        prepare_out = _run_prepare(
            source_root=anchor_abs,
            det_dir=det_dir,
            rec_dir=rec_dir,
            cls_dir=cls_dir,
            cls_optional=bool(args.cls_optional),
            source_notes=notes,
            det_url=det_url_prov,
            rec_url=rec_url_prov,
            cls_url=cls_url_prov,
            target_root=str(args.target_root),
            manifest=str(args.manifest),
            model_files_manifest=str(args.model_files_manifest),
            clean_target=bool(args.clean_target),
        )
        report["prepare"] = prepare_out
        if prepare_out.get("returncode") != 0:
            report["hard_blockers"].append("prepare_failed")

    if run_readiness and invoke_prepare and prepare_out and prepare_out.get("returncode") == 0:
        readiness_out = _run_readiness(str(args.manifest), "logs")
        report["readiness"] = readiness_out
        if readiness_out.get("returncode") != 0:
            report["soft_followups"].append("readiness_nonzero_exit_check_stdout")

    out_path = str(args.output)
    out_abs = os.path.abspath(os.path.join(REPO_ROOT, out_path)) if not os.path.isabs(out_path) else os.path.abspath(out_path)
    _write_json(out_abs, report)

    print(
        json.dumps(
            {
                "ok": len(report["hard_blockers"]) == 0,
                "output": os.path.relpath(out_abs, REPO_ROOT) if out_abs.startswith(REPO_ROOT) else out_abs,
                "hard_blockers": report["hard_blockers"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if not report["hard_blockers"] else 3


if __name__ == "__main__":
    raise SystemExit(main())

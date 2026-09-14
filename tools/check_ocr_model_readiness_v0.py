#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelOCR-003: OCR model readiness check (v0).

Reads a manifest and checks:
- manifest schema + invariants
- dependency import/version (best-effort; no installs)
- weights path/hash/size (no downloads)
- directory-based weights via file-level manifest (pinned_local / pinned_partial)
- provider kind legality and system provider precheck

Never enters runtime; never runs OCR.
Writes a JSON report under logs/.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import platform
import sys
from typing import Any, Dict, List, Optional, Tuple


REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("manifest must be a dict")
    return data


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


def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _dir_has_paddle_infer_files_tree(d: str) -> bool:
    """
    Treat a directory as a "real prepared" Paddle inference directory only if
    we find inference.pdiparams plus either inference.pdmodel or inference.json
    in the same folder (legacy vs PP-OCRv5 HF export layout).
    """
    if not d or not os.path.isdir(d):
        return False
    for root, dirs, files in os.walk(d):
        names = set(files)
        if "inference.pdiparams" not in names:
            continue
        if "inference.pdmodel" in names or "inference.json" in names:
            return True
    return False


def _resolve_repo_path(p: Optional[str]) -> Optional[str]:
    if not p:
        return None
    if os.path.isabs(p):
        return p
    return os.path.abspath(os.path.join(REPO_ROOT, p))


def _check_import(pkg: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {"package": pkg, "import_ok": False, "version": None, "error": None}
    try:
        __import__(pkg)
        out["import_ok"] = True
    except Exception as e:
        out["error"] = str(e)
        return out
    try:
        from importlib import metadata as _md

        out["version"] = _md.version(pkg)
    except Exception:
        pass
    return out


def _required_bool(m: Dict[str, Any], key: str, expected: bool, hard_blockers: List[str]) -> None:
    v = m.get(key, None)
    if v is not expected:
        hard_blockers.append(f"manifest_invariant_failed:{key} expected={expected} got={v}")


def _is_provider_kind_ok(v: str) -> bool:
    return v in ("local_model", "system_provider", "online_or_service", "unavailable")


def _is_weights_source_ok(v: str) -> bool:
    return v in ("pinned_local", "pinned_partial", "system_builtin", "manual_download_required", "unavailable")


def _load_file_manifest(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    if not isinstance(obj, dict):
        raise ValueError("model_files_manifest must be a dict")
    if "files" not in obj or not isinstance(obj.get("files"), list):
        raise ValueError("model_files_manifest missing 'files' list")
    return obj


def _file_manifest_summary(files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Stable aggregate hash for a set of file records.
    We hash lines of: sha256<TAB>size<TAB>role<TAB>relative_path
    sorted lexicographically by (role, relative_path).
    """
    norm_lines: List[str] = []
    total = 0
    for r in files:
        rp = str(r.get("relative_path") or "")
        role = str(r.get("role") or "")
        sha = str(r.get("sha256") or "")
        sz = int(r.get("file_size_bytes") or 0)
        total += max(sz, 0)
        norm_lines.append(f"{sha}\t{sz}\t{role}\t{rp}")
    norm_lines.sort()
    agg = _sha256_text("\n".join(norm_lines) + "\n")
    return {"algorithm": "sha256_of_manifest_lines_v0", "sha256": agg, "file_count": len(files), "total_file_size_bytes": total}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, help="Path to manifest JSON")
    ap.add_argument("--out-dir", default="logs", help="Directory for readiness logs (repo-relative)")
    args = ap.parse_args()

    manifest_path = _resolve_repo_path(args.manifest) or str(args.manifest)
    m = _load_json(manifest_path)

    hard_blockers: List[str] = []
    soft_followups: List[str] = []

    # Minimal schema presence
    for k in [
        "manifest_version",
        "model_config_id",
        "model_family",
        "model_name",
        "model_variant",
        "model_task",
        "candidate_tier",
        "provider_kind",
        "weights_source",
        "weights_paths",
        "raw_text_only",
        "semantic_interpretation_enabled",
        "allows_execute_now",
        "real_tts_invoked",
        "verification_status",
    ]:
        if k not in m:
            hard_blockers.append(f"missing_required_field:{k}")

    provider_kind = str(m.get("provider_kind") or "")
    weights_source = str(m.get("weights_source") or "")
    if not _is_provider_kind_ok(provider_kind):
        hard_blockers.append(f"invalid_provider_kind:{provider_kind}")
    if not _is_weights_source_ok(weights_source):
        hard_blockers.append(f"invalid_weights_source:{weights_source}")

    # Raw-text only invariants
    _required_bool(m, "raw_text_only", True, hard_blockers)
    _required_bool(m, "semantic_interpretation_enabled", False, hard_blockers)
    _required_bool(m, "allows_execute_now", False, hard_blockers)
    _required_bool(m, "real_tts_invoked", False, hard_blockers)

    weights_paths = m.get("weights_paths") if isinstance(m.get("weights_paths"), dict) else {}
    if not isinstance(weights_paths, dict):
        hard_blockers.append("weights_paths_not_dict")
        weights_paths = {}

    # Dependency check (best-effort)
    family = str(m.get("model_family") or "")
    dep_checks: List[Dict[str, Any]] = []
    if family == "paddleocr":
        for pkg in ["paddleocr", "paddle", "cv2", "numpy", "PIL"]:
            dep_checks.append(_check_import(pkg))
    elif family == "macos_vision_ocr":
        # This repo is Python; Vision OCR is a system framework (Swift/ObjC).
        # Precheck: only validate platform for now.
        dep_checks.append({"package": "platform_darwin", "import_ok": platform.system() == "Darwin", "version": None, "error": None})
    else:
        # candidates: do not require deps in ModelOCR-003
        dep_checks.append({"package": "not_checked", "import_ok": True, "version": None, "error": None})

    dep_missing = [d for d in dep_checks if not bool(d.get("import_ok"))]
    if family == "paddleocr" and dep_missing:
        soft_followups.append("dependency_missing:paddleocr_stack_not_installed")
    if family == "macos_vision_ocr" and platform.system() != "Darwin":
        hard_blockers.append("system_provider_unavailable:not_darwin")

    # Weights check (no downloads)
    weights_check: Dict[str, Any] = {
        "paths": {},
        "sha256": {},
        "sizes": {},
        "missing": [],
        "mismatch": [],
        "directory_mode": False,
        "model_files_manifest_path": m.get("model_files_manifest_path"),
        "model_files_manifest_check": {"attempted": False, "ok": None, "errors": [], "summary": None, "role_coverage": {}},
    }
    declared_sha = m.get("weights_sha256") if isinstance(m.get("weights_sha256"), dict) else {}
    declared_sz = m.get("weights_file_size_bytes") if isinstance(m.get("weights_file_size_bytes"), dict) else {}

    def _check_one(name: str, p: Optional[str]) -> None:
        rp = _resolve_repo_path(p)
        weights_check["paths"][name] = p
        if not rp:
            # tokenizer_path is optional for now
            if name != "tokenizer_path":
                weights_check["missing"].append(name)
            return
        if not os.path.exists(rp):
            if name != "tokenizer_path":
                weights_check["missing"].append(name)
            return
        if os.path.isdir(rp):
            weights_check["directory_mode"] = True
            # For skeleton manifests we still want to distinguish placeholders vs prepared dirs.
            # If this directory does NOT contain Paddle inference files, count it as missing.
            if name in ("det_model_path", "rec_model_path", "cls_model_path") and not _dir_has_paddle_infer_files_tree(rp):
                weights_check["missing"].append(name)
            return
        sha, size = _sha256_file(rp)
        weights_check["sha256"][name] = sha
        weights_check["sizes"][name] = size
        if declared_sha.get(name) and declared_sha.get(name) != sha:
            weights_check["mismatch"].append(f"sha256:{name}")
        if declared_sz.get(name) and int(declared_sz.get(name)) != int(size):
            weights_check["mismatch"].append(f"size:{name}")

    for k in ["det_model_path", "rec_model_path", "cls_model_path", "tokenizer_path"]:
        _check_one(k, weights_paths.get(k))

    # Directory-based weights: validate model_files_manifest when pinned_local/pinned_partial.
    cls_optional = bool((m.get("weights_policy") or {}).get("cls_optional")) if isinstance(m.get("weights_policy"), dict) else bool(m.get("cls_optional", False))
    if weights_check["directory_mode"] and weights_source in ("pinned_local", "pinned_partial"):
        mf_rel = m.get("model_files_manifest_path")
        mf_abs = _resolve_repo_path(str(mf_rel)) if mf_rel else None
        weights_check["model_files_manifest_check"]["attempted"] = True
        if not mf_abs or not os.path.exists(mf_abs):
            weights_check["model_files_manifest_check"]["ok"] = False
            weights_check["model_files_manifest_check"]["errors"].append("missing_model_files_manifest_path")
        else:
            try:
                mf_obj = _load_file_manifest(mf_abs)
                files = mf_obj.get("files") or []
                if not isinstance(files, list):
                    raise ValueError("'files' must be a list")
                role_cov = {"det": 0, "rec": 0, "cls": 0, "other": 0}
                errors: List[str] = []
                mismatch: List[str] = []
                missing: List[str] = []
                for r in files:
                    if not isinstance(r, dict):
                        errors.append("file_record_not_dict")
                        continue
                    rel_path = str(r.get("relative_path") or "")
                    sha_decl = str(r.get("sha256") or "")
                    sz_decl = r.get("file_size_bytes")
                    role = str(r.get("role") or "")
                    if role in ("det", "rec", "cls"):
                        role_cov[role] += 1
                    else:
                        role_cov["other"] += 1
                    if not rel_path or ".." in rel_path.replace("\\", "/").split("/"):
                        errors.append(f"bad_relative_path:{rel_path}")
                        continue
                    abs_path = os.path.abspath(os.path.join(REPO_ROOT, rel_path))
                    if not abs_path.startswith(REPO_ROOT):
                        errors.append(f"path_escape:{rel_path}")
                        continue
                    if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
                        missing.append(rel_path)
                        continue
                    sha_act, sz_act = _sha256_file(abs_path)
                    if sha_decl and sha_decl != sha_act:
                        mismatch.append(f"sha256:{rel_path}")
                    if sz_decl is not None and int(sz_decl) != int(sz_act):
                        mismatch.append(f"size:{rel_path}")
                weights_check["model_files_manifest_check"]["role_coverage"] = role_cov
                weights_check["model_files_manifest_check"]["summary"] = _file_manifest_summary([r for r in files if isinstance(r, dict)])
                if errors:
                    weights_check["model_files_manifest_check"]["errors"].extend(errors)
                if missing:
                    weights_check["model_files_manifest_check"]["errors"].append(f"missing_files_count:{len(missing)}")
                if mismatch:
                    weights_check["model_files_manifest_check"]["errors"].append(f"mismatch_count:{len(mismatch)}")
                # Surface into weights_check mismatch list for pinned gating.
                for x in mismatch:
                    weights_check["mismatch"].append(f"file_manifest_{x}")
                for x in missing:
                    weights_check["missing"].append(f"file_manifest_missing:{x}")
                # Basic role coverage: det+rec required; cls required unless optional.
                if role_cov["det"] <= 0:
                    weights_check["missing"].append("file_manifest_role_missing:det")
                if role_cov["rec"] <= 0:
                    weights_check["missing"].append("file_manifest_role_missing:rec")
                if role_cov["cls"] <= 0 and not cls_optional:
                    weights_check["missing"].append("file_manifest_role_missing:cls")
                weights_check["model_files_manifest_check"]["ok"] = len(weights_check["model_files_manifest_check"]["errors"]) == 0
            except Exception as e:
                weights_check["model_files_manifest_check"]["ok"] = False
                weights_check["model_files_manifest_check"]["errors"].append(f"manifest_parse_error:{e}")

    # Enforce "no fake pass": pinned_local requires weights present and matching.
    if weights_source == "pinned_local":
        if weights_check["missing"]:
            hard_blockers.append("pinned_local_but_missing_weights")
        if weights_check["mismatch"]:
            hard_blockers.append("pinned_local_but_hash_mismatch")
        if weights_check["directory_mode"] and not bool(weights_check["model_files_manifest_check"].get("ok")):
            hard_blockers.append("pinned_local_but_model_files_manifest_invalid")

    # pinned_partial: allow cls missing only if explicitly optional; still require det+rec and hash consistency when present.
    if weights_source == "pinned_partial":
        # If cls is optional, allow cls missing markers but not det/rec missing.
        missing = list(weights_check.get("missing") or [])
        if cls_optional:
            missing_non_cls = [x for x in missing if ("cls" not in x and "file_manifest_role_missing:cls" not in x)]
            if missing_non_cls:
                hard_blockers.append("pinned_partial_missing_required_assets")
        else:
            if missing:
                hard_blockers.append("pinned_partial_but_missing_weights")
        if weights_check["mismatch"]:
            hard_blockers.append("pinned_partial_but_hash_mismatch")

    # Provider check
    provider_check: Dict[str, Any] = {"provider_kind": provider_kind, "system_precheck_ok": None}
    if provider_kind == "system_provider":
        provider_check["system_precheck_ok"] = platform.system() == "Darwin"
    else:
        provider_check["system_precheck_ok"] = True

    # Contract check (declared output)
    contract_check = {
        "expected_output_format": m.get("expected_output_format"),
        "supports_bbox": m.get("supports_bbox"),
        "supports_confidence": m.get("supports_confidence"),
    }

    # Determine readiness status
    readiness_status = "ready"
    if hard_blockers:
        readiness_status = "not_ready"
    else:
        # Skeleton manifests with missing weights are partial, not ready.
        if weights_check["missing"] and weights_source in ("manual_download_required", "unavailable"):
            readiness_status = "partial"
        if family == "paddleocr" and dep_missing:
            readiness_status = "partial"
        if weights_source in ("pinned_local", "pinned_partial") and weights_check["directory_mode"]:
            # Directory pinned weights require file-manifest validation to be "ready".
            if not bool(weights_check["model_files_manifest_check"].get("ok")):
                readiness_status = "partial"

    report: Dict[str, Any] = {
        "phase": "Phase-ModelOCR-003",
        "timestamp": _now_iso(),
        "model_config_id": m.get("model_config_id"),
        "model_family": family,
        "candidate_tier": m.get("candidate_tier"),
        "manifest_path": os.path.relpath(manifest_path, REPO_ROOT) if manifest_path.startswith(REPO_ROOT) else manifest_path,
        "dependency_check": dep_checks,
        "weights_check": weights_check,
        "provider_check": provider_check,
        "raw_text_contract_check": contract_check,
        "forbidden_semantic_check": {
            "raw_text_only": m.get("raw_text_only"),
            "semantic_interpretation_enabled": m.get("semantic_interpretation_enabled"),
            "allows_execute_now": m.get("allows_execute_now"),
            "real_tts_invoked": m.get("real_tts_invoked"),
        },
        "fallback_check": m.get("fallback_policy"),
        "readiness_status": readiness_status,
        "hard_blockers": hard_blockers,
        "soft_followups": soft_followups,
        "recommendation": "do_not_enter_runtime",
    }

    out_dir = _resolve_repo_path(args.out_dir) or os.path.abspath(os.path.join(REPO_ROOT, "logs"))
    os.makedirs(out_dir, exist_ok=True)
    ts = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(out_dir, f"ocr_model_readiness_{m.get('model_config_id','unknown')}_{ts}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    print(json.dumps({"ok": True, "out": os.path.relpath(out_path, REPO_ROOT), "readiness_status": readiness_status}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


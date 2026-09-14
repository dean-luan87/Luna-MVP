# -*- coding: utf-8 -*-
"""Document Surface — iteration input loader v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

MANIFEST_REL = "_fixtures/document_surface_real_runtime_controlled_iteration_v2/registry_manifest_v1.json"
INPUT_ROOT_REL = "_fixtures/document_surface_real_runtime_controlled_iteration_v2/"
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def load_iteration_manifest(*, repo_root: Path) -> Dict[str, Any]:
    path = repo_root / MANIFEST_REL
    if not path.is_file():
        return {"entries": [], "manifest_missing": True}
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_iteration_image_path(
    *,
    repo_root: Path,
    image_ref: str,
    manifest: Optional[Dict[str, Any]] = None,
) -> Tuple[Optional[Path], Optional[str]]:
    if image_ref.startswith("/") or ".." in image_ref:
        return None, "input_not_in_registry"
    man = manifest or load_iteration_manifest(repo_root=repo_root)
    declared = {e.get("image_ref") for e in (man.get("entries") or [])}
    if image_ref not in declared:
        return None, "input_not_in_registry"
    full = (repo_root / INPUT_ROOT_REL / image_ref).resolve()
    root = (repo_root / INPUT_ROOT_REL).resolve()
    try:
        full.relative_to(root)
    except ValueError:
        return None, "input_not_in_registry"
    return full, None


def audit_iteration_fixtures(*, repo_root: Path) -> Dict[str, Any]:
    manifest = load_iteration_manifest(repo_root=repo_root)
    entries = manifest.get("entries") or []
    required = [e for e in entries if e.get("requires_execution") is not False]
    existing: List[str] = []
    missing: List[str] = []
    for entry in required:
        ref = entry.get("image_ref", "")
        if entry.get("real_image_attached") is False:
            missing.append(ref)
            continue
        path, _ = resolve_iteration_image_path(repo_root=repo_root, image_ref=ref, manifest=manifest)
        if path and path.is_file():
            existing.append(ref)
        else:
            missing.append(ref)
    return {
        "manifest_loaded": not manifest.get("manifest_missing"),
        "total_registry_entries": len(entries),
        "execution_entries_required": len(required),
        "existing_files": existing,
        "missing_files": missing,
        "iteration_fixtures_ready": len(missing) == 0 and len(required) >= 8,
        "blocked_by_missing_iteration_fixtures": len(missing) > 0,
    }


def load_iteration_image(*, repo_root: Path, image_ref: str, manifest: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    path, boundary_abort = resolve_iteration_image_path(repo_root=repo_root, image_ref=image_ref, manifest=manifest)
    if boundary_abort:
        return {"loaded": False, "abort_reason": boundary_abort, "image_ref": image_ref}
    if Path(image_ref).suffix.lower() not in ALLOWED_EXTENSIONS:
        return {"loaded": False, "abort_reason": "unsupported_image_format", "image_ref": image_ref}
    if not path or not path.is_file():
        return {"loaded": False, "abort_reason": "image_read_failed", "image_ref": image_ref}
    try:
        import cv2
        img = cv2.imread(str(path))
        if img is None:
            return {"loaded": False, "abort_reason": "image_read_failed", "image_ref": image_ref}
        return {"loaded": True, "image_ref": image_ref, "path": str(path), "image_bgr": img, "abort_reason": None}
    except ImportError:
        return {"loaded": False, "abort_reason": "dependency_missing", "image_ref": image_ref}

# -*- coding: utf-8 -*-
"""Document Surface — controlled input loader v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

MANIFEST_REL = "_fixtures/document_surface_real_runtime_controlled/registry_manifest_v1.json"
INPUT_ROOT_REL = "_fixtures/document_surface_real_runtime_controlled/"
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}
FORBIDDEN_PREFIXES = ("/Users/", "/home/", "http://", "https://", "s3://", "file://")


def load_registry_manifest(*, repo_root: Path) -> Dict[str, Any]:
    path = repo_root / MANIFEST_REL
    if not path.is_file():
        return {"entries": [], "manifest_missing": True}
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_registry_image_path(
    *,
    repo_root: Path,
    image_ref: str,
    manifest: Optional[Dict[str, Any]] = None,
) -> Tuple[Optional[Path], Optional[str]]:
    """Resolve image path only if declared in manifest. Returns (path, abort_reason)."""
    if any(image_ref.startswith(p) for p in FORBIDDEN_PREFIXES) or image_ref.startswith("/") or ".." in image_ref:
        return None, "input_not_in_registry"
    man = manifest or load_registry_manifest(repo_root=repo_root)
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


def check_extension_allowed(image_ref: str) -> bool:
    return Path(image_ref).suffix.lower() in ALLOWED_EXTENSIONS


def audit_fixture_availability(*, repo_root: Path) -> Dict[str, Any]:
    manifest = load_registry_manifest(repo_root=repo_root)
    entries = manifest.get("entries") or []
    existing: List[str] = []
    missing: List[str] = []
    for entry in entries:
        ref = entry.get("image_ref", "")
        path, _ = resolve_registry_image_path(repo_root=repo_root, image_ref=ref, manifest=manifest)
        if path and path.is_file():
            existing.append(ref)
        else:
            missing.append(ref)
    png_required = [
        e for e in entries
        if (e.get("image_ref") or "").endswith(".png")
        and e.get("real_image_attached", True) is not False
        and e.get("category") != "image_read_failed_controlled"
    ]
    png_missing = [e.get("image_ref") for e in png_required if e.get("image_ref") not in existing]
    return {
        "manifest_loaded": not manifest.get("manifest_missing"),
        "total_registry_entries": len(entries),
        "existing_files": existing,
        "missing_files": missing,
        "png_execution_images_missing": png_missing,
        "execution_fixtures_ready": len(png_missing) == 0 and len(png_required) > 0,
        "blocked_by_missing_fixtures": len(png_missing) > 0,
    }


def load_registry_image(
    *,
    repo_root: Path,
    image_ref: str,
    manifest: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Load image from registry path only. No registry-external reads."""
    path, boundary_abort = resolve_registry_image_path(repo_root=repo_root, image_ref=image_ref, manifest=manifest)
    if boundary_abort:
        return {"loaded": False, "abort_reason": boundary_abort, "image_ref": image_ref}
    if not check_extension_allowed(image_ref):
        return {"loaded": False, "abort_reason": "unsupported_image_format", "image_ref": image_ref, "path": str(path)}
    if not path or not path.is_file():
        return {"loaded": False, "abort_reason": "image_read_failed", "image_ref": image_ref, "path": str(path) if path else None}
    try:
        import cv2
        img = cv2.imread(str(path))
        if img is None:
            return {"loaded": False, "abort_reason": "image_read_failed", "image_ref": image_ref, "path": str(path)}
        return {
            "loaded": True,
            "image_ref": image_ref,
            "path": str(path),
            "shape": list(img.shape),
            "image_bgr": img,
            "abort_reason": None,
        }
    except ImportError:
        return {"loaded": False, "abort_reason": "dependency_missing", "image_ref": image_ref}

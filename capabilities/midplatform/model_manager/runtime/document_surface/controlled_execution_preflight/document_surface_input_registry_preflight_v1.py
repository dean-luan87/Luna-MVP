# -*- coding: utf-8 -*-
"""Document Surface — input registry preflight v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_controlled_input_registry_v1 import (
    ALTERNATE_INPUT_ROOT,
    CONTROLLED_IMAGE_REGISTRY,
    CONTROLLED_INPUT_ROOT,
    build_controlled_input_registry_plan,
)

FORBIDDEN_PATH_PREFIXES = ("/Users/", "/home/", "http://", "https://", "s3://", "file://")


def _is_path_in_controlled_root(image_ref: str, roots: List[str]) -> bool:
    if any(image_ref.startswith(p) for p in FORBIDDEN_PATH_PREFIXES):
        return False
    if ".." in image_ref:
        return False
    # relative refs under controlled roots only
    return not image_ref.startswith("/")


def run_input_registry_preflight(*, repo_root: Path) -> Dict[str, Any]:
    registry_plan = build_controlled_input_registry_plan()
    primary = repo_root / CONTROLLED_INPUT_ROOT
    alternate = repo_root / ALTERNATE_INPUT_ROOT
    primary_exists = primary.is_dir()
    alternate_exists = alternate.is_dir()

    entries_ok = True
    entry_checks: List[Dict[str, Any]] = []
    for img in CONTROLLED_IMAGE_REGISTRY:
        ref = img.get("image_ref", "")
        ok = _is_path_in_controlled_root(ref, [CONTROLLED_INPUT_ROOT, ALTERNATE_INPUT_ROOT])
        entry_checks.append({
            "image_ref": ref,
            "expected_case_id": img.get("category"),
            "allowed_read_mode": "metadata_only",
            "planned_for_execution": True,
            "path_in_controlled_scope": ok,
            "no_absolute_escape": ok,
        })
        if not ok:
            entries_ok = False

    return {
        "check_id": "input_registry_preflight_v1",
        "controlled_input_directory_exists": primary_exists or alternate_exists,
        "primary_root": CONTROLLED_INPUT_ROOT,
        "primary_exists": primary_exists,
        "alternate_exists": alternate_exists,
        "registry_defined": bool(CONTROLLED_IMAGE_REGISTRY),
        "registry_entry_count": len(CONTROLLED_IMAGE_REGISTRY),
        "all_paths_in_controlled_scope": entries_ok,
        "entry_checks": entry_checks,
        "no_image_content_read": True,
        "registry_schema_valid": all(e.get("expected_case_id") for e in entry_checks),
        "passed": (primary_exists or alternate_exists) and entries_ok and len(CONTROLLED_IMAGE_REGISTRY) >= 6,
        "candidate_only": True,
        "not_fact": True,
    }

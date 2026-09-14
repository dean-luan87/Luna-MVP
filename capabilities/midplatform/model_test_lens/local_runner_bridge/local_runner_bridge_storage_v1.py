# -*- coding: utf-8 -*-
"""Local Runner Bridge — storage layer v1."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path
from typing import List, Optional, Tuple

from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_skeleton_execution_types_v1 import (
    ASSET_STORE_REL,
    EVAL_OUT_REL,
    JOBS_STORE_REL,
    PHASE_ID,
)

_REPO_ROOT = Path(__file__).resolve().parents[4]


def repo_root() -> Path:
    for cand in (_REPO_ROOT, Path.cwd()):
        if (cand / "capabilities").is_dir():
            return cand.resolve()
    return _REPO_ROOT.resolve()


def artifact_roots() -> List[Path]:
    root = repo_root()
    roots: List[Path] = [root, Path.cwd()]
    for extra in (root.parent / "Luna-Core", root.parent / "Luna-Workspace-Min"):
        if extra.is_dir() and extra not in roots:
            roots.append(extra.resolve())
    return list(dict.fromkeys(roots))


def resolve_path(rel: str) -> Path:
    for base in artifact_roots():
        p = base / rel
        if p.exists():
            return p.resolve()
    return (repo_root() / rel).resolve()


def asset_store_dir() -> Path:
    p = repo_root() / ASSET_STORE_REL
    p.mkdir(parents=True, exist_ok=True)
    return p


def eval_out_dir() -> Path:
    p = repo_root() / EVAL_OUT_REL
    p.mkdir(parents=True, exist_ok=True)
    return p


def jobs_store_dir() -> Path:
    p = repo_root() / JOBS_STORE_REL
    p.mkdir(parents=True, exist_ok=True)
    return p


def job_output_dir(job_id: str) -> Path:
    p = eval_out_dir() / "jobs" / job_id
    p.mkdir(parents=True, exist_ok=True)
    return p


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_local_asset(src: Path, asset_id: str) -> Tuple[Optional[Path], str]:
    if not src.is_file():
        return None, "source_file_not_found"
    dest_dir = asset_store_dir() / asset_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    if not dest.is_file() or dest.stat().st_size != src.stat().st_size:
        shutil.copy2(src, dest)
    return dest, "copied_to_asset_store"


def boundary_flags() -> dict:
    return {
        "candidate_only": True,
        "not_fact": True,
        "not_runtime_output": True,
        "not_output_adapter_output": True,
        "not_semantic_output": True,
        "not_navigation_action_speech": True,
    }


def readiness_effect() -> dict:
    return {
        "runtime_ready": False,
        "output_adapter_ready": False,
        "semantic_layer_ready": False,
        "fact_write_ready": False,
        "navigation_action_speech_ready": False,
    }


def common_envelope_meta() -> dict:
    return {
        "phase_ref": PHASE_ID,
        "boundary_flags": boundary_flags(),
        "readiness_effect": readiness_effect(),
    }

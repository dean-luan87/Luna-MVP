# -*- coding: utf-8 -*-
"""External model path resolution — Luna-Core calls Luna-Models out-of-tree."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

_ENV_MODELS_ROOT = "LUNA_MODELS_ROOT"

# 外部分类（权重只落 Luna-Models，不落 Luna-Core）
MODEL_CATEGORIES: Dict[str, str] = {
    "vision": "视觉：检测 / 分割 / 深度 / 跟踪",
    "speech": "语音：TTS / ASR",
    "ocr": "文字识别",
    "language": "语言模型 / LLM",
    "spatial": "空间：SLAM / Scene Graph",
}

# 推荐子目录（manifest / 文档对齐）
MODEL_LAYOUT: Tuple[str, ...] = (
    "vision/detection/yolo",
    "vision/segmentation",
    "vision/depth",
    "vision/tracking",
    "speech/tts/piper",
    "speech/asr",
    "ocr/paddleocr_ppocrv5",
    "ocr/rapidocr",
    "language/llm",
    "spatial/slam",
    "spatial/scene_graph",
)

_WEIGHT_SUFFIXES = (".pt", ".pth", ".onnx", ".safetensors", ".bin", ".pdmodel", ".pdiparams")

# legacy in-repo or flat ref -> categorized external ref (longer prefix first)
_LEGACY_REF_PREFIXES: Tuple[Tuple[str, str], ...] = (
    ("capabilities/voice/models/piper/", "speech/tts/piper/"),
    ("capabilities/voice/models/", "speech/tts/"),
    ("models/ocr/", "ocr/"),
    ("models/yolo/", "vision/detection/yolo/"),
    ("voice/piper/", "speech/tts/piper/"),
    ("voice/", "speech/tts/"),
    ("yolo/", "vision/detection/yolo/"),
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_models_root() -> Path:
    sibling = repo_root().parent / "Luna-Models"
    if sibling.is_dir():
        return sibling.resolve()
    return (Path.home() / "Luna-Data" / "models").resolve()


def get_models_root() -> Path:
    override = os.getenv(_ENV_MODELS_ROOT, "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return default_models_root()


def is_weight_ref(ref: str) -> bool:
    raw = str(ref or "").strip().lower()
    if not raw:
        return False
    if raw.startswith(("configs/", "docs/")):
        return False
    return any(raw.endswith(s) for s in _WEIGHT_SUFFIXES) or "/" in raw and not raw.startswith("configs/")


def normalize_model_ref(ref: str) -> str:
    raw = str(ref or "").strip().replace("\\", "/")
    if not raw:
        return raw
    if raw.startswith("luna-models://"):
        return raw[len("luna-models://") :]
    for legacy, external in _LEGACY_REF_PREFIXES:
        if raw == legacy.rstrip("/") or raw.startswith(legacy):
            if raw == legacy.rstrip("/"):
                return external.rstrip("/")
            return external + raw[len(legacy) :]
    return raw.lstrip("/")


def resolve_model_path(
    ref: Optional[str],
    *,
    repo_root_override: Optional[Union[str, Path]] = None,
    must_exist: bool = False,
    allow_in_repo_fallback: bool = False,
) -> Optional[Path]:
    """Resolve a model ref to an absolute path under LUNA_MODELS_ROOT."""
    if ref is None:
        return None
    raw = str(ref).strip()
    if not raw:
        return None
    if os.path.isabs(raw):
        path = Path(raw).expanduser().resolve()
        if must_exist and not path.exists():
            return None
        return path

    normalized = normalize_model_ref(raw)
    root = get_models_root()
    candidates = [root / normalized]

    if allow_in_repo_fallback or not is_weight_ref(raw):
        rr = Path(repo_root_override).resolve() if repo_root_override else repo_root()
        candidates.append(rr / raw)
        if normalized != raw:
            candidates.append(rr / normalized)

    for path in candidates:
        if path.exists() or not must_exist:
            return path.resolve()
    return candidates[0].resolve()


def category_root(category: str) -> Path:
    if category not in MODEL_CATEGORIES:
        raise ValueError(f"unknown_model_category:{category}")
    return get_models_root() / category


def resolve_preset_model_params(preset: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(preset, dict):
        return preset
    out = dict(preset)
    mp = out.get("model_params")
    if not isinstance(mp, dict):
        return out
    mp2 = dict(mp)
    for key in ("model", "checkpoint_path", "voice_path"):
        if key in mp2 and mp2[key]:
            resolved = resolve_model_path(str(mp2[key]))
            if resolved is not None:
                mp2[key] = str(resolved)
    out["model_params"] = mp2
    return out


def resolve_manifest_weights_path(
    weights_path: str,
    *,
    repo_root_override: Optional[Union[str, Path]] = None,
) -> str:
    resolved = resolve_model_path(weights_path, repo_root_override=repo_root_override, must_exist=False)
    return str(resolved) if resolved is not None else weights_path


def resolve_manifest_model_dir(
    model_dir: str,
    *,
    repo_root_override: Optional[Union[str, Path]] = None,
) -> str:
    """Resolve OCR / multi-file model directory refs to external absolute paths."""
    resolved = resolve_model_path(model_dir, repo_root_override=repo_root_override, must_exist=False)
    return str(resolved) if resolved is not None else model_dir

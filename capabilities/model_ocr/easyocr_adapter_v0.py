from __future__ import annotations

import dataclasses
import hashlib
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

_WS_RE = re.compile(r"\s+")


def _normalize_text(s: str) -> str:
    return _WS_RE.sub(" ", (s or "").strip())


def _quad_to_aabb(pts: Sequence[Sequence[float]]) -> List[float]:
    xs = [float(p[0]) for p in pts]
    ys = [float(p[1]) for p in pts]
    return [min(xs), min(ys), max(xs), max(ys)]


@dataclasses.dataclass(frozen=True)
class _Cand:
    text_id: str
    text: str
    normalized_text: str
    bbox: Optional[List[float]]
    confidence: Optional[float]
    frame_id: str
    timestamp_ms: int
    line_order: int
    allows_execute_now: bool = False


def _serialize(c: _Cand) -> Dict[str, Any]:
    d = dataclasses.asdict(c)
    d["bbox_status"] = "present" if d.get("bbox") is not None else "not_available"
    d["confidence_status"] = "present" if d.get("confidence") is not None else "not_available"
    return d


class EasyOCRAdapterV0:
    """EasyOCR — raw text only (Phase-ModelOCR-006E)."""

    provider_id = "easyocr_multilingual_v0"
    model_config_id = "easyocr_multilingual_zh_en_v0"
    provider_kind = "pip_package"

    def __init__(self, *, lang_list: Optional[List[str]] = None) -> None:
        self._lang_list = lang_list or ["ch_sim", "en"]
        self._reader: Any = None

    def is_available(self) -> Tuple[bool, Optional[str]]:
        try:
            import easyocr  # noqa: F401

            return True, None
        except Exception as e:
            return False, repr(e)

    def dependency_probe(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "package_name": "easyocr",
            "import_name": "easyocr",
            "version": None,
            "install_source": "pip",
            "install_hint": "pip install easyocr",
        }
        try:
            from importlib import metadata as md

            out["version"] = md.version("easyocr")
        except Exception:
            pass
        return out

    def asset_report(self, *, repo_root: str) -> Dict[str, Any]:
        ok, err = self.is_available()
        dep = self.dependency_probe()
        cache_files: List[Dict[str, Any]] = []
        model_dir = Path.home() / ".EasyOCR" / "model"
        if model_dir.is_dir():
            for p in model_dir.rglob("*"):
                if p.is_file() and p.suffix.lower() in (".pth", ".onnx", ".txt", ".yml", ".zip"):
                    try:
                        h = hashlib.sha256()
                        with open(p, "rb") as f:
                            for ch in iter(lambda: f.read(1024 * 1024), b""):
                                h.update(ch)
                        cache_files.append({"path": str(p), "size_bytes": p.stat().st_size, "sha256": h.hexdigest()})
                    except Exception:
                        cache_files.append({"path": str(p), "size_bytes": None, "sha256": None})
        mas = "cache_detected" if cache_files else ("import_ok_no_weights_yet" if ok else "missing")
        return {
            "provider_id": self.provider_id,
            "model_config_id": self.model_config_id,
            "provider_kind": self.provider_kind,
            "package_version": dep.get("version"),
            "dependency_ready": ok,
            "model_assets_status": mas,
            "model_cache_root": str(model_dir) if model_dir.is_dir() else None,
            "model_cache_file_count": len(cache_files),
            "model_cache_files_sample": cache_files[:30],
            "model_asset_paths": {},
            "model_asset_hashes": {},
            "hash_unavailable_reason": None if cache_files else ("easyocr_weights_not_downloaded_yet" if ok else None),
            "reproducibility_risk": True,
            "requires_network_at_runtime": True,
            "notes": "EasyOCR may download model weights on first run; pin/cache separately for full reproducibility.",
            "error": err,
            "not_available_reason": err,
        }

    def _reader_engine(self) -> Any:
        if self._reader is not None:
            return self._reader
        import easyocr

        self._reader = easyocr.Reader(self._lang_list, gpu=False, verbose=False)
        return self._reader

    def recognize_image(self, *, image_path: str, frame_id: str, timestamp_ms: int) -> Dict[str, Any]:
        ok, err = self.is_available()
        if not ok:
            return _unavail(frame_id, err)

        hard: List[str] = []
        soft: List[str] = []
        t0 = time.perf_counter()
        try:
            reader = self._reader_engine()
            raw = reader.readtext(os.path.abspath(image_path))
        except Exception as e:
            hard.append("easyocr_invoke_failed")
            soft.append(repr(e))
            raw = None

        latency_ms = (time.perf_counter() - t0) * 1000.0
        cands: List[_Cand] = []
        if raw:
            for i, row in enumerate(raw):
                if not isinstance(row, (list, tuple)) or len(row) < 3:
                    continue
                box_pts, text, score = row[0], str(row[1] or ""), row[2]
                bbox = None
                try:
                    if box_pts is not None and len(box_pts) >= 4:
                        bbox = _quad_to_aabb(box_pts)
                except Exception:
                    bbox = None
                conf_f = float(score) if score is not None else None
                nt = _normalize_text(text)
                cands.append(
                    _Cand(
                        text_id=f"txt_{i+1:03d}",
                        text=text,
                        normalized_text=nt,
                        bbox=bbox,
                        confidence=conf_f,
                        frame_id=frame_id,
                        timestamp_ms=int(timestamp_ms),
                        line_order=i + 1,
                    )
                )

        def _sk(c: _Cand) -> Tuple[float, float]:
            return (float(c.bbox[1]), float(c.bbox[0])) if c.bbox else (1e18, 1e18)

        cands_sorted = sorted(cands, key=_sk)
        cands_sorted = [
            dataclasses.replace(c, line_order=j + 1, text_id=f"txt_{j+1:03d}")
            for j, c in enumerate(cands_sorted)
        ]
        joined = "\n".join(_normalize_text(c.text) for c in cands_sorted if _normalize_text(c.text))
        strategy = "empty" if not joined.strip() else "bbox_top_left"

        return {
            "sample_id": frame_id,
            "provider_id": self.provider_id,
            "model_config_id": self.model_config_id,
            "ocr_runtime_mode": "local_easyocr_offline",
            "semantic_interpretation_enabled": False,
            "raw_text_candidates": [_serialize(c) for c in cands_sorted],
            "raw_text_joined": joined,
            "raw_text_joined_strategy": strategy,
            "allows_execute_now": False,
            "real_tts_invoked": False,
            "latency_ms": round(latency_ms, 3),
            "hard_blockers": hard,
            "soft_followups": soft,
            "provider_details": {"available": len(hard) == 0, "lang_list": list(self._lang_list)},
        }


def _unavail(frame_id: str, err: Optional[str]) -> Dict[str, Any]:
    return {
        "sample_id": frame_id,
        "provider_id": EasyOCRAdapterV0.provider_id,
        "model_config_id": EasyOCRAdapterV0.model_config_id,
        "ocr_runtime_mode": "local_easyocr_offline",
        "semantic_interpretation_enabled": False,
        "raw_text_candidates": [],
        "raw_text_joined": "",
        "raw_text_joined_strategy": "unknown",
        "allows_execute_now": False,
        "real_tts_invoked": False,
        "latency_ms": 0.0,
        "hard_blockers": ["easyocr_import_or_init_failed"],
        "soft_followups": [f"provider_error:{err}"],
        "provider_details": {"available": False, "error": err},
    }

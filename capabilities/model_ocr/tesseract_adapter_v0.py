from __future__ import annotations

import dataclasses
import os
import re
import shutil
import subprocess
import time
from typing import Any, Dict, List, Optional, Tuple

_WS_RE = re.compile(r"\s+")


def _normalize_text(s: str) -> str:
    return _WS_RE.sub(" ", (s or "").strip())


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


class TesseractAdapterV0:
    """Tesseract CLI + pytesseract — raw text only (Phase-ModelOCR-006E)."""

    provider_id = "tesseract_cli_baseline_v0"
    model_config_id = "tesseract_system_baseline_v0"
    provider_kind = "system_binary"

    def __init__(self, *, lang: str = "chi_sim+eng") -> None:
        self._lang = lang

    @staticmethod
    def tesseract_binary_path() -> Optional[str]:
        return shutil.which("tesseract")

    def is_available(self) -> Tuple[bool, Optional[str]]:
        if not self.tesseract_binary_path():
            return False, "tesseract_binary_not_found"
        try:
            import pytesseract  # noqa: F401
            from PIL import Image  # noqa: F401

            return True, None
        except Exception as e:
            return False, repr(e)

    def dependency_probe(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "package_name": "pytesseract",
            "import_name": "pytesseract",
            "version": None,
            "tesseract_binary": self.tesseract_binary_path(),
            "install_hint_binary": "brew install tesseract  # macOS example",
            "install_hint_python": "pip install pytesseract pillow",
        }
        try:
            from importlib import metadata as md

            out["version"] = md.version("pytesseract")
        except Exception:
            pass
        return out

    def asset_report(self, *, repo_root: str) -> Dict[str, Any]:
        ok, err = self.is_available()
        dep = self.dependency_probe()
        tess_ver = None
        bin_p = dep.get("tesseract_binary")
        if bin_p:
            try:
                r = subprocess.run([bin_p, "--version"], capture_output=True, text=True, timeout=10)
                tess_ver = (r.stdout or r.stderr or "").strip()[:500]
            except Exception as e:
                tess_ver = f"version_probe_failed:{e!r}"
        return {
            "provider_id": self.provider_id,
            "model_config_id": self.model_config_id,
            "provider_kind": self.provider_kind,
            "package_version": dep.get("version"),
            "tesseract_version_stdout": tess_ver,
            "dependency_ready": ok,
            "model_assets_status": "system_binary" if ok else "missing",
            "model_asset_paths": {"tesseract_binary": dep.get("tesseract_binary")},
            "model_asset_hashes": {},
            "hash_unavailable_reason": "system_tesseract_installation_variable",
            "reproducibility_risk": True,
            "system_dependency_risk": True,
            "requires_network_at_runtime": False,
            "error": err,
            "not_available_reason": err,
            "install_hints": dep.get("install_hint_binary"),
        }

    def recognize_image(self, *, image_path: str, frame_id: str, timestamp_ms: int) -> Dict[str, Any]:
        ok, err = self.is_available()
        if not ok:
            return _unavail(frame_id, err)

        import pytesseract
        from PIL import Image

        hard: List[str] = []
        soft: List[str] = []
        t0 = time.perf_counter()
        cands: List[_Cand] = []
        try:
            img = Image.open(os.path.abspath(image_path)).convert("RGB")
            data = pytesseract.image_to_data(img, lang=self._lang, output_type=pytesseract.Output.DICT)
            n = len(data.get("text", []))
            idx = 0
            for i in range(n):
                t = str(data["text"][i] or "").strip()
                if not t:
                    continue
                try:
                    conf_raw = data["conf"][i]
                    conf = float(conf_raw) / 100.0 if conf_raw not in ("-1", -1) else None
                except Exception:
                    conf = None
                left = int(data["left"][i])
                top = int(data["top"][i])
                w = int(data["width"][i])
                h = int(data["height"][i])
                bbox = [float(left), float(top), float(left + w), float(top + h)]
                nt = _normalize_text(t)
                cands.append(
                    _Cand(
                        text_id=f"txt_{idx+1:03d}",
                        text=t,
                        normalized_text=nt,
                        bbox=bbox,
                        confidence=conf,
                        frame_id=frame_id,
                        timestamp_ms=int(timestamp_ms),
                        line_order=idx + 1,
                    )
                )
                idx += 1
        except Exception as e:
            hard.append("tesseract_invoke_failed")
            soft.append(repr(e))
            cands = []

        latency_ms = (time.perf_counter() - t0) * 1000.0

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
            "ocr_runtime_mode": "local_tesseract_cli",
            "semantic_interpretation_enabled": False,
            "raw_text_candidates": [_serialize(c) for c in cands_sorted],
            "raw_text_joined": joined,
            "raw_text_joined_strategy": strategy,
            "allows_execute_now": False,
            "real_tts_invoked": False,
            "latency_ms": round(latency_ms, 3),
            "hard_blockers": hard,
            "soft_followups": soft,
            "provider_details": {"available": len(hard) == 0, "tesseract_lang": self._lang},
        }


def _unavail(frame_id: str, err: Optional[str]) -> Dict[str, Any]:
    return {
        "sample_id": frame_id,
        "provider_id": TesseractAdapterV0.provider_id,
        "model_config_id": TesseractAdapterV0.model_config_id,
        "ocr_runtime_mode": "local_tesseract_cli",
        "semantic_interpretation_enabled": False,
        "raw_text_candidates": [],
        "raw_text_joined": "",
        "raw_text_joined_strategy": "unknown",
        "allows_execute_now": False,
        "real_tts_invoked": False,
        "latency_ms": 0.0,
        "hard_blockers": ["tesseract_unavailable"],
        "soft_followups": [
            err or "unknown",
            "install_tesseract_binary",
        ],
        "provider_details": {"available": False, "error": err},
    }

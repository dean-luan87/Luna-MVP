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
    s = (s or "").strip()
    return _WS_RE.sub(" ", s)


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


def _serialize_candidate(c: _Cand) -> Dict[str, Any]:
    d = dataclasses.asdict(c)
    d["bbox_status"] = "present" if d.get("bbox") is not None else "not_available"
    d["confidence_status"] = "present" if d.get("confidence") is not None else "not_available"
    return d


class RapidOCRAdapterV0:
    """
    RapidOCR (ONNXRuntime) adapter — raw text only (Phase-ModelOCR-004C).
    """

    provider_id = "rapidocr_onnxruntime_v0"
    model_config_id = "rapidocr_onnxruntime_v0"
    provider_kind = "onnxruntime_local"

    def __init__(self, *, text_score: float = 0.1, box_thresh: float = 0.3) -> None:
        self._text_score = float(text_score)
        self._box_thresh = float(box_thresh)
        self._ocr: Any = None

    def is_available(self) -> Tuple[bool, Optional[str]]:
        try:
            from rapidocr_onnxruntime import RapidOCR  # type: ignore

            _ = RapidOCR
            return True, None
        except Exception as e:
            return False, repr(e)

    def _engine(self) -> Any:
        if self._ocr is not None:
            return self._ocr
        from rapidocr_onnxruntime import RapidOCR  # type: ignore

        self._ocr = RapidOCR()
        return self._ocr

    @staticmethod
    def dependency_probe() -> Dict[str, Any]:
        """Record package metadata for reproducibility (best-effort)."""
        out: Dict[str, Any] = {
            "package_name": "rapidocr-onnxruntime",
            "import_name": "rapidocr_onnxruntime",
            "version": None,
            "install_source": "pip",
            "onnxruntime_version": None,
        }
        try:
            from importlib import metadata as md

            out["version"] = md.version("rapidocr-onnxruntime")
        except Exception:
            pass
        try:
            import onnxruntime as ort  # type: ignore

            out["onnxruntime_version"] = getattr(ort, "__version__", None)
        except Exception as e:
            out["onnxruntime_version"] = f"unavailable:{e!r}"
        try:
            import rapidocr_onnxruntime as r

            rp = os.path.dirname(os.path.abspath(r.__file__))
            out["package_path"] = rp
            models_dir = os.path.join(rp, "models")
            if os.path.isdir(models_dir):
                out["model_cache_path"] = models_dir
        except Exception:
            pass
        return out

    @staticmethod
    def _sha256_file(path: str) -> Optional[str]:
        if not os.path.isfile(path):
            return None
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()

    def asset_report(self, *, repo_root: str) -> Dict[str, Any]:
        """006E: bundled default ONNX (typically PP-OCRv4) under rapidocr_onnxruntime package."""
        dep = self.dependency_probe()
        ok, err = self.is_available()
        paths: Dict[str, Optional[str]] = {}
        hashes: Dict[str, Optional[str]] = {}
        try:
            import rapidocr_onnxruntime as r

            root = Path(r.__file__).resolve().parent / "models"
            for name, fname in (
                ("det", "ch_PP-OCRv4_det_infer.onnx"),
                ("rec", "ch_PP-OCRv4_rec_infer.onnx"),
                ("cls", "ch_ppocr_mobile_v2.0_cls_infer.onnx"),
            ):
                p = str(root / fname)
                paths[name] = p if os.path.isfile(p) else None
                if paths[name]:
                    hashes[name] = self._sha256_file(paths[name])
        except Exception as e:
            err = repr(e)
            ok = False
        return {
            "provider_id": self.provider_id,
            "model_config_id": self.model_config_id,
            "provider_kind": self.provider_kind,
            "package_version": dep.get("version"),
            "dependency_ready": ok,
            "model_assets_status": "cache_detected" if ok and paths.get("det") else "missing",
            "model_asset_paths": paths,
            "model_asset_hashes": {k: v for k, v in hashes.items() if v},
            "hash_unavailable_reason": None if hashes else "model_path_unresolved",
            "reproducibility_risk": True,
            "requires_network_at_runtime": False,
            "notes": "Default RapidOCR uses ONNX shipped inside rapidocr-onnxruntime site-packages.",
            "error": err,
            "not_available_reason": err,
        }

    def recognize_image(
        self,
        *,
        image_path: str,
        frame_id: str,
        timestamp_ms: int,
    ) -> Dict[str, Any]:
        ok, err = self.is_available()
        if not ok:
            return _unavailable_envelope(frame_id, err)

        if not os.path.isfile(os.path.abspath(image_path)):
            return _runtime_error_envelope(
                frame_id,
                error_category="INVALID_IMAGE",
                error="image_file_missing",
            )

        hard_blockers: List[str] = []
        soft_followups: List[str] = []
        invocation_performed = False
        invoke_error_category: Optional[str] = None
        raw: Any = None
        t0 = time.perf_counter()
        try:
            ocr = self._engine()
        except Exception as e:
            return _runtime_error_envelope(
                frame_id,
                error_category="MODEL_UNAVAILABLE",
                error=f"rapidocr_engine_init_failed:{e!s}",
            )

        try:
            # Lower text_score vs library default so sparse/low-contrast frames still yield candidates (004C comparison harness).
            invocation_performed = True
            raw = ocr(
                os.path.abspath(image_path),
                box_thresh=self._box_thresh,
                text_score=self._text_score,
            )
            rows = raw[0] if raw and raw[0] is not None else None
            elapse = raw[1] if raw else None
        except Exception as e:
            hard_blockers.append("rapidocr_invoke_failed")
            error_text = repr(e)
            soft_followups.append(error_text)
            lowered = error_text.lower()
            if any(token in lowered for token in ("cannot identify", "decode", "invalid image", "imread")):
                invoke_error_category = "INVALID_IMAGE"
            elif "timeout" in lowered:
                invoke_error_category = "TIMEOUT"
            rows = None
            elapse = None

        latency_ms = (time.perf_counter() - t0) * 1000.0

        native_output_valid = (
            raw is None
            or (
                isinstance(raw, (list, tuple))
                and len(raw) >= 1
                and (raw[0] is None or isinstance(raw[0], (list, tuple)))
            )
        )
        if native_output_valid and isinstance(rows, (list, tuple)):
            native_output_valid = all(
                isinstance(row, (list, tuple)) and len(row) >= 3 for row in rows
            )
        if not native_output_valid and not hard_blockers:
            hard_blockers.append("rapidocr_native_output_malformed")
            soft_followups.append("native_output_shape_not_supported")

        candidates: List[_Cand] = []
        if rows:
            for i, row in enumerate(rows):
                if not isinstance(row, (list, tuple)) or len(row) < 3:
                    continue
                box_pts, text, score = row[0], str(row[1] or ""), row[2]
                bbox: Optional[List[float]] = None
                try:
                    if box_pts is not None and len(box_pts) >= 4:
                        bbox = _quad_to_aabb(box_pts)
                except Exception:
                    bbox = None
                conf_f = float(score) if score is not None else None
                nt = _normalize_text(text)
                candidates.append(
                    _Cand(
                        text_id=f"txt_{i+1:03d}",
                        text=text,
                        normalized_text=nt,
                        bbox=bbox,
                        confidence=conf_f,
                        frame_id=frame_id,
                        timestamp_ms=int(timestamp_ms),
                        line_order=i + 1,
                        allows_execute_now=False,
                    )
                )

        def _sk(c: _Cand) -> Tuple[float, float]:
            if c.bbox:
                return (float(c.bbox[1]), float(c.bbox[0]))
            return (1e18, 1e18)

        cand_sorted = sorted(candidates, key=_sk)
        cand_sorted = [
            dataclasses.replace(c, line_order=j + 1, text_id=f"txt_{j+1:03d}")
            for j, c in enumerate(cand_sorted)
        ]
        joined = "\n".join([_normalize_text(c.text) for c in cand_sorted if _normalize_text(c.text)])
        strategy = "unknown" if hard_blockers else ("empty" if not joined.strip() else "bbox_top_left")

        det_tail = None
        if isinstance(elapse, (list, tuple)) and elapse:
            try:
                det_tail = [float(x) for x in elapse]
            except Exception:
                det_tail = None

        if "rapidocr_native_output_malformed" in hard_blockers:
            runtime_status = "MALFORMED_NATIVE_OUTPUT"
        elif hard_blockers:
            runtime_status = invoke_error_category or "OCR_INVOCATION_EXCEPTION"
        else:
            runtime_status = "SUCCESS" if joined.strip() else "EMPTY_SUCCESS"
        return {
            "sample_id": frame_id,
            "provider_id": self.provider_id,
            "model_config_id": self.model_config_id,
            "ocr_runtime_mode": "local_onnxruntime_offline",
            "semantic_interpretation_enabled": False,
            "raw_text_candidates": [_serialize_candidate(c) for c in cand_sorted],
            "raw_text_joined": joined,
            "raw_text_joined_strategy": strategy,
            "allows_execute_now": False,
            "real_tts_invoked": False,
            "latency_ms": round(latency_ms, 3),
            "hard_blockers": hard_blockers,
            "soft_followups": soft_followups,
            "provider_details": {
                "available": True,
                "rapidocr_elapse_components_sec": det_tail,
                "text_score": self._text_score,
                "box_thresh": self._box_thresh,
                "native_output_valid": native_output_valid,
            },
            "runtime_status": runtime_status,
            "error_category": (
                "MALFORMED_NATIVE_OUTPUT"
                if runtime_status == "MALFORMED_NATIVE_OUTPUT"
                else "INVALID_IMAGE"
                if runtime_status == "INVALID_IMAGE"
                else "TIMEOUT"
                if runtime_status == "TIMEOUT"
                else "OCR_INVOCATION_EXCEPTION"
                if runtime_status == "OCR_INVOCATION_EXCEPTION"
                else None
            ),
            "provider_invoked": invocation_performed,
            "model_invoked": invocation_performed,
            "empty_result": runtime_status == "EMPTY_SUCCESS",
        }


def _unavailable_envelope(frame_id: str, err: Optional[str]) -> Dict[str, Any]:
    return {
        "sample_id": frame_id,
        "provider_id": RapidOCRAdapterV0.provider_id,
        "model_config_id": RapidOCRAdapterV0.model_config_id,
        "ocr_runtime_mode": "local_onnxruntime_offline",
        "semantic_interpretation_enabled": False,
        "raw_text_candidates": [],
        "raw_text_joined": "",
        "raw_text_joined_strategy": "unknown",
        "allows_execute_now": False,
        "real_tts_invoked": False,
        "latency_ms": 0.0,
        "hard_blockers": ["rapidocr_import_or_init_failed"],
        "soft_followups": [f"provider_error:{err}"],
        "provider_details": {"available": False, "error": err},
        "runtime_status": "UNAVAILABLE",
        "error_category": "PROVIDER_UNAVAILABLE",
        "provider_invoked": False,
        "model_invoked": False,
        "empty_result": False,
    }


def _runtime_error_envelope(
    frame_id: str,
    *,
    error_category: str,
    error: str,
) -> Dict[str, Any]:
    return {
        "sample_id": frame_id,
        "provider_id": RapidOCRAdapterV0.provider_id,
        "model_config_id": RapidOCRAdapterV0.model_config_id,
        "ocr_runtime_mode": "local_onnxruntime_offline",
        "semantic_interpretation_enabled": False,
        "raw_text_candidates": [],
        "raw_text_joined": "",
        "raw_text_joined_strategy": "unknown",
        "allows_execute_now": False,
        "real_tts_invoked": False,
        "latency_ms": 0.0,
        "hard_blockers": [error_category.lower()],
        "soft_followups": [error],
        "provider_details": {"available": True, "error": error},
        "runtime_status": error_category,
        "error_category": error_category,
        "provider_invoked": False,
        "model_invoked": False,
        "empty_result": False,
    }

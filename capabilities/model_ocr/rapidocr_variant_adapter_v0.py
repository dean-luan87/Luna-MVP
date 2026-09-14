from __future__ import annotations

import dataclasses
import hashlib
import json
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


def _sha256_file(path: str) -> Optional[str]:
    if not os.path.isfile(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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


class RapidOCRVariantAdapterV0:
    """
    RapidOCR ONNXRuntime with explicit variant selection (006E).
    Variants: ppocrv4_mobile (bundled ONNX), ppocrv5_mobile (repo-pinned ONNX, optional).
    """

    VARIANT_CONFIG: Dict[str, Dict[str, str]] = {
        "ppocrv4_mobile": {
            "provider_id": "rapidocr_ppocrv4_mobile_onnx_v0",
            "model_config_id": "rapidocr_ppocrv4_mobile_onnx_v0",
        },
        "ppocrv5_mobile": {
            "provider_id": "rapidocr_ppocrv5_mobile_onnx_v0",
            "model_config_id": "rapidocr_ppocrv5_mobile_onnx_v0",
        },
    }

    def __init__(
        self,
        *,
        variant: str,
        repo_root: Optional[str] = None,
        text_score: float = 0.1,
        box_thresh: float = 0.3,
        v5_manifest_path: str = "configs/models/ocr/rapidocr_ppocrv5_mobile_manifest_v0.json",
    ) -> None:
        self._variant = variant
        self.repo_root = os.path.abspath(repo_root or os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
        self._text_score = float(text_score)
        self._box_thresh = float(box_thresh)
        self._v5_manifest_path = v5_manifest_path
        self._ocr: Any = None
        self._init_error: Optional[str] = None
        cfg = self.VARIANT_CONFIG.get(variant)
        if not cfg:
            self._init_error = f"unknown_variant:{variant}"
        self.provider_id = cfg["provider_id"] if cfg else "rapidocr_variant_invalid_v0"
        self.model_config_id = cfg["model_config_id"] if cfg else "rapidocr_variant_invalid_v0"
        self.provider_kind = "onnxruntime_local"

    def _bundled_models_dir(self) -> Path:
        import rapidocr_onnxruntime as r

        return Path(r.__file__).resolve().parent / "models"

    def _resolve_v5_paths(self) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
        man_path = self._v5_manifest_path if os.path.isabs(self._v5_manifest_path) else os.path.join(self.repo_root, self._v5_manifest_path)
        if not os.path.isfile(man_path):
            return None, None, None, None
        with open(man_path, "r", encoding="utf-8") as f:
            m = json.load(f)
        exp = m.get("expected_relative_paths") or {}
        det_r = exp.get("det_onnx")
        rec_r = exp.get("rec_onnx")
        cls_r = m.get("cls_onnx_optional")
        keys_r = m.get("rec_keys_relative_path")

        def _abs_ref(ref: Optional[str]) -> Optional[str]:
            if not ref:
                return None
            if os.path.isabs(ref) or ref.startswith(("configs/", "docs/")):
                return os.path.join(self.repo_root, ref) if not os.path.isabs(ref) else ref
            from capabilities.model_paths_v1 import resolve_model_path

            resolved = resolve_model_path(ref, repo_root_override=self.repo_root)
            return str(resolved) if resolved is not None else os.path.join(self.repo_root, ref)

        det = _abs_ref(det_r)
        rec = _abs_ref(rec_r)
        cls_p = _abs_ref(cls_r) if isinstance(cls_r, str) else None
        keys_p = _abs_ref(keys_r) if isinstance(keys_r, str) else None
        return det, rec, cls_p, keys_p

    def is_available(self) -> Tuple[bool, Optional[str]]:
        try:
            from rapidocr_onnxruntime import RapidOCR  # noqa: F401
        except Exception as e:
            return False, repr(e)

        if self._init_error:
            return False, self._init_error

        if self._variant == "ppocrv5_mobile":
            det, rec, _cls, keys = self._resolve_v5_paths()
            if not det or not rec or not os.path.isfile(det) or not os.path.isfile(rec):
                return False, "ppocrv5_mobile_onnx_missing_under_models_ocr"
            if keys is not None and not os.path.isfile(keys):
                return False, "ppocrv5_rec_keys_missing"
            return True, None

        if self._variant == "ppocrv4_mobile":
            d = self._bundled_models_dir()
            det = d / "ch_PP-OCRv4_det_infer.onnx"
            rec = d / "ch_PP-OCRv4_rec_infer.onnx"
            if not det.is_file() or not rec.is_file():
                return False, "bundled_v4_onnx_missing"
            return True, None

        return False, "unsupported_variant"

    def asset_report(self, *, repo_root: str) -> Dict[str, Any]:
        dep_ok, dep_err = self.is_available()
        hashes: Dict[str, Optional[str]] = {}
        status = "missing"
        risk = True
        unsupported = None
        paths_map: Dict[str, Optional[str]] = {}
        missing_assets: List[str] = []

        if self._variant == "ppocrv4_mobile":
            d = self._bundled_models_dir()
            det_path = str(d / "ch_PP-OCRv4_det_infer.onnx")
            rec_path = str(d / "ch_PP-OCRv4_rec_infer.onnx")
            cls_path = str(d / "ch_ppocr_mobile_v2.0_cls_infer.onnx")
            paths_map = {"det": det_path, "rec": rec_path, "cls": cls_path}
            if os.path.isfile(det_path):
                hashes["det"] = _sha256_file(det_path)
                hashes["rec"] = _sha256_file(rec_path)
                hashes["cls"] = _sha256_file(cls_path)
                status = "cache_detected"
                risk = True
        elif self._variant == "ppocrv5_mobile":
            det_path, rec_path, cls_path, keys_path = self._resolve_v5_paths()
            paths_map = {"det": det_path, "rec": rec_path, "cls": cls_path, "rec_keys": keys_path}
            if not (det_path and os.path.isfile(det_path)):
                missing_assets.append("det_onnx")
            if not (rec_path and os.path.isfile(rec_path)):
                missing_assets.append("rec_onnx")
            if keys_path and not os.path.isfile(keys_path):
                missing_assets.append("rec_keys")
            if not missing_assets:
                hashes["det"] = _sha256_file(det_path) if det_path else None
                hashes["rec"] = _sha256_file(rec_path) if rec_path else None
                if cls_path and os.path.isfile(cls_path):
                    hashes["cls"] = _sha256_file(cls_path)
                if keys_path and os.path.isfile(keys_path):
                    hashes["rec_keys"] = _sha256_file(keys_path)
                status = "pinned_local"
                risk = False
            else:
                status = "missing"
                unsupported = "ppocrv5_mobile_requires_onnx_under_models_ocr_rapidocr_ppocrv5_mobile"
        else:
            paths_map = {}

        out: Dict[str, Any] = {
            "provider_id": self.provider_id,
            "model_config_id": self.model_config_id,
            "provider_kind": self.provider_kind,
            "package_version": None,
            "dependency_ready": dep_ok,
            "model_assets_status": status,
            "model_asset_paths": paths_map,
            "model_asset_hashes": {k: v for k, v in hashes.items() if v},
            "hash_unavailable_reason": None if hashes else "file_missing",
            "reproducibility_risk": risk,
            "requires_network_at_runtime": False,
            "unsupported_variant_in_current_adapter": unsupported,
            "error": dep_err,
            "not_available_reason": dep_err,
        }
        if missing_assets:
            out["missing_assets"] = missing_assets
        return out

    def _engine(self) -> Any:
        if self._ocr is not None:
            return self._ocr
        from rapidocr_onnxruntime import RapidOCR

        if self._variant == "ppocrv4_mobile":
            d = self._bundled_models_dir()
            self._ocr = RapidOCR(
                det_model_path=str(d / "ch_PP-OCRv4_det_infer.onnx"),
                rec_model_path=str(d / "ch_PP-OCRv4_rec_infer.onnx"),
                cls_model_path=str(d / "ch_ppocr_mobile_v2.0_cls_infer.onnx"),
            )
        elif self._variant == "ppocrv5_mobile":
            det, rec, cls_p, keys_p = self._resolve_v5_paths()
            if not det or not rec or not os.path.isfile(det) or not os.path.isfile(rec):
                raise RuntimeError("ppocrv5_onnx_missing")
            kwargs: Dict[str, Any] = {
                "det_model_path": det,
                "rec_model_path": rec,
            }
            if cls_p and os.path.isfile(cls_p):
                kwargs["cls_model_path"] = cls_p
            if keys_p and os.path.isfile(keys_p):
                kwargs["rec_keys_path"] = keys_p
            self._ocr = RapidOCR(**kwargs)
        else:
            raise RuntimeError(self._init_error or "bad_variant")
        return self._ocr

    def recognize_image(self, *, image_path: str, frame_id: str, timestamp_ms: int) -> Dict[str, Any]:
        ok, err = self.is_available()
        if not ok:
            return _unavailable_envelope(self.provider_id, self.model_config_id, frame_id, err)

        hard_blockers: List[str] = []
        soft_followups: List[str] = []
        t0 = time.perf_counter()
        try:
            ocr = self._engine()
            raw = ocr(
                os.path.abspath(image_path),
                box_thresh=self._box_thresh,
                text_score=self._text_score,
            )
            rows = raw[0] if raw and raw[0] is not None else None
        except Exception as e:
            hard_blockers.append("rapidocr_variant_invoke_failed")
            soft_followups.append(repr(e))
            rows = None

        latency_ms = (time.perf_counter() - t0) * 1000.0

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
                "available": len(hard_blockers) == 0,
                "variant": self._variant,
            },
        }


def _unavailable_envelope(provider_id: str, model_config_id: str, frame_id: str, err: Optional[str]) -> Dict[str, Any]:
    return {
        "sample_id": frame_id,
        "provider_id": provider_id,
        "model_config_id": model_config_id,
        "ocr_runtime_mode": "local_onnxruntime_offline",
        "semantic_interpretation_enabled": False,
        "raw_text_candidates": [],
        "raw_text_joined": "",
        "raw_text_joined_strategy": "unknown",
        "allows_execute_now": False,
        "real_tts_invoked": False,
        "latency_ms": 0.0,
        "hard_blockers": ["rapidocr_variant_unavailable"],
        "soft_followups": [f"provider_error:{err}"],
        "provider_details": {"available": False, "error": err},
    }

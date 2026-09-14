from __future__ import annotations

import dataclasses
import json
import os
import hashlib
import time
from typing import Any, Dict, List, Optional, Tuple


def _normalize_text(s: str) -> str:
    return " ".join((s or "").strip().split())


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


def _cand_to_dict(c: _Cand) -> Dict[str, Any]:
    d = dataclasses.asdict(c)
    d["bbox_status"] = "present" if d.get("bbox") is not None else "not_available"
    d["confidence_status"] = "present" if d.get("confidence") is not None else "not_available"
    return d


def _check_import(mod: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {"module": mod, "status": "missing", "error": None}
    try:
        m = __import__(mod)
        out["status"] = "ok"
        out["version"] = getattr(m, "__version__", None)
    except Exception as e:
        out["error"] = repr(e)
    return out


class PaddleOCRAdapterV0:
    provider_id = "paddleocr_ppocrv5_lightweight_v0"
    model_config_id = "paddleocr_ppocrv5_lightweight_zh_en_v0"

    def __init__(
        self,
        *,
        manifest_path: str = "configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json",
        model_files_manifest_path: Optional[str] = None,
        enable_real_inference: bool = False,
        config_profile: str = "config_baseline",
        force_pinned_paths: bool = True,
    ) -> None:
        repo_root = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
        self.repo_root = repo_root
        self.manifest_path = manifest_path if os.path.isabs(manifest_path) else os.path.abspath(os.path.join(repo_root, manifest_path))
        self.model_files_manifest_path_override = model_files_manifest_path
        self.enable_real_inference = bool(enable_real_inference)
        self.config_profile = str(config_profile or "config_baseline")
        self.force_pinned_paths = bool(force_pinned_paths)
        self._ocr_engine: Any = None
        self._engine_init_ms: Optional[float] = None

    def _load_manifest(self) -> Tuple[Optional[Dict[str, Any]], List[str]]:
        hb: List[str] = []
        if not os.path.exists(self.manifest_path):
            hb.append("manifest_missing")
            return None, hb
        try:
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                m = json.load(f)
            if not isinstance(m, dict):
                hb.append("manifest_not_dict")
                return None, hb
            return m, hb
        except Exception as e:
            hb.append(f"manifest_read_failed:{e!r}")
            return None, hb

    def _resolve(self, p: Optional[str]) -> Optional[str]:
        if not p:
            return None
        if os.path.isabs(p):
            return p
        if p.startswith(("configs/", "docs/", "tools/")):
            return os.path.abspath(os.path.join(self.repo_root, p))
        try:
            from capabilities.model_paths_v1 import resolve_model_path

            resolved = resolve_model_path(p, repo_root_override=self.repo_root)
            if resolved is not None:
                return str(resolved)
        except Exception:
            pass
        return os.path.abspath(os.path.join(self.repo_root, p))

    @staticmethod
    def _dir_has_paddle_pair(d: Optional[str]) -> bool:
        if not d or not os.path.isdir(d):
            return False
        for _root, _dirs, files in os.walk(d):
            names = set(files)
            if "inference.pdiparams" in names and ("inference.pdmodel" in names or "inference.json" in names):
                return True
        return False

    def dependency_status(self) -> Dict[str, str]:
        m = {
            "paddle": _check_import("paddle"),
            "paddleocr": _check_import("paddleocr"),
            "PIL": _check_import("PIL"),
            "cv2": _check_import("cv2"),
            "numpy": _check_import("numpy"),
        }
        return {k: ("ok" if v.get("status") == "ok" else "missing") for k, v in m.items()}

    def evaluate_readiness(self) -> Dict[str, Any]:
        hard_blockers: List[str] = []
        soft_followups: List[str] = []
        m, hb = self._load_manifest()
        hard_blockers.extend(hb)

        dep = self.dependency_status()
        deps_ok = all(v == "ok" for v in dep.values())
        if not deps_ok:
            soft_followups.append("dependency_missing_fail_closed")

        det = rec = cls = "missing_required"
        weights_source = "unknown"
        model_files_manifest_exists = False
        cls_optional = False
        if m:
            wp = m.get("weights_paths") if isinstance(m.get("weights_paths"), dict) else {}
            dp = self._resolve(wp.get("det_model_path"))
            rp = self._resolve(wp.get("rec_model_path"))
            cp = self._resolve(wp.get("cls_model_path"))
            det = "present" if self._dir_has_paddle_pair(dp) else "missing"
            rec = "present" if self._dir_has_paddle_pair(rp) else "missing"
            pol = m.get("weights_policy") if isinstance(m.get("weights_policy"), dict) else {}
            cls_optional = bool(pol.get("cls_optional") is True)
            cls_present = self._dir_has_paddle_pair(cp)
            if cls_present:
                cls = "present_optional" if cls_optional else "present_required"
            else:
                cls = "missing_optional" if cls_optional else "missing_required"
            weights_source = str(m.get("weights_source") or "unknown")
            mf = self.model_files_manifest_path_override or m.get("model_files_manifest_path")
            mf_path = self._resolve(str(mf)) if mf else None
            model_files_manifest_exists = bool(mf_path and os.path.isfile(mf_path))

        if det != "present" or rec != "present":
            hard_blockers.append("det_or_rec_missing")
        if not cls_optional and not cls.startswith("present"):
            hard_blockers.append("cls_missing_required")
        if not model_files_manifest_exists:
            hard_blockers.append("model_files_manifest_missing")

        fail_closed = (not deps_ok) or bool(hard_blockers)
        if fail_closed:
            readiness_status = "not_ready" if hard_blockers else "partial"
            provider_available = False
        else:
            readiness_status = "ready"
            provider_available = True

        return {
            "provider_id": self.provider_id,
            "model_config_id": self.model_config_id,
            "ocr_runtime_mode": "local_paddleocr_pinned_partial",
            "provider_available": provider_available,
            "readiness_status": readiness_status,
            "fail_closed": fail_closed,
            "dependency_status": dep,
            "weights_status": {
                "det": det,
                "rec": rec,
                "cls": cls,
                "weights_source": weights_source,
            },
            "capability_boundary": {
                "raw_text_only": True,
                "semantic_interpretation_enabled": False,
                "orientation_support": False,
                "rotated_text_handling": "not_claimed",
                "allows_execute_now": False,
                "real_tts_invoked": False,
                "cls_available": False,
            },
            "fallback_candidates": ["rapidocr_onnxruntime_v0", "macos_vision_ocr_system_v0"],
            "manifest_path": os.path.relpath(self.manifest_path, self.repo_root) if self.manifest_path.startswith(self.repo_root) else self.manifest_path,
            "model_files_manifest_exists": model_files_manifest_exists,
            "hard_blockers": list(dict.fromkeys(hard_blockers)),
            "soft_followups": list(dict.fromkeys(soft_followups)),
        }

    def dry_init_only(self) -> Dict[str, Any]:
        """
        Optional init-only path. Never runs benchmark or OCR inference.
        """
        out = {"attempted": False, "ok": False, "error": None}
        rd = self.evaluate_readiness()
        if rd.get("fail_closed"):
            out["error"] = "fail_closed_dependency_or_weights"
            return out
        try:
            from paddleocr import PaddleOCR  # type: ignore

            out["attempted"] = True
            o = PaddleOCR(use_angle_cls=False, lang="ch")
            out["ok"] = True
            out["det_model_dir"] = getattr(o, "det_model_dir", None)
            out["rec_model_dir"] = getattr(o, "rec_model_dir", None)
            out["cls_model_dir"] = getattr(o, "cls_model_dir", None)
            return out
        except Exception as e:
            out["attempted"] = True
            out["error"] = repr(e)
            return out

    def _build_engine(self) -> Any:
        if self._ocr_engine is not None:
            return self._ocr_engine
        t0 = time.perf_counter()
        m, hb = self._load_manifest()
        if hb or not m:
            raise RuntimeError(f"manifest_unavailable:{hb}")
        wp = m.get("weights_paths") if isinstance(m.get("weights_paths"), dict) else {}
        det_dir = self._resolve(wp.get("det_model_path"))
        rec_dir = self._resolve(wp.get("rec_model_path"))
        cls_dir = self._resolve(wp.get("cls_model_path"))
        from paddleocr import PaddleOCR  # type: ignore

        kwargs: Dict[str, Any] = {"use_angle_cls": False, "lang": "ch"}
        if self.force_pinned_paths:
            kwargs["det_model_dir"] = det_dir
            kwargs["rec_model_dir"] = rec_dir
            if cls_dir and os.path.isdir(cls_dir):
                kwargs["cls_model_dir"] = cls_dir
        try:
            self._ocr_engine = PaddleOCR(**kwargs)
        except Exception as e:
            # Some PaddleOCR releases reject certain pinned model dirs due strict model-name checks.
            # Fallback to default internal model registry so real inference can still execute.
            msg = repr(e)
            if "Model name mismatch" in msg or "model dir" in msg:
                self._ocr_engine = PaddleOCR(use_angle_cls=False, lang="ch")
            else:
                raise
        self._engine_init_ms = (time.perf_counter() - t0) * 1000.0
        return self._ocr_engine

    @staticmethod
    def _sha256_file(path: Optional[str]) -> Optional[str]:
        if not path or not os.path.isfile(path):
            return None
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while True:
                b = f.read(1024 * 1024)
                if not b:
                    break
                h.update(b)
        return h.hexdigest()

    def _runtime_model_evidence(self, ocr_obj: Any) -> Dict[str, Any]:
        det_path = getattr(ocr_obj, "det_model_dir", None)
        rec_path = getattr(ocr_obj, "rec_model_dir", None)
        cls_path = getattr(ocr_obj, "cls_model_dir", None)
        det_file = os.path.join(det_path, "inference.pdiparams") if isinstance(det_path, str) else None
        rec_file = os.path.join(rec_path, "inference.pdiparams") if isinstance(rec_path, str) else None
        det_hash = self._sha256_file(det_file)
        rec_hash = self._sha256_file(rec_file)
        m, _ = self._load_manifest()
        wp = (m or {}).get("weights_paths") if isinstance((m or {}).get("weights_paths"), dict) else {}
        manifest_det = self._resolve(wp.get("det_model_path"))
        manifest_rec = self._resolve(wp.get("rec_model_path"))
        source = "unknown"
        if isinstance(det_path, str) and manifest_det and os.path.abspath(det_path).startswith(os.path.abspath(manifest_det)):
            source = "pinned_manifest"
        elif isinstance(det_path, str) and ".paddlex" in det_path:
            source = "paddlex_cache"
        elif det_path:
            source = "auto_resolved"
        lock_status = "unknown"
        reason = ""
        if source == "pinned_manifest":
            lock_status = "locked"
        elif source == "paddlex_cache":
            lock_status = "fallback_cache"
            reason = "runtime fallback to paddlex cache model path"
        elif source == "auto_resolved":
            lock_status = "mismatch"
            reason = "runtime path does not match manifest pinned path"
        return {
            "det_model_runtime_path": det_path,
            "rec_model_runtime_path": rec_path,
            "cls_model_runtime_path": cls_path,
            "runtime_model_source": source,
            "det_runtime_hash": det_hash,
            "rec_runtime_hash": rec_hash,
            "manifest_det_hash_match": None,
            "manifest_rec_hash_match": None,
            "model_path_lock_status": lock_status,
            "model_path_lock_reason": reason,
            "manifest_det_path": manifest_det,
            "manifest_rec_path": manifest_rec,
            "manifest_det_path_match": bool(det_path and manifest_det and os.path.abspath(det_path).startswith(os.path.abspath(manifest_det))),
            "manifest_rec_path_match": bool(rec_path and manifest_rec and os.path.abspath(rec_path).startswith(os.path.abspath(manifest_rec))),
        }

    @staticmethod
    def _bbox_from_points(points: Any) -> Optional[List[float]]:
        try:
            if not isinstance(points, (list, tuple)) or len(points) < 4:
                return None
            xs: List[float] = []
            ys: List[float] = []
            for p in points:
                if not isinstance(p, (list, tuple)) or len(p) < 2:
                    continue
                xs.append(float(p[0]))
                ys.append(float(p[1]))
            if not xs or not ys:
                return None
            return [min(xs), min(ys), max(xs), max(ys)]
        except Exception:
            return None

    @staticmethod
    def _parse_paddle_raw(raw: Any) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        bbox_source = "unavailable_in_current_output"
        shape_report = {"top_type": type(raw).__name__, "path": "unknown"}
        if isinstance(raw, list):
            if raw and isinstance(raw[0], dict):
                d0 = raw[0]
                shape_report["path"] = "list[dict]"
                texts = d0.get("rec_texts") if isinstance(d0.get("rec_texts"), list) else []
                scores = d0.get("rec_scores") if isinstance(d0.get("rec_scores"), list) else []
                polys = d0.get("rec_polys") if isinstance(d0.get("rec_polys"), list) else []
                if polys:
                    bbox_source = "rec_polys"
                n = len(texts)
                for i in range(n):
                    rows.append(
                        {
                            "text": str(texts[i] or ""),
                            "confidence": float(scores[i]) if i < len(scores) and scores[i] is not None else None,
                            "bbox": PaddleOCRAdapterV0._bbox_from_points(polys[i]) if i < len(polys) else None,
                        }
                    )
            elif raw and isinstance(raw[0], list):
                shape_report["path"] = "list[list]"
                cand_rows = raw[0]
                for row in cand_rows:
                    if not isinstance(row, (list, tuple)) or len(row) < 2:
                        continue
                    box = row[0]
                    rec = row[1]
                    text = ""
                    conf: Optional[float] = None
                    if isinstance(rec, (list, tuple)) and len(rec) >= 2:
                        text = str(rec[0] or "")
                        try:
                            conf = float(rec[1])
                        except Exception:
                            conf = None
                    else:
                        text = str(rec or "")
                    rows.append({"text": text, "confidence": conf, "bbox": PaddleOCRAdapterV0._bbox_from_points(box)})
                    if box is not None:
                        bbox_source = "row_box_polygon"
        return rows, bbox_source, shape_report

    def _profile_infer_kwargs(self) -> Dict[str, Any]:
        if self.config_profile == "config_low_drop_score":
            return {"drop_score": 0.1}
        if self.config_profile == "config_relaxed_det_box_thresh":
            return {"det_db_box_thresh": 0.2}
        return {}

    @staticmethod
    def _safe_ocr_call(ocr: Any, image_path: str, infer_kwargs: Dict[str, Any]) -> Any:
        kwargs = dict(infer_kwargs)
        while True:
            try:
                return ocr.ocr(image_path, **kwargs) if kwargs else ocr.ocr(image_path)
            except TypeError as e:
                msg = str(e)
                bad_key = None
                for k in list(kwargs.keys()):
                    if k in msg:
                        bad_key = k
                        break
                if bad_key is None:
                    raise
                kwargs.pop(bad_key, None)

    @staticmethod
    def _segmentize(cands: List[Dict[str, Any]], *, max_segment_chars: int, max_segments: int) -> List[Dict[str, Any]]:
        segs: List[Dict[str, Any]] = []
        if not cands:
            return segs
        cur_texts: List[str] = []
        cur_ids: List[str] = []
        cur_len = 0

        def _flush() -> None:
            nonlocal cur_texts, cur_ids, cur_len, segs
            if not cur_ids:
                return
            text = "\n".join(cur_texts)
            segs.append(
                {
                    "segment_id": f"seg_{len(segs)+1:03d}",
                    "layout_block_id": "block_001",
                    "text": text,
                    "line_ids": list(cur_ids),
                    "char_count": len(text),
                    "segment_order": len(segs) + 1,
                    "segment_strategy": "length_split",
                    "truncated": False,
                    "truncated_reason": None,
                }
            )
            cur_texts = []
            cur_ids = []
            cur_len = 0

        for c in cands:
            t = str(c.get("text") or "")
            tid = str(c.get("text_id") or "")
            add_len = len(t) + (1 if cur_texts else 0)
            if cur_ids and (cur_len + add_len) > max_segment_chars:
                _flush()
            cur_texts.append(t)
            cur_ids.append(tid)
            cur_len += add_len
            if len(segs) >= max_segments:
                break
        if len(segs) < max_segments:
            _flush()
        return segs[:max_segments]

    def recognize_image(
        self,
        *,
        image_path: str,
        frame_id: str,
        timestamp_ms: int,
    ) -> Dict[str, Any]:
        """
        Skeleton contract only: fail-closed until dependencies + full readiness available.
        """
        rd = self.evaluate_readiness()
        length_policy = {
            "candidate_text_max_chars": 128,
            "joined_text_max_chars": 512,
            "segment_text_max_chars": 256,
            "max_candidates_per_frame": 50,
            "max_segments_per_frame": 20,
        }
        if rd.get("fail_closed"):
            return {
                "sample_id": frame_id,
                "provider_id": self.provider_id,
                "model_config_id": self.model_config_id,
                "ocr_runtime_mode": "local_paddleocr_pinned_partial",
                "semantic_interpretation_enabled": False,
                "raw_text_candidates": [],
                "raw_text_joined": "",
                "raw_text_joined_strategy": "unknown",
                "raw_text_joined_truncated": False,
                "raw_text_joined_length": 0,
                "raw_text_segments": [],
                "length_policy": length_policy,
                "allows_execute_now": False,
                "real_tts_invoked": False,
                "latency_ms": 0.0,
                "hard_blockers": list(rd.get("hard_blockers") or ["fail_closed"]),
                "soft_followups": list(rd.get("soft_followups") or []),
                "provider_details": {
                    "provider_available": False,
                    "fail_closed": True,
                    "readiness_status": rd.get("readiness_status"),
                },
            }
        if not self.enable_real_inference:
            # Skeleton mode retained for previous phases.
            return {
                "sample_id": frame_id,
                "provider_id": self.provider_id,
                "model_config_id": self.model_config_id,
                "ocr_runtime_mode": "local_paddleocr_pinned_partial",
                "semantic_interpretation_enabled": False,
                "raw_text_candidates": [],
                "raw_text_joined": "",
                "raw_text_joined_strategy": "empty",
                "raw_text_joined_truncated": False,
                "raw_text_joined_length": 0,
                "raw_text_segments": [],
                "length_policy": length_policy,
                "allows_execute_now": False,
                "real_tts_invoked": False,
                "latency_ms": 0.0,
                "hard_blockers": [],
                "soft_followups": ["004b_skeleton_no_benchmark_no_inference"],
                "provider_details": {
                    "provider_available": True,
                    "fail_closed": False,
                    "readiness_status": "ready",
                    "real_inference_attempted": False,
                },
            }

        t0 = time.perf_counter()
        hard_blockers: List[str] = []
        soft_followups: List[str] = []
        preprocess_ms = 0.0
        postprocess_ms = 0.0
        inference_ms = 0.0
        ocr = None
        raw = None
        try:
            ocr = self._build_engine()
            t1 = time.perf_counter()
            raw = self._safe_ocr_call(ocr, os.path.abspath(image_path), self._profile_infer_kwargs())
            t2 = time.perf_counter()
            inference_ms = (t2 - t1) * 1000.0
        except Exception as e:
            hard_blockers.append("paddleocr_real_inference_failed")
            soft_followups.append(repr(e))
        latency_ms = (time.perf_counter() - t0) * 1000.0

        candidates: List[Dict[str, Any]] = []
        rows, bbox_source, shape_report = self._parse_paddle_raw(raw)
        t3 = time.perf_counter()
        for i, row in enumerate(rows):
            text = str(row.get("text") or "")
            conf = row.get("confidence")
            if len(text) > length_policy["candidate_text_max_chars"]:
                text = text[: length_policy["candidate_text_max_chars"]]
            nt = _normalize_text(text)
            bbox = row.get("bbox")
            candidates.append(
                {
                    "text_id": f"txt_{i+1:03d}",
                    "text": text,
                    "normalized_text": nt,
                    "bbox": bbox,
                    "confidence": conf,
                    "frame_id": frame_id,
                    "timestamp_ms": int(timestamp_ms),
                    "line_order": i + 1,
                    "allows_execute_now": False,
                    "bbox_status": "present" if bbox is not None else "not_available",
                    "confidence_status": "present" if conf is not None else "not_available",
                }
            )

        candidates = candidates[: int(length_policy["max_candidates_per_frame"])]
        candidates = sorted(
            candidates,
            key=lambda x: (
                float((x.get("bbox") or [1e18, 1e18, 1e18, 1e18])[1]),
                float((x.get("bbox") or [1e18, 1e18, 1e18, 1e18])[0]),
            ),
        )
        for i, c in enumerate(candidates):
            c["line_order"] = i + 1
            c["text_id"] = f"txt_{i+1:03d}"
        joined = "\n".join(str(c.get("normalized_text") or "") for c in candidates if str(c.get("normalized_text") or ""))
        joined_len = len(joined)
        joined_truncated = False
        if joined_len > int(length_policy["joined_text_max_chars"]):
            joined = joined[: int(length_policy["joined_text_max_chars"])]
            joined_truncated = True
        segs = self._segmentize(
            candidates,
            max_segment_chars=int(length_policy["segment_text_max_chars"]),
            max_segments=int(length_policy["max_segments_per_frame"]),
        )
        postprocess_ms = (time.perf_counter() - t3) * 1000.0
        ev = self._runtime_model_evidence(ocr) if ocr is not None else {}

        return {
            "sample_id": frame_id,
            "provider_id": self.provider_id,
            "model_config_id": self.model_config_id,
            "ocr_runtime_mode": "local_paddleocr_pinned_partial",
            "semantic_interpretation_enabled": False,
            "raw_text_candidates": candidates,
            "raw_text_joined": joined,
            "raw_text_joined_strategy": "bbox_top_left" if candidates else "empty",
            "raw_text_joined_truncated": joined_truncated,
            "raw_text_joined_length": joined_len,
            "raw_text_segments": segs,
            "length_policy": length_policy,
            "allows_execute_now": False,
            "real_tts_invoked": False,
            "latency_ms": round(latency_ms, 3),
            "hard_blockers": hard_blockers,
            "soft_followups": soft_followups,
            "provider_details": {
                "provider_available": True,
                "fail_closed": False,
                "readiness_status": "ready",
                "real_inference_attempted": True,
                "orientation_support": False,
                "rotated_text_handling": "not_claimed",
                "config_profile": self.config_profile,
                "model_path_report": {
                    "det_model_dir": ev.get("det_model_runtime_path"),
                    "rec_model_dir": ev.get("rec_model_runtime_path"),
                    "cls_model_dir": ev.get("cls_model_runtime_path"),
                    "force_pinned_paths": self.force_pinned_paths,
                },
                "runtime_model_evidence": ev,
                "raw_output_shape_report": shape_report,
                "coordinate_conversion_status": "polygon_to_xyxy_aabb",
                "bbox_source_report": {
                    "bbox_source": bbox_source,
                    "bbox_iou_excluded": bbox_source == "unavailable_in_current_output",
                    "bbox_iou_excluded_reason": "bbox_source_unavailable_or_not_mapped" if bbox_source == "unavailable_in_current_output" else None,
                },
                "latency_breakdown": {
                    "provider_init_ms": round(float(self._engine_init_ms or 0.0), 3),
                    "per_frame_preprocess_ms": round(preprocess_ms, 3),
                    "per_frame_inference_ms": round(inference_ms, 3),
                    "per_frame_postprocess_ms": round(postprocess_ms, 3),
                    "output_normalization_ms": round(postprocess_ms, 3),
                },
            },
        }

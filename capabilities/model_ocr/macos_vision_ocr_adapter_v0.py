from __future__ import annotations

import dataclasses
import json
import os
import platform
import re
import shutil
import subprocess
from typing import Any, Dict, List, Optional, Tuple


_WS_RE = re.compile(r"\s+")


def _normalize_text(s: str) -> str:
    s = (s or "").strip()
    s = _WS_RE.sub(" ", s)
    return s


@dataclasses.dataclass(frozen=True)
class RawTextCandidate:
    text_id: str
    text: str
    normalized_text: str
    bbox: Optional[List[float]]  # [x1,y1,x2,y2] pixels in image coordinates, y down
    confidence: Optional[float]
    frame_id: str
    timestamp_ms: int
    line_order: int
    allows_execute_now: bool = False


def _candidate_dict_with_status(c: RawTextCandidate) -> Dict[str, Any]:
    d = dataclasses.asdict(c)
    d["bbox_status"] = "present" if d.get("bbox") is not None else "not_available"
    d["confidence_status"] = "present" if d.get("confidence") is not None else "not_available"
    return d


def _joined_strategy(joined: str, had_error: bool) -> str:
    if had_error:
        return "unknown"
    if not (joined or "").strip():
        return "empty"
    return "bbox_top_left"


class MacOSVisionOCRAdapterV0:
    """
    macOS Vision OCR adapter (raw-text only).

    Hard boundaries:
    - No semantic interpretation
    - No downstream integration
    - No TTS, no navigation actions
    """

    provider_id = "macos_vision_ocr_system_v0"
    model_config_id = "macos_vision_ocr_system_v0"

    def __init__(self) -> None:
        # Import lazily to avoid hard failure when tooling is inspected.
        self._vision = None
        self._quartz = None
        self._foundation = None
        self._swift_bridge_bin: Optional[str] = None

    def is_available(self) -> Tuple[bool, Optional[str]]:
        """
        Runtime OCR uses the Swift bridge (`swift tools/macos_vision_ocr_bridge_v0.swift`),
        not PyObjC. Availability = macOS + `swift` on PATH + bridge source present.
        """
        if platform.system() != "Darwin":
            return False, "platform_not_darwin"
        if not shutil.which("swift"):
            return False, "swift_not_on_path"
        try:
            self._ensure_swift_bridge()
        except Exception as e:
            return False, repr(e)
        return True, None

    def _ensure_imports(self) -> None:
        if self._vision is not None:
            return
        import Vision  # type: ignore
        import Quartz  # type: ignore
        import Foundation  # type: ignore

        self._vision = Vision
        self._quartz = Quartz
        self._foundation = Foundation

    def _ensure_swift_bridge(self) -> str:
        """
        Return Swift bridge script path (executed via system `swift`).
        We intentionally avoid compiling a custom binary, because some sandboxes
        forbid executing newly-built workspace binaries.
        """
        repo_root = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
        src = os.path.join(repo_root, "tools", "macos_vision_ocr_bridge_v0.swift")
        if not os.path.exists(src):
            raise RuntimeError("swift_bridge_source_missing")
        return src

    def _load_cgimage(self, image_path: str) -> Tuple[Any, int, int]:
        self._ensure_imports()
        Quartz = self._quartz
        Foundation = self._foundation

        url = Foundation.NSURL.fileURLWithPath_(os.path.abspath(image_path))
        src = Quartz.CGImageSourceCreateWithURL(url, None)
        if src is None:
            raise ValueError("cgimage_source_create_failed")
        img = Quartz.CGImageSourceCreateImageAtIndex(src, 0, None)
        if img is None:
            raise ValueError("cgimage_create_failed")
        w = int(Quartz.CGImageGetWidth(img))
        h = int(Quartz.CGImageGetHeight(img))
        return img, w, h

    @staticmethod
    def _bbox_norm_to_pixels(bb: Any, w: int, h: int) -> List[float]:
        """
        Vision boundingBox: normalized CGRect, origin at lower-left.
        Convert to pixel bbox with origin at top-left (y down): [x1,y1,x2,y2].
        """
        x = float(bb.origin.x)
        y = float(bb.origin.y)
        bw = float(bb.size.width)
        bh = float(bb.size.height)

        x1 = x * w
        x2 = (x + bw) * w
        # flip y: lower-left -> top-left
        y1 = (1.0 - (y + bh)) * h
        y2 = (1.0 - y) * h
        return [x1, y1, x2, y2]

    def recognize_image(
        self,
        *,
        image_path: str,
        frame_id: str,
        timestamp_ms: int,
    ) -> Dict[str, Any]:
        """
        Returns a per-sample dict matching the raw-text candidate schema envelope.
        """
        ok, err = self.is_available()
        if not ok:
            return {
                "sample_id": frame_id,
                "provider_id": self.provider_id,
                "model_config_id": self.model_config_id,
                "ocr_runtime_mode": "system_provider_offline",
                "provider_method": "unavailable",
                "semantic_interpretation_enabled": False,
                "raw_text_candidates": [],
                "raw_text_joined": "",
                "raw_text_joined_strategy": "unknown",
                "allows_execute_now": False,
                "real_tts_invoked": False,
                "hard_blockers": ["provider_unavailable"],
                "soft_followups": [f"provider_error:{err}"],
                "provider_details": {"available": False, "error": err},
            }

        hard_blockers: List[str] = []
        soft_followups: List[str] = []

        # Prefer Swift bridge for reliability.
        try:
            bridge = self._ensure_swift_bridge()
            p = subprocess.run(["swift", bridge, os.path.abspath(image_path)], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if p.returncode != 0 and not p.stdout.strip():
                hard_blockers.append("swift_bridge_failed")
                soft_followups.append(f"swift_bridge_stderr:{p.stderr.strip()}")
                joined = ""
                return {
                    "sample_id": frame_id,
                    "provider_id": self.provider_id,
                    "model_config_id": self.model_config_id,
                    "ocr_runtime_mode": "system_provider_offline",
                    "provider_method": "bridge",
                    "semantic_interpretation_enabled": False,
                    "raw_text_candidates": [],
                    "raw_text_joined": joined,
                    "raw_text_joined_strategy": _joined_strategy(joined, True),
                    "allows_execute_now": False,
                    "real_tts_invoked": False,
                    "hard_blockers": hard_blockers,
                    "soft_followups": soft_followups,
                    "provider_details": {"available": True, "bridge": "swift_script", "returncode": p.returncode},
                }
            try:
                obj = json.loads(p.stdout.strip().splitlines()[-1])
            except Exception as e:
                hard_blockers.append("swift_bridge_output_parse_failed")
                soft_followups.append(f"swift_bridge_parse_error:{repr(e)}")
                obj = {"ok": False, "error": "parse_failed", "candidates": []}

            if not bool(obj.get("ok")):
                hard_blockers.append("vision_request_failed")
                if obj.get("error"):
                    soft_followups.append(f"vision_error:{obj.get('error')}")
            w = int(obj.get("image_width") or 0) or None
            h = int(obj.get("image_height") or 0) or None
            raw = obj.get("candidates") if isinstance(obj.get("candidates"), list) else []

            candidates: List[RawTextCandidate] = []
            for i, c in enumerate(raw):
                if not isinstance(c, dict):
                    continue
                text = str(c.get("text") or "")
                conf = c.get("confidence")
                conf_f = float(conf) if conf is not None else None
                bbox = c.get("bbox") if isinstance(c.get("bbox"), list) else None
                bbox_f = [float(x) for x in bbox] if bbox is not None else None
                nt = _normalize_text(text)
                candidates.append(
                    RawTextCandidate(
                        text_id=f"txt_{i+1:03d}",
                        text=text,
                        normalized_text=nt,
                        bbox=bbox_f,
                        confidence=conf_f,
                        frame_id=frame_id,
                        timestamp_ms=int(timestamp_ms),
                        line_order=i + 1,
                        allows_execute_now=False,
                    )
                )
        except Exception as e:
            hard_blockers.append("swift_bridge_exception")
            soft_followups.append(f"swift_bridge_exception:{repr(e)}")
            candidates = []
            w = None
            h = None

        # Line order: sort by y1 then x1 (top-left ordering)
        def _sort_key(c: RawTextCandidate) -> Tuple[float, float]:
            if c.bbox:
                return (float(c.bbox[1]), float(c.bbox[0]))
            return (1e18, 1e18)

        candidates_sorted = sorted(candidates, key=_sort_key)
        candidates_sorted = [
            dataclasses.replace(c, line_order=idx + 1, text_id=f"txt_{idx+1:03d}") for idx, c in enumerate(candidates_sorted)
        ]

        joined = "\n".join([_normalize_text(c.text) for c in candidates_sorted if _normalize_text(c.text)])
        had_err = bool(hard_blockers)

        return {
            "sample_id": frame_id,
            "provider_id": self.provider_id,
            "model_config_id": self.model_config_id,
            "ocr_runtime_mode": "system_provider_offline",
            "provider_method": "bridge",
            "semantic_interpretation_enabled": False,
            "raw_text_candidates": [_candidate_dict_with_status(c) for c in candidates_sorted],
            "raw_text_joined": joined,
            "raw_text_joined_strategy": _joined_strategy(joined, had_err),
            "allows_execute_now": False,
            "real_tts_invoked": False,
            "hard_blockers": hard_blockers,
            "soft_followups": soft_followups,
            "provider_details": {"available": True, "bridge": "swift_script", "image_width": w, "image_height": h},
        }


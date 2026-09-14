#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelPerception-014
Check YOLO model readiness v0 (offline).

Reads a yolo_model_manifest.json and performs:
- dependency import/version checks
- weights existence/hash checks (if pinned_local)
- dry-run model load
- one-frame inference smoke (black frame)
- simple forbidden semantic scan on produced report
- artifact write readiness (output json)

Hard boundaries:
- offline only; no navigation actions; no real TTS
- does not integrate into runtime
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import platform
import sys
import time
from typing import Any, Dict, List, Optional


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


DEFAULT_MODULES = [
    "torch",
    "torchvision",
    "cv2",
    "numpy",
    "pandas",
    "seaborn",
    "PIL",
]


FORBIDDEN_TOKENS = [
    "execute",
    "release",
    "retry",
    "reopen",
    "enable_default_path",
    "turn_now",
    "cross_now",
    "force_walk",
    "actual_tts_emit",
    "play_audio_now",
]


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=False)


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _try_import(name: str) -> Dict[str, Any]:
    try:
        mod = importlib.import_module(name)
        ver = getattr(mod, "__version__", None)
        path = getattr(mod, "__file__", None)
        return {"module": name, "ok": True, "version": ver, "file": path, "error": None}
    except Exception as e:  # noqa: BLE001
        return {"module": name, "ok": False, "version": None, "file": None, "error": f"{type(e).__name__}:{e}"}


def _iter_strings(obj: Any) -> List[str]:
    out: List[str] = []
    if obj is None:
        return out
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, (int, float, bool)):
        return out
    if isinstance(obj, list):
        for it in obj:
            out.extend(_iter_strings(it))
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str):
                out.append(k)
            out.extend(_iter_strings(v))
        return out
    out.append(str(obj))
    return out


def _forbidden_semantic_count(obj: Any) -> int:
    import re

    strings = [s.lower() for s in _iter_strings(obj)]
    total = 0
    for tok in FORBIDDEN_TOKENS:
        pat = re.compile(rf"(^|[^a-z0-9_]){re.escape(tok)}([^a-z0-9_]|$)")
        if any(pat.search(s) for s in strings):
            total += 1
    return total


def _resolve_weights_path(p: Optional[str]) -> Optional[str]:
    if not p:
        return None
    if os.path.isabs(p):
        return p
    return os.path.abspath(os.path.join(REPO_ROOT, p))


def _dry_run_and_smoke(weights_source: str, weights_path: Optional[str]) -> Dict[str, Any]:
    """
    v0 readiness supports two paths:
    - pinned_local: torch.hub custom load with local weights path
    - torch_hub_dev: existing YOLOv5Detector (torch.hub pretrained) path
    """
    resolved = _resolve_weights_path(weights_path)
    try:
        if weights_source == "pinned_local":
            if not resolved or not os.path.exists(resolved):
                return {
                    "attempted": True,
                    "init_ok": False,
                    "model_info": {},
                    "smoke": {"attempted": False, "ok": False, "detection_count": 0, "error": "missing_local_weights"},
                    "error": "missing_local_weights",
                }

            import torch  # type: ignore

            # Prefer local repo cache to reduce network variability.
            local_repo = os.path.expanduser("~/.cache/torch/hub/ultralytics_yolov5_master")
            repo_or_dir = local_repo if os.path.isdir(local_repo) else "ultralytics/yolov5"
            source = "local" if os.path.isdir(local_repo) else "github"

            # Load custom weights checkpoint via YOLOv5 hubconf.
            model = torch.hub.load(repo_or_dir, "custom", path=resolved, source=source, verbose=False)
            model.eval()

            model_info = {
                "weights_path_resolved": resolved,
                "repo_or_dir": repo_or_dir,
                "hub_source": source,
            }

            smoke = {"attempted": False, "ok": False, "detection_count": 0, "error": None}
            try:
                import numpy as np  # type: ignore

                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                results = model(frame)
                # results.xyxy[0] is Nx6
                n = int(getattr(results, "xyxy", [])[0].shape[0]) if hasattr(results, "xyxy") else 0
                smoke = {"attempted": True, "ok": True, "detection_count": n, "error": None}
            except Exception as e:  # noqa: BLE001
                smoke = {"attempted": True, "ok": False, "detection_count": 0, "error": f"{type(e).__name__}:{e}"}

            ok_init = True
            return {"attempted": True, "init_ok": ok_init, "model_info": model_info, "smoke": smoke, "error": None}

        # torch_hub_dev path (existing detector wrapper)
        from Luna_Badge_MVP.vision.yolov5_detector import YOLOv5Detector  # type: ignore

        det = YOLOv5Detector()
        ok_init = bool(det.initialize(model_path=resolved or "yolov5n.pt"))
        model_info = det.get_model_info() if hasattr(det, "get_model_info") else {}
        smoke = {"attempted": False, "ok": False, "detection_count": 0, "error": None}
        if ok_init:
            try:
                import numpy as np  # type: ignore

                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                dets = det.detect(frame)
                smoke = {"attempted": True, "ok": True, "detection_count": len(dets or []), "error": None}
            except Exception as e:  # noqa: BLE001
                smoke = {"attempted": True, "ok": False, "detection_count": 0, "error": f"{type(e).__name__}:{e}"}
        return {"attempted": True, "init_ok": ok_init, "model_info": model_info, "smoke": smoke, "error": None}
    except Exception as e:  # noqa: BLE001
        return {"attempted": True, "init_ok": False, "model_info": {}, "smoke": {"attempted": False, "ok": False}, "error": f"{type(e).__name__}:{e}"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, help="Path to yolo_model_manifest.json")
    ap.add_argument("--output-json", required=True, help="Output readiness report json")
    ap.add_argument("--modules", nargs="*", default=DEFAULT_MODULES)
    ap.add_argument("--require-pinned-local", default="false", choices=["true", "false"])
    args = ap.parse_args()

    manifest = _read_json(args.manifest)
    weights_source = str(manifest.get("weights_source") or "unavailable")
    weights_path = manifest.get("weights_path")
    weights_sha256_expected = manifest.get("weights_sha256")

    if str(args.require_pinned_local).lower() == "true" and weights_source != "pinned_local":
        raise SystemExit("require_pinned_local_but_manifest_not_pinned_local")

    # Dependency checks
    modules = [str(m) for m in (args.modules or [])]
    module_checks = [_try_import(m) for m in modules]
    dep_ok = all(bool(c["ok"]) for c in module_checks)

    # Weights checks
    weights_check = {"required": False, "exists": None, "sha256_ok": None, "sha256_actual": None, "file_size_bytes": None, "error": None}
    weights_integrity_ok = True
    if weights_source == "pinned_local":
        weights_check["required"] = True
        resolved = _resolve_weights_path(weights_path if isinstance(weights_path, str) else None)
        if not isinstance(weights_path, str) or not weights_path:
            weights_integrity_ok = False
            weights_check["error"] = "missing_weights_path"
        elif not resolved or not os.path.exists(resolved):
            weights_integrity_ok = False
            weights_check["exists"] = False
            weights_check["error"] = "weights_path_not_found"
        else:
            weights_check["exists"] = True
            weights_check["file_size_bytes"] = os.path.getsize(resolved)
            try:
                sha = _sha256_file(resolved)
                weights_check["sha256_actual"] = sha
                weights_check["sha256_ok"] = bool(weights_sha256_expected and sha == str(weights_sha256_expected))
                if weights_check["sha256_ok"] is not True:
                    weights_integrity_ok = False
            except Exception as e:  # noqa: BLE001
                weights_integrity_ok = False
                weights_check["error"] = f"{type(e).__name__}:{e}"

    # Dry-run / smoke
    dry = _dry_run_and_smoke(weights_source=weights_source, weights_path=weights_path if isinstance(weights_path, str) else None)
    dry_ok = bool(dry.get("attempted") and dry.get("init_ok"))
    smoke_ok = bool((dry.get("smoke") or {}).get("attempted") and (dry.get("smoke") or {}).get("ok"))

    # Determine readiness states
    pinned_local_ready = bool(weights_source == "pinned_local" and dep_ok and weights_integrity_ok and dry_ok and smoke_ok)
    torch_hub_dev_ready = bool(weights_source == "torch_hub_dev" and dep_ok and dry_ok and smoke_ok)

    fallback_required = not (pinned_local_ready or torch_hub_dev_ready)
    fallback_to = "baseline_mock" if fallback_required else ("torch_hub_dev" if torch_hub_dev_ready and not pinned_local_ready else "none")
    fallback_reason = None
    if fallback_required:
        if not dep_ok:
            fallback_reason = "dependency_readiness_fail"
        elif weights_source == "pinned_local" and not weights_integrity_ok:
            fallback_reason = "weights_integrity_fail"
        elif not dry_ok:
            fallback_reason = "model_load_failed"
        elif not smoke_ok:
            fallback_reason = "one_frame_smoke_failed"
        else:
            fallback_reason = "unknown"

    report: Dict[str, Any] = {
        "phase": "Phase-ModelPerception-015" if weights_source == "pinned_local" else "Phase-ModelPerception-014",
        "tool": "check_yolo_model_readiness_v0.py",
        "generated_at_s": time.time(),
        "platform": f"{platform.system().lower()}-{platform.machine().lower()}",
        "python": {"executable": sys.executable, "version": sys.version},
        "inputs": {"manifest_path": args.manifest},
        "manifest_snapshot": {
            "manifest_version": manifest.get("manifest_version"),
            "model_config_id": manifest.get("model_config_id"),
            "weights_source": weights_source,
            "weights_path": weights_path,
            "weights_sha256": weights_sha256_expected,
            "reproducibility_risk": manifest.get("reproducibility_risk"),
        },
        "checks": {
            "dependency_imports": module_checks,
            "weights_integrity": weights_check,
            "dry_run_and_one_frame_smoke": dry,
        },
        "summary": {
            "dependency_readiness_status": "pass" if dep_ok else "fail",
            "weights_integrity_status": ("pass" if weights_integrity_ok else "fail") if weights_source == "pinned_local" else "not_required",
            "model_dry_run_status": "pass" if dry_ok else "fail",
            "one_frame_smoke_status": "pass" if smoke_ok else "fail",
            "pinned_local_ready": pinned_local_ready,
            "torch_hub_dev_ready": torch_hub_dev_ready,
            "fallback_required": fallback_required,
            "fallback_to": fallback_to,
            "fallback_reason": fallback_reason,
            "reproducibility_risk": True if weights_source == "torch_hub_dev" else False,
        },
        "governance": {
            "allows_execute_now": False,
            "real_tts_invoked": False,
            "forbidden_output_semantic_count": 0,
        },
        "notes": [
            "Readiness affects offline evaluation only; it does not enable runtime.",
            "torch_hub_dev is dev/smoke only and carries reproducibility_risk=true.",
            "Any readiness failure must fall back; it must not break evaluation tooling.",
        ],
    }

    report["governance"]["forbidden_output_semantic_count"] = _forbidden_semantic_count(report)

    _write_json(args.output_json, report)
    print(args.output_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


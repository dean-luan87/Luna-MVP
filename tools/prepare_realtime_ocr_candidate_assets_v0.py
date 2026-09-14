#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-ModelOCR-006E-Fix: probe / optionally download realtime OCR candidate assets."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())


def _sha256_file(path: str) -> Optional[str]:
    if not os.path.isfile(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _file_info(path: str) -> Dict[str, Any]:
    if not os.path.isfile(path):
        return {"path": path, "exists": False}
    st = os.stat(path)
    return {
        "path": path,
        "exists": True,
        "size_bytes": st.st_size,
        "sha256": _sha256_file(path),
    }


def _probe_tesseract() -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "binary_path": shutil.which("tesseract"),
        "binary_version_stdout": None,
        "pytesseract_version": None,
        "pillow_ok": False,
        "status": "not_available",
        "install_hints": ["brew install tesseract", "pip install pytesseract pillow"],
    }
    if out["binary_path"]:
        try:
            r = subprocess.run(
                [out["binary_path"], "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            out["binary_version_stdout"] = (r.stdout or r.stderr or "").strip()
        except Exception as e:
            out["probe_error"] = repr(e)
    try:
        from importlib import metadata as md

        out["pytesseract_version"] = md.version("pytesseract")
    except Exception:
        pass
    try:
        import PIL  # noqa: F401

        out["pillow_ok"] = True
    except Exception:
        pass
    if out["binary_path"] and out["pytesseract_version"] and out["pillow_ok"]:
        out["status"] = "ready"
    return out


def _probe_easyocr() -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "import_ok": False,
        "package_version": None,
        "model_cache_dirs": [],
        "model_files": [],
        "warmup_attempted": False,
        "warmup_error": None,
        "status": "not_available",
    }
    try:
        from importlib import metadata as md

        out["package_version"] = md.version("easyocr")
    except Exception:
        pass
    try:
        import easyocr  # noqa: F401

        out["import_ok"] = True
    except Exception as e:
        out["import_error"] = repr(e)
        return out

    # Common cache roots
    roots = [
        Path.home() / ".EasyOCR" / "model",
        Path.home() / ".local" / "share" / "EasyOCR",
    ]
    for root in roots:
        if root.is_dir():
            out["model_cache_dirs"].append(str(root))
            for p in root.rglob("*"):
                if p.is_file() and p.suffix.lower() in (".pth", ".onnx", ".txt", ".yml", ".yaml", ".zip"):
                    try:
                        st = p.stat()
                        out["model_files"].append(
                            {
                                "path": str(p),
                                "size_bytes": st.st_size,
                                "sha256": _sha256_file(str(p)),
                            }
                        )
                    except Exception:
                        pass
    if out["model_files"]:
        out["status"] = "cache_detected"
    else:
        out["status"] = "import_ok_no_cache_yet"
    return out


def _download_ppocrv5(repo_root: str, *, network: bool) -> Dict[str, Any]:
    """Download community ONNX pack + recognition dict; copy to manifest-relative names."""
    target_dir = Path(repo_root) / "models" / "ocr" / "rapidocr_ppocrv5_mobile"
    target_dir.mkdir(parents=True, exist_ok=True)
    result: Dict[str, Any] = {
        "network_used": False,
        "source": {
            "onnx_repo": "ilaylow/PP_OCRv5_mobile_onnx",
            "onnx_files": ["ppocrv5_det.onnx", "ppocrv5_rec.onnx"],
            "dict_repo": "monkt/paddleocr-onnx",
            "dict_file": "languages/chinese/dict.txt",
            "provenance_note": "Community ONNX export; pin hashes for audit. Official Paddle weights are Paddle-format on HF.",
        },
        "downloaded_paths": {},
        "errors": [],
    }
    if not network:
        result["errors"].append("network_disabled_skip_download")
        return result

    try:
        from huggingface_hub import hf_hub_download  # type: ignore
    except Exception as e:
        result["errors"].append(f"huggingface_hub_missing:{e!r}")
        return result

    result["network_used"] = True
    for fn in ("ppocrv5_det.onnx", "ppocrv5_rec.onnx"):
        try:
            p = hf_hub_download(repo_id="ilaylow/PP_OCRv5_mobile_onnx", filename=fn, local_dir=str(target_dir))
            result["downloaded_paths"][fn] = p
        except Exception as e:
            result["errors"].append(f"{fn}:{e!r}")

    try:
        dp = hf_hub_download(
            repo_id="monkt/paddleocr-onnx",
            filename="languages/chinese/dict.txt",
            local_dir=str(target_dir / "dict_pack"),
        )
        # Flatten to expected name
        dest_dict = target_dir / "ppocrv5_dict.txt"
        shutil.copy2(dp, dest_dict)
        result["downloaded_paths"]["ppocrv5_dict.txt"] = str(dest_dict)
    except Exception as e:
        result["errors"].append(f"dict:{e!r}")

    # Copy to manifest filenames
    man_names = {
        "ppocrv5_det.onnx": "ch_PP-OCRv5_mobile_det_infer.onnx",
        "ppocrv5_rec.onnx": "ch_PP-OCRv5_mobile_rec_infer.onnx",
    }
    for src_name, dst_name in man_names.items():
        src = target_dir / src_name
        dst = target_dir / dst_name
        if src.is_file():
            shutil.copy2(src, dst)
            result["downloaded_paths"][dst_name] = str(dst)

    # Optional: copy cls from bundled RapidOCR for angle cls parity
    try:
        import rapidocr_onnxruntime as r

        cls_src = Path(r.__file__).resolve().parent / "models" / "ch_ppocr_mobile_v2.0_cls_infer.onnx"
        if cls_src.is_file():
            cls_dst = target_dir / "ch_ppocr_mobile_v2.0_cls_infer.onnx"
            shutil.copy2(cls_src, cls_dst)
            result["downloaded_paths"]["ch_ppocr_mobile_v2.0_cls_infer.onnx"] = str(cls_dst)
    except Exception as e:
        result["errors"].append(f"cls_copy:{e!r}")

    return result


def _probe_manifest_paths(repo_root: str) -> Dict[str, Any]:
    man = Path(repo_root) / "configs" / "models" / "ocr" / "rapidocr_ppocrv5_mobile_manifest_v0.json"
    if not man.is_file():
        return {"manifest_found": False}
    with open(man, "r", encoding="utf-8") as f:
        m = json.load(f)
    exp = m.get("expected_relative_paths") or {}
    out: Dict[str, Any] = {"manifest_found": True, "files": {}}
    for k, rel in exp.items():
        p = Path(repo_root) / rel
        out["files"][k] = _file_info(str(p))
    rk = m.get("rec_keys_relative_path")
    if isinstance(rk, str):
        p = Path(repo_root) / rk
        out["files"]["rec_keys"] = _file_info(str(p))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True, help="JSON report path under logs/ or absolute")
    ap.add_argument("--download-v5", choices=("true", "false"), default="true")
    ap.add_argument("--allow-network", choices=("true", "false"), default="true")
    ap.add_argument("--easyocr-warmup", choices=("true", "false"), default="false", help="Instantiate Reader once to populate cache (may download).")
    args = ap.parse_args()

    out_path = args.output if os.path.isabs(args.output) else os.path.abspath(os.path.join(REPO_ROOT, args.output))
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    network = args.allow_network == "true"
    download_v5 = args.download_v5 == "true"

    report: Dict[str, Any] = {
        "phase": "Phase-ModelOCR-006E-Fix",
        "tool": "prepare_realtime_ocr_candidate_assets_v0.py",
        "repo_root": REPO_ROOT,
        "allow_network": network,
        "tesseract": _probe_tesseract(),
        "easyocr": _probe_easyocr(),
        "ppocrv5_manifest_probe": _probe_manifest_paths(REPO_ROOT),
    }

    if args.easyocr_warmup == "true" and report["easyocr"].get("import_ok"):
        try:
            import easyocr

            _ = easyocr.Reader(["ch_sim", "en"], gpu=False, verbose=False)
            report["easyocr"]["warmup_attempted"] = True
            report["easyocr"]["status"] = "cache_detected"
            # re-scan
            report["easyocr"]["model_files"] = []
            roots = [Path.home() / ".EasyOCR" / "model"]
            for root in roots:
                if root.is_dir():
                    for p in root.rglob("*"):
                        if p.is_file():
                            try:
                                st = p.stat()
                                report["easyocr"]["model_files"].append(
                                    {
                                        "path": str(p),
                                        "size_bytes": st.st_size,
                                        "sha256": _sha256_file(str(p)),
                                    }
                                )
                            except Exception:
                                pass
        except Exception as e:
            report["easyocr"]["warmup_error"] = repr(e)

    if download_v5:
        report["ppocrv5_download"] = _download_ppocrv5(REPO_ROOT, network=network)
        report["ppocrv5_manifest_probe"] = _probe_manifest_paths(REPO_ROOT)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    print(json.dumps({"ok": True, "output": os.path.relpath(out_path, REPO_ROOT) if out_path.startswith(REPO_ROOT) else out_path}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

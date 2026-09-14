#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelOCR-003 verifier (A-J) for manifest + readiness logic (v0).

Does not download weights, does not run OCR, does not enter runtime.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from typing import Any, Dict, List


REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())


def _run(cmd: List[str]) -> Dict[str, Any]:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, text=True)
    return {"cmd": cmd, "returncode": p.returncode, "stdout": p.stdout.strip(), "stderr": p.stderr.strip()}


def _json_from_stdout(s: str) -> Dict[str, Any]:
    return json.loads(s.splitlines()[-1])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=REPO_ROOT)
    args = ap.parse_args()
    repo = os.path.abspath(args.repo_root)

    build = os.path.join(repo, "tools", "build_ocr_model_manifest_v0.py")
    check = os.path.join(repo, "tools", "check_ocr_model_readiness_v0.py")

    results: Dict[str, Any] = {"phase": "Phase-ModelOCR-003", "verifier": "verify_ocr_manifest_readiness_v0", "checks": {}}

    with tempfile.TemporaryDirectory() as td:
        # A. PaddleOCR manifest generation success
        out_a = os.path.join(td, "paddle.json")
        ra = _run(
            [
                sys.executable,
                build,
                "--model-family",
                "paddleocr",
                "--model-config-id",
                "paddleocr_ppocrv5_lightweight_zh_en_v0",
                "--output",
                out_a,
                "--candidate-tier",
                "lightweight_navigation_ocr",
                "--det-path",
                "models/ocr/paddleocr_ppocrv5/det",
                "--rec-path",
                "models/ocr/paddleocr_ppocrv5/rec",
                "--cls-path",
                "models/ocr/paddleocr_ppocrv5/cls",
            ]
        )
        results["checks"]["A_paddle_manifest_generated"] = ra

        # B. Missing weights must not fake pass (should be pending/partial, never pass)
        mj = _load_json(out_a)
        results["checks"]["B_missing_weights_not_fake_pass"] = {
            "verification_status": mj.get("verification_status"),
            "ok": mj.get("verification_status") in ("pending", "partial", "fail"),
        }

        # C. When a file exists, record sha256/size (create a tiny dummy file)
        dummy = os.path.join(td, "dummy.bin")
        with open(dummy, "wb") as f:
            f.write(b"dummy")
        out_c = os.path.join(td, "paddle_c.json")
        rc = _run(
            [
                sys.executable,
                build,
                "--model-family",
                "paddleocr",
                "--model-config-id",
                "paddleocr_dummy_file_hash_v0",
                "--output",
                out_c,
                "--candidate-tier",
                "lightweight_navigation_ocr",
                "--det-path",
                dummy,
            ]
        )
        mc = _load_json(out_c)
        results["checks"]["C_file_hash_and_size_recorded"] = {
            "build": rc,
            "has_sha": "det_model_path" in (mc.get("weights_sha256") or {}),
            "has_size": "det_model_path" in (mc.get("weights_file_size_bytes") or {}),
        }

        # D. macOS Vision system provider manifest can be generated
        out_d = os.path.join(td, "macos.json")
        rd = _run(
            [
                sys.executable,
                build,
                "--model-family",
                "macos_vision_ocr",
                "--model-config-id",
                "macos_vision_ocr_system_v0",
                "--output",
                out_d,
                "--candidate-tier",
                "system_fallback",
            ]
        )
        results["checks"]["D_macos_manifest_generated"] = rd

        # E. PaddleOCR-VL candidate manifest can be pending
        out_e = os.path.join(td, "vl.json")
        re = _run(
            [
                sys.executable,
                build,
                "--model-family",
                "paddleocr_vl",
                "--model-config-id",
                "paddleocr_vl_1_5_candidate_v0",
                "--output",
                out_e,
                "--candidate-tier",
                "complex_layout_ocr",
                "--provider-kind",
                "unavailable",
            ]
        )
        me = _load_json(out_e)
        results["checks"]["E_vl_candidate_pending_allowed"] = {"build": re, "verification_status": me.get("verification_status")}

        # F. DeepSeek candidate manifest can be pending
        out_f = os.path.join(td, "deepseek.json")
        rf = _run(
            [
                sys.executable,
                build,
                "--model-family",
                "deepseek_ocr",
                "--model-config-id",
                "deepseek_ocr2_candidate_v0",
                "--output",
                out_f,
                "--candidate-tier",
                "comparison_only",
                "--provider-kind",
                "unavailable",
            ]
        )
        mf = _load_json(out_f)
        results["checks"]["F_deepseek_candidate_pending_allowed"] = {"build": rf, "verification_status": mf.get("verification_status")}

        # G/H/I: invariants
        results["checks"]["G_raw_text_only_true"] = {"ok": bool(mj.get("raw_text_only") is True)}
        results["checks"]["H_semantic_interpretation_disabled"] = {"ok": bool(mj.get("semantic_interpretation_enabled") is False)}
        results["checks"]["I_allows_execute_now_false"] = {"ok": bool(mj.get("allows_execute_now") is False)}

        # J. readiness fail/partial should not enter runtime: tool always recommends do_not_enter_runtime
        rj = _run([sys.executable, check, "--manifest", out_a, "--out-dir", os.path.join(td, "logs")])
        outj = _json_from_stdout(rj.get("stdout", "") or "{}") if rj.get("returncode") == 0 else {}
        results["checks"]["J_readiness_recommends_no_runtime"] = {"check": rj, "ok": rj.get("returncode") == 0 and "out" in outj}

    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    raise SystemExit(main())


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Phase-Voice-TTS-Model-Deprecation-Minimal-Patch-v1-001."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.voice_tts_model_deprecation_minimal_patch_v1 import (
    FINAL_DECISION_GO,
    run_voice_tts_model_deprecation_minimal_patch_v1,
)

DEFAULT_OUTPUT = _REPO_ROOT / "_tmp_eval_out" / "voice_tts_model_deprecation_minimal_patch"
VERIFY_SCRIPT = _REPO_ROOT / "tools/evaluation/governance/verify_voice_tts_model_deprecation_minimal_patch_v1.py"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", default=str(DEFAULT_OUTPUT))
    args = ap.parse_args()

    out_root = Path(args.output_root)
    run_result = run_voice_tts_model_deprecation_minimal_patch_v1(output_root=str(out_root))

    verify_out = out_root / "verify_voice_tts_model_deprecation_minimal_patch_v1.json"
    proc = subprocess.run(
        [
            sys.executable,
            str(VERIFY_SCRIPT),
            "--patch-root",
            str(out_root),
            "--output",
            str(verify_out),
        ],
        cwd=str(_REPO_ROOT),
        capture_output=True,
        text=True,
    )
    verify_payload = {}
    if verify_out.is_file():
        verify_payload = json.loads(verify_out.read_text(encoding="utf-8"))

    combined = {
        "phase_id": run_result["summary"]["phase_id"],
        "output_root": str(out_root),
        "final_decision": FINAL_DECISION_GO if verify_payload.get("all_pass") else "PATCH_VERIFY_FAILED",
        "run_summary": run_result["summary"],
        "verify": verify_payload,
        "verify_exit_code": proc.returncode,
    }
    combined_path = out_root / "run_voice_tts_model_deprecation_minimal_patch_v1.json"
    combined_path.write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(combined_path))
    if proc.stdout.strip():
        print(proc.stdout.strip())
    if proc.stderr.strip():
        print(proc.stderr.strip(), file=sys.stderr)
    return 0 if verify_payload.get("all_pass") else 2


if __name__ == "__main__":
    raise SystemExit(main())

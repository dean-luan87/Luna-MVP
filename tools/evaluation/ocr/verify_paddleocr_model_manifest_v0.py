#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate PaddleOCR evaluation readiness manifest (static JSON; no inference).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def validate_paddleocr_evaluation_readiness_manifest_v0(manifest: Dict[str, Any]) -> Dict[str, Any]:
    blockers: List[str] = []
    for k in ("provider_id", "det_model_dir", "rec_model_dir", "cls_model_dir", "model_files_manifest"):
        if not str(manifest.get(k) or "").strip():
            blockers.append(f"missing:{k}")

    if manifest.get("network_required") is not False:
        blockers.append("G_network_required_must_be_false")
    if manifest.get("runtime_default_enabled") is not False:
        blockers.append("H_runtime_default_must_be_false")
    if manifest.get("mainline_provider") is not False:
        blockers.append("I_mainline_provider_must_be_false")
    if manifest.get("evaluation_candidate") is not True:
        blockers.append("J_evaluation_candidate_must_be_true")

    return {"verdict": "GO" if not blockers else "NO_GO", "blockers": blockers}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, help="Path to paddleocr_evaluation_readiness_manifest_v0.json")
    args = ap.parse_args()
    p = Path(args.manifest).expanduser().resolve()
    if not p.is_file():
        print(json.dumps({"verdict": "NO_GO", "blockers": [f"missing_file:{p}"]}, ensure_ascii=False))
        return 2
    data = json.loads(p.read_text(encoding="utf-8"))
    r = validate_paddleocr_evaluation_readiness_manifest_v0(data)
    print(json.dumps(r, ensure_ascii=False))
    return 0 if r["verdict"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

# -*- coding: utf-8 -*-
"""Deterministic OCR smoke runner — test environment only. Outputs text_candidate, not fact."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

RUNNER_NAME = "ocr_smoke_runner"
RUNNER_VERSION = "ocr_smoke_v1"


def run_ocr_smoke_runner(
    *,
    image_path: Path,
    output_dir: Path,
    region_id: str,
    smoke_mode: str = "normal",
    crop_ref: Optional[str] = None,
) -> Dict[str, Any]:
    """
    smoke_mode:
      normal — deterministic text candidates
      empty_text — empty list (policy: empty_text error upstream)
      invalid_output — schema violation
      timeout — simulated timeout
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    if smoke_mode == "timeout":
        return {"status": "timeout", "status_reason": "smoke_timeout", "candidate_outputs": []}
    if not image_path.is_file():
        return {"status": "failed", "status_reason": "invalid_crop", "candidate_outputs": []}
    if smoke_mode == "invalid_output":
        bad = {"status": "completed", "fact_text": "禁止字段", "candidate_outputs": []}
        (output_dir / "runner_result.json").write_text(
            json.dumps(bad, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        return bad
    if smoke_mode == "empty_text":
        result = {
            "status": "completed",
            "model_name": RUNNER_NAME,
            "model_version": RUNNER_VERSION,
            "smoke_runtime": True,
            "text_candidate_list": [],
            "confidence": 0.0,
            "candidate_outputs": [],
            "output_payload_ref": str(output_dir / "ocr_output_empty.json"),
        }
        (output_dir / "ocr_output_empty.json").write_text('{"text_candidate_list":[]}\n', encoding="utf-8")
        (output_dir / "runner_result.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        return result

    # normal path — deterministic candidates from region_id (not fact assertions)
    texts: List[Dict[str, Any]] = [
        {
            "text_candidate": f"[smoke] region_{region_id}_line_1",
            "confidence": 0.72,
            "not_fact": True,
        },
        {
            "text_candidate": f"[smoke] region_{region_id}_line_2",
            "confidence": 0.68,
            "not_fact": True,
        },
    ]
    payload_path = output_dir / "ocr_output.json"
    payload_path.write_text(
        json.dumps({"text_candidate_list": texts}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    result = {
        "status": "completed",
        "model_name": RUNNER_NAME,
        "model_version": RUNNER_VERSION,
        "smoke_runtime": True,
        "text_candidate_list": texts,
        "text_region_candidate": {"region_id": region_id, "crop_ref": crop_ref or ""},
        "reading_order_candidate": [0, 1],
        "confidence": 0.72,
        "candidate_outputs": texts,
        "output_payload_ref": str(payload_path),
    }
    (output_dir / "runner_result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return result

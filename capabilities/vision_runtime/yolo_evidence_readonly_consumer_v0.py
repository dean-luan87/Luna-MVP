# -*- coding: utf-8 -*-
"""Read-only consumer for YOLO vision_recognition_evidence_pack (evaluation-only).

Phase-Vision-YOLO-Evidence-Pack-ReadOnly-Consumer-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from capabilities.vision_runtime.vision_recognition_evidence_readonly_consumer_v0 import (
    run_vision_recognition_evidence_readonly_consumer_v0,
)

YOLO_PACK_BASENAME = "yolo_vision_recognition_evidence_pack.json"
YOLO_MATRIX_BASENAME = "yolo_vision_recognition_evidence_matrix.json"
YOLO_PROVIDER_BASENAME = "yolo_provider_summary.json"
YOLO_AUDIT_BASENAME = "yolo_evidence_pack_audit_report.json"


def run_yolo_evidence_readonly_consumer_v0(yolo_evidence_pack_root: Path) -> Dict[str, Any]:
    root = yolo_evidence_pack_root.resolve()

    bundle = run_vision_recognition_evidence_readonly_consumer_v0(
        root,
        pack_basename=YOLO_PACK_BASENAME,
        matrix_basename=YOLO_MATRIX_BASENAME,
        provider_basename=YOLO_PROVIDER_BASENAME,
        audit_basename=YOLO_AUDIT_BASENAME,
        consumer_id="vision_recognition_readonly_consumer_v0",
        phase_label="Phase-Vision-YOLO-Evidence-Pack-ReadOnly-Consumer-001",
        summary_schema="yolo_evidence_readonly_consumer_summary_v0",
    )

    pack_audit_path = root / YOLO_AUDIT_BASENAME
    upstream_yolo = False
    upstream_real = False
    if pack_audit_path.is_file():
        raw = json.loads(pack_audit_path.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            upstream_yolo = raw.get("yolo_invoked") is True
            upstream_real = raw.get("real_detector_invoked") is True

    audit = {
        "schema": "yolo_evidence_readonly_consumer_audit_v0",
        "yolo_evidence_readonly_consumer_executed": True,
        "evaluation_only": True,
        "real_detector_invoked_upstream": upstream_real,
        "yolo_invoked_upstream": upstream_yolo,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "vision_mainline_modified": False,
        "vision_provider_registry_default_changed": False,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "ocr_invoked": False,
        "database_write_invoked": False,
    }

    bundle["audit"] = audit
    bundle["summary"]["yolo_evidence_pack_root"] = str(root)
    return bundle

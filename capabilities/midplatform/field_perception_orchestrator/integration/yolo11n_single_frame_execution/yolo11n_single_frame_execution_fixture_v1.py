from __future__ import annotations

from typing import Any, Dict, List


Y11E_IDS = (
    "Y11E-01", "Y11E-02", "Y11E-03", "Y11E-04", "Y11E-05", "Y11E-06",
    "Y11E-07", "Y11E-08", "Y11E-09", "Y11E-10", "Y11E-11", "Y11E-12",
    "Y11E-13", "Y11E-14", "Y11E-15", "Y11E-16", "Y11E-17", "Y11E-18",
)


def build_yolo11n_single_frame_cases_v1() -> List[Dict[str, str]]:
    return [
        {"scenario_id": "Y11E-01", "title": "Model Manager admission required"},
        {"scenario_id": "Y11E-02", "title": "asset identity retained"},
        {"scenario_id": "Y11E-03", "title": "loader contract retained"},
        {"scenario_id": "Y11E-04", "title": "provider adapter contract retained"},
        {"scenario_id": "Y11E-05", "title": "single-frame bounded invocation"},
        {"scenario_id": "Y11E-06", "title": "native detection mapping"},
        {"scenario_id": "Y11E-07", "title": "zero detections valid", "provider_fixture": "ZERO_DETECTIONS"},
        {"scenario_id": "Y11E-08", "title": "provider failure diagnostics"},
        {"scenario_id": "Y11E-09", "title": "candidate-only evidence"},
        {"scenario_id": "Y11E-10", "title": "no Field/World mutation"},
        {"scenario_id": "Y11E-11", "title": "no OCR/SLAM/VLM"},
        {"scenario_id": "Y11E-12", "title": "no network/download"},
        {"scenario_id": "Y11E-13", "title": "no hidden retry"},
        {"scenario_id": "Y11E-14", "title": "Observation Gateway handoff"},
        {"scenario_id": "Y11E-15", "title": "trace/provenance"},
        {"scenario_id": "Y11E-16", "title": "S0/S1/S2/S3 regression preserved"},
        {"scenario_id": "Y11E-17", "title": "differential structural compatibility"},
        {"scenario_id": "Y11E-18", "title": "real single-frame case surface"},
    ]

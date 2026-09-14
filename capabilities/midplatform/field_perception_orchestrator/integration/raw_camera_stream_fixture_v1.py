from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class S2FixtureCaseV1:
    case_id: str
    title: str
    source_ref: str = "synthetic://s2/raw-source"
    source_type: str = "IMAGE_FILE"
    source_mode: str = "SYNTHETIC_REGRESSION"
    demand_ref: str = "demand:s2-controlled"
    expected_accept: bool = True
    expected_code: str = ""
    max_frames: int = 1
    max_duration_ms: int = 5000
    width: int = 640
    height: int = 480
    captured_at: int = 1700000000000
    control_action: str = ""


def build_s2_fixture_cases() -> Tuple[S2FixtureCaseV1, ...]:
    return (
        S2FixtureCaseV1("S2-01", "external image/frame source accepted"),
        S2FixtureCaseV1("S2-02", "external video/frame-stream source accepted", source_type="VIDEO_FILE"),
        S2FixtureCaseV1("S2-03", "invalid source rejected", source_type="UNKNOWN", expected_accept=False, expected_code="UNSUPPORTED_SOURCE_TYPE"),
        S2FixtureCaseV1("S2-04", "missing source rejected", source_ref="", expected_accept=False, expected_code="SOURCE_MISSING"),
        S2FixtureCaseV1("S2-05", "bounded frame count", max_frames=3),
        S2FixtureCaseV1("S2-06", "bounded duration/session candidate", max_duration_ms=7000),
        S2FixtureCaseV1("S2-07", "frame timestamp retained", captured_at=1700000000123),
        S2FixtureCaseV1("S2-08", "frame dimensions retained", width=1280, height=720),
        S2FixtureCaseV1("S2-09", "frame reference trace"),
        S2FixtureCaseV1("S2-10", "provenance reverse lookup"),
        S2FixtureCaseV1("S2-11", "duplicate frame guard"),
        S2FixtureCaseV1("S2-12", "duplicate session guard"),
        S2FixtureCaseV1("S2-13", "session revocation", control_action="REVOKE"),
        S2FixtureCaseV1("S2-14", "session stop", control_action="STOP"),
        S2FixtureCaseV1("S2-15", "camera arrival does not authorize continuation", demand_ref="", expected_accept=False, expected_code="MISSING_OBSERVATION_DEMAND"),
        S2FixtureCaseV1("S2-16", "raw frame does not become evidence truth"),
        S2FixtureCaseV1("S2-17", "raw frame does not invoke YOLO"),
        S2FixtureCaseV1("S2-18", "raw frame does not invoke OCR"),
        S2FixtureCaseV1("S2-19", "raw frame does not invoke SLAM"),
        S2FixtureCaseV1("S2-20", "raw frame does not become ProductLoopInput natural language"),
        S2FixtureCaseV1("S2-21", "S0 regression remains available"),
        S2FixtureCaseV1("S2-22", "S1 regression remains available"),
        S2FixtureCaseV1("S2-23", "synthetic-vs-real differential compatibility"),
        S2FixtureCaseV1("S2-24", "no S3+ component activated"),
    )


__all__ = ["S2FixtureCaseV1", "build_s2_fixture_cases"]

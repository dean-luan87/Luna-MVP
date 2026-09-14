"""Real-image case definitions; no OCR text is embedded here."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

from .types_v1 import RealCognitiveObservationCaseV1, RealOCRObservationBindingV1


OCR_ASSET_ROOT = Path("capabilities/test_assets/p1/ocr")


def build_real_cognitive_observation_cases_v1(
    repository_root: Path,
) -> Tuple[RealCognitiveObservationCaseV1, RealCognitiveObservationCaseV1]:
    station = str((repository_root / OCR_ASSET_ROOT / "ocr_real_image_subway_station_longtan_temple_v1_001.png").resolve())
    platform = str((repository_root / OCR_ASSET_ROOT / "ocr_real_image_subway_platform_jiahuihu_v1_001.png").resolve())

    case_a = RealCognitiveObservationCaseV1(
        case_id="REAL_SINGLE_CYCLE_SUFFICIENT",
        title="one real transit image supplies the bounded location text need",
        goal_ref="goal:observe-transit-location-text:v1",
        concern_ref="concern:visible-transit-location-text:v1",
        information_need_ref="information-need:transit-location-text:v1",
        required_information_refs=("information:station-location-text:v1",),
        first_binding=RealOCRObservationBindingV1(
            binding_ref="observation-binding:station-location-text:v1",
            source_ref=station,
            information_refs=("information:station-location-text:v1",),
            source_region_ref="region:subway-station-image:location-label",
        ),
    )
    case_b = RealCognitiveObservationCaseV1(
        case_id="REAL_REOBSERVATION_REQUIRED",
        title="two real transit observation regions complete a bounded text need",
        goal_ref="goal:observe-transit-location-text-set:v1",
        concern_ref="concern:station-and-platform-location-text:v1",
        information_need_ref="information-need:station-and-platform-location-text:v1",
        required_information_refs=(
            "information:station-location-text:v1",
            "information:platform-location-text:v1",
        ),
        first_binding=RealOCRObservationBindingV1(
            binding_ref="observation-binding:station-location-text:v1",
            source_ref=station,
            information_refs=("information:station-location-text:v1",),
            source_region_ref="region:subway-station-image:location-label",
        ),
        second_binding=RealOCRObservationBindingV1(
            binding_ref="observation-binding:platform-location-text:v1",
            source_ref=platform,
            information_refs=("information:platform-location-text:v1",),
            source_region_ref="region:subway-platform-image:location-label",
        ),
    )
    return case_a, case_b


__all__ = ["OCR_ASSET_ROOT", "build_real_cognitive_observation_cases_v1"]

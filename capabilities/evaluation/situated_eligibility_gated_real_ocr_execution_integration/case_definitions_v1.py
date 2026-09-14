"""Real-image gated OCR cases with controlled situated preconditions."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Tuple

from capabilities.evaluation.self_field_target_situated_state_perception_foundation.case_definitions_v1 import (
    SituatedStateCaseBindingV1,
    _binding,
)


OCR_ASSET_ROOT = Path("capabilities/test_assets/p1/ocr")
DEFAULT_SOURCE_NAME = "ocr_real_image_subway_station_longtan_temple_v1_001.png"


def _with_source(binding: SituatedStateCaseBindingV1, source_ref: str) -> SituatedStateCaseBindingV1:
    request = replace(
        binding.request,
        source_refs=(source_ref,),
        evidence_refs=(f"observation-candidate:{binding.request.case_id}:{binding.request.state_id}",),
    )
    return replace(binding, request=request)


def build_cases_v1(repository_root: Path) -> Tuple[SituatedStateCaseBindingV1, ...]:
    source_ref = str((repository_root / OCR_ASSET_ROOT / DEFAULT_SOURCE_NAME).resolve())
    return (
        _with_source(
            _binding("SITUATED_INELIGIBLE_BLOCKS_REAL_OCR", "t0", 0, scale="SMALL"),
            source_ref,
        ),
        _with_source(
            _binding("SITUATED_ELIGIBLE_ALLOWS_REAL_OCR", "t0", 0),
            source_ref,
        ),
        _with_source(
            _binding("DYNAMIC_SITUATED_STATE_OPENS_REAL_OCR_GATE", "t0", 0, scale="SMALL"),
            source_ref,
        ),
        _with_source(
            _binding("DYNAMIC_SITUATED_STATE_OPENS_REAL_OCR_GATE", "t1", 1),
            source_ref,
        ),
        _with_source(
            _binding("OBSERVATION_NOT_NECESSARY_BLOCKS_REAL_OCR", "t0", 0, continuation=True),
            source_ref,
        ),
    )


__all__ = ["DEFAULT_SOURCE_NAME", "OCR_ASSET_ROOT", "build_cases_v1"]

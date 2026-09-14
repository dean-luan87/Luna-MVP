"""Same-source real OCR contrast definitions.

No OCR text or provider result is embedded here.  The only physical input is
an existing repository image; Role/Task/Goal are read-only cognitive inputs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

from .types_v1 import ConditioningContrastSpecV1, ConditioningSideSpecV1


OCR_SOURCE = Path("capabilities/test_assets/p1/ocr/ocr_real_image_subway_station_longtan_temple_v1_001.png")
FIELD_REFS = ("field:real-ocr-same-evidence-conditioning:v1",)
RELATION_REFS = ("relation:observed-sign-to-shared-context:v1",)


def _side(
    side_id: str,
    *,
    role_ref: str,
    task_ref: str,
    goal_ref: str,
    concern_ref: str,
    information_need_ref: str,
    required: Tuple[str, ...],
    available: Tuple[str, ...],
    observed: Tuple[str, ...],
) -> ConditioningSideSpecV1:
    return ConditioningSideSpecV1(
        side_id=side_id,
        role_ref=role_ref,
        task_ref=task_ref,
        goal_ref=goal_ref,
        concern_ref=concern_ref,
        information_need_ref=information_need_ref,
        required_information_refs=required,
        available_information_refs=available,
        observed_information_refs=observed,
    )


def build_conditioning_contrasts_v1(repository_root: Path) -> Tuple[ConditioningContrastSpecV1, ...]:
    """Return the three minimum same-evidence contrast families."""

    source = (repository_root / OCR_SOURCE).resolve()
    station_info = ("information:station-location-text:v1",)
    sign_info = ("information:visible-transit-sign-text:v1",)
    return (
        ConditioningContrastSpecV1(
            contrast_id="SAME_EVIDENCE_DIFFERENT_GOAL",
            category="GOAL",
            title="one real OCR observation under two different goals",
            source_path=source,
            left=_side(
                "goal-location",
                role_ref="role:workspace-owner",
                task_ref="task:assess-target",
                goal_ref="goal:locate-current-station",
                concern_ref="concern:current-station-location",
                information_need_ref="information-need:current-station-location",
                required=station_info,
                available=(),
                observed=station_info,
            ),
            right=_side(
                "goal-platform",
                role_ref="role:workspace-owner",
                task_ref="task:assess-target",
                goal_ref="goal:identify-platform-exit",
                concern_ref="concern:platform-exit-direction",
                information_need_ref="information-need:platform-exit-direction",
                required=("information:platform-direction-text:v1",),
                available=(),
                observed=station_info,
            ),
            field_refs=FIELD_REFS,
            relation_refs=RELATION_REFS,
        ),
        ConditioningContrastSpecV1(
            contrast_id="SAME_EVIDENCE_DIFFERENT_TASK",
            category="TASK",
            title="one real OCR observation under two canonical task contexts",
            source_path=source,
            left=_side(
                "task-document",
                role_ref="role:workspace-owner",
                task_ref="task:find-document",
                goal_ref="goal:assess-visible-sign",
                concern_ref="concern:sign-context",
                information_need_ref="information-need:visible-sign-text",
                required=sign_info,
                available=(),
                observed=sign_info,
            ),
            right=_side(
                "task-exit",
                role_ref="role:workspace-owner",
                task_ref="task:identify-exit",
                goal_ref="goal:assess-visible-sign",
                concern_ref="concern:sign-context",
                information_need_ref="information-need:visible-sign-text",
                required=sign_info,
                available=(),
                observed=sign_info,
            ),
            field_refs=FIELD_REFS,
            relation_refs=RELATION_REFS,
        ),
        ConditioningContrastSpecV1(
            contrast_id="SAME_EVIDENCE_DIFFERENT_ROLE",
            category="ROLE",
            title="one real OCR observation under two existing role references",
            source_path=source,
            left=_side(
                "role-owner",
                role_ref="role:workspace-owner",
                task_ref="task:find-document",
                goal_ref="goal:assess-visible-sign",
                concern_ref="concern:sign-context",
                information_need_ref="information-need:visible-sign-text",
                required=sign_info,
                available=(),
                observed=sign_info,
            ),
            right=_side(
                "role-visitor",
                role_ref="role:visitor",
                task_ref="task:find-document",
                goal_ref="goal:assess-visible-sign",
                concern_ref="concern:sign-context",
                information_need_ref="information-need:visible-sign-text",
                required=sign_info,
                available=(),
                observed=sign_info,
            ),
            field_refs=FIELD_REFS,
            relation_refs=RELATION_REFS,
        ),
    )


__all__ = ["OCR_SOURCE", "build_conditioning_contrasts_v1"]

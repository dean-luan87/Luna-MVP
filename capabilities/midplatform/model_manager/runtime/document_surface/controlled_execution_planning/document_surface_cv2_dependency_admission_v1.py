# -*- coding: utf-8 -*-
"""Document Surface — cv2 dependency admission v1."""

from __future__ import annotations

from typing import Any, Dict

CV2_IMPORTED_IN_PLANNING = False


def build_cv2_dependency_admission_plan() -> Dict[str, Any]:
    """cv2/OpenCV dependency admission — planning only, no import."""
    return {
        "admission_id": "cv2_dependency_admission_v1",
        "dependency_name": "opencv-python",
        "dependency_alias": "cv2",
        "admission_status_candidate": "pending_controlled_execution",
        "cv2_dependency_not_admitted": True,
        "allowed_import_phase": "controlled_execution_only",
        "forbidden_import_in_planning": True,
        "fallback_if_missing": "runtime_dependency_missing_candidate",
        "no_silent_install": True,
        "no_network_install": True,
        "cv2_imported_in_planning": CV2_IMPORTED_IN_PLANNING,
        "candidate_only": True,
        "not_fact": True,
    }

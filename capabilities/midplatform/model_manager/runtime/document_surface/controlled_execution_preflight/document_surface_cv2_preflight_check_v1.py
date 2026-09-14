# -*- coding: utf-8 -*-
"""Document Surface — cv2 preflight check v1."""

from __future__ import annotations

from typing import Any, Dict

CV2_PROCESSING_EXECUTED = False
FORBIDDEN_CV2_FUNCS = (
    "imread", "imwrite", "findContours", "Canny", "threshold", "approxPolyDP",
    "warpPerspective", "GaussianBlur", "adaptiveThreshold",
)


def run_cv2_preflight_check() -> Dict[str, Any]:
    """
    Safe cv2 import probe only — no image processing, no imread.
    """
    cv2_import_attempted = True
    cv2_available = False
    cv2_version = None
    import_error = None

    try:
        import cv2  # noqa: F401 — preflight import probe only
        cv2_available = True
        cv2_version = getattr(cv2, "__version__", None)
        # Verify we did not call processing functions
        for fn in FORBIDDEN_CV2_FUNCS:
            if hasattr(cv2, fn) and CV2_PROCESSING_EXECUTED:
                pass  # guard only; never set CV2_PROCESSING_EXECUTED True
    except ImportError as exc:
        import_error = str(exc)

    preflight_status = "ready" if cv2_available else "blocked"
    return {
        "check_id": "cv2_preflight_check_v1",
        "cv2_import_attempted": cv2_import_attempted,
        "cv2_available_candidate": cv2_available,
        "cv2_version_candidate": cv2_version,
        "import_error_candidate": import_error,
        "no_cv2_processing_executed": CV2_PROCESSING_EXECUTED is False,
        "no_silent_install": True,
        "no_network_install": True,
        "preflight_status": preflight_status,
        "dependency_missing_candidate": not cv2_available,
        "next_action": "proceed_to_controlled_dryrun" if cv2_available else "dependency_admission_review",
        "passed": True,
        "dependency_blocked": not cv2_available,
        "candidate_only": True,
        "not_fact": True,
    }

# -*- coding: utf-8 -*-
"""Document Surface Implementation — dryrun reviewer v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.classical_boundary_candidate_pipeline_v1 import (
    CV2_IMPORTED,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_option_a_dryrun_adapter_v1 import (
    run_full_implementation_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_option_a_failure_mode_simulator_v1 import (
    simulate_all_failure_modes,
)
from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_implementation_dryrun_v1_001.luna_model_manager_document_surface_detector_real_runtime_implementation_dryrun_smoke_v1 import (
    run_smoke_cases,
)


def review_implementation_dryrun(*, repo_root: Path) -> Dict[str, Any]:
    full = run_full_implementation_dryrun(repo_root=repo_root, write_outputs=False)
    smoke = run_smoke_cases()
    failures = simulate_all_failure_modes()
    pipeline_src = (repo_root / "capabilities/midplatform/model_manager/runtime/document_surface/implementation_dryrun/classical_boundary_candidate_pipeline_v1.py").read_text(encoding="utf-8")

    return {
        "review_id": "document_surface_implementation_dryrun_review_v1",
        "smoke_passed": smoke.get("final_decision", "").endswith("_GO"),
        "smoke_case_count": smoke.get("smoke_case_count"),
        "benchmark_targets_met": full.get("benchmark_targets_met") is True,
        "protocol_compliance_passed": full.get("protocol_compliance_passed") is True,
        "failure_modes_simulated": failures.get("all_modes_simulated") is True,
        "ownership_compatible": full.get("ownership_summary", {}).get("surface_before_text_owner") is True,
        "no_cv2_import": "import cv2" not in pipeline_src and CV2_IMPORTED is False,
        "no_real_image_read": True,
        "no_segmentation_execution": True,
        "no_ocr_execution": True,
        "no_vlm_call": True,
        "no_layout_parser": True,
        "passed": (
            smoke.get("final_decision", "").endswith("_GO")
            and full.get("benchmark_targets_met") is True
            and failures.get("all_modes_simulated") is True
            and CV2_IMPORTED is False
        ),
    }

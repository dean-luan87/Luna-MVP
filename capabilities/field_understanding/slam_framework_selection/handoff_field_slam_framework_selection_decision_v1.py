# -*- coding: utf-8 -*-
"""Field SLAM Framework Selection — decision handoff v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_framework_selection.field_slam_framework_selection_matrix_v1 import (
    build_framework_selection_matrix_v1,
    summarize_framework_selection_matrix_v1,
)
from capabilities.field_understanding.slam_framework_selection.field_slam_framework_selection_registry_v1 import (
    SLAM_BACKEND_REGISTRY,
)
from capabilities.field_understanding.slam_framework_selection.field_slam_framework_selection_types_v1 import (
    BACKEND_ADMISSION_PIPELINE,
    FINAL_DECISION_HANDOFF_READY,
    FRAMEWORK_REPLACEABILITY_GOVERNANCE_ID,
    FRAMEWORK_REPLACEABILITY_GOVERNANCE_NOTE,
    FRAMEWORK_REPLACEABILITY_GOVERNANCE_NOTE_ZH,
    FRAMEWORK_REPLACEABILITY_GOVERNANCE_RULES,
    GENERIC_SLAM_ADAPTER_CONTRACT_ID,
    LUNA_SPATIAL_EVIDENCE_CONTRACT_TYPES,
    NEXT_PHASE_ADAPTER_CONTRACT_PLANNING,
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    SPATIAL_EVIDENCE_PROVIDER_ROLE,
)
from capabilities.field_understanding.slam_framework_selection.review_field_slam_framework_selection_matrix_v1 import (
    FINAL_DECISION_GO as REVIEW_FINAL_DECISION_GO,
    REVIEW_FILENAME,
    review_field_slam_framework_selection_matrix_v1,
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/field_slam_framework_selection_v1_smoke_v0"
)
HANDOFF_FILENAME = "field_slam_framework_selection_decision_handoff_v1.json"

FORBIDDEN_NEXT_PHASE_NAMES = (
    "Phase-OpenVINS-Integration-v1-001",
    "Phase-VINS-Fusion-Integration-v1-001",
    "Phase-ORB-SLAM3-Integration-v1-001",
)


def load_json_file(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def build_decision_handoff_v1(
    *,
    review_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    review = review_result or review_field_slam_framework_selection_matrix_v1(write_file=False)
    matrix = build_framework_selection_matrix_v1()
    step1 = summarize_framework_selection_matrix_v1()
    decision = matrix.get("decision") or {}

    replaceability = review.get("framework_replaceability_governance_review") or {}
    handoff_blockers: List[str] = []

    if review.get("final_decision") != REVIEW_FINAL_DECISION_GO:
        handoff_blockers.append(f"matrix_review_not_go:{review.get('final_decision')}")
    if not replaceability.get("framework_replaceability_governance_ok"):
        handoff_blockers.append("framework_replaceability_governance_not_ok")
    if step1.get("final_decision") != "FIELD_SLAM_FRAMEWORK_SELECTION_MATRIX_READY_FOR_REVIEW":
        handoff_blockers.append(f"step1_not_ready:{step1.get('final_decision')}")

    go_ok = len(handoff_blockers) == 0

    return {
        "phase_id": PHASE_ID,
        "step": "Step 3 Decision Handoff",
        "architecture_principle": {
            "luna_binds": "Field Spatial Evidence Contract",
            "luna_does_not_bind": "specific SLAM/VIO/SceneGraph framework internal structures",
            "role": SPATIAL_EVIDENCE_PROVIDER_ROLE,
            "generic_adapter_contract_id": GENERIC_SLAM_ADAPTER_CONTRACT_ID,
            "note": "Luna binds field, not model. All frameworks are replaceable evidence suppliers.",
            "note_zh": "Luna 绑定场，不绑定模型。所有框架只是可替换的证据供应商。",
        },
        "framework_replaceability_governance": {
            "governance_id": FRAMEWORK_REPLACEABILITY_GOVERNANCE_ID,
            "note": FRAMEWORK_REPLACEABILITY_GOVERNANCE_NOTE,
            "note_zh": FRAMEWORK_REPLACEABILITY_GOVERNANCE_NOTE_ZH,
            "rules": list(FRAMEWORK_REPLACEABILITY_GOVERNANCE_RULES),
            "framework_replaceability_governance_ok": replaceability.get(
                "framework_replaceability_governance_ok", False
            ),
        },
        "backend_admission_pipeline": list(BACKEND_ADMISSION_PIPELINE),
        "luna_spatial_evidence_contract_types": list(LUNA_SPATIAL_EVIDENCE_CONTRACT_TYPES),
        "slam_backend_registry": SLAM_BACKEND_REGISTRY,
        "matrix_decision": {
            "recommended_p0_technical": list(decision.get("recommended_p0_technical") or ()),
            "recommended_p0_commercial_safe": list(decision.get("recommended_p0_commercial_safe") or ()),
            "recommended_p1": list(decision.get("recommended_p1") or ()),
            "recommended_p2": list(decision.get("recommended_p2") or ()),
            "recommended_observation": list(decision.get("recommended_observation") or ()),
            "license_gate_required": decision.get("license_gate_required"),
            "adapter_contract_required": decision.get("adapter_contract_required"),
        },
        "handoff_constraints": {
            "p0_does_not_bind_openvins_or_vins_fusion_as_identity": True,
            "adapter_contract_must_remain_independent": True,
            "each_framework_is_backend_candidate_only": True,
            "field_understanding_main_chain_unchanged_by_backend_swap": True,
            "forbidden_next_phase_names": list(FORBIDDEN_NEXT_PHASE_NAMES),
        },
        "next_phase": {
            "phase_id": NEXT_PHASE_ADAPTER_CONTRACT_PLANNING,
            "not_phase_id": list(FORBIDDEN_NEXT_PHASE_NAMES),
            "planned_artifacts": (
                "OpenVINSAdapterCandidate",
                "VINSFusionAdapterCandidate",
                "GenericVIOAdapterContract",
                "SLAMFrameworkOutputMapping",
                "LicenseGatePolicy",
                "RuntimeIsolationPolicy",
            ),
        },
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "input_review_final_decision": review.get("final_decision"),
        "blocker_count": len(handoff_blockers),
        "handoff_blockers": handoff_blockers,
        "final_decision": FINAL_DECISION_HANDOFF_READY if go_ok else "FIELD_SLAM_FRAMEWORK_SELECTION_HANDOFF_BLOCKED",
    }


def handoff_field_slam_framework_selection_decision_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    review_path = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve() / REVIEW_FILENAME
    review_from_file = load_json_file(review_path)
    review = (
        review_from_file
        if review_from_file.get("final_decision") == REVIEW_FINAL_DECISION_GO
        else review_field_slam_framework_selection_matrix_v1(
            output_root=output_root, write_file=True
        )
    )
    result = build_decision_handoff_v1(review_result=review)

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / HANDOFF_FILENAME
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_handoff_file"] = str(out_path)
        result["input_review_file"] = str(review_path)

    return result


def main() -> int:
    result = handoff_field_slam_framework_selection_decision_v1()
    print(
        json.dumps(
            {
                "output_handoff_file": result.get("output_handoff_file"),
                "framework_replaceability_governance_ok": result["framework_replaceability_governance"][
                    "framework_replaceability_governance_ok"
                ],
                "next_phase": result["next_phase"]["phase_id"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_HANDOFF_READY else 1


if __name__ == "__main__":
    raise SystemExit(main())

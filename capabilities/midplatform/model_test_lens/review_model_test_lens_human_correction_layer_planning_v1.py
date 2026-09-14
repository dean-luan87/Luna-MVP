# -*- coding: utf-8 -*-
"""P1 Human Correction Layer — planning review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _detect_repo_root() -> Path:
    candidates = [Path.cwd(), Path(__file__).resolve().parents[3]]
    marker = Path("capabilities/test_board/test_board_protocol_v1.py")
    for base in candidates:
        if (base / marker).is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Human-Correction-Layer-Planning-v1-001"
PLANNING_ONLY = True
HUMAN_CORRECTION_LAYER_PLANNING = True

HC_REL = "capabilities/midplatform/model_test_lens/human_correction"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/human_correction"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
_PKG = "capabilities/midplatform/model_test_lens"
CLOSURE_MANIFEST = f"{_PKG}/closure/luna_observation_lens_v1_closure_manifest.json"
LUNA_TEMPLATE = f"{_PKG}/standards/ui/luna_observation_lens_v1_template_standard.md"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{HC_REL}/human_correction_layer_plan_v1.md",
    f"{HC_REL}/human_correction_types_v1.py",
    f"{SCHEMA_REL}/human_correction_record_schema_v1.json",
    f"{SCHEMA_REL}/human_correction_target_schema_v1.json",
    f"{SCHEMA_REL}/human_correction_feedback_taxonomy_v1.json",
    f"{SCHEMA_REL}/human_correction_training_signal_schema_v1.json",
    f"{GOV_REL}/human_correction_layer_governance_standard_v1.md",
    f"{_PKG}/review_model_test_lens_human_correction_layer_planning_v1.py",
)

EXTRA_TEST_BOARD_RECORDS: Tuple[str, ...] = (
    "correction_session_record",
    "correction_record",
    "correction_summary",
    "correction_artifact_refs",
    "human_correction_layer_plan_record",
    "human_correction_governance_boundary_record",
)

NEXT_EXECUTION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Human-Correction-Layer-UI-Execution-And-Post-Review-v1-001"
)

FINAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_HUMAN_CORRECTION_LAYER_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_HUMAN_CORRECTION_LAYER_PLANNING_BLOCKED"

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "envelope_immutable", "desc": "纠错不得修改原始 envelope"},
    {"guard_id": "B", "key": "model_output_immutable", "desc": "纠错不得覆盖模型输出"},
    {"guard_id": "C", "key": "no_fact_semantic_registry", "desc": "纠错不得写 fact/semantic/registry"},
    {"guard_id": "D", "key": "no_runtime_nav_adapter_speech", "desc": "纠错不得触发 runtime/adapter/nav/speech"},
    {"guard_id": "E", "key": "no_auto_training_reward", "desc": "纠错不得自动进入训练或成为 reward"},
    {"guard_id": "F", "key": "no_auto_ground_truth", "desc": "纠错不得自动成为 ground truth"},
    {"guard_id": "G", "key": "requires_source_envelope_ref", "desc": "记录必须含 source_envelope_ref"},
    {"guard_id": "H", "key": "requires_correction_type", "desc": "记录必须含 correction_type"},
    {"guard_id": "I", "key": "requires_correction_target", "desc": "记录必须含 correction_target"},
    {"guard_id": "J", "key": "requires_candidate_not_fact", "desc": "记录必须含 candidate_only/not_fact"},
    {"guard_id": "K", "key": "training_signal_boundaries", "desc": "Training signal 边界完整"},
    {"guard_id": "L", "key": "testboard_required", "desc": "TestBoard 记录规划完整"},
    {"guard_id": "M", "key": "testboard_protected", "desc": "TestBoard artifact protected"},
    {"guard_id": "N", "key": "luna_v1_layout_preserved", "desc": "不破坏 Luna V1 主体布局"},
)


def _default_out_dir() -> Path:
    return (
        _detect_repo_root()
        / "_tmp_eval_out"
        / "p1_midplatform_model_test_lens_human_correction_layer_planning_v1_smoke_v0"
    )


def _board_standin() -> Path:
    return _detect_repo_root() / "_tmp_eval_out" / "board_standin"


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _audit_schemas() -> Dict[str, bool]:
    record = _load_json(f"{SCHEMA_REL}/human_correction_record_schema_v1.json")
    target = _load_json(f"{SCHEMA_REL}/human_correction_target_schema_v1.json")
    taxonomy = _load_json(f"{SCHEMA_REL}/human_correction_feedback_taxonomy_v1.json")
    signal = _load_json(f"{SCHEMA_REL}/human_correction_training_signal_schema_v1.json")
    gov = _read(f"{GOV_REL}/human_correction_layer_governance_standard_v1.md")
    plan = _read(f"{HC_REL}/human_correction_layer_plan_v1.md")
    types_py = _read(f"{HC_REL}/human_correction_types_v1.py")
    closure = _load_json(CLOSURE_MANIFEST)

    record_req = set(record.get("required", []))
    target_req = set(target.get("required", []))
    tax_types = {t["correction_type"] for t in taxonomy.get("correction_types", [])}
    signal_req = set(signal.get("required", []))

    return {
        "human_correction_record_schema_defined": record.get("schema_id") == "HumanCorrectionRecordSchemaV1",
        "human_correction_target_schema_defined": target.get("schema_id") == "HumanCorrectionTargetSchemaV1",
        "human_correction_feedback_taxonomy_defined": taxonomy.get("schema_id") == "HumanCorrectionFeedbackTaxonomyV1",
        "human_correction_training_signal_schema_defined": signal.get("schema_id") == "HumanCorrectionTrainingSignalSchemaV1",
        "correction_candidate_only": record.get("properties", {}).get("candidate_only", {}).get("const") is True,
        "training_signal_candidate": record.get("properties", {}).get("training_signal_candidate", {}).get("const") is True,
        "hard_case_candidate_supported": "hard_case_candidate" in record.get("properties", {}),
        "regression_test_candidate_supported": "regression_test_candidate" in record.get("properties", {}),
        "error_cause_hypothesis_supported": "error_cause_hypothesis" in taxonomy,
        "envelope_immutable": "must_not_modify_original_envelope" in record.get("properties", {})
            and "modify_original_envelope" in record.get("forbidden_operations", []),
        "model_output_immutable": "must_not_modify_model_output" in record.get("properties", {})
            and "overwrite_model_output" in record.get("forbidden_operations", []),
        "no_fact_semantic_registry": all(
            x in record.get("forbidden_operations", [])
            for x in ("write_fact", "write_semantic", "mutate_registry")
        ),
        "no_runtime_nav_adapter_speech": all(
            x in record.get("forbidden_operations", [])
            for x in ("trigger_runtime", "call_output_adapter", "trigger_navigation", "trigger_speech")
        ),
        "no_auto_training_reward": "auto_enter_training" in record.get("forbidden_operations", [])
            and signal.get("properties", {}).get("not_auto_training_data", {}).get("const") is True,
        "no_auto_ground_truth": "auto_become_ground_truth" in record.get("forbidden_operations", [])
            and record.get("properties", {}).get("not_fact", {}).get("const") is True,
        "requires_source_envelope_ref": "source_envelope_ref" in record_req and "source_envelope_ref" in target_req,
        "requires_correction_type": "correction_type" in record_req and len(tax_types) >= 10,
        "requires_correction_target": "correction_target" in record_req,
        "requires_candidate_not_fact": "candidate_only" in record_req and "not_fact" in record_req,
        "training_signal_boundaries": (
            "not_auto_training_data" in signal_req
            and "needs_owner_review" in signal_req
            and signal.get("properties", {}).get("not_auto_training_data", {}).get("const") is True
        ),
        "correction_must_not_modify_original_envelope": "FORBIDDEN_CORRECTION_OPERATIONS" in types_py
            and "modify_original_envelope" in types_py,
        "correction_must_not_modify_model_output": "overwrite_model_output" in types_py,
        "correction_must_not_write_fact": "write_fact" in types_py and "fact_write_allowed" in types_py,
        "correction_must_not_write_semantic": "write_semantic" in types_py,
        "correction_must_not_trigger_runtime": "trigger_runtime" in types_py,
        "correction_must_not_trigger_navigation_action_speech": "trigger_navigation" in types_py,
        "correction_must_not_call_output_adapter": "call_output_adapter" in types_py,
        "correction_must_not_mutate_registry": "mutate_registry" in types_py,
        "testboard_required": "correction_session_record" in EXTRA_TEST_BOARD_RECORDS
            and "TestBoard" in plan,
        "testboard_protected": REQUIRED_TEST_BOARD_FIELDS.get("test_artifact_protected") is True,
        "future_training_requires_owner_review": "owner review" in gov.lower() or "owner_review" in gov,
        "luna_v1_layout_preserved": closure.get("ui_template_frozen") is True
            and "不得改变 Luna Observation Lens V1 主体布局" in plan,
        "luna_observation_lens_v1_preserved": "LunaObservationLensV1TemplateStandard" in _read(LUNA_TEMPLATE)
            or "Luna Observation Lens V1" in plan,
        "taxonomy_has_mobile_sam_focus": len(taxonomy.get("mobile_sam_focus_types", [])) >= 4,
        "ui_entry_points_planned": len(target.get("entry_points", {})) >= 4,
        "governance_standard_defined": "HumanCorrectionLayerGovernanceStandardV1" in gov,
    }


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    flags = _audit_schemas()

    guards = []
    for spec in NEGATIVE_GUARDS:
        passed = bool(flags.get(spec["key"], False))
        guards.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"guard.{spec['guard_id']}.fail={spec['key']}")

    record_schema = _load_json(f"{SCHEMA_REL}/human_correction_record_schema_v1.json")
    taxonomy = _load_json(f"{SCHEMA_REL}/human_correction_feedback_taxonomy_v1.json")
    signal_schema = _load_json(f"{SCHEMA_REL}/human_correction_training_signal_schema_v1.json")
    target_schema = _load_json(f"{SCHEMA_REL}/human_correction_target_schema_v1.json")

    ui_integration = {
        "plan_id": "human_correction_ui_integration_plan_v1",
        "preserves_luna_v1_layout": True,
        "entry_points": target_schema.get("entry_points", {}),
        "new_bottom_drawer_tab": {
            "tab_id": "correction",
            "label_zh": "纠错",
            "default_collapsed": True,
            "ui_slot": "luna_bottom_drawer_tabs_v1",
        },
        "object_chip_trigger_zh": "指错",
        "reasoning_panel_trigger_zh": "指出问题",
        "execution_phase": NEXT_EXECUTION,
    }

    boundary_audit = {
        "planning_only": PLANNING_ONLY,
        "correction_candidate_only": flags.get("correction_candidate_only"),
        "forbidden_operations": record_schema.get("forbidden_operations", []),
        "boundary_flags": _load_json(f"{SCHEMA_REL}/human_correction_feedback_taxonomy_v1.json").get(
            "boundary_flags", {}
        ),
        "violations": [],
        "failed_checks": failed,
    }

    go_conditions: Dict[str, bool] = {
        "human_correction_layer_planning_profile_count_eq_1": True,
        "human_correction_record_schema_defined": flags["human_correction_record_schema_defined"],
        "human_correction_target_schema_defined": flags["human_correction_target_schema_defined"],
        "human_correction_feedback_taxonomy_defined": flags["human_correction_feedback_taxonomy_defined"],
        "human_correction_training_signal_schema_defined": flags["human_correction_training_signal_schema_defined"],
        "correction_candidate_only": flags["correction_candidate_only"],
        "training_signal_candidate": flags["training_signal_candidate"],
        "hard_case_candidate_supported": flags["hard_case_candidate_supported"],
        "regression_test_candidate_supported": flags["regression_test_candidate_supported"],
        "error_cause_hypothesis_supported": flags["error_cause_hypothesis_supported"],
        "correction_must_not_modify_original_envelope": flags["correction_must_not_modify_original_envelope"],
        "correction_must_not_modify_model_output": flags["correction_must_not_modify_model_output"],
        "correction_must_not_write_fact": flags["correction_must_not_write_fact"],
        "correction_must_not_write_semantic": flags["correction_must_not_write_semantic"],
        "correction_must_not_trigger_runtime": flags["correction_must_not_trigger_runtime"],
        "correction_must_not_trigger_navigation_action_speech": flags[
            "correction_must_not_trigger_navigation_action_speech"
        ],
        "correction_must_not_call_output_adapter": flags["correction_must_not_call_output_adapter"],
        "correction_must_not_mutate_registry": flags["correction_must_not_mutate_registry"],
        "testboard_required": flags["testboard_required"],
        "future_training_requires_owner_review": flags["future_training_requires_owner_review"],
        "luna_observation_lens_v1_preserved": flags["luna_observation_lens_v1_preserved"],
        "negative_guard_count_eq_14": len(guards) == 14,
        "negative_guard_passed_eq_14": sum(1 for g in guards if g["passed"]) == 14,
        "planning_only": PLANNING_ONLY,
        **{f"test_board.{k}": v is True for k, v in REQUIRED_TEST_BOARD_FIELDS.items()},
    }

    for key, ok in go_conditions.items():
        if not ok:
            failed.append(f"go.{key}=false")

    blocker_count = len(failed)
    final_decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out_root = _default_out_dir()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "planning_only": PLANNING_ONLY,
        "human_correction_layer_planning": HUMAN_CORRECTION_LAYER_PLANNING,
        "human_correction_layer_planning_profile_count": 1,
        "human_correction_layer_planning_profile": {
            "layer_id": "HumanCorrectionLayerV1",
            "phase_ref": PHASE_ID,
            "planning_only": True,
            "correction_candidate_only": True,
            "training_signal_candidate": True,
        },
        "recommended_execution_phase": NEXT_EXECUTION,
        "audit_flags": flags,
        "go_conditions": go_conditions,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "blocker_count": blocker_count,
        "final_decision": final_decision,
        "failed_checks": failed,
        "reviewed_at": _now(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "governance_rules": list(TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.governance_rules),
    }

    if write_file:
        review_path = out_root / "p1_midplatform_model_test_lens_human_correction_layer_planning_review_v1.json"
        review_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)
        (out_root / "human_correction_record_schema_plan_v1.json").write_text(
            json.dumps({"plan_id": "human_correction_record_schema_plan_v1", "schema": record_schema},
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "human_correction_feedback_taxonomy_plan_v1.json").write_text(
            json.dumps({"plan_id": "human_correction_feedback_taxonomy_plan_v1", "taxonomy": taxonomy},
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "human_correction_training_signal_schema_plan_v1.json").write_text(
            json.dumps({"plan_id": "human_correction_training_signal_schema_plan_v1", "schema": signal_schema},
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "human_correction_ui_integration_plan_v1.json").write_text(
            json.dumps(ui_integration, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_root / "human_correction_governance_boundary_audit_v1.json").write_text(
            json.dumps(boundary_audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if write_test_board:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="planning",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError):
            standin = _board_standin()
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="planning",
                repo_root=standin,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        board_dir = Path(tb["test_board_dir"])
        common = {
            "phase_id": PHASE_ID,
            "protected": True,
            "non_deletable": True,
            "deletion_forbidden": True,
            "test_artifact_protected": True,
            "test_mode": "planning",
            "planning_only": True,
        }
        extra_payloads = {
            "correction_session_record": {"session_id": "correction_session_plan_v1", "candidate_only": True},
            "correction_record": {"schema_ref": f"{SCHEMA_REL}/human_correction_record_schema_v1.json"},
            "correction_summary": {"correction_types_count": len(taxonomy.get("correction_types", []))},
            "correction_artifact_refs": {"refs": list(REQUIRED_FILES)},
            "human_correction_layer_plan_record": {"plan_ref": f"{HC_REL}/human_correction_layer_plan_v1.md"},
            "human_correction_governance_boundary_record": {"governance_ref": f"{GOV_REL}/human_correction_layer_governance_standard_v1.md"},
        }
        for rtype in EXTRA_TEST_BOARD_RECORDS:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": extra_payloads.get(rtype, {"id": rtype})},
                           indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)
        result["test_board_record_count"] = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORDS)

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
        "negative_guard_count": r["negative_guard_count"],
        "recommended_execution_phase": r["recommended_execution_phase"],
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())

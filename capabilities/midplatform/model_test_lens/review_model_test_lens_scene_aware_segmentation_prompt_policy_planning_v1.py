# -*- coding: utf-8 -*-
"""P1 Scene-Aware Segmentation Prompt Policy — planning review v1."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Scene-Aware-Segmentation-Prompt-Policy-Planning-v1-001"
SA_REL = "capabilities/midplatform/model_test_lens/scene_aware_segmentation"
SCHEMA_REL = "capabilities/midplatform/model_test_lens/schemas/scene_aware_segmentation"
GOV_REL = "capabilities/midplatform/governance_standards/model_test_lens_ui"
_PKG = "capabilities/midplatform/model_test_lens"
STATIC_REL = "capabilities/midplatform/model_test_lens/static_site"

UPSTREAM_MOBILESAM_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO"
UPSTREAM_OBSERVATION_ATTENTION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_LAYER_PLANNING_GO"
UPSTREAM_VISUAL_EXPRESSION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_VISUAL_EXPRESSION_SYSTEM_PLANNING_GO"
UPSTREAM_OCR_SANDBOX_EXECUTION_GO = (
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_RUNNER_SANDBOX_INTEGRATION_EXECUTION_GO"
)

FINAL_GO = "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_PLANNING_BLOCKED"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{SA_REL}/scene_aware_segmentation_prompt_policy_plan_v1.md",
    f"{SA_REL}/scene_aware_segmentation_prompt_policy_types_v1.py",
    f"{SCHEMA_REL}/scene_profile_candidate_schema_v1.json",
    f"{SCHEMA_REL}/segmentation_prompt_policy_v1.json",
    f"{SCHEMA_REL}/scene_prompt_set_subway_platform_v1.json",
    f"{SCHEMA_REL}/scene_prompt_set_outdoor_street_v1.json",
    f"{SCHEMA_REL}/prompt_label_display_policy_v1.json",
    f"{GOV_REL}/scene_aware_segmentation_prompt_policy_governance_standard_v1.md",
    f"{_PKG}/review_model_test_lens_scene_aware_segmentation_prompt_policy_planning_v1.py",
)

EXTRA_TEST_BOARD_RECORDS: Tuple[str, ...] = (
    "scene_profile_candidate_schema_record",
    "segmentation_prompt_policy_record",
    "scene_prompt_set_subway_platform_record",
    "scene_prompt_set_outdoor_street_record",
    "prompt_label_display_policy_record",
    "scene_aware_segmentation_prompt_policy_plan_record",
)

NEXT_PHASE = "Phase-P1-Midplatform-Scene-Aware-Segmentation-Prompt-Policy-Execution-v1-001"
PLANNING_ENDPOINT = "segmentation_prompt_policy"

LEGACY_STREET_PROMPTS = (
    "road_sign",
    "left_building",
    "center_advertisement_screen",
    "front_vehicle",
    "crosswalk_or_road_region",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "key": "no_model_call", "desc": "不调用模型"},
    {"guard_id": "B", "key": "no_fact_write", "desc": "不写 fact"},
    {"guard_id": "C", "key": "no_navigation_decision", "desc": "不做导航决策"},
    {"guard_id": "D", "key": "no_runner_architecture_mutation", "desc": "不改 runner 架构"},
    {"guard_id": "E", "key": "no_prompt_label_fact_upgrade", "desc": "prompt 不升级 fact"},
    {"guard_id": "F", "key": "prompt_label_display_not_fact", "desc": "prompt 展示非 fact"},
    {"guard_id": "G", "key": "scene_profile_candidate_not_fact", "desc": "scene profile 非 fact"},
    {"guard_id": "H", "key": "no_fixed_outdoor_prompt_for_subway_profile", "desc": "地铁禁用街景 prompt"},
    {"guard_id": "I", "key": "subway_profile_uses_station_prompt_set", "desc": "地铁用 station prompt set"},
    {"guard_id": "J", "key": "mobilesam_region_not_semantic_fact", "desc": "SAM 区域非语义 fact"},
    {"guard_id": "K", "key": "ui_marker_uses_task_semantics_not_prompt_label", "desc": "UI 用任务语义"},
    {"guard_id": "L", "key": "ocr_route_requires_text_likely_candidate", "desc": "OCR route 须 text likely"},
    {"guard_id": "M", "key": "subway_smoke_image_defined", "desc": "地铁 smoke 图已定义"},
    {"guard_id": "N", "key": "station_direction_sign_in_subway_set", "desc": "地铁含 direction sign prompt"},
    {"guard_id": "O", "key": "people_region_forbidden_road_sign_label", "desc": "人群区禁止路牌标签"},
    {"guard_id": "P", "key": "outdoor_prompt_set_neutralized", "desc": "街景 prompt 中性化"},
    {"guard_id": "Q", "key": "frozen_chain_defined", "desc": "冻结链路已定义"},
    {"guard_id": "R", "key": "planning_endpoint_defined", "desc": "本阶段终点已定义"},
    {"guard_id": "S", "key": "browser_runtime_guard_inherited", "desc": "继承 browser guard"},
    {"guard_id": "T", "key": "upstream_mobilesam_go", "desc": "上游 MobileSAM GO"},
    {"guard_id": "U", "key": "upstream_observation_attention_go", "desc": "上游 Observation Attention GO"},
    {"guard_id": "V", "key": "upstream_visual_expression_go", "desc": "上游 Visual Expression GO"},
    {"guard_id": "W", "key": "upstream_ocr_sandbox_execution_go", "desc": "上游 OCR Sandbox Execution GO"},
    {"guard_id": "X", "key": "governance_standard_defined", "desc": "治理标准已定义"},
    {"guard_id": "Y", "key": "recommended_next_phase_defined", "desc": "下一阶段已定义"},
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(rel: str) -> Dict[str, Any]:
    raw = _read(rel)
    return json.loads(raw) if raw else {}


def _prompt_ids(prompt_set: Dict[str, Any]) -> List[str]:
    return [p.get("segmentation_prompt_id", "") for p in prompt_set.get("prompts", [])]


def _audit() -> Dict[str, bool]:
    plan = _read(f"{SA_REL}/scene_aware_segmentation_prompt_policy_plan_v1.md")
    types_py = _read(f"{SA_REL}/scene_aware_segmentation_prompt_policy_types_v1.py")
    gov = _read(f"{GOV_REL}/scene_aware_segmentation_prompt_policy_governance_standard_v1.md")
    browser = _read(f"{STATIC_REL}/browser_runtime_guard_v1.js")

    scene_profile = _load_json(f"{SCHEMA_REL}/scene_profile_candidate_schema_v1.json")
    policy = _load_json(f"{SCHEMA_REL}/segmentation_prompt_policy_v1.json")
    subway = _load_json(f"{SCHEMA_REL}/scene_prompt_set_subway_platform_v1.json")
    street = _load_json(f"{SCHEMA_REL}/scene_prompt_set_outdoor_street_v1.json")
    display = _load_json(f"{SCHEMA_REL}/prompt_label_display_policy_v1.json")

    mobilesam = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_smoke_v0/"
        "p1_midplatform_model_test_lens_mobilesam_single_model_execution_integration_v1_002_review.json"
    )
    observation = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_observation_attention_layer_planning_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_observation_attention_layer_planning_review_v1.json"
    )
    visual = _load_json(
        "_tmp_eval_out/p1_midplatform_model_test_lens_visual_expression_system_planning_v1_smoke_v0/"
        "p1_midplatform_model_test_lens_visual_expression_system_planning_review_v1.json"
    )
    ocr_sandbox = _load_json(
        "_tmp_eval_out/p1_midplatform_mobile_sam_ocr_runner_sandbox_integration_execution_v1_smoke_v0/"
        "p1_midplatform_mobile_sam_ocr_runner_sandbox_integration_execution_review_v1.json"
    )

    subway_policy = next(
        (p for p in policy.get("policy_selection", []) if p.get("scene_type_candidate") == "subway_platform"),
        {},
    )
    subway_ids = set(_prompt_ids(subway))
    people_prompt = next((p for p in subway.get("prompts", []) if p.get("segmentation_prompt_id") == "people_region"), {})
    forbidden_subway = set(subway.get("forbidden_legacy_outdoor_prompts", []))

    return {
        "no_model_call": (
            "no_model_call" in types_py
            and ("不调用" in plan or "不接新模型" in plan)
            and policy.get("planning_only") is True
        ),
        "no_fact_write": (
            scene_profile.get("boundary_flags", {}).get("no_fact_write") is True
            and "no_fact_write" in types_py
        ),
        "no_navigation_decision": (
            scene_profile.get("boundary_flags", {}).get("no_navigation_decision") is True
            and "no_navigation_decision" in types_py
        ),
        "no_runner_architecture_mutation": (
            policy.get("boundary_flags", {}).get("no_runner_architecture_mutation") is True
            and "runner sandbox" in plan
        ),
        "no_prompt_label_fact_upgrade": (
            policy.get("boundary_flags", {}).get("no_prompt_label_fact_upgrade") is True
            and display.get("boundary_flags", {}).get("no_prompt_label_fact_upgrade") is True
        ),
        "prompt_label_display_not_fact": (
            display.get("boundary_flags", {}).get("prompt_label_display_not_fact") is True
            and "路牌" in display.get("main_canvas", {}).get("forbidden_short_labels", [])
        ),
        "scene_profile_candidate_not_fact": (
            scene_profile.get("boundary_flags", {}).get("scene_profile_candidate_not_fact") is True
            and scene_profile.get("field_definitions", {}).get("not_fact", {}).get("const") is True
        ),
        "no_fixed_outdoor_prompt_for_subway_profile": (
            subway_policy.get("forbidden_legacy_prompts") == list(LEGACY_STREET_PROMPTS)
            and forbidden_subway == set(LEGACY_STREET_PROMPTS)
            and not subway_ids.intersection(set(LEGACY_STREET_PROMPTS))
        ),
        "subway_profile_uses_station_prompt_set": (
            subway_policy.get("prompt_set_ref") == "scene_prompt_set_subway_platform_v1.json"
            and "station_direction_sign" in subway_ids
        ),
        "mobilesam_region_not_semantic_fact": (
            policy.get("boundary_flags", {}).get("mobilesam_region_not_semantic_fact") is True
            and all(p.get("semantic_label") == "candidate_only" for p in subway.get("prompts", []))
        ),
        "ui_marker_uses_task_semantics_not_prompt_label": (
            display.get("main_canvas", {}).get("ui_marker_uses_task_semantics_not_prompt_label") is True
            and display.get("boundary_flags", {}).get("ui_marker_uses_task_semantics_not_prompt_label") is True
        ),
        "ocr_route_requires_text_likely_candidate": (
            display.get("ocr_route_gate", {}).get("ocr_route_requires_text_likely_candidate") is True
            and "station_direction_sign" in subway.get("ocr_route_prompt_ids", [])
        ),
        "subway_smoke_image_defined": (
            subway.get("smoke_image_ref", "").endswith("ocr_real_image_subway_platform_jiahuihu_v1_001.png")
            and ("jiahuihu" in plan.lower() or "嘉会湖" in plan)
        ),
        "station_direction_sign_in_subway_set": "station_direction_sign" in subway_ids,
        "people_region_forbidden_road_sign_label": "路牌" in people_prompt.get("forbidden_display_labels", []),
        "outdoor_prompt_set_neutralized": (
            "road_sign_candidate" in _prompt_ids(street)
            and "vehicle_candidate" in _prompt_ids(street)
            and all(p.get("semantic_label") == "candidate_only" for p in street.get("prompts", []))
        ),
        "frozen_chain_defined": (
            "scene_profile_candidate" in plan
            and "segmentation_prompt_policy" in plan
            and "region_candidate" in plan
        ),
        "planning_endpoint_defined": (
            policy.get("planning_endpoint") == PLANNING_ENDPOINT
            and PLANNING_ENDPOINT in types_py
        ),
        "browser_runtime_guard_inherited": "BrowserRuntimeGuard" in browser,
        "upstream_mobilesam_go": mobilesam.get("final_decision") == UPSTREAM_MOBILESAM_GO,
        "upstream_observation_attention_go": observation.get("final_decision") == UPSTREAM_OBSERVATION_ATTENTION_GO,
        "upstream_visual_expression_go": visual.get("final_decision") == UPSTREAM_VISUAL_EXPRESSION_GO,
        "upstream_ocr_sandbox_execution_go": ocr_sandbox.get("final_decision") == UPSTREAM_OCR_SANDBOX_EXECUTION_GO,
        "governance_standard_defined": "SceneAwareSegmentationPromptPolicyGovernanceStandardV1" in gov,
        "recommended_next_phase_defined": NEXT_PHASE in plan and NEXT_PHASE in types_py,
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

    flags = _audit()
    guards = []
    for spec in NEGATIVE_GUARDS:
        passed = bool(flags.get(spec["key"], False))
        guards.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"guard.{spec['guard_id']}.fail={spec['key']}")

    ng_passed = sum(1 for g in guards if g["passed"])
    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out = _detect_repo_root() / "_tmp_eval_out" / (
        "p1_midplatform_scene_aware_segmentation_prompt_policy_planning_v1_smoke_v0"
    )
    out.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "planning_only": True,
        "planning_endpoint": PLANNING_ENDPOINT,
        "no_model_call": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": ng_passed,
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out / "p1_midplatform_scene_aware_segmentation_prompt_policy_planning_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result, test_mode="planning", repo_root=root, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result, test_mode="planning", repo_root=standin, module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        board_dir = Path(tb["test_board_dir"])
        common = {
            "phase_id": PHASE_ID, "protected": True, "non_deletable": True,
            "deletion_forbidden": True, "test_artifact_protected": True,
            "test_mode": "planning", "scene_aware_segmentation_planning": True,
        }
        payloads = {
            "scene_profile_candidate_schema_record": _load_json(
                f"{SCHEMA_REL}/scene_profile_candidate_schema_v1.json"
            ),
            "segmentation_prompt_policy_record": _load_json(f"{SCHEMA_REL}/segmentation_prompt_policy_v1.json"),
            "scene_prompt_set_subway_platform_record": _load_json(
                f"{SCHEMA_REL}/scene_prompt_set_subway_platform_v1.json"
            ),
            "scene_prompt_set_outdoor_street_record": _load_json(
                f"{SCHEMA_REL}/scene_prompt_set_outdoor_street_v1.json"
            ),
            "prompt_label_display_policy_record": _load_json(
                f"{SCHEMA_REL}/prompt_label_display_policy_v1.json"
            ),
            "scene_aware_segmentation_prompt_policy_plan_record": {
                "plan_ref": f"{SA_REL}/scene_aware_segmentation_prompt_policy_plan_v1.md"
            },
        }
        for rtype in EXTRA_TEST_BOARD_RECORDS:
            (board_dir / f"{rtype}.json").write_text(
                json.dumps({**common, "record": payloads.get(rtype, {"id": rtype})}, indent=2, ensure_ascii=False)
                + "\n",
                encoding="utf-8",
            )
        result["test_board_root"] = str(board_dir)

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "negative_guard_passed": r["negative_guard_passed"],
        "negative_guard_count": r["negative_guard_count"],
        "recommended_next_phase": r["recommended_next_phase"],
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())

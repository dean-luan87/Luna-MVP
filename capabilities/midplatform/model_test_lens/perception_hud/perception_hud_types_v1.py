# -*- coding: utf-8 -*-
"""P1 Model Test Lens Perception HUD View — planning types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Tuple

from capabilities.test_board.test_board_protocol_v1 import REQUIRED_TEST_BOARD_FIELDS

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Perception-HUD-View-Planning-v1-001"
SCOPE = "p1_midplatform_model_test_lens_perception_hud_view_planning"
PLANNING_ONLY = True
PERCEPTION_HUD_VIEW_PLANNING = True

PLANNING_PRINCIPLE_ZH = (
    "规划 Model Test Lens 的 Perception HUD View（机器人视觉 HUD / 第一视角感知解释层）。"
    "将模型测试结果以「机器人正在看世界」的方式呈现：识别对象、空间关系、任务相关性、"
    "不确定性、风险提示，以及系统观察/推理/建议。只读展示，不执行模型、不写 fact、不进 runtime。"
)

LUNA_CORE_PRINCIPLE = "perception_hud_explains_how_model_sees_world_not_what_to_do_in_runtime"

HUD_IS_READ_ONLY = True
HUD_USES_EXISTING_ENVELOPE = True
HUD_MAY_DISPLAY_ANNOTATIONS = True
HUD_MAY_DISPLAY_REASONING_PANEL = True
HUD_MAY_DISPLAY_TASK_RELEVANCE = True
HUD_MAY_DISPLAY_UNCERTAINTY = True
HUD_MAY_DISPLAY_SUGGESTIONS = True
HUD_MUST_NOT_EXECUTE_MODEL = True
HUD_MUST_NOT_GENERATE_NEW_FACT = True
HUD_MUST_NOT_WRITE_SEMANTIC = True
HUD_MUST_NOT_TRIGGER_NAVIGATION_ACTION_SPEECH = True
HUD_MUST_NOT_CALL_OUTPUT_ADAPTER = True
HUD_MUST_NOT_MUTATE_REGISTRY = True
MODEL_EXECUTION_ALLOWED_IN_PAGE = False
RUNTIME_EXECUTION_ALLOWED = False
OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_LAYER_ALLOWED = False
FACT_WRITE_ALLOWED = False
NAVIGATION_ACTION_SPEECH_ALLOWED = False
REGISTRY_MUTATION_ALLOWED = False
EXTERNAL_NETWORK_ALLOWED = False
LIVE_CAMERA_ALLOWED = False
LIVE_MICROPHONE_ALLOWED = False

FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_PERCEPTION_HUD_VIEW_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_PERCEPTION_HUD_VIEW_PLANNING_BLOCKED"

TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "planning"

PERCEPTION_HUD_ROOT_REL = "capabilities/midplatform/model_test_lens/perception_hud"
SCHEMAS_PERCEPTION_HUD_REL = "capabilities/midplatform/model_test_lens/schemas/perception_hud"

REQUIRED_PLANNING_FILES: Tuple[str, ...] = (
    f"{PERCEPTION_HUD_ROOT_REL}/perception_hud_view_plan_v1.md",
    f"{PERCEPTION_HUD_ROOT_REL}/perception_hud_types_v1.py",
    f"{SCHEMAS_PERCEPTION_HUD_REL}/perception_hud_scene_annotation_schema_v1.json",
    f"{SCHEMAS_PERCEPTION_HUD_REL}/perception_hud_reasoning_panel_schema_v1.json",
    f"{SCHEMAS_PERCEPTION_HUD_REL}/perception_hud_overlay_layer_schema_v1.json",
)

TASK_CONTEXTS: Tuple[str, ...] = (
    "general_scene_understanding",
    "street_navigation_test",
    "crossing_road_test",
    "find_object_test",
    "find_text_test",
    "indoor_navigation_test",
    "model_quality_review",
)

ENTITY_TYPES: Tuple[str, ...] = (
    "object", "region", "text", "motion", "landmark",
    "road_structure", "person", "vehicle", "unknown",
)

SPATIAL_RELATIONS: Tuple[str, ...] = (
    "left", "right", "center", "front", "near", "far", "on_path", "off_path", "unknown",
)

TASK_RELEVANCE: Tuple[str, ...] = (
    "relevant", "possible_risk", "background", "needs_confirmation", "unknown",
)

UNCERTAINTY_TAGS: Tuple[str, ...] = (
    "low_confidence", "boundary_uncertain", "occluded", "missing_depth",
    "missing_tracking", "missing_ocr", "need_next_frame",
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "Perception HUD View is read-only.",
    "Perception HUD must use existing envelope outputs.",
    "Perception HUD must not execute models.",
    "Perception HUD must not generate facts.",
    "Perception HUD must not write semantic layer.",
    "Perception HUD must not trigger navigation/action/speech.",
    "Candidate labels must not be upgraded to fact labels.",
    "MobileSAM prompt labels remain candidate-only.",
    "Reasoning panel is required.",
    "Task context is required.",
    "Uncertainty display is required.",
    "Missing information display is required.",
    "TestBoard record is required.",
    "Test artifacts are protected.",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "go_key": "hud_not_model_executor", "depends_on": "hud_not_model_executor"},
    {"guard_id": "B", "go_key": "hud_not_runner_caller", "depends_on": "hud_not_runner_caller"},
    {"guard_id": "C", "go_key": "candidate_not_fact", "depends_on": "candidate_not_fact"},
    {"guard_id": "D", "go_key": "no_navigation_speech", "depends_on": "no_navigation_speech"},
    {"guard_id": "E", "go_key": "no_semantic_fact_registry", "depends_on": "no_semantic_fact_registry"},
    {"guard_id": "F", "go_key": "no_runtime_output_adapter", "depends_on": "no_runtime_output_adapter"},
    {"guard_id": "G", "go_key": "no_external_camera_mic", "depends_on": "no_external_camera_mic"},
    {"guard_id": "H", "go_key": "no_delete_artifact", "depends_on": "no_delete_artifact"},
    {"guard_id": "I", "go_key": "reasoning_panel_defined", "depends_on": "reasoning_panel_defined"},
    {"guard_id": "J", "go_key": "task_context_defined", "depends_on": "task_context_defined"},
    {"guard_id": "K", "go_key": "uncertainty_defined", "depends_on": "uncertainty_defined"},
    {"guard_id": "L", "go_key": "mobile_sam_prompt_candidate_only", "depends_on": "mobile_sam_prompt_candidate_only"},
    {"guard_id": "M", "go_key": "test_board_planned", "depends_on": "test_board_planned"},
    {"guard_id": "N", "go_key": "test_board_protected", "depends_on": "test_board_protected"},
)

UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    "Phase-P1-Midplatform-Model-Test-Lens-Visual-Compare-View-Execution-And-Post-Review-v1-001",
    "Phase-P1-Midplatform-Model-Test-Lens-Visual-Overlay-Layer-Execution-And-Post-Review-v1-001",
    "Phase-P1-Midplatform-Model-Test-Lens-Simple-Mode-UX-Patch-Execution-And-Post-Review-v1-001",
    "Phase-P1-Midplatform-Model-Test-Lens-Local-Runner-Bridge-Service-Skeleton-Execution-And-Post-Review-v1-001",
    "Phase-P1-Midplatform-Model-Test-Lens-Local-Asset-Import-UI-Patch-Execution-And-Post-Review-v1-001",
)

PRESERVED_VIEW_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/model_test_lens/static_site/simple_mode_ui_v1.js",
    "capabilities/midplatform/model_test_lens/static_site/visual_compare_view_v1.js",
    "capabilities/midplatform/model_test_lens/static_site/visual_overlay_layer_v1.js",
    "capabilities/midplatform/model_test_lens/static_site/visual_overlay_renderer_v1.js",
    "capabilities/midplatform/model_test_lens/local_runner_bridge/local_runner_bridge_server_v1.py",
)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "perception_hud_scene_annotation_schema_plan_record",
    "perception_hud_reasoning_panel_schema_plan_record",
    "perception_hud_overlay_layer_schema_plan_record",
    "perception_hud_mobile_sam_adapter_plan_record",
    "perception_hud_future_model_adapter_plan_record",
)

NEXT_PHASE_EXECUTION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Perception-HUD-View-Execution-v1-001"
)


@dataclass
class PerceptionHudViewPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    perception_hud_view_planning: bool
    hud_is_read_only: bool
    hud_uses_existing_envelope: bool
    hud_may_display_annotations: bool
    hud_may_display_reasoning_panel: bool
    hud_may_display_task_relevance: bool
    hud_may_display_uncertainty: bool
    hud_may_display_suggestions: bool
    hud_must_not_execute_model: bool
    hud_must_not_generate_new_fact: bool
    hud_must_not_write_semantic: bool
    hud_must_not_trigger_navigation_action_speech: bool
    hud_must_not_call_output_adapter: bool
    hud_must_not_mutate_registry: bool
    model_execution_allowed_in_page: bool
    runtime_execution_allowed: bool
    output_adapter_allowed: bool
    semantic_layer_allowed: bool
    fact_write_allowed: bool
    navigation_action_speech_allowed: bool
    registry_mutation_allowed: bool
    external_network_allowed: bool
    live_camera_allowed: bool
    live_microphone_allowed: bool
    target_chain_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass
class NegativePerceptionHudViewPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool


@dataclass
class P1MidplatformModelTestLensPerceptionHudViewPlanningDecision:
    decision_ref: str
    perception_hud_view_planning_profile_count: int
    hud_scene_annotation_schema_defined: bool
    hud_reasoning_panel_schema_defined: bool
    hud_overlay_layer_schema_defined: bool
    reasoning_panel_required: bool
    task_context_supported: bool
    uncertainty_display_required: bool
    missing_information_display_required: bool
    mobile_sam_prompt_label_candidate_only: bool
    detection_hud_adapter_reserved: bool
    ocr_hud_adapter_reserved: bool
    slam_hud_adapter_reserved: bool
    simple_mode_preserved: bool
    visual_compare_view_preserved: bool
    local_runner_bridge_preserved: bool
    debug_mode_preserved: bool
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


@dataclass
class PerceptionHudMobileSamAdapterPlan:
    record_id: str
    model_id: str
    provides: Tuple[str, ...]
    does_not_provide: Tuple[str, ...]
    label_source: str
    prompt_label_candidate_only: bool
    followup_runners: Tuple[str, ...]
    example_observations: Tuple[str, ...] = field(default_factory=tuple)


@dataclass
class PerceptionHudFutureModelAdapterPlan:
    record_id: str
    adapters: Dict[str, Dict[str, Any]]


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)

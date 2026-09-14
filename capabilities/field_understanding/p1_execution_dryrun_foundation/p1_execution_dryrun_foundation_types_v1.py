# -*- coding: utf-8 -*-
"""P1 Execution DryRun Foundation — types v1.

This phase puts the already-planned P1 runnable assets into an *abstract execution
simulation layer* for the first time. It is NOT model download, NOT inference and
NOT runtime execution: each node only performs structure-level verification —
(1) import feasibility check, (2) dependency resolution check (mock),
(3) execution mock signature — to decide a structural execution state.

Core principles:
1. This is an Execution Simulation Layer: structure-level run verification only.
2. No real inference, no model download, no runtime execution, no dataset pull.
3. Each model maps to one RuntimeSimulationNode with a DryRunExecutionResult.
4. Execution states: STATE_A runnable / STATE_B partial / STATE_C blocked /
   STATE_D deferred.
5. The dependency graph must build with no cycles; execution path must stay
   a valid linear+branching hybrid.
6. Fallback chains stay candidate-only (rule-based / lighter model / disabled path).
7. All model outputs still become evidence candidates and pass adapter +
   midplatform; governance is reused with no bypass; no VLA action chain.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-P1-Execution-DryRun-Foundation-v1-001"
SCOPE = "p1_execution_dryrun_foundation"
SOURCE_CHAIN = "p1_execution_dryrun_foundation_v1"

PLANNING_PRINCIPLE_ZH = (
    "把已规划好的 P1 可运行资产第一次放进“可执行运行环境抽象模拟器”里跑起来——只做结构级运行验证，"
    "不是下载模型，不是推理，不是 runtime 执行。每个节点只做三件事：① import feasibility check（能否被加载，不安装）"
    "② dependency resolution check（依赖是否满足，模拟）③ execution mock signature（是否具备可运行形态），"
    "据此判定执行状态：STATE_A runnable / STATE_B partial / STATE_C blocked / STATE_D deferred。"
    "依赖图必须可构建且无环；执行路径保持 segmentation→tracking→detection→depth 的合法 linear+branching 混合图；"
    "fallback 仅为 candidate（rule-based / 轻量模型 / disabled path）。所有模型输出仍须先成为 evidence candidate 且"
    "经 adapter + 中台，治理复用必须保持（no governance bypass），无 VLA action chain。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_execution_dryrun_foundation_is_execution_simulation_layer_structure_level_only_no_inference_no_download_no_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
EXECUTION_MODE = "p1_execution_dryrun_foundation_structure_simulation_only"
DRYRUN_ONLY = True
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_ADMISSION_CONTRACT_CREATED = False
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True

P1_DOWNLOAD_LICENSE_PLANNING_REF = "Phase-Recognition-Model-P1-Download-License-Planning-v1-001"
RUNTIME_TRIAL_PLANNING_REF = "Phase-Model-Governance-Runtime-Trial-Planning-v1-001"
MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF = (
    "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-v1-001"
)
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_STEP_OPTIONS_REF = "p1_execution_trace_streaming_dryrun"

P1_DOWNLOAD_LICENSE_PLANNING_EXPECTED_GO = "RECOGNITION_MODEL_P1_DOWNLOAD_LICENSE_PLANNING_GO"

# --------------------------------------------------------------------------- #
# Execution state classification (4)
# --------------------------------------------------------------------------- #
STATE_A = "STATE_A_runnable"
STATE_B = "STATE_B_partial"
STATE_C = "STATE_C_blocked"
STATE_D = "STATE_D_deferred"

EXECUTION_STATES: Tuple[Dict[str, str], ...] = (
    {"state": STATE_A, "label": "runnable", "description": "mock_executable_structurally_runnable"},
    {"state": STATE_B, "label": "partial", "description": "missing_deps_or_license_constrained_but_structurally_valid"},
    {"state": STATE_C, "label": "blocked", "description": "blocked_by_license_dependency_or_architecture"},
    {"state": STATE_D, "label": "deferred", "description": "deferred_p2_or_heavy_models"},
)

# --------------------------------------------------------------------------- #
# 1. P1 execution graph nodes (stage ordering for the dependency graph)
#    segmentation -> tracking -> detection -> depth -> scene_relation(deferred)
# --------------------------------------------------------------------------- #
EXECUTION_GRAPH_NODES: Tuple[Dict[str, Any], ...] = (
    {"node_id": "segmentation", "order": 1, "deferred": False},
    {"node_id": "tracking", "order": 2, "deferred": False},
    {"node_id": "detection", "order": 3, "deferred": False},
    {"node_id": "depth", "order": 4, "deferred": False},
    {"node_id": "scene_relation", "order": 5, "deferred": True},
)

# Directed edges (acyclic). Linear backbone + one deferred branch terminus.
EXECUTION_GRAPH_EDGES: Tuple[Dict[str, str], ...] = (
    {"src": "segmentation", "dst": "tracking"},
    {"src": "tracking", "dst": "detection"},
    {"src": "detection", "dst": "depth"},
    {"src": "depth", "dst": "scene_relation"},
)

# --------------------------------------------------------------------------- #
# 2. Per-model runtime simulation nodes (dry-run, structure-level only)
#    import_ok / dep_ok / mock_signature_ok drive the execution state.
# --------------------------------------------------------------------------- #
RUNTIME_SIMULATION_NODES: Tuple[Dict[str, Any], ...] = (
    # ---- Segmentation ---- #
    {
        "model_id": "mobile_sam",
        "graph_node": "segmentation",
        "import_ok": True,
        "dep_ok": True,
        "mock_signature_ok": True,
        "license_constrained": False,
        "local_available": True,
        "deferred": False,
        "expected_state": STATE_A,
    },
    {
        "model_id": "fast_sam",
        "graph_node": "segmentation",
        "import_ok": True,
        "dep_ok": True,
        "mock_signature_ok": True,
        "license_constrained": True,  # AGPL restriction, no local weight -> structurally OK only
        "local_available": False,
        "deferred": False,
        "expected_state": STATE_B,
    },
    # ---- Tracking ---- #
    {
        "model_id": "byte_track",
        "graph_node": "tracking",
        "import_ok": True,
        "dep_ok": True,
        "mock_signature_ok": True,
        "license_constrained": False,
        "local_available": True,
        "deferred": False,
        "expected_state": STATE_A,
    },
    {
        "model_id": "deep_sort",
        "graph_node": "tracking",
        "import_ok": True,
        "dep_ok": True,
        "mock_signature_ok": True,
        "license_constrained": False,
        "local_available": True,
        "deferred": False,
        "expected_state": STATE_A,
    },
    # ---- Detection ---- #
    {
        "model_id": "yolov8n",
        "graph_node": "detection",
        "import_ok": True,
        "dep_ok": True,
        "mock_signature_ok": True,
        "license_constrained": True,  # AGPL but local weight available -> still STATE_A per spec
        "local_available": True,
        "deferred": False,
        "expected_state": STATE_A,
    },
    {
        "model_id": "rt_detr",
        "graph_node": "detection",
        "import_ok": True,
        "dep_ok": False,  # missing deps but structurally valid
        "mock_signature_ok": True,
        "license_constrained": False,
        "local_available": False,
        "deferred": False,
        "expected_state": STATE_B,
    },
    # ---- Depth ---- #
    {
        "model_id": "midas",
        "graph_node": "depth",
        "import_ok": True,
        "dep_ok": True,
        "mock_signature_ok": True,
        "license_constrained": False,
        "local_available": True,
        "deferred": False,
        "expected_state": STATE_A,
    },
    {
        "model_id": "depth_anything",
        "graph_node": "depth",
        "import_ok": True,
        "dep_ok": False,  # GPU/deps missing but structurally valid
        "mock_signature_ok": True,
        "license_constrained": False,
        "local_available": False,
        "deferred": False,
        "expected_state": STATE_B,
    },
    # ---- Scene Relation / VLM (all deferred) ---- #
    {
        "model_id": "scene_relation_vlm",
        "graph_node": "scene_relation",
        "import_ok": False,
        "dep_ok": False,
        "mock_signature_ok": False,
        "license_constrained": False,
        "local_available": False,
        "deferred": True,
        "expected_state": STATE_D,
    },
    {
        "model_id": "open_vocab_vlm",
        "graph_node": "scene_relation",
        "import_ok": False,
        "dep_ok": False,
        "mock_signature_ok": False,
        "license_constrained": False,
        "local_available": False,
        "deferred": True,
        "expected_state": STATE_D,
    },
)


def classify_execution_state(
    *,
    import_ok: bool,
    dep_ok: bool,
    mock_signature_ok: bool,
    license_constrained: bool,
    deferred: bool,
    local_available: bool = False,
) -> str:
    """Structure-level execution-state classification (no real execution).

    A license constraint downgrades to STATE_B only when no local weight is
    available (e.g. FastSAM); with a local weight present the model can still be
    STATE_A (e.g. YOLOv8n local available). Missing deps always downgrade to
    STATE_B; failed import/signature -> STATE_C; deferred -> STATE_D.
    """
    if deferred:
        return STATE_D
    if not import_ok or not mock_signature_ok:
        return STATE_C
    if not dep_ok:
        return STATE_B
    if license_constrained and not local_available:
        return STATE_B
    return STATE_A

# --------------------------------------------------------------------------- #
# 3. Model invocation plans (mock, candidate-only)
# --------------------------------------------------------------------------- #
MODEL_INVOCATION_STEPS: Tuple[str, ...] = (
    "import_feasibility_check",
    "dependency_resolution_check",
    "execution_mock_signature_check",
)

# --------------------------------------------------------------------------- #
# 4. Fallback chains (candidate-only)
# --------------------------------------------------------------------------- #
FALLBACK_CHAINS: Tuple[Dict[str, str], ...] = (
    {
        "trigger": "yolo_unavailable",
        "fallback_route": "opencv_rule_based_detection_candidate",
        "verified": "yolo_unavailable_to_opencv_fallback_ok",
    },
    {
        "trigger": "vlm_unavailable",
        "fallback_route": "scene_relation_disabled_path",
        "verified": "vlm_unavailable_to_scene_relation_disabled_ok",
    },
    {
        "trigger": "segmentation_model_unavailable",
        "fallback_route": "lighter_segmentation_or_disabled_candidate",
        "verified": "segmentation_fallback_ok",
    },
    {
        "trigger": "depth_gpu_unavailable",
        "fallback_route": "cpu_light_depth_candidate_or_defer",
        "verified": "depth_fallback_ok",
    },
)

# --------------------------------------------------------------------------- #
# 5. Resource constraint profiles (mock)
# --------------------------------------------------------------------------- #
RESOURCE_CONSTRAINT_PROFILES: Tuple[Dict[str, Any], ...] = (
    {"resource": "cpu", "available_mock": True, "required_for_backbone": True},
    {"resource": "gpu", "available_mock": False, "required_for_backbone": False},
    {"resource": "local_weight_store", "available_mock": True, "required_for_backbone": False},
    {"resource": "network_download", "available_mock": False, "required_for_backbone": False},
)

# --------------------------------------------------------------------------- #
# 6. Negative guards (8) — id -> (go_key, depends_on invariant)
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {
        "guard_id": "invalid_real_inference",
        "go_key": "no_real_inference",
        "depends_on": "real_inference_not_allowed",
    },
    {
        "guard_id": "invalid_model_download",
        "go_key": "no_model_download",
        "depends_on": "model_download_not_allowed",
    },
    {
        "guard_id": "invalid_runtime_execution",
        "go_key": "no_runtime_execution",
        "depends_on": "runtime_execution_not_allowed",
    },
    {
        "guard_id": "invalid_dataset_pull",
        "go_key": "no_dataset_pull",
        "depends_on": "dataset_pull_not_allowed",
    },
    {
        "guard_id": "invalid_dependency_install",
        "go_key": "no_dependency_install",
        "depends_on": "dependency_install_not_allowed",
    },
    {
        "guard_id": "invalid_vla_action_activation",
        "go_key": "no_vla_action_activation",
        "depends_on": "vla_action_chain_not_allowed",
    },
    {
        "guard_id": "invalid_runtime_escalation",
        "go_key": "no_runtime_escalation",
        "depends_on": "runtime_escalation_not_allowed",
    },
    {
        "guard_id": "invalid_governance_bypass",
        "go_key": "no_governance_bypass",
        "depends_on": "governance_reuse_preserved",
    },
)

# --------------------------------------------------------------------------- #
# Governance rules (22)
# --------------------------------------------------------------------------- #
DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_execution_simulation_layer_only",
    "structure_level_run_verification_only",
    "no_real_inference_is_enforced",
    "no_model_download_is_enforced",
    "no_runtime_execution_is_enforced",
    "no_dataset_pull_is_enforced",
    "no_dependency_install_is_enforced",
    "import_feasibility_is_checked_without_install",
    "dependency_resolution_is_mock_only",
    "execution_mock_signature_does_not_execute",
    "dependency_graph_must_build_with_no_cycles",
    "execution_path_must_be_valid_linear_branching_hybrid",
    "execution_states_are_structure_level_only",
    "deferred_models_are_state_d_not_runtime",
    "fallback_chains_are_candidate_only",
    "model_output_must_pass_recognition_model_output_adapter",
    "model_output_must_pass_midplatform_model_data_handling",
    "model_output_must_pass_midplatform_model_control",
    "candidate_only_boundary_must_be_preserved",
    "vla_action_chain_is_excluded",
    "existing_governance_must_be_reused_no_governance_bypass",
    "p1_execution_trace_streaming_dryrun_requires_separate_phase",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "ExecutionContext",
    "RuntimeSimulationNode",
    "DependencyGraph",
    "ModelInvocationPlan",
    "ExecutionTrace",
    "FallbackChain",
    "ResourceConstraintProfile",
    "DryRunExecutionResult",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": "Phase-P1-Execution-Trace-Streaming-DryRun-v1-001",
        "go_key": "p1_execution_trace_streaming_dryrun_readiness_recorded",
    },
)

SYSTEM_STAGE_SNAPSHOT: Tuple[Dict[str, str], ...] = (
    {"stage": "stage_1_model_integration", "status": "complete"},
    {"stage": "stage_2_midplatform_governance", "status": "complete"},
    {"stage": "stage_3_execution_simulation", "status": "current"},
    {"stage": "stage_4_streaming_runtime", "status": "not_entered"},
    {"stage": "stage_5_semantic_layer", "status": "not_entered"},
)

FINAL_DECISION_GO = "P1_EXECUTION_DRYRUN_FOUNDATION_GO"
FINAL_DECISION_BLOCKED = "P1_EXECUTION_DRYRUN_FOUNDATION_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
}

NEGATED_CREATION_FLAGS: Dict[str, bool] = {
    "new_admission_contract_created": False,
    "new_runtime_governance_created": False,
}

DRYRUN_TRUE_INVARIANTS: Dict[str, bool] = {
    "execution_simulation_layer_established": True,
    "dependency_graph_builds": True,
    "no_cycle_detected": True,
    "execution_path_valid": True,
    "reserved_or_deferred_family_not_runtime": True,
    "candidate_only_boundary_preserved": True,
    "model_output_adapter_required": True,
    "midplatform_data_handling_required": True,
    "midplatform_model_control_required": True,
    "governance_reuse_preserved": True,
    "luna_emotion_multimodal_brain_first_preserved": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "real_inference_allowed": False,
    "model_download_allowed": False,
    "auto_download_allowed": False,
    "runtime_execution_allowed": False,
    "dataset_pull_allowed": False,
    "dataset_download_allowed": False,
    "dataset_usage_allowed": False,
    "dependency_install_allowed": False,
    "model_tuning_allowed": False,
    "training_use_allowed": False,
    "new_image_recognition_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "continuous_runtime_allowed": False,
    "runtime_activation_allowed": False,
    "runtime_escalation_allowed": False,
    "navigation_runtime_allowed": False,
    "action_runtime_allowed": False,
    "speech_runtime_allowed": False,
    "fact_write_runtime_allowed": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "vla_action_chain_allowed": False,
    "semantic_promotion_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class ExecutionContext:
    context_ref: str
    phase_id: str
    execution_mode: str
    dryrun_only: bool
    existing_governance_reuse_required: bool
    new_admission_contract_created: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    p1_download_license_planning_ref: str
    model_governance_integrated_closure_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    invocation_steps: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RuntimeSimulationNode:
    model_id: str
    graph_node: str
    import_ok: bool
    dep_ok: bool
    mock_signature_ok: bool
    license_constrained: bool
    local_available: bool
    deferred: bool


@dataclass(frozen=True)
class DependencyGraph:
    node_count: int
    edge_count: int
    graph_build: bool
    cycle_detection: str
    topological_order: Tuple[str, ...]
    valid_linear_branching_hybrid: bool


@dataclass(frozen=True)
class ModelInvocationPlan:
    model_id: str
    graph_node: str
    steps: Tuple[str, ...]
    executes_now: bool


@dataclass(frozen=True)
class ExecutionTrace:
    model_id: str
    graph_node: str
    import_feasibility_check: bool
    dependency_resolution_check: bool
    execution_mock_signature_check: bool
    executed_real_inference: bool


@dataclass(frozen=True)
class FallbackChain:
    trigger: str
    fallback_route: str
    candidate_only: bool
    verified: str


@dataclass(frozen=True)
class ResourceConstraintProfile:
    resource: str
    available_mock: bool
    required_for_backbone: bool


@dataclass(frozen=True)
class DryRunExecutionResult:
    model_id: str
    graph_node: str
    execution_state: str
    expected_state: str
    state_match: bool
    executed_real_inference: bool
    downloaded_model: bool


@dataclass
class P1ExecutionDryRunNegativeGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ExecutionDryRunHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    entered_this_phase: bool


@dataclass(frozen=True)
class P1ExecutionDryRunFoundationDecision:
    decision_ref: str
    execution_context_count: int
    execution_graph_node_count: int
    runtime_simulation_node_count: int
    model_invocation_plan_count: int
    execution_trace_count: int
    dryrun_execution_result_count: int
    state_match_count: int
    fallback_chain_count: int
    resource_constraint_profile_count: int
    graph_build: bool
    cycle_detection: str
    negative_guard_count: int
    negative_guard_passed: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)

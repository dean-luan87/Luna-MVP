/**
 * Luna Observation Lens — compact dashboard app v1.
 * Local JSON / local runner bridge only. No model execution in page.
 * Browser entry: use window only — never bare global (Node).
 */
(function () {
  "use strict";

  var Copy = function () { return window.LunaObservationCopy || {}; };
  var Layout = function () { return window.LunaObservationLayout; };
  var Compact = function () { return window.LunaObservationCompactUI; };
  var BottomDrawers = function () { return window.LunaBottomDrawerTabs; };
  var LeftDrawer = function () { return window.LunaLeftCapabilityDrawer; };
  var CanvasLayout = function () { return window.ObservationCanvasFirstLayout; };
  var ChipBar = function () { return window.HudObjectChipBar; };
  var CorrectionUI = function () { return window.HumanCorrectionUI; };
  var AttentionEngine = function () { return window.ObservationAttentionEngine; };

  var BUILTIN_MOBILE_SAM_EXAMPLE = {
    envelope_id: "mobile_sam_multi_real_image_example_envelope_v1",
    phase_ref: "Phase-P1-MobileSAM-Multi-Real-Image-Inference-Trial-Execution-And-Post-Review-v1-001",
    test_case_id: "mobile_sam_multi_real_image_street_scenes_v1",
    model_id: "mobile_sam",
    model_category: "segmentation",
    model_version_or_registry_ref:
      "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json",
    input_asset_refs: [
      "capabilities/test_assets/p1/mobile_sam/multi/mobile_sam_multi_real_image_street_scene_v1_001.png",
      "capabilities/test_assets/p1/mobile_sam/multi/mobile_sam_multi_real_image_street_scene_v1_002.png",
      "capabilities/test_assets/p1/mobile_sam/multi/mobile_sam_multi_real_image_street_scene_v1_003.png",
      "capabilities/test_assets/p1/mobile_sam/multi/mobile_sam_multi_real_image_street_scene_v1_004.png"
    ],
    test_manifest_ref:
      "_tmp_eval_out/p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_v1_smoke_v0/mobile_sam_multi_real_image_manifest_v1.json",
    execution_trace_ref:
      "_tmp_eval_out/p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_v1_smoke_v0/multi_real_image_prompt_execution_record_v1.json",
    candidate_outputs: [],
    visualization_layers: [
      {
        layer_id: "mask_overlay_building_001",
        layer_type: "mask",
        source_artifact_ref:
          "_tmp_eval_out/p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_v1_smoke_v0/candidate_masks/mobile_sam_multi_real_image_street_scene_v1_001_building_or_large_structure_candidate_mask.png",
        display_name: "building_or_large_structure",
        model_id: "mobile_sam",
        candidate_only: true,
        opacity: 0.55,
        color_class: "seg-building"
      }
    ],
    metrics: {
      image_count: 4,
      prompt_attempt_count: 20,
      prompt_success_count: 20,
      prompt_failure_count: 0,
      overall_success_rate: 1.0,
      per_category_average_score: {
        building_or_large_structure: 0.9323,
        road_or_crosswalk_or_large_plane: 0.9141,
        sign_or_advertisement_screen: 0.8112,
        vehicle_or_small_dynamic_object: 0.8555,
        street_facility_or_pole_or_edge_object: 0.7521
      }
    },
    failure_modes: [],
    quality_summary: {
      human_review_required: true,
      suitable_for_runtime_admission: false,
      suitable_for_quality_observation: true,
      not_semantic_fact: true,
      aggregate_note: "20/20 prompt success across 4 daytime street scenes"
    },
    test_board_refs: [
      "capabilities/test_board/recognition_models/phase_p1_mobilesam_multi_real_image_inference_trial_execution_and_post_review_v1_001/"
    ],
    protected_artifact_refs: [],
    boundary_flags: {
      candidate_only: true,
      not_fact: true,
      not_runtime_output: true,
      not_output_adapter_output: true,
      not_semantic_output: true,
      not_navigation_action_speech: true
    },
    readiness_effect: {
      runtime_ready: false,
      output_adapter_ready: false,
      semantic_layer_ready: false,
      fact_write_ready: false,
      navigation_action_speech_ready: false
    },
    testboard_protection: { protected: true, non_deletable: true, deletion_forbidden: true }
  };

  var BUILTIN_SLAM_EXAMPLE = {
    envelope_id: "slam_orb_luna_street_scene_envelope_example_slim_v1",
    phase_ref: "Phase-P1-Midplatform-Model-Test-Lens-MUEP-SLAM-Adapter-v1-001",
    test_case_id: "slam_luna_street_scene_v1_orb_slam_v1",
    model_id: "orb_slam",
    model_category: "slam_vio",
    input_asset_refs: [
      "capabilities/test_assets/p1/slam/luna_street_scene_v1/sequence_manifest_v1.json"
    ],
    muep: {
      protocol_version: "muep_v1",
      output: {
        metrics: {
          layer_a_task: { primary_metric_name: "ATE_rmse_m", primary_metric_value: 0.068, primary_metric_score_normalized: 0.864 },
          layer_b_robustness: { motion_blur_sensitivity: 0.19, low_light_degradation: 0.14, loop_closure_stability: 0.91, robustness_score_normalized: 0.857 },
          layer_c_structural: { structural_quality_score_normalized: 0.947, notes: ["trajectory_smoothness=0.998", "map_consistency=0.870"] },
          final_score: 0.875,
          scoring_weights: { task: 0.6, robustness: 0.25, structural: 0.15 }
        },
        failure_modes: ["tracking_lost"],
        confidence: 0.938
      }
    },
    visualization_layers: [
      {
        layer_id: "trajectory_xy_overlay",
        layer_type: "trajectory",
        display_name: "estimated vs ground_truth (XY)",
        trajectory_estimated: [
          [0,0.005,0],[0.23,0.024,0],[0.45,0.042,0],[0.67,0.058,0],[0.88,0.071,0],
          [1.1,0.08,0],[1.32,0.084,0],[1.55,0.085,0],[1.78,0.08,0],[2.01,0.072,0],
          [2.22,0.059,0],[2.44,0.044,0],[2.65,0.026,0],[2.88,0.007,0],[3.11,-0.012,0],
          [3.34,-0.03,0],[3.56,-0.046,0],[3.78,-0.06,0],[3.99,-0.069,0],[4.21,-0.074,0]
        ],
        trajectory_ground_truth: [
          [0,0,0],[0.21,0.019,0],[0.42,0.037,0],[0.63,0.053,0],[0.84,0.066,0],
          [1.05,0.075,0],[1.26,0.079,0],[1.47,0.08,0],[1.68,0.075,0],[1.89,0.067,0],
          [2.1,0.054,0],[2.31,0.039,0],[2.52,0.021,0],[2.73,0.002,0],[2.94,-0.017,0],
          [3.15,-0.035,0],[3.36,-0.051,0],[3.57,-0.065,0],[3.78,-0.074,0],[3.99,-0.079,0]
        ],
        candidate_only: true
      }
    ],
    metrics: {
      muep_final_score: 0.875,
      slam: {
        ate_rmse_m: 0.068,
        drift_rate: 0.0163,
        tracking_stability: 0.9583,
        slam_score: 0.853,
        path_length_m: 4.174,
        tracked_frames: 115,
        total_frames: 120,
        structural: { map_consistency_score: 0.87, trajectory_smoothness: 0.998, loop_closure_correctness: 1.0 },
        robustness: { motion_blur_sensitivity: 0.19, low_light_degradation: 0.14, loop_closure_stability: 0.91 }
      }
    },
    failure_modes: ["tracking_lost"],
    quality_summary: {
      human_review_required: true,
      suitable_for_runtime_admission: false,
      not_semantic_fact: true,
      aggregate_note: "SLAM adapter V1 — ORB-SLAM on Luna street scene (MUEP + ATE/drift)"
    },
    boundary_flags: {
      candidate_only: true,
      not_fact: true,
      not_runtime_output: true,
      not_output_adapter_output: true,
      not_semantic_output: true,
      not_navigation_action_speech: true
    },
    readiness_effect: {
      runtime_ready: false,
      output_adapter_ready: false,
      semantic_layer_ready: false,
      fact_write_ready: false,
      navigation_action_speech_ready: false
    },
    testboard_protection: { protected: true, non_deletable: true, deletion_forbidden: true }
  };

  var REQUIRED_ENVELOPE_FIELDS = [
    "envelope_id", "test_case_id", "model_id", "model_category",
    "input_asset_refs", "boundary_flags", "readiness_effect"
  ];

  var state = {
    envelope: null,
    capabilityId: "segmentation",
    viewMode: "hud",
    debugMode: false,
    advancedDrawerOpen: false,
    importApi: null,
    simpleController: null,
    dockApi: null,
    leftDrawerApi: null,
    hudApi: null,
    hudEntities: null,
    selectedEntityId: null,
    noAttentionRegionId: null,
    chipBarApi: null,
    correctionApi: null,
    attentionPkg: null,
    queueStore: null,
    queuePkg: null,
    requestStore: null,
    requestPkg: null,
    executionStore: null,
    executionPkg: null,
    resultStore: null,
    resultPkg: null,
    midplatformPkg: null,
    collaborationPkg: null,
    ocrStore: null,
    ocrPkg: null,
    sceneProfileCandidate: null,
    dualRoutePkg: null,
    activationPkg: null,
    situationPkg: null,
    agentPlanningPkg: null
  };

  function enrichEnvelopeSceneAware(data) {
    if (!data) return data;
    if (window.SegmentationPromptPolicy && window.SegmentationPromptPolicy.enrichEnvelopeLayers) {
      window.SegmentationPromptPolicy.enrichEnvelopeLayers(data);
    }
    if (!data.scene_profile_candidate && window.SceneProfileCandidate) {
      var ref = (data.input_asset_refs && data.input_asset_refs[0]) || data._source_file_name || "";
      data.scene_profile_candidate = window.SceneProfileCandidate.buildCandidate(data, ref);
    }
    if (!data.segmentation_prompt_policy && data.scene_profile_candidate && window.SegmentationPromptPolicy) {
      data.segmentation_prompt_policy = window.SegmentationPromptPolicy.selectPolicy(data.scene_profile_candidate);
    }
    state.sceneProfileCandidate = data.scene_profile_candidate || null;
    return data;
  }

  function taskContextFromEnvelope(envelope) {
    var scene = envelope && envelope.scene_profile_candidate;
    if (window.SceneProfilePolicy && scene) {
      return window.SceneProfilePolicy.taskContextForScene(scene.scene_type_candidate);
    }
    return "street_navigation_test";
  }

  function el(id) { return document.getElementById(id); }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function validateEnvelope(data) {
    if (!data || typeof data !== "object") return { ok: false, error: "not an object" };
    var missing = [];
    for (var i = 0; i < REQUIRED_ENVELOPE_FIELDS.length; i++) {
      if (data[REQUIRED_ENVELOPE_FIELDS[i]] === undefined) missing.push(REQUIRED_ENVELOPE_FIELDS[i]);
    }
    if (missing.length) return { ok: false, error: "missing fields: " + missing.join(", ") };
    return { ok: true };
  }

  function setLoadStatus(text, kind) {
    var s = el("lol-load-status");
    if (!s) return;
    s.textContent = text || "";
    s.className = "load-status" + (kind ? " " + kind : "");
  }

  function setServiceStatus(ok) {
    var s = el("lol-service-status");
    var recheck = el("lol-recheck-service");
    if (!s) return;
    s.textContent = ok ? Copy().serviceOk : Copy().serviceOff;
    s.className = "lol-service-status " + (ok ? "ok" : "warn");
    if (!ok) {
      s.title = Copy().serviceHint;
      if (recheck) recheck.hidden = false;
    } else if (recheck) {
      recheck.hidden = true;
    }
  }

  function recheckService() {
    if (!state.simpleController) return;
    var s = el("lol-service-status");
    if (s) s.textContent = "正在检查本地测试服务…";
    state.simpleController.checkService().then(updateStartButton);
  }

  function updateStartButton() {
    var btn = el("lol-start-btn");
    if (!btn || !state.simpleController) return;
    btn.disabled = !state.simpleController.canStart();
  }

  function capabilityFromEnvelope(env) {
    if (!env) return state.capabilityId;
    if (env.model_category === "slam_vio") return "slam";
    if (env.model_category === "segmentation" || env.model_id === "mobile_sam") return "segmentation";
    return state.capabilityId;
  }

  function renderLeftRail() {
    var host = el("lol-left-rail");
    if (!host) return;
    if (LeftDrawer()) {
      state.leftDrawerApi = LeftDrawer().render(host, state, function (capId) {
        state.capabilityId = capId;
        if (state.simpleController) state.simpleController.setCapability(capId);
        renderLeftRail();
        updateStartButton();
      });
      if (state.leftDrawerApi) {
        state.leftDrawerApi.updateInputSummary(
          state.simpleController && state.simpleController.getFile(),
          state.capabilityId
        );
      }
    } else if (Layout()) {
      Layout().renderCapabilityRail(host, state, function (capId) {
        state.capabilityId = capId;
        if (state.simpleController) state.simpleController.setCapability(capId);
        renderLeftRail();
        updateStartButton();
      });
      Layout().updateInputSummary(host, state.simpleController && state.simpleController.getFile(), state.capabilityId);
    }
    var samBtn = host.querySelector("#lol-example-sam");
    var slamBtn = host.querySelector("#lol-example-slam");
    if (samBtn) samBtn.addEventListener("click", loadBuiltinExample);
    if (slamBtn) slamBtn.addEventListener("click", loadBuiltinSlamExample);
  }

  function findEntityById(entityId) {
    if (!entityId || !state.hudEntities) return null;
    for (var i = 0; i < state.hudEntities.length; i++) {
      if (state.hudEntities[i].entity_id === entityId) return state.hudEntities[i];
    }
    return null;
  }

  function buildAttentionPackage(entities) {
    if (!AttentionEngine() || !state.envelope || !entities || !entities.length) {
      state.attentionPkg = null;
      return null;
    }
    state.attentionPkg = AttentionEngine().buildAttentionPackage(state.envelope, entities, {
      video_or_single_frame_context: "single_frame",
      task_context: taskContextFromEnvelope(state.envelope)
    });
    return state.attentionPkg;
  }

  function buildQueuePackage(entities) {
    if (!window.FollowupRunnerRouteQueue || !state.attentionPkg) {
      state.queuePkg = null;
      return null;
    }
    if (!state.queueStore && window.FollowupRunnerRouteQueueState) {
      state.queueStore = window.FollowupRunnerRouteQueueState.createStore();
    }
    state.queuePkg = window.FollowupRunnerRouteQueue.buildFromAttention(
      state.attentionPkg, entities || state.hudEntities, state.queueStore
    );
    return state.queuePkg;
  }

  function buildRequestPackage() {
    if (!window.RunnerManualTriggerRequest || !state.requestStore) {
      state.requestPkg = null;
      return null;
    }
    state.requestPkg = window.RunnerManualTriggerRequest.buildPackage(state.requestStore);
    if (window.RunnerInvocationAdmission && state.requestPkg) {
      state.requestPkg = window.RunnerInvocationAdmission.enrichPackage(state.requestPkg);
    }
    return state.requestPkg;
  }

  function buildExecutionPackage() {
    if (!window.ControlledRunnerExecutionUI || !state.executionStore) {
      state.executionPkg = null;
      state.resultPkg = null;
      return null;
    }
    state.executionPkg = window.ControlledRunnerExecutionUI.buildPackage(state.executionStore);
    if (state.executionPkg) {
      state.executionPkg = window.ControlledRunnerExecutionUI.enrichPackage(state.executionPkg);
    }
    return state.executionPkg;
  }

  function buildCollaborationPackage() {
    if (!window.MultiModelCollaborationState) {
      state.collaborationPkg = null;
      return null;
    }
    state.collaborationPkg = window.MultiModelCollaborationState.buildPackage(state.midplatformPkg);
    return state.collaborationPkg;
  }

  function ensureOcrStore() {
    if (!state.ocrStore && window.MobileSamOcrRequestState) {
      state.ocrStore = window.MobileSamOcrRequestState.createStore();
    }
    return state.ocrStore;
  }

  function buildOcrControlledPackage() {
    if (!window.MobileSamOcrControlledExecutionSummary) {
      state.ocrPkg = null;
      return null;
    }
    ensureOcrStore();
    state.ocrPkg = window.MobileSamOcrControlledExecutionSummary.buildPackage(state.ocrStore);
    if (window.MobileSamOcrAdmission && state.ocrPkg) {
      state.ocrPkg = window.MobileSamOcrAdmission.enrichPackage(state.ocrPkg);
    }
    return state.ocrPkg;
  }

  function findCollaborationItemByTaskId(taskId) {
    var items = state.collaborationPkg && state.collaborationPkg.items;
    if (!items || !taskId) return null;
    for (var i = 0; i < items.length; i++) {
      var task = items[i].ocr_task_candidate;
      if (task && task.task_candidate_id === taskId) return items[i];
    }
    return null;
  }

  function onGenerateOcrRequest(taskId) {
    if (!window.MobileSamOcrRequestUI) return;
    ensureOcrStore();
    var item = findCollaborationItemByTaskId(taskId);
    if (!item) return;
    var built = window.MobileSamOcrRequestUI.buildFromOcrTaskCandidate(
      item, state.envelope, state.ocrStore
    );
    if (!built.ok || !built.request) return;
    state.ocrStore.addRequest(built.request);
    buildOcrControlledPackage();
    refreshRightPanel();
    updateDockSummary();
  }

  function runOcrAdmissionCheck(oirId) {
    if (!window.MobileSamOcrAdmission || !state.ocrStore) return;
    var req = state.ocrStore.findRequest(oirId);
    if (!req || req.admission_status === "cancelled") return;
    var seq = state.ocrStore.nextEvalSeq ? state.ocrStore.nextEvalSeq() : 1;
    var evaluated = window.MobileSamOcrAdmission.evaluate(req, { seq: seq });
    if (evaluated && evaluated.result) {
      state.ocrStore.setAdmissionResult(oirId, evaluated.result);
    }
    buildOcrControlledPackage();
    refreshRightPanel();
    updateDockSummary();
  }

  function onGenerateOcrExecutionCandidate(oirId) {
    if (!window.MobileSamOcrExecutionCandidate || !state.ocrStore) return;
    var req = state.ocrStore.findRequest(oirId);
    if (!req) return;
    var built = window.MobileSamOcrExecutionCandidate.buildFromAdmittedRequest(
      req, state.ocrStore, state.envelope
    );
    if (!built.ok || !built.candidate) return;
    state.ocrStore.addExecutionCandidate(built.candidate);
    buildOcrControlledPackage();
    refreshRightPanel();
    updateDockSummary();
  }

  function onRunControlledOcr(ocecId) {
    if (!window.RunnerSandboxClient || !state.ocrStore) return;
    if (!state.resultStore && window.ResultLayerState) {
      state.resultStore = window.ResultLayerState.createStore();
    }
    var candidate = state.ocrStore.findCandidate(ocecId);
    if (!candidate) return;
    window.RunnerSandboxClient.runControlledOcr(candidate).then(function (resp) {
      var payload = resp && resp.result;
      if (state.resultStore && payload) state.resultStore.addExecutionResult(payload);
      buildResultPackage();
      buildOcrControlledPackage();
      refreshRightPanel();
      updateDockSummary();
    }).catch(function () {
      buildResultPackage();
      refreshRightPanel();
      updateDockSummary();
    });
  }

  function onOcrAction(action, oirId, ocecId) {
    if (action === "run-controlled-ocr") {
      if (ocecId) onRunControlledOcr(ocecId);
      return;
    }
    if (!state.ocrStore || !oirId) return;
    if (action === "run-admission") {
      runOcrAdmissionCheck(oirId);
      return;
    }
    if (action === "cancel") {
      state.ocrStore.cancelRequest(oirId);
      buildOcrControlledPackage();
      refreshRightPanel();
      updateDockSummary();
      return;
    }
    if (action === "generate-candidate") {
      onGenerateOcrExecutionCandidate(oirId);
    }
  }

  function onOcrCollabPanelClick(ev) {
    var btn = ev.target.closest("[data-ocr-collab-action]");
    if (!btn) return;
    ev.preventDefault();
    if (btn.getAttribute("data-ocr-collab-action") === "generate-request") {
      onGenerateOcrRequest(btn.getAttribute("data-task-id"));
    }
  }

  function buildDualRoutePackage() {
    if (!window.DualRoutePerceptionState || !state.envelope) {
      state.dualRoutePkg = null;
      return null;
    }
    if (state.envelope.model_category !== "segmentation" && state.envelope.model_id !== "mobile_sam") {
      state.dualRoutePkg = null;
      return null;
    }
    state.dualRoutePkg = window.DualRoutePerceptionState.buildPackage(state.envelope, {
      scene_profile_candidate: state.sceneProfileCandidate || state.envelope.scene_profile_candidate
    });
    return state.dualRoutePkg;
  }

  function buildSituationPackage() {
    if (!window.LunaSituationUnderstandingState || !state.envelope) {
      state.situationPkg = null;
      return null;
    }
    state.situationPkg = window.LunaSituationUnderstandingState.buildPackage(state.envelope, {
      scene_profile_candidate: state.sceneProfileCandidate || state.envelope.scene_profile_candidate
    });
    return state.situationPkg;
  }

  function buildAgentPlanningPackage() {
    if (!window.LunaAgentPlanningState || !state.envelope || !state.situationPkg) {
      state.agentPlanningPkg = null;
      return null;
    }
    state.agentPlanningPkg = window.LunaAgentPlanningState.buildPackage(state.envelope, {
      situationPkg: state.situationPkg,
      user_goal_candidate: state.envelope.user_goal_candidate ||
        state.envelope.user_goal_candidate_optional || null
    });
    return state.agentPlanningPkg;
  }

  function buildActivationPackage() {
    if (!window.SceneTaskModelActivationState || !state.envelope) {
      state.activationPkg = null;
      return null;
    }
    if (state.envelope.model_category !== "segmentation" && state.envelope.model_id !== "mobile_sam") {
      state.activationPkg = null;
      return null;
    }
    state.activationPkg = window.SceneTaskModelActivationState.buildPackage(state.envelope, {
      scene_profile_candidate: state.sceneProfileCandidate || state.envelope.scene_profile_candidate,
      attentionPkg: state.attentionPkg
    });
    return state.activationPkg;
  }

  function onActivationAssignmentSelect(assignment) {
    if (!assignment || !state.hudApi) return;
    var targetId = null;
    if (assignment.assigned_text_region_ids && assignment.assigned_text_region_ids.length) {
      targetId = assignment.assigned_text_region_ids[0];
    } else if (assignment.assigned_region_ids && assignment.assigned_region_ids.length) {
      targetId = assignment.assigned_region_ids[0];
    }
    if (!targetId) return;
    var ent = findEntityById(targetId);
    if (ent && state.hudApi.highlightEntity) {
      state.hudApi.highlightEntity(ent.entity_id);
    }
  }

  function buildMidplatformPackage() {
    if (!window.MidplatformInteractionState) {
      state.midplatformPkg = null;
      return null;
    }
    state.midplatformPkg = window.MidplatformInteractionState.buildPackage({
      resultPkg: state.resultPkg,
      attentionPkg: state.attentionPkg,
      executionPkg: state.executionPkg,
      imageRef: state.envelope && state.envelope.input_asset_refs &&
        state.envelope.input_asset_refs[0]
    });
    buildCollaborationPackage();
    buildOcrControlledPackage();
    return state.midplatformPkg;
  }

  function buildResultPackage() {
    if (!state.resultStore) {
      state.resultPkg = null;
      return null;
    }
    var results = state.resultStore.getActiveResults ? state.resultStore.getActiveResults() : [];
    var errors = state.resultStore.getErrors ? state.resultStore.getErrors() : [];
    var executions = state.resultStore.getExecutions ? state.resultStore.getExecutions() : [];
    state.resultPkg = {
      results: results,
      errors: errors,
      executions: executions,
      active_results: results,
      stats: { results: results.length, errors: errors.length, executions: executions.length },
      candidate_only: true,
      not_fact: true,
      result_layer_not_observation_layer: true
    };
    buildMidplatformPackage();
    return state.resultPkg;
  }

  function findTaskByRtc(rtcId) {
    if (!rtcId || !state.queuePkg || !state.queuePkg.tasks) return null;
    for (var i = 0; i < state.queuePkg.tasks.length; i++) {
      if (state.queuePkg.tasks[i].runner_task_candidate_id === rtcId) {
        return state.queuePkg.tasks[i];
      }
    }
    return null;
  }

  function updateDockSummary() {
    if (!state.dockApi || !state.envelope) return;
    var pkg = window.ModelInsightLayer.buildInsightPackage(state.envelope);
    state.dockApi.setSummary(Compact().buildMetricsSummary(
      state.envelope, pkg, state.attentionPkg, state.queuePkg, state.requestPkg,
      state.executionPkg, state.resultPkg, state.ocrPkg, state.dualRoutePkg, state.activationPkg,
      state.situationPkg, state.agentPlanningPkg
    ));
  }

  function onGenerateRequest(rtcId) {
    if (!window.RunnerManualTriggerRequest || !window.RunnerManualTriggerRequestState) return;
    if (!state.requestStore) {
      state.requestStore = window.RunnerManualTriggerRequestState.createStore();
    }
    var task = findTaskByRtc(rtcId);
    if (!task) return;
    var built = window.RunnerManualTriggerRequest.buildFromPinnedTask(
      task, state.envelope, state.requestStore, { developerMode: state.debugMode }
    );
    if (!built.ok || !built.request) return;
    state.requestStore.add(built.request);
    buildRequestPackage();
    refreshRightPanel();
    updateDockSummary();
  }

  function runAdmissionCheck(rirId, isRecheck) {
    if (!window.RunnerInvocationAdmission || !state.requestStore) return;
    var req = state.requestStore.findById(rirId);
    if (!req || req.admission_status === "cancelled") return;
    var task = findTaskByRtc(req.source_runner_task_candidate_id);
    var seq = state.requestStore.nextEvalSeq ? state.requestStore.nextEvalSeq() : 1;
    var evaluated = window.RunnerInvocationAdmission.evaluate(req, task, { seq: seq });
    if (evaluated && evaluated.result) {
      state.requestStore.setAdmissionResult(rirId, evaluated.result);
    }
    buildRequestPackage();
    refreshRightPanel();
    updateDockSummary();
  }

  function onGenerateExecutionCandidate(rirId) {
    if (!window.ControlledRunnerExecutionUI || !window.ControlledRunnerExecutionState) return;
    if (!state.requestStore) return;
    if (!state.executionStore) {
      state.executionStore = window.ControlledRunnerExecutionState.createStore();
    }
    var req = state.requestStore.findById(rirId);
    if (!req) return;
    var task = findTaskByRtc(req.source_runner_task_candidate_id);
    var built = window.ControlledRunnerExecutionUI.buildFromAdmittedRequest(
      req, task, state.envelope, state.executionStore, { developerMode: state.debugMode }
    );
    if (!built.ok || !built.candidate) return;
    state.executionStore.add(built.candidate);
    buildExecutionPackage();
    refreshRightPanel();
    updateDockSummary();
  }

  function onGenerateMobileSamCandidate(rirId) {
    if (!window.ControlledRunnerExecutionUI || !window.ControlledRunnerExecutionState) return;
    if (!state.requestStore) return;
    if (!state.executionStore) {
      state.executionStore = window.ControlledRunnerExecutionState.createStore();
    }
    var req = state.requestStore.findById(rirId);
    if (!req) return;
    var task = findTaskByRtc(req.source_runner_task_candidate_id);
    var built = window.ControlledRunnerExecutionUI.buildMobileSamFromAdmittedRequest(
      req, task, state.envelope, state.executionStore, { developerMode: state.debugMode }
    );
    if (!built.ok || !built.candidate) return;
    state.executionStore.add(built.candidate);
    buildExecutionPackage();
    refreshRightPanel();
    updateDockSummary();
  }

  function resolveImageRefForExecution(candidate) {
    if (!candidate) return "";
    if (candidate.input_payload_ref && candidate.input_payload_ref.indexOf("local-file://") === 0) {
      return candidate.input_payload_ref;
    }
    if (state.envelope && state.envelope.input_asset_refs && state.envelope.input_asset_refs.length) {
      return "local-file://" + state.envelope.input_asset_refs[0];
    }
    return candidate.input_payload_ref || "";
  }

  function onRunControlledMobileSam(crecId) {
    if (!window.RunnerSandboxClient || !state.executionStore) return;
    if (!state.resultStore && window.ResultLayerState) {
      state.resultStore = window.ResultLayerState.createStore();
    }
    var candidate = state.executionStore.findById(crecId);
    if (!candidate || !window.ControlledRunnerExecutionUI.canRunControlledMobileSam(candidate)) return;
    var imageRef = resolveImageRefForExecution(candidate);
    window.RunnerSandboxClient.runControlledMobileSam(candidate, imageRef).then(function (resp) {
      var payload = resp && resp.result;
      if (state.resultStore && payload) state.resultStore.addExecutionResult(payload);
      buildResultPackage();
      refreshRightPanel();
      updateDockSummary();
    }).catch(function () {
      buildResultPackage();
      refreshRightPanel();
      updateDockSummary();
    });
  }

  function onExecutionAction(action, crecId) {
    if (!state.executionStore || !crecId) return;
    if (action === "run-controlled-mobilesam") {
      onRunControlledMobileSam(crecId);
      return;
    }
    if (action === "cancel") state.executionStore.cancel(crecId);
    else if (action === "mark-ready") state.executionStore.setStatus(crecId, "ready_for_execution_review");
    buildExecutionPackage();
    refreshRightPanel();
    updateDockSummary();
  }

  function onRequestAction(action, rirId) {
    if (!state.requestStore || !rirId) return;
    if (action === "generate-execution-candidate") {
      onGenerateExecutionCandidate(rirId);
      return;
    }
    if (action === "generate-mobilesam-candidate") {
      onGenerateMobileSamCandidate(rirId);
      return;
    }
    if (action === "run-admission" || action === "recheck-admission") {
      runAdmissionCheck(rirId, action === "recheck-admission");
      return;
    }
    if (action === "cancel") state.requestStore.cancel(rirId);
    buildRequestPackage();
    refreshRightPanel();
    updateDockSummary();
  }

  function onQueueAction(action, rtcId) {
    if (action === "generate-request") {
      onGenerateRequest(rtcId);
      return;
    }
    if (!state.queueStore || !rtcId) return;
    if (action === "pin") state.queueStore.pin(rtcId);
    else if (action === "unpin") state.queueStore.unpin(rtcId);
    else if (action === "exclude") state.queueStore.exclude(rtcId);
    else if (action === "restore") state.queueStore.restore(rtcId);
    buildQueuePackage(state.hudEntities);
    refreshRightPanel();
    updateDockSummary();
  }

  function refreshAttentionUi(entities) {
    var ents = entities || state.hudEntities;
    if (!ents || !ents.length || !state.envelope) {
      state.attentionPkg = null;
      state.queuePkg = null;
      state.requestPkg = null;
      state.executionPkg = null;
      state.resultPkg = null;
      state.midplatformPkg = null;
      state.dualRoutePkg = null;
      state.activationPkg = null;
      state.situationPkg = null;
      state.agentPlanningPkg = null;
      return;
    }
    buildSituationPackage();
    buildAgentPlanningPackage();
    buildAttentionPackage(ents);
    buildQueuePackage(ents);
    buildRequestPackage();
    buildExecutionPackage();
    buildResultPackage();
    buildMidplatformPackage();
    buildDualRoutePackage();
    buildActivationPackage();
    if (state.chipBarApi && state.chipBarApi.update) {
      state.chipBarApi.update({ attentionPkg: state.attentionPkg });
    } else if (ents) {
      renderObjectChipBar(ents);
    }
    if (state.hudApi && state.hudApi.setAttentionPkg) {
      state.hudApi.setAttentionPkg(state.attentionPkg);
      state.hudApi.redraw();
    }
    refreshRightPanel();
    updateDockSummary();
  }

  function scrollToAttentionRecord(entityId) {
    var host = document.getElementById("lol-right-attention-host");
    if (window.ObservationAttentionPriorityPanel && host) {
      window.ObservationAttentionPriorityPanel.scrollToRegion(host, entityId);
    }
  }

  function hasAttentionRecord(regionId) {
    if (!regionId || !state.attentionPkg) return false;
    if (window.VisualExpressionInteraction) {
      return window.VisualExpressionInteraction.hasAttentionRecord(state.attentionPkg, regionId);
    }
    return !!(AttentionEngine() && AttentionEngine().lookupRecord(state.attentionPkg, regionId));
  }

  function onPanelHoverRegion(regionId) {
    if (state.hudApi && state.hudApi.hoverEntity) {
      state.hudApi.hoverEntity(regionId);
    }
  }

  function refreshRightPanel() {
    if (!state.envelope) return;
    var right = el("lol-right-panel");
    var pkg = window.ModelInsightLayer.buildInsightPackage(state.envelope);
    var reasoning = Compact().getReasoning(state.envelope);
    Compact().renderRightPanel(right, state.envelope, pkg, reasoning, {
      attentionPkg: state.attentionPkg,
      queuePkg: state.queuePkg,
      requestPkg: state.requestPkg,
      requestStore: state.requestStore,
      executionPkg: state.executionPkg,
      executionStore: state.executionStore,
      resultPkg: state.resultPkg,
      midplatformPkg: state.midplatformPkg,
      collaborationPkg: state.collaborationPkg,
      dualRoutePkg: state.dualRoutePkg,
      activationPkg: state.activationPkg,
      situationPkg: state.situationPkg,
      agentPlanningPkg: state.agentPlanningPkg,
      ocrPkg: state.ocrPkg,
      onOcrAction: onOcrAction,
      selectedEntity: findSelectedEntity(),
      noAttentionRegionId: state.noAttentionRegionId,
      getEntityGlyph: function (regionId) {
        var ent = findEntityById(regionId);
        return ent && ent.hud_number_glyph;
      },
      getEntityShortLabel: function (regionId) {
        var ent = findEntityById(regionId);
        return ent && ent.hud_short_label;
      },
      onSelectRegion: onChipSelect,
      onHoverRegion: onPanelHoverRegion,
      onQueueAction: onQueueAction,
      onActivationAssignmentSelect: onActivationAssignmentSelect,
      onRequestAction: onRequestAction,
      onExecutionAction: onExecutionAction,
      onClearSelection: function () {
        state.selectedEntityId = null;
        state.noAttentionRegionId = null;
        if (state.hudApi && state.hudApi.highlightEntity) state.hudApi.highlightEntity(null);
        if (state.hudApi && state.hudApi.hoverEntity) state.hudApi.hoverEntity(null);
        if (state.chipBarApi && state.chipBarApi.update) {
          state.chipBarApi.update({ selectedEntityId: null });
        }
      },
      onMarkProblem: state.correctionApi ? function () {
        var ent = findSelectedEntity();
        if (ent) state.correctionApi.openForEntity(ent);
      } : undefined,
      onReportIssue: state.correctionApi ? function (sectionKey, text) {
        state.correctionApi.openForReasoning(sectionKey, text, 0);
      } : undefined
    });
  }

  function attachCorrectionHud() {
    if (!state.correctionApi || !state.hudApi) return;
    var canvas = state.hudApi.getHudCanvas ? state.hudApi.getHudCanvas() : null;
    if (canvas) state.correctionApi.attachHudCanvas(canvas);
    var central = el("lol-central");
    var controls = central && central.querySelector("#phud-controls-host");
    if (controls) state.correctionApi.ensureMissingRegionButton(controls);
  }

  function findSelectedEntity() {
    if (!state.selectedEntityId || !state.hudEntities) return null;
    for (var i = 0; i < state.hudEntities.length; i++) {
      if (state.hudEntities[i].entity_id === state.selectedEntityId) return state.hudEntities[i];
    }
    return null;
  }

  function onChipSelect(entityId) {
    state.selectedEntityId = entityId;
    state.noAttentionRegionId = null;
    if (state.hudApi && state.hudApi.highlightEntity) {
      state.hudApi.highlightEntity(state.selectedEntityId);
    }
    if (state.chipBarApi && state.chipBarApi.update) {
      state.chipBarApi.update({ selectedEntityId: state.selectedEntityId });
    }
    if (state.envelope) refreshRightPanel();
    if (state.selectedEntityId) scrollToAttentionRecord(state.selectedEntityId);
  }

  function onCanvasEntitySelect(entityId) {
    state.selectedEntityId = entityId;
    state.noAttentionRegionId = hasAttentionRecord(entityId) ? null : entityId;
    if (state.hudApi && state.hudApi.highlightEntity) {
      state.hudApi.highlightEntity(state.selectedEntityId);
    }
    if (state.chipBarApi && state.chipBarApi.update) {
      state.chipBarApi.update({ selectedEntityId: state.selectedEntityId });
    }
    if (state.envelope) refreshRightPanel();
    var attentionHost = document.getElementById("lol-right-attention-host");
    if (attentionHost) attentionHost.scrollIntoView({ behavior: "smooth", block: "nearest" });
    if (state.selectedEntityId && hasAttentionRecord(state.selectedEntityId)) {
      scrollToAttentionRecord(state.selectedEntityId);
    }
  }

  function onChipCorrect(entityId) {
    var ent = findEntityById(entityId);
    if (ent && state.correctionApi) state.correctionApi.openForEntity(ent);
  }

  function renderObjectChipBar(entities) {
    var chipHost = el("lol-object-chip-host");
    if (!chipHost || !ChipBar()) return;
    state.chipBarApi = ChipBar().render(chipHost, entities || [], {
      selectedEntityId: state.selectedEntityId,
      attentionPkg: state.attentionPkg,
      onSelect: onChipSelect,
      onCorrect: state.correctionApi ? onChipCorrect : null,
      onHover: function (id) {
        if (state.hudApi && state.hudApi.hoverEntity) state.hudApi.hoverEntity(id);
      }
    });
  }

  function renderObjectsDrawer(panel, envelope) {
    if (!envelope) {
      panel.innerHTML = "<p class='muted'>暂无识别对象。</p>";
      return;
    }
    var hudPkg = window.PerceptionHUDView && window.PerceptionHUDView.buildAnnotationPackage(envelope);
    if (!hudPkg || !hudPkg.ok) {
      panel.innerHTML = "<p class='muted'>当前结果无法生成识别对象列表。</p>";
      return;
    }
    panel.innerHTML = "<div id='drawer-objects-host' class='lol-drawer-inner'></div>";
    var host = panel.querySelector("#drawer-objects-host");
    if (window.HudExternalAnnotationPanel) {
      window.HudExternalAnnotationPanel.render(host, hudPkg.annotation.entities, {
        selectedEntityId: state.selectedEntityId,
        onSelect: onChipSelect,
        onHover: function (id) {
          if (state.hudApi && state.hudApi.hoverEntity) state.hudApi.hoverEntity(id);
        },
        onToggleHidden: function (entityId) {
          hudPkg.annotation.entities.forEach(function (e, i) {
            if (e.entity_id === entityId) {
              e._hidden = true;
              if (hudPkg.layers[i]) hudPkg.layers[i].visible = false;
            }
          });
          if (state.hudApi && state.hudApi.redraw) state.hudApi.redraw();
          renderObjectChipBar(hudPkg.annotation.entities);
        }
      });
    }
  }

  function setViewMode(mode) {
    state.viewMode = mode;
    document.querySelectorAll(".lol-view-btn").forEach(function (btn) {
      var active = btn.dataset.view === mode;
      btn.classList.toggle("active", active);
      btn.setAttribute("aria-selected", active ? "true" : "false");
    });
    if (state.envelope) renderObservation(state.envelope);
  }

  function renderTrajectoryCanvas(container, est, gt) {
    if (!est || !est.length) { container.innerHTML = ""; return; }
    var w = 420, h = 220, pad = 24;
    var all = est.concat(gt || []);
    var xs = all.map(function (p) { return p[0]; });
    var ys = all.map(function (p) { return p[1]; });
    var minX = Math.min.apply(null, xs), maxX = Math.max.apply(null, xs);
    var minY = Math.min.apply(null, ys), maxY = Math.max.apply(null, ys);
    var spanX = maxX - minX || 1, spanY = maxY - minY || 1;
    function mapX(x) { return pad + ((x - minX) / spanX) * (w - 2 * pad); }
    function mapY(y) { return h - pad - ((y - minY) / spanY) * (h - 2 * pad); }
    function pathFromPts(pts) {
      return pts.map(function (p, i) {
        return (i === 0 ? "M" : "L") + mapX(p[0]).toFixed(1) + " " + mapY(p[1]).toFixed(1);
      }).join(" ");
    }
    var svg =
      "<svg class='traj-canvas' viewBox='0 0 " + w + " " + h + "' width='100%' height='220'>" +
      "<rect x='0' y='0' width='" + w + "' height='" + h + "' fill='#121820' rx='8'/>" +
      (gt && gt.length ? "<path d='" + pathFromPts(gt) + "' fill='none' stroke='#3ecf8e' stroke-width='2' stroke-dasharray='4 3'/>" : "") +
      "<path d='" + pathFromPts(est) + "' fill='none' stroke='#4d9fff' stroke-width='2.5'/>" +
      "<text x='" + pad + "' y='16' fill='#8b9cb3' font-size='11'>真值(绿) vs 估计(蓝)</text></svg>";
    container.innerHTML = "<div class='traj-wrap diag-panel'><h4>轨迹对比</h4>" + svg + "</div>";
  }

  function renderSegmentationBars(container, envelope) {
    var m = envelope.metrics || {};
    var perCat = m.per_category_average_score;
    if (!perCat || !Object.keys(perCat).length) {
      container.innerHTML = "<p class='muted'>分割成功率 " +
        Math.round((m.overall_success_rate || 0) * 100) + "%（" +
        (m.prompt_success_count || "—") + "/" + (m.prompt_attempt_count || "—") + " prompts）</p>";
      return;
    }
    var cats = Object.keys(perCat);
    var w = 400, barH = 18, gap = 8;
    var h = cats.length * (barH + gap) + 24;
    var svg = "<svg class='diag-canvas' viewBox='0 0 " + w + " " + h + "' width='100%'>";
    svg += "<rect width='" + w + "' height='" + h + "' fill='#121820' rx='8'/>";
    cats.forEach(function (cat, i) {
      var val = perCat[cat];
      var label = (window.LunaObservationLabelI18n && window.LunaObservationLabelI18n.mobileSamLabel)
        ? window.LunaObservationLabelI18n.mobileSamLabel(cat).replace(/候选$/, "")
        : cat.replace(/_/g, " ").slice(0, 22);
      var bw = val * (w - 140);
      var y = 12 + i * (barH + gap);
      var color = val >= 0.85 ? "#3ecf8e" : val >= 0.7 ? "#f0b429" : "#f07178";
      svg += "<text x='8' y='" + (y + 13) + "' fill='#8b9cb3' font-size='10'>" + escapeHtml(label) + "</text>";
      svg += "<rect x='130' y='" + y + "' width='" + bw.toFixed(1) + "' height='" + barH + "' fill='" + color + "' rx='4'/>";
      svg += "<text x='" + (136 + bw) + "' y='" + (y + 13) + "' fill='#e8eef6' font-size='10'>" + Math.round(val * 100) + "%</text>";
    });
    svg += "</svg>";
    container.innerHTML = "<div class='diag-panel'><h4>各类别分割得分</h4>" + svg + "</div>";
  }

  function renderMetricsDrawer(panel, envelope) {
    if (!envelope) {
      panel.innerHTML = "<p class='muted'>暂无指标数据。</p>";
      return;
    }
    var html = "<div class='lol-drawer-inner'><h3>详细指标</h3>";
    var m = envelope.metrics || {};
    html += "<dl class='kv-list metrics-human'>";
    if (m.slam) {
      var s = m.slam;
      html += "<dt>ATE</dt><dd>" + escapeHtml(String(s.ate_rmse_m)) + " m</dd>";
      html += "<dt>漂移率</dt><dd>" + escapeHtml(String(s.drift_rate)) + "</dd>";
      html += "<dt>跟踪稳定性</dt><dd>" + escapeHtml(String(Math.round((s.tracking_stability || 0) * 100))) + "%</dd>";
      html += "<dt>SLAM 综合分</dt><dd>" + escapeHtml(String(s.slam_score)) + "</dd>";
    }
    if (m.overall_success_rate != null) {
      html += "<dt>提示测试成功率</dt><dd>" + escapeHtml(String(Math.round(m.overall_success_rate * 100))) + "%</dd>";
      html += "<dt>成功 / 尝试</dt><dd>" + escapeHtml(String(m.prompt_success_count)) + " / " +
        escapeHtml(String(m.prompt_attempt_count)) + "</dd>";
    }
    if (m.muep_final_score != null) {
      html += "<dt>MUEP 综合分</dt><dd>" + escapeHtml(String(m.muep_final_score)) + "</dd>";
    }
    html += "</dl><div id='drawer-visual-host'></div></div>";
    panel.innerHTML = html;
    var vhost = panel.querySelector("#drawer-visual-host");
    var cat = envelope.model_category;
    if (cat === "slam_vio" || envelope.model_id === "orb_slam") {
      var wrap = document.createElement("div");
      wrap.className = "visual-grid";
      wrap.innerHTML = "<div id='slam-traj-host'></div><div id='slam-diag-visual-host'></div>";
      vhost.appendChild(wrap);
      var trajLayer = (envelope.visualization_layers || []).find(function (l) {
        return l.layer_type === "trajectory";
      });
      if (trajLayer) {
        renderTrajectoryCanvas(wrap.querySelector("#slam-traj-host"), trajLayer.trajectory_estimated, trajLayer.trajectory_ground_truth);
      }
      if (window.SlamDiagnosticPanels) {
        var diagHost = wrap.querySelector("#slam-diag-visual-host");
        diagHost.innerHTML = "<div id='slam-error-curve-host'></div><div id='slam-heatmap-host'></div>";
        var layers = envelope.visualization_layers || [];
        var diag = envelope.diagnostics || {};
        var diagInner = diag.diagnostics || {};
        var errorCurve = (layers.find(function (l) { return l.layer_type === "error_curve"; }) || {}).error_curve || diagInner.error_curve;
        var heatmap = (layers.find(function (l) { return l.layer_type === "drift_heatmap"; }) || {}).drift_heatmap || diagInner.drift_heatmap;
        if (!errorCurve && trajLayer) {
          errorCurve = [];
          var est = trajLayer.trajectory_estimated, gt = trajLayer.trajectory_ground_truth;
          var n = Math.min((est || []).length, (gt || []).length);
          for (var i = 0; i < n; i++) {
            var dx = est[i][0] - gt[i][0], dy = est[i][1] - gt[i][1];
            errorCurve.push({ t: i * 0.1, error: Math.sqrt(dx * dx + dy * dy) });
          }
        }
        window.SlamDiagnosticPanels.renderErrorCurvePanel(diagHost.querySelector("#slam-error-curve-host"), errorCurve || []);
        window.SlamDiagnosticPanels.renderDriftHeatmapPanel(diagHost.querySelector("#slam-heatmap-host"), heatmap || [], trajLayer);
      }
      return;
    }
    if (cat === "segmentation" || envelope.model_id === "mobile_sam") {
      renderSegmentationBars(vhost, envelope);
    }
  }

  function renderAdvancedDrawer(panel) {
    panel.innerHTML =
      "<div class='lol-drawer-inner'><h3>高级流程</h3>" +
      "<p class='muted'>Manifest / Job / Runner Bridge — 仅供技术流程使用。</p>" +
      "<div id='drawer-advanced-mount'></div></div>";
    var mount = panel.querySelector("#drawer-advanced-mount");
    var importHost = el("local-asset-import-host");
    var bridgeHost = el("runner-bridge-host");
    if (mount && importHost) mount.appendChild(importHost);
    if (mount && bridgeHost) mount.appendChild(bridgeHost);
  }

  function renderDeveloperDrawer(panel, envelope) {
    if (!envelope) {
      panel.innerHTML = "<p class='muted'>暂无 envelope 数据。</p>";
      return;
    }
    var st = state.importApi ? state.importApi.getState() : {};
    panel.innerHTML =
      "<div class='lol-drawer-inner'><h3>开发者数据</h3>" +
      "<details class='raw-json-block'><summary>原始 JSON envelope</summary>" +
      "<pre class='raw-json-pre'>" + escapeHtml(JSON.stringify(envelope, null, 2)) + "</pre></details>" +
      (st.manifest ? "<details class='raw-json-block'><summary>Manifest</summary><pre class='raw-json-pre'>" +
        escapeHtml(JSON.stringify(st.manifest, null, 2)) + "</pre></details>" : "") +
      (st.jobRequest ? "<details class='raw-json-block'><summary>Job Request</summary><pre class='raw-json-pre'>" +
        escapeHtml(JSON.stringify(st.jobRequest, null, 2)) + "</pre></details>" : "") +
      (st.runnerBridge ? "<details class='raw-json-block'><summary>Runner Bridge</summary><pre class='raw-json-pre'>" +
        escapeHtml(JSON.stringify(st.runnerBridge, null, 2)) + "</pre></details>" : "") +
      "<dl class='kv-list'><dt>phase_ref</dt><dd><code>" + escapeHtml(envelope.phase_ref || "—") + "</code></dd></dl>" +
      "</div>";
  }

  function renderTestBoardDrawer(panel, envelope) {
    if (!envelope) {
      panel.innerHTML = "<p class='muted'>暂无测试记录引用。</p>";
      return;
    }
    var refs = envelope.test_board_refs || [];
    var html = "<div class='lol-drawer-inner'><h3>测试记录</h3><ul class='ref-list'>";
    refs.forEach(function (ref) {
      html += "<li><code>" + escapeHtml(ref) + "</code></li>";
    });
    if (!refs.length) html += "<li class='muted'>—</li>";
    html += "</ul></div>";
    panel.innerHTML = html;
  }

  function renderObservation(envelope) {
    var central = el("lol-central");
    var right = el("lol-right-panel");
    if (!central || !Compact()) return;

    var pkg = window.ModelInsightLayer.buildInsightPackage(envelope);
    var reasoning = Compact().getReasoning(envelope);

    var viewMode = state.viewMode;
    if (viewMode === "hud" && window.PerceptionHUDView && !window.PerceptionHUDView.supportsHUD(envelope)) {
      viewMode = "compare";
    }

    var hudOptions = {
      attentionPkg: state.attentionPkg,
      onCanvasEntitySelect: onCanvasEntitySelect,
      onEntitiesChange: function (entities) {
        state.hudEntities = entities;
        refreshAttentionUi(entities);
      },
      onHudCanvasReady: function (canvas, controlsHost) {
        if (state.correctionApi) {
          state.correctionApi.attachHudCanvas(canvas);
          if (controlsHost) state.correctionApi.ensureMissingRegionButton(controlsHost);
        }
      }
    };

    if (state.hudApi && state.hudApi.destroy) state.hudApi.destroy();
    state.hudApi = Compact().renderCentral(central, envelope, viewMode, state.debugMode, hudOptions);
    refreshRightPanel();
    attachCorrectionHud();

    if (viewMode !== "hud") {
      state.hudEntities = null;
      state.attentionPkg = null;
      state.queuePkg = null;
      state.requestPkg = null;
      renderObjectChipBar([]);
    }

    if (state.dockApi) {
      var summary = Compact().buildMetricsSummary(
        envelope, pkg, state.attentionPkg, state.queuePkg, state.requestPkg,
        state.executionPkg, state.resultPkg, state.ocrPkg, state.dualRoutePkg,
        state.activationPkg, state.situationPkg, state.agentPlanningPkg
      );
      state.dockApi.setSummary(summary);
      state.dockApi._lastSummary = summary;
    }
  }

  function renderEmptyObservation() {
    var central = el("lol-central");
    var right = el("lol-right-panel");
    state.selectedEntityId = null;
    state.noAttentionRegionId = null;
    state.hudEntities = null;
    if (Compact()) {
      Compact().renderCentralEmpty(central);
      Compact().renderPlaceholderRight(right);
    }
    renderObjectChipBar([]);
    if (state.dockApi) {
      state.dockApi.setSummary("<span class='muted'>等待观察结果…</span>");
    }
  }

  function renderEnvelope(data) {
    data = enrichEnvelopeSceneAware(data);
    state.envelope = data;
    if (window.RunnerManualTriggerRequestState) {
      state.requestStore = window.RunnerManualTriggerRequestState.createStore();
      state.requestPkg = null;
    }
    if (window.ControlledRunnerExecutionState) {
      state.executionStore = window.ControlledRunnerExecutionState.createStore();
      state.executionPkg = null;
    }
    if (window.ResultLayerState) {
      state.resultStore = window.ResultLayerState.createStore();
      state.resultPkg = null;
    }
    if (window.MobileSamOcrRequestState) {
      state.ocrStore = window.MobileSamOcrRequestState.createStore();
      state.ocrPkg = null;
    }
    var v = validateEnvelope(data);
    if (!v.ok) {
      setLoadStatus("无法读取测试结果: " + v.error, "error");
      renderEmptyObservation();
      return;
    }

    var pkg = window.ModelInsightLayer.buildInsightPackage(data);
    state.capabilityId = capabilityFromEnvelope(data);
    setLoadStatus("已加载 · " + pkg.modelDisplayName + " · " + pkg.verdict.statusLabel, "ok");
    renderLeftRail();
    renderObservation(data);
  }

  function loadLocalJsonFile(file) {
    var reader = new FileReader();
    reader.onload = function (ev) {
      try {
        var data = JSON.parse(ev.target.result);
        data._source_file_ref = file.name || "local://" + file.name;
        renderEnvelope(data);
      } catch (e) {
        setLoadStatus("JSON parse error: " + e.message, "error");
      }
    };
    reader.readAsText(file);
  }

  function loadBuiltinExample() {
    state.capabilityId = "segmentation";
    renderEnvelope(BUILTIN_MOBILE_SAM_EXAMPLE);
    renderLeftRail();
  }

  function loadBuiltinSlamExample() {
    state.capabilityId = "slam";
    renderEnvelope(BUILTIN_SLAM_EXAMPLE);
    renderLeftRail();
  }

  function onImportStateChange() {
    if (state.importApi && state.importApi.runnerBridge) {
      state.importApi.runnerBridge.renderRunnerStatus(state.importApi.getState());
    }
  }

  function applyWorkflowArtifacts(artifacts) {
    if (!state.importApi || !artifacts) return;
    var st = state.importApi.getState();
    Object.keys(artifacts).forEach(function (k) {
      if (artifacts[k] !== undefined) st[k] = artifacts[k];
    });
    onImportStateChange();
  }

  function toggleAdvancedDrawer() {
    state.advancedDrawerOpen = !state.advancedDrawerOpen;
    if (state.dockApi) {
      if (state.advancedDrawerOpen) state.dockApi.openDrawer("advanced");
      else state.dockApi.closeDrawer();
    }
  }

  function toggleDeveloperMode() {
    state.debugMode = !state.debugMode;
    document.body.classList.toggle("debug-mode", state.debugMode);
    document.body.dataset.userMode = state.debugMode ? "developer" : "simple";
    if (state.envelope) renderObservation(state.envelope);
    if (state.debugMode && state.dockApi) state.dockApi.openDrawer("developer");
  }

  function init() {
    if (window.BrowserRuntimeGuard && window.BrowserRuntimeGuard.assertAppEntryUsesWindow) {
      window.BrowserRuntimeGuard.assertAppEntryUsesWindow();
    }
    document.body.dataset.modelExecutionAllowed = "false";
    document.body.dataset.runtimeAllowed = "false";
    document.body.dataset.candidateOnly = "true";

    if (CanvasLayout()) CanvasLayout().apply(el("lol-app"));

    var titleEl = el("lol-title");
    var subEl = el("lol-subtitle");
    if (titleEl) titleEl.textContent = Copy().title || "Luna 观察镜";
    if (subEl) subEl.textContent = Copy().subtitle;
    var bCand = el("lol-badge-candidate");
    var bRt = el("lol-badge-runtime");
    if (bCand) bCand.textContent = Copy().statusCandidate || "候选结果";
    if (bRt) bRt.textContent = Copy().statusNonRuntime || "非运行态";

    renderLeftRail();
    renderEmptyObservation();

    var importUi = null;
    var runnerUi = null;
    var advHost = el("advanced-workflow");
    if (window.LocalAssetImportUI && window.RunnerBridgeUI && advHost) {
      importUi = window.LocalAssetImportUI.init({
        rootEl: advHost.querySelector("#local-asset-import-host"),
        onStateChange: onImportStateChange,
        advancedOnly: true
      });
      runnerUi = window.RunnerBridgeUI.init({
        rootEl: advHost.querySelector("#runner-bridge-host"),
        getImportState: function () { return importUi.getState(); },
        onStateChange: onImportStateChange,
        advancedOnly: true
      });
      state.importApi = { getState: importUi.getState, runnerBridge: runnerUi };
    }

    if (window.SimpleModeUI && window.SimpleModeUI.initHeadless) {
      state.simpleController = window.SimpleModeUI.initHeadless({
        onEnvelope: function (envelope) {
          renderEnvelope(envelope);
          setViewMode("hud");
        },
        onWorkflowArtifacts: applyWorkflowArtifacts,
        onServiceStatus: function (ok) {
          setServiceStatus(ok);
          updateStartButton();
        },
        onFailure: function (msg) {
          setLoadStatus(msg, "error");
        },
        onSlamLimitedNotice: function () {}
      });
    }

    var dockHost = el("lol-bottom-dock");
    if (dockHost && BottomDrawers()) {
      state.dockApi = BottomDrawers().renderBottomDock(dockHost, {
        renderMetrics: function (panel) { renderMetricsDrawer(panel, state.envelope); },
        renderObjects: function (panel) { renderObjectsDrawer(panel, state.envelope); },
        renderAdvanced: renderAdvancedDrawer,
        renderDeveloper: function (panel) { renderDeveloperDrawer(panel, state.envelope); },
        renderTestBoard: function (panel) { renderTestBoardDrawer(panel, state.envelope); },
        renderCorrection: function (panel) {
          if (state.correctionApi) state.correctionApi.renderDrawer(panel);
        }
      });
    }

    if (CorrectionUI()) {
      state.correctionApi = CorrectionUI().init({
        getEnvelope: function () { return state.envelope; },
        getEntities: function () { return state.hudEntities || []; },
        onEntitySelect: onChipSelect,
        onRecordsChange: function () {
          refreshAttentionUi(state.hudEntities);
        }
      });
    }

    if (window.LunaTopbarCompactActions) {
      window.LunaTopbarCompactActions.init({
        onAdvanced: toggleAdvancedDrawer,
        onDeveloper: toggleDeveloperMode,
        onTestBoard: function () { if (state.dockApi) state.dockApi.openDrawer("testboard"); },
        onWhitebox: function () { if (state.dockApi) state.dockApi.openDrawer("whitebox"); }
      });
    }

    el("lol-file-input").addEventListener("change", function (ev) {
      var file = ev.target.files && ev.target.files[0];
      if (file && state.simpleController) {
        state.simpleController.setFile(file);
        renderLeftRail();
        updateStartButton();
      }
    });

    el("lol-start-btn").addEventListener("click", function () {
      if (!state.simpleController) return;
      setLoadStatus("正在观察…", "");
      state.simpleController.startTest().catch(function () {});
    });

    el("lol-json-input").addEventListener("change", function (ev) {
      var file = ev.target.files && ev.target.files[0];
      if (file) loadLocalJsonFile(file);
    });

    document.querySelectorAll(".lol-view-btn").forEach(function (btn) {
      btn.addEventListener("click", function () { setViewMode(btn.dataset.view); });
    });

    var recheckBtn = el("lol-recheck-service");
    if (recheckBtn) recheckBtn.addEventListener("click", recheckService);

    var rightPanel = el("lol-right-panel");
    if (rightPanel && !rightPanel._ocrCollabBound) {
      rightPanel.addEventListener("click", onOcrCollabPanelClick);
      rightPanel._ocrCollabBound = true;
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.ModelTestLens = {
    BUILTIN_MOBILE_SAM_EXAMPLE: BUILTIN_MOBILE_SAM_EXAMPLE,
    BUILTIN_SLAM_EXAMPLE: BUILTIN_SLAM_EXAMPLE,
    validateEnvelope: validateEnvelope,
    loadBuiltinExample: loadBuiltinExample,
    loadBuiltinSlamExample: loadBuiltinSlamExample,
    renderEnvelopeFromService: renderEnvelope,
    switchToHUDView: function () { setViewMode("hud"); },
    switchToCompareView: function () { setViewMode("compare"); }
  };
})();

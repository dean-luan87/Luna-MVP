/**
 * Followup Runner Route — build runner_task_candidate queue from Observation Attention.
 * Planning-aligned mapping; no runner execution, no fact write.
 */
(function (global) {
  "use strict";

  var AttnCopy = function () { return global.ObservationAttentionCopy || {}; };
  var RouteCopy = function () { return global.FollowupRunnerRouteCopy || {}; };

  var PRIORITY_MAP = {
    P0_immediate_attention: "P0",
    P1_high_attention: "P1",
    P2_medium_attention: "P2",
    P3_low_attention: "P3",
    ignore_for_now: "P3"
  };

  var ADMISSION = {
    P0_immediate_attention: "auto_eligible",
    P1_high_attention: "auto_eligible",
    P2_medium_attention: "manual_only",
    P3_low_attention: "manual_only",
    ignore_for_now: "rejected"
  };

  var ROUTE_REASON = {
    detection: "confirm_object_category",
    ocr: "read_text",
    tracking: "track_dynamic_object",
    depth: "estimate_distance",
    slam: "verify_walkable_structure",
    slam_reference: "use_as_slam_reference",
    motion_analysis: "check_motion",
    walkable_area_review: "verify_walkable_area",
    human_review: "validate_human_correction"
  };

  var ROUTE_REASON_ZH = {
    confirm_object_category: "标签不确定，建议检测复核类别",
    read_text: "疑似文字区域，建议 OCR 候选复核",
    track_dynamic_object: "动态/需跟踪复核，建议跟踪候选",
    estimate_distance: "结构候选，建议深度估计",
    verify_walkable_structure: "道路/可通行结构，建议深度与 SLAM 复核",
    use_as_slam_reference: "稳定结构，建议作为 SLAM 参考",
    check_motion: "运动状态候选，建议运动分析",
    verify_walkable_area: "可通行区域候选复核",
    validate_human_correction: "人工指错加权，建议复核（非 ground truth）"
  };

  function motionReasonZh(record) {
    var c = AttnCopy();
    var motion = (c.motionState || {})[record.motion_state_candidate] || record.motion_state_candidate;
    if (record.motion_state_candidate === "scene_structure_candidate") {
      return "结构候选，建议深度与 SLAM 复核";
    }
    if (record.motion_state_candidate === "needs_tracking_review") {
      return "需跟踪复核，建议跟踪与检测候选";
    }
    if (record.ocr_required) return "静态文字候选，建议 OCR 复核";
    return motion + "，" + (record.attention_summary || "");
  }

  function resolveQueueState(task, store) {
    var ov = store && store.getOverride ? store.getOverride(task.runner_task_candidate_id) : null;
    if (ov && ov.queue_state) return ov.queue_state;
    if (task.admission_mode === "manual_only") return "manual_only";
    if (task.admission_mode === "rejected") return "blocked_by_policy";
    return "candidate";
  }

  function isActiveInQueue(task) {
    var st = task.queue_state;
    if (st === "excluded" || st === "blocked_by_policy") return false;
    if (task.admission_mode === "auto_eligible" && (st === "candidate" || st === "pinned")) return true;
    if (task.admission_mode === "manual_only" && st === "pinned") return true;
    return false;
  }

  function buildFromAttention(attentionPkg, entities, store) {
    if (!attentionPkg || !attentionPkg.records || !attentionPkg.records.length) {
      return { tasks: [], stats: { auto_eligible: 0, manual_only: 0, pinned: 0, excluded: 0, active: 0 } };
    }

    var entityMap = {};
    (entities || []).forEach(function (e) { entityMap[e.entity_id] = e; });

    var tasks = [];
    var seq = 1;
    var dedupe = {};

    attentionPkg.records.forEach(function (rec) {
      if (rec.priority_level === "ignore_for_now") return;
      var admission = ADMISSION[rec.priority_level] || "manual_only";
      if (admission === "rejected") return;

      var models = (rec.recommended_followup_model || []).filter(function (m) {
        return m && m !== "no_followup_required";
      });
      if (!models.length) return;

      var ent = entityMap[rec.region_id];
      var regionLabel = (ent && ent.hud_short_label) || rec.region_display_name || rec.region_id;
      var pri = PRIORITY_MAP[rec.priority_level] || "P2";
      var followRef = rec.followup_route_refs || [];

      models.forEach(function (modelId, idx) {
        var dedupeKey = rec.region_id + "|" + modelId;
        if (dedupe[dedupeKey]) return;
        dedupe[dedupeKey] = true;

        var rtcId = "rtc_" + modelId + "_" + rec.region_id;
        var reasonKey = ROUTE_REASON[modelId] || "confirm_object_category";
        var routeReason = ROUTE_REASON_ZH[reasonKey] || motionReasonZh(rec);

        var task = {
          task_candidate_id: "T-" + String(seq).padStart(3, "0"),
          runner_task_candidate_id: rtcId,
          source_attention_record_id: rec.attention_record_id,
          linked_attention_record_id: rec.attention_record_id,
          source_region_id: rec.region_id,
          region_id: rec.region_id,
          region_display_name: regionLabel,
          priority_level: rec.priority_level,
          task_priority: pri,
          recommended_runner_type: modelId,
          target_model_id: modelId,
          route_reason: routeReason,
          route_reason_key: reasonKey,
          source_followup_route_ref: followRef[idx] || ("route_" + modelId + "_" + rec.region_id),
          admission_mode: admission,
          motion_state_candidate: rec.motion_state_candidate,
          correction_boosted: !!rec._correction_boosted,
          trigger_mode: "manual_only",
          runner_task_candidate_only: true,
          not_runner_execution: true,
          not_executed: true,
          not_fact: true,
          candidate_only: true
        };
        task.queue_state = resolveQueueState(task, store);
        task.in_active_queue = isActiveInQueue(task);
        tasks.push(task);
        seq += 1;
      });
    });

    var stats = { auto_eligible: 0, manual_only: 0, pinned: 0, excluded: 0, active: 0 };
    tasks.forEach(function (t) {
      if (t.admission_mode === "auto_eligible") stats.auto_eligible += 1;
      if (t.admission_mode === "manual_only") stats.manual_only += 1;
      if (t.queue_state === "pinned") stats.pinned += 1;
      if (t.queue_state === "excluded") stats.excluded += 1;
      if (t.in_active_queue) stats.active += 1;
    });

    return {
      candidate_only: true,
      not_runner_execution: true,
      not_executed: true,
      tasks: tasks,
      active_tasks: tasks.filter(function (t) { return t.in_active_queue; }),
      manual_pool: tasks.filter(function (t) {
        return t.admission_mode === "manual_only" && t.queue_state !== "pinned" && t.queue_state !== "excluded";
      }),
      excluded_tasks: tasks.filter(function (t) { return t.queue_state === "excluded"; }),
      stats: stats
    };
  }

  function formatRunnerLabel(modelId) {
    var c = AttnCopy();
    return (c.followupModel || {})[modelId] || modelId;
  }

  function groupRunnersForRegion(tasks, regionId) {
    var ids = [];
    tasks.forEach(function (t) {
      if (t.region_id === regionId && t.in_active_queue) ids.push(formatRunnerLabel(t.target_model_id));
    });
    return ids.join(" / ");
  }

  global.FollowupRunnerRouteQueue = {
    version: "followup_runner_route_queue_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-UI-Queue-Execution-And-Post-Review-v1-001",
    noRunnerExecution: true,
    noModelCall: true,
    noAutoRunnerTrigger: true,
    buildFromAttention: buildFromAttention,
    formatRunnerLabel: formatRunnerLabel,
    groupRunnersForRegion: groupRunnersForRegion,
    isActiveInQueue: isActiveInQueue
  };
})(typeof window !== "undefined" ? window : this);

/**
 * Runner Manual Trigger — build runner_invocation_request from pinned task. No runner call.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.RunnerManualTriggerCopy || {}; };

  var RUNNER_TYPE_MAP = {
    detection: "Detection",
    ocr: "OCR"
  };

  var SCOPED_MODELS = ["detection", "ocr"];

  function canGenerateRequest(task, store) {
    var c = Copy();
    if (!task) return { ok: false, hint: c.hintBlocked };
    if (task.queue_state === "excluded") return { ok: false, hint: c.hintExcluded };
    if (task.queue_state === "blocked_by_policy") return { ok: false, hint: c.hintBlocked };
    if (task.queue_state === "stale_candidate") return { ok: false, hint: c.hintStale };
    if (task.queue_state !== "pinned") {
      return { ok: false, hint: c.hintNeedPin };
    }
    if (SCOPED_MODELS.indexOf(task.target_model_id) < 0) {
      return { ok: false, hint: c.hintNotDetectionOcr };
    }
    if (task.target_model_id === "detection" && task.recommended_runner_type !== "detection") {
      return { ok: false, hint: c.hintRouteMismatch };
    }
    if (task.target_model_id === "ocr" && task.recommended_runner_type !== "ocr") {
      return { ok: false, hint: c.hintRouteMismatch };
    }
    if (store && store.findActiveByRtc && store.findActiveByRtc(task.runner_task_candidate_id)) {
      return { ok: false, hint: c.hintDuplicate };
    }
    return { ok: true };
  }

  function generateHintForTask(task) {
    return canGenerateRequest(task, null).hint || "";
  }

  function buildTraceChain(task, rirId) {
    return [
      { stage: "segmentation_region", ref: task.region_id || task.source_region_id },
      { stage: "observation_attention_record", ref: task.linked_attention_record_id || task.source_attention_record_id },
      { stage: "followup_model_route_candidate", ref: task.source_followup_route_ref },
      { stage: "runner_task_candidate", ref: task.runner_task_candidate_id, queue_state: "pinned" },
      { stage: "runner_invocation_request", ref: rirId }
    ];
  }

  function buildFromPinnedTask(task, envelope, store, options) {
    options = options || {};
    var check = canGenerateRequest(task, store);
    if (!check.ok) return { ok: false, error: check.hint };

    var modelId = task.target_model_id;
    var runnerType = RUNNER_TYPE_MAP[modelId];
    var seq = store && store.nextSeq ? store.nextSeq() : 1;
    var rirId = "rir_" + modelId + "_" + task.region_id + "_" + String(seq).padStart(3, "0");
    var envRef = (envelope && (envelope.envelope_id || envelope._source_file_ref)) || "local://envelope";

    var request = {
      invocation_request_id: rirId,
      source_runner_task_candidate_id: task.runner_task_candidate_id,
      source_region_id: task.region_id,
      source_attention_record_id: task.linked_attention_record_id,
      source_followup_model_route_candidate_id: task.source_followup_route_ref,
      source_envelope_ref: envRef,
      requested_runner_type: runnerType,
      source_target_model_id: modelId,
      requested_by: options.developerMode ? "developer_test_trigger" : "manual_user_trigger",
      trigger_mode: "manual_only",
      admission_status: "pending_admission",
      execution_status: "not_executed",
      input_payload_ref: envRef,
      region_geometry_ref: "region://" + task.region_id,
      route_reason: task.route_reason,
      source_queue_state_at_request: "pinned",
      trace_chain: buildTraceChain(task, rirId),
      candidate_only: true,
      not_fact: true,
      not_executed: true,
      no_navigation_decision: true,
      invocation_request_only: true,
      not_runner_execution: true,
      correction_boosted: !!task.correction_boosted,
      region_display_name: task.region_display_name,
      created_at: new Date().toISOString()
    };

    return { ok: true, request: request };
  }

  function buildPackage(store) {
    var list = store && store.getAll ? store.getAll() : [];
    var stats = { pending: 0, admitted: 0, rejected: 0, cancelled: 0, executed: 0, total: list.length };
    list.forEach(function (r) {
      if (r.admission_status === "pending_admission") stats.pending += 1;
      else if (r.admission_status === "admitted") stats.admitted += 1;
      else if (r.admission_status === "rejected") stats.rejected += 1;
      else if (r.admission_status === "cancelled") stats.cancelled += 1;
      if (r.execution_status === "executed") stats.executed += 1;
    });
    return {
      requests: list,
      active_requests: list.filter(function (r) {
        return r.admission_status !== "cancelled";
      }),
      stats: stats,
      candidate_only: true,
      not_runner_execution: true,
      execution_status_not_executed_only: stats.executed === 0
    };
  }

  function getGenerateButtonLabel(modelId) {
    var c = Copy();
    if (modelId === "detection") return c.generateDetectionBtn;
    if (modelId === "ocr") return c.generateOcrBtn;
    return c.sendToAdmissionBtn;
  }

  global.RunnerManualTriggerRequest = {
    version: "runner_manual_trigger_request_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Runner-Manual-Trigger-UI-Execution-And-Post-Review-v1-001",
    noRunnerExecution: true,
    noModelCall: true,
    noAutoRunnerTrigger: true,
    SCOPED_MODELS: SCOPED_MODELS,
    canGenerateRequest: canGenerateRequest,
    generateHintForTask: generateHintForTask,
    buildFromPinnedTask: buildFromPinnedTask,
    buildPackage: buildPackage,
    getGenerateButtonLabel: getGenerateButtonLabel
  };
})(typeof window !== "undefined" ? window : this);

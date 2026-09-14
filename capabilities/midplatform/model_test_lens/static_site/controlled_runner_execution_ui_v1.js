/**
 * Controlled Runner Execution — build execution candidate from admitted request. No runner call.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.ControlledRunnerExecutionCopy || {}; };

  var POLICY_REFS = {
    detection_crop: "schemas/controlled_runner_execution/detection_controlled_execution_input_policy_v1.json",
    ocr_crop: "schemas/controlled_runner_execution/ocr_controlled_execution_input_policy_v1.json",
    output_envelope: "schemas/controlled_runner_execution/runner_output_envelope_policy_v1.json",
    error: "schemas/controlled_runner_execution/runner_error_policy_v1.json",
    timeout: "schemas/controlled_runner_execution/runner_error_policy_v1.json#timeout"
  };

  var RUNNER_CONFIG_REFS = {
    Detection: "runner_config/detection_manual_controlled_v1.json",
    OCR: "runner_config/ocr_manual_controlled_v1.json",
    Segmentation: "runner_config/mobile_sam_manual_controlled_v1.json",
    MobileSAM: "runner_config/mobile_sam_manual_controlled_v1.json"
  };

  var MOBILE_SAM_POLICY = {
    crop: "schemas/mobile_sam_single_model_execution/mobile_sam_controlled_execution_input_policy_v1.json",
    output: "schemas/mobile_sam_single_model_execution/segmentation_result_envelope_schema_v1.json"
  };

  var OUTPUT_ENVELOPE_TYPES = {
    Detection: "detection_result_candidate",
    OCR: "ocr_text_candidate"
  };

  function canGenerateExecutionCandidate(request, executionStore) {
    var c = Copy();
    if (!request) return { ok: false, hint: c.hintNeedAdmitted };
    if (request.admission_status === "cancelled") return { ok: false, hint: c.hintCancelled };
    if (request.admission_status === "rejected") return { ok: false, hint: c.hintRejected };
    if (request.admission_status === "pending_admission") return { ok: false, hint: c.hintPending };
    if (!request.admission_result || request.admission_result.admission_decision !== "admitted") {
      return { ok: false, hint: c.hintNeedAdmitted };
    }
    if (request.execution_status !== "not_executed") return { ok: false, hint: c.hintNeedAdmitted };
    if (executionStore && executionStore.findActiveByRir &&
        executionStore.findActiveByRir(request.invocation_request_id)) {
      return { ok: false, hint: c.hintDuplicate };
    }
    return { ok: true };
  }

  function buildTraceChain(request, admissionResult, crecId) {
    var chain = (request.trace_chain || []).slice();
    if (admissionResult && admissionResult.admission_result_id) {
      chain.push({
        stage: "runner_invocation_admission",
        ref: admissionResult.admission_result_id
      });
    }
    chain.push({ stage: "controlled_runner_execution_candidate", ref: crecId });
    return chain;
  }

  function buildInputReview(candidate, request, task) {
    var runnerType = candidate.requested_runner_type;
    var regionId = candidate.source_region_id;
    var reason = (task && task.route_reason) || request.route_reason || "—";
    var cropRef = candidate.input_payload_ref;
    var base = {
      region_id: regionId,
      source_attention: request.source_attention_record_id || "Observation Attention",
      reason: reason,
      image_crop_ref: cropRef,
      forbidden_inputs: []
    };
    if (runnerType === "Detection") {
      return {
        title: Copy().detectionCandidateTitle,
        region_label: "region_id=" + regionId,
        source_label: "Observation Attention",
        reason_label: reason,
        input_label: "image crop reference · " + cropRef,
        allowed_inputs: ["region_crop", "region_geometry_ref", "source_image_ref", "prompt_label_candidate"],
        forbidden_inputs: [
          "fact label", "confirmed object name", "navigation context",
          "confirmed_dynamic", "prompt_label as truth"
        ],
        not_fact: true,
        candidate_only: true
      };
    }
    return {
      title: Copy().ocrCandidateTitle,
      region_label: "text-likely region · " + regionId,
      source_label: "Observation Attention",
      reason_label: reason,
      input_label: "image crop reference · " + cropRef,
      allowed_inputs: ["region_crop", "text_likely_region_ref", "ocr_target_reason"],
      forbidden_inputs: [
        "预填真实文字", "fact text", "human correction as ground truth",
        "preset real text", "navigation context"
      ],
      human_correction_note: request.correction_boosted
        ? "人工修正仅作 priority signal，非 ground truth"
        : null,
      not_fact: true,
      candidate_only: true
    };
  }

  function buildFromAdmittedRequest(request, sourceTask, envelope, executionStore, options) {
    options = options || {};
    var check = canGenerateExecutionCandidate(request, executionStore);
    if (!check.ok) return { ok: false, error: check.hint };

    var admission = request.admission_result;
    if (!admission || admission.admission_decision !== "admitted") {
      return { ok: false, error: Copy().hintNeedAdmitted };
    }

    var runnerType = request.requested_runner_type;
    var modelKey = runnerType === "Detection" ? "detection" : "ocr";
    var seq = executionStore && executionStore.nextSeq ? executionStore.nextSeq() : 1;
    var crecId = "crec_" + modelKey + "_" + request.source_region_id + "_" + String(seq).padStart(3, "0");
    var envRef = (envelope && (envelope.envelope_id || envelope._source_file_ref)) ||
      request.source_envelope_ref || "local://envelope";
    var cropPolicy = runnerType === "Detection" ? POLICY_REFS.detection_crop : POLICY_REFS.ocr_crop;

    var candidate = {
      execution_candidate_id: crecId,
      source_invocation_request_id: request.invocation_request_id,
      source_admission_result_id: admission.admission_result_id,
      source_runner_task_candidate_id: request.source_runner_task_candidate_id,
      source_region_id: request.source_region_id,
      source_attention_record_id: request.source_attention_record_id,
      source_followup_model_route_candidate_id: request.source_followup_model_route_candidate_id,
      requested_runner_type: runnerType,
      execution_mode: "manual_controlled",
      execution_status: "planned_only",
      input_region_ref: "region://" + request.source_region_id,
      input_payload_ref: envRef + "#crop/" + request.source_region_id,
      crop_policy_ref: cropPolicy,
      runner_config_ref: RUNNER_CONFIG_REFS[runnerType],
      output_envelope_schema_ref: POLICY_REFS.output_envelope,
      output_envelope_type: OUTPUT_ENVELOPE_TYPES[runnerType],
      timeout_policy_ref: POLICY_REFS.timeout,
      error_policy_ref: POLICY_REFS.error,
      admission_decision_at_create: "admitted",
      trace_chain: buildTraceChain(request, admission, crecId),
      input_review: null,
      region_display_name: request.region_display_name,
      route_reason: request.route_reason,
      correction_boosted: !!request.correction_boosted,
      candidate_only: true,
      not_executed: true,
      not_fact: true,
      no_navigation_decision: true,
      execution_candidate_only: true,
      not_runner_execution: true,
      needs_fact_admission_for_any_fact_write: true,
      execution_candidate_not_runner_execution: true,
      execution_candidate_not_model_output: true,
      created_at: new Date().toISOString()
    };

    candidate.input_review = buildInputReview(candidate, request, sourceTask);
    return { ok: true, candidate: candidate };
  }

  function buildMobileSamFromAdmittedRequest(request, sourceTask, envelope, executionStore, options) {
    options = options || {};
    var check = canGenerateExecutionCandidate(request, executionStore);
    if (!check.ok) return { ok: false, error: check.hint };
    var admission = request.admission_result;
    if (!admission || admission.admission_decision !== "admitted") {
      return { ok: false, error: Copy().hintNeedAdmitted };
    }
    var seq = executionStore && executionStore.nextSeq ? executionStore.nextSeq() : 1;
    var crecId = "crec_segmentation_" + request.source_region_id + "_" + String(seq).padStart(3, "0");
    var envRef = (envelope && (envelope.envelope_id || envelope._source_file_ref)) ||
      request.source_envelope_ref || "local://envelope";
    var imageRef = "";
    if (envelope && envelope.input_asset_refs && envelope.input_asset_refs.length) {
      imageRef = "local-file://" + envelope.input_asset_refs[0];
    }
    var candidate = {
      execution_candidate_id: crecId,
      source_invocation_request_id: request.invocation_request_id,
      source_admission_result_id: admission.admission_result_id,
      source_runner_task_candidate_id: request.source_runner_task_candidate_id,
      source_region_id: request.source_region_id,
      source_attention_record_id: request.source_attention_record_id,
      source_followup_model_route_candidate_id: request.source_followup_model_route_candidate_id,
      requested_runner_type: "Segmentation",
      model_id: "mobile_sam",
      execution_mode: "manual_controlled",
      execution_status: "planned_only",
      input_region_ref: "region://" + request.source_region_id,
      input_payload_ref: imageRef || (envRef + "#crop/" + request.source_region_id),
      crop_policy_ref: MOBILE_SAM_POLICY.crop,
      runner_config_ref: RUNNER_CONFIG_REFS.Segmentation,
      output_envelope_schema_ref: MOBILE_SAM_POLICY.output,
      output_envelope_type: "segmentation_result_envelope",
      timeout_policy_ref: POLICY_REFS.timeout,
      error_policy_ref: POLICY_REFS.error,
      admission_decision_at_create: "admitted",
      trace_chain: buildTraceChain(request, admission, crecId),
      region_display_name: request.region_display_name,
      route_reason: request.route_reason || "mobile_sam_segmentation_rerun",
      correction_boosted: !!request.correction_boosted,
      candidate_only: true,
      not_executed: true,
      not_fact: true,
      no_navigation_decision: true,
      execution_candidate_only: true,
      mobile_sam_controlled_execution: true,
      needs_fact_admission_for_any_fact_write: true,
      created_at: new Date().toISOString()
    };
    return { ok: true, candidate: candidate };
  }

  function isMobileSamCandidate(candidate) {
    if (!candidate) return false;
    var cfg = candidate.runner_config_ref || "";
    return candidate.requested_runner_type === "Segmentation" ||
      candidate.model_id === "mobile_sam" || cfg.indexOf("mobile_sam") >= 0;
  }

  function canRunControlledMobileSam(candidate) {
    if (!isMobileSamCandidate(candidate)) return false;
    if (candidate.execution_status === "cancelled" || candidate.execution_status === "blocked") return false;
    return candidate.execution_status === "ready_for_execution_review" ||
      candidate.execution_status === "planned_only";
  }

  function buildPackage(executionStore) {
    var list = executionStore && executionStore.getAll ? executionStore.getAll() : [];
    var stats = {
      planned_only: 0,
      ready_for_execution_review: 0,
      cancelled: 0,
      blocked: 0,
      total: list.length
    };
    list.forEach(function (c) {
      if (c.execution_status === "planned_only") stats.planned_only += 1;
      else if (c.execution_status === "ready_for_execution_review") stats.ready_for_execution_review += 1;
      else if (c.execution_status === "cancelled") stats.cancelled += 1;
      else if (c.execution_status === "blocked") stats.blocked += 1;
    });
    return {
      candidates: list,
      active_candidates: list.filter(function (c) {
        return c.execution_status !== "cancelled";
      }),
      stats: stats,
      candidate_only: true,
      not_runner_execution: true,
      execution_candidate_not_runner_execution: true,
      not_executed_only: true
    };
  }

  function enrichPackage(executionPkg) {
    if (!executionPkg) return executionPkg;
    executionPkg.execution_candidate_only = true;
    executionPkg.no_runner_invocation = true;
    return executionPkg;
  }

  function getGenerateButtonLabel(runnerType) {
    var c = Copy();
    if (runnerType === "Detection") return c.prepareDetectionBtn;
    if (runnerType === "OCR") return c.prepareOcrBtn;
    return c.generateExecutionCandidateBtn;
  }

  global.ControlledRunnerExecutionUI = {
    version: "controlled_runner_execution_ui_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Controlled-Runner-Execution-UI-Execution-v1-001",
    noRunnerExecution: true,
    noModelCall: true,
    noRunnerInvocation: true,
    executionCandidateNotRunnerExecution: true,
    executionCandidateNotModelOutput: true,
    POLICY_REFS: POLICY_REFS,
    canGenerateExecutionCandidate: canGenerateExecutionCandidate,
    buildFromAdmittedRequest: buildFromAdmittedRequest,
    buildMobileSamFromAdmittedRequest: buildMobileSamFromAdmittedRequest,
    isMobileSamCandidate: isMobileSamCandidate,
    canRunControlledMobileSam: canRunControlledMobileSam,
    buildInputReview: buildInputReview,
    buildPackage: buildPackage,
    enrichPackage: enrichPackage,
    getGenerateButtonLabel: getGenerateButtonLabel
  };
})(typeof window !== "undefined" ? window : this);

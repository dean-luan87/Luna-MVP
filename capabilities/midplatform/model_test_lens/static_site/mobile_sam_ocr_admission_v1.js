/**
 * OCR admission gate for midplatform OCR path. No OCR execution.
 */
(function (global) {
  "use strict";

  var REQUIRED_STAGES = [
    "segmentation_result_envelope",
    "result_candidate",
    "midplatform_analysis",
    "ocr_task_candidate",
    "ocr_invocation_request"
  ];

  var POLICY_REFS = [
    "OcrAdmissionPolicyV1",
    "MobileSamOcrControlledExecutionInputPolicyV1",
    "MobileSamOcrFusionPolicyV1"
  ];

  function verifyTrace(request) {
    var chain = request && request.trace_chain;
    if (!chain || chain.length < REQUIRED_STAGES.length) return false;
    for (var i = 0; i < REQUIRED_STAGES.length; i++) {
      var stage = REQUIRED_STAGES[i];
      var found = false;
      for (var j = 0; j < chain.length; j++) {
        if (chain[j].stage === stage && chain[j].ref) { found = true; break; }
      }
      if (!found) return false;
    }
    var last = chain[chain.length - 1];
    return last && last.stage === "ocr_invocation_request" &&
      last.ref === request.ocr_invocation_request_id;
  }

  function hasForbiddenInput(request) {
    var blob = JSON.stringify(request || {});
    return /confirmed_text|fact_label|这是路牌|这是广告牌/.test(blob);
  }

  function evaluate(request, options) {
    options = options || {};
    var seq = options.seq || 1;
    var oiarId = "oiar_" + (request.ocr_invocation_request_id || "x") + "_" + String(seq).padStart(3, "0");

    if (!request) {
      return { ok: false, result: reject(oiarId, "", "orphan_ocr_request", false, false) };
    }
    if (request.admission_status === "cancelled") {
      return { ok: true, result: {
        admission_result_id: oiarId,
        ocr_invocation_request_id: request.ocr_invocation_request_id,
        admission_decision: "cancelled",
        admission_reason: "用户已取消 OCR request",
        execution_status: "not_executed",
        trace_verified: verifyTrace(request),
        route_match_verified: request.route_type === "OCR",
        policy_refs: POLICY_REFS,
        not_fact: true, candidate_only: true, evaluated_at: new Date().toISOString()
      }};
    }

    var traceOk = verifyTrace(request);
    var routeOk = request.route_type === "OCR" && request.requested_runner_type === "OCR";
    var reason = null;

    if (!request.source_ocr_task_candidate_id) reason = "source_task_missing";
    else if (!request.source_region_id) reason = "source_region_missing";
    else if (!request.source_result_candidate_id) reason = "source_result_candidate_missing";
    else if (!traceOk) reason = "trace_incomplete";
    else if (!routeOk) reason = "route_not_ocr";
    else if (hasForbiddenInput(request)) reason = "confirmed_text_or_fact_label";
    else if (request.bypass_midplatform) reason = "bypass_midplatform";
    else if (!request.candidate_only || !request.not_fact || request.execution_status !== "not_executed") {
      reason = "missing_boundary_flags";
    }

    if (reason) {
      return { ok: true, result: reject(oiarId, request.ocr_invocation_request_id, reason, traceOk, routeOk) };
    }

    return { ok: true, result: {
      admission_result_id: oiarId,
      ocr_invocation_request_id: request.ocr_invocation_request_id,
      admission_decision: "admitted",
      admission_reason: "OCR route 匹配，trace 完整，source task/region/result 可追溯，通过准入",
      execution_status: "not_executed",
      trace_verified: true,
      route_match_verified: true,
      still_not_executed: true,
      policy_refs: POLICY_REFS,
      not_fact: true,
      candidate_only: true,
      admitted_does_not_execute_ocr: true,
      evaluated_at: new Date().toISOString()
    }};
  }

  function reject(id, reqId, reason, traceOk, routeOk) {
    return {
      admission_result_id: id,
      ocr_invocation_request_id: reqId,
      admission_decision: "rejected",
      rejection_reason: reason,
      execution_status: "not_executed",
      trace_verified: !!traceOk,
      route_match_verified: !!routeOk,
      policy_refs: POLICY_REFS,
      not_fact: true,
      candidate_only: true,
      evaluated_at: new Date().toISOString()
    };
  }

  function enrichPackage(pkg) {
    if (!pkg || !pkg.requests) return pkg;
    var stats = { pending: 0, admitted: 0, rejected: 0, cancelled: 0, executed: 0 };
    pkg.requests.forEach(function (r) {
      if (r.execution_status === "executed") stats.executed += 1;
      if (r.admission_status === "pending_admission") stats.pending += 1;
      else if (r.admission_status === "admitted") stats.admitted += 1;
      else if (r.admission_status === "rejected") stats.rejected += 1;
      else if (r.admission_status === "cancelled") stats.cancelled += 1;
    });
    pkg.admission_stats = stats;
    pkg.admitted_does_not_execute_ocr = true;
    return pkg;
  }

  global.MobileSamOcrAdmission = {
    version: "mobile_sam_ocr_admission_v1",
    no_ocr_execution: true,
    ocr_admission_requires_ocr_route: true,
    evaluate: evaluate,
    enrichPackage: enrichPackage,
    verifyTrace: verifyTrace
  };
})(typeof window !== "undefined" ? window : this);

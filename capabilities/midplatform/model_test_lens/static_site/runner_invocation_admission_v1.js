/**
 * Runner Invocation Admission Gate — evaluate requests. No runner execution.
 */
(function (global) {
  "use strict";

  var Policy = function () { return global.RunnerInvocationAdmissionPolicy || {}; };

  function verifyTraceChain(request) {
    var required = Policy().REQUIRED_TRACE_STAGES || [];
    var chain = request && request.trace_chain;
    if (!chain || chain.length < required.length) return false;
    for (var i = 0; i < required.length; i++) {
      var found = false;
      for (var j = 0; j < chain.length; j++) {
        if (chain[j].stage === required[i] && chain[j].ref) {
          found = true;
          break;
        }
      }
      if (!found) return false;
    }
    if (request.invocation_request_id) {
      var last = chain[chain.length - 1];
      if (!last || last.stage !== "runner_invocation_request") return false;
      if (last.ref !== request.invocation_request_id) return false;
    }
    return true;
  }

  function verifyRouteMatch(request, task) {
    if (!request || !task) return false;
    if (request.requested_runner_type === "Detection") {
      return task.target_model_id === "detection" && task.recommended_runner_type === "detection";
    }
    if (request.requested_runner_type === "OCR") {
      return task.target_model_id === "ocr" && task.recommended_runner_type === "ocr";
    }
    return false;
  }

  function mapAdmissionStatus(decision) {
    if (decision === "admitted") return "admitted";
    if (decision === "rejected") return "rejected";
    if (decision === "cancelled") return "cancelled";
    return "pending_admission";
  }

  function evaluate(request, sourceTask, options) {
    options = options || {};
    var codes = Policy().REJECTION_CODES || {};
    var policyRefs = (Policy().POLICY_REFS || []).slice();
    var seq = options.seq || 1;
    var riarId = "riar_" + (request.invocation_request_id || "unknown") + "_" + String(seq).padStart(3, "0");

    if (!request) {
      return {
        ok: false,
        result: {
          admission_result_id: riarId,
          invocation_request_id: "",
          admission_decision: "rejected",
          rejection_reason: codes.orphan_request,
          execution_status: "not_executed",
          trace_verified: false,
          route_match_verified: false,
          policy_refs: policyRefs,
          not_fact: true,
          not_navigation_decision: true,
          candidate_only: true,
          admission_result_not_runner_output: true,
          evaluated_at: new Date().toISOString()
        }
      };
    }

    if (request.admission_status === "cancelled") {
      return {
        ok: true,
        result: {
          admission_result_id: riarId,
          invocation_request_id: request.invocation_request_id,
          admission_decision: "cancelled",
          admission_reason: "用户已取消 request",
          execution_status: "not_executed",
          trace_verified: verifyTraceChain(request),
          route_match_verified: verifyRouteMatch(request, sourceTask),
          policy_refs: policyRefs,
          not_fact: true,
          not_navigation_decision: true,
          candidate_only: true,
          admission_result_not_runner_output: true,
          evaluated_at: new Date().toISOString()
        }
      };
    }

    var traceOk = verifyTraceChain(request);
    var routeOk = verifyRouteMatch(request, sourceTask);
    var rejection = null;

    if (!sourceTask) rejection = codes.orphan_request;
    else if (!traceOk) rejection = codes.trace_chain_incomplete;
    else if (sourceTask.queue_state === "excluded") rejection = codes.source_task_excluded;
    else if (sourceTask.queue_state === "blocked_by_policy") rejection = codes.source_task_blocked_by_policy;
    else if (sourceTask.queue_state === "stale_candidate") rejection = codes.stale_candidate_without_reconfirmation;
    else if (sourceTask.queue_state !== "pinned") rejection = codes.source_task_not_pinned;
    else if (request.execution_status !== "not_executed") rejection = codes.execution_status_not_not_executed;
    else if (!request.candidate_only || !request.not_fact || !request.not_executed) {
      rejection = codes.missing_candidate_boundary_flags;
    } else if (!routeOk) rejection = codes.route_type_mismatch;
    else if (!request.source_runner_task_candidate_id) rejection = codes.bypass_runner_task_candidate;

    if (rejection) {
      return {
        ok: true,
        result: {
          admission_result_id: riarId,
          invocation_request_id: request.invocation_request_id,
          admission_decision: "rejected",
          rejection_reason: rejection,
          execution_status: "not_executed",
          trace_verified: traceOk,
          route_match_verified: routeOk,
          policy_refs: policyRefs,
          not_fact: true,
          not_navigation_decision: true,
          candidate_only: true,
          admission_result_not_runner_output: true,
          evaluated_at: new Date().toISOString()
        }
      };
    }

    if (request.correction_boosted && options.strictCorrectionReview) {
      return {
        ok: true,
        result: {
          admission_result_id: riarId,
          invocation_request_id: request.invocation_request_id,
          admission_decision: "pending",
          admission_reason: "人工指错加权，建议人工复核（priority signal only，非 ground truth）",
          execution_status: "not_executed",
          trace_verified: traceOk,
          route_match_verified: routeOk,
          policy_refs: policyRefs,
          not_fact: true,
          not_navigation_decision: true,
          candidate_only: true,
          admission_result_not_runner_output: true,
          evaluated_at: new Date().toISOString()
        }
      };
    }

    var admitReason = request.requested_runner_type === "Detection"
      ? "Detection route 匹配，trace 完整，source task pinned，通过执行前准入"
      : "OCR route 匹配，trace 完整，source task pinned，通过执行前准入";

    return {
      ok: true,
      result: {
        admission_result_id: riarId,
        invocation_request_id: request.invocation_request_id,
        admission_decision: "admitted",
        admission_reason: admitReason,
        execution_status: "not_executed",
        trace_verified: true,
        route_match_verified: true,
        policy_refs: policyRefs,
        not_fact: true,
        not_navigation_decision: true,
        candidate_only: true,
        admission_result_not_runner_output: true,
        admitted_does_not_execute_runner: true,
        evaluated_at: new Date().toISOString()
      }
    };
  }

  function enrichPackage(requestPkg) {
    if (!requestPkg || !requestPkg.requests) return requestPkg;
    var stats = { admitted: 0, rejected: 0, pending: 0, cancelled: 0, executed: 0, unevaluated: 0 };
    requestPkg.requests.forEach(function (r) {
      if (r.execution_status === "executed") stats.executed += 1;
      var ar = r.admission_result;
      if (!ar) {
        if (r.admission_status === "cancelled") stats.cancelled += 1;
        else stats.unevaluated += 1;
        return;
      }
      if (ar.admission_decision === "admitted") stats.admitted += 1;
      else if (ar.admission_decision === "rejected") stats.rejected += 1;
      else if (ar.admission_decision === "pending") stats.pending += 1;
      else if (ar.admission_decision === "cancelled") stats.cancelled += 1;
    });
    requestPkg.admission_stats = stats;
    requestPkg.admission_gate_only = true;
    requestPkg.admitted_does_not_execute_runner = true;
    return requestPkg;
  }

  global.RunnerInvocationAdmission = {
    version: "runner_invocation_admission_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Runner-Invocation-Admission-Execution-And-Post-Review-v1-001",
    noRunnerExecution: true,
    admittedDoesNotExecuteRunner: true,
    verifyTraceChain: verifyTraceChain,
    verifyRouteMatch: verifyRouteMatch,
    evaluate: evaluate,
    enrichPackage: enrichPackage,
    mapAdmissionStatus: mapAdmissionStatus
  };
})(typeof window !== "undefined" ? window : this);

/**
 * Runner Manual Trigger — invocation request state store. No runner execution.
 */
(function (global) {
  "use strict";

  var ALLOWED_ADMISSION = ["pending_admission", "admitted", "rejected", "cancelled"];
  var FORBIDDEN_EXECUTION = [
    "running", "executed", "completed", "failed_with_model_output",
    "fact_written", "navigation_decided"
  ];

  function createRequestStore() {
    var requests = [];
    var seq = 1;

    function getAll() {
      return requests.slice();
    }

    function findById(rirId) {
      for (var i = 0; i < requests.length; i++) {
        if (requests[i].invocation_request_id === rirId) return requests[i];
      }
      return null;
    }

    function findActiveByRtc(rtcId) {
      for (var i = 0; i < requests.length; i++) {
        var r = requests[i];
        if (r.source_runner_task_candidate_id === rtcId &&
            r.admission_status !== "cancelled" && r.admission_status !== "rejected") {
          return r;
        }
      }
      return null;
    }

    function add(request) {
      if (!request || !request.invocation_request_id) return false;
      if (request.execution_status !== "not_executed") return false;
      if (FORBIDDEN_EXECUTION.indexOf(request.execution_status) >= 0) return false;
      requests.push(request);
      return true;
    }

    function setAdmission(rirId, status) {
      if (ALLOWED_ADMISSION.indexOf(status) < 0) return false;
      var r = findById(rirId);
      if (!r) return false;
      r.admission_status = status;
      r.execution_status = "not_executed";
      return true;
    }

    function cancel(rirId) {
      var r = findById(rirId);
      if (!r) return false;
      r.admission_status = "cancelled";
      r.execution_status = "not_executed";
      if (r.admission_result) {
        r.admission_result.admission_decision = "cancelled";
        r.admission_result.admission_reason = "用户取消 request";
        r.admission_result.execution_status = "not_executed";
      }
      return true;
    }

    function setAdmissionResult(rirId, result) {
      var r = findById(rirId);
      if (!r || !result) return false;
      r.admission_result = result;
      r.execution_status = "not_executed";
      if (result.admission_decision === "admitted") r.admission_status = "admitted";
      else if (result.admission_decision === "rejected") r.admission_status = "rejected";
      else if (result.admission_decision === "cancelled") r.admission_status = "cancelled";
      else r.admission_status = "pending_admission";
      return true;
    }

    var evalSeq = 1;
    function nextEvalSeq() {
      var n = evalSeq;
      evalSeq += 1;
      return n;
    }

    function reset() {
      requests = [];
      seq = 1;
    }

    function nextSeq() {
      var n = seq;
      seq += 1;
      return n;
    }

    return {
      getAll: getAll,
      findById: findById,
      findActiveByRtc: findActiveByRtc,
      add: add,
      setAdmission: setAdmission,
      setAdmissionResult: setAdmissionResult,
      cancel: cancel,
      reset: reset,
      nextSeq: nextSeq,
      nextEvalSeq: nextEvalSeq,
      noRunnerExecution: true,
      executionStatusNotExecutedOnly: true
    };
  }

  global.RunnerManualTriggerRequestState = {
    version: "runner_manual_trigger_request_state_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Runner-Manual-Trigger-UI-Execution-And-Post-Review-v1-001",
    ALLOWED_ADMISSION: ALLOWED_ADMISSION,
    FORBIDDEN_EXECUTION: FORBIDDEN_EXECUTION,
    createStore: createRequestStore,
    noRunnerExecution: true
  };
})(typeof window !== "undefined" ? window : this);

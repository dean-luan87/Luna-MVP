/**
 * MobileSAM → OCR — request & execution candidate state. No OCR runner.
 */
(function (global) {
  "use strict";

  var FORBIDDEN_EXEC = ["running", "executed", "completed", "success", "failed_with_model_output"];

  function createStore() {
    var requests = [];
    var candidates = [];
    var reqSeq = 0;
    var cecSeq = 0;

    function addRequest(req) {
      if (!req || !req.ocr_invocation_request_id) return false;
      if (req.execution_status !== "not_executed") return false;
      if (FORBIDDEN_EXEC.indexOf(req.execution_status) >= 0) return false;
      requests.push(req);
      return true;
    }

    function findRequest(id) {
      for (var i = 0; i < requests.length; i++) {
        if (requests[i].ocr_invocation_request_id === id) return requests[i];
      }
      return null;
    }

    function findActiveByTask(taskId) {
      for (var i = 0; i < requests.length; i++) {
        var r = requests[i];
        if (r.source_ocr_task_candidate_id === taskId &&
            r.admission_status !== "cancelled" && r.admission_status !== "rejected") {
          return r;
        }
      }
      return null;
    }

    function setAdmissionResult(id, result) {
      var r = findRequest(id);
      if (!r || !result) return false;
      r.admission_result = result;
      r.execution_status = "not_executed";
      if (result.admission_decision === "admitted") r.admission_status = "admitted";
      else if (result.admission_decision === "rejected") r.admission_status = "rejected";
      else if (result.admission_decision === "cancelled") r.admission_status = "cancelled";
      else r.admission_status = "pending_admission";
      return true;
    }

    function cancelRequest(id) {
      var r = findRequest(id);
      if (!r) return false;
      r.admission_status = "cancelled";
      r.execution_status = "not_executed";
      return true;
    }

    function addExecutionCandidate(c) {
      if (!c || !c.ocr_execution_candidate_id) return false;
      if (FORBIDDEN_EXEC.indexOf(c.execution_status) >= 0) return false;
      candidates.push(c);
      return true;
    }

    function findCandidate(id) {
      for (var i = 0; i < candidates.length; i++) {
        if (candidates[i].ocr_execution_candidate_id === id) return candidates[i];
      }
      return null;
    }

    function findCandidateByRequest(reqId) {
      for (var i = 0; i < candidates.length; i++) {
        if (candidates[i].source_ocr_invocation_request_id === reqId) return candidates[i];
      }
      return null;
    }

    function nextReqSeq() { reqSeq += 1; return reqSeq; }
    function nextCecSeq() { cecSeq += 1; return cecSeq; }
    function nextEvalSeq() { return nextReqSeq(); }

    function getStats() {
      var stats = { pending: 0, admitted: 0, rejected: 0, cancelled: 0, executed: 0,
        candidates_planned: 0, candidates_not_executed: 0 };
      requests.forEach(function (r) {
        if (r.execution_status === "executed") stats.executed += 1;
        if (r.admission_status === "pending_admission") stats.pending += 1;
        else if (r.admission_status === "admitted") stats.admitted += 1;
        else if (r.admission_status === "rejected") stats.rejected += 1;
        else if (r.admission_status === "cancelled") stats.cancelled += 1;
      });
      candidates.forEach(function (c) {
        if (c.execution_status === "planned_only" || c.execution_status === "not_executed") {
          stats.candidates_planned += 1;
          stats.candidates_not_executed += 1;
        }
      });
      return stats;
    }

    return {
      getRequests: function () { return requests.slice(); },
      getCandidates: function () { return candidates.slice(); },
      addRequest: addRequest,
      findRequest: findRequest,
      findActiveByTask: findActiveByTask,
      setAdmissionResult: setAdmissionResult,
      cancelRequest: cancelRequest,
      addExecutionCandidate: addExecutionCandidate,
      findCandidate: findCandidate,
      findCandidateByRequest: findCandidateByRequest,
      nextReqSeq: nextReqSeq,
      nextCecSeq: nextCecSeq,
      nextEvalSeq: nextEvalSeq,
      getStats: getStats,
      noOcrRunnerExecution: true,
      ocrExecutedMustBeZero: true
    };
  }

  global.MobileSamOcrRequestState = {
    version: "mobile_sam_ocr_request_state_v1",
    createStore: createStore
  };
})(typeof window !== "undefined" ? window : this);

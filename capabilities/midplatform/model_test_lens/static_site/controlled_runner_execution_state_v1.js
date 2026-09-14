/**
 * Controlled Runner Execution — execution candidate state store. No runner execution.
 */
(function (global) {
  "use strict";

  var ALLOWED_STATUS = ["planned_only", "ready_for_execution_review", "cancelled", "blocked"];
  var FORBIDDEN_STATUS = [
    "running", "executing", "completed", "success", "failed_model_output",
    "executed", "fact_written", "navigation_decided"
  ];

  function createExecutionStore() {
    var candidates = [];
    var seq = 1;

    function getAll() {
      return candidates.slice();
    }

    function findById(crecId) {
      for (var i = 0; i < candidates.length; i++) {
        if (candidates[i].execution_candidate_id === crecId) return candidates[i];
      }
      return null;
    }

    function findActiveByRir(rirId) {
      for (var i = 0; i < candidates.length; i++) {
        var c = candidates[i];
        if (c.source_invocation_request_id === rirId &&
            c.execution_status !== "cancelled" && c.execution_status !== "blocked") {
          return c;
        }
      }
      return null;
    }

    function add(candidate) {
      if (!candidate || !candidate.execution_candidate_id) return false;
      if (ALLOWED_STATUS.indexOf(candidate.execution_status) < 0) return false;
      if (FORBIDDEN_STATUS.indexOf(candidate.execution_status) >= 0) return false;
      if (!candidate.not_executed || !candidate.not_fact || !candidate.candidate_only) return false;
      candidates.push(candidate);
      return true;
    }

    function setStatus(crecId, status) {
      if (ALLOWED_STATUS.indexOf(status) < 0) return false;
      var c = findById(crecId);
      if (!c) return false;
      c.execution_status = status;
      c.not_executed = true;
      return true;
    }

    function cancel(crecId) {
      return setStatus(crecId, "cancelled");
    }

    function reset() {
      candidates = [];
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
      findActiveByRir: findActiveByRir,
      add: add,
      setStatus: setStatus,
      cancel: cancel,
      reset: reset,
      nextSeq: nextSeq,
      ALLOWED_STATUS: ALLOWED_STATUS,
      FORBIDDEN_STATUS: FORBIDDEN_STATUS,
      noRunnerExecution: true,
      executionCandidateNotRunnerExecution: true
    };
  }

  global.ControlledRunnerExecutionState = {
    version: "controlled_runner_execution_state_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Controlled-Runner-Execution-UI-Execution-v1-001",
    ALLOWED_STATUS: ALLOWED_STATUS,
    FORBIDDEN_STATUS: FORBIDDEN_STATUS,
    createStore: createExecutionStore,
    noRunnerExecution: true
  };
})(typeof window !== "undefined" ? window : this);

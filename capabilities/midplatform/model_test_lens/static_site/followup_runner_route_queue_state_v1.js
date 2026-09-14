/**
 * Followup Runner Route — queue state (pin / unpin / exclude). No runner execution.
 */
(function (global) {
  "use strict";

  var ALLOWED_STATES = ["candidate", "pinned", "excluded", "stale_candidate", "blocked_by_policy"];
  var FORBIDDEN_STATES = ["running", "executed", "completed", "fact_written", "navigation_decided"];

  function createQueueStateStore() {
    var overrides = {};

    function getOverride(rtcId) {
      return overrides[rtcId] || null;
    }

    function setOverride(rtcId, queueState) {
      if (FORBIDDEN_STATES.indexOf(queueState) >= 0) return false;
      if (ALLOWED_STATES.indexOf(queueState) < 0) return false;
      overrides[rtcId] = { queue_state: queueState, updated_at: Date.now() };
      return true;
    }

    function clearOverride(rtcId) {
      delete overrides[rtcId];
    }

    function pin(rtcId) {
      return setOverride(rtcId, "pinned");
    }

    function unpin(rtcId) {
      clearOverride(rtcId);
      return true;
    }

    function exclude(rtcId) {
      return setOverride(rtcId, "excluded");
    }

    function restore(rtcId) {
      clearOverride(rtcId);
      return true;
    }

    function reset() {
      overrides = {};
    }

    return {
      getOverride: getOverride,
      pin: pin,
      unpin: unpin,
      exclude: exclude,
      restore: restore,
      reset: reset,
      pinDoesNotExecuteRunner: true,
      noRunningStateAllowed: true
    };
  }

  global.FollowupRunnerRouteQueueState = {
    version: "followup_runner_route_queue_state_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-UI-Queue-Execution-And-Post-Review-v1-001",
    ALLOWED_STATES: ALLOWED_STATES,
    FORBIDDEN_STATES: FORBIDDEN_STATES,
    createStore: createQueueStateStore,
    noAutoRunnerTrigger: true,
    noRunnerExecution: true
  };
})(typeof window !== "undefined" ? window : this);

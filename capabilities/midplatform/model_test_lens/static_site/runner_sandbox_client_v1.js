/**
 * Runner Sandbox Client v1 — controlled MobileSAM execution via Local Runner Bridge (8787).
 * Page does not execute model directly; calls governance-gated API only.
 */
(function (global) {
  "use strict";

  var BRIDGE_BASE = "http://127.0.0.1:8787";

  function runControlledMobileSam(executionCandidate, imageRef, options) {
    options = options || {};
    var base = options.bridgeBase || BRIDGE_BASE;
    var body = {
      execution_candidate: executionCandidate,
      image_ref: imageRef || (executionCandidate && executionCandidate.input_payload_ref),
      environment: "test_environment",
      controlled_execution: true,
      candidate_only: true
    };
    return fetch(base + "/api/v1/controlled-execution/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    }).then(function (res) {
      return res.json().then(function (data) {
        return { httpStatus: res.status, result: data };
      });
    });
  }

  function runControlledOcr(executionCandidate, options) {
    options = options || {};
    var base = options.bridgeBase || BRIDGE_BASE;
    var body = {
      execution_candidate: executionCandidate,
      environment: "localhost_8787",
      controlled_execution: true,
      candidate_only: true,
      sandbox_only: true
    };
    return fetch(base + "/api/v1/controlled-execution/ocr/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    }).then(function (res) {
      return res.json().then(function (data) {
        return { httpStatus: res.status, result: data };
      });
    });
  }

  global.RunnerSandboxClient = {
    version: "runner_sandbox_client_v1",
    phaseRef: "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Runner-Sandbox-Integration-Execution-v1-001",
    BRIDGE_BASE: BRIDGE_BASE,
    runnerExecutionRequiresSandbox: true,
    runnerExecutionRequiresExecutionCandidate: true,
    ocrRunnerExecutionRequiresSandbox: true,
    noUiDirectModelCall: true,
    runControlledMobileSam: runControlledMobileSam,
    runControlledOcr: runControlledOcr
  };
})(typeof window !== "undefined" ? window : this);

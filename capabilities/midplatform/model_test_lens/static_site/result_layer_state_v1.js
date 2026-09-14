/**
 * Result Layer — state store for result envelope records. No fact write.
 */
(function (global) {
  "use strict";

  function createResultStore() {
    var results = [];
    var errors = [];
    var executions = [];

    function addExecutionResult(payload) {
      if (!payload) return false;
      if (payload.runner_execution_record) executions.push(payload.runner_execution_record);
      if (payload.ocr_execution_record) executions.push(payload.ocr_execution_record);
      if (payload.result_envelope_record) results.push(payload.result_envelope_record);
      if (payload.ocr_result_envelope) {
        var rec = payload.result_envelope_record || {
          result_type: "ocr_result_envelope",
          source_execution_id: payload.ocr_result_envelope.source_ocr_execution_id,
          source_execution_candidate_id: payload.ocr_result_envelope.source_ocr_execution_candidate_id,
          source_region_id: payload.ocr_result_envelope.source_region_id,
          text_candidate_list: payload.ocr_result_envelope.text_candidate_list,
          confidence: payload.ocr_result_envelope.confidence,
          model_source: payload.ocr_result_envelope.model_name,
          model_version: payload.ocr_result_envelope.model_version,
          needs_fact_admission: true,
          not_fact: true,
          candidate_only: true,
          trace_chain: payload.ocr_result_envelope.trace_chain
        };
        results.push(rec);
      }
      if (payload.runner_error_candidate) errors.push(payload.runner_error_candidate);
      if (payload.ocr_runner_error_candidate) errors.push(payload.ocr_runner_error_candidate);
      return true;
    }

    return {
      getResults: function () { return results.slice(); },
      getErrors: function () { return errors.slice(); },
      getExecutions: function () { return executions.slice(); },
      getActiveResults: function () {
        return results.filter(function (r) { return r && r.not_fact; });
      },
      reset: function () {
        results = [];
        errors = [];
        executions = [];
      },
      noDirectFactWriteFromRunner: true,
      resultLayerNotObservationLayer: true
    };
  }

  global.ResultLayerState = {
    version: "result_layer_state_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-MobileSAM-Single-Model-Execution-Integration-v1-002",
    createStore: createResultStore
  };
})(typeof window !== "undefined" ? window : this);

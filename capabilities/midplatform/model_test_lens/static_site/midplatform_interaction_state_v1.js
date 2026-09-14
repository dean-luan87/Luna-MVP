/**
 * Midplatform Interaction — build UI package from result + attention + corrections.
 */
(function (global) {
  "use strict";

  var Processor = function () { return global.MidplatformResultProcessor; };
  var HCStore = function () { return global.HumanCorrectionStore; };

  function buildPackage(state) {
    state = state || {};
    var case1 = null;
    if (Processor() && state.resultPkg) {
      case1 = Processor().processFromUiState(
        state.resultPkg,
        state.attentionPkg,
        state.executionPkg,
        { image_ref: state.imageRef, task_context: "street_navigation_test" }
      );
    }
    var corrections = [];
    if (HCStore() && HCStore().list) {
      corrections = HCStore().list().filter(function (c) {
        return c.midplatform_analysis || c.correction_id;
      });
    }
    return {
      case1: case1,
      corrections: corrections,
      candidate_only: true,
      not_fact: true,
      ocr_runner_forbidden: true,
      detection_runner_forbidden: true
    };
  }

  global.MidplatformInteractionState = {
    version: "midplatform_interaction_state_v1",
    buildPackage: buildPackage
  };
})(typeof window !== "undefined" ? window : this);

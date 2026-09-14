/**
 * Build multi-model collaboration package from midplatform Case 1 output.
 */
(function (global) {
  "use strict";

  var Processor = function () { return global.MidplatformResultProcessor; };

  function toCollaborationItem(evalItem) {
    if (!evalItem) return null;
    var regionId = evalItem.region_id;
    var rc = evalItem.result_candidate || {};
    var analysis = evalItem.analysis || {};
    var task = evalItem.task_candidate;
    if (!task) return { region_id: regionId, ocr_task_candidate: null };

    return {
      region_id: regionId,
      result_candidate: {
        source_region_id: regionId,
        result_candidate_id: "rc_seg_" + regionId,
        mask_ref: rc.mask_ref,
        confidence: rc.confidence
      },
      midplatform_analysis_record: {
        analysis_record_id: analysis.analysis_id || ("mar_" + regionId),
        appearance_signals: analysis.region_features || [],
        judgment: analysis.midplatform_judgment
      },
      ocr_task_candidate: {
        task_candidate_id: task.task_candidate_id,
        source_region_id: regionId,
        source_result_candidate_id: "rc_seg_" + regionId,
        source_analysis_record_id: analysis.analysis_id || ("mar_" + regionId),
        not_runner_execution: true,
        ocr_runner_forbidden: true,
        candidate_only: true
      },
      followup_model_route_candidate: evalItem.route_candidate || null,
      trace_chain: evalItem.trace_chain || []
    };
  }

  function buildPackage(midplatformPkg) {
    var items = [];
    if (!midplatformPkg || !midplatformPkg.case1 || !midplatformPkg.case1.items) {
      return { items: [], candidate_only: true, no_ocr_execution: true };
    }
    midplatformPkg.case1.items.forEach(function (it) {
      var mapped = toCollaborationItem(it);
      if (mapped) items.push(mapped);
    });
    return {
      phase_ref: "Phase-P1-Midplatform-Multi-Model-Interaction-MobileSAM-OCR-Exploration-Smoke-v1-001",
      items: items,
      candidate_only: true,
      no_ocr_execution: true,
      no_ocr_runner_call: true
    };
  }

  global.MultiModelCollaborationState = {
    version: "multi_model_collaboration_state_v1",
    buildPackage: buildPackage
  };
})(typeof window !== "undefined" ? window : this);

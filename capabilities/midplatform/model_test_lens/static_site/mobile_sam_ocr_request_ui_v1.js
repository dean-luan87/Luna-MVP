/**
 * Build OCR invocation request from OCR task candidate (midplatform path only).
 */
(function (global) {
  "use strict";

  var FORBIDDEN_FIELDS = ["confirmed_text", "fact_label", "这是路牌", "这是广告牌"];

  function buildTraceChain(collabItem, oirId) {
    var task = collabItem.ocr_task_candidate || {};
    var rc = collabItem.result_candidate || {};
    var analysis = collabItem.midplatform_analysis_record || {};
    var route = collabItem.followup_model_route_candidate || {};
    return [
      { stage: "segmentation_result_envelope", ref: rc.mask_ref || "mask" },
      { stage: "result_candidate", ref: rc.result_candidate_id || task.source_result_candidate_id },
      { stage: "midplatform_analysis", ref: analysis.analysis_record_id || task.source_analysis_record_id },
      { stage: "ocr_route_candidate", ref: route.followup_model_route_candidate_id || "fmrc_ocr" },
      { stage: "ocr_task_candidate", ref: task.task_candidate_id || task.runner_task_candidate_id },
      { stage: "ocr_invocation_request", ref: oirId }
    ];
  }

  function buildFromOcrTaskCandidate(collabItem, envelope, store) {
    if (!collabItem || !collabItem.ocr_task_candidate) {
      return { ok: false, error: "缺少 OCR task candidate" };
    }
    var task = collabItem.ocr_task_candidate;
    if (!task.source_region_id && !collabItem.region_id) {
      return { ok: false, error: "缺少 source_region_id" };
    }
    if (!task.source_result_candidate_id && !(collabItem.result_candidate || {}).result_candidate_id) {
      return { ok: false, error: "缺少 source_result_candidate_id（须经 MobileSAM result）" };
    }
    if (!task.source_analysis_record_id && !(collabItem.midplatform_analysis_record || {}).analysis_record_id) {
      return { ok: false, error: "缺少 source_analysis_record_id（须经中台分析）" };
    }
    var taskId = task.task_candidate_id || task.runner_task_candidate_id;
    if (store && store.findActiveByTask && store.findActiveByTask(taskId)) {
      return { ok: false, error: "该 OCR task 已有活跃 request" };
    }

    var regionId = task.source_region_id || collabItem.region_id;
    var seq = store && store.nextReqSeq ? store.nextReqSeq() : 1;
    var oirId = "oir_ocr_" + regionId + "_" + String(seq).padStart(3, "0");
    var envRef = (envelope && (envelope._source_file_ref || envelope.envelope_id)) || "local://envelope";
    var imageRef = (envelope && envelope.input_asset_refs && envelope.input_asset_refs[0]) || envRef;

    var request = {
      ocr_invocation_request_id: oirId,
      source_ocr_task_candidate_id: taskId,
      source_followup_model_route_candidate_id: task.source_followup_route_ref ||
        (collabItem.followup_model_route_candidate || {}).followup_model_route_candidate_id,
      source_region_id: regionId,
      source_result_candidate_id: task.source_result_candidate_id ||
        collabItem.result_candidate.result_candidate_id,
      source_analysis_record_id: task.source_analysis_record_id ||
        collabItem.midplatform_analysis_record.analysis_record_id,
      source_image_ref: imageRef,
      region_crop_ref: envRef + "#crop/" + regionId,
      region_geometry_ref: "region://" + regionId,
      ocr_target_reason: task.route_reason || "疑似文字区域，建议 OCR 候选复核（中台调度）",
      requested_runner_type: "OCR",
      trigger_mode: "manual_controlled",
      admission_status: "pending_admission",
      execution_status: "not_executed",
      route_type: "OCR",
      candidate_only: true,
      not_fact: true,
      not_executed: true,
      trace_chain: buildTraceChain(collabItem, oirId),
      midplatform_path_only: true,
      no_mobile_sam_direct_to_ocr: true
    };

    return { ok: true, request: request };
  }

  global.MobileSamOcrRequestUI = {
    version: "mobile_sam_ocr_request_ui_v1",
    no_ocr_runner_call: true,
    ocr_request_requires_ocr_task_candidate: true,
    buildFromOcrTaskCandidate: buildFromOcrTaskCandidate,
    buildTraceChain: buildTraceChain
  };
})(typeof window !== "undefined" ? window : this);

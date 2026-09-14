/**
 * OCR controlled execution candidate builder. Planning endpoint — no OCR runner.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.MobileSamOcrControlledExecutionCopy || {}; };

  var SCHEMA_REFS = {
    output: "schemas/multi_model_interaction/ocr_result_envelope_schema_v1.json",
    error: "schemas/multi_model_interaction/ocr_runner_error_candidate_schema_v1.json",
    input: "schemas/multi_model_interaction/mobile_sam_ocr_controlled_execution_input_policy_v1.json"
  };

  function canGenerate(request, store) {
    if (!request) return { ok: false, hint: "缺少 request" };
    if (request.admission_status === "cancelled") return { ok: false, hint: "request 已取消" };
    if (request.admission_status === "rejected") return { ok: false, hint: "request 已拒绝" };
    if (request.admission_status === "pending_admission") return { ok: false, hint: "须先通过 OCR 准入" };
    if (!request.admission_result || request.admission_result.admission_decision !== "admitted") {
      return { ok: false, hint: "须 admitted request" };
    }
    if (store && store.findCandidateByRequest &&
        store.findCandidateByRequest(request.ocr_invocation_request_id)) {
      return { ok: false, hint: "已存在 execution candidate" };
    }
    return { ok: true };
  }

  function buildInputReview(request) {
    return {
      title: Copy().inputReviewTitle,
      principle: Copy().inputPrinciple,
      allowed_inputs: [
        "source_image_ref", "source_region_id", "region_crop_ref", "region_geometry_ref",
        "source_result_candidate_id", "source_analysis_record_id", "source_ocr_task_candidate_id",
        "ocr_target_reason", "trace_chain"
      ],
      forbidden_inputs: [
        "confirmed text", "fact label", "这是路牌", "这是广告牌", "confirmed_dynamic",
        "human correction as ground truth", "MobileSAM prompt_label as fact", "navigation decision context"
      ],
      candidate_only: true,
      not_fact: true
    };
  }

  function buildFutureEnvelopePreview() {
    return {
      envelope_type: "ocr_result_envelope",
      fields: ["text_candidate_list", "text_region_candidate", "reading_order_candidate",
        "confidence", "needs_fact_admission", "not_fact"],
      planning_only: true,
      no_ocr_result_this_phase: true
    };
  }

  function buildFromAdmittedRequest(request, store, envelope) {
    var check = canGenerate(request, store);
    if (!check.ok) return { ok: false, error: check.hint };

    var seq = store && store.nextCecSeq ? store.nextCecSeq() : 1;
    var regionId = request.source_region_id;
    var ocecId = "ocec_ocr_" + regionId + "_" + String(seq).padStart(3, "0");
    var envRef = (envelope && (envelope._source_file_ref || envelope.envelope_id)) || request.source_image_ref;

    var trace = (request.trace_chain || []).slice();
    trace.push({ stage: "ocr_admission", ref: request.admission_result.admission_result_id });
    trace.push({ stage: "ocr_controlled_execution_candidate", ref: ocecId });

    var candidate = {
      ocr_execution_candidate_id: ocecId,
      source_ocr_invocation_request_id: request.ocr_invocation_request_id,
      source_ocr_task_candidate_id: request.source_ocr_task_candidate_id,
      source_region_id: regionId,
      source_result_candidate_id: request.source_result_candidate_id,
      source_analysis_record_id: request.source_analysis_record_id,
      requested_runner_type: "OCR",
      execution_mode: "manual_controlled",
      execution_status: "planned_only",
      input_crop_ref: request.region_crop_ref || (envRef + "#crop/" + regionId),
      input_region_geometry_ref: request.region_geometry_ref || ("region://" + regionId),
      ocr_runner_config_ref: "runner_config/ocr_manual_controlled_v1.json",
      output_envelope_schema_ref: SCHEMA_REFS.output,
      timeout_policy_ref: SCHEMA_REFS.error + "#timeout",
      error_policy_ref: SCHEMA_REFS.error,
      input_policy_ref: SCHEMA_REFS.input,
      ocr_target_reason: request.ocr_target_reason || "疑似文字区域，建议 OCR 候选复核（中台调度）",
      trace_chain: trace,
      input_review: buildInputReview(request),
      future_envelope_preview: buildFutureEnvelopePreview(),
      fusion_placeholder: {
        mobile_sam: "region geometry",
        ocr: "text candidate",
        output: "multimodal_evidence_candidate",
        needs_fact_admission: true
      },
      candidate_only: true,
      not_executed: true,
      not_fact: true,
      needs_fact_admission: true,
      no_ocr_runner_call: true
    };

    return { ok: true, candidate: candidate };
  }

  global.MobileSamOcrExecutionCandidate = {
    version: "mobile_sam_ocr_execution_candidate_v1",
    ocr_execution_candidate_requires_admitted_request: true,
    no_ocr_execution: true,
    canGenerate: canGenerate,
    buildFromAdmittedRequest: buildFromAdmittedRequest
  };
})(typeof window !== "undefined" ? window : this);

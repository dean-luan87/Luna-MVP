/**
 * Midplatform result processor — Case 1: MobileSAM result → OCR route candidate (JS, no runner).
 */
(function (global) {
  "use strict";

  function aspectRatio(bbox) {
    var w = Math.max(parseFloat(bbox && bbox.width) || 0, 1e-6);
    var h = Math.max(parseFloat(bbox && bbox.height) || 0, 1e-6);
    return h / w;
  }

  function textLikelihoodSignals(envelope, attentionRecord, taskContext) {
    var signals = [];
    var score = 0;
    var bbox = (envelope && envelope.bbox_hint) || (envelope && envelope.bbox) || {};
    if (bbox.width || bbox.height) {
      var ar = aspectRatio(bbox);
      if (ar >= 1.2) { signals.push("竖长结构"); score += 0.25; }
      if (ar >= 1.5 && ar <= 6) { signals.push("可能文本承载区域"); score += 0.25; }
    }
    if (attentionRecord) {
      if (attentionRecord.ocr_required) {
        signals.push("静态文字候选提示");
        score += 0.35;
      }
      if (attentionRecord.motion_state_candidate === "static_text_candidate") {
        signals.push("静态区域候选");
        score += 0.2;
      }
    }
    if (taskContext === "street_navigation_test") {
      signals.push("街景导航任务上下文");
      score += 0.1;
    }
    var conf = parseFloat(envelope && envelope.confidence);
    if (!isNaN(conf) && conf >= 0.4) {
      signals.push("分割置信度可接受");
      score += Math.min(conf * 0.2, 0.15);
    }
    return { signals: signals, score: Math.min(score, 1) };
  }

  function evaluateRegion(envelope, attentionRecord, options) {
    options = options || {};
    var taskContext = options.task_context || "street_navigation_test";
    var threshold = options.ocr_threshold || 0.45;
    var lik = textLikelihoodSignals(envelope, attentionRecord, taskContext);
    var textLikely = lik.score >= threshold;
    var regionId = (envelope && envelope.region_id) ||
      (attentionRecord && attentionRecord.region_id) || "unknown_region";

    var analysis = {
      analysis_id: "mpa_" + regionId,
      card_type: "midplatform_analysis_record",
      source_region_id: regionId,
      source_input: "MobileSAM Result",
      midplatform_judgment: textLikely ? "text-likely" : "needs_followup_review",
      region_features: lik.signals,
      midplatform_score: Math.round(lik.score * 1000) / 1000,
      route_type: textLikely ? "ocr" : null,
      route_label: textLikely ? "OCR route candidate" : null,
      route_reason: textLikely
        ? "该区域值得进一步文字观察（中台调度，非 MobileSAM 断言）"
        : "暂不建议 OCR 调度",
      training_candidate: "not_applicable",
      candidate_only: true,
      not_fact: true,
      result_analysis_not_fact: true,
      midplatform_analysis_not_model_output: true,
      route_candidate_not_execution: true,
      ocr_candidate_not_ocr_result: true
    };

    var taskCandidate = null;
    if (textLikely) {
      taskCandidate = {
        task_candidate_id: "T-ocr-" + regionId,
        recommended_runner_type: "ocr",
        route_reason: analysis.route_reason,
        candidate_only: true,
        not_runner_execution: true,
        ocr_runner_forbidden: true
      };
    }

    return {
      region_id: regionId,
      text_likely: textLikely,
      analysis: analysis,
      task_candidate: taskCandidate,
      result_candidate: buildResultCandidateView(envelope, regionId)
    };
  }

  function buildResultCandidateView(envelope, regionId) {
    return {
      card_type: "result_candidate",
      model: (envelope && envelope.model_source) || "MobileSAM",
      result_type: "Segmentation Result Candidate",
      region_id: regionId || "—",
      model_provides: "区域几何信息",
      mask_ref: (envelope && (envelope.mask_ref || envelope.payload_ref)) || "—",
      confidence: envelope && envelope.confidence != null ? envelope.confidence : "—",
      status: "candidate_only",
      candidate_only: true,
      not_fact: true,
      result_candidate_not_fact: true,
      no_fact_label: true
    };
  }

  function envelopeFromResultRecord(rec, executionLookup) {
    var crec = executionLookup && rec.source_execution_candidate_id
      ? executionLookup[rec.source_execution_candidate_id] : null;
    return {
      region_id: (crec && crec.source_region_id) || rec.region_id || "",
      mask_ref: rec.mask_ref || rec.payload_ref,
      payload_ref: rec.payload_ref,
      confidence: rec.confidence,
      model_source: rec.model_source || "MobileSAM",
      model_version: rec.model_version,
      source_execution_id: rec.source_execution_id,
      source_execution_candidate_id: rec.source_execution_candidate_id,
      bbox_hint: rec.bbox_hint || (crec && crec.bbox_hint)
    };
  }

  function buildExecutionLookup(executionPkg) {
    var map = {};
    var list = (executionPkg && executionPkg.candidates) || [];
    list.forEach(function (c) {
      if (c.execution_candidate_id) map[c.execution_candidate_id] = c;
    });
    return map;
  }

  function attentionByRegion(attentionPkg) {
    var map = {};
    ((attentionPkg && attentionPkg.records) || []).forEach(function (r) {
      if (r.region_id) map[r.region_id] = r;
    });
    return map;
  }

  function buildTraceChain(parts) {
    return parts.filter(Boolean);
  }

  function processFromUiState(resultPkg, attentionPkg, executionPkg, options) {
    options = options || {};
    var results = (resultPkg && resultPkg.active_results) || [];
    if (!results.length) {
      return { items: [], trace_chains: [], candidate_only: true, empty: true };
    }
    var execLookup = buildExecutionLookup(executionPkg);
    var attnMap = attentionByRegion(attentionPkg);
    var items = [];
    var traces = [];

    results.forEach(function (rec) {
      var env = envelopeFromResultRecord(rec, execLookup);
      var regionId = env.region_id;
      var attn = attnMap[regionId];
      var evalOut = evaluateRegion(env, attn, options);
      items.push(evalOut);

      traces.push(buildTraceChain([
        { stage: "Image", ref: options.image_ref || "input" },
        { stage: "Segmentation Region", ref: regionId },
        { stage: "Execution Record", ref: rec.source_execution_id },
        { stage: "Result Envelope", ref: rec.payload_ref || rec.mask_ref },
        { stage: "Midplatform Analysis", ref: evalOut.analysis.analysis_id },
        evalOut.task_candidate
          ? { stage: "OCR Task Candidate", ref: evalOut.task_candidate.task_candidate_id }
          : null
      ]));
    });

    return {
      phase_ref: "Phase-P1-Midplatform-Single-Model-Interaction-Validation-UI-Execution-v1-001",
      case_id: "Case-1-MobileSAM-to-OCR-Route-Candidate",
      items: items,
      trace_chains: traces,
      candidate_only: true,
      not_fact: true,
      ocr_runner_forbidden: true,
      midplatform_analysis_not_training_directive: true
    };
  }

  global.MidplatformResultProcessor = {
    version: "midplatform_result_processor_v1",
    evaluateRegion: evaluateRegion,
    processFromUiState: processFromUiState
  };
})(typeof window !== "undefined" ? window : this);

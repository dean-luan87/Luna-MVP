/**
 * Dual route perception — deterministic stub state builder (browser, no real models).
 */
(function (global) {
  "use strict";

  var SUBWAY_FIXTURE_A = [
    { grounding_prompt: "station direction sign candidate", detected_label_candidate: "direction_sign",
      bbox: { x1: 0.22, y1: 0.02, x2: 0.78, y2: 0.20 }, confidence: 0.81, text_likelihood: 0.88 },
    { grounding_prompt: "text region candidate", detected_label_candidate: "text_region",
      bbox: { x1: 0.20, y1: 0.05, x2: 0.80, y2: 0.24 }, confidence: 0.76, text_likelihood: 0.85 }
  ];
  var STREET_FIXTURE_A = [
    { grounding_prompt: "road sign candidate", detected_label_candidate: "sign",
      bbox: { x1: 0.62, y1: 0.42, x2: 0.88, y2: 0.63 }, confidence: 0.79, text_likelihood: 0.82 },
    { grounding_prompt: "vehicle candidate", detected_label_candidate: "vehicle_candidate",
      bbox: { x1: 0.37, y1: 0.70, x2: 0.51, y2: 0.79 }, confidence: 0.74, text_likelihood: 0.12 },
    { grounding_prompt: "advertisement panel candidate", detected_label_candidate: "advertisement_panel",
      bbox: { x1: 0.31, y1: 0.43, x2: 0.55, y2: 0.68 }, confidence: 0.71, text_likelihood: 0.55 }
  ];

  function uid(prefix) {
    return prefix + "_" + Math.random().toString(36).slice(2, 10);
  }

  function inferScene(envelope) {
    var sp = envelope && envelope.scene_profile_candidate;
    if (sp && sp.scene_type_candidate) return sp.scene_type_candidate;
    var name = (envelope && (envelope._source_file_name || envelope.test_case_id || "")).toLowerCase();
    if (/subway|jiahuihu|station|platform|地铁/.test(name)) return "subway_platform";
    if (/street|urban|road|街景/.test(name)) return "outdoor_street";
    return "unknown_scene";
  }

  function fixtureA(sceneType, fixtureConfig) {
    fixtureConfig = fixtureConfig || {};
    if (fixtureConfig.route_a_miss) return [];
    if (fixtureConfig.route_conflict) {
      return [{ grounding_prompt: "person candidate", detected_label_candidate: "person_candidate",
        bbox: { x1: 0.58, y1: 0.32, x2: 0.95, y2: 0.88 }, confidence: 0.77, text_likelihood: 0.05 }];
    }
    if (sceneType === "subway_platform" || sceneType === "indoor_station") return SUBWAY_FIXTURE_A.slice();
    if (sceneType === "outdoor_street") return STREET_FIXTURE_A.slice();
    return [];
  }

  function buildRouteA(imageRef, sceneType, fixtureConfig) {
    var specs = fixtureA(sceneType, fixtureConfig);
    var grounding = specs.map(function (spec) {
      var cid = uid("gdc");
      return {
        candidate_id: cid,
        source_image_ref: imageRef,
        grounding_prompt: spec.grounding_prompt,
        detected_label_candidate: spec.detected_label_candidate,
        bbox: spec.bbox,
        confidence: spec.confidence,
        text_likelihood: spec.text_likelihood,
        candidate_only: true,
        not_fact: true,
        detected_label_not_fact: true,
        trace_chain: [{ stage: "input_image", ref: imageRef }, { stage: "route_a_grounding_detection", ref: cid }]
      };
    });
    var masks = grounding.map(function (g) {
      var mid = uid("srmc");
      return {
        candidate_id: mid,
        source_grounding_candidate_id: g.candidate_id,
        mask_candidate_ref: "mask_stub/" + mid + ".png",
        refine_method: "sam_refine_stub",
        confidence: g.confidence,
        candidate_only: true,
        not_fact: true,
        sam_mask_not_semantic_fact: true,
        trace_chain: g.trace_chain.concat([{ stage: "route_a_sam_refine", ref: mid }])
      };
    });
    return {
      route_id: "route_a_detector_grounding_sam",
      no_grounding_real_model_call: true,
      grounding_detection_candidates: grounding,
      sam_refine_mask_candidates: masks,
      candidate_only: true,
      not_fact: true,
      route_a_candidate_only: true
    };
  }

  function buildRouteB(imageRef, sceneType, fixtureConfig) {
    fixtureConfig = fixtureConfig || {};
    var cid = uid("vlmrc");
    var attention = [];
    var followups = ["detection"];
    var reasoning = "场景候选；建议人工复核。";
    var uncertainty = 0.5;
    if (fixtureConfig.route_conflict) {
      attention = [{ region_hint: "top_sign_area", region_description_candidate: "上方导视文字区域候选",
        bbox_hint: { x1: 0.22, y1: 0.02, x2: 0.78, y2: 0.20 }, attention_reason_candidate: "ocr_task_semantic_candidate" }];
      followups = ["ocr", "detection"];
      reasoning = "VLM 建议关注上方导视区域候选；需与 Route A 对照，不确认类别。";
      uncertainty = 0.62;
    } else if (sceneType === "subway_platform" || sceneType === "indoor_station") {
      attention = [
        { region_hint: "top_direction_sign", region_description_candidate: "上方导视/站名区域候选",
          bbox_hint: { x1: 0.22, y1: 0.02, x2: 0.78, y2: 0.20 }, attention_reason_candidate: "text_likely_region_candidate" }
      ];
      followups = ["ocr", "detection"];
      reasoning = "地铁站场景候选；上方导视区域进入 OCR route candidate。";
      uncertainty = 0.35;
    } else if (sceneType === "outdoor_street") {
      attention = [
        { region_hint: "road_sign_area", region_description_candidate: "路侧标识区域候选",
          bbox_hint: { x1: 0.62, y1: 0.42, x2: 0.88, y2: 0.63 }, attention_reason_candidate: "text_likely_region_candidate" },
        { region_hint: "vehicle_area", region_description_candidate: "动态目标区域候选",
          bbox_hint: { x1: 0.37, y1: 0.70, x2: 0.51, y2: 0.79 }, attention_reason_candidate: "dynamic_target_candidate" }
      ];
      followups = ["ocr", "detection", "depth"];
      reasoning = "街景场景候选；标识与车辆分别进入 OCR / Detection route。";
      uncertainty = 0.41;
    }
    return {
      route_id: "route_b_vlm_route_candidate",
      no_vlm_real_model_call: true,
      vlm_route_candidate: {
        candidate_id: cid,
        source_image_ref: imageRef,
        scene_profile_candidate: sceneType,
        suggested_attention_regions: attention,
        suggested_followup_models: followups,
        reasoning_summary: reasoning,
        uncertainty: uncertainty,
        candidate_only: true,
        not_fact: true,
        vlm_output_not_fact: true,
        trace_chain: [{ stage: "input_image", ref: imageRef }, { stage: "route_b_vlm_route", ref: cid }]
      },
      candidate_only: true,
      not_fact: true,
      route_b_candidate_only: true
    };
  }

  function bboxOverlap(a, b) {
    var x1 = Math.max(a.x1, b.x1);
    var y1 = Math.max(a.y1, b.y1);
    var x2 = Math.min(a.x2, b.x2);
    var y2 = Math.min(a.y2, b.y2);
    if (x2 <= x1 || y2 <= y1) return 0;
    var inter = (x2 - x1) * (y2 - y1);
    var areaA = Math.max((a.x2 - a.x1) * (a.y2 - a.y1), 1e-6);
    var areaB = Math.max((b.x2 - b.x1) * (b.y2 - b.y1), 1e-6);
    return Math.max(0, Math.min(1, inter / (areaA + areaB - inter)));
  }

  function compareRoutes(routeA, routeB, fixtureConfig) {
    fixtureConfig = fixtureConfig || {};
    var grounding = routeA.grounding_detection_candidates || [];
    var vlm = routeB.vlm_route_candidate || {};
    var attention = vlm.suggested_attention_regions || [];
    var overlap = 0;
    grounding.forEach(function (g) {
      attention.forEach(function (a) {
        overlap = Math.max(overlap, bboxOverlap(g.bbox, a.bbox_hint || {}));
      });
    });
    var textScore = 0;
    grounding.forEach(function (g) { textScore = Math.max(textScore, g.text_likelihood || 0); });
    if ((vlm.suggested_followup_models || []).indexOf("ocr") >= 0) textScore = Math.max(textScore, 0.55);

    var agreement, followup, priority, conflictType, admission;
    if (fixtureConfig.route_a_miss || !grounding.length) {
      agreement = "route_a_miss_route_b_only";
      followup = "manual_review";
      priority = "downgrade";
      conflictType = "none";
      admission = "manual_review_only";
    } else if (fixtureConfig.route_conflict || grounding.some(function (g) {
      return g.detected_label_candidate === "person_candidate";
    }) && attention.some(function (a) { return /sign|ocr|text/.test(a.region_hint + a.attention_reason_candidate); })) {
      agreement = "conflict";
      followup = "conflict_review";
      priority = "block_auto_admission";
      conflictType = "label_semantic_conflict";
      admission = "block_auto_admission";
    } else if (overlap >= 0.45 && textScore >= 0.7) {
      agreement = "high_overlap";
      followup = "ocr_task_candidate";
      priority = "boost";
      conflictType = "none";
      admission = "task_candidate_only";
    } else if (overlap >= 0.2) {
      agreement = "partial_overlap";
      followup = textScore < 0.5 ? "detection_task_candidate" : "ocr_task_candidate";
      priority = "neutral";
      conflictType = "none";
      admission = "task_candidate_only";
    } else {
      agreement = "no_overlap";
      followup = "manual_review";
      priority = "downgrade";
      conflictType = "region_mismatch";
      admission = "manual_review_only";
    }

    var cmpId = uid("drc");
    return {
      comparison_id: cmpId,
      route_a_refs: grounding.map(function (g) { return g.candidate_id; }),
      route_b_refs: [vlm.candidate_id],
      agreement_level: agreement,
      conflict_type: conflictType,
      region_overlap_score: overlap,
      text_likelihood_score: textScore,
      recommended_followup_route: followup,
      priority_signal: priority,
      recommended_admission_mode: admission,
      candidate_only: true,
      not_fact: true,
      dual_route_comparison_not_fact: true,
      dual_route_conflict_not_auto_fact: priority === "block_auto_admission",
      trace_chain: [{ stage: "midplatform_dual_route_comparison", ref: cmpId }]
    };
  }

  function buildPackage(envelope, options) {
    options = options || {};
    if (!envelope) return null;
    var imageRef = envelope.test_manifest_ref || envelope._source_file_ref || envelope.envelope_id || "local";
    var sceneType = inferScene(envelope);
    var fixtureConfig = options.fixtureConfig || envelope.dual_route_fixture_config || {};
    var routeA = buildRouteA(imageRef, sceneType, fixtureConfig);
    var routeB = buildRouteB(imageRef, sceneType, fixtureConfig);
    var comparison = compareRoutes(routeA, routeB, fixtureConfig);
    return {
      execution_mode: "deterministic_stub",
      no_model_call: true,
      no_slam_text_detection: true,
      no_slam_text_recognition: true,
      no_slam_ocr_route_direct_generation: true,
      route_a: routeA,
      route_b: routeB,
      dual_route_comparison_candidate: comparison,
      candidate_only: true,
      not_fact: true
    };
  }

  global.DualRoutePerceptionState = {
    version: "dual_route_perception_state_v1",
    buildPackage: buildPackage,
    inferScene: inferScene,
    dual_route_comparison_not_fact: true,
    no_vlm_execution: true,
    no_grounding_real_model_call: true,
    no_vlm_real_model_call: true
  };
})(typeof window !== "undefined" ? window : this);

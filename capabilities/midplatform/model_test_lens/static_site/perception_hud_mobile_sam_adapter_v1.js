/**
 * Model Test Lens — Perception HUD MobileSAM adapter v1.
 * Generates display-only scene annotations and reasoning panel from envelope.
 * prompt_label remains candidate-only; never upgraded to fact.
 */
(function (global) {
  "use strict";

  var Ex = global.VisualOverlayExamples;
  var I18n = global.LunaObservationLabelI18n;
  var Display = function () { return global.PromptLabelDisplayPolicy; };
  var ScenePolicy = function () { return global.SceneProfilePolicy; };

  function taskSemanticName(layer) {
    var D = Display();
    var pid = (layer && layer.label) || (layer && layer.layer_id) || "";
    if (D) return D.taskSemanticShort(pid, layer);
    return "观察候选";
  }

  function humanizeLabel(label, layer) {
    if (layer && layer.display_task_semantic) {
      var D = Display();
      return D ? D.taskSemanticShort(label, layer) : String(layer.display_task_semantic);
    }
    var D2 = Display();
    if (D2 && label) return D2.taskSemanticShort(label, layer);
    if (I18n && I18n.mobileSamLabel) {
      var legacy = I18n.mobileSamLabel(label);
      if (D2 && D2.isForbiddenMainLabel(legacy)) return D2.taskSemanticShort(label, layer);
      return legacy;
    }
    if (!label) return "识别区域候选";
    return String(label).replace(/_/g, " ") + "候选";
  }

  var SEMANTIC_RISK_KEYWORDS = [
    "vehicle", "person", "pedestrian", "sign", "traffic", "crosswalk", "road"
  ];

  var SEMANTIC_OCR_KEYWORDS = ["sign", "text", "advertisement", "screen", "plate"];

  function inferSpatialRelation(bbox, imgW) {
    if (!bbox || !imgW) return "unknown";
    var cx = bbox.x + bbox.w / 2;
    var ratio = cx / imgW;
    if (ratio < 0.33) return "left";
    if (ratio > 0.66) return "right";
    return "center";
  }

  function inferTaskRelevance(label, confidence) {
    var low = label.toLowerCase();
    if (confidence != null && confidence < 0.72) return "needs_confirmation";
    for (var i = 0; i < SEMANTIC_RISK_KEYWORDS.length; i++) {
      if (low.indexOf(SEMANTIC_RISK_KEYWORDS[i]) >= 0) return "possible_risk";
    }
    if (low.indexOf("background") >= 0 || low.indexOf("sky") >= 0) return "background";
    return "relevant";
  }

  function inferUncertaintyTags(label, confidence) {
    var tags = [];
    if (confidence != null && confidence < 0.75) tags.push("low_confidence");
    if (confidence != null && confidence < 0.85) tags.push("boundary_uncertain");
    var low = label.toLowerCase();
    for (var i = 0; i < SEMANTIC_RISK_KEYWORDS.length; i++) {
      if (low.indexOf(SEMANTIC_RISK_KEYWORDS[i]) >= 0) {
        tags.push("missing_tracking");
        break;
      }
    }
    for (var j = 0; j < SEMANTIC_OCR_KEYWORDS.length; j++) {
      if (low.indexOf(SEMANTIC_OCR_KEYWORDS[j]) >= 0) tags.push("missing_ocr");
    }
    tags.push("need_next_frame");
    return tags.filter(function (t, idx, arr) { return arr.indexOf(t) === idx; });
  }

  function entityTypeFromLabel(label) {
    var low = (label || "").toLowerCase();
    if (low.indexOf("people") >= 0 || low.indexOf("person") >= 0 || low.indexOf("pedestrian") >= 0) return "person";
    if (low.indexOf("vehicle") >= 0 || low.indexOf("train_door") >= 0) return "vehicle";
    if (low.indexOf("floor") >= 0 || low.indexOf("walkable") >= 0 || low.indexOf("crosswalk") >= 0) return "road_structure";
    if (low.indexOf("building") >= 0 || low.indexOf("structure") >= 0) return "landmark";
    if (low.indexOf("station") >= 0 || low.indexOf("sign") >= 0 || low.indexOf("route") >= 0 || low.indexOf("text") >= 0) return "text";
    if (low.indexOf("advertisement") >= 0 || low.indexOf("screen") >= 0) return "text";
    return "region";
  }

  function createSceneAnnotation(envelope) {
    var sourceRef = Ex.pickSourceImageRef(envelope);
    var layers = Ex.buildOverlayLayers(envelope);
    if (!sourceRef) {
      return { ok: false, error: "missing_source_image", message: "缺少原图，无法生成机器人视角。" };
    }
    if (!layers.length) {
      return { ok: false, error: "missing_masks", message: "模型结果中没有可显示的识别区域。" };
    }

    var sceneProfile = envelope.scene_profile_candidate;
    if (!sceneProfile && ScenePolicy()) sceneProfile = ScenePolicy().inferFromEnvelope(envelope);
    var sceneType = (sceneProfile && sceneProfile.scene_type_candidate) || "general_scene_understanding";
    var taskContext = {
      task_name: sceneType === "subway_platform" ? "查看地铁站台画面" : "查看当前街景画面",
      task_goal: "查看这张图中哪些区域值得观察，判断哪些结果可信、哪些需要复核。",
      task_context_type: ScenePolicy() ? ScenePolicy().taskContextForScene(sceneType) : "general_scene_understanding",
      scene_profile_candidate: sceneProfile,
      test_mode: true
    };

    if (global.SegmentationPromptPolicy) {
      global.SegmentationPromptPolicy.enrichEnvelopeLayers(envelope);
    }

    var entities = layers.map(function (layer, i) {
      if (global.PromptLabelDisplayPolicy) global.PromptLabelDisplayPolicy.enrichLayerMeta(layer);
      var label = layer.label || layer.layer_id || "region";
      var conf = layer.confidence;
      var taskSemantic = taskSemanticName(layer);
      return {
        entity_id: layer.overlay_layer_id || layer.layer_id || "entity_" + i,
        display_name: humanizeLabel(label, layer),
        entity_type: entityTypeFromLabel(label),
        geometry_type: "mask",
        geometry_ref: layer.artifact_ref,
        label: label,
        label_source: "source_prompt_hint",
        source_prompt_hint: layer.source_prompt_hint || (label + "_prompt"),
        original_prompt_label: label,
        task_semantic_candidate: taskSemantic,
        prompt_is_not_fact: true,
        display_label_source: "midplatform_task_semantics",
        ocr_route_candidate: !!layer.ocr_route_candidate,
        confidence: conf,
        spatial_relation: "unknown",
        task_relevance: inferTaskRelevance(label, conf),
        uncertainty_tags: inferUncertaintyTags(label, conf),
        evidence_refs: [layer.artifact_ref].filter(Boolean),
        candidate_only: true,
        _overlay: layer
      };
    });

    if (global.HudColorSemantics) {
      entities.forEach(function (e) {
        global.HudColorSemantics.applyToEntity(e, taskContext);
      });
    }

    if (global.HudLabelLayoutPolicy) {
      global.HudLabelLayoutPolicy.assignNumbers(entities);
    }

    return {
      ok: true,
      annotation: {
        annotation_id: "phud_annotation_" + (envelope.envelope_id || "local"),
        source_envelope_ref: envelope.envelope_id || "local_envelope",
        source_image_ref: sourceRef,
        model_id: envelope.model_id || "mobile_sam",
        model_category: envelope.model_category || "segmentation",
        task_context: taskContext,
        scene_profile_candidate: sceneProfile,
        segmentation_prompt_policy: envelope.segmentation_prompt_policy,
        entities: entities,
        candidate_only: true,
        not_fact: true
      },
      layers: layers,
      sourceImageRef: sourceRef
    };
  }

  function createReasoningPanel(envelope, annotation) {
    var entities = (annotation && annotation.entities) || [];
    var metrics = envelope.metrics || {};
    var perCat = metrics.per_category_average_score || {};
    var sceneProfile = (annotation && annotation.scene_profile_candidate) ||
      (envelope && envelope.scene_profile_candidate);
    var sceneType = (sceneProfile && sceneProfile.scene_type_candidate) || "general_scene_understanding";
    var lowConf = entities.filter(function (e) {
      return e.confidence != null && e.confidence < 0.75;
    });
    var stable = entities.filter(function (e) {
      return e.confidence != null && e.confidence >= 0.85;
    });

    var observations = [
      "画面中共标出 " + entities.length + " 个候选区域。",
      stable.length
        ? "部分大区域边界较稳定，可作为结构观察参考。"
        : "当前各区域置信度普遍需要进一步确认。"
    ];

    var goalJudgment = [
      sceneType === "subway_platform"
        ? "当前任务聚焦：站台导视/文字观察候选与通行结构区域。"
        : "当前任务聚焦：道路通行相关区域与潜在风险目标。",
      "分割结果仅提供边界，不能单独作为类别判断依据。"
    ];

    var reasoning = [
      {
        step: 1,
        text: "这些区域来自图像分割模型的结果，说明模型找到了可能有意义的视觉边界。",
        evidence_refs: entities.map(function (e) { return e.geometry_ref; }).slice(0, 3)
      },
      {
        step: 2,
        text: "但分割模型不是目标检测模型，不能单独证明这些区域的真实类别。",
        uncertainty_refs: ["prompt_label_candidate_only"]
      },
      {
        step: 3,
        text: "分割提示标签仅表示测试时使用的提示词，属于候选判断，不是事实标签。",
        uncertainty_refs: ["label_source_prompt_label"]
      }
    ];

    var uncertainty = [
      "分割结果不能直接证明真实类别。",
      "车辆、路牌、行人需要目标检测或文字识别复核。",
      lowConf.length ? "低置信度区域不能作为稳定识别结果。" : "建议结合多组分割提示交叉验证。"
    ];

    var missing = [];
    if (!Object.keys(perCat).length && !entities.length) {
      missing.push("当前结果只包含指标，暂时无法生成完整机器人视角。");
    }
    missing.push("缺少跟踪与深度信息，无法判断运动方向或距离。");
    if (entities.some(function (e) {
      return (e.label || "").toLowerCase().indexOf("sign") >= 0;
    })) {
      missing.push("路牌文字区域需要文字识别复核。");
    }
    if (entities.some(function (e) {
      return (e.label || "").toLowerCase().indexOf("vehicle") >= 0;
    })) {
      missing.push("车辆候选区域需要目标检测确认类别与数量。");
    }
    missing.push("可能漏掉远处小目标或未提示的物体。");

    var recommendations = [
      {
        action_type: "supplement_test",
        text: "接入目标检测，确认车辆和行人。"
      },
      {
        action_type: "supplement_test",
        text: "接入文字识别，检查路牌和广告文字。"
      },
      {
        action_type: "human_review",
        text: "建议保留当前结果作为候选，不进入事实层。"
      }
    ];

    return {
      reasoning_panel_id: "phud_reasoning_" + (envelope.envelope_id || "local"),
      source_annotation_ref: annotation.annotation_id,
      current_task: {
        task_name: "查看当前画面中的识别结果",
        task_goal: "查看这张图中哪些区域被模型识别，判断哪些结果可信、哪些需要复核。",
        task_context: "general_scene_understanding",
        test_mode: true
      },
      system_observations: observations,
      goal_judgment: goalJudgment,
      reasoning_steps: reasoning,
      uncertainty_summary: uncertainty,
      missing_information: missing,
      risks_and_gaps: {
        missing_objects: ["交通灯", "完整斑马线", "远处行人"],
        low_confidence_items: lowConf.map(function (e) { return humanizeLabel(e._overlay && e._overlay.label ? e._overlay.label : e.label); }),
        possible_false_positive: ["分割提示标签可能与真实物体不完全对应"],
        possible_false_negative: ["未提示的物体不会出现在分割结果中"],
        model_limitations: [
          "图像分割模型仅提供区域边界，不提供语义检测",
          "不能独立证明车辆/建筑/道路等类别"
        ]
      },
      recommended_next_steps: recommendations,
      compressed_view: global.HudReasoningCompression
        ? global.HudReasoningCompression.buildFromLegacy({
          current_task: {
            task_name: "查看当前街景画面",
            task_goal: "判断哪些区域可信、哪些需要复核，不进入事实层。",
            test_mode: true
          },
          system_observations: observations,
          goal_judgment: goalJudgment,
          uncertainty_summary: uncertainty.slice(0, 2),
          missing_information: missing.slice(0, 1),
          recommended_next_steps: recommendations.slice(0, 2),
          reasoning_steps: reasoning
        })
        : null,
      human_review_required: true,
      candidate_only: true,
      not_fact: true,
      not_navigation_instruction: true,
      not_speech_output: true
    };
  }

  global.PerceptionHUDMobileSAMAdapter = {
    createSceneAnnotation: createSceneAnnotation,
    createReasoningPanel: createReasoningPanel,
    inferSpatialRelation: inferSpatialRelation,
    humanizeLabel: humanizeLabel
  };
})(typeof window !== "undefined" ? window : this);

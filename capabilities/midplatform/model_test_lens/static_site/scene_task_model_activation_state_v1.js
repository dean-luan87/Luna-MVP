/**
 * Scene-Task Model Activation — deterministic state builder (browser, no runner execution).
 */
(function (global) {
  "use strict";

  var ALL_MODELS = [
    "ocr_text_detector", "ocr_recognizer", "detection", "depth",
    "tracking", "slam", "vlm_route_enhancer", "mobile_sam_region_proposal"
  ];

  function uid(prefix) {
    return prefix + "_" + Math.random().toString(36).slice(2, 10);
  }

  function trace(stage, ref) {
    return { stage: stage, ref: ref };
  }

  function normalizeSceneType(sceneType) {
    if (sceneType === "outdoor_street") return "outdoor_street_crossing";
    if (sceneType === "indoor_station") return "subway_platform";
    return sceneType || "unknown_scene";
  }

  function inferScene(envelope) {
    if (envelope && envelope.scene_profile_candidate) {
      var sp = Object.assign({}, envelope.scene_profile_candidate);
      sp.scene_type_candidate = normalizeSceneType(sp.scene_type_candidate);
      return sp;
    }
    if (global.SceneProfilePolicy) {
      var inferred = global.SceneProfilePolicy.inferFromEnvelope(envelope);
      if (inferred) {
        inferred.scene_type_candidate = normalizeSceneType(inferred.scene_type_candidate);
        return inferred;
      }
    }
    return {
      scene_profile_id: uid("spc"),
      scene_type_candidate: "unknown_scene",
      confidence: 0.5,
      evidence_refs: [],
      candidate_only: true,
      not_fact: true,
      scene_profile_candidate_not_fact: true
    };
  }

  function inferTaskIntent(sceneType, options) {
    options = options || {};
    if (options.task_intent_candidate) return options.task_intent_candidate;
    if (options.correction_signal && options.correction_signal.task_type_candidate) {
      return {
        task_intent_id: uid("tic"),
        task_type_candidate: options.correction_signal.task_type_candidate,
        source: "correction_signal",
        confidence: 0.9,
        candidate_only: true,
        not_fact: true,
        task_intent_candidate_not_fact: true,
        trace_chain: [trace("task_intent_candidate", "correction")]
      };
    }
    if (options.user_goal_candidate && options.user_goal_candidate.task_type_candidate) {
      return {
        task_intent_id: uid("tic"),
        task_type_candidate: options.user_goal_candidate.task_type_candidate,
        source: "user_goal",
        confidence: options.user_goal_candidate.confidence || 0.86,
        candidate_only: true,
        not_fact: true,
        task_intent_candidate_not_fact: true,
        trace_chain: [trace("task_intent_candidate", "user_goal")]
      };
    }
    var taskMap = {
      shopfront_sign: "read_text",
      text_signage_scene: "read_text",
      subway_platform: options.navigation_context ? "find_direction" : "read_text",
      outdoor_street_crossing: "assess_walkable_area",
      corridor: "assess_walkable_area",
      indoor_navigation: "locate_place",
      unknown_scene: "manual_review"
    };
    var taskType = taskMap[sceneType] || "understand_scene";
    var tid = uid("tic");
    return {
      task_intent_id: tid,
      task_type_candidate: taskType,
      source: "scene_policy",
      confidence: 0.84,
      candidate_only: true,
      not_fact: true,
      task_intent_candidate_not_fact: true,
      trace_chain: [trace("task_intent_candidate", tid)]
    };
  }

  function extractTextRegionIds(attentionPkg, sceneType) {
    var ids = [];
    var records = (attentionPkg && attentionPkg.records) || [];
    records.forEach(function (rec) {
      var blob = [
        rec.attention_reason, rec.task_semantic, rec.region_semantic, rec.hud_short_label, rec.label_candidate
      ].join(" ").toLowerCase();
      if (/text|sign|ocr|导视|文字|站名|店招/.test(blob)) {
        ids.push(rec.region_id || rec.entity_id || uid("tr"));
      }
    });
    if (!ids.length) {
      if (sceneType === "shopfront_sign" || sceneType === "text_signage_scene") {
        ids.push("shop_sign_text_region_001");
      } else if (sceneType === "subway_platform") {
        ids.push("subway_direction_sign_region_001");
      } else if (sceneType === "outdoor_street_crossing") {
        ids.push("street_sign_text_region_001");
      }
    }
    return ids;
  }

  function extractRegionIds(attentionPkg, sceneType) {
    var ids = [];
    var records = (attentionPkg && attentionPkg.records) || [];
    records.forEach(function (rec) {
      var blob = [
        rec.attention_reason, rec.task_semantic, rec.region_semantic, rec.hud_short_label
      ].join(" ").toLowerCase();
      if (/walk|vehicle|person|cross|dynamic|obstacle|platform|floor/.test(blob)) {
        ids.push(rec.region_id || rec.entity_id || uid("rg"));
      }
    });
    if (!ids.length && sceneType === "corridor") ids.push("corridor_walkable_candidate");
    if (!ids.length && sceneType === "outdoor_street_crossing") {
      ids.push("crosswalk_candidate", "vehicle_lane_candidate");
    }
    return ids;
  }

  function hasDynamicTargets(attentionPkg, sceneType) {
    if (sceneType === "outdoor_street_crossing") return true;
    var records = (attentionPkg && attentionPkg.records) || [];
    return records.some(function (rec) {
      var blob = [rec.attention_reason, rec.task_semantic, rec.hud_short_label].join(" ").toLowerCase();
      return /vehicle|person|dynamic|moving|track/.test(blob);
    });
  }

  function buildModelActivationPlan(imageRef, scene, task, opts) {
    opts = opts || {};
    var sceneType = scene.scene_type_candidate;
    var taskType = task.task_type_candidate;
    var sceneRef = scene.scene_profile_id;
    var taskRef = task.task_intent_id;
    var textRegionIds = opts.text_region_ids || [];
    var regionIds = opts.region_ids || [];
    var activated = [];
    var assignments = [];
    var noopReasons = {};
    var textTasks = { read_text: 1, find_direction: 1, locate_place: 1 };
    var spatialTasks = { assess_walkable_area: 1, track_dynamic_target: 1, identify_object: 1 };
    var textScenes = { text_signage_scene: 1, shopfront_sign: 1, subway_platform: 1, indoor_navigation: 1 };

    function activate(model, reason, assignKw) {
      assignKw = assignKw || {};
      activated.push({
        model_name: model,
        activation_reason: reason,
        allowed_runner_type: assignKw.runner_type || "controlled_runner_candidate",
        candidate_only: true,
        not_fact: true
      });
      assignments.push({
        assignment_id: uid("mra"),
        model_name: model,
        assigned_region_ids: assignKw.region_ids || [],
        assigned_text_region_ids: assignKw.text_region_ids || [],
        assignment_reason: reason,
        input_constraints: { execution_stub: true, no_runner_execution: true },
        allowed_runner_type: assignKw.runner_type || "controlled_runner_candidate",
        candidate_only: true,
        not_fact: true,
        trace_chain: [trace("model_region_assignment", model)]
      });
    }

    function setNoop(model, reason) {
      noopReasons[model] = reason;
    }

    if (sceneType === "outdoor_street_crossing" && textRegionIds.length) {
      activate("ocr_text_detector", "sign/text region only; not blanket OCR",
        { text_region_ids: textRegionIds, runner_type: "ocr_task_candidate" });
      activate("ocr_recognizer", "sign/text region only",
        { text_region_ids: textRegionIds, runner_type: "ocr_task_candidate" });
    } else if (textTasks[taskType] && textScenes[sceneType] && textRegionIds.length) {
      activate("ocr_text_detector", "task=" + taskType + "; scene=" + sceneType + "; text_likelihood_high",
        { text_region_ids: textRegionIds, runner_type: "ocr_task_candidate" });
      activate("ocr_recognizer", "task=" + taskType + "; follows text_detector for sign reading",
        { text_region_ids: textRegionIds, runner_type: "ocr_task_candidate" });
    } else {
      if (spatialTasks[taskType] && sceneType !== "unknown_scene" && sceneType !== "outdoor_street_crossing") {
        setNoop("ocr_text_detector", "task is spatial/dynamic; no blanket OCR");
        setNoop("ocr_recognizer", "task is spatial/dynamic; no blanket OCR");
      } else if (sceneType === "corridor" && !textRegionIds.length) {
        setNoop("ocr_text_detector", "pure spatial navigation; no text region");
        setNoop("ocr_recognizer", "pure spatial navigation; no text region");
      } else if (sceneType === "unknown_scene") {
        setNoop("ocr_text_detector", "unknown scene; pending VLM route or manual_review");
        setNoop("ocr_recognizer", "unknown scene; pending VLM route or manual_review");
      } else if (sceneType === "outdoor_street_crossing" && !textRegionIds.length) {
        setNoop("ocr_text_detector", "street crossing; no sign/text region candidate");
        setNoop("ocr_recognizer", "street crossing; no sign/text region candidate");
      } else {
        setNoop("ocr_text_detector", "no text_likelihood or task not text-primary");
        setNoop("ocr_recognizer", "no text_likelihood or task not text-primary");
      }
    }

    var slamActivate = false;
    if (opts.spatial_continuity_requested || opts.navigation_context) slamActivate = true;
    else if (sceneType === "corridor" && (taskType === "assess_walkable_area" || taskType === "understand_scene")) {
      slamActivate = true;
    } else if (textTasks[taskType] && (sceneType === "shopfront_sign" || sceneType === "text_signage_scene")) {
      slamActivate = false;
    } else if (textTasks[taskType] && sceneType === "subway_platform" && !opts.navigation_context) {
      slamActivate = false;
    }

    if (slamActivate) {
      activate("slam", "spatial continuity; scene=" + sceneType + "; task=" + taskType,
        { region_ids: regionIds, runner_type: "slam_task_candidate" });
    } else if (textTasks[taskType]) {
      setNoop("slam", "task_intent=" + taskType + "; no spatial continuity required");
    } else {
      setNoop("slam", "scene=" + sceneType + "; spatial continuity not requested");
    }

    if ((taskType === "identify_object" || taskType === "track_dynamic_target" || taskType === "assess_walkable_area") &&
        (opts.object_candidates || opts.dynamic_targets || sceneType === "outdoor_street_crossing")) {
      activate("detection", "task=" + taskType + "; object/dynamic candidate in " + sceneType,
        { region_ids: regionIds.length ? regionIds : ["full_frame_candidate"], runner_type: "detection_task_candidate" });
    } else if (opts.safety_context && sceneType === "subway_platform") {
      activate("detection", "optional safety context for people/doors",
        { region_ids: ["platform_safety_zone_candidate"], runner_type: "detection_task_candidate" });
    } else {
      setNoop("detection", "task is text-only or no object-like target");
    }

    if (taskType === "assess_walkable_area" || taskType === "track_dynamic_target" ||
        sceneType === "outdoor_street_crossing" || sceneType === "corridor") {
      if (taskType === "read_text" && (sceneType === "shopfront_sign" || sceneType === "text_signage_scene")) {
        setNoop("depth", "pure text reading; no distance/walkable risk");
      } else if (sceneType === "corridor" || sceneType === "outdoor_street_crossing") {
        activate("depth", "spatial risk / walkable assessment; scene=" + sceneType,
          { region_ids: regionIds.length ? regionIds : ["walkable_area_candidate"], runner_type: "depth_task_candidate" });
      } else {
        setNoop("depth", "no spatial risk requirement");
      }
    } else {
      setNoop("depth", "no distance/walkable risk requirement");
    }

    if (opts.dynamic_targets || taskType === "track_dynamic_target") {
      activate("tracking", "dynamic target / multi-frame review",
        { region_ids: regionIds.length ? regionIds : ["dynamic_target_candidate"], runner_type: "tracking_task_candidate" });
    } else {
      setNoop("tracking", "static scene or text-only; no dynamic target tracking");
    }

    if (sceneType === "unknown_scene" || taskType === "manual_review") {
      activate("vlm_route_enhancer", "unknown scene or manual_review; high-level route candidate",
        { runner_type: "vlm_route_candidate" });
    } else {
      setNoop("vlm_route_enhancer", "task clear and covered by specialized models");
    }

    if ((sceneType === "shopfront_sign" || sceneType === "text_signage_scene") && taskType === "read_text") {
      setNoop("mobile_sam_region_proposal", "text-first scene; SAM not primary text detector");
    } else if (sceneType === "unknown_scene") {
      setNoop("mobile_sam_region_proposal", "unknown scene; pending VLM route");
    } else {
      setNoop("mobile_sam_region_proposal", "region refine deferred; not primary activation path");
    }

    var activeNames = {};
    activated.forEach(function (a) { activeNames[a.model_name] = true; });
    ALL_MODELS.forEach(function (m) {
      if (!activeNames[m] && !noopReasons[m]) noopReasons[m] = "not selected by activation policy";
    });

    var noopSet = ALL_MODELS.filter(function (m) { return !activeNames[m]; }).map(function (m) {
      return {
        model_name: m,
        noop_reason: noopReasons[m],
        scene_profile_ref: sceneRef,
        task_intent_ref: taskRef,
        policy_ref: "scene_task_model_activation_policy_v1",
        candidate_only: true,
        not_fact: true
      };
    });

    var followupTasks = assignments.filter(function (a) {
      return activeNames[a.model_name] && (a.allowed_runner_type || "").indexOf("_task_candidate") >= 0;
    }).map(function (a) {
      return {
        task_candidate_id: uid("frtc"),
        model_name: a.model_name,
        runner_task_type: a.allowed_runner_type,
        assigned_region_ids: a.assigned_region_ids || [],
        assigned_text_region_ids: a.assigned_text_region_ids || [],
        candidate_only: true,
        not_fact: true,
        no_runner_execution: true
      };
    });

    var followup = "manual_review";
    if (activeNames.ocr_text_detector) followup = "ocr_task_candidate";
    if (activeNames.vlm_route_enhancer) followup = "vlm_route_candidate";
    else if (activeNames.detection && !activeNames.ocr_text_detector) followup = "detection_task_candidate";
    else if (activeNames.slam && !activeNames.ocr_text_detector) followup = "slam_task_candidate";

    var planId = uid("map");
    return {
      plan_id: planId,
      image_ref: imageRef,
      scene_profile_ref: sceneRef,
      task_intent_ref: taskRef,
      scene_profile_candidate: scene,
      task_intent_candidate: task,
      model_activation_plan_candidate: true,
      activated_model_set: activated,
      model_noop_set: noopSet,
      model_region_assignment: assignments,
      followup_runner_task_candidates: followupTasks,
      activation_summary: "scene=" + sceneType + "; task=" + taskType,
      recommended_followup_runner_task_candidate: followup,
      candidate_only: true,
      not_fact: true,
      model_activation_candidate_not_fact: true,
      no_fact_write: true,
      no_runner_execution_in_activation_execution: true,
      execution_mode: "deterministic_stub",
      no_model_call: true,
      trace_chain: [
        trace("input_image", imageRef),
        trace("scene_profile_candidate", sceneRef),
        trace("task_intent_candidate", taskRef),
        trace("model_activation_plan_candidate", planId)
      ]
    };
  }

  function buildPackage(envelope, options) {
    options = options || {};
    if (!envelope) return null;
    if (envelope.model_category !== "segmentation" && envelope.model_id !== "mobile_sam") return null;

    var imageRef = envelope.test_manifest_ref || envelope._source_file_ref || envelope.envelope_id || "local";
    var scene = inferScene(envelope);
    var sceneType = scene.scene_type_candidate;
    var task = inferTaskIntent(sceneType, options);
    var attentionPkg = options.attentionPkg || null;
    var textRegionIds = options.text_region_ids || extractTextRegionIds(attentionPkg, sceneType);
    var regionIds = options.region_ids || extractRegionIds(attentionPkg, sceneType);

    var plan = buildModelActivationPlan(imageRef, scene, task, {
      text_region_ids: textRegionIds,
      region_ids: regionIds,
      spatial_continuity_requested: !!options.spatial_continuity_requested,
      navigation_context: !!options.navigation_context,
      object_candidates: sceneType === "outdoor_street_crossing" || !!options.object_candidates,
      dynamic_targets: hasDynamicTargets(attentionPkg, sceneType),
      safety_context: sceneType === "subway_platform" && !!options.safety_context
    });

    return {
      execution_mode: "deterministic_stub",
      no_model_call: true,
      no_runner_execution_in_activation_execution: true,
      model_activation_plan_candidate: plan,
      activated_model_set: plan.activated_model_set,
      model_noop_set: plan.model_noop_set,
      model_region_assignment: plan.model_region_assignment,
      followup_runner_task_candidates: plan.followup_runner_task_candidates,
      recommended_followup_runner_task_candidate: plan.recommended_followup_runner_task_candidate,
      scene_profile_candidate: plan.scene_profile_candidate,
      task_intent_candidate: plan.task_intent_candidate,
      candidate_only: true,
      not_fact: true,
      model_activation_candidate_not_fact: true
    };
  }

  global.SceneTaskModelActivationState = {
    version: "scene_task_model_activation_state_v1",
    buildPackage: buildPackage,
    buildModelActivationPlan: buildModelActivationPlan,
    inferScene: inferScene,
    inferTaskIntent: inferTaskIntent,
    model_activation_candidate_not_fact: true,
    no_ocr_execution: true,
    no_detection_execution: true,
    no_vlm_execution: true,
    no_slam_execution: true,
    no_runner_execution_in_activation_execution: true
  };
})(typeof window !== "undefined" ? window : this);

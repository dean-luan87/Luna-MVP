/**
 * Luna Situation Understanding — browser state builder (dry-run, no runner execution).
 */
(function (global) {
  "use strict";

  var SHOPFRONT_FILES = ["ocr_real_image_shop_sign", "shop_sign", "shopfront"];
  var SUBWAY_FILES = ["subway_direction_sign_jiahuihu", "jiahuihu", "subway"];
  var STREET_HINTS = ["crosswalk_hint", "vehicle_hint", "person_hint", "open_road"];
  var CORRIDOR_HINTS = ["corridor_lines", "indoor_path", "spatial_boundary"];
  var SHOPFRONT_HINTS = ["large_text_density", "storefront_layout", "logo_region"];
  var SUBWAY_HINTS = ["platform_screen_door", "direction_sign_text_density", "public_transport_hint"];

  function uid(prefix) {
    return prefix + "_" + Math.random().toString(36).slice(2, 10);
  }

  function evidenceValues(input) {
    return (input.visual_evidence_candidates || []).map(function (e) { return e.value; });
  }

  function hasEvidence(input, hints) {
    var vals = evidenceValues(input);
    return hints.some(function (h) { return vals.indexOf(h) >= 0; });
  }

  function envelopeToJob(envelope) {
    var fileName = envelope._source_file_name || envelope.test_case_id || "";
    if (!fileName && envelope.input_asset_refs && envelope.input_asset_refs[0]) {
      fileName = String(envelope.input_asset_refs[0]).split("/").pop();
    }
    var runnerScene = envelope.scene_profile_candidate && envelope.scene_profile_candidate.scene_type_candidate;
    var promptSet = envelope.segmentation_prompt_policy && envelope.segmentation_prompt_policy.prompt_set_id;
    var promptResults = (envelope.segmentation_results || envelope.prompt_results || []).map(function (r, i) {
      return {
        prompt_id: r.prompt_id || r.region_id || ("generic_region_candidate_" + (i + 1)),
        ocr_route_candidate: r.ocr_route_candidate === true,
        score: r.score || 0.8
      };
    });
    if (!promptResults.length && envelope.entities) {
      promptResults = envelope.entities.slice(0, 5).map(function (e, i) {
        return {
          prompt_id: e.entity_id || ("generic_region_candidate_" + (i + 1)),
          ocr_route_candidate: false,
          score: 0.8
        };
      });
    }
    return {
      job_id: envelope.job_id || envelope.envelope_id || uid("job"),
      source: "replay",
      created_at: envelope.created_at || new Date().toISOString(),
      asset_manifest: { file_name: fileName, asset_id: uid("asset") },
      runner_scene_hint_optional: runnerScene,
      prompt_set_id_optional: promptSet,
      runner_result: {
        scene_profile_candidate: envelope.scene_profile_candidate || { scene_type_candidate: runnerScene },
        segmentation_prompt_policy: envelope.segmentation_prompt_policy || { prompt_set_id: promptSet },
        prompt_results: promptResults
      },
      user_goal_candidate_optional: envelope.user_goal_candidate || { goal_type: "unknown", confidence: 0.2, source: "unknown" },
      dryrun_extra_evidence: envelope._situation_extra_evidence || [],
      dryrun_case_ref_key: envelope._situation_case_ref_key || null,
      situation_case_refs_optional: envelope._situation_case_refs || []
    };
  }

  function extractFrameContext(job) {
    var manifest = job.asset_manifest || {};
    return {
      frame_id: "frame_" + (job.job_id || manifest.file_name),
      image_id: manifest.asset_id || uid("img"),
      file_name: manifest.file_name || "",
      timestamp: job.created_at || "",
      source: job.source || "replay",
      job_id_optional: job.job_id || "",
      candidate_only: true,
      not_fact: true
    };
  }

  function extractRunnerEvidence(job) {
    var hint = job.runner_scene_hint_optional;
    var runner = job.runner_result || {};
    if (!hint && runner.scene_profile_candidate) {
      hint = runner.scene_profile_candidate.scene_type_candidate;
    }
    if (!hint) return null;
    return {
      evidence_id: uid("ev_runner"),
      source: "runner_scene_hint",
      evidence_type: "scene_hint",
      value: hint,
      confidence: (runner.scene_profile_candidate && runner.scene_profile_candidate.confidence) || 0.55,
      source_trace_ref: job.job_id || "",
      candidate_only: true,
      not_fact: true
    };
  }

  function extractVisualEvidence(job) {
    var evidence = [];
    var fileName = ((job.asset_manifest && job.asset_manifest.file_name) || "").toLowerCase();
    var runnerEv = extractRunnerEvidence(job);
    if (runnerEv) evidence.push(runnerEv);

    function ev(source, etype, value, conf) {
      evidence.push({
        evidence_id: uid("ev"),
        source: source,
        evidence_type: etype,
        value: value,
        confidence: conf || 0.8,
        source_trace_ref: job.job_id || "",
        candidate_only: true,
        not_fact: true
      });
    }

    SHOPFRONT_FILES.forEach(function (k) {
      if (fileName.indexOf(k) >= 0) {
        ev("metadata", "text_density", "large_text_density", 0.85);
        ev("metadata", "scene_hint", "storefront_layout", 0.82);
        ev("metadata", "region", "logo_region", 0.78);
      }
    });
    SUBWAY_FILES.forEach(function (k) {
      if (fileName.indexOf(k) >= 0) {
        ev("metadata", "scene_hint", "platform_screen_door", 0.84);
        ev("text_detector", "text_density", "direction_sign_text_density", 0.86);
        ev("metadata", "scene_hint", "public_transport_hint", 0.8);
      }
    });
    if (fileName.indexOf("street_crossing") >= 0 || fileName.indexOf("crosswalk") >= 0) {
      ev("detection", "scene_hint", "crosswalk_hint", 0.83);
      ev("detection", "object_hint", "vehicle_hint", 0.8);
      ev("detection", "object_hint", "person_hint", 0.78);
      ev("metadata", "spatial_hint", "open_road", 0.76);
    }
    if (fileName.indexOf("corridor") >= 0) {
      ev("metadata", "spatial_hint", "corridor_lines", 0.82);
      ev("depth", "spatial_hint", "indoor_path", 0.8);
      ev("sam", "spatial_hint", "spatial_boundary", 0.78);
    }

    var promptSet = job.prompt_set_id_optional ||
      (job.runner_result && job.runner_result.segmentation_prompt_policy &&
        job.runner_result.segmentation_prompt_policy.prompt_set_id);
    if (promptSet) {
      ev("sam", "scene_hint", "prompt_set:" + promptSet, 0.7);
      if (promptSet.indexOf("generic") >= 0) ev("sam", "region", "generic_sam_regions", 0.65);
    }

    (job.dryrun_extra_evidence || []).forEach(function (e) { evidence.push(e); });
    return evidence;
  }

  function attachCaseRefs(job) {
    if (job.situation_case_refs_optional && job.situation_case_refs_optional.length) {
      return job.situation_case_refs_optional.map(function (ref) {
        if (typeof ref === "string") {
          return { case_id: ref, case_type: ref.replace("_case", ""), similarity_score: 0.85, matched_clues: [], candidate_only: true, not_fact: true };
        }
        return ref;
      });
    }
    var fileName = ((job.asset_manifest && job.asset_manifest.file_name) || "").toLowerCase();
    var refs = [];
    if (SHOPFRONT_FILES.some(function (k) { return fileName.indexOf(k) >= 0; })) {
      refs.push({ case_id: "shopfront_sign_case", case_type: "shopfront_sign", similarity_score: 0.9, matched_clues: ["storefront_layout"], candidate_only: true, not_fact: true });
    }
    if (SUBWAY_FILES.some(function (k) { return fileName.indexOf(k) >= 0; })) {
      refs.push({ case_id: "subway_platform_case", case_type: "subway_platform", similarity_score: 0.88, matched_clues: ["public_transport_hint"], candidate_only: true, not_fact: true });
    }
    if (job.dryrun_case_ref_key) {
      refs.push({ case_id: job.dryrun_case_ref_key, case_type: job.dryrun_case_ref_key.replace("_case", ""), similarity_score: 0.85, matched_clues: [], candidate_only: true, not_fact: true });
    }
    return refs;
  }

  function buildInput(job) {
    return {
      frame_context: extractFrameContext(job),
      user_goal_candidate: Object.assign({
        goal_type: "unknown", confidence: 0.2, source: "unknown", candidate_only: true, not_fact: true
      }, job.user_goal_candidate_optional || {}),
      visual_evidence_candidates: extractVisualEvidence(job),
      situation_case_refs: attachCaseRefs(job),
      environment_memory_candidates: [],
      human_correction_signals: [],
      available_capabilities: [],
      candidate_only: true,
      not_fact: true
    };
  }

  function inferScene(input) {
    var frame = input.frame_context || {};
    var fileName = frame.file_name || "";
    var caseTypes = (input.situation_case_refs || []).map(function (c) { return c.case_type; });
    var runnerHint = null;
    (input.visual_evidence_candidates || []).forEach(function (e) {
      if (e.source === "runner_scene_hint") runnerHint = e.value;
    });
    var sceneType = "unknown_scene";
    var confidence = 0.35;
    var conflictTraces = [];

    if (runnerHint) {
      conflictTraces.push({ stage: "runner_scene_hint_received", ref: runnerHint, resolution: "runner_hint_is_evidence_only_not_owner" });
    }

    if (SHOPFRONT_FILES.some(function (k) { return fileName.indexOf(k) >= 0; }) ||
        caseTypes.indexOf("shopfront_sign") >= 0 || hasEvidence(input, SHOPFRONT_HINTS)) {
      sceneType = "shopfront_sign"; confidence = 0.88;
    } else if (SUBWAY_FILES.some(function (k) { return fileName.indexOf(k) >= 0; }) ||
        caseTypes.indexOf("subway_platform") >= 0 || hasEvidence(input, SUBWAY_HINTS)) {
      sceneType = "subway_platform"; confidence = 0.85;
    } else if (hasEvidence(input, STREET_HINTS)) {
      sceneType = "street_crossing"; confidence = 0.82;
    } else if (hasEvidence(input, CORRIDOR_HINTS)) {
      sceneType = "corridor"; confidence = 0.8;
    }

    if (runnerHint && runnerHint !== sceneType) {
      conflictTraces.push({
        stage: "runner_scene_hint_conflict",
        runner_hint: runnerHint,
        situation_layer_scene: sceneType,
        resolution: "situation_layer_owns_scene_profile",
        policy_ref: "scene_profile_owned_by_situation_layer"
      });
    }

    return {
      scene_type: sceneType,
      confidence: confidence,
      evidence_refs: (input.visual_evidence_candidates || []).map(function (e) { return e.evidence_id || e.value; }),
      case_refs: (input.situation_case_refs || []).map(function (c) { return c.case_id; }),
      owned_by: "situation_understanding_layer",
      candidate_only: true,
      not_fact: true,
      trace_refs: conflictTraces
    };
  }

  function inferSurvival(sceneType, goalType) {
    var envMap = { shopfront_sign: "commercial_entry", subway_platform: "public_transport", street_crossing: "street_mobility", corridor: "indoor_navigation" };
    var mobility = "low", information = "medium", risk = "low", uncertainty = "medium";
    if (sceneType === "shopfront_sign") { information = "high"; mobility = "low"; }
    else if (sceneType === "subway_platform") { information = "high"; mobility = goalType === "navigate" ? "medium" : "low"; }
    else if (sceneType === "street_crossing") { mobility = "high"; risk = "medium"; information = "low"; }
    else if (sceneType === "corridor") { mobility = "high"; information = "low"; }
    else if (sceneType === "unknown_scene") { uncertainty = "high"; risk = "unknown"; mobility = "unknown"; information = "unknown"; }
    return {
      environment_type: envMap[sceneType] || "unknown",
      risk_level: risk,
      mobility_relevance: mobility,
      information_relevance: information,
      social_relevance: "low",
      task_pressure: sceneType === "street_crossing" ? "medium" : "low",
      uncertainty_level: uncertainty,
      candidate_only: true,
      not_fact: true
    };
  }

  function inferTaskClues(sceneType) {
    var clues = [];
    function clue(taskType, priority, reason) {
      clues.push({ task_type: taskType, priority: priority, reason: reason, evidence_refs: [], candidate_only: true, not_fact: true });
    }
    if (sceneType === "shopfront_sign") { clue("read_text", "P0", "店招场景默认需要读取文字"); clue("identify_place", "P1", "店招场景需要识别地点/店名"); }
    else if (sceneType === "subway_platform") { clue("find_direction", "P0", "地铁站场景默认需要找方向"); clue("read_text", "P0", "方向牌/站台信息需要读文字"); }
    else if (sceneType === "street_crossing") { clue("assess_walkable", "P0", "街道路口需要评估可通行性"); clue("avoid_obstacle", "P1", "街道路口需要避让车辆/行人"); }
    else if (sceneType === "corridor") { clue("assess_walkable", "P0", "走廊导航需要评估可通行路径"); }
    else { clue("ask_user", "P0", "未知场景需要用户目标澄清"); clue("manual_review", "P1", "未知场景建议人工复核"); }
    return clues;
  }

  function inferMissing(taskClues) {
    var mapping = {
      read_text: ["text_content", "ocr", "需要读取可见文字内容"],
      identify_place: ["place_identity", "ocr", "需要识别地点/店名"],
      find_direction: ["direction_info", "ocr", "需要方向/指引信息"],
      assess_walkable: ["walkable_area", "depth", "需要可通行区域信息"],
      avoid_obstacle: ["dynamic_motion", "tracking", "需要动态障碍信息"],
      ask_user: ["user_goal", "speech", "需要用户目标澄清"]
    };
    return taskClues.map(function (tc) {
      var m = mapping[tc.task_type];
      if (!m) return null;
      return { info_type: m[0], required_for: tc.task_type, suggested_capability: m[1], reason: m[2], candidate_only: true, not_fact: true };
    }).filter(Boolean);
  }

  function inferAttention(sceneType) {
    var hints = [];
    function hint(targetType, priority, reason) {
      hints.push({ target_hint_id: uid("ath"), target_type: targetType, priority: priority, reason: reason, region_ref_optional: "", candidate_only: true, not_fact: true });
    }
    if (sceneType === "shopfront_sign") { hint("primary_text_block", "P0", "店招主文字区域"); }
    else if (sceneType === "subway_platform") { hint("direction_sign", "P0", "方向指示牌"); }
    else if (sceneType === "street_crossing") { hint("walkable_path", "P0", "可通行路径"); hint("obstacle_candidate", "P1", "车辆/行人障碍"); }
    else if (sceneType === "corridor") { hint("spatial_boundary", "P0", "走廊空间边界"); hint("walkable_path", "P0", "走廊可通行路径"); }
    else { hint("unknown_region", "P0", "未知场景全图需审慎关注"); }
    return hints;
  }

  function inferModelNeeds(sceneType, goalType, hasTextEvidence) {
    var likely = [], optional = [], notNeeded = [];
    function need(cap, reason, policy, bucket) {
      var item = { capability_type: cap, reason: reason, policy_ref: policy, candidate_only: true, not_fact: true };
      if (bucket === "likely") likely.push(item);
      else if (bucket === "optional") optional.push(item);
      else notNeeded.push(item);
    }
    if (sceneType === "shopfront_sign") {
      need("ocr", "shopfront_sign 默认需要 OCR 读取文字", "shopfront_sign_prefers_ocr", "likely");
      ["slam", "tracking", "depth"].forEach(function (c) { need(c, "文字识别场景默认不需要空间/动态模型", "text_task_no_default_slam", "not_needed"); });
    } else if (sceneType === "subway_platform") {
      need("ocr", "地铁站方向/站台信息读取", "subway_direction_prefers_ocr", "likely");
      need("detection", "站台门/行人检测可选", "subway_direction_prefers_ocr", "optional");
      if (goalType !== "navigate") need("slam", "非导航目标不需要 SLAM", "subway_direction_prefers_ocr", "not_needed");
    } else if (sceneType === "street_crossing") {
      ["detection", "depth", "tracking"].forEach(function (c) { need(c, "街道路口通行评估需要感知动态与深度", "street_crossing_prefers_detection_depth_tracking", "likely"); });
      need("ocr", hasTextEvidence ? "仅在有文字证据时可选 OCR" : "无文字证据时不应全图默认 OCR", "street_crossing_prefers_detection_depth_tracking", hasTextEvidence ? "optional" : "not_needed");
    } else if (sceneType === "corridor") {
      need("depth", "走廊空间理解需要深度", "corridor_prefers_spatial_tools", "likely");
      need("slam", "走廊导航需要空间连续性", "corridor_prefers_spatial_tools", "likely");
      need("ocr", hasTextEvidence ? "有文字证据时 OCR 可选" : "走廊默认不需要 OCR", "corridor_prefers_spatial_tools", hasTextEvidence ? "optional" : "not_needed");
    } else {
      need("vlm", "未知场景可用 VLM advisor 辅助理解", "unknown_scene_requires_uncertainty", "optional");
      ["slam", "detection", "ocr", "tracking", "depth"].forEach(function (c) { need(c, "未知场景禁止 blanket activate", "no_blanket_model_activation", "not_needed"); });
    }
    return { likely_needed: likely, optional: optional, not_needed: notNeeded };
  }

  function inferUncertainty(sceneType, goalType, confidence) {
    var needsManual = sceneType === "unknown_scene" || confidence < 0.5;
    return {
      needs_user_goal: goalType === "unknown" && sceneType === "unknown_scene",
      needs_manual_review: needsManual,
      ambiguity_reason_optional: sceneType === "unknown_scene" ? "weak_evidence" : "",
      fallback_suggestion: needsManual ? "ask_user / vlm_advisor" : "",
      candidate_only: true,
      not_fact: true
    };
  }

  function buildCandidateFromInput(input) {
    var scene = inferScene(input);
    var goalType = (input.user_goal_candidate && input.user_goal_candidate.goal_type) || "unknown";
    var survival = inferSurvival(scene.scene_type, goalType);
    var taskClues = inferTaskClues(scene.scene_type);
    var missing = inferMissing(taskClues);
    var attention = inferAttention(scene.scene_type);
    var hasText = hasEvidence(input, "large_text_density", "direction_sign_text_density", "sign_text");
    var modelNeeds = inferModelNeeds(scene.scene_type, goalType, hasText);
    var uncertainty = inferUncertainty(scene.scene_type, goalType, scene.confidence);
    return {
      situation_id: uid("sit"),
      scene_profile_candidate: scene,
      survival_context: survival,
      task_clue_candidates: taskClues,
      missing_information_candidates: missing,
      attention_target_hints: attention,
      model_need_hints: modelNeeds,
      uncertainty: uncertainty,
      trace_refs: scene.trace_refs || [],
      candidate_only: true,
      not_fact: true,
      no_runner_invocation: true,
      no_fact_write: true
    };
  }

  function buildPackage(envelope, options) {
    options = options || {};
    if (options.ui_payload) return options.ui_payload;
    if (!envelope) return null;
    var job = envelopeToJob(envelope);
    var input = buildInput(job);
    var candidate = buildCandidateFromInput(input);
    var runnerEv = extractRunnerEvidence(job);
    var conflict = candidate.scene_profile_candidate.trace_refs || [];
    var summary = {
      likely_needed: candidate.model_need_hints.likely_needed.map(function (h) { return h.capability_type; }),
      optional: candidate.model_need_hints.optional.map(function (h) { return h.capability_type; }),
      not_needed: candidate.model_need_hints.not_needed.map(function (h) { return h.capability_type; })
    };
    return {
      situation_id: candidate.situation_id,
      job_id: job.job_id,
      scene_profile_candidate: candidate.scene_profile_candidate,
      survival_context: candidate.survival_context,
      task_clue_candidates: candidate.task_clue_candidates,
      missing_information_candidates: candidate.missing_information_candidates,
      attention_target_hints: candidate.attention_target_hints,
      model_need_hints: candidate.model_need_hints,
      model_need_hint_summary: summary,
      uncertainty: candidate.uncertainty,
      runner_scene_hint_evidence: runnerEv,
      conflict_trace: candidate.scene_profile_candidate.trace_refs || [],
      badges: ["candidate_only", "not_fact", "no_runner_invocation", "no_fact_write"],
      candidate_only: true,
      not_fact: true,
      trace_refs: candidate.trace_refs,
      no_runner_invocation: true,
      no_fact_write: true,
      dryrun_only: true
    };
  }

  global.LunaSituationUnderstandingState = {
    version: "luna_situation_understanding_state_v1",
    buildPackage: buildPackage,
    envelopeToJob: envelopeToJob,
    buildCandidateFromInput: buildCandidateFromInput
  };
})(typeof window !== "undefined" ? window : this);

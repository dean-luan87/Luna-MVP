/**
 * Observation Attention Layer V1 — candidate-only attention engine (no runner, no fact).
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.ObservationAttentionCopy || {}; };
  var CorrectionStore = function () { return global.HumanCorrectionStore; };

  var PRIORITY_ORDER = {
    P0_immediate_attention: 0,
    P1_high_attention: 1,
    P2_medium_attention: 2,
    P3_low_attention: 3,
    ignore_for_now: 4
  };

  var MOTION_ORDER = {
    dynamic_candidate: 0,
    needs_tracking_review: 1,
    scene_structure_candidate: 2,
    static_candidate: 3,
    unknown_motion_state: 4
  };

  function normKey(s) {
    return String(s || "").trim().toLowerCase().replace(/\s+/g, "_");
  }

  function labelBlob(entity) {
    var parts = [
      entity.display_name,
      entity.label,
      entity.entity_type,
      entity.task_semantic_candidate,
      entity.source_prompt_hint,
      entity._overlay && entity._overlay.label,
      entity._overlay && entity._overlay.display_task_semantic
    ];
    return parts.filter(Boolean).join(" ").toLowerCase();
  }

  function matchPattern(blob, pattern) {
    return pattern.split("|").some(function (p) { return blob.indexOf(p) >= 0; });
  }

  function inferMotionState(entity, frameContext) {
    var blob = labelBlob(entity);
    var promptKey = normKey((entity._overlay && entity._overlay.label) || entity.label || "");
    if (promptKey.indexOf("people_region") >= 0 || matchPattern(blob, "people_region|person_candidate|pedestrian|cyclist|dynamic|train_door")) {
      return frameContext === "single_frame" ? "needs_tracking_review" : "dynamic_candidate";
    }
    if (matchPattern(blob, "vehicle|car|bus") && promptKey.indexOf("people") < 0) {
      return frameContext === "single_frame" ? "needs_tracking_review" : "dynamic_candidate";
    }
    if (matchPattern(blob, "road|crosswalk|walkable|plane|ground|pavement")) {
      return "scene_structure_candidate";
    }
    if (matchPattern(blob, "sign|advertisement|screen|text|facade|ocr|station_direction|station_name|route_map|文字观察")) {
      return "static_candidate";
    }
    if (matchPattern(blob, "building|structure|facility|pole|edge")) {
      if (matchPattern(blob, "pole|facility|edge")) return "scene_structure_candidate";
      return "static_candidate";
    }
    return "unknown_motion_state";
  }

  function inferPriority(motion, entity, blob) {
    if (motion === "dynamic_candidate" || motion === "needs_tracking_review") {
      return entity.task_relevance === "possible_risk" ? "P0_immediate_attention" : "P1_high_attention";
    }
    if (motion === "scene_structure_candidate") {
      return matchPattern(blob, "road|crosswalk") ? "P0_immediate_attention" : "P1_high_attention";
    }
    if (motion === "static_candidate") {
      if (matchPattern(blob, "sign|text|advertisement|screen")) return "P1_high_attention";
      if (matchPattern(blob, "building|structure")) return "P3_low_attention";
      return "P2_medium_attention";
    }
    return "P2_medium_attention";
  }

  function inferFollowup(motion, blob) {
    var models = [];
    if (motion === "dynamic_candidate" || motion === "needs_tracking_review") {
      models = ["tracking", "detection", "depth"];
    } else if (motion === "scene_structure_candidate") {
      models = matchPattern(blob, "road|crosswalk") ? ["depth", "slam"] : ["depth", "slam_reference"];
    } else if (motion === "static_candidate") {
      models = matchPattern(blob, "sign|text|advertisement|screen") ? ["ocr", "detection"] : ["detection", "slam_reference"];
    } else {
      models = ["detection", "human_review"];
    }
    return models;
  }

  function priorityReasons(motion, blob) {
    var reasons = [];
    if (motion === "dynamic_candidate" || motion === "needs_tracking_review") {
      reasons.push("possible_risk", "needs_detection_review");
      if (motion === "needs_tracking_review") reasons.push("needs_tracking_review");
    }
    if (motion === "scene_structure_candidate") reasons.push("navigation_relevant", "needs_depth_review");
    if (motion === "static_candidate" && matchPattern(blob, "sign|text")) reasons.push("text_relevant", "needs_ocr_review");
    if (matchPattern(blob, "building")) reasons.push("stable_background_reference");
    return reasons.filter(function (r, i, a) { return a.indexOf(r) === i; });
  }

  function buildSummary(entity, motion, priority, followups, frameContext) {
    var name = entity.display_name || entity.entity_id;
    var motionZh = (Copy().motionState || {})[motion] || motion;
    var followZh = followups.slice(0, 2).map(function (m) {
      return (Copy().followupModel || {})[m] || m;
    }).join(" + ");
    var note = frameContext === "single_frame" && (motion === "dynamic_candidate" || motion === "needs_tracking_review")
      ? "（单帧动态候选，需多帧跟踪复核）" : "";
    return name + "：" + motionZh + "，建议 " + followZh + note;
  }

  function hasCorrectionType(c, typeId) {
    if (c.correction_types && c.correction_types.indexOf(typeId) >= 0) return true;
    return c.correction_type === typeId;
  }

  function applyCorrectionBoost(record, corrections) {
    (corrections || []).forEach(function (c) {
      var target = c.correction_target || {};
      if (target.source_object_id !== record.region_id && target.target_id !== record.region_id) return;
      if (hasCorrectionType(c, "false_negative") || c.user_note && /会动|移动/.test(c.user_note)) {
        record.motion_state_candidate = "dynamic_candidate";
        record.priority_level = "P0_immediate_attention";
        record.tracking_required = true;
        record.recommended_followup_model = ["tracking", "detection", "human_review"];
        record._correction_boosted = true;
      }
      if (hasCorrectionType(c, "wrong_label") || /文字|读/.test(c.user_note || "")) {
        record.motion_state_candidate = "static_candidate";
        record.ocr_required = true;
        record.recommended_followup_model = ["ocr", "detection", "human_review"];
        record._correction_boosted = true;
      }
      if (hasCorrectionType(c, "boundary_inaccurate")) {
        record.priority_level = "P1_high_attention";
        record.recommended_followup_model = ["detection", "depth", "human_review"];
        record._correction_boosted = true;
      }
      record.human_correction_refs = record.human_correction_refs || [];
      record.human_correction_refs.push(c.correction_id);
    });
    return record;
  }

  function envelopeRef(envelope) {
    if (!envelope) return "";
    if (envelope._source_file_ref) return envelope._source_file_ref;
    if (envelope.test_manifest_ref) return envelope.test_manifest_ref;
    if (envelope.envelope_id) return "envelope://" + envelope.envelope_id;
    return "";
  }

  function buildAttentionPackage(envelope, entities, options) {
    options = options || {};
    var frameContext = options.video_or_single_frame_context || "single_frame";
    var taskContext = (options.task_context || "street_navigation_test");
    var corrections = options.corrections;
    if (!corrections && CorrectionStore()) corrections = CorrectionStore().list();

    var records = (entities || []).filter(function (e) { return !e._hidden; }).map(function (entity, idx) {
      var blob = labelBlob(entity);
      var motion = inferMotionState(entity, frameContext);
      var priority = inferPriority(motion, entity, blob);
      var followups = inferFollowup(motion, blob);
      var record = {
        attention_record_id: "attention_ui_" + (entity.entity_id || idx),
        source_envelope_ref: envelopeRef(envelope),
        source_hud_annotation_ref: entity.entity_id,
        source_model_id: (envelope && envelope.model_id) || "mobile_sam",
        source_model_category: (envelope && envelope.model_category) || "segmentation",
        task_context: taskContext,
        region_id: entity.entity_id,
        region_display_name: entity.display_name || entity.entity_id,
        region_confidence: entity.confidence,
        prompt_label_candidate: entity.source_prompt_hint || (entity._overlay && entity._overlay.label),
        source_prompt_hint: entity.source_prompt_hint,
        task_semantic_candidate: entity.task_semantic_candidate,
        scene_profile_candidate: (envelope && envelope.scene_profile_candidate) || null,
        geometry_candidate: entity.geometry_ref,
        prompt_is_not_fact: entity.prompt_is_not_fact !== false,
        ocr_route_candidate: !!entity.ocr_route_candidate,
        motion_state_candidate: motion,
        motion_state_confidence: entity.confidence,
        motion_state_reason: priorityReasons(motion, blob),
        priority_level: priority,
        priority_reason: priorityReasons(motion, blob),
        uncertainty_tags: entity.uncertainty_tags || [],
        recommended_followup_model: followups,
        followup_route_refs: followups.map(function (m) { return "route_" + m + "_" + entity.entity_id; }),
        video_or_single_frame_context: frameContext,
        tracking_required: followups.indexOf("tracking") >= 0,
        ocr_required: followups.indexOf("ocr") >= 0 || !!entity.ocr_route_candidate,
        depth_required: followups.indexOf("depth") >= 0,
        detection_required: followups.indexOf("detection") >= 0,
        attention_summary: "",
        candidate_only: true,
        not_fact: true,
        not_navigation_instruction: true,
        not_runtime_output: true,
        not_speech_output: true,
        human_correction_refs: []
      };
      record.attention_summary = buildSummary(entity, record.motion_state_candidate, record.priority_level,
        record.recommended_followup_model, frameContext);
      return applyCorrectionBoost(record, corrections);
    });

    records.sort(function (a, b) {
      var pa = PRIORITY_ORDER[a.priority_level] != null ? PRIORITY_ORDER[a.priority_level] : 9;
      var pb = PRIORITY_ORDER[b.priority_level] != null ? PRIORITY_ORDER[b.priority_level] : 9;
      if (pa !== pb) return pa - pb;
      var ma = MOTION_ORDER[a.motion_state_candidate] != null ? MOTION_ORDER[a.motion_state_candidate] : 9;
      var mb = MOTION_ORDER[b.motion_state_candidate] != null ? MOTION_ORDER[b.motion_state_candidate] : 9;
      return ma - mb;
    });

    var top = records.filter(function (r) {
      return r.priority_level !== "ignore_for_now" && r.priority_level !== "P3_low_attention";
    }).slice(0, 6);

    var motionCounts = {};
    top.forEach(function (r) {
      var k = r.motion_state_candidate;
      motionCounts[k] = (motionCounts[k] || 0) + 1;
    });

    return {
      candidate_only: true,
      not_fact: true,
      observation_attention_candidate_only: true,
      followup_model_route_candidate_only: true,
      video_or_single_frame_context: frameContext,
      records: records,
      sorted_entities: sortEntitiesByAttention(entities, records),
      priority_panel: top,
      summary: buildFrameSummary(top, motionCounts),
      motion_counts: motionCounts
    };
  }

  function sortEntitiesByAttention(entities, records) {
    var order = {};
    records.forEach(function (r, i) { order[r.region_id] = i; });
    return (entities || []).slice().sort(function (a, b) {
      var oa = order[a.entity_id] != null ? order[a.entity_id] : 999;
      var ob = order[b.entity_id] != null ? order[b.entity_id] : 999;
      return oa - ob;
    });
  }

  function buildFrameSummary(top, motionCounts) {
    var c = Copy();
    if (!top.length) return "";
    var parts = [];
    Object.keys(motionCounts).forEach(function (k) {
      var label = (c.motionState || {})[k] || k;
      parts.push(label + " " + motionCounts[k] + " 个");
    });
    return (c.summaryPrefix || "本帧建议优先观察") + " " + top.length +
      (c.summaryRegions || " 个区域") + "：" + parts.join("、") + "。";
  }

  function lookupRecord(pkg, entityId) {
    if (!pkg || !entityId) return null;
    for (var i = 0; i < pkg.records.length; i++) {
      if (pkg.records[i].region_id === entityId) return pkg.records[i];
    }
    return null;
  }

  function formatChipBadges(record) {
    if (!record) return "";
    var c = Copy();
    var pri = (c.priorityLevel || {})[record.priority_level] || "";
    var motion = (c.motionState || {})[record.motion_state_candidate] || "";
    var flags = [];
    if (record.tracking_required) flags.push(c.flags.tracking);
    if (record.ocr_required) flags.push(c.flags.ocr);
    if (record.depth_required) flags.push(c.flags.depth);
    if (record.detection_required && flags.indexOf(c.flags.detection) < 0) flags.push(c.flags.detection);
    var route = record.recommended_followup_model && record.recommended_followup_model[0]
      ? ((c.followupModel || {})[record.recommended_followup_model[0]] || record.recommended_followup_model[0])
      : "";
    return { priority: pri, motion: motion, flags: flags, route: route };
  }

  global.ObservationAttentionEngine = {
    version: "observation_attention_engine_v1",
    candidateOnly: true,
    buildAttentionPackage: buildAttentionPackage,
    lookupRecord: lookupRecord,
    formatChipBadges: formatChipBadges,
    buildFrameSummary: buildFrameSummary
  };
})(typeof window !== "undefined" ? window : this);

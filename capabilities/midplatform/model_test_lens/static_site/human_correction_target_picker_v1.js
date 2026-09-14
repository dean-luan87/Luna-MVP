/**
 * Human Correction Layer V1 — correction target builders.
 */
(function (global) {
  "use strict";

  var Store = function () { return global.HumanCorrectionStore; };

  function baseTarget(envelope, overrides) {
    var ref = Store() ? Store().envelopeRef(envelope) : "";
    return Object.assign({
      source_envelope_ref: ref,
      source_model_id: (envelope && envelope.model_id) || "",
      source_model_category: (envelope && envelope.model_category) || "",
      candidate_only: true
    }, overrides || {});
  }

  function objectTarget(entity, envelope) {
    if (!entity) return null;
    var targetType = "segmentation_mask";
    if (envelope && envelope.model_category === "detection") targetType = "detection_box";
    if (entity.layer_type === "ocr") targetType = "ocr_text_box";
    return baseTarget(envelope, {
      target_id: entity.entity_id,
      target_type: targetType,
      source_object_id: entity.entity_id,
      source_annotation_id: entity.annotation_id || entity.entity_id,
      target_display_name: entity.display_name || entity.entity_id
    });
  }

  function chipTarget(entity, envelope) {
    var t = objectTarget(entity, envelope);
    if (t) t.target_type = "object_chip";
    return t;
  }

  function reasoningTarget(sectionKey, text, envelope, index) {
    var isRec = sectionKey === "recommendations" || sectionKey === "next_steps";
    return baseTarget(envelope, {
      target_id: "reasoning_" + sectionKey + "_" + (index != null ? index : 0),
      target_type: isRec ? "recommendation_item" : "reasoning_panel_statement",
      source_reasoning_panel_id: sectionKey,
      target_display_name: (text || "").slice(0, 48)
    });
  }

  function missingRegionTarget(region, envelope) {
    return baseTarget(envelope, {
      target_id: "missing_region_" + Date.now(),
      target_type: "missing_region",
      target_display_name: "漏识别区域",
      source_geometry_ref: "user_marked_region"
    });
  }

  global.HumanCorrectionTargetPicker = {
    version: "human_correction_target_picker_v1",
    objectTarget: objectTarget,
    chipTarget: chipTarget,
    reasoningTarget: reasoningTarget,
    missingRegionTarget: missingRegionTarget
  };
})(typeof window !== "undefined" ? window : this);

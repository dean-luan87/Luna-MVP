/**
 * Model Test Lens — Visual Overlay Layer schema & examples v1.
 *
 * Overlay layer schema (read-only display):
 * {
 *   overlay_layer_id, overlay_type: segmentation_mask|detection_box|ocr_text_box|...
 *   source_image_ref, artifact_ref, label, confidence, candidate_only,
 *   visible_by_default, opacity, color_class,
 *   geometry: { type: mask|box|..., data_ref }
 * }
 */
(function (global) {
  "use strict";

  function artifactBase() {
    var host = "127.0.0.1";
    if (typeof window !== "undefined" && window.location && window.location.hostname) {
      host = window.location.hostname;
    }
    return "http://" + host + ":8787/api/v1/local-file?rel=";
  }

  var ARTIFACT_BASE = artifactBase();

  var OVERLAY_COLORS = [
    "rgba(255, 99, 71, 0.55)",
    "rgba(65, 105, 225, 0.55)",
    "rgba(50, 205, 50, 0.55)",
    "rgba(255, 165, 0, 0.55)",
    "rgba(186, 85, 211, 0.55)",
    "rgba(0, 206, 209, 0.55)",
    "rgba(255, 215, 0, 0.55)",
    "rgba(220, 20, 60, 0.55)"
  ];

  var OUTLINE_COLORS = [
    "#ff6347", "#4169e1", "#32cd32", "#ffa500",
    "#ba55d3", "#00ced1", "#ffd700", "#dc143c"
  ];

  function artifactUrl(ref) {
    if (!ref || typeof ref !== "string") return null;
    if (/^https?:\/\//i.test(ref)) return null;
    return artifactBase() + encodeURIComponent(ref);
  }

  function pickSourceImageRef(envelope) {
    var refs = envelope.input_asset_refs || [];
    if (!refs.length) return null;
    var first = refs[0];
    if (typeof first === "string") return first;
    return first.path || first.ref || null;
  }

  function buildOverlayLayers(envelope) {
    var layers = [];
    var viz = envelope.visualization_layers || [];
    var cands = envelope.candidate_outputs || [];
    var metrics = envelope.metrics || {};
    var perCat = metrics.per_category_average_score || {};
    var idx = 0;

    function pushLayer(spec) {
      layers.push({
        overlay_layer_id: spec.overlay_layer_id || "overlay_" + idx,
        layer_id: spec.overlay_layer_id || spec.layer_id,
        overlay_type: spec.overlay_type || "segmentation_mask",
        source_image_ref: spec.source_image_ref,
        artifact_ref: spec.artifact_ref,
        label: spec.label || "识别区域",
        display_task_semantic: spec.display_task_semantic,
        source_prompt_hint: spec.source_prompt_hint,
        prompt_is_not_fact: spec.prompt_is_not_fact !== false,
        ocr_route_candidate: !!spec.ocr_route_candidate,
        confidence: spec.confidence,
        candidate_only: true,
        visible_by_default: spec.visible_by_default !== false,
        opacity: typeof spec.opacity === "number" ? spec.opacity : 0.45,
        color_class: spec.color_class || ("seg-color-" + idx),
        color: OVERLAY_COLORS[idx % OVERLAY_COLORS.length],
        outline_color: OUTLINE_COLORS[idx % OUTLINE_COLORS.length],
        geometry: { type: "mask", data_ref: spec.artifact_ref }
      });
      idx += 1;
    }

    viz.forEach(function (layer) {
      if (layer.layer_type !== "mask" && layer.overlay_type !== "segmentation_mask") return;
      var ref = layer.source_artifact_ref || layer.mask_ref;
      if (!ref) return;
      var label = layer.label || layer.layer_id || "mask";
      pushLayer({
        overlay_layer_id: layer.layer_id,
        layer_id: layer.layer_id,
        artifact_ref: ref,
        label: label,
        display_task_semantic: layer.display_task_semantic,
        source_prompt_hint: layer.source_prompt_hint,
        prompt_is_not_fact: layer.prompt_is_not_fact,
        ocr_route_candidate: layer.ocr_route_candidate,
        confidence: perCat[label] != null ? perCat[label] : layer.score,
        opacity: layer.opacity,
        color_class: layer.color_class
      });
    });

    if (!layers.length && cands.length) {
      cands.forEach(function (out) {
        var ref = out.mask_ref || out.source_artifact_ref;
        if (!ref) return;
        var label = out.output_id || out.display_name || "region";
        pushLayer({
          overlay_layer_id: out.output_id,
          layer_id: out.output_id,
          artifact_ref: ref,
          label: label,
          display_task_semantic: out.display_task_semantic,
          source_prompt_hint: out.source_prompt_hint,
          prompt_is_not_fact: out.prompt_is_not_fact,
          ocr_route_candidate: out.ocr_route_candidate,
          confidence: out.score != null ? out.score : perCat[label]
        });
      });
    }

    return layers;
  }

  global.VisualOverlayExamples = {
    ARTIFACT_BASE: ARTIFACT_BASE,
    OVERLAY_COLORS: OVERLAY_COLORS,
    OUTLINE_COLORS: OUTLINE_COLORS,
    artifactUrl: artifactUrl,
    pickSourceImageRef: pickSourceImageRef,
    buildOverlayLayers: buildOverlayLayers
  };
})(typeof window !== "undefined" ? window : this);

/**
 * Model Test Lens — Perception HUD examples & reserved adapter interfaces v1.
 * Display-only annotations; read-only; candidate-only.
 */
(function (global) {
  "use strict";

  function canGenerateHUD(envelope) {
    if (!envelope) return false;
    var cat = envelope.model_category;
    var modelId = envelope.model_id;
    if (cat === "segmentation" || modelId === "mobile_sam") return true;
    if (cat === "detection_tracking") return false;
    if (cat === "ocr") return false;
    if (cat === "slam_vio") return false;
    if (cat === "depth_world") return false;
    var viz = envelope.visualization_layers || [];
    var cands = envelope.candidate_outputs || [];
    return viz.length > 0 || cands.length > 0;
  }

  function createDetectionHUDAnnotations(envelope) {
    return { supported: false, reason: "detection_hud_reserved", entities: [] };
  }

  function renderDetectionHUDView(envelope, host, options) {
    host.innerHTML = "<p class='muted'>Detection HUD 预留接口，尚未实现。</p>";
  }

  function createOCRHUDAnnotations(envelope) {
    return { supported: false, reason: "ocr_hud_reserved", entities: [] };
  }

  function renderOCRHUDView(envelope, host, options) {
    host.innerHTML = "<p class='muted'>OCR HUD 预留接口，尚未实现。</p>";
  }

  function createSLAMHUDAnnotations(envelope) {
    return { supported: false, reason: "slam_hud_reserved", entities: [] };
  }

  function renderSLAMHUDView(envelope, host, options) {
    host.innerHTML = "<p class='muted'>SLAM HUD 预留接口，尚未实现。</p>";
  }

  function createDepthHUDAnnotations(envelope) {
    return { supported: false, reason: "depth_hud_reserved", entities: [] };
  }

  function renderDepthHUDView(envelope, host, options) {
    host.innerHTML = "<p class='muted'>Depth HUD 预留接口，尚未实现。</p>";
  }

  global.PerceptionHUDExamples = {
    canGenerateHUD: canGenerateHUD,
    createDetectionHUDAnnotations: createDetectionHUDAnnotations,
    renderDetectionHUDView: renderDetectionHUDView,
    createOCRHUDAnnotations: createOCRHUDAnnotations,
    renderOCRHUDView: renderOCRHUDView,
    createSLAMHUDAnnotations: createSLAMHUDAnnotations,
    renderSLAMHUDView: renderSLAMHUDView,
    createDepthHUDAnnotations: createDepthHUDAnnotations,
    renderDepthHUDView: renderDepthHUDView
  };
})(typeof window !== "undefined" ? window : this);

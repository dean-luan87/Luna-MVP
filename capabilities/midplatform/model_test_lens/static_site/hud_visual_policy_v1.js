/**
 * HUD Visual Policy V1 — default display rules for Perception HUD.
 * Display-only; does not modify envelope or model output.
 */
(function (global) {
  "use strict";

  var DEFAULT_STATE = {
    showLineBox: true,
    showLabels: true,
    showUncertainty: true,
    showMaskFill: false,
    maskFillOpacity: 0.35,
    useSemanticColors: true,
    showRawPromptNames: false,
    dimP2Opacity: 0.4,
    dimP3Opacity: 0.26,
    showDebugGuidelines: false,
    showAttentionMarkers: true,
    showAllAttentionMarkers: false,
    showAllCandidateMarkersDefaultOff: true,
    routeFilter: "all"
  };

  function createDefaultState(overrides) {
    var s = {};
    Object.keys(DEFAULT_STATE).forEach(function (k) { s[k] = DEFAULT_STATE[k]; });
    if (overrides) Object.keys(overrides).forEach(function (k) { s[k] = overrides[k]; });
    return s;
  }

  global.HudVisualPolicy = {
    version: "hud_visual_policy_v2_visual_expression_post_review",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Visual-Expression-System-UI-Execution-Post-Review-And-Minor-Fix-v1-001",
    DEFAULT_STATE: DEFAULT_STATE,
    createDefaultState: createDefaultState,
    maskFillHiddenByDefault: true,
    fullImageTintRemovedByDefault: true,
    lineBoxDefaultVisible: true
  };
})(typeof window !== "undefined" ? window : this);

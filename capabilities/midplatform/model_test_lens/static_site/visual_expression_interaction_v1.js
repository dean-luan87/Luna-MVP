/**
 * Visual Expression System V1 — interaction helpers (mapping only, no runner/fact).
 */
(function (global) {
  "use strict";

  var VL = function () { return global.HudAttentionVisualLanguage; };
  var Engine = function () { return global.ObservationAttentionEngine; };

  function lookupAttention(attentionPkg, regionId) {
    if (!attentionPkg || !regionId || !Engine()) return null;
    return Engine().lookupRecord(attentionPkg, regionId);
  }

  function hasAttentionRecord(attentionPkg, regionId) {
    var rec = lookupAttention(attentionPkg, regionId);
    if (!rec) return false;
    return rec.priority_level !== "ignore_for_now";
  }

  function buildHoverHint(entity, record) {
    if (!VL() || !entity) return "";
    return VL().formatFloatMarker(entity, record, { hoverEntityId: entity.entity_id });
  }

  global.VisualExpressionInteraction = {
    version: "visual_expression_interaction_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Visual-Expression-System-UI-Execution-And-Post-Review-v1-001",
    annotationLayerOnly: true,
    segmentationSoleBoundaryOwner: true,
    noBoundaryClone: true,
    noRunnerExecution: true,
    noFactWrite: true,
    lookupAttention: lookupAttention,
    hasAttentionRecord: hasAttentionRecord,
    buildHoverHint: buildHoverHint
  };
})(typeof window !== "undefined" ? window : this);

/**
 * Scene-Task Model Activation — compact metrics summary line.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.SceneTaskModelActivationCopy || {}; };

  function modelLabel(name) {
    var labels = Copy().modelLabels || {};
    return labels[name] || name;
  }

  function summaryLine(activationPkg) {
    if (!activationPkg || !activationPkg.model_activation_plan_candidate) return "";
    var active = activationPkg.activated_model_set || [];
    var noop = activationPkg.model_noop_set || [];
    var activeNames = active.map(function (a) { return modelLabel(a.model_name); });
    var noopNames = noop.filter(function (n) {
      return ["slam", "tracking", "depth", "detection", "vlm_route_enhancer"].indexOf(n.model_name) >= 0;
    }).map(function (n) { return modelLabel(n.model_name) + " no-op"; });
    var parts = [];
    if (activeNames.length) parts.push("激活 " + activeNames.join(" / "));
    if (noopNames.length) parts.push(noopNames.slice(0, 4).join(" · "));
    return "模型激活：" + (parts.join("；") || "—") + " · candidate_only";
  }

  global.SceneTaskModelActivationSummary = {
    version: "scene_task_model_activation_summary_v1",
    summaryLine: summaryLine
  };
})(typeof window !== "undefined" ? window : this);

/**
 * Luna Situation Understanding — conflict trace view v1.
 */
(function (global) {
  "use strict";

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function render(host, payload, options) {
    options = options || {};
    var Copy = global.LunaSituationUnderstandingCopy || {};
    var traces = (payload && payload.conflict_trace) || [];
    var runnerEv = payload && payload.runner_scene_hint_evidence;
    var scene = payload && payload.scene_profile_candidate;
    if (!traces.length && !runnerEv) {
      host.innerHTML = "";
      host.hidden = true;
      return;
    }
    host.hidden = false;
    var lines = [];
    if (runnerEv) {
      lines.push("<p><span class='lsu-k'>Runner scene_hint</span> " + escapeHtml(runnerEv.value) + " <span class='lsu-tag'>runner hint as evidence</span></p>");
    }
    if (scene) {
      lines.push("<p><span class='lsu-k'>Situation scene</span> " + escapeHtml(scene.scene_type) + " candidate</p>");
      lines.push("<p><span class='lsu-k'>Owner</span> " + escapeHtml(scene.owned_by || "situation_understanding_layer") + "</p>");
    }
    traces.forEach(function (t) {
      if (t.stage === "runner_scene_hint_conflict") {
        lines.push(
          "<p><span class='lsu-k'>Conflict</span> runner_scene_hint_conflict</p>" +
          "<p class='lsu-muted'>Resolution: runner hint treated as evidence only; scene owned by situation_understanding_layer</p>"
        );
      }
    });
  if (payload && payload.job_id) {
      lines.push("<p><span class='lsu-k'>Trace refs</span> " + escapeHtml(payload.job_id) + " · runner_scene_hint_evidence · evidence_ref</p>");
    }
    host.innerHTML =
      "<div class='lsu-trace-block'>" +
      "<h4>" + escapeHtml(Copy.conflictTitle || "Runner 冲突记录") + "</h4>" +
      lines.join("") +
      "</div>";
  }

  global.LunaSituationUnderstandingTraceView = {
    version: "luna_situation_understanding_trace_view_v1",
    render: render
  };
})(typeof window !== "undefined" ? window : this);

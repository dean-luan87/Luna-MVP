/**
 * Scene-Task Model Activation — right panel (scene/task → activated/no-op models).
 * No runner execution · candidate_only · not_fact · no boundary clone on main canvas.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.SceneTaskModelActivationCopy || {}; };
  var FORBIDDEN_PARTS = ["OCR结果", "导航到", "已识别"];

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function safeText(text) {
    var s = String(text || "");
    for (var i = 0; i < FORBIDDEN_PARTS.length; i++) {
      if (s.indexOf(FORBIDDEN_PARTS[i]) >= 0) return "[文案违规已屏蔽]";
    }
    return s || "—";
  }

  function modelLabel(name) {
    var labels = Copy().modelLabels || {};
    return labels[name] || name;
  }

  function renderScene(scene) {
    if (!scene) return "";
    var c = Copy();
    return (
      "<div class='stma-block'>" +
      "<h4>" + escapeHtml(c.sceneTitle || "场景候选") + "</h4>" +
      "<p><span class='stma-k'>scene_profile</span> " + escapeHtml(safeText(scene.scene_type_candidate)) + " candidate</p>" +
      "<p><span class='stma-k'>confidence</span> " + escapeHtml(String(scene.confidence)) + "</p>" +
      "<p class='stma-status'><span class='stma-tag'>candidate_only</span> · <span class='stma-tag'>not_fact</span></p>" +
      "</div>"
    );
  }

  function renderTask(task) {
    if (!task) return "";
    var c = Copy();
    return (
      "<div class='stma-block'>" +
      "<h4>" + escapeHtml(c.taskTitle || "任务意图") + "</h4>" +
      "<p><span class='stma-k'>task_intent</span> " + escapeHtml(safeText(task.task_type_candidate)) + " candidate</p>" +
      "<p><span class='stma-k'>source</span> " + escapeHtml(safeText(task.source)) + "</p>" +
      "<p class='stma-status'><span class='stma-tag'>candidate_only</span> · <span class='stma-tag'>not_fact</span></p>" +
      "</div>"
    );
  }

  function findAssignment(assignments, modelName) {
    return (assignments || []).find(function (a) { return a.model_name === modelName; }) || null;
  }

  function renderActivated(plan, options) {
    var c = Copy();
    var active = (plan && plan.activated_model_set) || [];
    var assignments = (plan && plan.model_region_assignment) || [];
    if (!active.length) return "<p class='muted stma-empty'>无激活模型</p>";
    var items = active.map(function (a) {
      var assign = findAssignment(assignments, a.model_name);
      var regionText = "—";
      if (assign) {
        var parts = [];
        if (assign.assigned_text_region_ids && assign.assigned_text_region_ids.length) {
          parts.push("text: " + assign.assigned_text_region_ids.join(", "));
        }
        if (assign.assigned_region_ids && assign.assigned_region_ids.length) {
          parts.push("region: " + assign.assigned_region_ids.join(", "));
        }
        regionText = parts.join(" · ") || "—";
      }
      return (
        "<li class='stma-item stma-active-item' data-stma-model='" + escapeHtml(a.model_name) + "' " +
        "data-stma-text-regions='" + escapeHtml(JSON.stringify((assign && assign.assigned_text_region_ids) || [])) + "' " +
        "data-stma-regions='" + escapeHtml(JSON.stringify((assign && assign.assigned_region_ids) || [])) + "'>" +
        "<span class='stma-k'>" + escapeHtml(modelLabel(a.model_name)) + "</span>" +
        "<br><span class='stma-k'>activation_reason</span> " + escapeHtml(safeText(a.activation_reason)) +
        "<br><span class='stma-k'>assigned_region</span> " + escapeHtml(safeText(regionText)) +
        "<br><span class='stma-k'>runner_type</span> " + escapeHtml(safeText(a.allowed_runner_type)) +
        " · <span class='stma-tag'>candidate_only</span> · <span class='stma-tag'>not_fact</span></li>"
      );
    }).join("");
    return (
      "<div class='stma-block'>" +
      "<h4>" + escapeHtml(c.activatedTitle || "Activated Models") + "</h4>" +
      "<ul class='stma-list'>" + items + "</ul></div>"
    );
  }

  function renderNoop(plan) {
    var c = Copy();
    var noop = (plan && plan.model_noop_set) || [];
    if (!noop.length) return "";
    var items = noop.map(function (n) {
      return (
        "<li class='stma-item stma-noop-item'>" +
        "<span class='stma-k'>" + escapeHtml(modelLabel(n.model_name)) + "</span>" +
        "<br><span class='stma-k'>noop_reason</span> " + escapeHtml(safeText(n.noop_reason)) +
        (n.policy_ref ? "<br><span class='stma-k'>policy_ref</span> " + escapeHtml(safeText(n.policy_ref)) : "") +
        "</li>"
      );
    }).join("");
    return (
      "<div class='stma-block stma-noop-block'>" +
      "<h4>" + escapeHtml(c.noopTitle || "No-op Models") + "</h4>" +
      "<ul class='stma-list'>" + items + "</ul></div>"
    );
  }

  function renderFollowup(plan) {
    var c = Copy();
    if (!plan) return "";
    var tasks = plan.followup_runner_task_candidates || [];
    var taskLines = tasks.map(function (t) {
      return "<li class='stma-item'>" + escapeHtml(modelLabel(t.model_name)) + " → " +
        escapeHtml(safeText(t.runner_task_type)) + " · <span class='stma-tag'>no_runner_execution</span></li>";
    }).join("");
    return (
      "<div class='stma-block'>" +
      "<h4>" + escapeHtml(c.followupTitle || "Followup task candidate") + "</h4>" +
      "<p><span class='stma-k'>recommended</span> " +
      escapeHtml(safeText(plan.recommended_followup_runner_task_candidate)) + "</p>" +
      (taskLines ? "<ul class='stma-list'>" + taskLines + "</ul>" : "") +
      "</div>"
    );
  }

  function bindAssignmentClicks(host, options) {
    if (!host || !options || !options.onSelectAssignment) return;
    host.querySelectorAll(".stma-active-item").forEach(function (el) {
      el.addEventListener("click", function () {
        var textRegions = [];
        var regions = [];
        try {
          textRegions = JSON.parse(el.getAttribute("data-stma-text-regions") || "[]");
          regions = JSON.parse(el.getAttribute("data-stma-regions") || "[]");
        } catch (e) { /* ignore */ }
        options.onSelectAssignment({
          model_name: el.getAttribute("data-stma-model"),
          assigned_text_region_ids: textRegions,
          assigned_region_ids: regions
        });
      });
    });
  }

  function render(host, activationPkg, options) {
    if (!host) return;
    options = options || {};
    var c = Copy();
    if (!activationPkg || !activationPkg.model_activation_plan_candidate) {
      host.innerHTML = (
        "<section class='stma-panel stma-panel-empty'>" +
        "<h3 class='stma-heading'>" + escapeHtml(c.sectionTitle || "模型激活计划") + "</h3>" +
        "<p class='muted'>" + escapeHtml(c.emptyHint || "") + "</p></section>"
      );
      host.hidden = false;
      return;
    }
    var plan = activationPkg.model_activation_plan_candidate;
    host.innerHTML = (
      "<section class='stma-panel'>" +
      "<h3 class='stma-heading'>" + escapeHtml(c.sectionTitle || "模型激活计划") + "</h3>" +
      renderScene(plan.scene_profile_candidate) +
      renderTask(plan.task_intent_candidate) +
      renderActivated(plan, options) +
      renderNoop(plan) +
      renderFollowup(plan) +
      "<p class='stma-trace muted'>" + escapeHtml(c.notExecuted || "") + "</p>" +
      "<p class='stma-trace muted'>" + escapeHtml(c.traceHint || "") + "</p>" +
      "</section>"
    );
    bindAssignmentClicks(host, options);
    host.hidden = false;
  }

  global.SceneTaskModelActivationPanel = {
    version: "scene_task_model_activation_panel_v1",
    no_ocr_execution: true,
    no_detection_execution: true,
    no_vlm_execution: true,
    no_slam_execution: true,
    no_fact_write: true,
    no_runner_execution_in_activation_execution: true,
    segmentationSoleBoundaryOwner: true,
    no_boundary_clone: true,
    render: render
  };
})(typeof window !== "undefined" ? window : this);

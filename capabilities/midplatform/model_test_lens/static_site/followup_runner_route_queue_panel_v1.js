/**
 * Followup Runner Route — queue panel UI (pin/unpin, no runner execution).
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.FollowupRunnerRouteCopy || {}; };
  var Queue = function () { return global.FollowupRunnerRouteQueue; };
  var RmtCopy = function () { return global.RunnerManualTriggerCopy || {}; };
  var RmtReq = function () { return global.RunnerManualTriggerRequest; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function renderTaskItem(task, options, section) {
    var c = Copy();
    var Q = Queue();
    var runner = Q ? Q.formatRunnerLabel(task.target_model_id) : task.target_model_id;
    var active = options.selectedRegionId === task.region_id ? " frr-queue-item-active" : "";
    var boost = task.correction_boosted
      ? "<span class='frr-badge frr-badge-hc'>" + escapeHtml(c.correctionBoost) + "</span>" : "";

    var actions = "";
    var requestHint = "";
    var R = RmtReq();
    var rc = RmtCopy();

    if (section === "manual") {
      requestHint = "<p class='frr-queue-hint muted'>" + escapeHtml(rc.hintNeedPin) + "</p>";
      actions = "<button type='button' class='frr-btn frr-btn-pin' data-action='pin' data-rtc='" +
        escapeHtml(task.runner_task_candidate_id) + "'>" + escapeHtml(c.pinBtn) + "</button>";
    } else if (section === "active") {
      if (task.queue_state === "pinned") {
        actions = "<button type='button' class='frr-btn frr-btn-ghost' data-action='unpin' data-rtc='" +
          escapeHtml(task.runner_task_candidate_id) + "'>" + escapeHtml(c.unpinBtn) + "</button>";
        if (R && (task.target_model_id === "detection" || task.target_model_id === "ocr")) {
          var genCheck = R.canGenerateRequest(task, options.requestStore);
          if (genCheck.ok) {
            actions += "<button type='button' class='frr-btn frr-btn-request' data-action='generate-request' data-rtc='" +
              escapeHtml(task.runner_task_candidate_id) + "'>" +
              escapeHtml(R.getGenerateButtonLabel(task.target_model_id)) + "</button>";
          } else if (genCheck.hint) {
            requestHint = "<p class='frr-queue-hint muted'>" + escapeHtml(genCheck.hint) + "</p>";
          }
        }
      } else if (task.queue_state === "candidate") {
        requestHint = "<p class='frr-queue-hint muted'>" + escapeHtml(rc.hintNeedPin) + "</p>";
      }
      actions += "<button type='button' class='frr-btn frr-btn-ghost' data-action='exclude' data-rtc='" +
        escapeHtml(task.runner_task_candidate_id) + "'>" + escapeHtml(c.excludeBtn) + "</button>";
    } else if (section === "excluded") {
      requestHint = "<p class='frr-queue-hint muted'>" + escapeHtml(rc.hintExcluded) + "</p>";
      actions = "<button type='button' class='frr-btn frr-btn-ghost' data-action='restore' data-rtc='" +
        escapeHtml(task.runner_task_candidate_id) + "'>" + escapeHtml(c.restoreBtn) + "</button>";
    }

    return (
      "<li class='frr-queue-item" + active + "' data-region-id='" + escapeHtml(task.region_id) + "' " +
      "data-rtc-id='" + escapeHtml(task.runner_task_candidate_id) + "' role='button' tabindex='0'>" +
      "<div class='frr-queue-head'>" +
      "<strong>" + escapeHtml(task.task_candidate_id) + "｜" + escapeHtml(task.task_priority) + "｜" +
      escapeHtml(task.region_display_name) + "｜" + escapeHtml(runner) + "</strong>" + boost +
      "</div>" +
      "<p class='frr-queue-meta'><span class='muted'>" + escapeHtml(c.labelAdmission) + "：</span>" +
      escapeHtml(task.admission_mode) + " · queue_state: " + escapeHtml(task.queue_state) + "</p>" +
      "<p class='frr-queue-reason'><span class='muted'>" + escapeHtml(c.labelReason) + "：</span>" +
      escapeHtml(task.route_reason) + "</p>" +
      "<p class='frr-queue-runner muted'>" + escapeHtml(c.labelRecommendedOnly) + "</p>" +
      "<p class='frr-queue-status'>" + escapeHtml(c.statusLine) + "</p>" +
      "<p class='frr-queue-trace muted'>region: " + escapeHtml(task.region_id) +
      " · attention: " + escapeHtml(task.linked_attention_record_id) + "</p>" +
      requestHint +
      (actions ? "<div class='frr-queue-actions'>" + actions + "</div>" : "") +
      "</li>"
    );
  }

  function render(host, queuePkg, options) {
    options = options || {};
    if (!host) return;
    var c = Copy();
    if (!queuePkg || !queuePkg.tasks || !queuePkg.tasks.length) {
      host.innerHTML = "";
      host.hidden = true;
      return;
    }
    host.hidden = false;

    var active = queuePkg.active_tasks || [];
    var manual = queuePkg.manual_pool || [];
    var excluded = queuePkg.excluded_tasks || [];

    var activeHtml = active.length
      ? "<ol class='frr-queue-list'>" + active.map(function (t) {
        return renderTaskItem(t, options, "active");
      }).join("") + "</ol>"
      : "<p class='muted'>暂无已入队候选。</p>";

    var manualHtml = manual.length
      ? "<details class='frr-manual-pool' open><summary>" + escapeHtml(c.manualOnlyTitle) +
        " (" + manual.length + ")</summary><ol class='frr-queue-list'>" +
        manual.map(function (t) { return renderTaskItem(t, options, "manual"); }).join("") +
        "</ol></details>" : "";

    var excludedHtml = excluded.length
      ? "<details class='frr-excluded-pool'><summary>" + escapeHtml(c.excludedTitle) +
        " (" + excluded.length + ")</summary><ol class='frr-queue-list'>" +
        excluded.map(function (t) { return renderTaskItem(t, options, "excluded"); }).join("") +
        "</ol></details>" : "";

    host.innerHTML =
      "<section class='frr-queue-panel'>" +
      "<h3 class='frr-queue-title'>" + escapeHtml(c.panelTitle) + "</h3>" +
      "<p class='frr-queue-notice muted'>" + escapeHtml(c.panelNotice) + "</p>" +
      "<h4 class='frr-queue-subtitle'>" + escapeHtml(c.activeQueueTitle) + "</h4>" +
      activeHtml + manualHtml + excludedHtml +
      "</section>";

    function bindActions() {
      host.querySelectorAll("[data-action]").forEach(function (btn) {
        btn.addEventListener("click", function (ev) {
          ev.stopPropagation();
          var action = btn.dataset.action;
          var rtc = btn.dataset.rtc;
          if (options.onQueueAction) options.onQueueAction(action, rtc);
        });
      });
    }

    function bindSelect() {
      host.querySelectorAll(".frr-queue-item").forEach(function (li) {
        var regionId = li.dataset.regionId;
        li.addEventListener("click", function (ev) {
          if (ev.target.closest("[data-action]")) return;
          if (options.onSelectRegion) options.onSelectRegion(regionId);
        });
        li.addEventListener("mouseenter", function () {
          if (options.onHoverRegion) options.onHoverRegion(regionId);
        });
        li.addEventListener("mouseleave", function () {
          if (options.onHoverRegion) options.onHoverRegion(null);
        });
      });
    }

    bindActions();
    bindSelect();
  }

  global.FollowupRunnerRouteQueuePanel = {
    version: "followup_runner_route_queue_panel_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-UI-Queue-Execution-And-Post-Review-v1-001",
    panelContainsQueueExplanation: true,
    noRunnerExecution: true,
    render: render
  };
})(typeof window !== "undefined" ? window : this);

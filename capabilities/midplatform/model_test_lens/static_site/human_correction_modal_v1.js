/**
 * Human Correction Layer V1 — correction form modal (on-demand, candidate-only).
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.HumanCorrectionCopy || {}; };
  var Store = function () { return global.HumanCorrectionStore; };
  var Preview = function () { return global.HumanCorrectionTrainingSignalPreview; };
  var Midplatform = function () { return global.HumanCorrectionMidplatformAnalyzer; };

  var _overlay = null;
  var _onSaved = null;

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function optionsHtml(items, selected) {
    return items.map(function (item) {
      var sel = item.id === selected ? " selected" : "";
      return "<option value='" + escapeHtml(item.id) + "'" + sel + ">" + escapeHtml(item.label) + "</option>";
    }).join("");
  }

  function issueCheckboxes(items, selected) {
    selected = selected || [];
    return items.map(function (item) {
      var checked = selected.indexOf(item.id) >= 0 ? " checked" : "";
      return "<label class='hc-issue-item'><input type='checkbox' name='correction_type' value='" +
        escapeHtml(item.id) + "'" + checked + " data-group='" + escapeHtml(item.group || "") + "'>" +
        escapeHtml(item.label) + "</label>";
    }).join("");
  }

  function followupCheckboxes(selected) {
    selected = selected || [];
    return (Copy().followupModels || []).map(function (m) {
      var checked = selected.indexOf(m.id) >= 0 ? " checked" : "";
      return "<label class='hc-followup-item'><input type='checkbox' name='followup' value='" +
        escapeHtml(m.id) + "'" + checked + ">" + escapeHtml(m.label) + "</label>";
    }).join("");
  }

  function targetSummary(target) {
    if (!target) return "—";
    return (target.target_display_name || target.target_id || target.target_type) +
      " · " + (target.target_type || "");
  }

  function closeModal() {
    if (_overlay) {
      _overlay.remove();
      _overlay = null;
    }
  }

  function collectCorrectionTypes(form) {
    var types = [];
    form.querySelectorAll("input[name='correction_type']:checked").forEach(function (cb) {
      types.push(cb.value);
    });
    return types;
  }

  function openModal(ctx) {
    ctx = ctx || {};
    closeModal();
    var target = ctx.target;
    var envelope = ctx.envelope;
    var entity = ctx.entity;
    var c = Copy();
    var preselected = ctx.prefillTypes || (ctx.prefillType ? [ctx.prefillType] : []);

    _overlay = document.createElement("div");
    _overlay.className = "hc-modal-overlay";
    _overlay.setAttribute("role", "dialog");
    _overlay.setAttribute("aria-modal", "true");
    _overlay.innerHTML =
      "<div class='hc-modal hc-modal-wide'>" +
      "<header class='hc-modal-head'><h3>" + escapeHtml(c.modalTitle || "人工指错") + "</h3>" +
      "<button type='button' class='hc-modal-close' aria-label='关闭'>&times;</button></header>" +
      "<p class='hc-boundary-notice'>" + escapeHtml(c.boundaryNotice || "") + "</p>" +
      "<p class='hc-boundary-notice muted'>" + escapeHtml(c.notFactNotice || "") + "</p>" +
      "<form class='hc-modal-form' id='hc-modal-form'>" +
      "<div class='hc-field'><label>问题对象</label>" +
      "<div class='hc-readonly'>" + escapeHtml(targetSummary(target)) + "</div>" +
      (entity ? "<div class='hc-readonly muted'>编号 " + escapeHtml(entity.entity_id || "") +
        " · " + escapeHtml(envelope.model_id || "") + "</div>" : "") +
      "</div>" +
      "<div class='hc-field'><label>" + escapeHtml(c.modelIssueSection) + "</label>" +
      "<div class='hc-issue-grid'>" + issueCheckboxes(c.modelIssues || [], preselected) + "</div></div>" +
      "<div class='hc-field'><label>" + escapeHtml(c.environmentIssueSection) + "</label>" +
      "<div class='hc-issue-grid'>" + issueCheckboxes(c.environmentIssues || [], preselected) + "</div></div>" +
      "<div class='hc-field'><label>" + escapeHtml(c.otherIssueSection) + "</label>" +
      "<div class='hc-issue-grid hc-issue-grid-compact'>" + issueCheckboxes(c.otherIssues || [], preselected) + "</div></div>" +
      "<div class='hc-field'><label for='hc-manual'>" + escapeHtml(c.manualAnnotationLabel) +
      " <span class='req'>*</span></label>" +
      "<textarea id='hc-manual' name='manual_annotation' rows='3' placeholder='" +
      escapeHtml(c.manualAnnotationPlaceholder || "") + "' required></textarea>" +
      "<p class='hc-field-hint muted'>" + escapeHtml(c.manualAnnotationHint || "") + "</p></div>" +
      "<div class='hc-field'><label for='hc-severity'>严重度</label>" +
      "<select id='hc-severity' name='severity'>" + optionsHtml(c.severityLevels || [], "medium") + "</select></div>" +
      "<div class='hc-field'><label for='hc-fix'>期望修正（可选）</label>" +
      "<textarea id='hc-fix' name='suggested_fix' rows='2' placeholder='希望它怎么判断？'></textarea></div>" +
      "<div class='hc-field'><label>建议补测</label><div class='hc-followup-grid'>" +
      followupCheckboxes(ctx.defaultFollowups || []) + "</div></div>" +
      "<p class='hc-form-error' id='hc-form-error' hidden></p>" +
      "<div id='hc-preview-host'></div>" +
      "<footer class='hc-modal-foot'>" +
      "<button type='button' class='btn btn-ghost hc-cancel'>" + escapeHtml(c.buttons.cancel) + "</button>" +
      "<button type='submit' class='btn btn-primary'>" + escapeHtml(c.buttons.save) + "</button>" +
      "</footer></form></div>";

    document.body.appendChild(_overlay);

    _overlay.querySelector(".hc-modal-close").addEventListener("click", closeModal);
    _overlay.querySelector(".hc-cancel").addEventListener("click", closeModal);
    _overlay.addEventListener("click", function (ev) {
      if (ev.target === _overlay) closeModal();
    });

    var form = _overlay.querySelector("#hc-modal-form");
    if (ctx.prefillNote && form.manual_annotation) form.manual_annotation.value = ctx.prefillNote;

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var errEl = _overlay.querySelector("#hc-form-error");
      var correctionTypes = collectCorrectionTypes(form);
      var followups = [];
      form.querySelectorAll("input[name='followup']:checked").forEach(function (cb) {
        followups.push(cb.value);
      });
      var formData = {
        correction_types: correctionTypes,
        correction_type: correctionTypes[0] || "",
        severity: form.severity.value,
        manual_annotation: form.manual_annotation.value,
        user_note: form.manual_annotation.value,
        suggested_fix: form.suggested_fix.value,
        recommended_followup_models: followups,
        user_marked_region: ctx.user_marked_region
      };
      var submitted = Store().submitCorrection
        ? Store().submitCorrection(target, envelope, formData)
        : (function () {
          var built = Store().buildRecord(target, envelope, formData);
          if (!built.ok) return built;
          Store().add(built.record);
          return { ok: true, record: built.record, analysis: null };
        })();
      if (!submitted.ok) {
        errEl.hidden = false;
        errEl.textContent = submitted.error;
        return;
      }
      var previewHost = _overlay.querySelector("#hc-preview-host");
      if (Midplatform() && submitted.analysis) {
        Midplatform().renderRoutingPreview(previewHost, submitted.analysis);
      }
      if (Preview() && submitted.analysis && submitted.analysis.training_candidate === "pending_review") {
        Preview().renderPreview(previewHost, submitted.record, submitted.analysis.purified_training_signal);
      }
      if (typeof ctx.onSaved === "function") ctx.onSaved(submitted.record);
      if (typeof _onSaved === "function") _onSaved(submitted.record);
      setTimeout(closeModal, 600);
    });
  }

  global.HumanCorrectionModal = {
    version: "human_correction_modal_v1",
    open: openModal,
    close: closeModal,
    setOnSaved: function (fn) { _onSaved = fn; }
  };
})(typeof window !== "undefined" ? window : this);

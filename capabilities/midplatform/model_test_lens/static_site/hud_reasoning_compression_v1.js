/**
 * HUD Reasoning Compression V1 — result-first observation panel.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.LunaObservationCopy || {}; };
  var I18n = function () { return global.LunaObservationLabelI18n; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function localize(text) {
    if (!text) return text;
    return I18n() ? I18n().localizeReasoningLine(text) : text;
  }

  function renderList(items, max) {
    max = max || 2;
    var slice = (items || []).filter(Boolean).map(localize).slice(0, max);
    if (!slice.length) return "<p class='muted'>—</p>";
    return "<ul class='lol-rp-list'>" + slice.map(function (t) {
      return "<li>" + escapeHtml(t) + "</li>";
    }).join("") + "</ul>";
  }

  function primaryRiskLine(view) {
    var risks = view.risks_uncertainty || [];
    for (var i = 0; i < risks.length; i++) {
      var t = localize(risks[i]);
      if (/风险|复核|不确定|不能/.test(t)) return t;
    }
    return risks[0] ? localize(risks[0]) : "未发现显著整体风险。";
  }

  function buildFromLegacy(panel) {
    if (!panel) return null;
    if (panel.compressed_view) return panel.compressed_view;

    var task = panel.current_task || {};
    return {
      current_task: {
        title: task.task_name || "查看当前画面中的识别结果",
        goal: task.task_goal || "判断哪些区域可信、哪些需要复核。",
        mode: task.test_mode ? "本地模型测试" : "观察模式"
      },
      fact_observations: panel.system_observations || [],
      goal_judgment: panel.goal_judgment || [
        "当前主要关注：道路区域、前方车辆、路牌/广告屏。",
        "当前可作为稳定观察的只有部分大区域边界。"
      ],
      risks_uncertainty: [].concat(
        panel.uncertainty_summary || [],
        (panel.missing_information || []).slice(0, 2)
      ),
      recommendations: (panel.recommended_next_steps || []).map(function (r) {
        return r.text || r;
      }),
      reasoning_process: panel.reasoning_steps || [],
      evidence_notes: [
        "图像分割模型提供区域边界，不是目标检测结论。",
        "分割提示标签是候选提示，不是事实标签。",
        "车辆/路牌/文字区域需要目标检测或文字识别复核。"
      ],
      evidence_refs: (panel.reasoning_steps || []).reduce(function (acc, s) {
        return acc.concat(s.evidence_refs || []);
      }, []).slice(0, 5)
    };
  }

  function sectionHeader(title, sectionKey, options) {
    var reportBtn = options.onReportIssue
      ? " <button type='button' class='hc-report-issue btn-ghost-inline' data-section='" +
        escapeHtml(sectionKey) + "'>指出问题</button>"
      : "";
    return "<h3>" + escapeHtml(title) + reportBtn + "</h3>";
  }

  function renderCompressedPanel(host, panel, options) {
    options = options || {};
    var view = buildFromLegacy(panel);
    if (!view) {
      host.innerHTML = "<p class='muted'>暂无观察结论。</p>";
      return;
    }

    var sec = Copy().sections || {};
    var html =
      "<h2 class='lol-rp-title'>" + escapeHtml(Copy().rightPanelTitle || "Luna 观察面板") + "</h2>" +
      "<section class='lol-rp-section'>" + sectionHeader(sec.current_task || "当前任务", "current_task", options) +
      "<p data-section-text='current_task'>" + escapeHtml(localize(view.current_task.goal)) + "</p></section>" +
      "<section class='lol-rp-section'>" + sectionHeader(sec.fact_observations || "总体观察", "fact_observations", options) +
      renderList(view.fact_observations, 2) + "</section>" +
      "<section class='lol-rp-section'>" + sectionHeader(sec.goal_judgment || "主要判断", "goal_judgment", options) +
      renderList(view.goal_judgment, 2) + "</section>" +
      "<section class='lol-rp-section'>" + sectionHeader(sec.risks_uncertainty || "主要风险", "risks_uncertainty", options) +
      "<p data-section-text='risks_uncertainty'>" + escapeHtml(primaryRiskLine(view)) + "</p></section>" +
      "<section class='lol-rp-section'>" + sectionHeader(sec.next_steps || "下一步建议", "recommendations", options) +
      renderList(view.recommendations, 2) + "</section>" +
      "<details class='lol-rp-collapsed'><summary>" + escapeHtml(Copy().expandProcess || "展开观察过程") + "</summary>" +
      renderList((view.reasoning_process || []).map(function (s) { return s.text || s; }), 4) +
      "</details>" +
      (options.onReportIssue
        ? "<p class='lol-rp-foot'><button type='button' class='btn btn-ghost btn-sm hc-report-issue' data-section='whole_panel'>指出问题</button></p>"
        : "") +
      "<p class='lol-rp-foot muted'>对象级细节见中央「识别对象」列表。当前结果仅用于模型评估。</p>";

    host.innerHTML = html;

    if (options.onReportIssue) {
      host.querySelectorAll(".hc-report-issue").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var key = btn.dataset.section;
          var textEl = host.querySelector("[data-section-text='" + key + "']");
          var text = textEl ? textEl.textContent : (key === "whole_panel" ? "整体观察面板" : key);
          options.onReportIssue(key, text, 0);
        });
      });
    }
  }

  global.HudReasoningCompression = {
    version: "hud_reasoning_compression_v1",
    buildFromLegacy: buildFromLegacy,
    renderCompressedPanel: renderCompressedPanel
  };
})(typeof window !== "undefined" ? window : this);

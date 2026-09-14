/**
 * HUD Selected Object Detail V1 — on-demand compact object detail.
 */
(function (global) {
  "use strict";

  var LabelPolicy = function () { return global.HudLabelLayoutPolicy; };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function render(host, entity, options) {
    options = options || {};
    if (!host) return;
    if (!entity) {
      host.innerHTML = "";
      host.hidden = true;
      return;
    }
    var P = LabelPolicy();
    var detail = P ? P.buildExternalDetail(entity, (entity.hud_number || 1) - 1) : null;
    if (!detail) {
      host.hidden = true;
      return;
    }

    host.hidden = false;
    host.innerHTML =
      "<section class='lol-selected-object' style='--hud-item-color:" + escapeHtml(detail.stroke) + "'>" +
      "<h3 class='lol-selected-title'>选中分割区域</h3>" +
      "<header class='lol-selected-head'>" +
      "<span class='lol-selected-num' style='color:" + escapeHtml(detail.stroke) + "'>" +
      escapeHtml(detail.number_glyph) + "</span>" +
      "<strong>" + escapeHtml(detail.name) + "</strong></header>" +
      "<dl class='lol-selected-meta'>" +
      "<div><dt>置信度</dt><dd>" + escapeHtml(detail.confidence_text || "—") + "</dd></div>" +
      "<div><dt>分割状态</dt><dd>" + escapeHtml(detail.status) + "</dd></div>" +
      "</dl>" +
      "<p class='muted oa-panel-pointer'>观察调度说明见上方「优先观察」。</p>" +
      "<p class='lol-selected-explain'>" + escapeHtml(detail.explanation) + "</p>" +
      "<p class='lol-selected-suggest muted'>建议：" + escapeHtml(detail.suggestion) + "</p>" +
      (detail.source_prompt_hint
        ? "<dl class='lol-selected-prompt-meta muted'>" +
          "<div><dt>source_prompt_hint</dt><dd class='oa-mono'>" + escapeHtml(detail.source_prompt_hint) + "</dd></div>" +
          "<div><dt>original_prompt_label</dt><dd class='oa-mono'>" + escapeHtml(detail.original_prompt_label || "—") + "</dd></div>" +
          "<div><dt>prompt_is_not_fact</dt><dd>true</dd></div>" +
          "<div><dt>display_label_source</dt><dd>" + escapeHtml(detail.display_label_source || "midplatform_task_semantics") + "</dd></div>" +
          "</dl>"
        : "") +
      (options.onMarkProblem
        ? "<button type='button' class='btn btn-ghost btn-sm lol-selected-mark'>标记问题</button>"
        : "") +
      (options.showClose
        ? "<button type='button' class='btn btn-ghost btn-sm lol-selected-close'>收起</button>"
        : "") +
      "</section>";

    var closeBtn = host.querySelector(".lol-selected-close");
    if (closeBtn && options.onClose) {
      closeBtn.addEventListener("click", options.onClose);
    }
    var markBtn = host.querySelector(".lol-selected-mark");
    if (markBtn && options.onMarkProblem) {
      markBtn.addEventListener("click", options.onMarkProblem);
    }
  }

  global.HudSelectedObjectDetail = {
    version: "hud_selected_object_detail_v1",
    render: render
  };
})(typeof window !== "undefined" ? window : this);

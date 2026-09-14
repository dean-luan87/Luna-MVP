/**
 * Luna Observation Lens — layout & capability cards v1.
 */
(function (global) {
  "use strict";

  var I18n = function () { return global.LunaObservationLabelI18n; };
  var Copy = function () { return global.LunaObservationCopy || {}; };

  var CAPABILITIES = [
    { id: "segmentation", label: "图像分割", group: "vision", status: "可测试", testTypeId: "segmentation", example: "mobile_sam" },
    { id: "detection", label: "目标检测", group: "vision", status: "未接入" },
    { id: "ocr", label: "文字识别", group: "vision", status: "未接入", testTypeId: "ocr" },
    { id: "slam", label: "空间定位 / SLAM", group: "vision", status: "实验中", testTypeId: "slam_vio", example: "slam" },
    { id: "depth", label: "深度感知", group: "vision", status: "未接入" },
    { id: "asr", label: "语音识别", group: "audio", status: "未接入", testTypeId: "asr" },
    { id: "tts", label: "语音合成", group: "audio", status: "未接入" },
    { id: "speaker", label: "说话人识别", group: "audio", status: "未接入" },
    { id: "face", label: "表情 / 手势", group: "multimodal", status: "未接入" },
    { id: "vlm", label: "多模态理解", group: "multimodal", status: "未接入" }
  ];

  var GROUPS = [
    { id: "vision", title: "视觉能力" },
    { id: "audio", title: "声音能力" },
    { id: "multimodal", title: "综合理解" }
  ];

  function statusClass(status) {
    if (status === "可测试") return "lol-cap-ok";
    if (status === "实验中") return "lol-cap-exp";
    return "lol-cap-off";
  }

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function renderCapabilityRail(host, state, onSelect) {
    var html = "<div class='lol-input-summary' id='lol-input-summary'><p class='muted'>" +
      escapeHtml(Copy().emptyInput) + "</p></div>";
    html += "<div class='lol-cap-groups'>";
    GROUPS.forEach(function (g) {
      html += "<div class='lol-cap-group'><h3>" + g.title + "</h3><ul class='lol-cap-list'>";
      CAPABILITIES.filter(function (c) { return c.group === g.id; }).forEach(function (cap) {
        var active = state.capabilityId === cap.id ? " active" : "";
        var disabled = cap.status === "未接入" ? " disabled" : "";
        html +=
          "<li><button type='button' class='lol-cap-card" + active + disabled + "' data-cap='" + cap.id + "'" +
          (disabled ? " disabled" : "") + ">" +
          "<span class='lol-cap-label'>" + cap.label + "</span>" +
          "<span class='lol-cap-status " + statusClass(cap.status) + "'>" + cap.status + "</span>" +
          "</button></li>";
      });
      html += "</ul></div>";
    });
    html += "</div>";
    html += "<div class='lol-rail-examples'>" +
      "<button type='button' class='btn btn-ghost btn-sm' id='lol-example-sam'>" + escapeHtml(Copy().exampleSam || "分割示例") + "</button>" +
      "<button type='button' class='btn btn-ghost btn-sm' id='lol-example-slam'>" + escapeHtml(Copy().exampleSlam || "空间定位示例") + "</button>" +
      "</div>";
    host.innerHTML = html;
    host.querySelectorAll(".lol-cap-card:not([disabled])").forEach(function (btn) {
      btn.addEventListener("click", function () {
        onSelect(btn.dataset.cap);
      });
    });
  }

  function updateInputSummary(host, file, capabilityId) {
    var el = host.querySelector("#lol-input-summary");
    if (!el) return;
    if (!file) {
      el.innerHTML = "<p class='muted'>" + escapeHtml(Copy().emptyInput) + "</p>";
      return;
    }
    var cap = CAPABILITIES.find(function (c) { return c.id === capabilityId; });
    var capStatus = cap ? cap.status : "可测试";
    var summary = I18n() ? I18n().formatInputSummary(file, capabilityId) : null;
    if (summary) {
      el.innerHTML =
        "<p class='lol-input-label'>" + escapeHtml(summary.title) + "</p>" +
        "<p><strong>当前图片</strong></p>" +
        "<p class='muted'>" + escapeHtml(summary.line) + "</p>" +
        (summary.fileShort ? "<p class='lol-input-filename muted'>" + escapeHtml(summary.fileShort) + "</p>" : "") +
        "<p class='lol-input-label lol-input-cap-label'>" + escapeHtml(Copy().inputSummary.capabilityTitle || "当前能力") + "</p>" +
        "<p class='muted'>" + escapeHtml((cap && cap.label) || "图像分割") + " · " + escapeHtml(capStatus) + "</p>";
    }
  }

  global.LunaObservationLayout = {
    CAPABILITIES: CAPABILITIES,
    GROUPS: GROUPS,
    renderCapabilityRail: renderCapabilityRail,
    updateInputSummary: updateInputSummary,
    getCapability: function (id) {
      for (var i = 0; i < CAPABILITIES.length; i++) {
        if (CAPABILITIES[i].id === id) return CAPABILITIES[i];
      }
      return null;
    }
  };
})(typeof window !== "undefined" ? window : this);

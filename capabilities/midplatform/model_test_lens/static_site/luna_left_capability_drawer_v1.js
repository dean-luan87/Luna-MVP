/**
 * Luna Left Capability Drawer V1 — collapsible capability rail with grid trigger.
 */
(function (global) {
  "use strict";

  var Layout = function () { return global.LunaObservationLayout; };
  var Copy = function () { return global.LunaObservationCopy || {}; };
  var CanvasLayout = function () { return global.ObservationCanvasFirstLayout; };
  var GridTrigger = function () { return global.LunaCapabilityGridTrigger; };

  var CAP_ICONS = {
    segmentation: "分",
    detection: "检",
    ocr: "文",
    slam: "位",
    depth: "深",
    asr: "听",
    tts: "说",
    speaker: "人",
    face: "表",
    vlm: "多"
  };

  var CAP_SHORT = {
    segmentation: "分割",
    detection: "检测",
    ocr: "OCR",
    slam: "SLAM",
    depth: "深度",
    asr: "语音",
    tts: "合成",
    speaker: "说话",
    face: "表情",
    vlm: "多模"
  };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function statusClass(status) {
    if (status === "可测试") return "lol-cap-ok";
    if (status === "实验中") return "lol-cap-exp";
    return "lol-cap-off";
  }

  function toggleExpanded() {
    if (!CanvasLayout()) return;
    CanvasLayout().setLeftExpanded(!CanvasLayout().isLeftExpanded());
  }

  function renderCollapsedMiniList(caps, currentId, onSelect) {
    return caps.map(function (cap) {
      var active = cap.id === currentId ? " active" : "";
      var disabled = cap.status === "未接入" ? " disabled" : "";
      var short = CAP_SHORT[cap.id] || cap.label.slice(0, 2);
      return (
        "<button type='button' class='lol-left-mini-cap" + active + disabled + "' data-cap='" + cap.id + "' " +
        "title='" + escapeHtml(cap.label) + " · " + escapeHtml(cap.status) + "'" +
        (disabled ? " disabled" : "") + ">" +
        "<span class='lol-left-mini-icon'>" + (CAP_ICONS[cap.id] || "·") + "</span>" +
        "<span class='lol-left-mini-label'>" + escapeHtml(short) + "</span>" +
        "</button>"
      );
    }).join("");
  }

  function render(host, state, callbacks) {
    callbacks = callbacks || {};
    var onSelect = callbacks.onSelect || function () {};
    var caps = Layout() ? Layout().CAPABILITIES : [];
    var groups = Layout() ? Layout().GROUPS : [];
    var expanded = CanvasLayout() ? CanvasLayout().isLeftExpanded() : false;
    var gridBtn = GridTrigger() ? GridTrigger().renderButton({ expanded: expanded }) : "";

    if (!expanded) {
      host.innerHTML =
        "<div class='lol-left-drawer lol-left-collapsed-view'>" +
        gridBtn +
        "<nav class='lol-left-mini-list' aria-label='能力快捷入口'>" +
        renderCollapsedMiniList(caps, state.capabilityId, onSelect) +
        "</nav></div>";
      var trigger = host.querySelector("#lol-cap-grid-trigger");
      if (GridTrigger()) GridTrigger().bind(trigger, function () {
        if (CanvasLayout()) CanvasLayout().setLeftExpanded(true);
        render(host, state, callbacks);
      });
      host.querySelectorAll(".lol-left-mini-cap:not([disabled])").forEach(function (btn) {
        btn.addEventListener("click", function () {
          onSelect(btn.dataset.cap);
        });
      });
    } else {
      var html =
        "<div class='lol-left-drawer lol-left-expanded-view'>" +
        "<div class='lol-left-drawer-head'>" +
        gridBtn +
        "<span class='lol-left-drawer-title'>能力面板</span>" +
        "</div>" +
        "<div class='lol-input-summary' id='lol-input-summary'></div>";
      groups.forEach(function (g) {
        html += "<div class='lol-cap-group'><h3>" + g.title + "</h3><ul class='lol-cap-list'>";
        caps.filter(function (c) { return c.group === g.id; }).forEach(function (cap) {
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
      html +=
        "<div class='lol-rail-examples'>" +
        "<button type='button' class='btn btn-ghost btn-sm' id='lol-example-sam'>" +
        escapeHtml(Copy().exampleSam || "分割示例") + "</button>" +
        "<button type='button' class='btn btn-ghost btn-sm' id='lol-example-slam'>" +
        escapeHtml(Copy().exampleSlam || "空间定位示例") + "</button></div></div>";
      host.innerHTML = html;
      var triggerExp = host.querySelector("#lol-cap-grid-trigger");
      if (GridTrigger()) GridTrigger().bind(triggerExp, function () {
        if (CanvasLayout()) CanvasLayout().setLeftExpanded(false);
        render(host, state, callbacks);
      });
      host.querySelectorAll(".lol-cap-card:not([disabled])").forEach(function (btn) {
        btn.addEventListener("click", function () {
          onSelect(btn.dataset.cap);
          if (CanvasLayout()) CanvasLayout().setLeftExpanded(false);
          render(host, state, callbacks);
        });
      });
    }

    return {
      updateInputSummary: function (file, capabilityId) {
        if (!expanded) return;
        if (Layout()) Layout().updateInputSummary(host, file, capabilityId);
      }
    };
  }

  global.LunaLeftCapabilityDrawer = {
    version: "luna_left_capability_drawer_v1",
    render: render
  };
})(typeof window !== "undefined" ? window : this);

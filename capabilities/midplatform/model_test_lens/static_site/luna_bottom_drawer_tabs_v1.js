/**
 * Luna Bottom Drawer Tabs V1 — overlay drawers, strictly collapsed by default.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.LunaObservationCopy || {}; };
  var Guard = function () { return global.LunaBottomDrawerStateGuard; };

  function renderBottomDock(host, api) {
    api = api || {};
    var tabs = Copy().drawerTabs || {};
    var guard = Guard();

    host.innerHTML =
      "<div class='lol-dock-bar'>" +
      "<div class='lol-dock-summary' id='lol-metrics-summary'>" +
      "<span class='muted'>等待观察结果…</span></div>" +
      "<div class='lol-dock-tabs' role='tablist' aria-label='折叠面板'>" +
      "<button type='button' class='lol-dock-tab' data-drawer='metrics' role='tab'>" +
      escapeHtml(tabs.metrics || "指标") + "</button>" +
      "<button type='button' class='lol-dock-tab' data-drawer='objects' role='tab'>" +
      escapeHtml(tabs.objects || "对象") + "</button>" +
      "<button type='button' class='lol-dock-tab' data-drawer='advanced' role='tab'>" +
      escapeHtml(tabs.advanced || "高级") + "</button>" +
      "<button type='button' class='lol-dock-tab' data-drawer='developer' role='tab'>" +
      escapeHtml(tabs.developer || "开发者") + "</button>" +
      "<button type='button' class='lol-dock-tab' data-drawer='whitebox' role='tab'>" +
      escapeHtml(tabs.whitebox || "白盒") + "</button>" +
      "<button type='button' class='lol-dock-tab' data-drawer='correction' role='tab'>" +
      escapeHtml(tabs.correction || "纠错") + "</button>" +
      "<button type='button' class='lol-dock-tab' data-drawer='testboard' role='tab'>" +
      escapeHtml(tabs.testboard || "记录") + "</button>" +
      "</div></div>";

    var overlayRoot = guard ? guard.getOverlayRoot() : host;
    var existing = document.getElementById(guard ? guard.OVERLAY_ID : "lol-drawer-overlay");
    if (existing) existing.remove();

    var overlay = document.createElement("div");
    overlay.id = guard ? guard.OVERLAY_ID : "lol-drawer-overlay";
    overlay.className = "lol-drawer-overlay";
    overlay.hidden = true;
    overlay.setAttribute("aria-hidden", "true");
    overlay.innerHTML =
      "<div class='lol-drawer-overlay-head'>" +
      "<span id='lol-drawer-overlay-title' class='lol-drawer-overlay-title'></span>" +
      "<button type='button' class='lol-drawer-close' id='lol-drawer-close' aria-label='关闭抽屉'>关闭</button>" +
      "</div>" +
      "<div id='lol-drawer-panel' class='lol-drawer-panel-overlay'></div>";
    overlayRoot.appendChild(overlay);

    var panel = overlay.querySelector("#lol-drawer-panel");
    var titleEl = overlay.querySelector("#lol-drawer-overlay-title");
    var activeDrawer = null;

    var titles = {
      metrics: tabs.metrics || "指标",
      objects: tabs.objects || "对象",
      advanced: tabs.advanced || "高级",
      developer: tabs.developer || "开发者",
      whitebox: tabs.whitebox || "白盒",
      correction: tabs.correction || "纠错",
      testboard: tabs.testboard || "记录"
    };

    function closeDrawer() {
      activeDrawer = null;
      if (guard) guard.closeOverlay(overlay);
      if (guard) guard.markClosed(host);
    }

    if (guard) guard.ensureCollapsed(host);

    overlay.querySelector("#lol-drawer-close").addEventListener("click", closeDrawer);

    host.querySelectorAll(".lol-dock-tab").forEach(function (tab) {
      tab.addEventListener("click", function () {
        var id = tab.dataset.drawer;
        if (activeDrawer === id) {
          closeDrawer();
          return;
        }
        activeDrawer = id;
        host.querySelectorAll(".lol-dock-tab").forEach(function (t) {
          t.classList.toggle("active", t.dataset.drawer === id);
        });
        titleEl.textContent = titles[id] || id;
        panel.innerHTML = "";
        if (guard) {
          guard.openOverlay(overlay);
          guard.markOpen(host);
        } else {
          overlay.hidden = false;
        }
        if (id === "metrics" && api.renderMetrics) api.renderMetrics(panel);
        else if (id === "objects" && api.renderObjects) api.renderObjects(panel);
        else if (id === "advanced" && api.renderAdvanced) api.renderAdvanced(panel);
        else if (id === "developer" && api.renderDeveloper) api.renderDeveloper(panel);
        else if (id === "whitebox") {
          panel.innerHTML = guard
            ? guard.emptyState(Copy().whiteboxPlaceholder || "暂无白盒链路，后续接入 trace 后显示。")
            : "<p class='lol-whitebox-placeholder'>" + (Copy().whiteboxPlaceholder || "") + "</p>";
        } else if (id === "testboard" && api.renderTestBoard) api.renderTestBoard(panel);
        else if (id === "correction" && api.renderCorrection) api.renderCorrection(panel);
        if (!panel.innerHTML && guard) {
          panel.innerHTML = guard.emptyState("暂无内容。");
        }
      });
    });

    return {
      setSummary: function (text) {
        var s = host.querySelector("#lol-metrics-summary");
        if (s) s.innerHTML = text;
      },
      closeDrawer: closeDrawer,
      openDrawer: function (id) {
        var tab = host.querySelector("[data-drawer='" + id + "']");
        if (tab) tab.click();
      }
    };
  }

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  global.LunaBottomDrawerTabs = {
    version: "luna_bottom_drawer_tabs_v1",
    renderBottomDock: renderBottomDock
  };
})(typeof window !== "undefined" ? window : this);

/**
 * Luna Observation Lens — bottom drawers v1.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.LunaObservationCopy || {}; };

  function renderBottomDock(host, api) {
    api = api || {};
    host.innerHTML =
      "<div class='lol-dock-summary' id='lol-metrics-summary'>" +
      "<span class='muted'>等待观察结果…</span></div>" +
      "<div class='lol-dock-tabs' role='tablist'>" +
      "<button type='button' class='lol-dock-tab' data-drawer='metrics' role='tab'>" + Copy().drawerTabs.metrics + "</button>" +
      "<button type='button' class='lol-dock-tab' data-drawer='advanced' role='tab'>" + Copy().drawerTabs.advanced + "</button>" +
      "<button type='button' class='lol-dock-tab' data-drawer='developer' role='tab'>" + Copy().drawerTabs.developer + "</button>" +
      "<button type='button' class='lol-dock-tab' data-drawer='whitebox' role='tab'>" + Copy().drawerTabs.whitebox + "</button>" +
      "<button type='button' class='lol-dock-tab' data-drawer='testboard' role='tab'>" + Copy().drawerTabs.testboard + "</button>" +
      "</div>" +
      "<div id='lol-drawer-panel' class='lol-drawer-panel' hidden></div>";

    var panel = host.querySelector("#lol-drawer-panel");
    var activeDrawer = null;

    function closeDrawer() {
      activeDrawer = null;
      panel.hidden = true;
      panel.innerHTML = "";
      host.querySelectorAll(".lol-dock-tab").forEach(function (t) { t.classList.remove("active"); });
    }

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
        panel.hidden = false;
        if (id === "metrics" && api.renderMetrics) api.renderMetrics(panel);
        else if (id === "advanced" && api.renderAdvanced) api.renderAdvanced(panel);
        else if (id === "developer" && api.renderDeveloper) api.renderDeveloper(panel);
        else if (id === "whitebox") panel.innerHTML = "<p class='lol-whitebox-placeholder'>" + Copy().whiteboxPlaceholder + "</p>";
        else if (id === "testboard" && api.renderTestBoard) api.renderTestBoard(panel);
      });
    });

    return {
      setSummary: function (text) {
        var s = host.querySelector("#lol-metrics-summary");
        if (s) s.innerHTML = text;
      },
      closeDrawer: closeDrawer
    };
  }

  global.LunaObservationDrawers = { renderBottomDock: renderBottomDock };
})(typeof window !== "undefined" ? window : this);

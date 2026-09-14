/**
 * Luna Bottom Drawer State Guard V1 — default collapsed, no blank body.
 */
(function (global) {
  "use strict";

  var OVERLAY_ID = "lol-drawer-overlay";

  function emptyState(message) {
    return (
      "<div class='lol-drawer-empty'>" +
      "<p class='muted'>" + String(message || "暂无内容。") + "</p>" +
      "</div>"
    );
  }

  function ensureCollapsed(dockHost) {
    var overlay = document.getElementById(OVERLAY_ID);
    if (overlay) {
      overlay.hidden = true;
      overlay.setAttribute("aria-hidden", "true");
      overlay.classList.remove("lol-drawer-overlay-open");
      var panel = overlay.querySelector("#lol-drawer-panel");
      if (panel) panel.innerHTML = "";
    }
    if (dockHost) {
      dockHost.classList.add("lol-bottom-dock-collapsed");
      dockHost.classList.remove("lol-bottom-dock-expanded");
      dockHost.querySelectorAll(".lol-dock-tab").forEach(function (t) {
        t.classList.remove("active");
      });
    }
    if (document.body) {
      document.body.classList.remove("lol-drawer-body-open");
    }
  }

  function markOpen(dockHost) {
    if (dockHost) {
      dockHost.classList.remove("lol-bottom-dock-collapsed");
      dockHost.classList.add("lol-bottom-dock-expanded");
    }
    if (document.body) {
      document.body.classList.add("lol-drawer-body-open");
    }
  }

  function markClosed(dockHost) {
    ensureCollapsed(dockHost);
  }

  function openOverlay(overlay) {
    if (!overlay) return;
    overlay.hidden = false;
    overlay.setAttribute("aria-hidden", "false");
    overlay.classList.add("lol-drawer-overlay-open");
  }

  function closeOverlay(overlay) {
    if (!overlay) return;
    overlay.hidden = true;
    overlay.setAttribute("aria-hidden", "true");
    overlay.classList.remove("lol-drawer-overlay-open");
    var panel = overlay.querySelector("#lol-drawer-panel");
    if (panel) panel.innerHTML = "";
  }

  function getOverlayRoot() {
    var app = document.getElementById("lol-app");
    if (!app) return document.body;
    var existing = document.getElementById(OVERLAY_ID);
    if (existing) return existing.parentElement || app;
    return app;
  }

  global.LunaBottomDrawerStateGuard = {
    version: "luna_bottom_drawer_state_guard_v1",
    OVERLAY_ID: OVERLAY_ID,
    emptyState: emptyState,
    ensureCollapsed: ensureCollapsed,
    markOpen: markOpen,
    markClosed: markClosed,
    openOverlay: openOverlay,
    closeOverlay: closeOverlay,
    getOverlayRoot: getOverlayRoot
  };
})(typeof window !== "undefined" ? window : this);

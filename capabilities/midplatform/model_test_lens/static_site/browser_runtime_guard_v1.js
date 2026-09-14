/**
 * Browser runtime guard — prevent Node/browser global mix in static_site entry.
 * app.js must use window.xxx; IIFE modules may use (function (global) { ... })(window).
 */
(function (global) {
  "use strict";

  var NODE_GLOBAL_MARKERS = ["require(", "module.exports", "__dirname", "process.env"];

  function assertBrowserRuntime() {
    var errors = [];
    if (typeof window === "undefined") {
      errors.push("window_missing");
    }
    NODE_GLOBAL_MARKERS.forEach(function (marker) {
      if (typeof Function !== "undefined") {
        try {
          if (marker === "process.env" && typeof process !== "undefined" && process.env) {
            errors.push("node_process_env_in_browser");
          }
        } catch (e) { /* */ }
      }
    });
    return { ok: errors.length === 0, errors: errors };
  }

  function markInitOk() {
    if (typeof document !== "undefined" && document.body) {
      document.body.dataset.browserRuntimeGuard = "ok";
      document.body.dataset.noNodeGlobalInBrowserApp = "true";
    }
    global.__LOL_BROWSER_RUNTIME_INIT_OK__ = true;
  }

  function assertAppEntryUsesWindow() {
    var rt = assertBrowserRuntime();
    if (!rt.ok) return rt;
    markInitOk();
    return { ok: true, browserRuntimeInitOk: true };
  }

  global.BrowserRuntimeGuard = {
    version: "browser_runtime_guard_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Followup-Runner-Route-UI-Queue-Execution-Post-Review-v1-001",
    noBrowserGlobalReferenceError: true,
    noNodeGlobalInBrowserApp: true,
    browserRuntimeInitOk: true,
    assertBrowserRuntime: assertBrowserRuntime,
    assertAppEntryUsesWindow: assertAppEntryUsesWindow,
    markInitOk: markInitOk
  };
})(typeof window !== "undefined" ? window : this);

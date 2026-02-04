// frontend/system/watchdog.js

(function () {
  "use strict";
  if (window.LunaWatchdog) return;

  const HEARTBEAT_INTERVAL = 5000; // ms
  let lastTaskActivity = Date.now();
  let lastNavActivity = Date.now();

  window.LunaWatchdog = {
    markTaskActivity: function () {
      lastTaskActivity = Date.now();
    },

    markNavActivity: function () {
      lastNavActivity = Date.now();
    },
  };

  function checkFrontendHealth() {
    const now = Date.now();
    const staleTask = now - lastTaskActivity > 15000; // 15s
    const staleNav = now - lastNavActivity > 15000;

    if (staleTask && staleNav) {
      // 触发一次前端自恢复（例如刷新导航、重置任务链）
      console.warn("[Watchdog] Frontend seems stalled, requesting backend status...");
      fetch("/api/v1/system/status")
        .then((r) => r.json())
        .then((data) => {
          console.log("[Watchdog] Backend status:", data);
          if (!data.success || data.data.status !== "running") {
            // 请求后端执行重启
            return fetch("/api/v1/system/reboot", { method: "POST" });
          }
        })
        .catch((err) => {
          console.error("[Watchdog] system status check failed", err);
        });
    }
  }

  setInterval(checkFrontendHealth, HEARTBEAT_INTERVAL);

  console.log("[LunaWatchdog] 前端看门狗已启动");
})();


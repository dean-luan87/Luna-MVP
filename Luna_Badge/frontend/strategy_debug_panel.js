// frontend/strategy_debug_panel.js
// 策略调试面板：记录所有策略事件

(function () {
  "use strict";
  if (window.StrategyDebugPanel) return;

  const Hooks = window.Hooks || { onActionSuggest: [] };
  const EventDispatcher = window.EventDispatcher || { subscribe: () => {} };

  class StrategyDebugPanelClass {
    constructor() {
      this.history = [];
      this.maxHistory = 50;
    }

    logStrategy(event) {
      const ts = new Date().toISOString();
      const entry = {
        time: ts,
        severity: event.severity || "info",
        code: event.code || "UNKNOWN",
        message: event.message || "",
        raw: event,
      };

      this.history.push(entry);
      if (this.history.length > this.maxHistory) {
        this.history.shift();
      }

      if (window.__debugPanel && typeof window.__debugPanel.logStrategy === "function") {
        window.__debugPanel.logStrategy(entry);
      } else if (window.__debugPanel) {
        // 没有 logStrategy 方法时，使用现有方法
        if (typeof window.__debugPanel.logTask === "function") {
          window.__debugPanel.logTask(
            `🎯 策略 [${entry.severity}] (${entry.code}) ${entry.message}`
          );
        } else if (typeof window.__debugPanel.logNav === "function") {
          window.__debugPanel.logNav(
            `🎯 策略 [${entry.severity}] (${entry.code}) ${entry.message}`
          );
        } else {
          console.log("[__debugPanel.logStrategy]", entry);
        }
      } else {
        // 没有 UI 面板时，打到控制台
        const severityColor = {
          critical: "🔴",
          warning: "🟡",
          info: "🔵",
          success: "🟢",
        };
        const icon = severityColor[entry.severity] || "⚪";
        console.log(
          `[StrategyDebug] ${icon} ${entry.time} [${entry.severity}] (${entry.code}) ${entry.message}`
        );
      }
    }

    getHistory() {
      return this.history.slice();
    }

    clearHistory() {
      this.history = [];
    }
  }

  const panel = new StrategyDebugPanelClass();

  // 挂到全局
  window.StrategyDebugPanel = panel;

  // 给已有 debugPanel 扩展一个 logStrategy
  if (window.__debugPanel && !window.__debugPanel.logStrategy) {
    window.__debugPanel.logStrategy = function (entry) {
      // 简单串到 existing logTask/logNav
      if (typeof window.__debugPanel.logTask === "function") {
        window.__debugPanel.logTask(
          `🎯 策略 [${entry.severity}] (${entry.code}) ${entry.message}`
        );
      } else if (typeof window.__debugPanel.logNav === "function") {
        window.__debugPanel.logNav(
          `🎯 策略 [${entry.severity}] (${entry.code}) ${entry.message}`
        );
      } else {
        console.log("[__debugPanel.logStrategy]", entry);
      }
    };
  }

  // 处理策略事件的函数
  function handleStrategyEvent(data) {
    const message =
      data.message ||
      (window.SpeechPolicy && typeof window.SpeechPolicy.getHazardSentence === "function"
        ? window.SpeechPolicy.getHazardSentence(data)
        : "策略提示（未定义文案）");

    panel.logStrategy({
      severity: data.severity || (data.distance && data.distance < 0.5 ? "critical" : "warning"),
      code: data.code || "NAV_STRATEGY",
      message: message,
      data: data,
    });
  }

  // 绑定 Hooks.onActionSuggest
  if (Hooks.onActionSuggest && Array.isArray(Hooks.onActionSuggest)) {
    Hooks.onActionSuggest.push(handleStrategyEvent);
  }

  // 同时监听EventDispatcher的NAV_GUIDANCE事件
  if (EventDispatcher.subscribe) {
    EventDispatcher.subscribe(function (event) {
      if (event.type === "NAV_GUIDANCE") {
        panel.logStrategy({
          severity: event.severity || "info",
          code: event.code || "NAV_STRATEGY",
          message: event.message || "",
          raw: event,
        });
      }
    });
  }

  console.log("[StrategyDebugPanel] 策略调试面板已加载");
})();




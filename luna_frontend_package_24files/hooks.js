// frontend/hooks.js
// 全局钩子系统（Hooks）- 情绪/任务系统预留钩子

(function () {
  "use strict";
  if (window.Hooks) return;

  window.Hooks = {
    onHazard: [],
    onStep: [],
    onNavigation: [],
    onEmotion: [],
    onTask: [],
    onActionSuggest: [], // v1.1.1 新增：动作建议入口（1.2.0 用）

    emit(list, data) {
      if (!Array.isArray(list)) {
        console.warn("[Hooks] List must be an array");
        return;
      }
      list.forEach((fn) => {
        try {
          if (typeof fn === "function") {
            fn(data);
          }
        } catch (e) {
          console.error("[Hooks] Hook execution error:", e);
        }
      });
    },

    // 注册钩子
    on(eventName, callback) {
      if (!this[eventName]) {
        console.warn(`[Hooks] Unknown event: ${eventName}`);
        return;
      }
      if (typeof callback !== "function") {
        console.warn("[Hooks] Callback must be a function");
        return;
      }
      this[eventName].push(callback);
    },

    // 移除钩子
    off(eventName, callback) {
      if (!this[eventName]) return;
      const index = this[eventName].indexOf(callback);
      if (index > -1) {
        this[eventName].splice(index, 1);
      }
    },
  };

  console.log("[Hooks] 全局钩子系统已加载");
})();


// frontend/core/error/ErrorHandler.js
// 错误处理模块：监听NAV_ERROR事件并显示

(function () {
  "use strict";
  if (window.ErrorHandler) return;

  const EventDispatcher = window.EventDispatcher || { subscribe: () => {} };
  const ErrorCodeMapper = window.errorCodeMapper || null;
  const GuidanceBubble = window.GuidanceBubble || null;

  class ErrorHandlerClass {
    constructor() {
      this.errorHistory = [];
      this.maxHistory = 50;
    }

    /**
     * 处理错误事件
     * @param {Object} event - 错误事件
     */
    handle(event) {
      if (event.type !== "NAV_ERROR") {
        return;
      }

      // 映射错误码（如果ErrorCodeMapper可用）
      let errorInfo = event;
      if (ErrorCodeMapper && typeof ErrorCodeMapper.map === "function") {
        errorInfo = ErrorCodeMapper.map(event.code, event.message);
      }

      // 记录错误历史
      this.errorHistory.push({
        ...errorInfo,
        timestamp: Date.now(),
      });

      if (this.errorHistory.length > this.maxHistory) {
        this.errorHistory.shift();
      }

      // 显示错误提示（如果GuidanceBubble可用）
      if (GuidanceBubble && typeof GuidanceBubble.show === "function") {
        GuidanceBubble.show({
          message: errorInfo.message || "导航系统出现错误",
          severity: errorInfo.severity || "error",
          duration: errorInfo.severity === "critical" ? 6000 : 4000,
          position: "top-right",
        });
      }

      // 控制台输出
      const severityIcon = {
        critical: "🔴",
        error: "🟠",
        warning: "🟡",
        info: "🔵",
      };

      const icon = severityIcon[errorInfo.severity] || "⚪";
      console.error(
        `[ErrorHandler] ${icon} [${errorInfo.module || "Unknown"}] ${errorInfo.code}: ${errorInfo.message}`,
        errorInfo
      );

      // 触发自定义事件（供其他模块监听）
      if (window.dispatchEvent) {
        window.dispatchEvent(
          new CustomEvent("navigation_error", {
            detail: errorInfo,
          })
        );
      }
    }

    /**
     * 获取错误历史
     * @returns {Array} 错误历史数组
     */
    getHistory() {
      return this.errorHistory.slice();
    }

    /**
     * 清空错误历史
     */
    clearHistory() {
      this.errorHistory = [];
    }
  }

  const handler = new ErrorHandlerClass();

  // 监听EventDispatcher的NAV_ERROR事件
  if (EventDispatcher.subscribe) {
    EventDispatcher.subscribe(function (event) {
      if (event.type === "NAV_ERROR") {
        handler.handle(event);
      }
    });
  }

  // 挂载到全局
  window.ErrorHandler = ErrorHandlerClass;
  window.errorHandler = handler;

  console.log("[ErrorHandler] 错误处理模块已加载并自动监听NAV_ERROR事件");
})();




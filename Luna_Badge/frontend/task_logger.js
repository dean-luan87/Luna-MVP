// frontend/task_logger.js
// 统一任务日志 + 后端上报

(function () {
  "use strict";

  if (window.TaskLogger) return;

  class TaskLogger {
    constructor() {
      this.logs = [];
      this.uploadUrl = "/log_task_event"; // 后端路由，后面在 Flask 里补
    }

    _push(level, source, message, extra) {
      const entry = {
        ts: new Date().toISOString(),
        level,
        source,
        message,
        extra: extra || null,
      };
      this.logs.push(entry);
      console.log(`[TaskLog][${level}][${source}] ${message}`, extra || "");

      // 异步上报后端
      try {
        fetch(this.uploadUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(entry),
        }).catch(() => {});
      } catch (e) {
        // 忽略网络错误
      }
    }

    info(source, msg, extra) {
      this._push("INFO", source, msg, extra);
    }
    warn(source, msg, extra) {
      this._push("WARN", source, msg, extra);
    }
    error(source, msg, extra) {
      this._push("ERROR", source, msg, extra);
    }

    dump() {
      return this.logs.slice();
    }
  }

  window.TaskLogger = new TaskLogger();
})();

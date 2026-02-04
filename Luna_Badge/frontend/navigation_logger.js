// =====================================================
// Unified Navigation Logger — v1.0
// 统一记录导航视觉 → 推理 → FSM → taskChain → 执行器 → 播报 的全链路日志
// =====================================================

(function () {
  'use strict';

  if (window.NavLog) return;

  class NavLogger {
    constructor() {
      this.logs = [];
      this.enabled = true;

      // 将日志同步写入后台
      this.autoUpload = true;
      this.uploadURL = "/log_nav_event";
    }

    // =====================================================
    // 基础日志方法
    // =====================================================
    _log(level, source, message, extra = null) {
      if (!this.enabled) return;

      const entry = {
        time: new Date().toISOString(),
        level,
        source,
        message,
        extra
      };

      this.logs.push(entry);
      
      // 控制台输出
      const logMethod = level === 'ERROR' ? console.error : (level === 'WARN' ? console.warn : console.log);
      logMethod(`[${level}] [${source}] ${message}`, extra || "");

      // 限制日志数量（避免内存溢出）
      if (this.logs.length > 1000) {
        this.logs.shift(); // 移除最旧的日志
      }

      // 自动上传到后台
      if (this.autoUpload) {
        this._upload(entry);
      }
    }

    info(source, msg, extra = null) {
      this._log("INFO", source, msg, extra);
    }

    warn(source, msg, extra = null) {
      this._log("WARN", source, msg, extra);
    }

    error(source, msg, extra = null) {
      this._log("ERROR", source, msg, extra);
    }

    // =====================================================
    // 后台上传
    // =====================================================
    _upload(entry) {
      try {
        fetch(this.uploadURL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(entry)
        }).catch(err => {
          // 静默失败，避免影响主流程
          console.warn("[NavLog] 后台上传失败", err);
        });
      } catch (err) {
        console.warn("[NavLog] 后台上传异常", err);
      }
    }

    // 清空日志（不常用）
    clear() {
      this.logs = [];
    }

    // 下载日志（给你调试）
    download() {
      const blob = new Blob(
        [JSON.stringify(this.logs, null, 2)],
        { type: "application/json" }
      );
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `navigation_logs_${Date.now()}.json`;
      a.click();
      URL.revokeObjectURL(url);
    }

    // 获取最近N条日志
    getRecent(count = 50) {
      return this.logs.slice(-count);
    }

    // 按来源过滤日志
    getBySource(source) {
      return this.logs.filter(log => log.source === source);
    }
  }

  window.NavLog = new NavLogger();
  console.log("[NavLog] 统一导航日志系统已加载");
})();


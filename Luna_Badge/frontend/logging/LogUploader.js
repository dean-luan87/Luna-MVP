// frontend/logging/LogUploader.js
// 全链路日志上传系统

(function () {
  "use strict";
  if (window.LogUploader) return;

  const ErrorCode = window.ErrorCode || {};

  class LogUploaderClass {
    constructor() {
      this.queue = [];
      this.endpoint = "/api/v1/log/client"; // 使用统一API Gateway
      this.flushInterval = 5000; // 5秒自动刷新一次
      this.maxQueueSize = 100;
      this._startAutoFlush();
    }

    _startAutoFlush() {
      setInterval(() => {
        this.flush();
      }, this.flushInterval);
    }

    push(entry) {
      const log = {
        timestamp: Date.now(),
        ts: new Date().toISOString(),
        ...entry,
      };

      this.queue.push(log);

      // 防止队列过大
      if (this.queue.length > this.maxQueueSize) {
        this.queue.shift();
      }

      // 立即尝试上传（不阻塞）
      this.flush().catch(() => {
        // 静默失败，等待下次自动刷新
      });
    }

    async flush() {
      if (this.queue.length === 0) return;

      const payload = [...this.queue];
      this.queue = [];

      try {
        const response = await fetch(this.endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const result = await response.json();
        if (result.success) {
          console.debug("[LogUploader] 日志上传成功", { count: payload.length });
        } else {
          throw new Error(result.message || "Upload failed");
        }
      } catch (err) {
        // 上传失败，重新加入队列（保留最近的）
        console.warn("[LogUploader] 日志上传失败，重新入队", err);
        this.queue.unshift(...payload.slice(-50)); // 只保留最近50条
      }
    }

    // 立即上传并等待完成
    async flushSync() {
      while (this.queue.length > 0) {
        await this.flush();
      }
    }
  }

  window.LogUploader = new LogUploaderClass();
  console.log("[LogUploader] 全链路日志上传系统已加载");
})();




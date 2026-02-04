// frontend/task_chain_unified.js
// 统一任务链（TaskChain）- 新增基础管线

(function () {
  "use strict";
  if (window.TaskChainUnified) return;

  class TaskChainUnified {
    constructor() {
      this.queue = [];
      this.running = false;
    }

    enqueue(task) {
      if (typeof task !== "function") {
        console.warn("[TaskChainUnified] Task must be a function");
        return;
      }
      this.queue.push(task);
      this.run();
    }

    async run() {
      if (this.running) return;
      this.running = true;

      while (this.queue.length > 0) {
        const task = this.queue.shift();
        try {
          await task();
        } catch (err) {
          console.error("[TaskChainUnified] Task error:", err);
          // 记录错误日志
          if (window.LogUploader) {
            window.LogUploader.push({
              level: "error",
              code: window.ErrorCode?.TASK_STEP_ERROR || "E_TASK_STEP_ERROR",
              message: "TaskChainUnified task failed",
              error: err.toString(),
              source: "TaskChainUnified",
            });
          }
        }
      }

      this.running = false;
    }

    clear() {
      this.queue = [];
      this.running = false;
    }

    getQueueLength() {
      return this.queue.length;
    }
  }

  window.TaskChainUnified = new TaskChainUnified();
  console.log("[TaskChainUnified] 统一任务链已加载");
})();




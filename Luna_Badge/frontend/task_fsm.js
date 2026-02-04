// frontend/task_fsm.js
// Task FSM：idle / pending / running / waiting / paused / finished / failed

(function () {
  "use strict";

  if (window.TaskFSM) return;

  const logger = window.TaskLogger || {
    info: console.log,
    warn: console.warn,
    error: console.error,
  };

  class TaskFSM {
    constructor() {
      this.state = "idle";
      this.currentTask = null;
    }

    getState() {
      return this.state;
    }

    _setState(next, detail) {
      const prev = this.state;
      this.state = next;
      logger.info("TaskFSM", `状态 ${prev} → ${next}`, detail || {});
    }

    onTaskEnqueued(task) {
      if (this.state === "idle" || this.state === "finished") {
        this._setState("pending", { reason: "first_task_enqueued" });
      }
    }

    beforeTaskRun(task) {
      this.currentTask = task;
      this._setState("running", { taskType: task.type });
    }

    afterTaskRun(task, ok) {
      if (!ok) {
        this._setState("failed", { taskType: task.type });
      } else {
        logger.info("TaskFSM", "单个任务执行完成", { taskType: task.type });
      }
    }

    onAllTasksFinished() {
      this.currentTask = null;
      this._setState("finished");
    }

    pause(reason) {
      this._setState("paused", { reason });
    }

    resume() {
      this._setState("running", { reason: "resume" });
    }

    wait(reason) {
      this._setState("waiting", { reason });
    }

    reset() {
      this.currentTask = null;
      this._setState("idle", { reason: "reset" });
    }
  }

  window.TaskFSM = new TaskFSM();
})();

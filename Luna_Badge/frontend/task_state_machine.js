// =====================================================
// Task State Machine — v1.0
// 控制任务从 pending → running → waiting → paused → finished → failed 的状态流转
// =====================================================

(function () {
    "use strict";

    if (window.TaskStateMachine) return;

    class TaskStateMachine {
        constructor() {
            this.state = "idle";   // idle | pending | running | waiting | paused | finished | failed
            this.context = {};     // 存储任务链上下文（当前step、历史step、环境状态）
            this.history = [];     // 状态历史记录
        }

        setState(newState, meta = {}) {
            const prev = this.state;
            
            // 状态转移验证
            if (!this._canTransition(prev, newState)) {
                console.warn(`[TaskStateMachine] 不允许的状态转移: ${prev} → ${newState}`);
                return false;
            }

            this.state = newState;
            this.history.push({
                from: prev,
                to: newState,
                timestamp: Date.now(),
                meta: meta
            });

            console.log(`[TaskStateMachine] ${prev} → ${newState}`, meta);

            // 状态转移事件
            if (newState === "running") this.onRunning(meta);
            if (newState === "waiting") this.onWaiting(meta);
            if (newState === "paused") this.onPaused(meta);
            if (newState === "finished") this.onFinished(meta);
            if (newState === "failed") this.onFailed(meta);

            return true;
        }

        _canTransition(from, to) {
            const allowed = {
                "idle": ["pending", "running"],
                "pending": ["running", "paused", "failed"],
                "running": ["waiting", "paused", "finished", "failed"],
                "waiting": ["running", "paused", "failed"],
                "paused": ["running", "finished", "failed"],
                "finished": ["idle", "pending"],
                "failed": ["idle", "pending"]
            };

            return (allowed[from] || []).includes(to);
        }

        onRunning(meta) {
            // 负责调用 stepRunner
            if (window.logInfo) {
                window.logInfo('[TaskStateMachine] 任务开始运行', meta);
            }
            
            // 触发事件
            if (window.taskChain && typeof window.taskChain.onStateChange === 'function') {
                window.taskChain.onStateChange('running', meta);
            }
        }

        onWaiting(meta) {
            // 例如等待用户回复、等红绿灯、等叫号
            // 此处无需填内容，由 stepRunner 调用即可
            if (window.logInfo) {
                window.logInfo('[TaskStateMachine] 任务等待中', meta);
            }
        }

        onPaused(meta) {
            // 中断任务（如用户去洗手间）
            if (window.logInfo) {
                window.logInfo('[TaskStateMachine] 任务已暂停', meta);
            }
            
            // 触发事件
            if (window.taskChain && typeof window.taskChain.onStateChange === 'function') {
                window.taskChain.onStateChange('paused', meta);
            }
        }

        onFinished(meta) {
            if (window.logInfo) {
                window.logInfo('[TaskStateMachine] 任务已完成', meta);
            }
            
            // 触发事件
            if (window.taskChain && typeof window.taskChain.onStateChange === 'function') {
                window.taskChain.onStateChange('finished', meta);
            }
        }

        onFailed(meta) {
            if (window.logError) {
                window.logError('[TaskStateMachine] 任务失败', meta);
            }
            
            // 触发事件
            if (window.taskChain && typeof window.taskChain.onStateChange === 'function') {
                window.taskChain.onStateChange('failed', meta);
            }
        }

        getState() {
            return this.state;
        }

        getContext() {
            return this.context;
        }

        updateContext(key, value) {
            this.context[key] = value;
        }

        getHistory() {
            return this.history;
        }
    }

    window.TaskStateMachine = new TaskStateMachine();
    console.log("[TaskStateMachine] 已加载");
})();




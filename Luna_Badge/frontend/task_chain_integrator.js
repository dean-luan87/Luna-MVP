// =====================================================
// TaskChain Integrator — v1.0
// 负责把 FSM、IntentTracker 与 TaskChain 组合成统一任务系统
// =====================================================

(function () {
    "use strict";

    if (window.TaskChainIntegrator) return;

    class TaskChainIntegrator {
        constructor() {
            this.fsm = window.TaskStateMachine || null;
            this.intent = window.IntentContextTracker || null;
            this.taskChain = window.taskChain || null;
            this.logger = window.TaskLogger || null;
        }

        handleUserInput(text) {
            if (!this.intent) {
                console.warn('[TaskChainIntegrator] IntentContextTracker 未初始化');
                return { success: false, message: "系统未就绪" };
            }

            const decision = this.intent.updateIntent(text);

            if (this.logger) {
                this.logger.log({
                    type: 'user_input',
                    text: text,
                    decision: decision
                });
            }

            switch (decision) {
                case "cancel":
                    return this._handleCancel(text);

                case "resume":
                    return this._handleResume(text);

                case "insert":
                    return this._handleInsert(text);

                case "replace":
                    return this._handleReplace(text);

                case "continue":
                default:
                    return this._handleContinue(text);
            }
        }

        _handleCancel(text) {
            if (this.fsm) {
                this.fsm.setState("paused", { reason: "user_cancel", text });
            }

            if (this.taskChain && typeof this.taskChain.interrupt === 'function') {
                this.taskChain.interrupt();
            }

            return {
                success: true,
                message: "任务已暂停",
                action: "cancel"
            };
        }

        _handleResume(text) {
            if (this.fsm) {
                this.fsm.setState("running", { reason: "user_resume", text });
            }

            if (this.taskChain && typeof this.taskChain.resume === 'function') {
                // 假设 taskChain 有 resume 方法
                // this.taskChain.resume();
            }

            return {
                success: true,
                message: "继续执行任务",
                action: "resume"
            };
        }

        _handleInsert(text) {
            console.log("[TaskChainIntegrator] 检测到插入任务:", text);

            // 暂停当前任务
            if (this.taskChain && typeof this.taskChain.interrupt === 'function') {
                this.taskChain.interrupt();
            }

            // 构建临时任务
            const tempTask = this._buildTempTask(text);
            if (this.intent) {
                this.intent.setInsertedTask(tempTask);
            }

            // 插入到任务链
            if (this.taskChain && typeof this.taskChain.enqueue === 'function') {
                if (Array.isArray(tempTask.steps)) {
                    // 如果是 taskPlan 格式
                    this.taskChain.enqueue(tempTask);
                } else {
                    // 如果是单个任务
                    tempTask.steps.forEach(step => {
                        this.taskChain.enqueue(step.type, step.payload, step.priority || 'HIGH');
                    });
                }
            }

            if (this.fsm) {
                this.fsm.setState("running", { reason: "insert_task", task: tempTask });
            }

            return {
                success: true,
                message: "正在执行插入任务",
                action: "insert",
                task: tempTask
            };
        }

        _handleReplace(text) {
            console.log("[TaskChainIntegrator] 检测到新主任务:", text);

            // 重置任务链
            if (this.taskChain && typeof this.taskChain.clear === 'function') {
                this.taskChain.clear();
            }

            // 构建新主任务
            const mainTask = this._buildMainTask(text);
            if (this.intent) {
                this.intent.setMainTask(mainTask);
                this.intent.clearInsertedTask();
            }

            // 加载新任务
            if (this.taskChain && typeof this.taskChain.enqueue === 'function') {
                this.taskChain.enqueue(mainTask);
            }

            if (this.fsm) {
                this.fsm.setState("running", { reason: "replace_task", task: mainTask });
            }

            return {
                success: true,
                message: "已开始新的主任务",
                action: "replace",
                task: mainTask
            };
        }

        _handleContinue(text) {
            return {
                success: true,
                message: "继续当前任务",
                action: "continue"
            };
        }

        _buildTempTask(text) {
            // 提取目标地点
            const target = text.replace(/(顺便|先去|顺路|拿个东西|买)/g, "").trim();
            
            return {
                taskId: `insert_${Date.now()}`,
                type: "INSERT_TASK",
                steps: [
                    {
                        type: "MOVE_TOWARDS_TARGET",
                        payload: { target: target },
                        priority: "HIGH"
                    },
                    {
                        type: "CONFIRM_ARRIVAL_BY_OCR",
                        payload: { keywords: [target] },
                        priority: "MEDIUM"
                    },
                    {
                        type: "ANNOUNCE_ARRIVAL",
                        payload: { message: `已到达 ${target}` },
                        priority: "LOW"
                    }
                ]
            };
        }

        _buildMainTask(text) {
            // 提取目标地点
            const destination = text.replace(/(我要去|带我去|导航到|去一下|去一趟|帮我)/g, "").trim();
            
            return {
                taskId: `main_${Date.now()}`,
                type: "MAIN_TASK",
                steps: [
                    {
                        type: "NAV_START",
                        payload: { destination: destination },
                        priority: "HIGH"
                    },
                    {
                        type: "MOVE_TOWARDS_TARGET",
                        payload: { target: destination },
                        priority: "HIGH"
                    },
                    {
                        type: "CONFIRM_ARRIVAL_BY_DISTANCE_OR_OCR",
                        payload: { targetText: destination },
                        priority: "MEDIUM"
                    },
                    {
                        type: "ANNOUNCE_ARRIVAL",
                        payload: { message: `已到达 ${destination}` },
                        priority: "CRITICAL"
                    }
                ]
            };
        }
    }

    window.TaskChainIntegrator = new TaskChainIntegrator();
    console.log("[TaskChainIntegrator] 已加载");
})();




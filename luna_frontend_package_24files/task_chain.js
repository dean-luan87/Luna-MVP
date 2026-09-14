/**
 * 轻量级任务链系统（规范要求）
 * 提供可插拔、可恢复、可中断的任务执行流程
 */

(function() {
    'use strict';

    // ✅ G: 引入单例
    const TaskLogger = window.TaskLogger;
    const TaskFSM = window.TaskFSM;
    const IntentTracker = window.IntentTracker;
    const NavigationExecutors = window.NavigationExecutors;

    /**
     * 任务优先级枚举
     */
    const TaskPriority = {
        CRITICAL: 0,  // 危险、台阶（最高优先级）
        HIGH: 1,      // 导航转向
        MEDIUM: 2,    // 标识牌、设施
        LOW: 3        // 普通提示
    };

    /**
     * 任务类型枚举
     */
    const TaskType = {
        HAZARD_WARNING: 'hazard_warning',
        STEP_WARNING: 'step_warning',
        NAVIGATION: 'navigation',
        TTS_BROADCAST: 'tts_broadcast',
        UI_UPDATE: 'ui_update',
        LOG_RECORD: 'log_record',
        EMOTION_EVENT: 'emotion_event'
    };

    /**
     * 任务链管理器
     */
    class TaskChain {
        constructor() {
            this.queue = [];
            this.running = false;
            this.currentTask = null;
            this.handlers = new Map();
            this.stats = {
                totalEnqueued: 0,
                totalCompleted: 0,
                totalFailed: 0,
                totalInterrupted: 0
            };
            
            // 注册默认处理器
            this._registerDefaultHandlers();
            
            console.log('✅ TaskChain初始化完成', { module: 'task_chain' });
        }

        /**
         * 注册默认处理器
         */
        _registerDefaultHandlers() {
            // 危险警告处理器
            this.registerHandler(TaskType.HAZARD_WARNING, async (payload) => {
                const { type, level, meta } = payload;
                console.log(`🚨 [TaskChain] 处理危险警告: ${type}, 级别: ${level}`, { module: 'task_chain', meta });
                
                // 触发统一事件（如果存在）
                if (window.emitHazardEvent) {
                    window.emitHazardEvent({ type, level, meta });
                } else {
                    // 降级处理：直接调用TTS
                    if (window.speakText) {
                        const message = this._generateHazardMessage(type, level, meta);
                        await window.speakText(message, 'urgent', true);
                    }
                }
            });

            // 台阶警告处理器
            this.registerHandler(TaskType.STEP_WARNING, async (payload) => {
                const { direction, distance, meta } = payload;
                console.log(`📐 [TaskChain] 处理台阶警告: ${direction}, 距离: ${distance}`, { module: 'task_chain', meta });
                
                if (window.emitHazardEvent) {
                    window.emitHazardEvent({ type: 'step', level: 'high', meta: { direction, distance, ...meta } });
                } else {
                    if (window.speakText) {
                        const message = `前方${distance}米有台阶，请${direction === 'up' ? '减速' : '小心'}`;
                        await window.speakText(message, 'urgent', true);
                    }
                }
            });

            // 导航处理器
            this.registerHandler(TaskType.NAVIGATION, async (payload) => {
                const { action, direction, distance, meta } = payload;
                console.log(`🧭 [TaskChain] 处理导航: ${action}, 方向: ${direction}`, { module: 'task_chain', meta });
                
                if (window.emitNavigationEvent) {
                    window.emitNavigationEvent({ action, direction, distance, ...meta });
                } else {
                    // 降级处理
                    if (window.speakText) {
                        const message = this._generateNavigationMessage(action, direction, distance);
                        await window.speakText(message, 'cheerful', true);
                    }
                }
            });

            // TTS播报处理器
            this.registerHandler(TaskType.TTS_BROADCAST, async (payload) => {
                const { text, style, priority } = payload;
                console.log(`🔊 [TaskChain] TTS播报: ${text.substring(0, 30)}...`, { module: 'task_chain' });
                
                if (window.speakText) {
                    await window.speakText(text, style || 'calm', priority || false);
                }
            });

            // UI更新处理器
            this.registerHandler(TaskType.UI_UPDATE, async (payload) => {
                const { elementId, content, className } = payload;
                console.log(`🖥️ [TaskChain] UI更新: ${elementId}`, { module: 'task_chain' });
                
                const element = document.getElementById(elementId);
                if (element) {
                    if (content !== undefined) {
                        element.textContent = content;
                    }
                    if (className !== undefined) {
                        element.className = className;
                    }
                }
            });

            // 日志记录处理器
            this.registerHandler(TaskType.LOG_RECORD, async (payload) => {
                const { level, message, meta } = payload;
                console.log(`📝 [TaskChain] 日志记录: ${level} - ${message}`, { module: 'task_chain', meta });
                
                // 可以发送到后端日志API
                if (window.lunaLog) {
                    window.lunaLog(level, message, meta || {});
                }
            });

            // 情绪事件处理器
            this.registerHandler(TaskType.EMOTION_EVENT, async (payload) => {
                const { event, level, meta } = payload;
                console.log(`💭 [TaskChain] 情绪事件: ${event}, 级别: ${level}`, { module: 'task_chain', meta });
                
                // 触发情绪事件hook（如果存在）
                if (window.emotion_event) {
                    window.emotion_event(event, level, meta);
                } else {
                    // 降级：只记录日志
                    console.log(`[情绪事件] ${event} (级别: ${level})`, meta);
                }
            });

            // ✅ Scene Nodes 任务类型处理器
            this.registerHandler('SCAN_ENV', async (payload) => {
                const { target, scene } = payload;
                console.log(`🔍 [TaskChain] 扫描环境: ${target}`, { module: 'task_chain', scene });
                
                // 使用 SceneNodeDetector 扫描环境
                if (window.SceneNodeDetector && window.latestYOLOResult) {
                    window.SceneNodeDetector.updateDetections(window.latestYOLOResult);
                }
                
                // 语音提示
                if (window.speakText) {
                    await window.speakText(`正在扫描环境，寻找${target}`, 'calm', false);
                }
            });

            this.registerHandler('MOVE_TO_NODE', async (payload) => {
                const { nodeName, scene } = payload;
                console.log(`🚶 [TaskChain] 前往节点: ${nodeName}`, { module: 'task_chain', scene });
                
                // 语音提示
                if (window.speakText) {
                    await window.speakText(`正在前往${nodeName}`, 'calm', false);
                }
                
                // 可以在这里集成导航逻辑
                if (window.NodeTaskBridge && typeof window.NodeTaskBridge.goToNode === 'function') {
                    // 节点任务桥接器会处理导航逻辑
                }
            });

            this.registerHandler('CONFIRM_ARRIVAL', async (payload) => {
                const { nodeName, scene } = payload;
                console.log(`✅ [TaskChain] 确认到达: ${nodeName}`, { module: 'task_chain', scene });
                
                // 确认节点到达
                if (window.SceneNodes && typeof window.SceneNodes.confirmNode === 'function') {
                    window.SceneNodes.confirmNode(nodeName, {
                        confirmedBy: 'task_chain',
                        confirmedAt: Date.now()
                    });
                }
                
                // 语音提示
                if (window.speakText) {
                    await window.speakText(`已到达${nodeName}`, 'calm', false);
                }
            });
        }

        /**
         * 注册任务处理器
         */
        registerHandler(taskType, handler) {
            this.handlers.set(taskType, handler);
            console.log(`✅ [TaskChain] 注册处理器: ${taskType}`, { module: 'task_chain' });
        }

        /**
         * 入队任务
         * 支持两种格式：
         * 1. 旧格式：enqueue(taskType, payload, priority)
         * 2. 新格式：enqueue(taskPlan) - taskPlan 包含 steps 数组
         */
        enqueue(taskTypeOrPlan, payload, priority = TaskPriority.MEDIUM) {
            // 转换字符串优先级到数字
            if (typeof priority === 'string') {
                const priorityMap = {
                    'CRITICAL': TaskPriority.CRITICAL,
                    'HIGH': TaskPriority.HIGH,
                    'MEDIUM': TaskPriority.MEDIUM,
                    'LOW': TaskPriority.LOW
                };
                priority = priorityMap[priority] !== undefined ? priorityMap[priority] : TaskPriority.MEDIUM;
            }
            
            // 检测是否是 taskPlan 格式（有 steps 数组）
            if (taskTypeOrPlan && typeof taskTypeOrPlan === 'object' && Array.isArray(taskTypeOrPlan.steps)) {
                // 新格式：taskPlan 对象
                const taskPlan = taskTypeOrPlan;
                console.log(`📋 [TaskChain] 任务计划入队: ${taskPlan.taskId || 'unknown'}`, { 
                    module: 'task_chain', 
                    steps: taskPlan.steps?.length || 0 
                });
                
                // 记录日志
                if (window.__lunaLog) {
                    window.__lunaLog('task_enqueue', { taskPlan });
                } else if (window.LunaLogger) {
                    window.LunaLogger.info('task_enqueue', { taskPlan });
                }
                
                // 自动执行任务计划
                if (window.TaskChainExecutor && typeof window.TaskChainExecutor.runTask === 'function') {
                    window.TaskChainExecutor.runTask(taskPlan).catch(err => {
                        console.error(`❌ [TaskChain] 任务计划执行失败: ${taskPlan.taskId}`, { 
                            module: 'task_chain', 
                            error: err.message 
                        });
                    });
                } else {
                    console.warn(`⚠️ [TaskChain] TaskChainExecutor 未初始化，无法执行任务计划`, { module: 'task_chain' });
                }
                
                return taskPlan.taskId || `plan_${Date.now()}`;
            }
            
            // 旧格式：taskType, payload, priority
            const task = {
                id: `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
                type: taskTypeOrPlan,
                payload: payload || {},
                priority: priority,
                timestamp: Date.now(),
                status: 'pending'
            };

            // 按优先级插入队列
            let inserted = false;
            for (let i = 0; i < this.queue.length; i++) {
                if (this.queue[i].priority > priority) {
                    this.queue.splice(i, 0, task);
                    inserted = true;
                    break;
                }
            }
            if (!inserted) {
                this.queue.push(task);
            }

            this.stats.totalEnqueued++;
            console.log(`📋 [TaskChain] 任务入队: ${taskTypeOrPlan} (优先级: ${priority})`, { module: 'task_chain', taskId: task.id });
            
            // ✅ 记录 taskChain 任务入队日志
            if (window.NavLog) {
              window.NavLog.info("taskChain", "任务入队", { 
                type: task.type, 
                priority: task.priority, 
                taskId: task.id,
                payload: task.payload 
              });
            }

            // ✅ G: TaskLogger + TaskFSM 集成
            if (TaskLogger) {
                TaskLogger.info("TaskChain", "任务入队", {
                    type: task.type,
                    payload: task.payload || null,
                    priority: task.priority || "NORMAL",
                    taskId: task.id
                });
            }

            if (TaskFSM) {
                TaskFSM.onTaskEnqueued(task);
            }

            // 如果当前没有运行，启动处理
            if (!this.running) {
                this._processQueue();
            }

            return task.id;
        }

        /**
         * 执行任务内部逻辑
         */
        async _executeTaskInternal(task) {
            // —— BEGIN: 导航任务执行器优先检查（NavigationExecutors） ——
            if (NavigationExecutors) {
                switch (task.type) {
                    case "NAV_START":
                        await NavigationExecutors.execStart(task.payload);
                        return;
                    case "NAV_TURN":
                        await NavigationExecutors.execTurn(task.payload);
                        return;
                    case "NAV_STRAIGHT":
                        await NavigationExecutors.execStraight(task.payload);
                        return;
                    case "NAV_POI":
                        await NavigationExecutors.execPOI(task.payload);
                        return;
                    case "NAV_END":
                        await NavigationExecutors.execEnd(task.payload);
                        return;
                    case "NAV_ERROR":
                        await NavigationExecutors.execError(task.payload);
                        return;
                }
            }
            // —— END: 导航任务执行器优先检查 ——

            // —— BEGIN: 旧版导航任务执行器检查（兼容性） ——
            const executors = window.NavigationTaskExecutors || {};
            const executor = executors[task.type];
            
            if (executor) {
                // ✅ 记录执行器开始执行日志
                if (window.NavLog) {
                  window.NavLog.info("Executor", "开始执行任务", { type: task.type, taskId: task.id, payload: task.payload });
                }
                if (window.logInfo) {
                    window.logInfo(`[taskChain] Executing ${task.type}`, { taskId: task.id });
                }
                await executor(task);
                // ✅ 记录执行器完成日志
                if (window.NavLog) {
                  window.NavLog.info("Executor", "任务执行完成", { type: task.type, taskId: task.id });
                }
                return;
            }
            // —— END: 旧版导航任务执行器检查 ——

            // 使用注册的处理器
            const handler = this.handlers.get(task.type);
            if (handler) {
                await handler(task.payload);
            } else {
                // 场景节点任务类型处理
                switch (task.type) {
                    case "SCAN_ENV":
                        // TODO：可以在这里触发 YOLO 强制扫描一帧
                        if (window.SceneNodeDetector && window.latestYOLOResult) {
                            window.SceneNodeDetector.updateDetections(window.latestYOLOResult);
                        }
                        break;
                    case "MOVE_TO_NODE":
                        // TODO：根据 nodeName 调用导航逻辑 / 提示用户移动方向
                        const { nodeName } = task.payload || {};
                        if (window.speakText && nodeName) {
                            await window.speakText(`正在前往${nodeName}`, 'calm', false);
                        }
                        break;
                    case "CONFIRM_ARRIVAL":
                        // TODO：提示用户确认是否已到达
                        const { nodeName: arrivalNodeName } = task.payload || {};
                        if (window.SceneNodes && arrivalNodeName) {
                            window.SceneNodes.confirmNode(arrivalNodeName, {
                                confirmedBy: 'task_chain',
                                confirmedAt: Date.now()
                            });
                        }
                        if (window.speakText && arrivalNodeName) {
                            await window.speakText(`已到达${arrivalNodeName}`, 'calm', false);
                        }
                        break;
                    default:
                        if (TaskLogger) {
                            TaskLogger.warn("TaskChain", "未知任务类型", { type: task.type });
                        }
                        console.warn(`⚠️ [TaskChain] 未找到处理器: ${task.type}`, { module: 'task_chain', taskId: task.id });
                        throw new Error(`Unknown task type: ${task.type}`);
                }
            }
        }

        /**
         * 处理队列
         */
        async _processQueue() {
            if (this.running) {
                return;
            }

            this.running = true;

            while (this.queue.length > 0) {
                const task = this.queue.shift();
                this.currentTask = task;

                // ✅ G: TaskFSM beforeTaskRun
                if (TaskFSM) {
                    TaskFSM.beforeTaskRun(task);
                }
                if (TaskLogger) {
                    TaskLogger.info("TaskChain", "开始执行任务", {
                        type: task.type,
                        payload: task.payload || null,
                        taskId: task.id
                    });
                }

                let ok = true;
                try {
                    task.status = 'running';
                    console.log(`▶️ [TaskChain] 开始执行任务: ${task.type}`, { module: 'task_chain', taskId: task.id });

                    // 执行任务（内部逻辑）
                    await this._executeTaskInternal(task);
                    
                    task.status = 'completed';
                    this.stats.totalCompleted++;
                    console.log(`✅ [TaskChain] 任务完成: ${task.type}`, { module: 'task_chain', taskId: task.id });
                } catch (error) {
                    ok = false;
                    task.status = 'failed';
                    task.error = error.message;
                    this.stats.totalFailed++;
                    
                    // ✅ 记录任务失败日志
                    if (window.NavLog) {
                      window.NavLog.error("taskChain", "任务执行失败", { 
                        type: task.type, 
                        taskId: task.id, 
                        error: error.message,
                        stack: error.stack 
                      });
                    }
                    if (TaskLogger) {
                        TaskLogger.error("TaskChain", "任务执行异常", {
                            type: task.type,
                            error: error && error.message,
                            taskId: task.id
                        });
                    }
                    console.error(`❌ [TaskChain] 任务失败: ${task.type}`, { module: 'task_chain', taskId: task.id, error: error.message });
                }

                // ✅ G: TaskFSM afterTaskRun
                if (TaskFSM) {
                    TaskFSM.afterTaskRun(task, ok);
                }

                this.currentTask = null;
            }

            // ✅ G: 所有任务执行完成
            if (this.queue.length === 0) {
                if (TaskLogger) {
                    TaskLogger.info("TaskChain", "所有任务执行完成", {});
                }
                if (TaskFSM) {
                    TaskFSM.onAllTasksFinished();
                }
            }

            this.running = false;
            console.log(`🏁 [TaskChain] 队列处理完成`, { module: 'task_chain' });
        }

        /**
         * 中断当前任务
         */
        interrupt() {
            if (this.currentTask) {
                this.currentTask.status = 'interrupted';
                this.stats.totalInterrupted++;
                console.log(`⏸️ [TaskChain] 任务中断: ${this.currentTask.type}`, { module: 'task_chain', taskId: this.currentTask.id });
                
                // ✅ G: TaskFSM + TaskLogger
                if (TaskFSM) {
                    TaskFSM.pause("interrupted");
                }
                if (TaskLogger) {
                    TaskLogger.info("TaskChain", "任务中断", { taskId: this.currentTask.id, type: this.currentTask.type });
                }
                
                this.currentTask = null;
            }
        }

        /**
         * ✅ G: 暂停所有任务
         */
        pauseAll() {
            this.interrupt();
            if (TaskFSM) {
                TaskFSM.pause("user_pause");
            }
        }

        /**
         * ✅ G: 恢复所有任务
         */
        resumeAll() {
            if (TaskFSM) {
                TaskFSM.resume();
            }
            if (!this.running && this.queue.length > 0) {
                this._processQueue();
            }
        }

        /**
         * 清空队列
         */
        clear() {
            this.queue = [];
            this.interrupt();
            console.log(`🗑️ [TaskChain] 队列已清空`, { module: 'task_chain' });
        }

        /**
         * 获取统计信息
         */
        getStats() {
            return {
                ...this.stats,
                queueLength: this.queue.length,
                currentTask: this.currentTask ? {
                    id: this.currentTask.id,
                    type: this.currentTask.type,
                    status: this.currentTask.status
                } : null
            };
        }

        /**
         * 生成危险消息
         */
        _generateHazardMessage(type, level, meta) {
            const templates = {
                'water': '前方有积水，请小心',
                'obstacle': '前方有障碍物，请绕行',
                'slippery': '地面湿滑，请减速',
                'construction': '前方施工，请注意安全'
            };
            return templates[type] || `检测到${type}危险，请小心`;
        }

        /**
         * 生成导航消息
         */
        _generateNavigationMessage(action, direction, distance) {
            if (action === 'turn') {
                return `前方${distance || ''}米${direction === 'left' ? '左' : '右'}转`;
            } else if (action === 'straight') {
                return `请直行${distance ? distance + '米' : ''}`;
            } else if (action === 'stop') {
                return '已到达目的地';
            }
            return '请跟随导航指引';
        }
    }

    // 创建全局TaskChain实例
    window.taskChain = new TaskChain();

    // 导出便捷方法
    window.taskChainEnqueue = function(taskType, payload, priority) {
        return window.taskChain.enqueue(taskType, payload, priority);
    };

    console.log('✅ TaskChain模块加载完成', { module: 'task_chain' });

    // ✅ G: 用户语音处理函数（供外部调用）
    window.onUserSentenceRecognized = function(text) {
        if (!IntentTracker) {
            console.warn('[TaskChain] IntentTracker 未初始化');
            return;
        }

        const decision = IntentTracker.updateIntent(text);

        switch (decision) {
            case "cancel":
                if (TaskLogger) TaskLogger.info("Intent", "用户请求取消任务", { text });
                if (TaskFSM) TaskFSM.pause("user_cancel");
                // 可以清空队列或仅暂停
                if (window.taskChain && typeof window.taskChain.pauseAll === 'function') {
                    window.taskChain.pauseAll();
                }
                break;

            case "resume":
                if (TaskLogger) TaskLogger.info("Intent", "用户请求恢复任务", { text });
                if (TaskFSM) TaskFSM.resume();
                if (window.taskChain && typeof window.taskChain.resumeAll === 'function') {
                    window.taskChain.resumeAll();
                }
                break;

            case "insert":
                if (TaskLogger) TaskLogger.info("Intent", "用户请求插入任务", { text });
                // 这里可以解析插入目的地，构建一个临时任务，比如去711
                // 示例：构建临时导航任务
                if (window.taskChain && typeof window.taskChain.enqueue === 'function') {
                    // 提取目标（简化处理）
                    const target = text.replace(/(顺便|先去|顺路|路过)/g, "").trim();
                    window.taskChain.enqueue('NAV_POI', { name: target }, 'HIGH');
                }
                break;

            case "replace":
                if (TaskLogger) TaskLogger.info("Intent", "用户请求更换主任务", { text });
                // 清掉旧任务，重新构建导航任务
                if (window.taskChain && typeof window.taskChain.clear === 'function') {
                    window.taskChain.clear();
                }
                if (TaskFSM) {
                    TaskFSM.reset();
                }
                // 提取目标并构建新任务（简化处理）
                const destination = text.replace(/(我要去|带我去|导航到|帮我去)/g, "").trim();
                if (window.taskChain && typeof window.taskChain.enqueue === 'function') {
                    window.taskChain.enqueue('NAV_START', { destination: destination }, 'HIGH');
                }
                break;

            case "continue":
            default:
                // 当普通对话处理
                break;
        }
    };
})();

// =============================
//  STEP EXECUTION REGISTRY
// =============================
(function() {
    'use strict';

    /**
     * Step 执行器注册中心
     * 每个 step.type 对应一个处理器函数
     */
    window.StepExecutors = {
        // ====== OCR 扫描关键词 ======
        "SCAN_OCR_FOR_KEYWORDS": async function(step, context) {
            const logData = { step, context };
            if (window.__lunaLog) {
                window.__lunaLog('step_start', logData);
            } else if (window.LunaLogger) {
                window.LunaLogger.info('step_start', logData);
            } else {
                console.log(`[StepExecutor] SCAN_OCR_FOR_KEYWORDS 开始`, logData);
            }
            
            // 获取最新的 OCR 结果（从全局变量或事件总线）
            let ocrResult = null;
            if (window.latestOCRResult) {
                ocrResult = window.latestOCRResult;
            } else if (window.vision_engine && window.vision_engine.getLatestOCR) {
                ocrResult = window.vision_engine.getLatestOCR();
            }
            
            if (!ocrResult || !ocrResult.text) {
                return { success: false, reason: "NO_OCR_DATA" };
            }

            const keywords = step.keywords || [];
            const matched = keywords.filter(k => ocrResult.text.includes(k));
            const hit = matched.length > 0;
            
            return {
                success: hit,
                matched: matched,
                ocrText: ocrResult.text.substring(0, 100) // 只返回前100字符
            };
        },

        // ====== OCR 查找目标名字 ======
        "SCAN_OCR_FOR_TARGET_NAME": async function(step, context) {
            const logData = { step, context };
            if (window.__lunaLog) {
                window.__lunaLog('step_start', logData);
            } else if (window.LunaLogger) {
                window.LunaLogger.info('step_start', logData);
            } else {
                console.log(`[StepExecutor] SCAN_OCR_FOR_TARGET_NAME 开始`, logData);
            }
            
            // 获取最新的 OCR 结果
            let ocrResult = null;
            if (window.latestOCRResult) {
                ocrResult = window.latestOCRResult;
            } else if (window.vision_engine && window.vision_engine.getLatestOCR) {
                ocrResult = window.vision_engine.getLatestOCR();
            }
            
            if (!ocrResult || !ocrResult.text) {
                return { success: false, reason: "NO_OCR_DATA" };
            }

            const text = ocrResult.text;
            const target = step.targetText || '';
            
            if (!target) {
                return { success: false, reason: "NO_TARGET_TEXT" };
            }

            // 精确匹配或模糊匹配
            let hit = false;
            if (step.fuzzy) {
                // 模糊匹配：检查目标文本是否包含在OCR文本中，或OCR文本是否包含目标文本
                hit = text.includes(target) || target.includes(text.substring(0, target.length));
            } else {
                hit = text.includes(target);
            }
            
            return {
                success: hit,
                fuzzy: step.fuzzy || false,
                targetText: target,
                matchedText: hit ? text.substring(0, 200) : null
            };
        },

        // ====== 跟随方向箭头（未来可扩展为 YOLO 箭头检测）======
        "FOLLOW_DIRECTION_SIGN": async function(step, context) {
            const logData = { step, context };
            if (window.__lunaLog) {
                window.__lunaLog('follow_sign', logData);
            } else if (window.LunaLogger) {
                window.LunaLogger.info('follow_sign', logData);
            } else {
                console.log(`[StepExecutor] FOLLOW_DIRECTION_SIGN 开始`, logData);
            }
            
            // 获取最新的 YOLO 检测结果
            let yoloResult = null;
            if (window.latestYOLOResult) {
                yoloResult = window.latestYOLOResult;
            } else if (window.vision_engine && window.vision_engine.getLatestYOLO) {
                yoloResult = window.vision_engine.getLatestYOLO();
            }
            
            if (!yoloResult || !Array.isArray(yoloResult)) {
                return { success: false, reason: "NO_DETECTION" };
            }

            // 查找箭头检测结果
            const arrow = yoloResult.find(o => 
                o.label === "arrow" || 
                o.label === "sign" || 
                (o.class && o.class.toLowerCase().includes('arrow'))
            );
            
            if (arrow) {
                // 使用 TTS 播报
                const ttsText = step.message || '请按照箭头方向前进';
                if (window.enqueueTTS) {
                    window.enqueueTTS(ttsText);
                } else if (window.MemoryAwareVoice && window.MemoryAwareVoice.handleTask) {
                    window.MemoryAwareVoice.handleTask({
                        type: 'NAV_HINT',
                        payload: { text: ttsText }
                    });
                } else if (window.SpeechRhythm && window.SpeechRhythm.handleTask) {
                    window.SpeechRhythm.handleTask({
                        type: 'NAV_HINT',
                        payload: { text: ttsText }
                    });
                } else if (window.speakText) {
                    window.speakText(ttsText);
                }
                
                return { success: true, arrowDetected: true };
            }
            
            return { success: false, reason: "NO_ARROW" };
        },

        // ====== 避障（基于 YOLO 分类）======
        "AVOID_OBSTACLES_WHILE_MOVING": async function(step, context) {
            const logData = { step, context };
            if (window.__lunaLog) {
                window.__lunaLog('avoid_obstacles', logData);
            } else if (window.LunaLogger) {
                window.LunaLogger.info('avoid_obstacles', logData);
            } else {
                console.log(`[StepExecutor] AVOID_OBSTACLES_WHILE_MOVING 开始`, logData);
            }
            
            // 获取最新的 YOLO 检测结果
            let yoloResult = null;
            if (window.latestYOLOResult) {
                yoloResult = window.latestYOLOResult;
            } else if (window.vision_engine && window.vision_engine.getLatestYOLO) {
                yoloResult = window.vision_engine.getLatestYOLO();
            }
            
            if (!yoloResult || !Array.isArray(yoloResult)) {
                return { success: true }; // 没数据，先不阻塞
            }

            // 检测危险物体（车辆、近距离障碍物）
            const danger = yoloResult.find(o => {
                const label = (o.label || '').toLowerCase();
                const isVehicle = label.includes('car') || label.includes('truck') || 
                                 label.includes('bus') || label.includes('bike');
                const isClose = typeof o.distance === 'number' && o.distance < 1.0;
                return isVehicle || isClose;
            });
            
            if (danger) {
                const ttsText = step.message || '前方有障碍物，请小心';
                if (window.enqueueTTS) {
                    window.enqueueTTS(ttsText);
                } else if (window.MemoryAwareVoice && window.MemoryAwareVoice.handleTask) {
                    window.MemoryAwareVoice.handleTask({
                        type: 'HAZARD_WARNING',
                        payload: { 
                            hazard_text: ttsText,
                            hazard: danger
                        }
                    });
                } else if (window.SpeechRhythm && window.SpeechRhythm.handleTask) {
                    window.SpeechRhythm.handleTask({
                        type: 'HAZARD_WARNING',
                        payload: { 
                            hazard_text: ttsText,
                            hazard: danger
                        }
                    });
                } else if (window.speakText) {
                    window.speakText(ttsText);
                }
            }
            
            return { success: true, dangerDetected: !!danger };
        },

        // ====== 到达确认（OCR / 距离）======
        "CONFIRM_ARRIVAL_BY_OCR": async function(step, context) {
            const logData = { step, context };
            if (window.__lunaLog) {
                window.__lunaLog('confirm_arrival', logData);
            } else if (window.LunaLogger) {
                window.LunaLogger.info('confirm_arrival', logData);
            }
            
            // 获取最新的 OCR 结果
            let ocrResult = null;
            if (window.latestOCRResult) {
                ocrResult = window.latestOCRResult;
            } else if (window.vision_engine && window.vision_engine.getLatestOCR) {
                ocrResult = window.vision_engine.getLatestOCR();
            }
            
            if (!ocrResult || !ocrResult.text) {
                return { success: false, reason: "NO_OCR_DATA" };
            }

            const text = ocrResult.text;
            const keywords = step.keywords || [];
            const matched = keywords.filter(k => text.includes(k));
            const hit = matched.length > 0;
            
            return { 
                success: hit, 
                matchedKeywords: matched,
                ocrText: text.substring(0, 100)
            };
        },

        // ====== 通用"到达播报"======
        "ANNOUNCE_ARRIVAL": async function(step, context) {
            const logData = { step, context };
            if (window.__lunaLog) {
                window.__lunaLog('announce_arrival', logData);
            } else if (window.LunaLogger) {
                window.LunaLogger.info('announce_arrival', logData);
            }
            
            const message = step.message || "已到达目标位置。";
            
            // 使用 TTS 播报
            if (window.enqueueTTS) {
                window.enqueueTTS(message);
            } else if (window.MemoryAwareVoice && window.MemoryAwareVoice.handleTask) {
                window.MemoryAwareVoice.handleTask({
                    type: 'NAV_HINT',
                    payload: { text: message }
                });
            } else if (window.SpeechRhythm && window.SpeechRhythm.handleTask) {
                window.SpeechRhythm.handleTask({
                    type: 'NAV_HINT',
                    payload: { text: message }
                });
            } else if (window.speakText) {
                window.speakText(message);
            }
            
            return { success: true };
        },

        // ====== 查找斑马线或安全过街点 ======
        "FIND_CROSSWALK_OR_SAFE_POINT": async function(step, context) {
            const logData = { step, context };
            if (window.__lunaLog) {
                window.__lunaLog('find_crosswalk', logData);
            } else if (window.LunaLogger) {
                window.LunaLogger.info('find_crosswalk', logData);
            }
            
            // 获取最新的 YOLO 检测结果
            let yoloResult = null;
            if (window.latestYOLOResult) {
                yoloResult = window.latestYOLOResult;
            } else if (window.vision_engine && window.vision_engine.getLatestYOLO) {
                yoloResult = window.vision_engine.getLatestYOLO();
            }
            
            // 查找斑马线或人行横道标识
            const crosswalk = yoloResult && Array.isArray(yoloResult) ? yoloResult.find(o => {
                const label = (o.label || '').toLowerCase();
                return label.includes('crosswalk') || label.includes('zebra') || 
                       label.includes('pedestrian') || label.includes('crossing');
            }) : null;
            
            return { 
                success: !!crosswalk, 
                crosswalkDetected: !!crosswalk 
            };
        },

        // ====== 检查交通灯或车辆 ======
        "CHECK_TRAFFIC_LIGHT_OR_VEHICLES": async function(step, context) {
            const logData = { step, context };
            if (window.__lunaLog) {
                window.__lunaLog('check_traffic', logData);
            } else if (window.LunaLogger) {
                window.LunaLogger.info('check_traffic', logData);
            }
            
            // 获取最新的 YOLO 检测结果
            let yoloResult = null;
            if (window.latestYOLOResult) {
                yoloResult = window.latestYOLOResult;
            } else if (window.vision_engine && window.vision_engine.getLatestYOLO) {
                yoloResult = window.vision_engine.getLatestYOLO();
            }
            
            if (!yoloResult || !Array.isArray(yoloResult)) {
                return { success: false, reason: "NO_DETECTION" };
            }
            
            // 查找交通灯和车辆
            const trafficLight = yoloResult.find(o => {
                const label = (o.label || '').toLowerCase();
                return label.includes('traffic') || label.includes('light') || 
                       label.includes('signal');
            });
            
            const vehicles = yoloResult.filter(o => {
                const label = (o.label || '').toLowerCase();
                return label.includes('car') || label.includes('truck') || 
                       label.includes('bus') || label.includes('motorcycle');
            });
            
            const hasVehicles = vehicles.length > 0;
            const isSafe = !hasVehicles || (trafficLight && trafficLight.state === 'green');
            
            return { 
                success: isSafe, 
                hasVehicles: hasVehicles,
                trafficLightDetected: !!trafficLight,
                vehicleCount: vehicles.length
            };
        },

        // ====== 引导用户过街 ======
        "GUIDE_USER_ACROSS": async function(step, context) {
            const logData = { step, context };
            if (window.__lunaLog) {
                window.__lunaLog('guide_across', logData);
            } else if (window.LunaLogger) {
                window.LunaLogger.info('guide_across', logData);
            }
            
            const message = step.message || "正在引导您安全穿过马路，请保持前进。";
            
            // 使用 TTS 播报
            if (window.enqueueTTS) {
                window.enqueueTTS(message);
            } else if (window.MemoryAwareVoice && window.MemoryAwareVoice.handleTask) {
                window.MemoryAwareVoice.handleTask({
                    type: 'NAV_HINT',
                    payload: { text: message }
                });
            } else if (window.speakText) {
                window.speakText(message);
            }
            
            return { success: true };
        },

        // ====== 确认完成 ======
        "CONFIRM_FINISH": async function(step, context) {
            const logData = { step, context };
            if (window.__lunaLog) {
                window.__lunaLog('confirm_finish', logData);
            } else if (window.LunaLogger) {
                window.LunaLogger.info('confirm_finish', logData);
            }
            
            const message = step.message || "任务已完成。";
            
            // 使用 TTS 播报
            if (window.enqueueTTS) {
                window.enqueueTTS(message);
            } else if (window.MemoryAwareVoice && window.MemoryAwareVoice.handleTask) {
                window.MemoryAwareVoice.handleTask({
                    type: 'NAV_HINT',
                    payload: { text: message }
                });
            } else if (window.speakText) {
                window.speakText(message);
            }
            
            return { success: true };
        },

        // ====== 移动到目标 ======
        "MOVE_TOWARDS_TARGET": async function(step, context) {
            const logData = { step, context };
            if (window.__lunaLog) {
                window.__lunaLog('move_towards_target', logData);
            } else if (window.LunaLogger) {
                window.LunaLogger.info('move_towards_target', logData);
            }
            
            // 这个步骤主要是持续监控，不阻塞
            // 实际的导航逻辑由其他模块处理
            return { success: true };
        },

        // ====== 通过距离或OCR确认到达 ======
        "CONFIRM_ARRIVAL_BY_DISTANCE_OR_OCR": async function(step, context) {
            const logData = { step, context };
            if (window.__lunaLog) {
                window.__lunaLog('confirm_arrival_distance', logData);
            } else if (window.LunaLogger) {
                window.LunaLogger.info('confirm_arrival_distance', logData);
            }
            
            // 检查距离（如果有导航状态）
            let distanceOk = false;
            if (window.NavigationFSM && window.NavigationFSM.currentRoute) {
                // 可以从导航状态获取距离信息
                distanceOk = true; // 简化处理
            }
            
            // 检查OCR
            let ocrOk = false;
            let ocrResult = null;
            if (window.latestOCRResult) {
                ocrResult = window.latestOCRResult;
            } else if (window.vision_engine && window.vision_engine.getLatestOCR) {
                ocrResult = window.vision_engine.getLatestOCR();
            }
            
            if (ocrResult && ocrResult.text) {
                const target = step.targetText || context?.taskPlan?.intent?.target_name || '';
                if (target) {
                    ocrOk = ocrResult.text.includes(target);
                }
            }
            
            return { 
                success: distanceOk || ocrOk, 
                distanceOk: distanceOk,
                ocrOk: ocrOk
            };
        }
    };

    console.log('✅ StepExecutors 注册中心初始化完成', { 
        module: 'task_chain', 
        executorCount: Object.keys(window.StepExecutors).length 
    });
})();

// =============================
// TASK CHAIN EXECUTION ENGINE
// =============================
(function() {
    'use strict';

    /**
     * 任务链执行引擎
     * 负责按顺序执行 taskPlan 中的 steps
     */
    window.TaskChainExecutor = {
        /**
         * 执行任务计划
         * @param {Object} taskPlan - 任务计划对象，包含 steps 数组
         */
        async runTask(taskPlan) {
            if (!taskPlan || !Array.isArray(taskPlan.steps)) {
                console.error(`❌ [TaskChainExecutor] 无效的任务计划`, { module: 'task_chain' });
                return;
            }

            const taskId = taskPlan.taskId || `plan_${Date.now()}`;
            
            // 记录任务开始
            if (window.__lunaLog) {
                window.__lunaLog('task_start', { taskPlan });
            } else if (window.LunaLogger) {
                window.LunaLogger.info('task_start', { taskPlan });
            } else {
                console.log(`🚀 [TaskChainExecutor] 开始执行任务计划: ${taskId}`, { 
                    module: 'task_chain',
                    steps: taskPlan.steps.length 
                });
            }

            const context = { taskPlan };
            let stepIndex = 0;

            // 按顺序执行每个 step
            for (const step of taskPlan.steps) {
                stepIndex++;
                const stepType = step.type || 'UNKNOWN';
                
                console.log(`▶️ [TaskChainExecutor] 执行步骤 ${stepIndex}/${taskPlan.steps.length}: ${stepType}`, { 
                    module: 'task_chain',
                    step,
                    taskId
                });

                // 获取 step 处理器
                const handler = window.StepExecutors[stepType];
                
                if (!handler) {
                    const errorMsg = `未找到 step 处理器: ${stepType}`;
                    console.warn(`⚠️ [TaskChainExecutor] ${errorMsg}`, { 
                        module: 'task_chain',
                        step,
                        taskId
                    });
                    
                    // 记录错误
                    if (window.__lunaLog) {
                        window.__lunaLog('task_error', {
                            step,
                            error: "NO_HANDLER",
                            stepIndex,
                            taskId
                        });
                    } else if (window.LunaLogger) {
                        window.LunaLogger.warn('task_error', {
                            step,
                            error: "NO_HANDLER",
                            stepIndex,
                            taskId
                        });
                    }
                    
                    // 继续执行下一个步骤（不中断任务）
                    continue;
                }

                let result = null;
                try {
                    // 执行 step
                    result = await handler(step, context);
                    
                    // 记录步骤结果
                    if (window.__lunaLog) {
                        window.__lunaLog('step_result', {
                            step,
                            result,
                            stepIndex,
                            taskId
                        });
                    } else if (window.LunaLogger) {
                        window.LunaLogger.info('step_result', {
                            step,
                            result,
                            stepIndex,
                            taskId
                        });
                    } else {
                        console.log(`✅ [TaskChainExecutor] 步骤完成: ${stepType}`, { 
                            module: 'task_chain',
                            result,
                            stepIndex,
                            taskId
                        });
                    }

                    // 检查步骤是否成功
                    if (result && result.success === false) {
                        const reason = result.reason || 'UNKNOWN';
                        console.warn(`⚠️ [TaskChainExecutor] 步骤失败: ${stepType} (原因: ${reason})`, { 
                            module: 'task_chain',
                            step,
                            result,
                            stepIndex,
                            taskId
                        });
                        
                        // 记录失败
                        if (window.__lunaLog) {
                            window.__lunaLog('step_failed', { 
                                step, 
                                result,
                                stepIndex,
                                taskId
                            });
                        } else if (window.LunaLogger) {
                            window.LunaLogger.warn('step_failed', { 
                                step, 
                                result,
                                stepIndex,
                                taskId
                            });
                        }

                        // 检查是否有 timeoutSec，如果有则等待一段时间后继续
                        if (step.timeoutSec && stepIndex < taskPlan.steps.length) {
                            console.log(`⏳ [TaskChainExecutor] 等待 ${step.timeoutSec} 秒后继续...`, { 
                                module: 'task_chain',
                                stepIndex,
                                taskId
                            });
                            await new Promise(resolve => setTimeout(resolve, step.timeoutSec * 1000));
                        }
                        
                        // 暂时不中断任务，继续执行下一步（可配置）
                        // 未来可以扩展成"询问用户是否继续"
                    }

                } catch (e) {
                    const errorMsg = e.toString();
                    console.error(`❌ [TaskChainExecutor] 步骤执行异常: ${stepType}`, { 
                        module: 'task_chain',
                        error: errorMsg,
                        stack: e.stack,
                        step,
                        stepIndex,
                        taskId
                    });
                    
                    // 记录异常
                    if (window.__lunaLog) {
                        window.__lunaLog('step_exception', {
                            step,
                            error: errorMsg,
                            stack: e.stack,
                            stepIndex,
                            taskId
                        });
                    } else if (window.LunaLogger) {
                        window.LunaLogger.error('step_exception', {
                            step,
                            error: errorMsg,
                            stack: e.stack,
                            stepIndex,
                            taskId
                        });
                    }
                    
                    // 继续执行下一个步骤（不中断任务）
                }

                // 步骤之间的延迟（可选）
                if (stepIndex < taskPlan.steps.length) {
                    await new Promise(resolve => setTimeout(resolve, 100)); // 100ms 延迟
                }
            }

            // 记录任务完成
            if (window.__lunaLog) {
                window.__lunaLog('task_complete', {
                    taskId,
                    stepCount: taskPlan.steps.length
                });
            } else if (window.LunaLogger) {
                window.LunaLogger.info('task_complete', {
                    taskId,
                    stepCount: taskPlan.steps.length
                });
            } else {
                console.log(`🏁 [TaskChainExecutor] 任务计划执行完成: ${taskId}`, { 
                    module: 'task_chain',
                    stepCount: taskPlan.steps.length
                });
            }
        }
    };

    console.log('✅ TaskChainExecutor 执行引擎初始化完成', { module: 'task_chain' });
})();



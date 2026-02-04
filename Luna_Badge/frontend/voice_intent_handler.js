// frontend/voice_intent_handler.js
// 语音意图处理和任务链集成模块

(function () {
    if (window.VoiceIntentHandler) return;

    function logInfo(msg, details) {
        if (window.logInfo) window.logInfo('[VoiceIntentHandler] ' + msg, details || {});
        else console.log('[VoiceIntentHandler]', msg, details || {});
    }

    function logError(msg, details) {
        if (window.logError) window.logError('[VoiceIntentHandler] ' + msg, details || {});
        else console.error('[VoiceIntentHandler]', msg, details || {});
    }

    /**
     * 处理用户语音命令
     * @param {string} finalText - ASR 识别出的最终文本
     */
    async function handleUserVoiceCommand(finalText) {
        if (!finalText || !finalText.trim()) {
            logError('handleUserVoiceCommand: 空文本');
            return;
        }

        try {
            logInfo('处理语音命令', { text: finalText });

            const res = await fetch('/api/voice_intent', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: finalText })
            });

            if (!res.ok) {
                throw new Error(`HTTP ${res.status}`);
            }

            const data = await res.json();

            if (data.status !== 'ok' || !data.task_plan) {
                const message = data.message || '暂时没听懂你的任务';
                logInfo('意图未识别', { text: finalText, message });
                
                // 显示提示（如果有 UI 组件）
                if (window.showToast && typeof window.showToast === 'function') {
                    window.showToast(message);
                } else if (window.speakText && typeof window.speakText === 'function') {
                    window.speakText(message);
                }
                return;
            }

            logInfo('意图识别成功', {
                intent: data.intent,
                task_plan_type: data.task_plan.type
            });

            // 将任务计划丢给任务链系统
            if (window.taskChain && typeof window.taskChain.enqueue === 'function') {
                window.taskChain.enqueue(data.task_plan);
                logInfo('任务已加入任务链', { taskId: data.task_plan.taskId });
            } else {
                logError('taskChain.enqueue 不存在，无法执行任务', { task_plan: data.task_plan });
            }

        } catch (e) {
            logError('handleUserVoiceCommand error', { error: e.toString(), stack: e.stack });
        }
    }

    /**
     * ASR 最终结果处理函数
     * @param {string} text - ASR 识别出的文本
     */
    function onASRFinalResult(text) {
        if (!text || !text.trim()) {
            return;
        }

        // 先把原始识别文本展示出来（如果有聊天界面）
        if (window.appendChatBubble && typeof window.appendChatBubble === 'function') {
            window.appendChatBubble('user', text);
        }

        // 然后交给任务解析接口
        handleUserVoiceCommand(text);
    }

    // 导出到全局
    window.VoiceIntentHandler = {
        handleUserVoiceCommand: handleUserVoiceCommand,
        onASRFinalResult: onASRFinalResult
    };

    // 兼容性：如果已有 ASR 回调，自动绑定
    if (typeof window.onASRResult === 'undefined') {
        window.onASRResult = onASRFinalResult;
    }

    logInfo('VoiceIntentHandler 模块已初始化', {});
})();


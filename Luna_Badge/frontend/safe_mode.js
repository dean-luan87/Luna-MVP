/**
 * Safe Mode（安全模式）系统（规范要求）
 * 提供安全模式，暂停核心功能但保留基础能力
 */

(function() {
    'use strict';

    window.SafeMode = {
        enabled: false,
        reason: null,
        originalStates: {},  // 保存原始状态
        
        /**
         * 启用安全模式
         */
        enable(reason = "用户手动启用") {
            if (this.enabled) {
                console.log('⚠️ [SafeMode] 安全模式已启用', { module: 'safe_mode' });
                return;
            }
            
            this.enabled = true;
            this.reason = reason;
            
            console.log(`🛡️ [SafeMode] 启用安全模式: ${reason}`, { module: 'safe_mode' });
            
            // 保存原始状态
            this.originalStates = {
                visionActive: window.productModeActive || false,
                navigationActive: window.navigationActive || false,
                taskChainActive: window.taskChain ? window.taskChain.running : false
            };
            
            // 暂停视觉分析
            if (window.productModeActive !== undefined) {
                window.productModeActive = false;
            }
            
            // 暂停导航决策
            if (window.navigationActive !== undefined) {
                window.navigationActive = false;
            }
            
            // 暂停任务链执行（通过标志）
            if (window.taskChain) {
                window.taskChain.running = false;
            }
            
            // 显示安全模式状态条
            this._showStatusBar();
            
            // 播报提示
            if (window.speakText) {
                window.speakText(`系统已进入安全模式：${reason}`, 'calm', false);
            }
            
            // 触发情绪事件
            if (window.emotion_event) {
                window.emotion_event('safe_mode_enabled', 'medium', { reason });
            }
        },
        
        /**
         * 禁用安全模式
         */
        disable() {
            if (!this.enabled) {
                console.log('ℹ️ [SafeMode] 安全模式未启用', { module: 'safe_mode' });
                return;
            }
            
            console.log('✅ [SafeMode] 禁用安全模式', { module: 'safe_mode' });
            
            this.enabled = false;
            const reason = this.reason;
            this.reason = null;
            
            // 恢复原始状态
            if (this.originalStates.visionActive !== undefined) {
                window.productModeActive = this.originalStates.visionActive;
            }
            
            if (this.originalStates.navigationActive !== undefined) {
                window.navigationActive = this.originalStates.navigationActive;
            }
            
            if (window.taskChain && this.originalStates.taskChainActive) {
                window.taskChain.running = true;
                // 重新处理队列
                if (window.taskChain.queue && window.taskChain.queue.length > 0) {
                    window.taskChain._processQueue();
                }
            }
            
            // 隐藏状态条
            this._hideStatusBar();
            
            // 播报提示
            if (window.speakText) {
                window.speakText('安全模式已关闭，系统恢复正常运行', 'cheerful', false);
            }
            
            // 触发情绪事件
            if (window.emotion_event) {
                window.emotion_event('safe_mode_disabled', 'medium', { previous_reason: reason });
            }
        },
        
        /**
         * 检查是否启用
         */
        isEnabled() {
            return this.enabled;
        },
        
        /**
         * 显示安全模式状态条
         */
        _showStatusBar() {
            // 移除旧的状态条（如果存在）
            const existingBar = document.getElementById('safeModeStatusBar');
            if (existingBar) {
                existingBar.remove();
            }
            
            // 创建状态条
            const statusBar = document.createElement('div');
            statusBar.id = 'safeModeStatusBar';
            statusBar.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: #ff9800;
                color: white;
                padding: 10px;
                text-align: center;
                font-weight: bold;
                z-index: 10000;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            `;
            statusBar.textContent = `🛡️ SAFE MODE ACTIVE: ${this.reason}`;
            
            document.body.insertBefore(statusBar, document.body.firstChild);
        },
        
        /**
         * 隐藏安全模式状态条
         */
        _hideStatusBar() {
            const statusBar = document.getElementById('safeModeStatusBar');
            if (statusBar) {
                statusBar.remove();
            }
        },
        
        /**
         * 检查是否应该处理事件（在事件处理函数中调用）
         */
        shouldProcess() {
            return !this.enabled;
        },

        /**
         * 强制硬重启（模拟浏览器刷新）
         */
        forceHardRestart() {
            const LogUploader = window.LogUploader || { push: console.log };
            const ErrorCode = window.ErrorCode || {};
            
            LogUploader.push({
                level: "critical",
                code: ErrorCode.SYS_FORCE_RECOVER || "E_SYS_FORCE_RECOVER",
                message: "Hard restart triggered from SafeMode",
                source: "SafeMode",
                timestamp: Date.now(),
            });

            // 尝试同步上传日志
            if (LogUploader.flushSync && typeof LogUploader.flushSync === 'function') {
                LogUploader.flushSync().catch(() => {
                    // 即使上传失败也继续重启
                });
            }

            console.error("🔄 [SafeMode] 强制硬重启触发，页面即将刷新...");
            
            // 延迟一小段时间确保日志上传
            setTimeout(() => {
                location.reload(); // 浏览器模拟硬重启
            }, 500);
        }
    };
    
    console.log('✅ SafeMode模块加载完成', { module: 'safe_mode' });
})();



/**
 * Recovery Mode（恢复模式）系统（规范要求）
 * 提供系统恢复和重置功能
 */

(function() {
    'use strict';

    window.RecoveryMode = {
        /**
         * 强制硬重启（模拟浏览器刷新）
         */
        forceHardRestart() {
            const LogUploader = window.LogUploader || { push: console.log };
            const ErrorCode = window.ErrorCode || {};
            
            LogUploader.push({
                level: "critical",
                code: ErrorCode.SYS_FORCE_RECOVER || "E_SYS_FORCE_RECOVER",
                message: "Hard restart triggered",
                source: "RecoveryMode",
                timestamp: Date.now(),
            });

            // 尝试同步上传日志
            if (LogUploader.flushSync && typeof LogUploader.flushSync === 'function') {
                LogUploader.flushSync().catch(() => {
                    // 即使上传失败也继续重启
                });
            }

            console.error("🔄 [RecoveryMode] 强制硬重启触发，页面即将刷新...");
            
            // 延迟一小段时间确保日志上传
            setTimeout(() => {
                location.reload(); // 浏览器模拟硬重启
            }, 500);
        },

        /**
         * 重置所有状态
         */
        resetAll() {
            console.log('🔄 [RecoveryMode] 开始重置所有状态...', { module: 'recovery_mode' });
            
            // 1. 清理所有定时器
            if (window.__intervals) {
                let clearedCount = 0;
                for (const key in window.__intervals) {
                    if (window.__intervals.hasOwnProperty(key)) {
                        clearInterval(window.__intervals[key]);
                        clearedCount++;
                    }
                }
                window.__intervals = {};
                console.log(`  ✅ 已清理 ${clearedCount} 个定时器`, { module: 'recovery_mode' });
            }
            
            // 2. 清空TTS队列
            if (window.priorityTTSQueue) {
                window.priorityTTSQueue.queue = [];
                window.priorityTTSQueue.currentAudio = null;
                window.priorityTTSQueue.currentPriority = 999;
                console.log('  ✅ 已清空TTS队列', { module: 'recovery_mode' });
            }
            
            if (window.ttsQueue && Array.isArray(window.ttsQueue)) {
                window.ttsQueue.length = 0;
                console.log('  ✅ 已清空旧TTS队列', { module: 'recovery_mode' });
            }
            
            // 3. 清空任务链队列
            if (window.taskChain) {
                window.taskChain.clear();
                console.log('  ✅ 已清空任务链队列', { module: 'recovery_mode' });
            }
            
            // 4. 清空视觉/导航相关的临时状态
            if (window.lastSpokenGuidance) {
                window.lastSpokenGuidance = {};
            }
            
            if (window.cameraMotionState) {
                window.cameraMotionState.lastFrame = null;
                window.cameraMotionState.motionDetected = false;
                window.cameraMotionState.lastMotionTime = 0;
            }
            
            // 5. 停止所有正在播放的声音
            if (window.priorityTTSQueue && window.priorityTTSQueue.currentAudio) {
                try {
                    window.priorityTTSQueue.currentAudio.pause();
                    window.priorityTTSQueue.currentAudio.currentTime = 0;
                    window.priorityTTSQueue.currentAudio = null;
                } catch (e) {
                    console.warn('  ⚠️ 停止音频失败:', e);
                }
            }
            
            // 6. 重置导航状态（如果存在）
            if (window.getNavStateManager) {
                try {
                    const navManager = window.getNavStateManager();
                    if (navManager && navManager.cancel) {
                        navManager.cancel('系统重置');
                    }
                } catch (e) {
                    console.warn('  ⚠️ 重置导航状态失败:', e);
                }
            }
            
            // 7. 重置导航FSM（如果存在）
            if (window.NavigationFSM && window.NavigationFSM.reset) {
                window.NavigationFSM.reset();
                console.log('  ✅ 已重置导航状态机', { module: 'recovery_mode' });
            }
            
            // 8. 清空路点（如果存在）
            if (window.WaypointManager && window.WaypointManager.clearWaypoints) {
                window.WaypointManager.clearWaypoints();
                console.log('  ✅ 已清空路点', { module: 'recovery_mode' });
            }
            
            console.log('✅ [RecoveryMode] 重置完成', { module: 'recovery_mode' });
            
            // 触发情绪事件
            if (window.emotion_event) {
                window.emotion_event('system_reset', 'medium', {});
            }
        },
        
        /**
         * 重启核心模块
         */
        restartCore() {
            console.log('🔄 [RecoveryMode] 开始重启核心模块...', { module: 'recovery_mode' });
            
            // 1. 先重置所有状态
            this.resetAll();
            
            // 2. 重新初始化（按顺序）
            try {
                // 2.1 重新初始化任务链（如果存在）
                if (window.taskChain) {
                    // 任务链会自动初始化，这里只需要确保运行标志正确
                    window.taskChain.running = false;
                    console.log('  ✅ 任务链已准备就绪', { module: 'recovery_mode' });
                }
                
                // 2.2 重新初始化视觉模块（如果有初始化函数）
                if (typeof window.initProductMode === 'function') {
                    // 不直接调用，避免重复初始化
                    console.log('  ℹ️ 视觉模块初始化函数存在，但跳过自动调用', { module: 'recovery_mode' });
                }
                
                // 2.3 恢复UI按钮状态
                const startBtn = document.getElementById('startProductModeBtn');
                const stopBtn = document.getElementById('stopProductModeBtn');
                if (startBtn) {
                    startBtn.disabled = false;
                }
                if (stopBtn) {
                    stopBtn.disabled = true;
                }
                
                // 2.4 重置产品模式状态
                if (window.productModeActive !== undefined) {
                    window.productModeActive = false;
                }
                
                console.log('✅ [RecoveryMode] 核心模块重启完成', { module: 'recovery_mode' });
                
                // 3. 播报恢复消息
                if (window.speakText) {
                    setTimeout(() => {
                        window.speakText('系统已恢复，可以重新开始使用', 'cheerful', false);
                    }, 500);
                }
                
                // 触发情绪事件
                if (window.emotion_event) {
                    window.emotion_event('system_recovered', 'medium', {});
                }
                
            } catch (error) {
                console.error('❌ [RecoveryMode] 重启失败:', error, { module: 'recovery_mode' });
                
                // 即使失败也播报消息
                if (window.speakText) {
                    window.speakText('系统恢复过程中遇到问题，请手动重启', 'urgent', true);
                }
            }
        },
        
        /**
         * 软重启（只重置关键状态，不重启整个系统）
         */
        softReset() {
            console.log('🔄 [RecoveryMode] 执行软重置...', { module: 'recovery_mode' });
            
            // 只清理队列和定时器，不重启模块
            if (window.__intervals) {
                for (const key in window.__intervals) {
                    if (window.__intervals.hasOwnProperty(key)) {
                        clearInterval(window.__intervals[key]);
                    }
                }
                window.__intervals = {};
            }
            
            if (window.taskChain) {
                window.taskChain.clear();
            }
            
            if (window.priorityTTSQueue) {
                window.priorityTTSQueue.queue = [];
            }
            
            console.log('✅ [RecoveryMode] 软重置完成', { module: 'recovery_mode' });
        }
    };
    
    console.log('✅ RecoveryMode模块加载完成', { module: 'recovery_mode' });
})();



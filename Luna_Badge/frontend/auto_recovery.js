/**
 * Auto-Recovery（自动恢复）模块（规范要求）
 * 监控核心模块是否异常，并调用RecoveryMode自愈
 */

(function() {
    'use strict';

    window.AutoRecovery = {
        stats: {
            visionErrors: 0,
            navErrors: 0,
            ttsBlockedCount: 0,
            taskChainStallCount: 0,
            lastCheckTime: Date.now()
        },
        
        thresholds: {
            visionErrors: 3,      // 视觉错误超过3次触发恢复
            navErrors: 3,         // 导航错误超过3次触发恢复
            ttsBlocked: 5,        // TTS阻塞超过5次触发恢复
            taskChainStall: 10,   // 任务链停滞超过10次触发恢复
            checkInterval: 5000   // 每5秒检查一次
        },
        
        errorHistory: [],
        maxHistory: 20,
        
        /**
         * 记录错误
         */
        record(module, type, detail = {}) {
            const record = {
                module,
                type,
                detail,
                timestamp: Date.now()
            };
            
            this.errorHistory.push(record);
            if (this.errorHistory.length > this.maxHistory) {
                this.errorHistory.shift();
            }
            
            // 更新统计
            if (module === 'vision' && type === 'error') {
                this.stats.visionErrors++;
            } else if (module === 'navigation' && type === 'error') {
                this.stats.navErrors++;
            } else if (module === 'tts' && type === 'blocked') {
                this.stats.ttsBlockedCount++;
            } else if (module === 'taskChain' && type === 'stall') {
                this.stats.taskChainStallCount++;
            }
            
            console.log(`📊 [AutoRecovery] 记录错误: ${module}.${type}`, { module: 'auto_recovery', detail });
            
            // 如果超过阈值，立即检查
            if (this._shouldTriggerRecovery(module, type)) {
                console.warn(`⚠️ [AutoRecovery] ${module}错误超过阈值，触发检查`, { module: 'auto_recovery' });
                this.checkAndRecover();
            }
        },
        
        /**
         * 检查并恢复
         */
        checkAndRecover() {
            const now = Date.now();
            const timeSinceLastCheck = now - this.stats.lastCheckTime;
            this.stats.lastCheckTime = now;
            
            console.log('🔍 [AutoRecovery] 执行健康检查...', { module: 'auto_recovery' });
            
            let recoveryNeeded = false;
            const recoveryReasons = [];
            
            // 1. 检查视觉模块
            if (this.stats.visionErrors >= this.thresholds.visionErrors) {
                recoveryNeeded = true;
                recoveryReasons.push(`视觉错误过多 (${this.stats.visionErrors}次)`);
            }
            
            // 2. 检查导航模块
            if (this.stats.navErrors >= this.thresholds.navErrors) {
                recoveryNeeded = true;
                recoveryReasons.push(`导航错误过多 (${this.stats.navErrors}次)`);
            }
            
            // 3. 检查TTS队列
            if (this.stats.ttsBlockedCount >= this.thresholds.ttsBlocked) {
                recoveryNeeded = true;
                recoveryReasons.push(`TTS队列阻塞 (${this.stats.ttsBlockedCount}次)`);
            }
            
            // 4. 检查任务链
            if (this.stats.taskChainStallCount >= this.thresholds.taskChainStall) {
                recoveryNeeded = true;
                recoveryReasons.push(`任务链停滞 (${this.stats.taskChainStallCount}次)`);
            }
            
            // 5. 检查任务链是否真的停滞
            if (window.taskChain) {
                const stats = window.taskChain.getStats();
                const currentTask = stats.currentTask;
                
                // 如果当前任务运行时间过长（超过30秒）
                if (currentTask && currentTask.status === 'running') {
                    const taskAge = now - (currentTask.timestamp || 0);
                    if (taskAge > 30000) {
                        recoveryNeeded = true;
                        recoveryReasons.push(`任务链任务运行超时 (${Math.round(taskAge/1000)}秒)`);
                    }
                }
            }
            
            // 6. 检查TTS队列是否长时间未处理（兼容大小写两种命名）
            const ttsQueue =
              (window.PriorityTTSQueue && window.PriorityTTSQueue.queue)
                ? window.PriorityTTSQueue
                : (window.priorityTTSQueue || null);

            if (ttsQueue) {
              const queueLength = Array.isArray(ttsQueue.queue) ? ttsQueue.queue.length : 0;
              if (queueLength > 10) {
                recoveryNeeded = true;
                recoveryReasons.push(`TTS队列积压过多 (${queueLength}条)`);
              }
            }
            
            if (recoveryNeeded) {
                console.warn(`⚠️ [AutoRecovery] 检测到异常，开始恢复...`, { 
                    module: 'auto_recovery',
                    reasons: recoveryReasons
                });
                
                // 记录日志
                if (window.lunaLog) {
                    window.lunaLog('warning', '自动恢复触发', {
                        reasons: recoveryReasons,
                        stats: { ...this.stats }
                    });
                }
                
                // 触发情绪事件
                if (window.emotion_event) {
                    window.emotion_event('system_error', 'high', {
                        type: 'auto_recovery_triggered',
                        reasons: recoveryReasons,
                        stats: { ...this.stats }
                    });
                }
                
                // 执行恢复
                if (window.RecoveryMode) {
                    // 根据严重程度选择恢复方式
                    const isCritical = recoveryReasons.some(r => r.includes('超时') || r.includes('积压'));
                    
                    if (isCritical) {
                        console.log('  🔄 [AutoRecovery] 执行完整重启...', { module: 'auto_recovery' });
                        window.RecoveryMode.restartCore();
                    } else {
                        console.log('  🔄 [AutoRecovery] 执行软重置...', { module: 'auto_recovery' });
                        window.RecoveryMode.softReset();
                    }
                } else {
                    console.warn('  ⚠️ [AutoRecovery] RecoveryMode未加载，无法执行恢复', { module: 'auto_recovery' });
                }
                
                // 重置错误计数（避免重复触发）
                this.stats.visionErrors = 0;
                this.stats.navErrors = 0;
                this.stats.ttsBlockedCount = 0;
                this.stats.taskChainStallCount = 0;
                
                console.log('✅ [AutoRecovery] 恢复完成', { module: 'auto_recovery' });
            } else {
                console.log('✅ [AutoRecovery] 系统健康，无需恢复', { module: 'auto_recovery' });
            }
        },
        
        /**
         * 判断是否应该触发恢复
         */
        _shouldTriggerRecovery(module, type) {
            if (module === 'vision' && type === 'error') {
                return this.stats.visionErrors >= this.thresholds.visionErrors;
            }
            if (module === 'navigation' && type === 'error') {
                return this.stats.navErrors >= this.thresholds.navErrors;
            }
            if (module === 'tts' && type === 'blocked') {
                return this.stats.ttsBlockedCount >= this.thresholds.ttsBlocked;
            }
            if (module === 'taskChain' && type === 'stall') {
                return this.stats.taskChainStallCount >= this.thresholds.taskChainStall;
            }
            return false;
        },
        
        /**
         * 启动自动监控
         */
        startMonitoring() {
            if (this.monitoringInterval) {
                console.log('ℹ️ [AutoRecovery] 监控已在运行', { module: 'auto_recovery' });
                return;
            }
            
            console.log('✅ [AutoRecovery] 启动自动监控', { module: 'auto_recovery' });
            
            // 注册到全局定时器管理
            if (window.__intervals) {
                window.__intervals.autoRecovery = setInterval(() => {
                    this.checkAndRecover();
                }, this.thresholds.checkInterval);
            } else {
                // 降级：直接使用setInterval
                this.monitoringInterval = setInterval(() => {
                    this.checkAndRecover();
                }, this.thresholds.checkInterval);
            }
        },
        
        /**
         * 停止自动监控
         */
        stopMonitoring() {
            if (window.__intervals && window.__intervals.autoRecovery) {
                clearInterval(window.__intervals.autoRecovery);
                delete window.__intervals.autoRecovery;
            }
            
            if (this.monitoringInterval) {
                clearInterval(this.monitoringInterval);
                this.monitoringInterval = null;
            }
            
            console.log('⏸️ [AutoRecovery] 停止自动监控', { module: 'auto_recovery' });
        },
        
        /**
         * 获取统计信息
         */
        getStats() {
            return {
                ...this.stats,
                errorHistory: this.errorHistory.slice(-10),  // 最近10条错误
                thresholds: this.thresholds
            };
        },
        
        /**
         * 重置统计
         */
        resetStats() {
            this.stats = {
                visionErrors: 0,
                navErrors: 0,
                ttsBlockedCount: 0,
                taskChainStallCount: 0,
                lastCheckTime: Date.now()
            };
            this.errorHistory = [];
            console.log('🔄 [AutoRecovery] 统计已重置', { module: 'auto_recovery' });
        }
    };
    
    // 自动启动监控（延迟启动，确保其他模块已加载）
    setTimeout(() => {
        if (window.AutoRecovery && window.AutoRecovery.startMonitoring) {
            window.AutoRecovery.startMonitoring();
        }
    }, 2000);
    
    console.log('✅ AutoRecovery模块加载完成', { module: 'auto_recovery' });
})();



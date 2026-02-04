/**
 * 统一事件派发系统（规范要求）
 * 提供统一的危险/台阶/导航事件处理流程
 * 统一：文案生成 → TTS队列 → UI更新 → 日志记录
 */

(function() {
    'use strict';

    /**
     * 统一事件管理器
     */
    class UnifiedEventManager {
        constructor() {
            this.messageTemplates = {
                hazard: {
                    water: '前方有积水，请小心',
                    obstacle: '前方有障碍物，请绕行',
                    slippery: '地面湿滑，请减速',
                    construction: '前方施工，请注意安全',
                    default: '检测到危险区域，请小心'
                },
                step: {
                    up: (distance) => `前方${distance || ''}米有台阶，请减速`,
                    down: (distance) => `前方${distance || ''}米有下台阶，请小心`,
                    default: (distance) => `前方${distance || ''}米有台阶，请注意`
                },
                navigation: {
                    turn_left: (distance) => `前方${distance || ''}米左转`,
                    turn_right: (distance) => `前方${distance || ''}米右转`,
                    straight: (distance) => `请直行${distance ? distance + '米' : ''}`,
                    stop: () => '已到达目的地',
                    default: () => '请跟随导航指引'
                }
            };

            this.eventHistory = [];
            this.maxHistory = 100;

            console.log('✅ UnifiedEventManager初始化完成', { module: 'unified_events' });
        }

        /**
         * 生成消息文案
         */
        _generateMessage(type, subtype, meta = {}) {
            const templates = this.messageTemplates[type];
            if (!templates) {
                return meta.message || '提示信息';
            }

            const template = templates[subtype] || templates.default;
            if (typeof template === 'function') {
                return template(meta.distance, meta);
            }
            return template;
        }

        /**
         * 记录事件历史
         */
        _recordEvent(event) {
            this.eventHistory.push({
                ...event,
                timestamp: Date.now()
            });
            if (this.eventHistory.length > this.maxHistory) {
                this.eventHistory.shift();
            }
        }
    }

    /**
     * 危险事件派发
     */
    window.emitHazardEvent = function({ type, level = 'medium', meta = {} }) {
        const manager = new UnifiedEventManager();
        const message = manager._generateMessage('hazard', type, meta);
        
        console.log(`🚨 [统一事件] 危险事件: ${type}, 级别: ${level}`, { module: 'unified_events', meta });

        // 1. 生成文案
        const finalMessage = meta.message || message;

        // 2. 入TTS队列（通过taskChain）
        if (window.taskChain) {
            window.taskChain.enqueue('hazard_warning', {
                type,
                level,
                meta: { ...meta, message: finalMessage }
            }, level === 'critical' || level === 'high' ? 0 : 2);
        } else if (window.speakText) {
            // 降级：直接调用TTS
            window.speakText(finalMessage, 'urgent', level === 'critical' || level === 'high');
        }

        // 3. 更新UI
        const uiElement = document.getElementById('hazardAlert');
        if (uiElement) {
            uiElement.textContent = finalMessage;
            uiElement.className = `hazard-alert level-${level}`;
            uiElement.style.display = 'block';
            
            // 3秒后自动隐藏
            setTimeout(() => {
                uiElement.style.display = 'none';
            }, 3000);
        }

        // 4. 记录日志
        if (window.taskChain) {
            window.taskChain.enqueue('log_record', {
                level: 'warning',
                message: `危险事件: ${type}`,
                meta: { level, ...meta }
            }, 3);
        }

        // 5. 触发情绪事件（如果存在）
        if (window.emotion_event) {
            window.emotion_event('hazard_detected', level, { type, ...meta });
        }

        // 6. 记录事件历史
        manager._recordEvent({
            type: 'hazard',
            subtype: type,
            level,
            message: finalMessage,
            meta
        });

        return {
            success: true,
            message: finalMessage,
            type,
            level
        };
    };

    /**
     * 台阶事件派发
     */
    window.emitStepEvent = function({ direction = 'up', distance, meta = {} }) {
        const manager = new UnifiedEventManager();
        const message = manager._generateMessage('step', direction, { distance, ...meta });
        
        console.log(`📐 [统一事件] 台阶事件: ${direction}, 距离: ${distance}`, { module: 'unified_events', meta });

        // 1. 生成文案
        const finalMessage = meta.message || message;

        // 2. 入TTS队列（通过taskChain）
        if (window.taskChain) {
            window.taskChain.enqueue('step_warning', {
                direction,
                distance,
                meta: { ...meta, message: finalMessage }
            }, 0); // 台阶警告是critical优先级
        } else if (window.speakText) {
            window.speakText(finalMessage, 'urgent', true);
        }

        // 3. 更新UI
        const uiElement = document.getElementById('stepAlert');
        if (uiElement) {
            uiElement.textContent = finalMessage;
            uiElement.className = 'step-alert critical';
            uiElement.style.display = 'block';
            
            setTimeout(() => {
                uiElement.style.display = 'none';
            }, 3000);
        }

        // 4. 记录日志
        if (window.taskChain) {
            window.taskChain.enqueue('log_record', {
                level: 'info',
                message: `台阶事件: ${direction}`,
                meta: { distance, ...meta }
            }, 3);
        }

        // 5. 触发情绪事件
        if (window.emotion_event) {
            window.emotion_event('step_detected', 'high', { direction, distance, ...meta });
        }

        // 6. 记录事件历史
        manager._recordEvent({
            type: 'step',
            direction,
            distance,
            message: finalMessage,
            meta
        });

        return {
            success: true,
            message: finalMessage,
            direction,
            distance
        };
    };

    /**
     * 导航事件派发
     */
    window.emitNavigationEvent = function({ action, direction, distance, meta = {} }) {
        const manager = new UnifiedEventManager();
        const subtype = action === 'turn' ? `turn_${direction}` : action;
        const message = manager._generateMessage('navigation', subtype, { distance, ...meta });
        
        console.log(`🧭 [统一事件] 导航事件: ${action}, 方向: ${direction}`, { module: 'unified_events', meta });

        // 1. 生成文案
        const finalMessage = meta.message || message;

        // 2. 入TTS队列（通过taskChain）
        if (window.taskChain) {
            window.taskChain.enqueue('navigation', {
                action,
                direction,
                distance,
                meta: { ...meta, message: finalMessage }
            }, 1); // 导航是high优先级
        } else if (window.speakText) {
            window.speakText(finalMessage, 'cheerful', true);
        }

        // 3. 更新UI
        const uiElement = document.getElementById('navigationGuidance');
        if (uiElement) {
            uiElement.textContent = finalMessage;
            uiElement.className = `navigation-guidance action-${action}`;
            uiElement.style.display = 'block';
        }

        // 4. 更新导航状态（如果存在）
        if (window.getNavStateManager) {
            const navManager = window.getNavStateManager();
            if (navManager && navManager.updateStep) {
                // 更新当前步骤
                const stepIndex = meta.stepIndex || 0;
                navManager.updateStep(stepIndex);
            }
        }

        // 5. 记录日志
        if (window.taskChain) {
            window.taskChain.enqueue('log_record', {
                level: 'info',
                message: `导航事件: ${action}`,
                meta: { direction, distance, ...meta }
            }, 3);
        }

        // 6. 记录事件历史
        manager._recordEvent({
            type: 'navigation',
            action,
            direction,
            distance,
            message: finalMessage,
            meta
        });

        return {
            success: true,
            message: finalMessage,
            action,
            direction,
            distance
        };
    };

    console.log('✅ UnifiedEventManager模块加载完成', { module: 'unified_events' });
})();



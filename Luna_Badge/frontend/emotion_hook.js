/**
 * 情绪事件Hook系统（规范要求）
 * 为Luna情绪系统预留接口
 */

(function() {
    'use strict';

    /**
     * 情绪事件管理器
     */
    class EmotionEventManager {
        constructor() {
            this.hooks = new Map();
            this.eventHistory = [];
            this.maxHistory = 50;
            this.enabled = true;

            // 注册默认hook（空实现，只记录日志）
            this._registerDefaultHooks();

            console.log('✅ EmotionEventManager初始化完成', { module: 'emotion_hook' });
        }

        /**
         * 注册默认hooks
         */
        _registerDefaultHooks() {
            // 危险检测hook
            this.registerHook('hazard_detected', (level, meta) => {
                console.log(`💭 [情绪事件] 危险检测: 级别=${level}`, { module: 'emotion_hook', meta });
                // TODO: 未来接入情绪模块时，这里会触发情绪变化
                // 例如：emotionModule.triggerAnxiety(level, meta);
            });

            // 台阶检测hook
            this.registerHook('step_detected', (level, meta) => {
                console.log(`💭 [情绪事件] 台阶检测: 级别=${level}`, { module: 'emotion_hook', meta });
                // TODO: 未来接入情绪模块
            });

            // 导航开始hook
            this.registerHook('navigation_started', (level, meta) => {
                console.log(`💭 [情绪事件] 导航开始`, { module: 'emotion_hook', meta });
                // TODO: 未来接入情绪模块
            });

            // 导航完成hook
            this.registerHook('navigation_completed', (level, meta) => {
                console.log(`💭 [情绪事件] 导航完成`, { module: 'emotion_hook', meta });
                // TODO: 未来接入情绪模块
            });

            // 用户交互hook
            this.registerHook('user_interaction', (level, meta) => {
                console.log(`💭 [情绪事件] 用户交互`, { module: 'emotion_hook', meta });
                // TODO: 未来接入情绪模块
            });

            // 系统错误hook
            this.registerHook('system_error', (level, meta) => {
                console.log(`💭 [情绪事件] 系统错误: 级别=${level}`, { module: 'emotion_hook', meta });
                // TODO: 未来接入情绪模块，触发焦虑/压力
            });
        }

        /**
         * 注册hook
         */
        registerHook(eventName, handler) {
            if (!this.hooks.has(eventName)) {
                this.hooks.set(eventName, []);
            }
            this.hooks.get(eventName).push(handler);
            console.log(`✅ [情绪事件] 注册hook: ${eventName}`, { module: 'emotion_hook' });
        }

        /**
         * 触发事件
         */
        trigger(eventName, level = 'medium', meta = {}) {
            if (!this.enabled) {
                return;
            }

            // 记录事件历史
            this.eventHistory.push({
                event: eventName,
                level,
                meta,
                timestamp: Date.now()
            });
            if (this.eventHistory.length > this.maxHistory) {
                this.eventHistory.shift();
            }

            // 调用所有注册的handlers
            const handlers = this.hooks.get(eventName) || [];
            handlers.forEach(handler => {
                try {
                    handler(level, meta);
                } catch (error) {
                    console.error(`❌ [情绪事件] Hook执行失败: ${eventName}`, { 
                        module: 'emotion_hook', 
                        error: error.message 
                    });
                }
            });

            console.log(`🔔 [情绪事件] 触发: ${eventName} (级别: ${level})`, { module: 'emotion_hook', meta });
        }

        /**
         * 获取事件历史
         */
        getHistory(limit = 10) {
            return this.eventHistory.slice(-limit);
        }

        /**
         * 启用/禁用
         */
        enable() {
            this.enabled = true;
            console.log('✅ [情绪事件] 已启用', { module: 'emotion_hook' });
        }

        disable() {
            this.enabled = false;
            console.log('⏸️ [情绪事件] 已禁用', { module: 'emotion_hook' });
        }
    }

    // 创建全局实例
    const emotionManager = new EmotionEventManager();

    /**
     * 全局emotion_event函数（规范要求）
     */
    window.emotion_event = function(eventName, level = 'medium', meta = {}) {
        emotionManager.trigger(eventName, level, meta);
    };

    // 导出管理器（供高级用法）
    window.emotionEventManager = emotionManager;

    console.log('✅ EmotionHook模块加载完成', { module: 'emotion_hook' });
})();



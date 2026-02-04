/**
 * 导航事件桥接 (v1.2.0)
 * 处理导航策略输出的nav_action，通过EventDispatcher分发到TTS和调试面板
 */

(function () {
    'use strict';
    
    if (window.NavigationEventBridge) {
        return; // 已加载
    }
    
    function log(msg, extra) {
        console.log('[NavEventBridge] ' + msg, extra || {});
    }
    
    /**
     * 处理nav_action并分发事件
     * @param {Object} navAction - 导航动作对象
     * @param {Object} visionData - 视觉数据（可选）
     */
    function handleNavAction(navAction, visionData) {
        if (!navAction) {
            return;
        }
        
        const action = navAction.action || 'noop';
        const description = navAction.description || '';
        const strategy = navAction.strategy || 'unknown';
        
        log('处理nav_action', { action, strategy, description });
        
        // 通过EventDispatcher分发导航事件
        if (window.EventDispatcher && typeof window.EventDispatcher.emitNavigationEvent === 'function') {
            const navEventData = {
                navState: window.NavigationFSM ? (window.NavigationFSM.state || 'unknown') : 'unknown',
                action: action,
                direction: visionData?.guidance_direction || null,
                distance: navAction.distance || null,
                meta: {
                    strategy: strategy,
                    description: description,
                    error: navAction.error || null,
                    error_code: navAction.error_code || null,
                },
            };
            
            window.EventDispatcher.emitNavigationEvent(navEventData);
            log('已发送导航事件到EventDispatcher', navEventData);
        } else {
            log('⚠️ EventDispatcher未找到，无法分发导航事件');
        }
        
        // 如果nav_action包含TTS描述，直接播报
        if (description && typeof window.speakText === 'function') {
            window.speakText(description, {
                source: 'NavigationStrategy',
                priority: action === 'stop_and_warn' ? 'high' : 'normal',
                strategy: strategy
            });
            log('已通过speakText播报', { description, strategy });
        }
        
        // 更新调试面板（如果存在）
        if (window.__debugPanel && typeof window.__debugPanel.updateNavAction === 'function') {
            window.__debugPanel.updateNavAction(navAction);
        }
    }
    
    /**
     * 处理visual_guidance API响应
     * @param {Object} responseData - API响应数据
     */
    function handleVisualGuidanceResponse(responseData) {
        if (!responseData || !responseData.success) {
            log('⚠️ visual_guidance响应失败', responseData);
            return;
        }
        
        const navAction = responseData.data?.nav_action;
        if (navAction) {
            handleNavAction(navAction, responseData.data);
        } else {
            log('响应中没有nav_action');
        }
    }
    
    // 导出API
    window.NavigationEventBridge = {
        handleNavAction: handleNavAction,
        handleVisualGuidanceResponse: handleVisualGuidanceResponse,
    };
    
    log('NavigationEventBridge已加载');
    
    // 如果存在全局的visual_guidance轮询，自动集成
    if (window.visualGuidancePolling) {
        const originalCallback = window.visualGuidancePolling.callback;
        window.visualGuidancePolling.callback = function(data) {
            if (originalCallback) {
                originalCallback(data);
            }
            handleVisualGuidanceResponse(data);
        };
        log('已集成到visualGuidancePolling');
    }
    
})();




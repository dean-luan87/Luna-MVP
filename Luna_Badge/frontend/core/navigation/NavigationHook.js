/**
 * 导航指引Hook
 * 监听导航指引事件，处理策略优先级、冷却、融合，并触发TTS播报
 * 
 * 完整接入：
 * - 优先级队列
 * - 冷却机制
 * - 策略融合器
 */

import { strategyQueue, strategyCooldown, strategyFusion } from "../strategy";
import { TTSManager } from "../tts/TTSManager";
import { EventDispatcher } from "../event/EventDispatcher";

/**
 * 使用导航指引Hook（React Hook版本）
 * @returns {Object} Hook返回值（当前为空对象）
 */
export function useNavigationGuidance() {
  // 注意：这是React Hook，如果不在React环境中，使用setupNavigationGuidance
  if (typeof window === "undefined" || !window.React) {
    console.warn("[NavigationHook] useNavigationGuidance: React not available, use setupNavigationGuidance instead");
    return {};
  }

  const { useEffect } = window.React;

  useEffect(() => {
    loadModules(); // 确保模块已加载
    
    if (!strategyQueue || !strategyCooldown || !strategyFusion || !TTSManager || !EventDispatcher) {
      console.error("[NavigationHook] 模块未加载完整，无法设置导航指引");
      return;
    }

    function handler(event) {
      if (event.type !== "NAV_GUIDANCE") return;

      // ① 冷却过滤
      if (!strategyCooldown.canTrigger(event.code)) {
        console.log(`[NavigationHook] 策略 ${event.code} 在冷却中，跳过`);
        return;
      }

      // ② 加入优先级队列
      strategyQueue.enqueue(event);

      // ③ 取队列中的全部事件做融合（多个策略同一帧）
      const all = [];
      while (strategyQueue.size() > 0) {
        all.push(strategyQueue.dequeue());
      }

      // ④ 融合策略
      const finalEvent = strategyFusion.fuse(all);

      if (!finalEvent) {
        console.log("[NavigationHook] 融合后无有效事件，跳过");
        return;
      }

      // ⑤ 播报最终策略
      const priority = finalEvent.severity === "critical" ? "HIGH" : 
                      finalEvent.severity === "high" ? "HIGH" : "MEDIUM";

      TTSManager.speak(finalEvent.message, {
        priority: priority,
        style: finalEvent.severity === "critical" ? "urgent" : "calm",
      });

      console.log(`[NavigationHook] 播报策略指引: ${finalEvent.message}`, {
        code: finalEvent.code,
        severity: finalEvent.severity,
        fused: finalEvent.meta?.fused || false,
      });
    }

    EventDispatcher.subscribe(handler);

    return () => {
      EventDispatcher.unsubscribe(handler);
    };
  }, []);

  return {}; // 不返回状态，由 EventDispatcher 驱动 UI
}

/**
 * 设置导航指引监听器（非React版本）
 * 可以在任何JavaScript环境中使用
 */
export function setupNavigationGuidance() {
  loadModules(); // 确保模块已加载
  
  if (!strategyQueue || !strategyCooldown || !strategyFusion || !TTSManager || !EventDispatcher) {
    console.error("[NavigationHook] 模块未加载完整，延迟设置导航指引");
    // 延迟重试
    setTimeout(() => {
      if (strategyQueue && strategyCooldown && strategyFusion && TTSManager && EventDispatcher) {
        setupNavigationGuidance();
      }
    }, 500);
    return () => {};
  }

  function handler(event) {
    if (event.type !== "NAV_GUIDANCE") return;

    // ① 冷却过滤
    if (!strategyCooldown.canTrigger(event.code)) {
      console.log(`[NavigationHook] 策略 ${event.code} 在冷却中，跳过`);
      return;
    }

    // ② 加入优先级队列
    strategyQueue.enqueue(event);

    // ③ 取队列中的全部事件做融合（多个策略同一帧）
    const all = [];
    while (strategyQueue.size() > 0) {
      all.push(strategyQueue.dequeue());
    }

    // ④ 融合策略
    const finalEvent = strategyFusion.fuse(all);

    if (!finalEvent) {
      console.log("[NavigationHook] 融合后无有效事件，跳过");
      return;
    }

    // ⑤ 播报最终策略
    const priority = finalEvent.severity === "critical" ? "HIGH" : 
                    finalEvent.severity === "high" ? "HIGH" : "MEDIUM";

    TTSManager.speak(finalEvent.message, {
      priority: priority,
      style: finalEvent.severity === "critical" ? "urgent" : "calm",
    });

    console.log(`[NavigationHook] 播报策略指引: ${finalEvent.message}`, {
      code: finalEvent.code,
      severity: finalEvent.severity,
      fused: finalEvent.meta?.fused || false,
    });
  }

  EventDispatcher.subscribe(handler);

  // 返回清理函数
  return () => {
    EventDispatcher.unsubscribe(handler);
  };
}

// 自动设置（如果不在React环境中）
if (typeof window !== "undefined") {
  // 延迟初始化，确保其他模块已加载
  function autoSetup() {
    loadModules();
    if (strategyQueue && strategyCooldown && strategyFusion && TTSManager && EventDispatcher) {
      setupNavigationGuidance();
      console.log("[NavigationHook] 导航指引监听器已自动设置");
    } else {
      console.log("[NavigationHook] 等待模块加载...");
      setTimeout(autoSetup, 200);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      setTimeout(autoSetup, 300);
    });
  } else {
    setTimeout(autoSetup, 300);
  }
}

// 导出清理函数供手动调用
export function cleanupNavigationGuidance() {
  if (strategyQueue) strategyQueue.clear();
  if (strategyCooldown) strategyCooldown.reset();
  if (window.guidanceProcessor && typeof window.guidanceProcessor.clear === "function") {
    window.guidanceProcessor.clear();
  }
  console.log("[NavigationHook] 导航指引已清理");
}


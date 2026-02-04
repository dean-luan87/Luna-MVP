/**
 * 策略融合器
 * 多个策略合并成一个最终事件
 * 
 * 用途：
 * - 多个策略同一帧同时触发 → 合并
 * - 例如：弱光 + 反射面 + 积水 → 自动生成一个合成提示
 * - 避免连续播报多次
 * 
 * 融合规则：
 * - 如果 critical 类型存在 → 优先播报 critical
 * - 否则合并 medium / low 级别成一句话
 */

export class StrategyFusion {
  /**
   * 融合多个策略事件
   * @param {Array<Object>} events - 策略事件数组
   * @returns {Object|null} 融合后的事件对象或null
   */
  fuse(events) {
    if (!events || events.length === 0) return null;

    // 若存在 critical 策略 → 直接返回该策略
    const criticalEvent = events.find(e => e.severity === "critical");
    if (criticalEvent) {
      return {
        ...criticalEvent,
        meta: {
          ...criticalEvent.meta,
          fused: false,
          original_count: events.length,
        },
      };
    }

    // 若存在 high 策略 → 优先返回 high
    const highEvent = events.find(e => e.severity === "high");
    if (highEvent && events.length === 1) {
      return highEvent;
    }

    // 否则融合所有 message
    const messages = events.map(e => e.message).filter(Boolean);
    if (messages.length === 0) return null;

    // 去重并合并消息
    const uniqueMessages = [...new Set(messages)];
    const combinedMsg = uniqueMessages.join("，");

    // 确定最高严重程度
    const severities = events.map(e => e.severity);
    const severityOrder = { critical: 4, high: 3, medium: 2, low: 1, info: 0 };
    const maxSeverity = severities.reduce((max, s) => 
      severityOrder[s] > severityOrder[max] ? s : max, "info"
    );

    return {
      type: "NAV_GUIDANCE",
      severity: maxSeverity,
      message: combinedMsg,
      code: "NAV_STRAT_FUSED",
      meta: {
        fused: true,
        count: events.length,
        original_codes: events.map(e => e.code),
      },
    };
  }

  /**
   * 检查是否可以融合
   * @param {Array<Object>} events - 策略事件数组
   * @returns {boolean} 是否可以融合
   */
  canFuse(events) {
    if (!events || events.length < 2) return false;
    
    // 如果有critical，不融合（直接返回critical）
    const hasCritical = events.some(e => e.severity === "critical");
    return !hasCritical;
  }
}

// 导出单例
export const strategyFusion = new StrategyFusion();

// 兼容性：挂载到window（如果使用非模块方式加载）
if (typeof window !== "undefined") {
  window.strategyFusion = strategyFusion;
  window.StrategyFusion = StrategyFusion;
}


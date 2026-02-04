// frontend/core/guidance/StrategyFusion.js
// Guidance 去重（策略融合器）
// 避免出现多条重复指导，比如："光线较暗" + "前方有暗区" + "亮暗交替" → 合并成一句

(function () {
  "use strict";
  if (window.StrategyFusionV2) return; // 避免与旧版本冲突

  class StrategyFusionClass {
    constructor() {
      this.activeCodes = new Set(); // 已经提示过的策略
      this.fusionWindow = 1500; // 1.5 秒内合并策略
      this.lastEmitTime = 0;
      this.cache = []; // 等待融合的事件
      this.resetTimer = null;
    }

    /**
     * 添加策略事件，返回融合后的结果（如果有）
     * @param {Object} event - 策略事件
     * @returns {Object|null} 融合后的事件或null
     */
    add(event) {
      const now = Date.now();

      // 如果策略重复，多次触发就不再播报
      if (this.activeCodes.has(event.code)) {
        console.log(`[StrategyFusion] 策略 ${event.code} 已激活，跳过重复`);
        return null;
      }

      this.cache.push(event);
      this.activeCodes.add(event.code);

      // 设置重置定时器（融合窗口后重置activeCodes）
      if (this.resetTimer) {
        clearTimeout(this.resetTimer);
      }
      this.resetTimer = setTimeout(() => {
        this.activeCodes.clear();
      }, this.fusionWindow * 2);

      // 如果上次融合较久 → 输出新的融合策略
      if (now - this.lastEmitTime > this.fusionWindow) {
        this.lastEmitTime = now;
        const merged = this.merge(this.cache);
        this.cache = [];
        return merged;
      }

      // 否则继续等待融合窗口
      return null;
    }

    /**
     * 合并策略
     * @param {Array<Object>} events - 策略事件数组
     * @returns {Object|null} 融合后的事件
     */
    merge(events) {
      if (!events || events.length === 0) return null;

      const codes = events.map(e => e.code);
      const messages = events.map(e => e.message).filter(Boolean);

      // 规则1: 弱光 + 暗区跳变 → 合并
      if (
        codes.includes("NAV_STRAT_LOW_LIGHT") &&
        codes.includes("NAV_STRAT_DARK_ZONE_AHEAD")
      ) {
        return {
          type: "NAV_GUIDANCE",
          message: "前方光线偏暗，注意脚下。",
          severity: "warning",
          code: "NAV_STRAT_FUSED_LOW_LIGHT_DARK",
          meta: {
            fused: true,
            original_codes: codes,
            count: events.length,
          },
        };
      }

      // 规则2: 反射面 + 多点光源 → 合并
      if (
        codes.includes("NAV_STRAT_REFLECTIVE_SURFACE") &&
        codes.includes("NAV_STRAT_MULTI_LIGHT")
      ) {
        return {
          type: "NAV_GUIDANCE",
          message: "前方环境光线复杂，可能有反光区域，请小心行走。",
          severity: "info",
          code: "NAV_STRAT_FUSED_REFLECTIVE_MULTI",
          meta: {
            fused: true,
            original_codes: codes,
            count: events.length,
          },
        };
      }

      // 规则3: 影子 + 积水 → 合并
      if (
        codes.includes("NAV_STRAT_SHADOW_RISK") &&
        codes.includes("NAV_STRAT_WATER_REFLECTION")
      ) {
        return {
          type: "NAV_GUIDANCE",
          message: "前方地面可能有台阶或积水，请放慢速度，注意脚下。",
          severity: "warning",
          code: "NAV_STRAT_FUSED_SHADOW_WATER",
          meta: {
            fused: true,
            original_codes: codes,
            count: events.length,
          },
        };
      }

      // 规则4: 弱光 + 强逆光 → 合并（矛盾情况）
      if (
        codes.includes("NAV_STRAT_LOW_LIGHT") &&
        codes.includes("NAV_STRAT_BACKLIGHT")
      ) {
        return {
          type: "NAV_GUIDANCE",
          message: "前方光线变化较大，请放慢速度，注意观察。",
          severity: "warning",
          code: "NAV_STRAT_FUSED_LIGHT_CHANGE",
          meta: {
            fused: true,
            original_codes: codes,
            count: events.length,
          },
        };
      }

      // 默认规则：存在critical → 直接返回critical
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

      // 默认：取权重最高的，合并消息
      const sorted = events.sort((a, b) => {
        const weight = { critical: 3, warning: 2, info: 1 };
        return (weight[b.severity] || 0) - (weight[a.severity] || 0);
      });

      const top = sorted[0];
      const uniqueMessages = [...new Set(messages)];

      if (uniqueMessages.length === 1) {
        return top; // 只有一条消息，直接返回
      }

      // 多条消息合并
      return {
        type: "NAV_GUIDANCE",
        message: uniqueMessages.join("，"),
        severity: top.severity,
        code: "NAV_STRAT_FUSED",
        meta: {
          fused: true,
          original_codes: codes,
          count: events.length,
        },
      };
    }

    /**
     * 强制输出当前缓存的事件（不等待融合窗口）
     * @returns {Object|null} 融合后的事件
     */
    flush() {
      if (this.cache.length === 0) return null;
      const merged = this.merge(this.cache);
      this.cache = [];
      this.lastEmitTime = Date.now();
      return merged;
    }

    /**
     * 清空缓存和激活状态
     */
    clear() {
      this.cache = [];
      this.activeCodes.clear();
      this.lastEmitTime = 0;
      if (this.resetTimer) {
        clearTimeout(this.resetTimer);
        this.resetTimer = null;
      }
    }
  }

  window.StrategyFusionV2 = StrategyFusionClass;
  window.strategyFusionV2 = new StrategyFusionClass();

  console.log("[StrategyFusionV2] Guidance去重融合器已加载");
})();




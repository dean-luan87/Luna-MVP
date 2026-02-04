// frontend/core/guidance/GuidanceQueue.js
// Guidance 优先级队列 + 冷却机制
// 规则：critical > warning > info，同优先级按时间顺序处理

(function () {
  "use strict";
  if (window.GuidanceQueue) return;

  const PRIORITY_WEIGHT = {
    critical: 3,
    warning: 2,
    info: 1,
  };

  class GuidanceQueueClass {
    constructor() {
      this.queue = [];
      this.cooldownMap = {}; // { code: timestamp }
      this.cooldown = 2500; // 默认冷却：2.5 秒
    }

    /**
     * 添加 guidance
     * @param {Object} event - 策略事件
     * @param {string} event.severity - 严重程度: critical/warning/info
     * @param {string} event.code - 策略代码
     * @param {string} event.message - 提示消息
     */
    push(event) {
      const now = Date.now();
      const last = this.cooldownMap[event.code];

      // 冷却中 → 不重复播报
      if (last && now - last < this.cooldown) {
        console.log(`[GuidanceQueue] 策略 ${event.code} 在冷却中，跳过`);
        return false;
      }

      this.cooldownMap[event.code] = now;

      this.queue.push({
        ...event,
        weight: PRIORITY_WEIGHT[event.severity] || 1,
        timestamp: now,
      });

      // 重新排序：先按权重降序，再按时间戳升序
      this.queue.sort((a, b) => b.weight - a.weight || a.timestamp - b.timestamp);

      return true;
    }

    /**
     * 取出一个 guidance（最高优先级）
     * @returns {Object|null} 策略事件或null
     */
    pop() {
      return this.queue.shift() || null;
    }

    /**
     * 查看队首（不移除）
     * @returns {Object|null} 策略事件或null
     */
    peek() {
      return this.queue[0] || null;
    }

    /**
     * 当前队列是否为空
     * @returns {boolean}
     */
    isEmpty() {
      return this.queue.length === 0;
    }

    /**
     * 获取队列长度
     * @returns {number}
     */
    size() {
      return this.queue.length;
    }

    /**
     * 清空队列
     */
    clear() {
      this.queue = [];
    }

    /**
     * 重置冷却时间
     * @param {string} code - 策略代码（可选，不传则重置所有）
     */
    resetCooldown(code) {
      if (code) {
        delete this.cooldownMap[code];
      } else {
        this.cooldownMap = {};
      }
    }

    /**
     * 设置冷却时间
     * @param {number} ms - 冷却时间（毫秒）
     */
    setCooldown(ms) {
      this.cooldown = ms;
    }
  }

  window.GuidanceQueue = GuidanceQueueClass;
  window.guidanceQueue = new GuidanceQueueClass();

  console.log("[GuidanceQueue] Guidance优先级队列已加载");
})();




/**
 * 导航策略优先级队列
 * priority: critical > high > medium > low
 * 
 * 用途：
 * - 弱光、反射面、积水等策略 → 按优先级进入队列
 * - TTSManager 只从队列消费最高优先级的项
 * - 避免重复、避免语音轰炸
 */

const PRIORITY_WEIGHTS = {
  critical: 4,
  high: 3,
  medium: 2,
  low: 1,
};

export class StrategyPriorityQueue {
  constructor() {
    this.queue = [];
  }

  /**
   * 入队策略事件
   * @param {Object} strategyEvent - 策略事件对象
   * @param {string} strategyEvent.severity - 严重程度: critical/high/medium/low
   * @param {string} strategyEvent.message - 提示消息
   * @param {string} strategyEvent.code - 策略代码
   * @param {Object} strategyEvent.extra - 额外信息
   */
  enqueue(strategyEvent) {
    const weight = PRIORITY_WEIGHTS[strategyEvent.severity || "low"];
    this.queue.push({ ...strategyEvent, _w: weight });

    // 按权重排序（降序）
    this.queue.sort((a, b) => b._w - a._w);
  }

  /**
   * 出队（取出最高优先级的项）
   * @returns {Object|null} 策略事件对象或null
   */
  dequeue() {
    return this.queue.shift() || null;
  }

  /**
   * 查看队首（不移除）
   * @returns {Object|null} 策略事件对象或null
   */
  peek() {
    return this.queue[0] || null;
  }

  /**
   * 清空队列
   */
  clear() {
    this.queue = [];
  }

  /**
   * 获取队列长度
   * @returns {number} 队列长度
   */
  size() {
    return this.queue.length;
  }

  /**
   * 获取所有队列项（不移除）
   * @returns {Array} 队列数组的副本
   */
  getAll() {
    return [...this.queue];
  }
}

// 导出单例
export const strategyQueue = new StrategyPriorityQueue();

// 兼容性：挂载到window（如果使用非模块方式加载）
if (typeof window !== "undefined") {
  window.strategyQueue = strategyQueue;
  window.StrategyPriorityQueue = StrategyPriorityQueue;
}


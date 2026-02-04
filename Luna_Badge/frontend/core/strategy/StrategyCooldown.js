/**
 * 策略冷却控制
 * 每种策略都有自身的冷却时间，避免重复播报
 * 
 * 用途：
 * - "弱光"每 8 秒最多播报一次
 * - "反光"每 10 秒
 * - "积水"每 15 秒
 * - 按策略类型设定不同冷却时间
 */

const DEFAULT_COOLDOWN = 8000; // 8秒默认冷却

const STRATEGY_COOLDOWN = {
  NAV_STRAT_LOW_LIGHT: 8000,
  NAV_STRAT_REFLECTIVE_SURFACE: 10000,
  NAV_STRAT_SHADOW_RISK: 12000,
  NAV_STRAT_MULTI_LIGHT: 6000,
  NAV_STRAT_WATER_REFLECTION: 15000,
  NAV_STRAT_BACKLIGHT: 8000,
  NAV_STRAT_DARK_ZONE_AHEAD: 10000,
  NAV_STRAT_BRIGHT_ZONE_AHEAD: 10000,
  NAV_STRAT_INTERNAL_ERROR: 5000,
};

export class StrategyCooldown {
  constructor() {
    this.lastTrigger = {}; // { code: timestamp }
  }

  /**
   * 检查是否可以触发策略
   * @param {string} code - 策略代码
   * @returns {boolean} 是否可以触发
   */
  canTrigger(code) {
    const now = Date.now();
    const cooldown = STRATEGY_COOLDOWN[code] || DEFAULT_COOLDOWN;

    if (!this.lastTrigger[code] || now - this.lastTrigger[code] >= cooldown) {
      this.lastTrigger[code] = now;
      return true;
    }
    return false;
  }

  /**
   * 重置指定策略的冷却时间
   * @param {string} code - 策略代码
   */
  reset(code) {
    if (code) {
      delete this.lastTrigger[code];
    } else {
      this.lastTrigger = {};
    }
  }

  /**
   * 获取策略剩余冷却时间（毫秒）
   * @param {string} code - 策略代码
   * @returns {number} 剩余冷却时间，0表示可以触发
   */
  getRemainingCooldown(code) {
    const now = Date.now();
    const cooldown = STRATEGY_COOLDOWN[code] || DEFAULT_COOLDOWN;
    const lastTrigger = this.lastTrigger[code];

    if (!lastTrigger) return 0;

    const elapsed = now - lastTrigger;
    return Math.max(0, cooldown - elapsed);
  }
}

// 导出单例
export const strategyCooldown = new StrategyCooldown();

// 兼容性：挂载到window（如果使用非模块方式加载）
if (typeof window !== "undefined") {
  window.strategyCooldown = strategyCooldown;
  window.StrategyCooldown = StrategyCooldown;
}


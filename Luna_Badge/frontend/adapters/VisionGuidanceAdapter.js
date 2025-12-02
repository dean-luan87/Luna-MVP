/**
 * 视觉导航指引适配器
 * 将后端返回的guidance数据转换为前端事件格式
 */

/**
 * 映射后端guidance响应为前端事件数组
 * @param {Object} responseData - 后端返回的数据
 * @param {Object} responseData.vision - 视觉识别结果
 * @param {Array} responseData.guidance - 策略指引数组
 * @returns {Array<Object>} 事件数组
 */
function mapGuidanceResponse(responseData) {
  if (!responseData || !responseData.guidance) {
    return [];
  }

  const events = [];

  // 遍历每个策略指引
  responseData.guidance.forEach((guidance) => {
    events.push({
      type: "NAV_GUIDANCE",
      severity: guidance.severity || "info",
      message: guidance.message || "",
      code: guidance.code || "UNKNOWN",
      extra: guidance.extra || {},
      timestamp: Date.now(),
    });
  });

  return events;
}

/**
 * 映射单个guidance对象为事件
 * @param {Object} guidance - 单个策略指引对象
 * @returns {Object} 事件对象
 */
function mapSingleGuidance(guidance) {
  return {
    type: "NAV_GUIDANCE",
    severity: guidance.severity || "info",
    message: guidance.message || "",
    code: guidance.code || "UNKNOWN",
    extra: guidance.extra || {},
    timestamp: Date.now(),
  };
}

// 兼容性：导出到全局
if (typeof window !== "undefined") {
  window.mapGuidanceResponse = mapGuidanceResponse;
  window.mapSingleGuidance = mapSingleGuidance;
}

// ES6模块导出
if (typeof module !== "undefined" && module.exports) {
  module.exports = { mapGuidanceResponse, mapSingleGuidance };
}


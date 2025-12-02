// frontend/core/error/ErrorCodeMapper.js
// 错误码系统（ERR_NAV_XXX）→ 前端事件映射
// 让前端能根据错误码快速定位是哪个模块出错

(function () {
  "use strict";
  if (window.ErrorCodeMapper) return;

  /**
   * 错误码映射表
   * 格式：NAV_[模块]_[编号]
   */
  const ERROR_CODE_MAP = {
    // 导航通用错误
    NAV_GENERAL_001: { module: "Navigation", category: "General", level: "error", message: "请求参数缺失" },
    NAV_GENERAL_002: { module: "Navigation", category: "General", level: "error", message: "图片格式不支持" },
    NAV_GENERAL_003: { module: "Navigation", category: "General", level: "error", message: "请求超时" },

    // 图像输入/IO类错误
    NAV_IO_001: { module: "Navigation", category: "IO", level: "error", message: "图片无法读取" },
    NAV_IO_002: { module: "Navigation", category: "IO", level: "error", message: "图片解码失败" },
    NAV_IO_003: { module: "Navigation", category: "IO", level: "error", message: "关键字段为空（vision_frame）" },

    // 视觉处理模块
    NAV_VIS_001: { module: "Vision", category: "YOLO", level: "error", message: "YOLO推理失败" },
    NAV_VIS_002: { module: "Vision", category: "OCR", level: "error", message: "OCR推理失败" },
    NAV_VIS_003: { module: "Vision", category: "Detection", level: "warning", message: "目标检测结果为空" },
    NAV_VIS_004: { module: "Vision", category: "Brightness", level: "warning", message: "摄像头亮度值异常" },

    // 环境识别模块
    NAV_ENV_001: { module: "Environment", category: "Light", level: "error", message: "弱光场景检测失败" },
    NAV_ENV_002: { module: "Environment", category: "Light", level: "error", message: "光照不均衡检测失败" },
    NAV_ENV_003: { module: "Environment", category: "Reflection", level: "error", message: "反射面识别异常" },
    NAV_ENV_004: { module: "Environment", category: "Water", level: "error", message: "水迹检测失败" },
    NAV_ENV_005: { module: "Environment", category: "Backlight", level: "error", message: "逆光区域推测失败" },
    NAV_ENV_006: { module: "Environment", category: "DarkZone", level: "error", message: "暗区跳变分析失败" },
    NAV_ENV_007: { module: "Environment", category: "Glare", level: "error", message: "光斑/眩光分析失败" },

    // 策略生成模块
    NAV_STRAT_001: { module: "Strategy", category: "Generation", level: "error", message: "策略生成失败" },
    NAV_STRAT_002: { module: "Strategy", category: "Fusion", level: "error", message: "策略融合失败" },
    NAV_STRAT_003: { module: "Strategy", category: "Scoring", level: "error", message: "策略评分模块异常" },
    NAV_STRAT_004: { module: "Strategy", category: "Queue", level: "error", message: "策略队列处理失败" },

    // 地图/位置推理模块
    NAV_MAP_001: { module: "Map", category: "Direction", level: "error", message: "无法推断行走方向" },
    NAV_MAP_002: { module: "Map", category: "Path", level: "error", message: "无法确定可通行区域" },
    NAV_MAP_003: { module: "Map", category: "Scene", level: "error", message: "场景分类器错误（室内/室外/夜间判断失败）" },

    // 系统类
    NAV_SYS_001: { module: "System", category: "Memory", level: "critical", message: "内存不足" },
    NAV_SYS_002: { module: "System", category: "Hardware", level: "critical", message: "GPU/NN加速器不可用" },
    NAV_SYS_003: { module: "System", category: "Unknown", level: "error", message: "未知异常" },
  };

  /**
   * 错误码映射器
   */
  class ErrorCodeMapperClass {
    /**
     * 映射错误码到事件对象
     * @param {string|number} code - 错误码（如 "NAV_VIS_001" 或 400030）
     * @param {string} customMessage - 自定义消息（可选）
     * @returns {Object} 事件对象
     */
    map(code, customMessage) {
      // 如果是数字，尝试转换为字符串
      if (typeof code === "number") {
        code = this._numberToCode(code);
      }

      const errorInfo = ERROR_CODE_MAP[code] || {
        module: "Unknown",
        category: "Unknown",
        level: "error",
        message: customMessage || `未知错误码: ${code}`,
      };

      return {
        type: "NAV_ERROR",
        code: code,
        message: customMessage || errorInfo.message,
        module: errorInfo.module,
        category: errorInfo.category,
        severity: errorInfo.level === "critical" ? "critical" : 
                 errorInfo.level === "warning" ? "warning" : "error",
        timestamp: Date.now(),
      };
    }

    /**
     * 将数字错误码转换为字符串代码（简化版）
     * @param {number} code - 数字错误码
     * @returns {string} 字符串代码
     */
    _numberToCode(code) {
      // 简化映射（实际应该从后端获取完整映射表）
      const codeMap = {
        400010: "NAV_GENERAL_001",
        400011: "NAV_GENERAL_002",
        400012: "NAV_GENERAL_003",
        400020: "NAV_IO_001",
        400021: "NAV_IO_002",
        400022: "NAV_IO_003",
        400030: "NAV_VIS_001",
        400031: "NAV_VIS_002",
        400032: "NAV_VIS_003",
        400033: "NAV_VIS_004",
        400040: "NAV_ENV_001",
        400041: "NAV_ENV_002",
        400042: "NAV_ENV_003",
        400043: "NAV_ENV_004",
        400044: "NAV_ENV_005",
        400045: "NAV_ENV_006",
        400046: "NAV_ENV_007",
        400050: "NAV_STRAT_001",
        400051: "NAV_STRAT_002",
        400052: "NAV_STRAT_003",
        400053: "NAV_STRAT_004",
        400060: "NAV_MAP_001",
        400061: "NAV_MAP_002",
        400062: "NAV_MAP_003",
        400070: "NAV_SYS_001",
        400071: "NAV_SYS_002",
        400072: "NAV_SYS_003",
      };
      return codeMap[code] || `NAV_UNKNOWN_${code}`;
    }

    /**
     * 获取错误码信息
     * @param {string|number} code - 错误码
     * @returns {Object} 错误信息
     */
    getInfo(code) {
      if (typeof code === "number") {
        code = this._numberToCode(code);
      }
      return ERROR_CODE_MAP[code] || null;
    }
  }

  const mapper = new ErrorCodeMapperClass();

  // 挂载到全局
  window.ErrorCodeMapper = ErrorCodeMapperClass;
  window.errorCodeMapper = mapper;

  console.log("[ErrorCodeMapper] 错误码映射器已加载");
})();




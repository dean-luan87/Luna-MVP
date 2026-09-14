// frontend/params/ParameterHub.js
// 全局参数中心（危险阈值 / TTS速率 / 检测置信度 / 环境参数）

(function () {
  "use strict";
  if (window.ParameterHub) return;

  window.ParameterHub = {
    // YOLO 置信度阈值
    yolo: {
      dangerThreshold: 0.45,
      generalThreshold: 0.30,
      personThreshold: 0.50,
      distanceDangerMeters: 1.2,
      distanceWarnMeters: 2.5,
    },

    // 导航参数
    navigation: {
      rerouteDistanceMeters: 3.0,
      lostTrackingSeconds: 4,
      stuckRetryCount: 3,
      stuckRetryInterval: 1500,
    },

    // TTS 参数
    tts: {
      rate: 1.0,
      pitch: 1.0,
      volume: 1.0,
      queueEnabled: true,
      minIntervalMs: 1200,
    },

    // 场景图参数
    scene: {
      decayFactor: 0.88,
      memoryReinforceStep: 1.15,
      maxNodeAgeSec: 25,
      mergeDistanceMeter: 1.2,
    },

    // 获取参数值（支持嵌套路径）
    get(path, defaultValue) {
      const parts = path.split(".");
      let value = this;
      for (const part of parts) {
        if (value && typeof value === "object" && part in value) {
          value = value[part];
        } else {
          return defaultValue;
        }
      }
      return value;
    },

    // 设置参数值（支持嵌套路径）
    set(path, value) {
      const parts = path.split(".");
      const lastKey = parts.pop();
      let target = this;
      for (const part of parts) {
        if (!target[part] || typeof target[part] !== "object") {
          target[part] = {};
        }
        target = target[part];
      }
      target[lastKey] = value;
      return true;
    },
  };

  console.log("[ParameterHub] 全局参数中心已加载");
})();


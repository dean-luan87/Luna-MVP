// frontend/vision/VisionBridge.js
// YOLO → SceneGraph → Navigation 桥接

(function () {
  "use strict";
  if (window.VisionBridge) return;

  const ErrorCode = window.ErrorCode || {};
  const LogUploader = window.LogUploader || { push: console.log };
  const ParameterHub = window.ParameterHub || { get: () => null };

  class VisionBridgeClass {
    constructor() {
      this.lastDetectionTime = 0;
      this.detectionCooldown = 100; // 100ms冷却
    }

    // YOLO 输出数据 → SceneGraph
    ingestYolo(detections) {
      const now = Date.now();
      if (now - this.lastDetectionTime < this.detectionCooldown) {
        return; // 冷却中，跳过
      }
      this.lastDetectionTime = now;

      if (!detections || detections.length === 0) {
        LogUploader.push({
          level: "warning",
          code: ErrorCode.YOLO_EMPTY || "E_VISION_EMPTY",
          message: "YOLO returned empty",
          source: "VisionBridge",
        });
        return;
      }

      // 过滤低置信度检测
      const threshold = ParameterHub.get("yolo.generalThreshold", 0.3);
      const filtered = detections.filter((d) => (d.confidence || d.conf) >= threshold);

      if (filtered.length === 0) {
        LogUploader.push({
          level: "warning",
          code: ErrorCode.YOLO_LOW_CONF || "E_VISION_LOW_CONF",
          message: "All detections below threshold",
          source: "VisionBridge",
        });
        return;
      }

      // 更新场景图（如果存在）
      let graphUpdate = null;
      if (window.SceneNodes) {
        try {
          filtered.forEach((detection) => {
            const label = detection.label || detection.class || "unknown";
            window.SceneNodeDetector &&
              window.SceneNodeDetector.updateDetections([detection]);
          });

          graphUpdate = {
            newNodes: filtered.map((d) => ({
              label: d.label || d.class,
              confidence: d.confidence || d.conf,
              position: { x: d.x, y: d.y },
              dangerLevel: this._calculateDangerLevel(d),
            })),
            timestamp: now,
          };
        } catch (err) {
          LogUploader.push({
            level: "error",
            code: ErrorCode.SCENE_UPDATE_FAIL || "E_SCENE_UPDATE_FAIL",
            message: "SceneGraph update failed",
            error: err.toString(),
            source: "VisionBridge",
          });
          return;
        }
      }

      // 场景变化 → 导航钩子
      if (graphUpdate && window.NavigationHook) {
        try {
          window.NavigationHook.handleSceneUpdate(graphUpdate);
        } catch (err) {
          console.warn("[VisionBridge] NavigationHook failed", err);
        }
      }

      // 记录日志
      LogUploader.push({
        level: "info",
        code: "VISION_UPDATE",
        message: "YOLO detection processed",
        source: "VisionBridge",
        details: {
          totalDetections: detections.length,
          filteredDetections: filtered.length,
          graphUpdate: graphUpdate ? graphUpdate.newNodes.length : 0,
        },
      });
    }

    _calculateDangerLevel(detection) {
      const label = (detection.label || detection.class || "").toLowerCase();
      const conf = detection.confidence || detection.conf || 0;

      // 危险物体
      if (label.includes("car") || label.includes("truck") || label.includes("bus")) {
        return conf > 0.5 ? 3 : 2;
      }

      // 台阶/楼梯
      if (label.includes("stair") || label.includes("step")) {
        return conf > 0.6 ? 2 : 1;
      }

      // 行人（中等风险）
      if (label.includes("person") || label.includes("human")) {
        return conf > 0.7 ? 2 : 1;
      }

      return 0;
    }
  }

  window.VisionBridge = new VisionBridgeClass();
  console.log("[VisionBridge] YOLO → SceneGraph → Navigation 桥接已加载");
})();


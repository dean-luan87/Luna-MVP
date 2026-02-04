// frontend/navigation/NavigationHook.js
// 场景影响导航的钩子

(function () {
  "use strict";
  if (window.NavigationHook) return;

  const ParameterHub = window.ParameterHub || { get: () => null };
  const LogUploader = window.LogUploader || { push: console.log };
  const ErrorCode = window.ErrorCode || {};

  class NavigationHookClass {
    static handleSceneUpdate(graphUpdate) {
      if (!graphUpdate || !graphUpdate.newNodes) return;

      // 检查导航是否激活
      const navFSM = window.NavigationFSM;
      if (!navFSM || !navFSM.getState || navFSM.getState() === "IDLE") {
        return;
      }

      const dangerThreshold = ParameterHub.get("yolo.dangerThreshold", 0.45);
      const distanceDanger = ParameterHub.get("yolo.distanceDangerMeters", 1.2);

      for (const node of graphUpdate.newNodes) {
        // 检查危险级别
        if (node.dangerLevel >= 2) {
          // 计算距离（如果有位置信息）
          let shouldAlert = true;
          if (node.position) {
            const distance = Math.sqrt(
              Math.pow(node.position.x || 0, 2) + Math.pow(node.position.y || 0, 2)
            );
            shouldAlert = distance < distanceDanger;
          }

          if (shouldAlert) {
            // 生成TTS警告
            const message = this._generateDangerMessage(node);
            if (window.speakText) {
              window.speakText(message);
            } else if (window.PriorityTTSQueue) {
              window.PriorityTTSQueue.enqueue({
                text: message,
                priority: "HIGH",
                category: "hazard",
              });
            }

            // 记录日志
            LogUploader.push({
              level: "alert",
              code: "NAV_DANGER",
              message: "Navigation danger detected",
              source: "NavigationHook",
              node: node,
            });

            // 更新调试面板
            if (window.__debugPanel) {
              window.__debugPanel.logNav(`⚠️ 危险检测: ${node.label}`);
            }
          }
        }
      }
    }

    static _generateDangerMessage(node) {
      const label = node.label || "障碍物";
      const dangerLevel = node.dangerLevel || 0;

      if (dangerLevel >= 3) {
        return `危险！前方有${label}，请立即避让。`;
      } else if (dangerLevel >= 2) {
        return `注意，前方有${label}，请小心通过。`;
      } else {
        return `前方有${label}，请注意。`;
      }
    }

    // 处理导航卡住
    static handleStuck() {
      const stuckRetryCount = ParameterHub.get("navigation.stuckRetryCount", 3);
      const stuckRetryInterval = ParameterHub.get("navigation.stuckRetryInterval", 1500);

      LogUploader.push({
        level: "warning",
        code: ErrorCode.NAV_STUCK || "E_NAV_STUCK",
        message: "Navigation appears stuck",
        source: "NavigationHook",
      });

      // 触发重路由逻辑（如果存在）
      if (window.NavigationFSM && window.NavigationFSM.reroute) {
        setTimeout(() => {
          window.NavigationFSM.reroute();
        }, stuckRetryInterval);
      }
    }
  }

  window.NavigationHook = NavigationHookClass;
  console.log("[NavigationHook] 场景影响导航钩子已加载");
})();




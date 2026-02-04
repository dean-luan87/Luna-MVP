// frontend/event_dispatcher.js
// 统一事件派发中心（EventDispatcher）

(function () {
  "use strict";
  if (window.EventDispatcher) return;

  const TaskChainUnified = window.TaskChainUnified || {
    enqueue: (fn) => {
      console.warn("[EventDispatcher] TaskChainUnified not found, executing directly");
      try {
        fn();
      } catch (e) {
        console.error("[EventDispatcher] Direct execution error:", e);
      }
    },
  };

  const Hooks = window.Hooks || {
    emit: () => {},
    onScene: [],  // ✅ 新增：场景描述回调
  };

  // 处理危险事件
  function handleHazard(data) {
    const { type, msg, level, meta } = data || {};
    const message = msg || window.SpeechPolicy?.getHazardMessage(type) || "请注意前方情况。";

    // 触发钩子
    Hooks.emit(Hooks.onHazard, { type, message, level, meta });

    // TTS播报
    if (window.speakText) {
      window.speakText(message, level === "critical" ? "urgent" : "calm", false);
    } else if (window.PriorityTTSQueue) {
      window.PriorityTTSQueue.enqueue({
        text: message,
        priority: level === "critical" ? "HIGH" : "MEDIUM",
        category: "hazard",
      });
    }

    // 记录日志
    if (window.LogUploader) {
      window.LogUploader.push({
        level: level || "warning",
        code: "HAZARD_DETECTED",
        message: "Hazard detected",
        source: "EventDispatcher",
        details: { type, message, meta },
      });
    }

    // 更新调试面板
    if (window.__debugPanel) {
      window.__debugPanel.logVision(`⚠️ 危险: ${type} - ${message}`);
    }
  }

  // 处理台阶事件
  function handleStep(data) {
    const { direction, distance, meta } = data || {};
    const message =
      window.SpeechPolicy?.getStepMessage(direction, distance) ||
      `前方${distance || ""}米有台阶，请注意。`;

    // 触发钩子
    Hooks.emit(Hooks.onStep, { direction, distance, message, meta });

    // TTS播报
    if (window.speakText) {
      window.speakText(message, "calm", false);
    } else if (window.PriorityTTSQueue) {
      window.PriorityTTSQueue.enqueue({
        text: message,
        priority: "MEDIUM",
        category: "step",
      });
    }

    // 记录日志
    if (window.LogUploader) {
      window.LogUploader.push({
        level: "info",
        code: "STEP_DETECTED",
        message: "Step detected",
        source: "EventDispatcher",
        details: { direction, distance, message, meta },
      });
    }

    // 更新调试面板
    if (window.__debugPanel) {
      window.__debugPanel.logVision(`📐 台阶: ${direction} - ${distance}m`);
    }
  }

  // 处理导航事件
  function handleNavigation(data) {
    const { navState, action, direction, distance, meta } = data || {};
    const message =
      window.SpeechPolicy?.getNavigationMessage(action, direction, distance) ||
      "请跟随导航指引";

    // 触发钩子
    Hooks.emit(Hooks.onNavigation, { navState, action, direction, distance, message, meta });

    // TTS播报（如果需要）
    if (action && window.speakText) {
      window.speakText(message, "cheerful", false);
    } else if (action && window.PriorityTTSQueue) {
      window.PriorityTTSQueue.enqueue({
        text: message,
        priority: "MEDIUM",
        category: "navigation",
      });
    }

    // 记录日志
    if (window.LogUploader) {
      window.LogUploader.push({
        level: "info",
        code: "NAVIGATION_UPDATE",
        message: "Navigation state updated",
        source: "EventDispatcher",
        details: { navState, action, direction, distance, meta },
      });
    }

    // 更新调试面板
    if (window.__debugPanel) {
      window.__debugPanel.updateNavStatus(navState || {});
      if (action) {
        window.__debugPanel.logNav(`🧭 导航: ${action} - ${message}`);
      }
    }
  }

  // v1.1.1 新增：支持 enhanced hazard data（方向 + 距离）
  function handleEnhancedHazard(bbox, type) {
    const direction = window.calcDirection ? window.calcDirection(bbox) : "front";
    const distance = window.calcDistance ? window.calcDistance(bbox) : null;
    const data = {
      type,
      direction,
      distance,
      width: bbox.x2 - bbox.x1 || null,
      height: bbox.y2 - bbox.y1 || null,
      bbox: bbox, // 保留原始bbox供未来使用
    };

    // 1) 事件加入任务链
    TaskChainUnified.enqueue(() => handleHazard(data));

    // 2) 给语音策略处理（使用新的拟人化文案）
    const msg =
      window.SpeechPolicy?.getHazardSentence(data) ||
      window.SpeechPolicy?.getHazardMessage(type) ||
      "请注意前方情况。";

    TaskChainUnified.enqueue(() => {
      if (window.speakText) {
        window.speakText(msg, data.distance && data.distance < 0.5 ? "urgent" : "calm", false);
      } else if (window.PriorityTTSQueue) {
        window.PriorityTTSQueue.enqueue({
          text: msg,
          priority: data.distance && data.distance < 0.5 ? "HIGH" : "MEDIUM",
          category: "hazard",
        });
      }
    });

    // 3) 发给钩子（未来 Luna 情绪 / 动作建议 入口）
    Hooks.emit(Hooks.onHazard, data);
    Hooks.emit(Hooks.onActionSuggest, data);

    // 4) 记录日志
    if (window.LogUploader) {
      window.LogUploader.push({
        level: data.distance && data.distance < 0.5 ? "warning" : "info",
        code: "ENHANCED_HAZARD_DETECTED",
        message: "Enhanced hazard detected",
        source: "EventDispatcher",
        details: data,
      });
    }

    // 5) 更新调试面板
    if (window.__debugPanel) {
      window.__debugPanel.logVision(`⚠️ 增强危险: ${type} - ${direction} - ${distance ? distance.toFixed(1) + "m" : "未知距离"}`);
    }
  }

  window.EventDispatcher = {
    emitHazardEvent(data) {
      TaskChainUnified.enqueue(() => handleHazard(data));
    },

    // v1.1.1 新增：支持 bbox + type 的增强危险事件
    emitEnhancedHazardEvent(bbox, type) {
      if (!bbox || !type) {
        console.warn("[EventDispatcher] emitEnhancedHazardEvent: missing bbox or type");
        return;
      }
      handleEnhancedHazard(bbox, type);
    },

    emitStepEvent(data) {
      TaskChainUnified.enqueue(() => handleStep(data));
    },

    emitNavigationEvent(data) {
      TaskChainUnified.enqueue(() => handleNavigation(data));
    },

    // ✅ v2.0 新增：场景描述事件入口
    emitSceneDescriptionEvent(data) {
      TaskChainUnified.enqueue(() => handleSceneDescription(data));
    },
  };

  // ✅ v2.0 新增：处理场景描述事件
  function handleSceneDescription(data) {
    const summary = data?.description || data?.summary || "当前场景信息不明确。";
    const sceneType = data?.scene_type || "unknown";

    // 触发 Hooks
    if (Hooks.onScene && Array.isArray(Hooks.onScene)) {
      Hooks.emit(Hooks.onScene, {
        sceneType,
        summary,
        environment: data.environment || {},
        objects: data.objects || [],
        hazards: data.hazards || [],
        explanation: data.explanation || "",
      });
    }

    // TTS 播报（可选，建议只在用户主动问"你看到什么"时才播）
    if (data.shouldSpeak && (window.speakText || window.PriorityTTSQueue)) {
      if (window.speakText) {
        window.speakText(summary, "calm", false);
      } else if (window.PriorityTTSQueue) {
        window.PriorityTTSQueue.enqueue({
          text: summary,
          priority: "MEDIUM",
          category: "scene",
        });
      }
    }

    // 记录日志
    if (window.LogUploader) {
      window.LogUploader.push({
        level: "info",
        code: "SCENE_DESCRIPTION",
        message: "Scene description updated",
        source: "EventDispatcher",
        details: {
          sceneType,
          environment: data.environment || {},
        },
      });
    }

    // 更新调试面板
    if (window.__debugPanel && window.__debugPanel.logVision) {
      window.__debugPanel.logVision(`🖼 场景描述: ${summary}`);
    }
  }

  console.log("[EventDispatcher] 统一事件派发中心已加载");
})();


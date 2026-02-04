// frontend/core/scene/SceneDescriptionHook.js
// 场景描述Hook：监听SCENE_DESCRIPTION事件并自动处理（TTS播报、UI显示等）

(function () {
  "use strict";
  if (window.SceneDescriptionHook) return;

  const EventDispatcher = window.EventDispatcher || { subscribe: () => {} };
  const GuidanceBubble = window.GuidanceBubble || null;
  const TTSManager = window.TTSManager || null;

  class SceneDescriptionHookClass {
    constructor() {
      this.lastDescription = null;
      this.isEnabled = true;
    }

    /**
     * 处理场景描述事件
     * @param {Object} event - SCENE_DESCRIPTION事件
     */
    handle(event) {
      if (!this.isEnabled) return;

      if (event.type !== "SCENE_DESCRIPTION") return;

      this.lastDescription = event;

      // 1. TTS播报
      const summary = event.summary || "";
      if (summary && TTSManager && typeof TTSManager.speak === "function") {
        TTSManager.speak(summary, {
          priority: "MEDIUM",
          style: "calm",
        });
      } else if (summary && window.speakText && typeof window.speakText === "function") {
        window.speakText(summary, {
          source: "SceneDescription",
          priority: "medium",
        });
      }

      // 2. UI显示（如果GuidanceBubble可用）
      if (GuidanceBubble && typeof GuidanceBubble.show === "function") {
        GuidanceBubble.show({
          message: summary,
          severity: this._getSeverityFromScene(event),
          duration: 5000,
          position: "bottom-right",
        });
      }

      // 3. 控制台输出
      console.log("[SceneDescriptionHook] 场景描述:", {
        scene: event.scene,
        summary: summary,
        objects: event.objects?.length || 0,
        hazards: event.hazards?.length || 0,
      });
    }

    /**
     * 处理场景问答事件
     * @param {Object} event - SCENE_QUERY事件
     */
    handleQuery(event) {
      if (!this.isEnabled) return;

      if (event.type !== "SCENE_QUERY") return;

      const answer = event.answer || "";

      // TTS播报答案
      if (answer && TTSManager && typeof TTSManager.speak === "function") {
        TTSManager.speak(answer, {
          priority: "MEDIUM",
          style: "calm",
        });
      } else if (answer && window.speakText && typeof window.speakText === "function") {
        window.speakText(answer, {
          source: "SceneQuery",
          priority: "medium",
        });
      }

      console.log("[SceneDescriptionHook] 场景问答:", {
        question: event.question,
        answer: answer,
      });
    }

    /**
     * 根据场景类型获取严重程度
     * @param {Object} event - SCENE_DESCRIPTION事件
     * @returns {string} 严重程度
     */
    _getSeverityFromScene(event) {
      if (event.hazards && event.hazards.length > 0) {
        const hasHighHazard = event.hazards.some(h => h.severity === "high");
        return hasHighHazard ? "warning" : "info";
      }

      if (event.scene === "dark_indoor") {
        return "warning";
      }

      return "info";
    }

    /**
     * 启用/禁用场景描述Hook
     * @param {boolean} enabled - 是否启用
     */
    setEnabled(enabled) {
      this.isEnabled = enabled;
    }

    /**
     * 获取最后一次场景描述
     * @returns {Object|null} 场景描述事件
     */
    getLastDescription() {
      return this.lastDescription;
    }
  }

  const hook = new SceneDescriptionHookClass();

  // 监听EventDispatcher事件
  if (EventDispatcher.subscribe) {
    EventDispatcher.subscribe(function (event) {
      if (event.type === "SCENE_DESCRIPTION") {
        hook.handle(event);
      } else if (event.type === "SCENE_QUERY") {
        hook.handleQuery(event);
      }
    });
  }

  // 挂载到全局
  window.SceneDescriptionHook = SceneDescriptionHookClass;
  window.sceneDescriptionHook = hook;

  console.log("[SceneDescriptionHook] 场景描述Hook已加载并自动监听事件");
})();




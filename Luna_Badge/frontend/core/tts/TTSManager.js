/**
 * TTS管理器
 * 统一管理文本转语音功能
 */

export const TTSManager = {
  /**
   * 播报文本
   * @param {string} text - 要播报的文本
   * @param {Object} options - 选项
   * @param {string} options.priority - 优先级: HIGH/MEDIUM/LOW
   * @param {string} options.style - 语音风格
   * @param {Function} options.onComplete - 完成回调
   */
  speak(text, options = {}) {
    if (!text || typeof text !== "string") {
      console.warn("[TTSManager] speak: invalid text", text);
      return;
    }

    const priority = options.priority || "MEDIUM";
    const style = options.style || "calm";

    // 使用统一的speakText入口
    if (typeof window.speakText === "function") {
      window.speakText(text, {
        source: "TTSManager",
        priority: priority.toLowerCase(),
        style: style,
        onComplete: options.onComplete,
      });
    } else if (typeof window.PriorityTTSQueue !== "undefined") {
      // 降级到PriorityTTSQueue
      window.PriorityTTSQueue.enqueue({
        text: text,
        priority: priority,
        meta: {
          source: "TTSManager",
          style: style,
        },
        onFinish: options.onComplete,
      });

      // 触发队列处理
      if (window.AudioPipeline && typeof window.AudioPipeline._drain === "function") {
        window.AudioPipeline._drain();
      }
    } else {
      console.warn("[TTSManager] speak: no TTS backend available");
    }
  },

  /**
   * 停止当前播报
   */
  stop() {
    // TODO: 实现停止逻辑
    console.log("[TTSManager] stop: not implemented yet");
  },

  /**
   * 清空队列
   */
  clear() {
    if (window.PriorityTTSQueue && typeof window.PriorityTTSQueue.clear === "function") {
      window.PriorityTTSQueue.clear();
    }
  },
};

// 兼容性：如果全局已有TTSManager，不覆盖
if (typeof window !== "undefined" && !window.TTSManager) {
  window.TTSManager = TTSManager;
}




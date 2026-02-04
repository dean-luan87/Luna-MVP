// frontend/core/guidance/GuidanceProcessor.js
// Guidance 处理器：整合融合器 + 优先级队列 + TTS播报
// 这是Guidance系统的核心处理引擎

(function () {
  "use strict";
  if (window.GuidanceProcessor) return;

  // 延迟加载依赖
  const GuidanceQueue = window.GuidanceQueue || window.StrategyPriorityQueue;
  const StrategyFusion = window.StrategyFusionV2 || window.StrategyFusion;
  const EventDispatcher = window.EventDispatcher || { subscribe: () => {} };
  const TTSManager = window.TTSManager || { speak: () => {} };

  class GuidanceProcessorClass {
    constructor() {
      this.queue = GuidanceQueue ? new GuidanceQueue() : null;
      this.fusion = StrategyFusion ? (typeof StrategyFusion === "function" ? new StrategyFusion() : StrategyFusion) : null;
      this.isProcessing = false;
      this.processInterval = null;
    }

    /**
     * 处理策略事件
     * @param {Object} event - 策略事件
     */
    process(event) {
      if (!event || event.type !== "NAV_GUIDANCE") {
        return;
      }

      // 1. 先送入融合器
      let fused = null;
      if (this.fusion && typeof this.fusion.add === "function") {
        fused = this.fusion.add(event);
      } else {
        // 如果没有融合器，直接使用原事件
        fused = event;
      }

      if (!fused) {
        return; // 融合器返回null（去重或等待融合窗口）
      }

      // 2. 融合后再进入优先级队列
      if (this.queue && typeof this.queue.push === "function") {
        const pushed = this.queue.push(fused);
        if (!pushed) {
          return; // 队列push返回false（冷却中）
        }
      }

      // 3. 触发处理循环
      this._startProcessing();
    }

    /**
     * 开始处理队列
     */
    _startProcessing() {
      if (this.isProcessing) {
        return; // 已在处理中
      }

      this.isProcessing = true;

      // 立即处理一次
      this._processNext();

      // 设置定时器持续处理
      if (this.processInterval) {
        clearInterval(this.processInterval);
      }

      this.processInterval = setInterval(() => {
        if (this.queue && this.queue.isEmpty()) {
          this._stopProcessing();
          return;
        }
        this._processNext();
      }, 500); // 每500ms处理一次
    }

    /**
     * 停止处理
     */
    _stopProcessing() {
      this.isProcessing = false;
      if (this.processInterval) {
        clearInterval(this.processInterval);
        this.processInterval = null;
      }
    }

    /**
     * 处理下一个guidance
     */
    _processNext() {
      if (!this.queue || this.queue.isEmpty()) {
        return;
      }

      // 弹出最优先需要播报的 guidance
      const next = this.queue.pop();
      if (!next) {
        return;
      }

      // 4. 播报（若有 TTS 模块）
      // 根据策略强度评分（score）设置优先级
      let priority = "LOW";
      const score = next.meta?.score || 0;
      
      if (score > 80 || next.severity === "critical") {
        priority = "HIGH";
      } else if (score > 50 || next.severity === "warning") {
        priority = "MEDIUM";
      } else {
        priority = "LOW";
      }

      if (window.TTSManager && typeof window.TTSManager.speak === "function") {
        window.TTSManager.speak(next.message, {
          priority: priority,
          style: next.severity === "critical" ? "urgent" : "calm",
        });
      } else if (window.speakText && typeof window.speakText === "function") {
        window.speakText(next.message, {
          source: "GuidanceProcessor",
          priority: priority.toLowerCase(),
        });
      } else if (window.PriorityTTSQueue && typeof window.PriorityTTSQueue.enqueue === "function") {
        window.PriorityTTSQueue.enqueue({
          text: next.message,
          priority: priority,
          meta: {
            source: "GuidanceProcessor",
            severity: next.severity,
            code: next.code,
          },
        });

        // 触发队列处理
        if (window.AudioPipeline && typeof window.AudioPipeline._drain === "function") {
          window.AudioPipeline._drain();
        }
      }

      console.log(`[GuidanceProcessor] 播报策略指引: ${next.message}`, {
        code: next.code,
        severity: next.severity,
        fused: next.meta?.fused || false,
      });

      // 触发自定义事件（供其他模块监听）
      if (window.dispatchEvent) {
        window.dispatchEvent(new CustomEvent("guidance_processed", {
          detail: next,
        }));
      }
    }

    /**
     * 清空所有状态
     */
    clear() {
      if (this.queue) this.queue.clear();
      if (this.fusion && typeof this.fusion.clear === "function") {
        this.fusion.clear();
      }
      this._stopProcessing();
    }
  }

  const processor = new GuidanceProcessorClass();

  // 监听EventDispatcher的NAV_GUIDANCE事件
  if (EventDispatcher.subscribe) {
    EventDispatcher.subscribe(function (event) {
      if (event.type === "NAV_GUIDANCE") {
        processor.process(event);
      }
    });
  }

  // 监听Hooks.onActionSuggest（兼容现有系统）
  if (window.Hooks && window.Hooks.onActionSuggest && Array.isArray(window.Hooks.onActionSuggest)) {
    window.Hooks.onActionSuggest.push(function (data) {
      processor.process({
        type: "NAV_GUIDANCE",
        severity: data.severity || (data.distance && data.distance < 0.5 ? "critical" : "warning"),
        code: data.code || "NAV_STRATEGY",
        message: data.message || "导航提示",
        extra: data,
      });
    });
  }

  window.GuidanceProcessor = GuidanceProcessorClass;
  window.guidanceProcessor = processor;

  console.log("[GuidanceProcessor] Guidance处理器已加载并自动监听事件");
})();


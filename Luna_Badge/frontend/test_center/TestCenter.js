// frontend/test_center/TestCenter.js
// Luna Badge 测试中心 - 四大板块统一管理

(function () {
  "use strict";
  if (window.TestCenter) return;

  const TestCenter = {
    // ==================== ① 实时视觉调试 ====================
    
    /**
     * 视觉调试：获取完整视觉分析结果
     * @param {Blob|File|string} image - 图像
     * @param {Function} onSuccess - 成功回调
     * @param {Function} onError - 错误回调
     */
    async visionDebug(image, onSuccess, onError) {
      try {
        const form = new FormData();
        if (image instanceof Blob || image instanceof File) {
          form.append("image", image);
        } else if (typeof image === "string") {
          // base64
          const resp = await fetch("/api/test/vision/debug", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: image }),
          });
          const json = await resp.json();
          if (json.success && onSuccess) onSuccess(json.data);
          else if (!json.success && onError) onError(json);
          return json;
        } else {
          throw new Error("image参数必须是Blob、File或base64字符串");
        }

        const resp = await fetch("/api/test/vision/debug", {
          method: "POST",
          body: form,
        });

        const json = await resp.json();
        if (json.success && onSuccess) {
          onSuccess(json.data);
        } else if (!json.success && onError) {
          onError(json);
        }
        return json;
      } catch (error) {
        console.error("[TestCenter] visionDebug error:", error);
        if (onError) onError(error);
        throw error;
      }
    },

    // ==================== ② 功能测试台 ====================

    /**
     * YOLO目标检测测试
     */
    async testYOLO(image, onSuccess, onError) {
      return this._testFeature("/api/test/feature/yolo", image, onSuccess, onError);
    },

    /**
     * OCR文字识别测试
     */
    async testOCR(image, onSuccess, onError) {
      return this._testFeature("/api/test/feature/ocr", image, onSuccess, onError);
    },

    /**
     * 危险检测测试
     */
    async testHazard(image, onSuccess, onError) {
      return this._testFeature("/api/test/feature/hazard", image, onSuccess, onError);
    },

    /**
     * 台阶检测测试
     */
    async testStep(image, onSuccess, onError) {
      return this._testFeature("/api/test/feature/step", image, onSuccess, onError);
    },

    /**
     * 导航功能测试
     */
    async testNavigation(action, data, onSuccess, onError) {
      try {
        const resp = await fetch("/api/test/feature/navigation", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ action: action, ...data }),
        });
        const json = await resp.json();
        if (json.success && onSuccess) onSuccess(json.data);
        else if (!json.success && onError) onError(json);
        return json;
      } catch (error) {
        console.error("[TestCenter] testNavigation error:", error);
        if (onError) onError(error);
        throw error;
      }
    },

    /**
     * TTS语音合成测试
     */
    async testTTS(text, voice, rate, onSuccess, onError) {
      try {
        const resp = await fetch("/api/test/feature/tts", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: text, voice: voice || "zh-CN-XiaoxiaoNeural", rate: rate || "+0%" }),
        });
        const json = await resp.json();
        if (json.success && onSuccess) onSuccess(json.data);
        else if (!json.success && onError) onError(json);
        return json;
      } catch (error) {
        console.error("[TestCenter] testTTS error:", error);
        if (onError) onError(error);
        throw error;
      }
    },

    /**
     * 通用功能测试方法
     */
    async _testFeature(endpoint, image, onSuccess, onError) {
      try {
        const form = new FormData();
        if (image instanceof Blob || image instanceof File) {
          form.append("image", image);
        } else {
          throw new Error("image参数必须是Blob或File");
        }

        const resp = await fetch(endpoint, {
          method: "POST",
          body: form,
        });

        const json = await resp.json();
        if (json.success && onSuccess) {
          onSuccess(json.data);
        } else if (!json.success && onError) {
          onError(json);
        }
        return json;
      } catch (error) {
        console.error(`[TestCenter] ${endpoint} error:`, error);
        if (onError) onError(error);
        throw error;
      }
    },

    // ==================== ③ 联动场景模拟 ====================

    /**
     * 场景A：街道路况导航
     */
    async scenarioStreetNavigation(frames, onSuccess, onError) {
      return this._testScenario("/api/test/scenario/street_navigation", { frames: frames }, onSuccess, onError);
    },

    /**
     * 场景B：室内导航
     */
    async scenarioIndoorNavigation(frames, sceneType, onSuccess, onError) {
      return this._testScenario("/api/test/scenario/indoor_navigation", { frames: frames, scene_type: sceneType }, onSuccess, onError);
    },

    /**
     * 场景C：生活场景
     */
    async scenarioLifeScenarios(scenario, image, onSuccess, onError) {
      return this._testScenario("/api/test/scenario/life_scenarios", { scenario: scenario, image: image }, onSuccess, onError);
    },

    /**
     * 场景D：任务链联动
     */
    async scenarioTaskChain(tasks, onSuccess, onError) {
      return this._testScenario("/api/test/scenario/task_chain", { tasks: tasks }, onSuccess, onError);
    },

    /**
     * 通用场景测试方法
     */
    async _testScenario(endpoint, data, onSuccess, onError) {
      try {
        const resp = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });
        const json = await resp.json();
        if (json.success && onSuccess) onSuccess(json.data);
        else if (!json.success && onError) onError(json);
        return json;
      } catch (error) {
        console.error(`[TestCenter] ${endpoint} error:`, error);
        if (onError) onError(error);
        throw error;
      }
    },

    // ==================== ④ 实时日志 + 性能监控 ====================

    /**
     * 获取性能指标
     */
    async getPerformanceMetrics(onSuccess, onError) {
      try {
        const resp = await fetch("/api/test/performance/metrics");
        const json = await resp.json();
        if (json.success && onSuccess) onSuccess(json.data);
        else if (!json.success && onError) onError(json);
        return json;
      } catch (error) {
        console.error("[TestCenter] getPerformanceMetrics error:", error);
        if (onError) onError(error);
        throw error;
      }
    },

    /**
     * 获取最近日志
     */
    async getRecentLogs(onSuccess, onError) {
      try {
        const resp = await fetch("/api/test/logs/recent");
        const json = await resp.json();
        if (json.success && onSuccess) onSuccess(json.data);
        else if (!json.success && onError) onError(json);
        return json;
      } catch (error) {
        console.error("[TestCenter] getRecentLogs error:", error);
        if (onError) onError(error);
        throw error;
      }
    },

    /**
     * 获取错误日志
     */
    async getErrorLogs(onSuccess, onError) {
      try {
        const resp = await fetch("/api/test/logs/errors");
        const json = await resp.json();
        if (json.success && onSuccess) onSuccess(json.data);
        else if (!json.success && onError) onError(json);
        return json;
      } catch (error) {
        console.error("[TestCenter] getErrorLogs error:", error);
        if (onError) onError(error);
        throw error;
      }
    },
  };

  // 挂载到全局
  window.TestCenter = TestCenter;

  console.log("[TestCenter] Luna Badge测试中心已加载");
})();




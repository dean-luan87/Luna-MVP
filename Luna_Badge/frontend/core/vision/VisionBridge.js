/**
 * 视觉桥接器
 * 负责与后端视觉API通信，并将结果转换为前端事件
 */

import { mapGuidanceResponse } from "../../adapters/VisionGuidanceAdapter";
import { EventDispatcher } from "../event/EventDispatcher";

export const VisionBridge = {
  /**
   * 发送图像帧进行导航指引分析
   * @param {Blob|File} imageBlob - 图像Blob或File对象
   * @param {Object} options - 选项
   * @param {Function} options.onSuccess - 成功回调
   * @param {Function} options.onError - 错误回调
   * @returns {Promise<Array>} 返回事件数组
   */
  async sendFrameForNavigationGuidance(imageBlob, options = {}) {
    if (!imageBlob) {
      const error = new Error("imageBlob is required");
      if (options.onError) options.onError(error);
      throw error;
    }

    try {
      const form = new FormData();
      form.append("image", imageBlob);

      const resp = await fetch("/api/navigation/visual_guidance", {
        method: "POST",
        body: form,
      });

      if (!resp.ok) {
        throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
      }

      const json = await resp.json();

      if (!json.success) {
        throw new Error(json.message || "API返回失败");
      }

      // 映射响应数据为事件
      const events = mapGuidanceResponse(json.data || {});

      // 分发所有事件到EventDispatcher
      events.forEach(e => {
        EventDispatcher.dispatch(e);
        
        // 同时触发Hooks.onActionSuggest（兼容现有系统）
        if (window.Hooks && window.Hooks.onActionSuggest && Array.isArray(window.Hooks.onActionSuggest)) {
          window.Hooks.onActionSuggest.forEach(fn => {
            try {
              fn({
                type: "guidance",
                severity: e.severity,
                code: e.code,
                message: e.message,
                distance: e.extra?.distance,
                direction: e.extra?.direction,
                ...e.extra,
              });
            } catch (err) {
              console.warn("[VisionBridge] Hooks.onActionSuggest error:", err);
            }
          });
        }
      });

      if (options.onSuccess) {
        options.onSuccess(events);
      }

      return events;
    } catch (error) {
      console.error("[VisionBridge] sendFrameForNavigationGuidance error:", error);
      
      if (options.onError) {
        options.onError(error);
      }

      throw error;
    }
  },

  /**
   * 发送base64图像进行导航指引分析
   * @param {string} imageBase64 - base64编码的图像
   * @param {Object} options - 选项
   * @returns {Promise<Array>} 返回事件数组
   */
  async sendBase64ForNavigationGuidance(imageBase64, options = {}) {
    if (!imageBase64) {
      const error = new Error("imageBase64 is required");
      if (options.onError) options.onError(error);
      throw error;
    }

    try {
      const resp = await fetch("/api/navigation/visual_guidance", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          image: imageBase64,
        }),
      });

      if (!resp.ok) {
        throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
      }

      const json = await resp.json();

      if (!json.success) {
        throw new Error(json.message || "API返回失败");
      }

      // 映射响应数据为事件
      const events = mapGuidanceResponse(json.data || {});

      // 分发所有事件到EventDispatcher
      events.forEach(e => {
        EventDispatcher.dispatch(e);
        
        // 同时触发Hooks.onActionSuggest（兼容现有系统）
        if (window.Hooks && window.Hooks.onActionSuggest && Array.isArray(window.Hooks.onActionSuggest)) {
          window.Hooks.onActionSuggest.forEach(fn => {
            try {
              fn({
                type: "guidance",
                severity: e.severity,
                code: e.code,
                message: e.message,
                distance: e.extra?.distance,
                direction: e.extra?.direction,
                ...e.extra,
              });
            } catch (err) {
              console.warn("[VisionBridge] Hooks.onActionSuggest error:", err);
            }
          });
        }
      });

      if (options.onSuccess) {
        options.onSuccess(events);
      }

      return events;
    } catch (error) {
      console.error("[VisionBridge] sendBase64ForNavigationGuidance error:", error);
      
      if (options.onError) {
        options.onError(error);
      }

      throw error;
    }
  },
};

// ✅ 新增：场景描述方法
if (typeof window !== "undefined") {
  const EventDispatcher = window.EventDispatcher || { dispatch: () => {} };
  
  // 记录最近一帧 YOLO 结果
  VisionBridge.lastDetections = VisionBridge.lastDetections || [];

  /**
   * 请求场景描述（新API：/api/vision/describe_scene）
   * 支持传入base64图片或使用已有检测结果
   */
  VisionBridge.requestSceneDescription = async function (imageBase64, options = {}) {
    try {
      // 如果传入的是base64图片
      if (imageBase64 && typeof imageBase64 === 'string' && imageBase64.startsWith('data:image')) {
        const res = await fetch("/api/vision/describe_scene", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ image: imageBase64.split(',')[1] || imageBase64 })
        });

        const json = await res.json();
        if (!json.success) {
          console.warn("[VisionBridge] describe_scene 调用失败:", json.message || json.error);
          return null;
        }

        const data = json.data || json;
        const sceneEvent = {
          summary: data.summary || data.description,
          scene_type: data.scene_type,
          environment: data.environment,
          objects: data.objects || [],
          hazards: data.hazards || [],
          explanation: data.explanation,
          shouldSpeak: options.shouldSpeak !== false,
        };

        // 分发场景描述事件
        if (EventDispatcher.emitSceneDescriptionEvent) {
          EventDispatcher.emitSceneDescriptionEvent(sceneEvent);
        } else if (EventDispatcher.dispatch) {
          EventDispatcher.dispatch({
            type: "SCENE_DESCRIPTION",
            ...sceneEvent,
          });
        }

        return sceneEvent;
      } else {
        // 使用已有检测结果（不传图片版本）
        const payload = {
          detections: imageBase64 || VisionBridge.lastDetections || window.lastYoloOutput || [],
          // 如果你有 OCR 或其它信息，可以一起发
          // ocr_results: window.lastOcrOutput || [],
          // env: { brightness: ..., reflection: ... }
        };

        const res = await fetch("/api/navigation/describe_scene", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });

        const json = await res.json();
        if (!json.success) {
          console.warn("[VisionBridge] describe_scene 调用失败:", json.message || json.error);
          return null;
        }

        const data = json.data || json;
        const sceneEvent = {
          summary: data.summary || data.description,
          scene_type: data.scene_type,
          environment: data.environment,
          objects: data.objects || [],
          hazards: data.hazards || [],
          explanation: data.explanation,
          shouldSpeak: options.shouldSpeak !== false,
        };

        // 分发场景描述事件
        if (EventDispatcher.emitSceneDescriptionEvent) {
          EventDispatcher.emitSceneDescriptionEvent(sceneEvent);
        } else if (EventDispatcher.dispatch) {
          EventDispatcher.dispatch({
            type: "SCENE_DESCRIPTION",
            ...sceneEvent,
          });
        }

        return sceneEvent;
      }
    } catch (e) {
      console.error("[VisionBridge] requestSceneDescription error:", e);
      throw e;
    }
  };

  /**
   * 描述场景（简化版，兼容旧代码）
   */
  VisionBridge.describeScene = VisionBridge.requestSceneDescription;

  /**
   * 提供一个全局方法给测试 / 语音指令用：
   * window.describeCurrentScene()
   */
  window.describeCurrentScene = function (speak = true) {
    if (VisionBridge.requestSceneDescription) {
      VisionBridge.requestSceneDescription({ shouldSpeak: speak });
    } else {
      console.warn("[describeCurrentScene] VisionBridge.requestSceneDescription 未定义");
    }
  };
}

// 兼容性：如果全局已有VisionBridge，合并方法
if (typeof window !== "undefined") {
  if (!window.VisionBridge) {
    window.VisionBridge = VisionBridge;
  } else {
    // 合并新方法到现有VisionBridge
    const existing = window.VisionBridge;
    if (existing.sendFrameForNavigationGuidance === undefined) {
      existing.sendFrameForNavigationGuidance = VisionBridge.sendFrameForNavigationGuidance;
    }
    if (existing.sendBase64ForNavigationGuidance === undefined) {
      existing.sendBase64ForNavigationGuidance = VisionBridge.sendBase64ForNavigationGuidance;
    }
    if (existing.requestSceneDescription === undefined) {
      existing.requestSceneDescription = VisionBridge.requestSceneDescription;
    }
    if (existing.describeScene === undefined) {
      existing.describeScene = VisionBridge.describeScene;
    }
  }
}


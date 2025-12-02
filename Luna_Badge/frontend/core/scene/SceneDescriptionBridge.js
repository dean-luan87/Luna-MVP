// frontend/core/scene/SceneDescriptionBridge.js
// 场景描述桥接器：连接后端场景描述API和前端事件系统

(function () {
  "use strict";
  if (window.SceneDescriptionBridge) return;

  const EventDispatcher = window.EventDispatcher || { dispatch: () => {} };

  const SceneDescriptionBridge = {
    /**
     * 描述当前场景（被动问询）
     * @param {Blob|File|string} image - 图像Blob/File或base64字符串
     * @param {Object} options - 选项
     * @param {Function} options.onSuccess - 成功回调
     * @param {Function} options.onError - 错误回调
     * @returns {Promise<Object>} 场景描述结果
     */
    async describeScene(image, options = {}) {
      try {
        const form = new FormData();
        
        // 处理图像输入
        if (image instanceof Blob || image instanceof File) {
          form.append("image", image);
        } else if (typeof image === "string") {
          // base64字符串
          const body = JSON.stringify({ image: image });
          const resp = await fetch("/api/navigation/describe_scene", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: body,
          });

          if (!resp.ok) {
            throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
          }

          const json = await resp.json();

          if (!json.success) {
            throw new Error(json.message || "场景描述失败");
          }

          // 分发SCENE_DESCRIPTION事件
          const event = {
            type: "SCENE_DESCRIPTION",
            scene: json.data.scene,
            summary: json.data.description,
            objects: json.data.objects || [],
            environment: json.data.environment || {},
            hazards: json.data.hazards || [],
            raw: json.data,
            timestamp: Date.now(),
          };

          EventDispatcher.dispatch(event);

          if (options.onSuccess) {
            options.onSuccess(event);
          }

          return event;
        } else {
          throw new Error("image参数必须是Blob、File或base64字符串");
        }

        // FormData方式
        const resp = await fetch("/api/navigation/describe_scene", {
          method: "POST",
          body: form,
        });

        if (!resp.ok) {
          throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
        }

        const json = await resp.json();

        if (!json.success) {
          throw new Error(json.message || "场景描述失败");
        }

        // 分发SCENE_DESCRIPTION事件
        const event = {
          type: "SCENE_DESCRIPTION",
          scene: json.data.scene,
          summary: json.data.description,
          objects: json.data.objects || [],
          environment: json.data.environment || {},
          hazards: json.data.hazards || [],
          raw: json.data,
          timestamp: Date.now(),
        };

        EventDispatcher.dispatch(event);

        if (options.onSuccess) {
          options.onSuccess(event);
        }

        return event;
      } catch (error) {
        console.error("[SceneDescriptionBridge] describeScene error:", error);
        
        if (options.onError) {
          options.onError(error);
        }

        throw error;
      }
    },

    /**
     * 场景问答
     * @param {string} question - 用户问题
     * @param {Blob|File|string} image - 图像（可选）
     * @param {Object} options - 选项
     * @param {Function} options.onSuccess - 成功回调
     * @param {Function} options.onError - 错误回调
     * @returns {Promise<Object>} 回答结果
     */
    async queryScene(question, image = null, options = {}) {
      try {
        const body = {
          question: question,
        };

        // 如果有图像，添加到请求中
        if (image instanceof Blob || image instanceof File) {
          const form = new FormData();
          form.append("question", question);
          form.append("image", image);

          const resp = await fetch("/api/navigation/scene_query", {
            method: "POST",
            body: form,
          });

          if (!resp.ok) {
            throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
          }

          const json = await resp.json();

          if (!json.success) {
            throw new Error(json.message || "场景问答失败");
          }

          const result = {
            question: question,
            answer: json.data.answer,
            meta: json.data.meta || {},
            timestamp: Date.now(),
          };

          // 分发SCENE_QUERY事件
          EventDispatcher.dispatch({
            type: "SCENE_QUERY",
            question: question,
            answer: result.answer,
            meta: result.meta,
            timestamp: result.timestamp,
          });

          if (options.onSuccess) {
            options.onSuccess(result);
          }

          return result;
        } else {
          // JSON方式
          if (typeof image === "string") {
            body.image = image;
          }

          const resp = await fetch("/api/navigation/scene_query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
          });

          if (!resp.ok) {
            throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
          }

          const json = await resp.json();

          if (!json.success) {
            throw new Error(json.message || "场景问答失败");
          }

          const result = {
            question: question,
            answer: json.data.answer,
            meta: json.data.meta || {},
            timestamp: Date.now(),
          };

          // 分发SCENE_QUERY事件
          EventDispatcher.dispatch({
            type: "SCENE_QUERY",
            question: question,
            answer: result.answer,
            meta: result.meta,
            timestamp: result.timestamp,
          });

          if (options.onSuccess) {
            options.onSuccess(result);
          }

          return result;
        }
      } catch (error) {
        console.error("[SceneDescriptionBridge] queryScene error:", error);
        
        if (options.onError) {
          options.onError(error);
        }

        throw error;
      }
    },
  };

  // 挂载到全局
  window.SceneDescriptionBridge = SceneDescriptionBridge;

  console.log("[SceneDescriptionBridge] 场景描述桥接器已加载");
})();




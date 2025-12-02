/**
 * 事件分发器
 * 统一管理前端事件订阅和分发
 */

export const EventDispatcher = {
  _subs: [],

  /**
   * 订阅事件
   * @param {Function} fn - 事件处理函数
   */
  subscribe(fn) {
    if (typeof fn !== "function") {
      console.warn("[EventDispatcher] subscribe: fn must be a function");
      return;
    }
    this._subs.push(fn);
  },

  /**
   * 取消订阅
   * @param {Function} fn - 要移除的事件处理函数
   */
  unsubscribe(fn) {
    this._subs = this._subs.filter(x => x !== fn);
  },

  /**
   * 分发事件
   * @param {Object} event - 事件对象
   */
  dispatch(event) {
    if (!event || typeof event !== "object") {
      console.warn("[EventDispatcher] dispatch: invalid event", event);
      return;
    }

    // 确保事件有type
    if (!event.type) {
      console.warn("[EventDispatcher] dispatch: event missing type", event);
      return;
    }

    // 添加时间戳（如果没有）
    if (!event.timestamp) {
      event.timestamp = Date.now();
    }

    // 通知所有订阅者
    this._subs.forEach(fn => {
      try {
        fn(event);
      } catch (e) {
        console.error("[EventDispatcher] subscriber error:", e);
      }
    });
  },

  /**
   * 清空所有订阅者
   */
  clear() {
    this._subs = [];
  },

  /**
   * 获取订阅者数量
   * @returns {number} 订阅者数量
   */
  getSubscriberCount() {
    return this._subs.length;
  },

  /**
   * 处理场景描述事件
   * @param {Object} data - 场景描述数据
   */
  handleSceneDescription(data) {
    if (!data) return;
    
    console.log('📸 [Scene] 场景描述：', data);
    
    // 更新UI显示
    const box = document.getElementById("sceneDescriptionBox");
    if (box) {
      box.innerHTML = `
        <div class="summary">${data.summary || '无描述'}</div>
        <pre class="objects">${JSON.stringify(data.objects || [], null, 2)}</pre>
      `;
    }
    
    // 触发TTS播报
    if (data.summary && window.speakText) {
      window.speakText(data.summary, { source: 'SceneDescription', priority: 'normal' });
    }
    
    // 显示场景描述UI
    if (window.GuidanceBubble && data.summary) {
      window.GuidanceBubble.show({
        message: data.summary,
        severity: 'info',
        position: 'bottom-right'
      });
    }
  },

  /**
   * 场景描述事件处理（别名，兼容旧代码）
   * @param {Object} data - 场景描述数据
   */
  onSceneDescription(data) {
    this.handleSceneDescription(data);
  },

  /**
   * 发送场景描述事件
   * @param {Object} data - 场景描述数据
   */
  emitSceneDescriptionEvent(data) {
    this.dispatch({
      type: 'SCENE_DESCRIPTION',
      ...data
    });
    this.handleSceneDescription(data);
  },
};

// 兼容性：如果全局已有EventDispatcher，不覆盖
if (typeof window !== "undefined" && !window.EventDispatcher) {
  window.EventDispatcher = EventDispatcher;
}


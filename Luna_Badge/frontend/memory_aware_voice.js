// frontend/memory_aware_voice.js
/**
 * MemoryAwareVoice / 记忆敏感语音引擎
 * 解决："同一个地方的同一条提醒，不要一直重复说"
 * 结合 MapMemoryPro 的结构记忆做语音抑制 / 降频
 */
(function () {
  'use strict';
  
  if (window.MemoryAwareVoice) return;

  function logInfo(m, p) { window.logInfo?.('[MemoryAwareVoice] ' + m, p ?? {}); }
  function logDebug(m, p) { window.logDebug?.('[MemoryAwareVoice] ' + m, p ?? {}); }
  function logError(m, p) { window.logError?.('[MemoryAwareVoice] ' + m, p ?? {}); }

  function MemoryAwareVoiceClass() {
    this.lastByKey = {}; // key -> { ts, count }
    this.cooldownMs = 8000; // 同一类提示 8 秒内不重复
  }

  MemoryAwareVoiceClass.prototype._makeKey = function (task) {
    try {
      if (!task?.type) return null;
      const type = task.type;
      const text = task.payload?.text || '';
      const sceneType = task.payload?.scene_type || '';
      const code = task.payload?.code || '';

      // 粗略 hash
      return `${type}|${code}|${sceneType}|${text.slice(0, 20)}`;
    } catch (e) {
      logError('_makeKey error', { e });
      return null;
    }
  };

  MemoryAwareVoiceClass.prototype._shouldSuppress = function (key) {
    if (!key) return false;
    const info = this.lastByKey[key];
    if (!info) return false;

    const now = Date.now();
    if (now - info.ts < this.cooldownMs) return true;
    return false;
  };

  MemoryAwareVoiceClass.prototype._record = function (key) {
    if (!key) return;
    const now = Date.now();
    const old = this.lastByKey[key];
    this.lastByKey[key] = {
      ts: now,
      count: old ? old.count + 1 : 1
    };
  };

  /**
   * 包装一个任务，决定是否让它继续进入 SpeechRhythm
   */
  MemoryAwareVoiceClass.prototype.handleTask = function (task) {
    try {
      const key = this._makeKey(task);
      if (this._shouldSuppress(key)) {
        logDebug('suppress repeated task', { key, task });
        return; // 丢弃
      }

      this._record(key);

      // 继续丢给 SpeechRhythm
      if (window.SpeechRhythm && typeof window.SpeechRhythm.handleTask === 'function') {
        window.SpeechRhythm.handleTask(task);
      } else {
        logDebug('SpeechRhythm not ready, skip', {});
      }
    } catch (e) {
      logError('handleTask error', { e });
    }
  };

  window.MemoryAwareVoice = new MemoryAwareVoiceClass();

  // 一个便捷函数：对外统一入口
  window.enqueueNavHintWithMemory = function (text, extra) {
    const task = {
      type: 'NAV_HINT',
      payload: Object.assign({ text }, extra || {})
    };
    window.MemoryAwareVoice.handleTask(task);
  };

  if (window.logInfo) {
    window.logInfo('MemoryAwareVoice模块加载完成', { module: 'memory_aware_voice' });
  } else {
    console.log('✅ MemoryAwareVoice模块加载完成', { module: 'memory_aware_voice' });
  }
})();


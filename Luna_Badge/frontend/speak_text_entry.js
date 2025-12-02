// frontend/speak_text_entry.js
// 提供一个统一的 window.speakText 入口

(function () {
  'use strict';

  if (typeof window.speakText === 'function') {
    // 已经有实现就不覆盖
    return;
  }

  function log(msg, extra) {
    console.log('[speakText] ' + msg, extra || {});
  }

  window.speakText = function (text, options) {
    options = options || {};
    const PriorityTTSQueue = window.PriorityTTSQueue || window.priorityTTSQueue;
    const AudioPipeline = window.AudioPipeline;

    if (!text || typeof text !== 'string') {
      log('⚠️ 无效的 text 参数', { text });
      return;
    }

    if (PriorityTTSQueue && typeof PriorityTTSQueue.enqueue === 'function') {
      PriorityTTSQueue.enqueue({
        type: 'TTS',
        text,
        meta: {
          source: options.source || 'speakText',
          priority: options.priority || 'normal'
        }
      });
      // 如果 AudioPipeline 有 _drain 方法，手动触发一次
      if (AudioPipeline && typeof AudioPipeline._drain === 'function') {
        AudioPipeline._drain();
      }
      log('已通过 PriorityTTSQueue 发送 TTS', { text });
    } else {
      log('⚠️ 未找到 PriorityTTSQueue，无法播报', {});
    }
  };

  log('speakText 已挂载到 window');
})();


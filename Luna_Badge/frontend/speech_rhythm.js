// frontend/speech_rhythm.js
/**
 * SpeechRhythm / 语音播报节奏管理
 * 节流、去骚扰、优先级、连续播报
 */
(function () {
  'use strict';
  
  if (window.SpeechRhythm) return;

  function logInfo(m, p) { window.logInfo?.('[SpeechRhythm] ' + m, p ?? {}); }
  function logDebug(m, p) { window.logDebug?.('[SpeechRhythm] ' + m, p ?? {}); }
  function logError(m, p) { window.logError?.('[SpeechRhythm] ' + m, p ?? {}); }

  const PRIORITY = { CRITICAL: 3, HIGH: 2, MEDIUM: 1, LOW: 0 };
  const now = () => Date.now();

  function sortQueue(q) {
    q.sort((a, b) => {
      const pa = PRIORITY[a.priority] ?? 0;
      const pb = PRIORITY[b.priority] ?? 0;
      if (pa !== pb) return pb - pa;
      return a.ts - b.ts;
    });
  }

  function Rhythm() {
    this.queue = [];
    this.lastTs = 0;
    this.minInterval = 1200;
    this.isSpeaking = false;
    this.timer = null;
    this.userMute = false;
  }

  Rhythm.prototype._ensureTimer = function () {
    if (this.timer) return;
    this.timer = setInterval(() => this._tick(), 300);
  };

  Rhythm.prototype._tick = function () {
    if (!this.queue.length) return;
    if (this.isSpeaking) return;
    if (now() - this.lastTs < this.minInterval) return;
    if (this.userMute) return;

    sortQueue(this.queue);
    const task = this.queue.shift();
    if (!task) return;

    this._speak(task);
  };

  Rhythm.prototype._speak = function (task) {
    this.isSpeaking = true;
    this.lastTs = now();

    logInfo('speak', task);

    try {
      if (window.PriorityTTSQueue?.enqueue) {
        window.PriorityTTSQueue.enqueue({
          text: task.text,
          priority: task.priority,
          category: task.category,
          onFinish: () => (this.isSpeaking = false),
          onError: () => (this.isSpeaking = false)
        });
        return;
      }

      if (window.speakText) {
        window.speakText(task.text);
        this.isSpeaking = false;
        return;
      }
    } catch (err) {
      logError('TTS error', err);
    }
    this.isSpeaking = false;
  };

  Rhythm.prototype.enqueueSpeech = function (o) {
    if (!o?.text) return;

    this.queue.push({
      text: o.text,
      category: o.category || 'info',
      priority: o.priority || 'MEDIUM',
      meta: o.meta || {},
      ts: now()
    });

    this._ensureTimer();
  };

  Rhythm.prototype.handleTask = function (task) {
    if (!task?.type) return;

    if (task.type === 'HAZARD_WARNING') {
      const text =
        task.payload?.hazard_text ||
        window.SpatialSemantic?.buildHazardText(task.payload?.hazard, task.payload?.enhancedState);

      if (!text) return;

      this.enqueueSpeech({
        text,
        category: 'hazard',
        priority: 'CRITICAL'
      });
      return;
    }

    if (task.type === 'NAV_HINT') {
      if (task.payload?.text)
        this.enqueueSpeech({
          text: task.payload.text,
          category: 'nav',
          priority: 'HIGH'
        });
      return;
    }

    if (task.type === 'INFO_TTS') {
      if (task.payload?.text)
        this.enqueueSpeech({
          text: task.payload.text,
          category: 'info',
          priority: 'LOW'
        });
    }
  };

  window.SpeechRhythm = new Rhythm();

  if (window.logInfo) {
    window.logInfo('SpeechRhythm模块加载完成', { module: 'speech_rhythm' });
  } else {
    console.log('✅ SpeechRhythm模块加载完成', { module: 'speech_rhythm' });
  }
})();


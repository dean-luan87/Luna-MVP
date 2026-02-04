// frontend/logger.js
/**
 * 统一日志系统（浏览器 → 后端）
 * 支持 info / warn / error / debug 等级
 * 所有视觉 / 导航 / TTS / 状态机 / 异常都走这里
 */
(function () {
  'use strict';
  
  if (window.LunaLogger) return;

  const DEFAULT_ENDPOINT = "/api/logs/ingest";

  class LunaLogger {
    constructor() {
      this.sessionId = this._generateSessionId();
      this.endpoint = DEFAULT_ENDPOINT;
      this.enabled = true;
    }

    _generateSessionId() {
      if (window.crypto && window.crypto.randomUUID) {
        return window.crypto.randomUUID();
      }
      return 'sess-' + Date.now() + '-' + Math.random().toString(16).slice(2);
    }

    setEndpoint(url) {
      this.endpoint = url;
    }

    _basePayload(extra) {
      return Object.assign({
        ts: Date.now(),
        sessionId: this.sessionId,
        userAgent: navigator.userAgent || '',
      }, extra || {});
    }

    _toConsole(level, msg, payload) {
      const prefix = `[Luna/${level.toUpperCase()}]`;
      if (level === 'error') {
        console.error(prefix, msg, payload || '');
      } else if (level === 'warn') {
        console.warn(prefix, msg, payload || '');
      } else if (level === 'debug') {
        console.debug(prefix, msg, payload || '');
      } else {
        console.log(prefix, msg, payload || '');
      }
    }

    _toBackend(level, msg, payload) {
      if (!this.enabled || !this.endpoint || !window.fetch) return;
      const body = this._basePayload(Object.assign({
        level,
        message: msg,
        payload: payload || {}
      }));

      try {
        fetch(this.endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body)
        }).catch(() => { /* 静默失败，不打断主流程 */ });
      } catch (e) {
        // ignore
      }
    }

    log(level, msg, payload) {
      this._toConsole(level, msg, payload);
      this._toBackend(level, msg, payload);
    }

    info(msg, payload) { this.log('info', msg, payload); }
    warn(msg, payload) { this.log('warn', msg, payload); }
    error(msg, payload) { this.log('error', msg, payload); }
    debug(msg, payload) { this.log('debug', msg, payload); }
  }

  window.LunaLogger = new LunaLogger();

  window.logInfo = (msg, payload) => window.LunaLogger.info(msg, payload);
  window.logWarn = (msg, payload) => window.LunaLogger.warn(msg, payload);
  window.logError = (msg, payload) => window.LunaLogger.error(msg, payload);
  window.logDebug = (msg, payload) => window.LunaLogger.debug(msg, payload);
  
  console.log('✅ LunaLogger模块加载完成', { module: 'logger' });
})();



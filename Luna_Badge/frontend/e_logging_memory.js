// frontend/e_logging_memory.js
// E 系列：结构化日志 + 远程上传 + 记忆审计
// 说明：不会破坏现有 console.*，而是在此基础上增强。

(function () {
  'use strict';
  
  if (window.LunaLogger && window.RemoteLogger && window.MemoryAudit) {
    return;
  }

  // =========================
  // E1. LunaLogger 结构化日志
  // =========================
  if (!window.LunaLogger) {
    function LunaLoggerClass() {
      this.deviceId = window.__LUNA_DEVICE_ID__ || null;
      this.sessionId =
        window.__LUNA_SESSION_ID__ ||
        (Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 8));
      this.buffer = [];
      this.subscribers = [];
      this.maxBuffer = 500;
    }

    LunaLoggerClass.prototype._emit = function (level, message, details) {
      const evt = {
        ts: new Date().toISOString(),
        level: level.toUpperCase(),
        message: message || '',
        details: details || {},
        deviceId: this.deviceId,
        sessionId: this.sessionId,
      };

      // console 输出
      try {
        const tag = `[Luna][${evt.level}]`;
        if (evt.level === 'ERROR') console.error(tag, evt.message, evt.details);
        else if (evt.level === 'WARN') console.warn(tag, evt.message, evt.details);
        else console.log(tag, evt.message, evt.details);
      } catch (e) {
        console.log('[Luna][LOG-FALLBACK]', evt);
      }

      // 放入缓冲
      this.buffer.push(evt);
      if (this.buffer.length > this.maxBuffer) {
        this.buffer.shift();
      }

      // 通知订阅者（例如 RemoteLogger / 本地调试 UI）
      for (const sub of this.subscribers) {
        try {
          sub(evt);
        } catch (e) {
          console.log('[Luna][Logger subscriber error]', e);
        }
      }

      return evt;
    };

    LunaLoggerClass.prototype.debug = function (msg, details) {
      return this._emit('DEBUG', msg, details);
    };

    LunaLoggerClass.prototype.info = function (msg, details) {
      return this._emit('INFO', msg, details);
    };

    LunaLoggerClass.prototype.warn = function (msg, details) {
      return this._emit('WARN', msg, details);
    };

    LunaLoggerClass.prototype.error = function (msg, details) {
      return this._emit('ERROR', msg, details);
    };

    LunaLoggerClass.prototype.subscribe = function (fn) {
      if (typeof fn === 'function') {
        this.subscribers.push(fn);
      }
    };

    LunaLoggerClass.prototype.drainBuffer = function () {
      const data = this.buffer.slice();
      this.buffer = [];
      return data;
    };

    window.LunaLogger = new LunaLoggerClass();

    // 全局便捷函数（兼容之前 logInfo/logWarn 等）
    window.logDebug = function (msg, details) {
      window.LunaLogger.debug(msg, details);
    };

    window.logInfo = function (msg, details) {
      window.LunaLogger.info(msg, details);
    };

    window.logWarn = function (msg, details) {
      window.LunaLogger.warn(msg, details);
    };

    window.logError = function (msg, details) {
      window.LunaLogger.error(msg, details);
    };
  }

  // =========================
  // E2. RemoteLogger 远程日志上传
  // =========================
  if (!window.RemoteLogger) {
    function RemoteLoggerClass() {
      this.endpoint = window.__LUNA_LOG_ENDPOINT__ || '/api/logs';
      this.queue = [];
      this.sending = false;
      this.timer = null;
      this.batchSize = 30;
      this.intervalMs = 3000;
      this.maxQueue = 1000;
      this.enabled = true;
      this._initTimer();
    }

    RemoteLoggerClass.prototype._initTimer = function () {
      if (this.timer) clearInterval(this.timer);
      this.timer = setInterval(() => this._flush(), this.intervalMs);
    };

    RemoteLoggerClass.prototype.push = function (evt) {
      if (!this.enabled) return;
      this.queue.push(evt);
      if (this.queue.length > this.maxQueue) {
        this.queue.splice(0, this.queue.length - this.maxQueue);
      }
    };

    RemoteLoggerClass.prototype._flush = function () {
      if (!this.enabled) return;
      if (this.sending) return;
      if (!this.queue.length) return;
      if (typeof fetch !== 'function') return;

      const batch = this.queue.splice(0, this.batchSize);
      if (!batch.length) return;

      this.sending = true;

      fetch(this.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ logs: batch }),
      })
        .then((res) => {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res.text();
        })
        .then(() => {
          this.sending = false;
        })
        .catch((e) => {
          // 出错则把 batch 放回队列前面
          this.sending = false;
          this.queue = batch.concat(this.queue);
          console.warn('[RemoteLogger] flush error, will retry', e);
        });
    };

    RemoteLoggerClass.prototype.setEnabled = function (flag) {
      this.enabled = !!flag;
    };

    window.RemoteLogger = new RemoteLoggerClass();

    // 订阅 LunaLogger
    window.LunaLogger.subscribe(function (evt) {
      window.RemoteLogger.push(evt);
    });
  }

  // =========================
  // E3. MemoryAudit 记忆修改审计
  // =========================
  if (!window.MemoryAudit) {
    function MemoryAuditClass() {
      this.records = [];
      this.maxRecords = 500;
    }

    /**
     * 记录一次记忆更新
     * @param {Object} payload - {
     *   source: 'vision' | 'user' | 'system' | ...,
     *   key: 'scene.hospital.3f.toilet',
     *   before: any,
     *   after: any,
     *   confidence: number,
     *   note: string
     * }
     */
    MemoryAuditClass.prototype.recordUpdate = function (payload) {
      const rec = {
        ts: new Date().toISOString(),
        source: payload.source || 'unknown',
        key: payload.key || '',
        before: payload.before,
        after: payload.after,
        confidence:
          typeof payload.confidence === 'number' ? payload.confidence : null,
        note: payload.note || '',
      };

      this.records.push(rec);
      if (this.records.length > this.maxRecords) {
        this.records.shift();
      }

      if (window.LunaLogger) {
        window.LunaLogger.info('Memory update', { memoryUpdate: rec });
      }

      return rec;
    };

    MemoryAuditClass.prototype.getRecent = function (limit) {
      if (!limit || limit <= 0) limit = 50;
      if (this.records.length <= limit) {
        return this.records.slice();
      }
      return this.records.slice(this.records.length - limit);
    };

    window.MemoryAudit = new MemoryAuditClass();

    // 一个便捷函数：统一入口
    window.logMemoryUpdate = function (payload) {
      return window.MemoryAudit.recordUpdate(payload || {});
    };
  }

  // =========================
  // E4. 未捕获错误 & Promise 拦截
  // =========================
  if (typeof window !== 'undefined') {
    window.addEventListener('error', function (event) {
      try {
        window.LunaLogger.error('window.error', {
          message: event.message,
          filename: event.filename,
          lineno: event.lineno,
          colno: event.colno,
          error: event.error ? String(event.error) : null,
        });
      } catch (e) {
        console.error('[Luna][window.error logger failed]', e);
      }
    });

    window.addEventListener('unhandledrejection', function (event) {
      try {
        window.LunaLogger.error('unhandledrejection', {
          reason: event.reason ? String(event.reason) : null,
        });
      } catch (e) {
        console.error('[Luna][unhandledrejection logger failed]', e);
      }
    });
  }

  window.LunaLogger.info('E Logging+Memory module initialized', {});
})();


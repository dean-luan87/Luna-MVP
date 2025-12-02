// frontend/de_navigation_audio.js
// D 系列：导航 FSM + 播报链 + 危险打断/恢复
// 说明：全部挂在 window 上，不破坏现有代码，如果已有同名对象则跳过。

(function () {
  'use strict';
  
  // 避免重复加载
  if (window.NavigationFSM && window.AudioPipeline && window.DangerEnginePro) {
    return;
  }

  // 简单日志封装（优先走 LunaLogger）
  function log(level, msg, details) {
    try {
      if (window.LunaLogger && window.LunaLogger[level]) {
        window.LunaLogger[level](msg, details || {});
      } else {
        const tag = `[${level.toUpperCase()}][DE]`;
        if (level === 'error') console.error(tag, msg, details || {});
        else if (level === 'warn') console.warn(tag, msg, details || {});
        else console.log(tag, msg, details || {});
      }
    } catch (e) {
      console.log('[DE][log-fallback]', msg, details || {}, e);
    }
  }

  // =========================
  // D1. AudioPipeline 语音播报管线
  // =========================
  if (!window.AudioPipeline) {
    function AudioPipelineClass() {
      this.queue = [];
      this.playing = false;
      this.currentTaskId = null;
      this.defaultVoice = 'default';
      this.fallbackSpeakFn = window.speakText || window.speakTextSmart || null;
    }

    // 入队：text 必填，priority 越小优先级越高（0=critical）
    AudioPipelineClass.prototype.enqueue = function (opts) {
      const task = {
        id: opts.id || ('tts-' + Date.now() + '-' + Math.random().toString(16).slice(2)),
        text: opts.text,
        priority: typeof opts.priority === 'number' ? opts.priority : 5,
        category: opts.category || 'nav', // nav / danger / info / system
        meta: opts.meta || {},
        onDone: typeof opts.onDone === 'function' ? opts.onDone : null,
      };
      if (!task.text) return;

      this.queue.push(task);
      // 简单优先级排序
      this.queue.sort((a, b) => a.priority - b.priority);

      log('debug', 'AudioPipeline enqueue', { len: this.queue.length, task });
      this._drain();
    };

    AudioPipelineClass.prototype._drain = function () {
      if (this.playing) return;
      if (!this.queue.length) return;

      const task = this.queue.shift();
      this.playing = true;
      this.currentTaskId = task.id;

      log('info', 'AudioPipeline play', {
        id: task.id,
        category: task.category,
        text: task.text,
      });

      // 优先使用 SpeechRhythm（如果存在）
      if (window.SpeechRhythm && typeof window.SpeechRhythm.handleTask === 'function') {
        try {
          window.SpeechRhythm.handleTask({
            type: 'TTS',
            payload: {
              text: task.text,
              category: task.category,
              meta: task.meta,
              onDone: () => this._finish(task),
            },
          });
          // 注意：如果 SpeechRhythm 内部没有调用 onDone，我们需要兜底
          this._fallbackTimeout(task);
          return;
        } catch (e) {
          log('error', 'SpeechRhythm handleTask error', { e });
        }
      }

      // 然后尝试 PriorityTTSQueue（如果存在）
      if (window.PriorityTTSQueue && typeof window.PriorityTTSQueue.enqueue === 'function') {
        try {
          window.PriorityTTSQueue.enqueue({
            text: task.text,
            priority: task.priority,
            onFinish: () => this._finish(task),
          });
          this._fallbackTimeout(task);
          return;
        } catch (e) {
          log('error', 'PriorityTTSQueue enqueue error', { e });
        }
      }

      // 最后使用 fallback speak 函数（老逻辑）
      if (this.fallbackSpeakFn) {
        try {
          const maybePromise = this.fallbackSpeakFn(task.text);
          if (maybePromise && typeof maybePromise.then === 'function') {
            maybePromise
              .then(() => this._finish(task))
              .catch((e) => {
                log('error', 'fallbackSpeakFn error', { e });
                this._finish(task);
              });
          } else {
            // 没有 promise，则设置一个大致时长
            this._fallbackTimeout(task, Math.max(1500, task.text.length * 80));
          }
          return;
        } catch (e) {
          log('error', 'fallbackSpeakFn call error', { e });
        }
      }

      // 如果什么都没有，直接结束
      this._finish(task);
    };

    AudioPipelineClass.prototype._fallbackTimeout = function (task, ms) {
      const timeout = typeof ms === 'number' ? ms : Math.max(2000, task.text.length * 80);
      const id = task.id;
      setTimeout(() => {
        if (this.currentTaskId === id) {
          log('warn', 'AudioPipeline timeout fallback', { id, timeout });
          this._finish(task);
        }
      }, timeout);
    };

    AudioPipelineClass.prototype._finish = function (task) {
      this.playing = false;
      this.currentTaskId = null;
      try {
        if (task.onDone) task.onDone();
      } catch (e) {
        log('error', 'AudioPipeline onDone error', { e });
      }
      this._drain();
    };

    window.AudioPipeline = new AudioPipelineClass();
  }

  // =========================
  // D2. Navigation FSM 导航状态机
  // =========================
  if (!window.NavigationFSM) {
    const NAV_STATE = {
      IDLE: 'IDLE',
      PREPARING: 'PREPARING',
      NAVIGATING: 'NAVIGATING',
      PAUSED: 'PAUSED',
      ARRIVED: 'ARRIVED',
      ERROR: 'ERROR',
    };

    function NavigationFSMClass() {
      this.state = NAV_STATE.IDLE;
      this.currentRoute = null; // { goalId, waypoints, currentIndex }
      this.lastUpdateTs = 0;
      this.hazardPaused = false;
    }

    NavigationFSMClass.prototype._setState = function (nextState, meta) {
      if (this.state === nextState) return;
      const prev = this.state;
      this.state = nextState;
      this.lastUpdateTs = Date.now();

      log('info', 'NavigationFSM state change', { from: prev, to: nextState, meta: meta || {} });

      // 对外发事件（给 taskChain / 其他模块）
      try {
        if (window.taskChain && window.taskChain.enqueue) {
          window.taskChain.enqueue({
            type: 'NAV_FSM_EVENT',
            priority: 'HIGH',
            payload: {
              from: prev,
              to: nextState,
              meta: meta || {},
              ts: this.lastUpdateTs,
            },
          });
        }
      } catch (e) {
        log('error', 'NavigationFSM emit NAV_FSM_EVENT error', { e });
      }
    };

    NavigationFSMClass.prototype.startNavigation = function (route) {
      if (!route || !Array.isArray(route.waypoints) || !route.waypoints.length) {
        log('warn', 'startNavigation invalid route', { route });
        this._setState(NAV_STATE.ERROR, { reason: 'invalid_route' });
        return;
      }

      this.currentRoute = {
        goalId: route.goalId || route.goal_id || 'unknown',
        waypoints: route.waypoints,
        currentIndex: 0,
      };
      this.hazardPaused = false;

      this._setState(NAV_STATE.PREPARING, { route: this.currentRoute });

      // 起始播报
      const text =
        route.startText ||
        '导航已启动，我会根据前方环境和路线，提醒你安全前进。';

      window.AudioPipeline.enqueue({
        text,
        priority: 2,
        category: 'nav',
        meta: { phase: 'nav_start' },
        onDone: () => {
          this._setState(NAV_STATE.NAVIGATING, {});
          this._speakNextWaypoint();
        },
      });
    };

    NavigationFSMClass.prototype._speakNextWaypoint = function () {
      if (!this.currentRoute) return;

      const idx = this.currentRoute.currentIndex;
      const wp = this.currentRoute.waypoints[idx];
      if (!wp) return;

      // 文案可以由后端给，也可以简单拼接
      const text =
        wp.text ||
        `接下来，请沿当前方向前进大约 ${wp.distance || '一小段'}，在 ${wp.landmark ||
          '前方'} 位置附近准备 ${wp.action || '转向' }。`;

      window.AudioPipeline.enqueue({
        text,
        priority: 4,
        category: 'nav',
        meta: { phase: 'waypoint', index: idx },
      });
    };

    // 由导航模块 / 后端调用，更新当前进度
    // navInfo 例子：{ goal_id, distance_to_goal_m, reached_waypoint: true, at_goal: false }
    NavigationFSMClass.prototype.updateProgress = function (navInfo) {
      this.lastUpdateTs = Date.now();

      if (!this.currentRoute) return;

      // 到达目标
      if (navInfo && navInfo.at_goal) {
        this._setState(NAV_STATE.ARRIVED, { navInfo });

        window.AudioPipeline.enqueue({
          text: '已经到达目标位置。',
          priority: 1,
          category: 'nav',
          meta: { phase: 'arrived' },
        });
        return;
      }

      // 路径点推进
      if (navInfo && navInfo.reached_waypoint && this.state === NAV_STATE.NAVIGATING) {
        const len = this.currentRoute.waypoints.length;
        if (this.currentRoute.currentIndex < len - 1) {
          this.currentRoute.currentIndex += 1;
          log('info', 'NavigationFSM waypoint advanced', {
            index: this.currentRoute.currentIndex,
            len,
          });
          this._speakNextWaypoint();
        }
      }
    };

    NavigationFSMClass.prototype.pause = function (reason) {
      if (this.state !== NAV_STATE.NAVIGATING) return;
      this._setState(NAV_STATE.PAUSED, { reason: reason || 'manual' });
    };

    NavigationFSMClass.prototype.resume = function () {
      if (this.state !== NAV_STATE.PAUSED) return;
      this._setState(NAV_STATE.NAVIGATING, { reason: 'resume' });
      this._speakNextWaypoint();
    };

    NavigationFSMClass.prototype.stop = function (reason) {
      this._setState(NAV_STATE.IDLE, { reason: reason || 'stop' });
      this.currentRoute = null;
      this.hazardPaused = false;
    };

    // 危险打断：来自 DangerEnginePro
    NavigationFSMClass.prototype.onHazard = function (hazardInfo) {
      if (!hazardInfo) return;

      log('warn', 'NavigationFSM onHazard', hazardInfo);

      if (this.state === NAV_STATE.NAVIGATING) {
        this.hazardPaused = true;
        this._setState(NAV_STATE.PAUSED, { reason: 'hazard', hazard: hazardInfo });
      }

      // 播报危险警告
      const text =
        hazardInfo.text ||
        '前方存在潜在危险，请放慢速度，注意脚下和周围环境。';

      window.AudioPipeline.enqueue({
        text,
        priority: 0, // 最高优先级
        category: 'danger',
        meta: { hazard: hazardInfo },
        onDone: () => {
          // 危险播报结束后尝试恢复导航
          if (this.hazardPaused && this.currentRoute) {
            this.hazardPaused = false;
            this._setState(NAV_STATE.NAVIGATING, { reason: 'hazard_cleared' });
            this._speakNextWaypoint();
          }
        },
      });
    };

    // =========================
    // 新增：handleEvent（兼容 EventFlow & EventFlowPro）
    // =========================
    NavigationFSMClass.prototype.handleEvent = function (evt) {
      if (!evt || !evt.type) return;

      // 1) Pro 版空间更新（来自 EventFlowPro）
      if (evt.type === 'space_update_enhanced') {
        const spaceState = evt.spaceState || {};
        const navInfo = spaceState.nav_info || spaceState.navInfo || null;

        // 如果空间状态里带有导航进度信息，就推进进度
        if (navInfo) {
          this.updateProgress(navInfo);
        }

        // 如果带有明显危险信息，转成 onHazard
        if (spaceState.primary_hazard &&
            (spaceState.overall_risk === 'high' || spaceState.overall_risk === 'critical')) {
          this.onHazard({
            type: spaceState.primary_hazard.type,
            distance_m: spaceState.primary_hazard.distance,
            risk: spaceState.overall_risk,
            text: null  // 文案交给上游
          });
        }

        return;
      }

      // 2) 旧版空间更新（来自 EventFlow）
      if (evt.type === 'space_update') {
        const spaceState = evt.spaceState || {};
        const navInfo = spaceState.nav_info || spaceState.navInfo || null;

        if (navInfo) {
          this.updateProgress(navInfo);
        }

        if (spaceState.primary_hazard &&
            (spaceState.overall_risk === 'high' || spaceState.overall_risk === 'critical')) {
          this.onHazard({
            type: spaceState.primary_hazard.type,
            distance_m: spaceState.primary_hazard.distance,
            risk: spaceState.overall_risk,
            text: null
          });
        }
        return;
      }

      // 3) 直接传进来 nav_progress 之类的事件
      if (evt.type === 'nav_progress' && evt.navInfo) {
        this.updateProgress(evt.navInfo);
        return;
      }

      // 其他类型先忽略，保留扩展点
      log('debug', 'NavigationFSM handleEvent unknown type', { type: evt.type });
    };

    window.NavigationFSM = new NavigationFSMClass();
    // 强制初始化检查
    if (!window.NavigationFSM.initialized) {
      window.NavigationFSM.initialized = true;
      window.NavigationFSM.state = window.NavigationFSM.state || "IDLE";
      console.log("✅ NavigationFSM 强制初始化完成 (Instance)");
    }
  }

  // =========================
  // D3. DangerEnginePro 多帧危险降噪
  // =========================
  if (!window.DangerEnginePro) {
    function DangerEngineProClass() {
      this.history = []; // 最近 N 帧检测
      this.maxFrames = 8;
      this.minStableFrames = 3;
      this.minConfidence = 0.65;
    }

    // detections 结构假设：[{ label, confidence, bbox: { x, y, w, h }, distance_m }]
    DangerEngineProClass.prototype.ingestFrame = function (detections, meta) {
      const ts = Date.now();
      this.history.push({ ts, detections: detections || [], meta: meta || {} });

      if (this.history.length > this.maxFrames) {
        this.history.shift();
      }

      // 输出危险结论
      return this._analyzeDanger();
    };

    DangerEngineProClass.prototype._analyzeDanger = function () {
      if (!this.history.length) return null;

      // 简单合并最近几帧的"高置信度 + 近距离"目标
      const merged = {};

      for (const frame of this.history) {
        for (const det of frame.detections) {
          if (!det || typeof det.confidence !== 'number') continue;
          if (det.confidence < this.minConfidence) continue;

          const key = det.label || 'unknown';
          if (!merged[key]) {
            merged[key] = { count: 0, closest: Infinity, last: det };
          }

          merged[key].count += 1;
          const d = typeof det.distance_m === 'number' ? det.distance_m : 999;
          if (d < merged[key].closest) merged[key].closest = d;
          merged[key].last = det;
        }
      }

      let best = null;
      for (const [label, info] of Object.entries(merged)) {
        if (info.count >= this.minStableFrames && info.closest < 2.0) {
          // 前方 2m 内且持续出现
          best = {
            label,
            frames: info.count,
            nearest_distance_m: info.closest,
            raw: info.last,
          };
          break;
        }
      }

      if (!best) return null;

      // 生成文案
      let text = '前方有障碍物，请放慢速度。';
      if (best.label === 'person') {
        text = '前方有人，请注意避让，放慢脚步。';
      } else if (best.label === 'bicycle' || best.label === 'bike') {
        text = '前方有自行车或障碍物，请稍微靠一侧行走。';
      } else if (best.label === 'stairs' || best.label === 'stair') {
        text = '前方疑似是楼梯区域，请放慢速度，注意台阶。';
      }

      const hazardInfo = {
        type: 'obstacle',
        label: best.label,
        distance_m: best.nearest_distance_m,
        frames: best.frames,
        text,
      };

      log('warn', 'DangerEnginePro hazard detected', hazardInfo);
      return hazardInfo;
    };

    window.DangerEnginePro = new DangerEngineProClass();
  }

  log('info', 'DE Navigation+Audio module initialized', {});
})();


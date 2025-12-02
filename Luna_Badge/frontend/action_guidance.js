// frontend/action_guidance.js
/**
 * ActionGuidance / 动作级导航引擎
 * 负责把"场景 + 通行性"转换为动作建议：adjust_left / adjust_right / keep_center / slow_down / stop 等
 */
(function () {
  'use strict';
  
  if (window.ActionGuidance) return;

  function logInfo(m, p) { window.logInfo?.('[ActionGuidance] ' + m, p ?? {}); }
  function logDebug(m, p) { window.logDebug?.('[ActionGuidance] ' + m, p ?? {}); }
  function logError(m, p) { window.logError?.('[ActionGuidance] ' + m, p ?? {}); }

  /**
   * ActionGuidance
   * 负责把"场景 + 通行性"转换为 动作建议：
   * adjust_left / adjust_right / keep_center / slow_down / stop 等。
   */
  function ActionGuidanceClass() {
    this.lastAction = null;
    this.lastActionTs = 0;
    this.cooldownMs = 1500; // 相同动作的最小间隔
  }

  ActionGuidanceClass.prototype._canEmitSameAction = function (code) {
    if (!this.lastAction || this.lastAction !== code) return true;
    const now = Date.now();
    return now - this.lastActionTs > this.cooldownMs;
  };

  ActionGuidanceClass.prototype._recordAction = function (code) {
    this.lastAction = code;
    this.lastActionTs = Date.now();
  };

  /**
   * 主入口：
   * @param {Object} sceneCtx  SceneReasoner.getLastContext()
   * @param {Object} pathHints PathFeasibility.analyze(...)
   * @param {Object} structInfo StructureAnalyzer.analyze(...)
   * @param {Object} topoInfo TopologyBuilder.build(...)
   * @param {Object} bottleInfo BottleneckDetector.detect(...)
   * @returns {Array<{code, urgency, text}>}
   */
  ActionGuidanceClass.prototype.deriveActions = function (
    sceneCtx,
    pathHints,
    structInfo,
    topoInfo,
    bottleInfo
  ) {
    try {
      const actions = [];

      if (!sceneCtx || !pathHints) return actions;

      const phase = sceneCtx.phase || 'idle';
      const navHints = sceneCtx.nav_hints || {};
      const bestSide = pathHints.best_side || navHints.preferred_side || 'center';
      const bottleneck = pathHints.bottleneck || bottleInfo?.bottleneck;
      const exitFound = bottleInfo?.exit;

      // 1) 狭窄 / 瓶颈 → 减速 + 微调
      if (bottleneck) {
        actions.push({
          code: 'slow_down',
          urgency: 'high',
          text: '前方通道较窄，请放慢速度，小心通过。'
        });
      }

      // 2) 侧向微调
      if (bestSide === 'left') {
        actions.push({
          code: 'adjust_left',
          urgency: 'medium',
          text: '请稍微向左侧偏一点，避开右侧障碍。'
        });
      } else if (bestSide === 'right') {
        actions.push({
          code: 'adjust_right',
          urgency: 'medium',
          text: '请稍微向右侧偏一点，避开左侧障碍。'
        });
      } else {
        // center：不强制说话，除非真需要
      }

      // 3) 楼梯场景
      if (sceneCtx.is_stair_zone || phase === 'approaching_stairs' || phase === 'at_stairs') {
        if (phase === 'approaching_stairs') {
          actions.push({
            code: 'prep_stairs',
            urgency: 'high',
            text: '前方是楼梯区域，请放慢脚步，注意台阶。'
          });
        } else if (phase === 'at_stairs') {
          actions.push({
            code: 'on_stairs',
            urgency: 'high',
            text: '已经到达楼梯位置，请慢慢行走，注意脚下。'
          });
        }
      }

      // 4) 出口提示
      if (exitFound) {
        actions.push({
          code: 'near_exit',
          urgency: 'low',
          text: '前方空间变宽，这是一个出口区域。'
        });
      }

      // 5) 拥挤场景
      const crowd = sceneCtx.topology?.crowd_density;
      if (typeof crowd === 'number' && crowd > 1.5) {
        actions.push({
          code: 'crowded',
          urgency: 'high',
          text: '前方行人较多，请放慢速度，注意避让。'
        });
      }

      // 动作去重 + 冷却
      const filtered = [];
      for (const a of actions) {
        if (!this._canEmitSameAction(a.code)) continue;
        this._recordAction(a.code);
        filtered.push(a);
      }

      logDebug('deriveActions', {
        phase,
        bestSide,
        bottleneck,
        exitFound,
        crowd,
        actions: filtered
      });

      return filtered;
    } catch (e) {
      logError('deriveActions error', { e });
      return [];
    }
  };

  /**
   * 把动作转成 NAV_HINT 任务并交给 SpeechRhythm
   */
  ActionGuidanceClass.prototype.dispatch = function (actions) {
    if (!actions || !actions.length) return;

    for (const a of actions) {
      const task = {
        type: 'NAV_HINT',
        payload: { text: a.text, code: a.code, urgency: a.urgency || 'medium' }
      };

      // ✅ 优先通过 MemoryAwareVoice
      if (window.MemoryAwareVoice && typeof window.MemoryAwareVoice.handleTask === 'function') {
        window.MemoryAwareVoice.handleTask(task);
      } else if (window.SpeechRhythm && typeof window.SpeechRhythm.handleTask === 'function') {
        window.SpeechRhythm.handleTask(task);
      }
    }
  };

  window.ActionGuidance = new ActionGuidanceClass();

  if (window.logInfo) {
    window.logInfo('ActionGuidance模块加载完成', { module: 'action_guidance' });
  } else {
    console.log('✅ ActionGuidance模块加载完成', { module: 'action_guidance' });
  }
})();


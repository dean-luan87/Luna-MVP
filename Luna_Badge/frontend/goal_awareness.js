// frontend/goal_awareness.js
/**
 * GoalAwareness / 目标距离 × 阶段播报引擎
 * 用于："距离目标还有 50 米 / 20 米 / 5 米 / 已到达"
 * 支持楼层/建筑/科室多阶段
 * 不依赖地图细节，由后端传入高层导航状态
 */
(function () {
  'use strict';
  
  if (window.GoalAwareness) return;

  function logInfo(m, p) { window.logInfo?.('[GoalAwareness] ' + m, p ?? {}); }
  function logDebug(m, p) { window.logDebug?.('[GoalAwareness] ' + m, p ?? {}); }
  function logError(m, p) { window.logError?.('[GoalAwareness] ' + m, p ?? {}); }

  const DIST_MILESTONES = [50, 30, 20, 10, 5]; // 米
  const STAGES = [
    'outdoor_to_building',
    'in_building',
    'in_elevator',
    'on_floor',
    'at_goal'
  ];

  function GoalAwarenessClass() {
    this.currentGoalId = null;
    this.lastMilestoneIndex = null;
    this.stageAnnounced = {};
  }

  GoalAwarenessClass.prototype._resetForGoal = function (goalId) {
    this.currentGoalId = goalId;
    this.lastMilestoneIndex = null;
    this.stageAnnounced = {};
  };

  GoalAwarenessClass.prototype._pickMilestoneIndex = function (dist) {
    for (let i = 0; i < DIST_MILESTONES.length; i++) {
      if (dist <= DIST_MILESTONES[i]) return i;
    }
    return null;
  };

  GoalAwarenessClass.prototype._buildDistText = function (dist) {
    if (dist <= 3) return '马上就要到了。';
    if (dist <= 5) return '还有五米左右。';
    if (dist <= 10) return '还有十米左右。';
    if (dist <= 20) return '还有二十米左右。';
    if (dist <= 50) return '还有五十米左右。';
    return '';
  };

  GoalAwarenessClass.prototype._buildStageText = function (stage) {
    if (stage === 'outdoor_to_building') return '正在前往目标建筑。';
    if (stage === 'in_building') return '已经进入建筑内部，继续按照指引前进。';
    if (stage === 'in_elevator') return '已进入电梯，请根据楼层提示选择目标楼层。';
    if (stage === 'on_floor') return '已经在目标楼层附近，马上就要到达目的地。';
    if (stage === 'at_goal') return '已经到达目标位置。';
    return '';
  };

  /**
   * 后端每次导航状态更新时调用
   * @param {Object} navInfo
   *   - goal_id
   *   - distance_to_goal_m
   *   - eta_sec
   *   - stage
   *   - segment_index
   *   - segment_count
   */
  GoalAwarenessClass.prototype.update = function (navInfo) {
    try {
      if (!navInfo?.goal_id) return;

      if (navInfo.goal_id !== this.currentGoalId) {
        this._resetForGoal(navInfo.goal_id);
        logInfo('new goal', { goal_id: navInfo.goal_id });
      }

      const dist = navInfo.distance_to_goal_m;
      if (typeof dist !== 'number') return;

      const stage = navInfo.stage || 'unknown';
      const stageText = this._buildStageText(stage);

      // 1) 阶段播报（每阶段只说一次）
      if (stageText && !this.stageAnnounced[stage]) {
        this.stageAnnounced[stage] = true;
        this._speak(stageText, 'nav');
      }

      // 2) 距离里程碑播报
      const idx = this._pickMilestoneIndex(dist);
      if (idx === null) return;

      if (this.lastMilestoneIndex === null || idx < this.lastMilestoneIndex) {
        // 里程碑从大到小递进
        this.lastMilestoneIndex = idx;
        const text = this._buildDistText(dist);
        if (text) this._speak(text, 'nav');
      }

      // 3) 到达目标
      if (stage === 'at_goal') {
        this._speak('您已经到达目标位置。', 'nav');
      }
    } catch (e) {
      logError('update error', { e });
    }
  };

  GoalAwarenessClass.prototype._speak = function (text, category) {
    if (!text) return;
    const task = {
      type: 'NAV_HINT',
      payload: { text, code: 'goal_update' }
    };

    // 首选记忆敏感语音层
    if (window.MemoryAwareVoice && typeof window.MemoryAwareVoice.handleTask === 'function') {
      window.MemoryAwareVoice.handleTask(task);
      return;
    }
    if (window.SpeechRhythm && typeof window.SpeechRhythm.handleTask === 'function') {
      window.SpeechRhythm.handleTask(task);
      return;
    }
  };

  window.GoalAwareness = new GoalAwarenessClass();

  if (window.logInfo) {
    window.logInfo('GoalAwareness模块加载完成', { module: 'goal_awareness' });
  } else {
    console.log('✅ GoalAwareness模块加载完成', { module: 'goal_awareness' });
  }
})();


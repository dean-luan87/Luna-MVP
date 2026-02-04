// frontend/navigation_task_executors.js
// 导航任务执行器：将导航 Step 转换为语音/UI/日志

(function () {
  'use strict';

  if (window.NavigationTaskExecutors) return;

  function log(event, payload) {
    if (window.__lunaLog) {
      window.__lunaLog(event, payload);
    } else if (window.logInfo) {
      window.logInfo(`[NavExecutors] ${event}`, payload || {});
    }
  }

  function speakText(text, style = 'calm', priority = false) {
    if (window.speakText) {
      window.speakText(text, style, priority);
    } else if (window.enqueueTTS) {
      window.enqueueTTS(text, { style, priority });
    }
  }

  /**
   * 导航任务执行器注册表
   */
  window.NavigationTaskExecutors = {
    /**
     * NAV_START: 导航开始
     */
    "NAV_START": async (step) => {
      const { route, eta, distance } = step.payload || {};
      const etaText = eta ? `预计需要 ${eta} 分钟` : '';
      const distText = distance ? `，距离 ${distance} 米` : '';
      const message = `路线规划完成${distText}${etaText}。`;
      
      // ✅ 记录执行器日志
      if (window.NavLog) {
        window.NavLog.info("Executor", "执行 NAV_START", { route, eta, distance, message });
      }
      
      log('nav_start', { route, eta, distance });
      speakText(message, 'cheerful', false);
      
      if (window.NavigationFSM && typeof window.NavigationFSM.start === 'function') {
        window.NavigationFSM.start({ route, destination: route?.goalId || route?.to });
      }
    },

    /**
     * NAV_TURN: 转弯指令
     */
    "NAV_TURN": async (step) => {
      const { direction, distance } = step.payload || {};
      let message = '';
      
      if (direction === 'left') {
        message = distance ? `请在前方 ${distance} 米左转` : '请在前方左转';
      } else if (direction === 'right') {
        message = distance ? `请在前方 ${distance} 米右转` : '请在前方右转';
      } else if (direction === 'u-turn' || direction === 'uturn') {
        message = distance ? `请在前方 ${distance} 米掉头` : '请在前方掉头';
      } else {
        message = '请按提示行进';
      }
      
      // ✅ 记录执行器日志
      if (window.NavLog) {
        window.NavLog.info("Executor", "执行 NAV_TURN", { direction, distance, message });
      }
      
      log('nav_turn', { direction, distance });
      speakText(message, 'cheerful', true);
    },

    /**
     * NAV_STRAIGHT: 直行播报
     */
    "NAV_STRAIGHT": async (step) => {
      const { distance } = step.payload || {};
      const message = distance ? `请直行 ${distance} 米` : '请继续直行';
      
      // ✅ 记录执行器日志
      if (window.NavLog) {
        window.NavLog.info("Executor", "执行 NAV_STRAIGHT", { distance, message });
      }
      
      log('nav_straight', { distance });
      speakText(message, 'calm', false);
    },

    /**
     * NAV_POI: 关键节点（医院入口、商场门口等）
     */
    "NAV_POI": async (step) => {
      const { name, type } = step.payload || {};
      const message = name ? `您已到达 ${name}` : (type ? `您已到达 ${type}` : '您已到达关键节点');
      
      // ✅ 记录执行器日志
      if (window.NavLog) {
        window.NavLog.info("Executor", "执行 NAV_POI", { name, type, message });
      }
      
      log('nav_poi', { name, type });
      speakText(message, 'cheerful', false);
    },

    /**
     * NAV_END: 到达终点
     */
    "NAV_END": async (step) => {
      const { destination } = step.payload || {};
      const message = destination ? `已到达 ${destination}` : '已到达目的地';
      
      // ✅ 记录执行器日志
      if (window.NavLog) {
        window.NavLog.info("Executor", "执行 NAV_END", { destination, message });
      }
      
      log('nav_end', { destination });
      speakText(message, 'cheerful', true);
      
      if (window.NavigationFSM && typeof window.NavigationFSM.finish === 'function') {
        window.NavigationFSM.finish({ destination });
      }
    },

    /**
     * NAV_ERROR: 导航失败
     */
    "NAV_ERROR": async (step) => {
      const { reason, code } = step.payload || {};
      const message = reason ? `导航出错：${reason}` : '导航出现错误，请重新规划路线';
      
      // ✅ 记录执行器错误日志
      if (window.NavLog) {
        window.NavLog.error("Executor", "执行 NAV_ERROR", { reason, code, message });
      }
      
      log('nav_error', { reason, code });
      speakText(message, 'urgent', true);
      
      if (window.NavigationFSM && typeof window.NavigationFSM.reset === 'function') {
        window.NavigationFSM.reset({ reason: reason || 'error' });
      }
    }
  };

  console.log('✅ NavigationTaskExecutors 初始化完成', { module: 'navigation_executors' });
})();


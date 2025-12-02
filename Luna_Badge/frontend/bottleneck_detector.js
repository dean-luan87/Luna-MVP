// frontend/bottleneck_detector.js
/**
 * BottleneckDetector / 瓶颈检测器
 * 判断是否进入拥挤区、出口通道、狭窄口
 * 输出：bottleneck / wide / narrow / exit
 */
(function () {
  'use strict';
  
  if (window.BottleneckDetector) return;

  function logDebug(msg, p) { window.logDebug?.('[BottleneckDetector] ' + msg, p || {}); }
  function logError(msg, p) { window.logError?.('[BottleneckDetector] ' + msg, p || {}); }

  function BottleneckDetectorClass() {}

  /**
   * 输入：StructureAnalyzer + TopologyBuilder
   * 输出：瓶颈、出口发现
   */
  BottleneckDetectorClass.prototype.detect = function (structureInfo, topologyInfo) {
    try {
      if (!structureInfo || !topologyInfo) return null;

      const isBottleneck =
        structureInfo.is_narrow ||
        (topologyInfo.left_blocked && topologyInfo.right_blocked);

      const isExit =
        structureInfo.is_wide && !topologyInfo.left_blocked && !topologyInfo.right_blocked;

      const result = {
        bottleneck: isBottleneck,
        exit: isExit,
        hint: isBottleneck
          ? 'bottleneck'
          : isExit
          ? 'exit_found'
          : 'normal'
      };

      logDebug('detect result', result);
      return result;
    } catch (e) {
      logError('detect error', e);
      return null;
    }
  };

  window.BottleneckDetector = new BottleneckDetectorClass();

  if (window.logInfo) {
    window.logInfo('BottleneckDetector模块加载完成', { module: 'bottleneck_detector' });
  } else {
    console.log('✅ BottleneckDetector模块加载完成', { module: 'bottleneck_detector' });
  }
})();


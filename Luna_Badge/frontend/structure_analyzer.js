// frontend/structure_analyzer.js
/**
 * StructureAnalyzer / 结构分析器
 * 提取走廊边线、墙、柱子、台阶、坡道、宽度变化
 * 输出结构特征（走廊/开阔/狭窄/出口/弯道）
 */
(function () {
  'use strict';
  
  if (window.StructureAnalyzer) return;

  function logDebug(msg, p) { window.logDebug?.('[StructureAnalyzer] ' + msg, p || {}); }
  function logError(msg, p) { window.logError?.('[StructureAnalyzer] ' + msg, p || {}); }

  /**
   * StructureAnalyzer
   * 输入：enhancedState.pointGrid（BEV 投影点）
   * 输出：结构特征：左右墙、宽度、走廊感、坡度、台阶等
   */
  function StructureAnalyzerClass() {}

  StructureAnalyzerClass.prototype.analyze = function (enhancedState) {
    try {
      if (!enhancedState?.pointGrid) return null;

      const pts = enhancedState.pointGrid;
      const width = enhancedState.grid?.width_m ?? 4.0;

      let leftMin = 999, rightMin = 999;
      let leftHasWall = false, rightHasWall = false;

      let verticalCluster = 0;   // 是否形成"走廊线"
      let centerOpen = 0;

      let hasStair = false;
      let hasSlope = false;

      for (const p of pts) {
        if (p.y < 0.3 || p.y > 5.0) continue;

        // 楼梯识别
        if (p.type?.includes('stair')) hasStair = true;

        // 斜坡（高度变化）
        if (typeof p.slope === 'number' && Math.abs(p.slope) > 0.15)
          hasSlope = true;

        // 左右距中心的偏移
        if (p.x < 0) {
          leftMin = Math.min(leftMin, Math.abs(p.x));
          if (Math.abs(p.x) < 0.3) leftHasWall = true;
        } else {
          rightMin = Math.min(rightMin, Math.abs(p.x));
          if (Math.abs(p.x) < 0.3) rightHasWall = true;
        }

        // 走廊线：沿 y 方向延伸且 x 稳定
        if (Math.abs(p.x) < 0.5) verticalCluster++;
        if (Math.abs(p.x) < 0.3) centerOpen++;
      }

      const corridorScore = verticalCluster / pts.length;
      const isCorridor = corridorScore > 0.25;
      const isNarrow = leftMin + rightMin < 1.2;
      const isWide = leftMin + rightMin > 3.0;

      const result = {
        left_wall: leftHasWall,
        right_wall: rightHasWall,
        left_distance: leftMin,
        right_distance: rightMin,
        corridor_score: corridorScore,
        is_corridor: isCorridor,
        is_narrow: isNarrow,
        is_wide: isWide,
        has_stair: hasStair,
        has_slope: hasSlope
      };

      logDebug('analyze result', result);
      return result;
    } catch (e) {
      logError('Analyze error', e);
      return null;
    }
  };

  window.StructureAnalyzer = new StructureAnalyzerClass();

  if (window.logInfo) {
    window.logInfo('StructureAnalyzer模块加载完成', { module: 'structure_analyzer' });
  } else {
    console.log('✅ StructureAnalyzer模块加载完成', { module: 'structure_analyzer' });
  }
})();


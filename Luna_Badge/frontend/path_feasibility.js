// frontend/path_feasibility.js
/**
 * PathFeasibility / 路径可行性评估
 * 左/中/右路径可行性评估 + 结合结构记忆
 */
(function () {
  'use strict';
  
  if (window.PathFeasibility) return;

  function logDebug(m, p) { window.logDebug?.('[PathFeasibility] ' + m, p ?? {}); }
  function logError(m, p) { window.logError?.('[PathFeasibility] ' + m, p ?? {}); }

  function PF() {
    this.last = null;
  }

  PF.prototype.analyze = function (enhancedState, structureSnapshot) {
    try {
      if (!enhancedState?.pointGrid) return null;

      const pts = enhancedState.pointGrid;
      const width = enhancedState.grid?.width_m ?? 4.0;
      const centerHalf = (width * 0.4) / 2;

      let L = 0, C = 0, R = 0;
      let leftCount = 0, centerCount = 0, rightCount = 0;

      for (const p of pts) {
        if (p.y < 0.5 || p.y > 4.0) continue;

        const zone =
          Math.abs(p.x) <= centerHalf ? 'C' : p.x < 0 ? 'L' : 'R';

        const level = p.risk_level || 'low';
        let base =
          level === 'critical' ? 3 :
          level === 'high' ? 2 :
          level === 'medium' ? 1 : 0;

        const dist = Math.max(p.distance ?? p.y, 0.1);
        const score = base * (1 / dist);

        if (zone === 'L') { L += score; leftCount++; }
        else if (zone === 'C') { C += score; centerCount++; }
        else { R += score; rightCount++; }
      }

      if (structureSnapshot?.leftWallStable) L *= 1.1;
      if (structureSnapshot?.rightWallStable) R *= 1.1;

      const passL = L < 3.0;
      const passC = C < 3.0;
      const passR = R < 3.0;

      let best = 'center';
      let bestScore = passC ? C : Infinity;

      if (passL && L < bestScore) { bestScore = L; best = 'left'; }
      if (passR && R < bestScore) { bestScore = R; best = 'right'; }

      const result = {
        left_passable: passL,
        center_passable: passC,
        right_passable: passR,
        left_block_score: L,
        center_block_score: C,
        right_block_score: R,
        best_side: best,
        bottleneck: !passL && !passC && !passR
      };

      this.last = result;
      logDebug('result', result);
      return result;
    } catch (err) {
      logError('analyze error', err);
      return null;
    }
  };

  PF.prototype.getLast = function () {
    return this.last;
  };

  window.PathFeasibility = new PF();

  if (window.logInfo) {
    window.logInfo('PathFeasibility模块加载完成', { module: 'path_feasibility' });
  } else {
    console.log('✅ PathFeasibility模块加载完成', { module: 'path_feasibility' });
  }
})();


// frontend/spatial_semantic.js
/**
 * SpatialSemantic / 空间语义化
 * 把"位置 + 当下环境"转成中文句子
 */
(function () {
  'use strict';
  
  if (window.SpatialSemantic) return;

  function logDebug(msg, payload) {
    if (window.logDebug) window.logDebug('[SpatialSemantic] ' + msg, payload || {});
    else console.debug('[SpatialSemantic]', msg, payload || {});
  }

  function logError(msg, payload) {
    if (window.logError) window.logError('[SpatialSemantic] ' + msg, payload || {});
    else console.error('[SpatialSemantic]', msg, payload || {});
  }

  function describeDirection(bearingDeg, bevX) {
    if (typeof bearingDeg !== 'number') {
      if (typeof bevX === 'number') {
        if (bevX < -0.5) return '左侧';
        if (bevX > 0.5) return '右侧';
      }
      return '前方';
    }

    let a = ((bearingDeg % 360) + 360) % 360;
    if (a > 180) a -= 360;

    if (a > -20 && a <= 20) return '正前方';
    if (a > 20 && a <= 70) return '右前方';
    if (a > 70 && a <= 140) return '右侧';
    if (a <= -20 && a > -70) return '左前方';
    if (a <= -70 && a > -140) return '左侧';
    return '前方';
  }

  function describeDistance(d) {
    if (typeof d !== 'number') return '';
    if (d < 0.7) return '就在身边';
    if (d < 1.5) return '一米左右';
    if (d < 3.0) return '两三米';
    if (d < 6.0) return '几米之外';
    return '稍远处';
  }

  function normalizeTypeLabel(t) {
    if (!t) return '障碍物';
    const s = String(t).toLowerCase();
    if (s.includes('stair') || s.includes('steps')) return '台阶';
    if (s.includes('person') || s.includes('human')) return '行人';
    if (s.includes('car') || s.includes('truck') || s.includes('bus')) return '车辆';
    if (s.includes('door')) return '门口';
    if (s.includes('elevator')) return '电梯';
    if (s.includes('bike')) return '自行车';
    return '障碍物';
  }

  function riskPrefix(level) {
    if (level === 'critical') return '危险！';
    if (level === 'high') return '注意，前方有风险，';
    if (level === 'medium') return '请注意，';
    return '';
  }

  window.SpatialSemantic = {
    buildHazardText(hazard, enhancedState) {
      try {
        if (!hazard) return '';

        const distance = hazard.distance ?? hazard.pro_distance;
        const bearing = hazard.bearing;
        const bevX = hazard.bev?.x;

        const dirText = describeDirection(bearing, bevX);
        const distText = describeDistance(distance);
        const typeText = normalizeTypeLabel(hazard.type || hazard.label);
        const risk = enhancedState?.overall_risk || hazard.risk_level || 'medium';

        return `${riskPrefix(risk)}${dirText}${distText}有${typeText}`;
      } catch (e) {
        logError('buildHazardText error', { e });
        return '';
      }
    },

    buildNavHintText(sceneCtx, pathHints) {
      try {
        if (!sceneCtx && !pathHints) return '';

        let txt = '';
        const side = pathHints?.best_side;
        const slow = pathHints?.bottleneck || sceneCtx?.topology?.crowd_density > 1.5;

        if (side === 'left') txt += '请稍微向左侧行走，避开右侧人群。';
        else if (side === 'right') txt += '请稍微向右侧行走，避开左侧人群。';

        if (slow) txt += ' 前方环境复杂，请放慢速度。';

        return txt;
      } catch (e) {
        logError('buildNavHintText error', { e });
        return '';
      }
    },

    buildSceneOverviewText(sceneCtx) {
      try {
        if (!sceneCtx) return '';

        const t = sceneCtx.inferred_scene_type || '';
        const crowd = sceneCtx.topology?.crowd_density;

        let txt = '';

        if (t.includes('stair')) txt += '当前处在楼梯附近。';
        else if (t.includes('corridor')) txt += '当前在走廊中。';
        else if (t.includes('street')) txt += '当前在街道上。';

        if (crowd > 1.5) txt += ' 前方人较多。';

        return txt;
      } catch (e) {
        logError('buildSceneOverviewText error', { e });
        return '';
      }
    }
  };

  if (window.logInfo) {
    window.logInfo('SpatialSemantic模块加载完成', { module: 'spatial_semantic' });
  } else {
    console.log('✅ SpatialSemantic模块加载完成', { module: 'spatial_semantic' });
  }
})();


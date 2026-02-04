// frontend/spatial_engine_pro.js
/**
 * SpatialEnginePro / 空间引擎 Pro 版
 * 基于现有 spaceState 做增强：伪深度、接近速度、简单运动向量 + pointGrid
 * 
 * 输入：spaceState（来自 SpaceEngine）
 * 输出：enhancedState（交给 EventFlowPro / 导航 / 记忆Pro）
 */
(function () {
  'use strict';
  
  if (window.SpatialEnginePro) return;

  function logDebug(msg, payload) {
    if (window.logDebug) window.logDebug(msg, payload);
    else console.debug('[SpatialEnginePro]', msg, payload || '');
  }

  function logError(msg, payload) {
    if (window.logError) window.logError(msg, payload);
    else console.error('[SpatialEnginePro]', msg, payload || '');
  }

  function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
  }

  /**
   * SpatialEngineProClass：空间引擎 Pro 版主类
   * 简单的运动估计：用历史空间状态里的同一 trackId 做差分
   */
  class SpatialEngineProClass {
    constructor() {
      this.lastObjectsById = {}; // trackId -> { ts, distance, bearing, bev_x, bev_y }
      this.lastEnhancedState = null;
    }

    /**
     * 主入口：由 EventFlow.onSpaceState 调用
     * @param {Object} spaceState 原始SpaceEngine输出
     * @returns {Object|null} enhancedState
     */
    ingestSpaceState(spaceState) {
      try {
        if (!spaceState || !spaceState.objects) {
          return null;
        }

        const now = Date.now();
        const objects = spaceState.objects || [];
        const enhancedObjects = [];
        const pointGrid = [];

        for (let i = 0; i < objects.length; i++) {
          const obj = objects[i];
          const trackId = obj.trackId || ('obj_' + i);
          const geom = {
            distance: obj.distance,
            bearing: obj.bearing,
            bev_x: obj.bev && typeof obj.bev.x === 'number' ? obj.bev.x : null,
            bev_y: obj.bev && typeof obj.bev.y === 'number' ? obj.bev.y : null
          };

          const history = this.lastObjectsById[trackId];
          let approachSpeed = 0; // m/s，正数表示靠近
          let lateralSpeed = 0;  // m/s，正数表示向右

          if (history && typeof history.distance === 'number' && typeof geom.distance === 'number') {
            const dtSec = (now - history.ts) / 1000.0;
            if (dtSec > 0.01 && dtSec < 2.0) {
              approachSpeed = (history.distance - geom.distance) / dtSec;
              if (typeof history.bev_x === 'number' && typeof geom.bev_x === 'number') {
                lateralSpeed = (geom.bev_x - history.bev_x) / dtSec;
              }
            }
          }

          this.lastObjectsById[trackId] = {
            ts: now,
            distance: geom.distance,
            bearing: geom.bearing,
            bev_x: geom.bev_x,
            bev_y: geom.bev_y
          };

          // 运动趋势基本判断
          let motionPro = 'static';
          if (approachSpeed > 0.2) motionPro = 'approaching_fast';
          else if (approachSpeed > 0.05) motionPro = 'approaching';
          else if (approachSpeed < -0.2) motionPro = 'leaving_fast';
          else if (approachSpeed < -0.05) motionPro = 'leaving';
          else if (Math.abs(lateralSpeed) > 0.2) motionPro = 'crossing';

          const enhancedObj = Object.assign({}, obj, {
            pro_motion: motionPro,
            pro_approach_speed: approachSpeed, // m/s
            pro_lateral_speed: lateralSpeed    // m/s
          });
          enhancedObjects.push(enhancedObj);

          // pointGrid 点云增强
          if (geom.bev_x !== null && geom.bev_y !== null && typeof geom.distance === 'number') {
            pointGrid.push({
              x: geom.bev_x,
              y: geom.bev_y,
              distance: geom.distance,
              type: obj.type || obj.label || 'unknown',
              risk_level: obj.risk_level || 'low',
              trackId: trackId,
              pro_motion: motionPro,
              pro_approach_speed: approachSpeed,
              pro_lateral_speed: lateralSpeed
            });
          }
        }

        const enhancedState = Object.assign({}, spaceState, {
          objects: enhancedObjects,
          pointGrid: pointGrid
        });

        this.lastEnhancedState = enhancedState;
        logDebug('SpatialEnginePro.enhancedState', {
          scene_type: enhancedState.scene_type,
          object_count: enhancedObjects.length,
          point_count: pointGrid.length
        });

        // 分发给 Pro 版事件流优先，否则回落到普通 EventFlow
        if (window.EventFlowPro && typeof window.EventFlowPro.onSpaceStateEnhanced === 'function') {
          window.EventFlowPro.onSpaceStateEnhanced(enhancedState);
        } else if (window.EventFlow && typeof window.EventFlow.onSpaceState === 'function') {
          // 回落逻辑：用增强后的状态代替原来状态
          window.EventFlow.onSpaceState(enhancedState);
        }

        return enhancedState;
      } catch (e) {
        logError('SpatialEnginePro.ingestSpaceState error', {
          error: e.toString(),
          stack: e.stack
        });
        return null;
      }
    }

    getLastEnhancedState() {
      return this.lastEnhancedState;
    }
  }

  window.SpatialEnginePro = new SpatialEngineProClass();

  // 提供一个全局便捷函数：原来的 EventFlow.onSpaceState 可以改成调用这里
  window.ingestSpaceStatePro = function (spaceState) {
    if (!window.SpatialEnginePro) return null;
    return window.SpatialEnginePro.ingestSpaceState(spaceState);
  };

  if (window.logInfo) {
    window.logInfo('SpatialEnginePro模块加载完成', { module: 'spatial_engine_pro' });
  } else {
    console.log('✅ SpatialEnginePro模块加载完成', { module: 'spatial_engine_pro' });
  }
})();


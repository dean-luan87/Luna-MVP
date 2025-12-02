// frontend/map_memory_pro.js
/**
 * MapMemoryPro / 地图记忆 Pro 版
 * 在已有 MapMemory 之上，再加一个 Pro 版（结构记忆 / 区域记忆 / 时间维度）
 * 
 * 输入：enhancedState（来自 SpatialEnginePro）
 * 输出：结构化 placeStructure + 记忆追踪日志
 */
(function () {
  'use strict';
  
  if (window.MapMemoryPro) return;

  function logInfo(msg, payload) {
    if (window.logInfo) window.logInfo(msg, payload);
    else console.log('[MapMemoryPro]', msg, payload || '');
  }

  function logDebug(msg, payload) {
    if (window.logDebug) window.logDebug(msg, payload);
    else console.debug('[MapMemoryPro]', msg, payload || '');
  }

  function logError(msg, payload) {
    if (window.logError) window.logError(msg, payload);
    else console.error('[MapMemoryPro]', msg, payload || '');
  }

  const STATIC_TYPES = ['stairs', 'staircase', 'pillar', 'wall', 'door'];
  const CENTER_ZONE_RATIO = 0.4; // 中央行进区域宽度占整宽比例

  /**
   * ZoneStats：区域统计
   */
  class ZoneStats {
    constructor(name) {
      this.name = name;
      this.sampleCount = 0;
      this.staticHazards = 0;
      this.dynamicObjects = 0;
      this.avgWidthM = null;
    }

    addSample(sample) {
      this.sampleCount += 1;
      if (sample.isStaticHazard) this.staticHazards += 1;
      if (sample.isDynamic) this.dynamicObjects += 1;
      if (typeof sample.localWidthM === 'number') {
        if (this.avgWidthM == null) this.avgWidthM = sample.localWidthM;
        else this.avgWidthM = this.avgWidthM * 0.9 + sample.localWidthM * 0.1;
      }
    }
  }

  /**
   * PlaceStructure：地点结构（Pro 版）
   */
  class PlaceStructure {
    constructor(placeId) {
      this.placeId = placeId;
      this.lastUpdateTs = Date.now();
      this.sceneTypes = {};
      this.corridorWidthM = null;
      this.leftWallStable = false;
      this.rightWallStable = false;
      this.leftSideStaticCount = 0;
      this.rightSideStaticCount = 0;
      this.centerZone = new ZoneStats('center');
      this.leftZone = new ZoneStats('left');
      this.rightZone = new ZoneStats('right');
    }

    updateFromEnhancedState(enhancedState) {
      this.lastUpdateTs = Date.now();
      const st = enhancedState.scene_type || 'unknown';
      this.sceneTypes[st] = (this.sceneTypes[st] || 0) + 1;

      const grid = enhancedState.grid;
      const widthM = grid && typeof grid.width_m === 'number' ? grid.width_m : 4.0;

      const objects = enhancedState.objects || [];
      for (let i = 0; i < objects.length; i++) {
        const obj = objects[i];
        const bev = obj.bev || {};
        const x = typeof bev.x === 'number' ? bev.x : null;
        const y = typeof bev.y === 'number' ? bev.y : null;
        if (x === null || y === null) continue;

        const type = (obj.type || obj.label || '').toLowerCase();
        const isStaticLike = STATIC_TYPES.some(t => type.indexOf(t) !== -1);
        const isStaticHazard = !!(obj.memory && obj.memory.is_static_hazard);
        const isDynamic =
          obj.pro_motion === 'approaching' ||
          obj.pro_motion === 'approaching_fast' ||
          obj.pro_motion === 'leaving' ||
          obj.pro_motion === 'leaving_fast' ||
          obj.pro_motion === 'crossing';

        const isLeft = x < 0;
        const isCenter = Math.abs(x) <= (widthM * CENTER_ZONE_RATIO / 2);

        const localWidth = widthM; // 简化：用当前grid宽作为局部宽度估计

        const sample = {
          isStaticHazard: isStaticHazard || isStaticLike,
          isDynamic: isDynamic,
          localWidthM: localWidth
        };

        if (isCenter) this.centerZone.addSample(sample);
        else if (isLeft) {
          this.leftZone.addSample(sample);
          if (sample.isStaticHazard) this.leftSideStaticCount += 1;
        } else {
          this.rightZone.addSample(sample);
          if (sample.isStaticHazard) this.rightSideStaticCount += 1;
        }
      }

      // 粗略判断走廊宽度
      if (this.centerZone.avgWidthM != null) {
        if (this.corridorWidthM == null) {
          this.corridorWidthM = this.centerZone.avgWidthM;
        } else {
          this.corridorWidthM =
            this.corridorWidthM * 0.9 + this.centerZone.avgWidthM * 0.1;
        }
      }

      // 左右墙稳定判断：静态结构次数达到一定数量
      this.leftWallStable = this.leftSideStaticCount >= 20;
      this.rightWallStable = this.rightSideStaticCount >= 20;
    }

    getSnapshot() {
      return {
        placeId: this.placeId,
        updated_at: this.lastUpdateTs,
        sceneTypes: this.sceneTypes,
        corridorWidthM: this.corridorWidthM,
        leftWallStable: this.leftWallStable,
        rightWallStable: this.rightWallStable,
        centerZone: {
          sampleCount: this.centerZone.sampleCount,
          staticHazards: this.centerZone.staticHazards,
          dynamicObjects: this.centerZone.dynamicObjects,
          avgWidthM: this.centerZone.avgWidthM
        },
        leftZone: {
          sampleCount: this.leftZone.sampleCount,
          staticHazards: this.leftZone.staticHazards,
          dynamicObjects: this.leftZone.dynamicObjects,
          avgWidthM: this.leftZone.avgWidthM
        },
        rightZone: {
          sampleCount: this.rightZone.sampleCount,
          staticHazards: this.rightZone.staticHazards,
          dynamicObjects: this.rightZone.dynamicObjects,
          avgWidthM: this.rightZone.avgWidthM
        }
      };
    }
  }

  /**
   * MapMemoryProClass：地图记忆 Pro 版主类
   */
  class MapMemoryProClass {
    constructor() {
      this.places = {}; // placeId -> PlaceStructure
      this.currentPlaceId = 'session_default';
      this.lastTraceId = 0;
    }

    _allocTraceId() {
      this.lastTraceId += 1;
      return 'mmtrace_' + this.lastTraceId;
    }

    getCurrentPlaceStructure() {
      if (!this.places[this.currentPlaceId]) {
        this.places[this.currentPlaceId] = new PlaceStructure(this.currentPlaceId);
      }
      return this.places[this.currentPlaceId];
    }

    setCurrentPlaceId(placeId) {
      if (!placeId) return;
      this.currentPlaceId = placeId;
      if (!this.places[placeId]) {
        this.places[placeId] = new PlaceStructure(placeId);
        logInfo('MapMemoryPro: new place structure created', { placeId: placeId });
      } else {
        logDebug('MapMemoryPro: switch place structure', { placeId: placeId });
      }
    }

    /**
     * 主入口：由 SpatialEnginePro / EventFlowPro 调用
     * @param {Object} enhancedState
     * @param {Object} context {placeId?: string}
     */
    ingestEnhancedState(enhancedState, context) {
      try {
        if (!enhancedState || !enhancedState.grid) return;
        if (context && context.placeId) {
          this.setCurrentPlaceId(context.placeId);
        }
        const structure = this.getCurrentPlaceStructure();
        const before = structure.getSnapshot();
        structure.updateFromEnhancedState(enhancedState);
        const after = structure.getSnapshot();

        // 如果结构发生显著变化，记录一条 trace 日志
        this._maybeEmitStructureTrace(before, after);
      } catch (e) {
        logError('MapMemoryPro.ingestEnhancedState error', {
          error: e.toString(),
          stack: e.stack
        });
      }
    }

    _maybeEmitStructureTrace(before, after) {
      try {
        let changed = false;
        const diff = {};

        if (before.corridorWidthM !== after.corridorWidthM) {
          changed = true;
          diff.corridorWidthM = {
            before: before.corridorWidthM,
            after: after.corridorWidthM
          };
        }
        if (before.leftWallStable !== after.leftWallStable) {
          changed = true;
          diff.leftWallStable = {
            before: before.leftWallStable,
            after: after.leftWallStable
          };
        }
        if (before.rightWallStable !== after.rightWallStable) {
          changed = true;
          diff.rightWallStable = {
            before: before.rightWallStable,
            after: after.rightWallStable
          };
        }

        if (!changed) return;

        const traceId = this._allocTraceId();
        const payload = {
          traceId: traceId,
          placeId: after.placeId,
          event: 'structure_update',
          diff: diff,
          snapshot: after
        };
        logInfo('MapMemoryPro.structure_update', payload);

        // 若有后台上传模块，也可以在这里调用
        if (window.uploadLunaLog) {
          window.uploadLunaLog('map_memory_structure', payload);
        }
      } catch (e) {
        logError('MapMemoryPro._maybeEmitStructureTrace error', {
          error: e.toString(),
          stack: e.stack
        });
      }
    }

    getCurrentStructureSnapshot() {
      const structure = this.getCurrentPlaceStructure();
      return structure.getSnapshot();
    }
  }

  window.MapMemoryPro = new MapMemoryProClass();

  // 全局调试接口
  window.debugPrintMapMemoryPro = function () {
    if (!window.MapMemoryPro) return null;
    const snapshot = window.MapMemoryPro.getCurrentStructureSnapshot();
    logInfo('MapMemoryPro snapshot', snapshot);
    return snapshot;
  };

  if (window.logInfo) {
    window.logInfo('MapMemoryPro模块加载完成', { module: 'map_memory_pro' });
  } else {
    console.log('✅ MapMemoryPro模块加载完成', { module: 'map_memory_pro' });
  }
})();


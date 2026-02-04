// frontend/map_memory.js
/**
 * MapMemory / 地图记忆系统
 * 场景级记忆引擎：记住环境结构、静态地标、高频危险区域
 * 含记忆变更日志输出
 */
(function () {
  'use strict';
  
  if (window.MapMemory) return;

  const MAX_CELL_HISTORY = 50;     // 每个格子最多保留多少条样本
  const MIN_STATIC_COUNT = 5;      // 超过多少次可以认为是"稳定存在"
  const STATIC_TYPES = ['stairs', 'staircase', 'pillar', 'wall', 'door'];

  // 统一的 risk 数值映射
  const RISK_WEIGHT = {
    low: 0,
    medium: 1,
    high: 2,
    critical: 3
  };

  function safeLogInfo(msg, payload) {
    if (window.logInfo) {
      window.logInfo(msg, payload);
    } else {
      console.log('[MapMemory/INFO]', msg, payload || '');
    }
  }

  function safeLogDebug(msg, payload) {
    if (window.logDebug) {
      window.logDebug(msg, payload);
    } else {
      console.debug('[MapMemory/DEBUG]', msg, payload || '');
    }
  }

  function safeLogError(msg, payload) {
    if (window.logError) {
      window.logError(msg, payload);
    } else {
      console.error('[MapMemory/ERROR]', msg, payload || '');
    }
  }

  function normalizeType(type) {
    if (!type) return 'unknown';
    return String(type).toLowerCase();
  }

  /**
   * CellStats：单个格子的统计信息
   */
  class CellStats {
    constructor(xIndex, yIndex) {
      this.xIndex = xIndex;
      this.yIndex = yIndex;
      this.samples = [];       // [{type, risk, ts}]
      this.typeCounts = {};    // { 'stairs': 10, 'wall': 5 ...}
      this.riskSum = 0;
      this.riskCount = 0;
      this.isStaticHazard = false;
      this.staticType = null;
    }

    addSample(obj) {
      const now = Date.now();
      const type = normalizeType(obj.type);
      const risk = obj.risk_level || 'low';

      this.samples.push({
        type: type,
        risk: risk,
        ts: now
      });
      if (this.samples.length > MAX_CELL_HISTORY) {
        this.samples.shift();
      }

      // 类型统计
      this.typeCounts[type] = (this.typeCounts[type] || 0) + 1;

      // 风险统计
      const weight = RISK_WEIGHT[risk] || 0;
      this.riskSum += weight;
      this.riskCount += 1;

      this._updateStaticHazard();
    }

    _updateStaticHazard() {
      const before = this.isStaticHazard;
      const dom = this.getDominantType();
      const avgRisk = this.getAvgRiskLevel();

      const isStaticType = dom.type &&
        STATIC_TYPES.some(t => dom.type.indexOf(t) !== -1);

      const enoughCount = dom.count >= MIN_STATIC_COUNT;
      const riskHigh = avgRisk === 'high' || avgRisk === 'critical';

      this.isStaticHazard = !!(isStaticType && (enoughCount || riskHigh));
      this.staticType = this.isStaticHazard ? dom.type : null;

      // 只有从 false -> true 时才记一条日志
      if (!before && this.isStaticHazard) {
        safeLogInfo('MapMemory: cell promoted to static hazard', {
          cell: { xIndex: this.xIndex, yIndex: this.yIndex },
          static_type: this.staticType,
          dominant_count: dom.count,
          avg_risk: avgRisk
        });
      }
    }

    getDominantType() {
      let bestType = null;
      let bestCount = 0;
      Object.keys(this.typeCounts).forEach(k => {
        const v = this.typeCounts[k];
        if (v > bestCount) {
          bestCount = v;
          bestType = k;
        }
      });
      return { type: bestType, count: bestCount };
    }

    getAvgRiskLevel() {
      if (!this.riskCount) return 'low';
      const avg = this.riskSum / this.riskCount;
      if (avg >= 2.5) return 'critical';
      if (avg >= 1.5) return 'high';
      if (avg >= 0.5) return 'medium';
      return 'low';
    }
  }

  /**
   * PlaceMap：地点地图（对应一个场景）
   */
  class PlaceMap {
    constructor(placeId) {
      this.placeId = placeId;
      this.grid = {}; // key: "xIndex,yIndex" -> CellStats
      this.lastUpdateTs = Date.now();
      this.sceneTypes = {}; // 场景类型分布
    }

    _cellKey(xIndex, yIndex) {
      return xIndex + ',' + yIndex;
    }

    updateFromSpaceState(spaceState) {
      this.lastUpdateTs = Date.now();
      if (!spaceState || !spaceState.grid) return;

      const st = spaceState.scene_type || 'unknown';
      this.sceneTypes[st] = (this.sceneTypes[st] || 0) + 1;

      const grid = spaceState.grid;
      const objects = spaceState.objects || [];

      for (let i = 0; i < objects.length; i++) {
        const obj = objects[i];
        const bev = obj.bev || {};
        const x = bev.x;
        const y = bev.y;
        if (typeof x !== 'number' || typeof y !== 'number') continue;

        const xIndex = Math.floor((x + grid.width_m / 2) / grid.resolution_m);
        const yIndex = Math.floor(y / grid.resolution_m);
        if (xIndex < 0 || yIndex < 0) continue;

        const key = this._cellKey(xIndex, yIndex);
        if (!this.grid[key]) {
          this.grid[key] = new CellStats(xIndex, yIndex);
        }

        this.grid[key].addSample({
          type: obj.type,
          risk_level: obj.risk_level
        });
      }
    }

    queryCell(xIndex, yIndex) {
      const key = this._cellKey(xIndex, yIndex);
      return this.grid[key] || null;
    }

    queryByBevCoord(x, y, gridMeta) {
      if (!gridMeta) return null;
      const xIndex = Math.floor((x + gridMeta.width_m / 2) / gridMeta.resolution_m);
      const yIndex = Math.floor(y / gridMeta.resolution_m);
      return this.queryCell(xIndex, yIndex);
    }

    /**
     * 判断某点是否是"记忆中的静态危险点"
     */
    isStaticHazardAt(x, y, gridMeta) {
      const cell = this.queryByBevCoord(x, y, gridMeta);
      return !!(cell && cell.isStaticHazard);
    }

    getSnapshotSummary() {
      // 用于调试：导出一个简要概览
      const cells = [];
      Object.keys(this.grid).forEach(key => {
        const cell = this.grid[key];
        const dom = cell.getDominantType();
        const avgRisk = cell.getAvgRiskLevel();
        if (!dom.type) return;
        cells.push({
          key: key,
          type: dom.type,
          count: dom.count,
          avg_risk: avgRisk,
          is_static_hazard: cell.isStaticHazard
        });
      });
      return {
        placeId: this.placeId,
        updated_at: this.lastUpdateTs,
        sceneTypes: this.sceneTypes,
        cells: cells
      };
    }
  }

  /**
   * MapMemoryClass：地图记忆主类
   */
  class MapMemoryClass {
    constructor() {
      this.places = {}; // placeId -> PlaceMap
      this.currentPlaceId = 'session_default';
    }

    setCurrentPlace(placeId) {
      if (!placeId) return;
      this.currentPlaceId = placeId;
      if (!this.places[placeId]) {
        this.places[placeId] = new PlaceMap(placeId);
        safeLogInfo('MapMemory: new place created', { placeId: placeId });
      } else {
        safeLogDebug('MapMemory: switch to existing place', { placeId: placeId });
      }
    }

    getCurrentPlace() {
      if (!this.places[this.currentPlaceId]) {
        this.places[this.currentPlaceId] = new PlaceMap(this.currentPlaceId);
      }
      return this.places[this.currentPlaceId];
    }

    /**
     * 入口：SpaceEngine 每帧调用，用当前空间状态更新记忆
     * context 可以传 placeId、gps 等
     */
    update(spaceState, context) {
      try {
        if (!spaceState || !spaceState.grid) return;
        if (context && context.placeId) {
          this.setCurrentPlace(context.placeId);
        }

        const place = this.getCurrentPlace();
        place.updateFromSpaceState(spaceState);

        safeLogDebug('MapMemory.update', {
          placeId: this.currentPlaceId,
          scene_type: spaceState.scene_type,
          objects: (spaceState.objects || []).length
        });
      } catch (e) {
        safeLogError('MapMemory.update error', {
          error: e.toString(),
          stack: e.stack
        });
      }
    }

    /**
     * 用记忆增强 SpaceState，在每个 object 上挂 memory 字段
     */
    enrichSpaceState(spaceState) {
      if (!spaceState || !spaceState.grid) return spaceState;
      const place = this.getCurrentPlace();
      const gridMeta = spaceState.grid;

      const enrichedObjects = (spaceState.objects || []).map(obj => {
        const bev = obj.bev || {};
        const cell = place.queryByBevCoord(bev.x, bev.y, gridMeta);
        if (!cell) {
          return obj;
        }
        const dom = cell.getDominantType();
        const avgRisk = cell.getAvgRiskLevel();
        const memoryTag = {
          dominant_type: dom.type,
          dominant_count: dom.count,
          avg_risk: avgRisk,
          is_static_hazard: cell.isStaticHazard
        };
        return Object.assign({}, obj, { memory: memoryTag });
      });

      return Object.assign({}, spaceState, {
        objects: enrichedObjects
      });
    }

    /** 调试接口：打印当前 PlaceMap 概览 */
    debugPrintCurrentPlace() {
      const place = this.getCurrentPlace();
      const snapshot = place.getSnapshotSummary();
      safeLogInfo('MapMemory snapshot', snapshot);
      return snapshot;
    }
  }

  // 挂到全局
  window.MapMemory = new MapMemoryClass();

  // 提供一个便捷调试函数
  window.debugPrintMapMemory = function () {
    if (!window.MapMemory) return;
    return window.MapMemory.debugPrintCurrentPlace();
  };

  if (window.logInfo) {
    window.logInfo('MapMemory模块加载完成', { module: 'map_memory' });
  } else {
    console.log('✅ MapMemory模块加载完成', { module: 'map_memory' });
  }
})();

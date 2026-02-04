// frontend/spatial_engine.js
/**
 * SpaceEngine / 空间引擎
 * 在 YOLO 之上构建"鸟瞰图 + 风险评估 + 行为建议"
 * 
 * 输入：YOLO检测结果（detections, frameWidth, frameHeight）
 * 输出：spaceState（场景类型、鸟瞰图、风险评估、行为建议）
 */
(function () {
  'use strict';
  
  if (window.SpaceEngine) return;

  const M_PER_PIXEL_BASE = 0.002; // 粗略系数：后期可标定调整
  const BEV_MAX_FORWARD_M = 5.0;
  const BEV_HALF_WIDTH_M = 2.0;
  const BEV_RESOLUTION_M = 0.25; // 每格 25cm

  const SCENE_TYPES = {
    UNKNOWN: 'unknown',
    STREET: 'street',
    SUBWAY: 'subway',
    MALL: 'mall',
    HOSPITAL: 'hospital',
    INDOOR_CORRIDOR: 'indoor_corridor',
    STAIRS_AREA: 'stairs_area'
  };

  const RISK_LEVELS = ['low', 'medium', 'high', 'critical'];

  function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
  }

  function sign(v) {
    return v >= 0 ? 1 : -1;
  }

  /**
   * Track：多帧追踪单个目标
   */
  class Track {
    constructor(id, det, frameWidth, frameHeight) {
      this.id = id;
      this.label = det.label || det.class || '';
      this.history = [];
      this.stableFrames = 0;
      this.lastUpdateTs = Date.now();
      this.addObservation(det, frameWidth, frameHeight);
    }

    addObservation(det, frameWidth, frameHeight) {
      const now = Date.now();
      const geom = SpaceEngineGeometry.computeGeometry(det, frameWidth, frameHeight);
      this.history.push({
        ts: now,
        det,
        geom
      });
      if (this.history.length > 10) {
        this.history.shift();
      }
      this.lastUpdateTs = now;

      // 稳定帧数：连续出现则增加
      this.stableFrames += 1;
    }

    getLatest() {
      return this.history[this.history.length - 1] || null;
    }

    // 速度/运动趋势估计
    getMotion() {
      if (this.history.length < 2) return 'static';
      const last = this.history[this.history.length - 1];
      const prev = this.history[this.history.length - 2];
      const dy = prev.geom.distance_m - last.geom.distance_m; // 正数表示靠近
      const dx = last.geom.bearing_deg - prev.geom.bearing_deg;

      if (Math.abs(dy) < 0.05 && Math.abs(dx) < 1) return 'static';
      if (dy > 0.1) return 'approaching';
      if (dy < -0.1) return 'leaving';
      // 水平穿越
      if (Math.abs(dx) > 3) return 'crossing';
      return 'unknown';
    }
  }

  /**
   * SpaceEngineGeometry：几何计算（2D → 伪3D）
   */
  const SpaceEngineGeometry = {
    // 估算距离 & 方位；不用物理精度，保持一致性即可
    computeGeometry(det, frameWidth, frameHeight) {
      const box = det.box || det.bbox || det.rect;
      if (!box) {
        return {
          distance_m: 10,
          bearing_deg: 0,
          in_path: false,
          bev_x: 0,
          bev_y: 10
        };
      }
      const x1 = box.x1, y1 = box.y1, x2 = box.x2, y2 = box.y2;
      const w = x2 - x1;
      const h = y2 - y1;
      const cx = (x1 + x2) / 2;
      const cy = (y1 + y2) / 2;
      const area = Math.max(w * h, 1);

      // 距离估算：面积越大，距离越近
      const approxDistanceM = clamp((1.0 / Math.sqrt(area)) / M_PER_PIXEL_BASE, 0.2, 10.0);

      // bearing：相对水平中心的偏移
      const centerX = frameWidth / 2;
      const offsetX = (cx - centerX) / centerX; // -1 ~ 1
      const MAX_FOV_DEG = 80; // 视场角可以后续标定
      const bearingDeg = clamp(offsetX * (MAX_FOV_DEG / 2), -MAX_FOV_DEG / 2, MAX_FOV_DEG / 2);

      // in_path：中心区域
      const PATH_REGION_RATIO = 0.4;
      const pathHalfWidthPx = frameWidth * PATH_REGION_RATIO / 2;
      const inPath = Math.abs(cx - centerX) <= pathHalfWidthPx;

      // 鸟瞰坐标：以脚下为原点，y 正向前，x 左负右正
      const rad = bearingDeg * Math.PI / 180.0;
      const bevY = approxDistanceM * Math.cos(rad);
      const bevX = approxDistanceM * Math.sin(rad);

      return {
        distance_m: approxDistanceM,
        bearing_deg: bearingDeg,
        in_path: inPath,
        bev_x: bevX,
        bev_y: bevY
      };
    }
  };

  /**
   * SpaceEngineClass：主引擎类
   */
  class SpaceEngineClass {
    constructor() {
      this.tracks = {};
      this.nextId = 1;
      this.lastSpaceState = null;
    }

    _allocId() {
      return 'trk_' + (this.nextId++);
    }

    // 简单 IoU 匹配：将新检测匹配到已有 Track
    _matchDetectionsToTracks(detections, frameWidth, frameHeight) {
      const usedTrackIds = new Set();
      const detAssignments = []; // {det, track}

      // 把历史 track 的最新 box 拿出来
      const trackList = Object.values(this.tracks).map(track => {
        const latest = track.getLatest();
        return latest ? { track, box: latest.det.box || latest.det.bbox || latest.det.rect } : null;
      }).filter(Boolean);

      function iou(boxA, boxB) {
        if (!boxA || !boxB) return 0;
        const x1 = Math.max(boxA.x1, boxB.x1);
        const y1 = Math.max(boxA.y1, boxB.y1);
        const x2 = Math.min(boxA.x2, boxB.x2);
        const y2 = Math.min(boxA.y2, boxB.y2);
        const interW = Math.max(0, x2 - x1);
        const interH = Math.max(0, y2 - y1);
        const interArea = interW * interH;
        const areaA = (boxA.x2 - boxA.x1) * (boxA.y2 - boxA.y1);
        const areaB = (boxB.x2 - boxB.x1) * (boxB.y2 - boxB.y1);
        if (areaA <= 0 || areaB <= 0) return 0;
        return interArea / (areaA + areaB - interArea);
      }

      detections.forEach(det => {
        const box = det.box || det.bbox || det.rect;
        let bestTrack = null;
        let bestIoU = 0;

        trackList.forEach(entry => {
          if (usedTrackIds.has(entry.track.id)) return;
          const score = iou(box, entry.box);
          if (score > bestIoU) {
            bestIoU = score;
            bestTrack = entry.track;
          }
        });

        if (bestTrack && bestIoU > 0.3) {
          usedTrackIds.add(bestTrack.id);
          detAssignments.push({ det, track: bestTrack });
        } else {
          // 新建 track
          const newId = this._allocId();
          const t = new Track(newId, det, frameWidth, frameHeight);
          this.tracks[newId] = t;
          usedTrackIds.add(newId);
          detAssignments.push({ det, track: t });
        }
      });

      // 清理长时间未更新的 Track
      const now = Date.now();
      Object.keys(this.tracks).forEach(id => {
        const t = this.tracks[id];
        if (now - t.lastUpdateTs > 5000) { // 5s 没更新就删
          delete this.tracks[id];
        }
      });

      // 更新匹配到的 track
      detAssignments.forEach(assign => {
        assign.track.addObservation(assign.det, frameWidth, frameHeight);
      });

      return Object.values(this.tracks);
    }

    // 场景类型判断
    _classifyScene(detections) {
      const labels = detections.map(d => d.label || d.class || '');
      const has = (name) => labels.some(l => l && l.toLowerCase().includes(name));

      if (has('train') || has('platform')) return SCENE_TYPES.SUBWAY;
      if (has('escalator') || has('shopping_cart') || has('shelf')) return SCENE_TYPES.MALL;
      if (has('car') || has('bus') || has('traffic_light') || has('crosswalk')) return SCENE_TYPES.STREET;
      if (has('bed') || has('wheelchair') || has('stretcher')) return SCENE_TYPES.HOSPITAL;
      if (has('stairs') || has('staircase')) return SCENE_TYPES.STAIRS_AREA;
      if (has('door') || has('corridor')) return SCENE_TYPES.INDOOR_CORRIDOR;
      return SCENE_TYPES.UNKNOWN;
    }

    // 风险打分
    _computeRiskForTrack(track, sceneType) {
      const latest = track.getLatest();
      if (!latest) return { score: 0, level: 'low' };

      const g = latest.geom;
      const motion = track.getMotion();
      const label = track.label.toLowerCase();
      let score = 0;

      if (g.in_path) score += 3;
      if (g.distance_m < 1.5) score += 3;
      if (g.distance_m < 0.8) score += 3;
      if (motion === 'approaching') score += 3;
      if (motion === 'crossing') score += 2;
      if (track.stableFrames >= 3) score += 2;

      // 类型 + 场景加权
      if (label.includes('stairs') || label.includes('staircase')) {
        score += 5;
      }
      if (sceneType === SCENE_TYPES.STREET && (label.includes('car') || label.includes('bus'))) {
        score += 4;
      }
      if (sceneType === SCENE_TYPES.SUBWAY && label.includes('platform_edge')) {
        score += 5;
      }

      // ✅ 使用地图记忆加权风险（如果某点被记为静态危险点，就加权）
      if (window.MapMemory && this.lastSpaceState && this.lastSpaceState.grid) {
        try {
          const gridMeta = this.lastSpaceState.grid;
          const latest = track.getLatest();
          if (latest && typeof latest.geom.bev_x === 'number' && typeof latest.geom.bev_y === 'number') {
            const place = window.MapMemory.getCurrentPlace && window.MapMemory.getCurrentPlace();
            if (place) {
              const cell = place.queryByBevCoord(latest.geom.bev_x, latest.geom.bev_y, gridMeta);
              if (cell && cell.isStaticHazard) {
                score += 2; // 静态危险点：额外加权
                if (window.logDebug) {
                  window.logDebug('SpaceEngine: risk boosted by MapMemory', {
                    label: track.label,
                    bev_x: latest.geom.bev_x,
                    bev_y: latest.geom.bev_y,
                    cell_type: cell.staticType,
                    new_score: score
                  });
                }
              }
            }
          }
        } catch (e) {
          if (window.logError) {
            window.logError('SpaceEngine: MapMemory risk boost error', {
              error: e.toString(),
              stack: e.stack
            });
          }
        }
      }

      // 转 level
      let level = 'low';
      if (score >= 12) level = 'critical';
      else if (score >= 8) level = 'high';
      else if (score >= 4) level = 'medium';

      return { score, level };
    }

    // 构建鸟瞰 Grid
    _buildGridFromTracks(tracks) {
      const widthM = BEV_HALF_WIDTH_M * 2;
      const heightM = BEV_MAX_FORWARD_M;
      const res = BEV_RESOLUTION_M;
      const cols = Math.ceil(widthM / res);
      const rows = Math.ceil(heightM / res);
      const cells = [];

      function coordToIndex(x, y) {
        const col = Math.floor((x + BEV_HALF_WIDTH_M) / res);
        const row = Math.floor(y / res);
        if (col < 0 || col >= cols || row < 0 || row >= rows) return null;
        return { col, row };
      }

      tracks.forEach(track => {
        const latest = track.getLatest();
        if (!latest) return;
        const gx = latest.geom.bev_x;
        const gy = latest.geom.bev_y;
        const idx = coordToIndex(gx, gy);
        if (!idx) return;
        cells.push({
          xIndex: idx.col,
          yIndex: idx.row,
          occupied: true,
          type: track.label,
          risk: track._riskLevel || 'low'
        });
      });

      return {
        width_m: widthM,
        height_m: heightM,
        resolution_m: res,
        cells
      };
    }

    // 入口：每帧更新
    updateFromDetections(frameData) {
      try {
        const { detections, frameWidth, frameHeight } = frameData || {};
        if (!Array.isArray(detections) || !frameWidth || !frameHeight) {
          if (window.logDebug) {
            window.logDebug('SpaceEngine.updateFromDetections: invalid frameData', frameData);
          }
          return null;
        }

        // 1) 更新追踪
        const tracks = this._matchDetectionsToTracks(detections, frameWidth, frameHeight);

        // 2) 场景判断
        const sceneType = this._classifyScene(detections);

        // 3) 风险评估
        let primaryHazard = null;
        let maxScore = -1;
        const objectStates = [];

        tracks.forEach(track => {
          const latest = track.getLatest();
          if (!latest) return;
          const geom = latest.geom;
          const motion = track.getMotion();
          const risk = this._computeRiskForTrack(track, sceneType);
          track._riskScore = risk.score;
          track._riskLevel = risk.level;

          const objState = {
            trackId: track.id,
            type: track.label,
            distance: geom.distance_m,
            bearing: geom.bearing_deg,
            in_path: geom.in_path,
            stable_frames: track.stableFrames,
            motion,
            risk_score: risk.score,
            risk_level: risk.level,
            bev: { x: geom.bev_x, y: geom.bev_y }
          };
          objectStates.push(objState);

          if (risk.score > maxScore) {
            maxScore = risk.score;
            primaryHazard = objState;
          }
        });

        // 4) overall risk
        let overallRisk = 'low';
        if (maxScore >= 12) overallRisk = 'critical';
        else if (maxScore >= 8) overallRisk = 'high';
        else if (maxScore >= 4) overallRisk = 'medium';

        // 5) 推荐行为
        let recommendedAction = 'keep';
        if (overallRisk === 'medium') recommendedAction = 'slow_down';
        if (overallRisk === 'high') recommendedAction = 'prepare_stop';
        if (overallRisk === 'critical') recommendedAction = 'stop_immediately';

        // 6) 构建鸟瞰 grid
        const grid = this._buildGridFromTracks(tracks);

        let spaceState = {
          ts: Date.now(),
          scene_type: sceneType,
          ego: {
            position: { x: 0, y: 0 },
            direction: 'forward'
          },
          grid,
          objects: objectStates,
          primary_hazard: primaryHazard,
          overall_risk: overallRisk,
          recommended_action: recommendedAction
        };

        // ✅ 利用地图记忆模块：更新 + 增强
        if (window.MapMemory) {
          try {
            window.MapMemory.update(spaceState, {
              placeId: 'session_default'  // 一期先这样，后面可以用真实 placeId
            });
            const enriched = window.MapMemory.enrichSpaceState(spaceState);
            if (enriched) {
              spaceState = enriched;
            }
          } catch (e) {
            if (window.logError) {
              window.logError('SpaceEngine: MapMemory integration error', {
                error: e.toString(),
                stack: e.stack
              });
            }
          }
        }

        this.lastSpaceState = spaceState;

        if (window.logDebug) {
          window.logDebug('SpaceEngine.spaceState', spaceState);
        }

        // 通知 EventFlow / NavigationFSM / WaypointManager
        if (window.EventFlow && window.EventFlow.onSpaceState) {
          window.EventFlow.onSpaceState(spaceState);
        }

        return spaceState;
      } catch (e) {
        if (window.logError) {
          window.logError('SpaceEngine.updateFromDetections error', {
            error: e.toString(),
            stack: e.stack
          });
        } else {
          console.error('SpaceEngine.updateFromDetections error', e);
        }
        return null;
      }
    }

    getLastSpaceState() {
      return this.lastSpaceState;
    }
  }

  window.SpaceEngine = new SpaceEngineClass();
  
  if (window.logInfo) {
    window.logInfo('SpaceEngine模块加载完成', { module: 'spatial_engine' });
  } else {
    console.log('✅ SpaceEngine模块加载完成', { module: 'spatial_engine' });
  }
})();


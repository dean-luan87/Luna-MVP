// frontend/vision_enhancer.js
/**
 * 旗舰视觉增强（YOLO六层逻辑）
 * - 多帧稳定（Stability）
 * - 伪深度估计（Pseudo-Depth）
 * - 场景分层（Scene / Geometry / Risk）
 * - 简易对象追踪（可占位实现）
 * - 环境"空场景"稳定滤波
 * - 输出统一的 visionSummary 供导航/危险逻辑使用
 */
(function () {
  'use strict';
  
  if (window.VisionEnhancer) return;

  const CENTER_REGION_RATIO = 0.5;   // 中央区域判定
  const NEAR_DISTANCE_CM = 150;      // 近距离危险阈值
  const STABILITY_WINDOW = 6;        // 多帧窗口
  const STABILITY_DANGER_THRESHOLD = 4;
  const SAFE_FRAME_WINDOW = 10;
  const SAFE_FRAME_THRESHOLD = 7;

  class StabilityFilter {
    constructor() {
      this.frames = [];
    }
    push(frame) {
      this.frames.push(frame);
      if (this.frames.length > STABILITY_WINDOW) {
        this.frames.shift();
      }
    }
    isDangerStable() {
      const count = this.frames.filter(f => f.isDangerFrame).length;
      return count >= STABILITY_DANGER_THRESHOLD;
    }
    reset() {
      this.frames = [];
    }
  }

  class SafeFrameFilter {
    constructor() {
      this.safeFrames = [];
    }
    push(isSafe) {
      this.safeFrames.push(isSafe);
      if (this.safeFrames.length > SAFE_FRAME_WINDOW) {
        this.safeFrames.shift();
      }
    }
    isStableSafe() {
      const countSafe = this.safeFrames.filter(Boolean).length;
      return countSafe >= SAFE_FRAME_THRESHOLD;
    }
    reset() {
      this.safeFrames = [];
    }
  }

  class VisionEnhancer {
    constructor() {
      this.stabilityFilter = new StabilityFilter();
      this.safeFilter = new SafeFrameFilter();
      this.suppressDangerUntil = 0;
      this.lastSummary = null;
    }

    estimateDistance(box, frameWidth, frameHeight) {
      const w = (box.x2 - box.x1);
      const h = (box.y2 - box.y1);
      const area = Math.max(w * h, 1);
      const k = 20000; // 可以后续通过标定调整
      return k / Math.sqrt(area);
    }

    isBoxCenter(block, frameWidth, frameHeight) {
      const cx = (block.x1 + block.x2) / 2;
      const cy = (block.y1 + block.y2) / 2;
      const rx = frameWidth * CENTER_REGION_RATIO / 2;
      const ry = frameHeight * CENTER_REGION_RATIO / 2;
      const centerX = frameWidth / 2;
      const centerY = frameHeight / 2;
      return (Math.abs(cx - centerX) <= rx && Math.abs(cy - centerY) <= ry);
    }

    classifyScene(detections) {
      // ✅ 防御性编程：确保 detections 不为 null
      if (!detections || !Array.isArray(detections)) {
        return 'unknown';
      }
      const labels = detections.map(d => d.label || d.class || '').filter(Boolean);
      let sceneType = 'unknown';
      if (labels.some(l => l.includes('train') || l.includes('platform'))) sceneType = 'subway';
      else if (labels.some(l => l.includes('escalator') || l.includes('shopping'))) sceneType = 'mall';
      else if (labels.some(l => l.includes('car') || l.includes('bus') || l.includes('vehicle'))) sceneType = 'street';
      else if (labels.some(l => l.includes('bed') || l.includes('monitor') || l.includes('chair'))) sceneType = 'indoor';
      
      // ✅ E4: 自动区域识别 - 输入视觉提示
      if (window.ZoneAutoDetector && sceneType !== 'unknown') {
        window.ZoneAutoDetector.feedVisualHint(sceneType);
      }
      
      return sceneType;
    }

    analyzeRisk(raw) {
      // ✅ 防御性编程：检查输入有效性
      if (!raw || !raw.detections || !Array.isArray(raw.detections)) {
        // 没有有效检测结果，当作安全帧处理
        this.stabilityFilter.push({ isDangerFrame: false });
        this.safeFilter.push(true);

        const summary = {
          ts: Date.now(),
          scene: 'unknown',
          hasDangerFrame: false,
          isDangerStable: this.stabilityFilter.isDangerStable(),
          dangerSuppressed: false,
          riskLevel: 'low',
          closestDanger: null,
          hazards: [],
          rawDetections: []
        };
        this.lastSummary = summary;
        return summary;
      }

      const { detections, frameWidth, frameHeight } = raw;
      let hasDanger = false;
      let closestDanger = null;
      const hazards = [];

      const now = Date.now();
      const dangerSuppressed = now < this.suppressDangerUntil;

      // ✅ 修复：先过滤掉 null/undefined，再处理
      const processed = (detections || [])
        .filter(Boolean)                 // ① 先把 null / undefined 过滤掉
        .map(rawDet => {
          const det = rawDet || {};      // ② 再兜一层保险

          // 兼容不同的box格式
          const box = det.box || det.bbox || { x1: 0, y1: 0, x2: 0, y2: 0 };
          const distance = this.estimateDistance(box, frameWidth || 640, frameHeight || 480);
          const inCenter = this.isBoxCenter(box, frameWidth || 640, frameHeight || 480);
          return Object.assign({}, det, { distance, inCenter, box }); // ③ 这里就安全了
        });

      for (const det of processed) {
        const { label, class: className, distance, inCenter } = det;
        const labelStr = label || className || '';

        if (labelStr.includes('person') && distance < 100 && inCenter) {
          // 认为可能是"自己"或紧贴镜头人脸，默认不报危险
          continue;
        }

        if (distance < NEAR_DISTANCE_CM && inCenter) {
          hasDanger = true;
          hazards.push({
            label: labelStr,
            distance,
            reason: 'near_center_obstacle',
          });
          if (!closestDanger || distance < closestDanger.distance) {
            closestDanger = { label: labelStr, distance };
          }
        }
      }

      const isDangerFrame = hasDanger && !dangerSuppressed;

      this.stabilityFilter.push({ isDangerFrame });
      this.safeFilter.push(!hasDanger);

      if (this.safeFilter.isStableSafe()) {
        // 连续多帧安全 → 短时间内压制危险
        this.suppressDangerUntil = Date.now() + 1000;
      }

      const stableDanger = this.stabilityFilter.isDangerStable() && !dangerSuppressed;

      const riskLevel = stableDanger
        ? (closestDanger && closestDanger.distance < 80 ? 'high' : 'medium')
        : 'low';

      // ✅ MiniMap 集成：检测到危险时添加到小地图
      if (stableDanger && window.MiniMap && closestDanger) {
        // 根据危险位置判断方向（简化处理：默认前方）
        window.MiniMap.addHazard('front');
      }

      const summary = {
        ts: Date.now(),
        scene: this.classifyScene(detections || []),
        hasDangerFrame: hasDanger,
        isDangerStable: this.stabilityFilter.isDangerStable(),
        dangerSuppressed,
        riskLevel,
        closestDanger,
        hazards,
        rawDetections: processed
      };

      this.lastSummary = summary;
      return summary;
    }

    /**
     * 桥接视觉结果到 NavigationFSM
     */
    _bridgeToNavigationFSM(summary, yoloOutput) {
      if (!window.NavigationFSM || !window.NavigationFSM.onVisionUpdate) {
        return;
      }

      const detections = summary.rawDetections || [];
      if (detections.length === 0) return;

      // 检测导航相关的视觉信息
      const navSigns = detections.filter(d => {
        const label = (d.label || d.class || '').toLowerCase();
        return label.includes('sign') || 
               label.includes('arrow') || 
               label.includes('turn') ||
               label.includes('straight') ||
               label.includes('left') ||
               label.includes('right');
      });

      // 检测关键节点（POI）
      const poiLabels = ['entrance', 'exit', 'door', 'gate', 'hospital', 'mall', 'subway'];
      const pois = detections.filter(d => {
        const label = (d.label || d.class || '').toLowerCase();
        return poiLabels.some(poi => label.includes(poi));
      });

      // 如果有导航标志，派发 NAV_TURN 或 NAV_STRAIGHT
      if (navSigns.length > 0) {
        const sign = navSigns[0];
        const label = (sign.label || sign.class || '').toLowerCase();
        const distance = sign.distance || null;
        
        let direction = null;
        if (label.includes('left') || label.includes('turn-left')) {
          direction = 'left';
        } else if (label.includes('right') || label.includes('turn-right')) {
          direction = 'right';
        } else if (label.includes('straight') || label.includes('forward')) {
          direction = 'straight';
        }

        if (direction === 'left' || direction === 'right') {
          // ✅ 记录 YOLO → FSM 日志
          if (window.NavLog) {
            window.NavLog.info("YOLO", "视觉方向更新", { direction, distance, raw: sign });
          }
          
          // ✅ MiniMap 集成：添加方向标记（作为视觉更新）
          if (window.MiniMap && direction) {
            const dir = direction === 'straight' ? 'front' : direction;
            window.MiniMap.addHazard(dir);
          }
          
          window.NavigationFSM.onVisionUpdate({
            type: 'NAV_TURN',
            payload: { direction, distance },
            priority: 'HIGH'
          });
        } else if (direction === 'straight') {
          // ✅ 记录 YOLO → FSM 日志
          if (window.NavLog) {
            window.NavLog.info("YOLO", "视觉方向更新", { direction: 'straight', distance, raw: sign });
          }
          
          // ✅ MiniMap 集成：添加方向标记（作为视觉更新）
          if (window.MiniMap) {
            window.MiniMap.addHazard('front');
          }
          
          window.NavigationFSM.onVisionUpdate({
            type: 'NAV_STRAIGHT',
            payload: { distance },
            priority: 'MEDIUM'
          });
        }
      }

      // 如果有关键节点，派发 NAV_POI
      if (pois.length > 0) {
        const poi = pois[0];
        const name = poi.label || poi.class || '关键节点';
        // ✅ 记录 POI 检测日志
        if (window.NavLog) {
          window.NavLog.info("YOLO", "检测到关键节点", { name, type: poi.class, distance: poi.distance });
        }
        window.NavigationFSM.onVisionUpdate({
          type: 'NAV_POI',
          payload: { name, type: poi.class },
          priority: 'MEDIUM'
        });
      }
    }

    processFrame(yoloOutput) {
      try {
        const summary = this.analyzeRisk(yoloOutput);

        // 原来：this.lastSummary = summary;
        this.lastSummary = summary;

        // ✅ 新增：把 yoloOutput 交给 SpaceEngine 构建 spaceState
        if (window.SpaceEngine) {
          try {
            const spaceState = window.SpaceEngine.updateFromDetections({
              detections: (yoloOutput && yoloOutput.detections) || [],
              frameWidth: yoloOutput.frameWidth,
              frameHeight: yoloOutput.frameHeight
            });
            summary.space_state = spaceState || null;
          } catch (e) {
            if (window.logError) {
              window.logError('SpaceEngine.updateFromDetections error in VisionEnhancer', {
                error: e.toString(),
                stack: e.stack
              });
            }
          }
        }

        if (window.logDebug) {
          window.logDebug('VisionEnhancer.summary', summary);
        }

        // 继续走 EventFlow
        if (window.EventFlow && window.EventFlow.onVisionSummary) {
          window.EventFlow.onVisionSummary(summary);
        }

        // ✅ 新增：桥接 YOLO → NavigationFSM
        this._bridgeToNavigationFSM(summary, yoloOutput);
        
        // ✅ 新增：记录 YOLO 视觉日志
        if (window.NavLog) {
          const navSigns = summary.rawDetections?.filter(d => {
            const label = (d.label || d.class || '').toLowerCase();
            return label.includes('sign') || label.includes('arrow') || label.includes('turn') || label.includes('straight');
          }) || [];
          if (navSigns.length > 0) {
            window.NavLog.info("YOLO", "检测到导航标志", { 
              signs: navSigns.map(s => ({ label: s.label || s.class, distance: s.distance })),
              summary: { scene: summary.scene, riskLevel: summary.riskLevel }
            });
          }
        }

        return summary;
      } catch (e) {
        if (window.logError) {
          window.logError('VisionEnhancer.processFrame error', { error: e.toString(), stack: e.stack });
        } else {
          console.error('VisionEnhancer.processFrame error', e);
        }
        return null;
      }
    }
  }

  window.VisionEnhancer = new VisionEnhancer();
  console.log('✅ VisionEnhancer模块加载完成', { module: 'vision_enhancer' });
})();



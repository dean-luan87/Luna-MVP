// frontend/scene_reasoner.js
/**
 * Scene Reasoning Engine (SRE) / 场景推理引擎
 * 输入：enhancedState（来自 SpatialEnginePro）
 * 输出：sceneContext（场景推理结果），自动打日志、可被导航/任务链使用
 */
(function () {
  'use strict';
  
  if (window.SceneReasoner) return;

  function logInfo(msg, payload) {
    if (window.logInfo) window.logInfo(msg, payload);
    else console.log('[SceneReasoner]', msg, payload || '');
  }

  function logDebug(msg, payload) {
    if (window.logDebug) window.logDebug(msg, payload);
    else console.debug('[SceneReasoner]', msg, payload || '');
  }

  function logError(msg, payload) {
    if (window.logError) window.logError(msg, payload);
    else console.error('[SceneReasoner]', msg, payload || '');
  }

  function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
  }

  function safeGet(obj, path, defVal) {
    try {
      const parts = path.split('.');
      let cur = obj;
      for (let i = 0; i < parts.length; i++) {
        if (!cur) return defVal;
        cur = cur[parts[i]];
      }
      return cur == null ? defVal : cur;
    } catch (e) {
      return defVal;
    }
  }

  // ---- 场景分类器（轻量规则版） ----------------------------------
  class SceneClassifier {
    constructor() {
      this.lastSceneType = 'unknown';
    }

    classify(enhancedState, structureSnapshot) {
      const baseType = enhancedState.scene_type || 'unknown';
      const grid = enhancedState.grid || {};
      const widthM = typeof grid.width_m === 'number' ? grid.width_m : 4.0;
      const objects = enhancedState.objects || [];

      let stairsCount = 0;
      let vehicleCount = 0;
      let chairCount = 0;
      let signCount = 0;

      for (let i = 0; i < objects.length; i++) {
        const t = (objects[i].type || objects[i].label || '').toLowerCase();
        if (t.indexOf('stair') !== -1) stairsCount++;
        if (t.indexOf('car') !== -1 || t.indexOf('bus') !== -1 || t.indexOf('truck') !== -1) vehicleCount++;
        if (t.indexOf('chair') !== -1 || t.indexOf('sofa') !== -1 || t.indexOf('seat') !== -1) chairCount++;
        if (t.indexOf('sign') !== -1 || t.indexOf('board') !== -1 || t.indexOf('panel') !== -1) signCount++;
      }

      const leftWallStable = structureSnapshot && !!structureSnapshot.leftWallStable;
      const rightWallStable = structureSnapshot && !!structureSnapshot.rightWallStable;
      const corridorWidthM = structureSnapshot && structureSnapshot.corridorWidthM;

      let inferred = 'unknown';
      let indoor = false;
      let corridorLike = false;
      let stairZone = false;

      // 1) 优先根据楼梯 + 墙 + 宽度判断"楼梯区 / 走廊"
      if (stairsCount > 0) {
        stairZone = true;
      }

      if ((leftWallStable || rightWallStable) && (corridorWidthM || widthM) <= 4.5) {
        corridorLike = true;
      }

      // 粗分：室内 vs 室外（很简化，但够用）
      // 有大量车辆 & 宽度大 → 街道 / 室外
      if (vehicleCount >= 2 && widthM >= 5.0) {
        indoor = false;
      } else if (chairCount > 0 || signCount > 0 || corridorLike || stairZone) {
        indoor = true;
      } else {
        // fallback：沿用 baseType 的室内/外特征
        indoor = (baseType.indexOf('indoor') !== -1 || baseType.indexOf('corridor') !== -1);
      }

      if (stairZone && corridorLike) {
        inferred = 'indoor_stair_corridor';
      } else if (stairZone && indoor) {
        inferred = 'indoor_stair_area';
      } else if (corridorLike && indoor) {
        inferred = 'indoor_corridor';
      } else if (!indoor && vehicleCount > 0) {
        inferred = 'street_roadside';
      } else if (!indoor && vehicleCount === 0 && widthM < 5.0) {
        inferred = 'street_sidewalk';
      } else if (indoor && widthM >= 6.0 && vehicleCount === 0 && stairsCount === 0) {
        inferred = 'indoor_open_area';
      } else {
        inferred = baseType || 'unknown';
      }

      this.lastSceneType = inferred;
      return {
        base_scene_type: baseType,
        inferred_scene_type: inferred,
        is_indoor: indoor,
        is_corridor_like: corridorLike,
        is_stair_zone: stairZone,
        widthM: corridorWidthM || widthM
      };
    }
  }

  // ---- 拓扑分析：左右区 / 中央区 / 密度 -----------------------------
  class TopologyAnalyzer {
    analyze(enhancedState, structureSnapshot) {
      const grid = enhancedState.grid || {};
      const widthM = typeof grid.width_m === 'number' ? grid.width_m : 4.0;
      const objects = enhancedState.objects || [];
      const pointGrid = enhancedState.pointGrid || [];

      // 分左右 + 中央区
      let leftDyn = 0, centerDyn = 0, rightDyn = 0;
      let leftStaticHaz = 0, centerStaticHaz = 0, rightStaticHaz = 0;
      let dynTotal = 0;

      const centerHalf = widthM * 0.4 / 2; // 中央区域宽度比例

      for (let i = 0; i < objects.length; i++) {
        const obj = objects[i];
        const bev = obj.bev || {};
        const x = typeof bev.x === 'number' ? bev.x : null;
        if (x === null) continue;

        const isDynamic =
          obj.pro_motion === 'approaching' ||
          obj.pro_motion === 'approaching_fast' ||
          obj.pro_motion === 'leaving' ||
          obj.pro_motion === 'leaving_fast' ||
          obj.pro_motion === 'crossing';

        const isStaticHazard = !!(obj.memory && obj.memory.is_static_hazard);

        let zone = 'center';
        if (Math.abs(x) <= centerHalf) zone = 'center';
        else if (x < 0) zone = 'left';
        else zone = 'right';

        if (isDynamic) {
          dynTotal++;
          if (zone === 'center') centerDyn++;
          else if (zone === 'left') leftDyn++;
          else rightDyn++;
        }

        if (isStaticHazard) {
          if (zone === 'center') centerStaticHaz++;
          else if (zone === 'left') leftStaticHaz++;
          else rightStaticHaz++;
        }
      }

      const forwardPoints = pointGrid.filter(p => typeof p.y === 'number' && p.y > 0 && p.y <= 5.0);
      const crowdDensity = dynTotal / Math.max(forwardPoints.length || 1, 1); // 简单比值

      let preferredSide = 'center';
      // 如果中央动态太多，尽量靠人少的一侧
      if (centerDyn > leftDyn && centerDyn > rightDyn) {
        if (leftDyn <= rightDyn) preferredSide = 'left';
        else preferredSide = 'right';
      } else if (centerDyn === 0 && (leftDyn > 0 || rightDyn > 0)) {
        // 中央无动态，人都在两边
        preferredSide = 'center';
      }

      const staticHazAhead = (centerStaticHaz + leftStaticHaz + rightStaticHaz) > 0;

      return {
        widthM: widthM,
        crowd_density: crowdDensity,  // 0 ~ N
        dynamic_distribution: {
          left: leftDyn,
          center: centerDyn,
          right: rightDyn
        },
        static_hazard_distribution: {
          left: leftStaticHaz,
          center: centerStaticHaz,
          right: rightStaticHaz
        },
        preferred_side: preferredSide,
        has_static_hazard_ahead: staticHazAhead
      };
    }
  }

  // ---- 场景状态机（高层状态：行走 / 转向 / 接近出口/楼梯） ---------
  class SceneStateMachine {
    constructor() {
      this.state = {
        phase: 'idle', // idle / walking / turning / approaching_stairs / at_stairs / crowded
        since: Date.now(),
        lastUpdate: Date.now()
      };
    }

    update(enhancedState, classification, topology) {
      const now = Date.now();
      const oldPhase = this.state.phase;
      const crowd = topology.crowd_density;
      const stairZone = classification.is_stair_zone;

      let newPhase = oldPhase;

      // 简单启发式状态机
      if (crowd > 1.5) {
        newPhase = 'crowded';
      } else if (stairZone) {
        // 有楼梯目标，且风险不是 low → 接近或处于楼梯区域
        const hazard = enhancedState.primary_hazard;
        if (hazard && (hazard.type || '').toLowerCase().indexOf('stair') !== -1) {
          if (hazard.distance != null && hazard.distance < 1.5) {
            newPhase = 'at_stairs';
          } else {
            newPhase = 'approaching_stairs';
          }
        } else {
          newPhase = 'approaching_stairs';
        }
      } else {
        // 非楼梯、非高人群
        // 看一下 dynamic object 的接近速度，粗略判断是否在行走中
        const objs = enhancedState.objects || [];
        let maxApproach = 0;
        for (let i = 0; i < objs.length; i++) {
          const ap = objs[i].pro_approach_speed || 0;
          if (ap > maxApproach) maxApproach = ap;
        }
        if (maxApproach > 0.05) {
          newPhase = 'walking';
        } else if (crowd > 0.2) {
          newPhase = 'walking';
        } else {
          newPhase = 'idle';
        }
      }

      if (newPhase !== oldPhase) {
        this.state.phase = newPhase;
        this.state.since = now;
        logInfo('SceneStateMachine: phase changed', {
          from: oldPhase,
          to: newPhase
        });
      }

      this.state.lastUpdate = now;
      return Object.assign({}, this.state);
    }
  }

  // ---- 主 Reasoner ---------------------------------------------------
  class SceneReasonerClass {
    constructor() {
      this.classifier = new SceneClassifier();
      this.topologyAnalyzer = new TopologyAnalyzer();
      this.stateMachine = new SceneStateMachine();
      this.lastContext = null;
    }

    /**
     * 主入口：由 EventFlowPro.onSpaceStateEnhanced 调用
     * @param {Object} enhancedState
     * @returns {Object|null} sceneContext
     */
    ingestEnhancedState(enhancedState) {
      try {
        if (!enhancedState || !enhancedState.grid) return null;

        // 1) 取结构记忆快照（如果有）
        let structureSnapshot = null;
        if (window.MapMemoryPro && typeof window.MapMemoryPro.getCurrentStructureSnapshot === 'function') {
          structureSnapshot = window.MapMemoryPro.getCurrentStructureSnapshot();
        }

        // 2) 场景分类
        const classification = this.classifier.classify(enhancedState, structureSnapshot);

        // 3) 拓扑分析
        const topology = this.topologyAnalyzer.analyze(enhancedState, structureSnapshot);

        // 4) 状态机更新
        const phaseState = this.stateMachine.update(enhancedState, classification, topology);

        // 5) 导出综合场景上下文
        const sceneContext = {
          ts: Date.now(),
          base_scene_type: classification.base_scene_type,
          inferred_scene_type: classification.inferred_scene_type,
          is_indoor: classification.is_indoor,
          is_corridor_like: classification.is_corridor_like,
          is_stair_zone: classification.is_stair_zone,
          widthM: classification.widthM,
          topology: topology,
          phase: phaseState.phase,
          phase_since: phaseState.since,
          // 导航建议：当前是否建议减速 / 哪侧更安全
          nav_hints: this._buildNavHints(enhancedState, classification, topology, phaseState),
          // 可选：结构快照摘要
          structure: structureSnapshot
        };

        this.lastContext = sceneContext;

        logDebug('SceneReasoner.context', {
          inferred_scene_type: sceneContext.inferred_scene_type,
          phase: sceneContext.phase,
          preferred_side: sceneContext.nav_hints.preferred_side,
          should_slow_down: sceneContext.nav_hints.should_slow_down
        });

        // 6) 分发：给导航、任务链、AutoRecovery 等模块使用
        this._dispatchSceneContext(sceneContext);

        return sceneContext;
      } catch (e) {
        logError('SceneReasoner.ingestEnhancedState error', {
          error: e.toString(),
          stack: e.stack
        });
        return null;
      }
    }

    _buildNavHints(enhancedState, classification, topology, phaseState) {
      const risk = enhancedState.overall_risk || 'low';
      const crowd = topology.crowd_density;
      const staticHaz = topology.has_static_hazard_ahead;
      const preferredSide = topology.preferred_side;
      const isStair = classification.is_stair_zone || phaseState.phase === 'approaching_stairs' || phaseState.phase === 'at_stairs';

      let shouldSlowDown = false;
      let cautionText = null;

      if (risk === 'high' || risk === 'critical') {
        shouldSlowDown = true;
        cautionText = '前方存在高风险，请减速并注意脚下。';
      } else if (isStair) {
        shouldSlowDown = true;
        cautionText = '前方是楼梯区域，请注意台阶高度。';
      } else if (crowd > 1.0) {
        shouldSlowDown = true;
        cautionText = '前方人较多，请放慢速度。';
      } else if (staticHaz) {
        shouldSlowDown = true;
        cautionText = '前方存在固定障碍物，请小心通过。';
      }

      return {
        preferred_side: preferredSide,        // 'left' / 'right' / 'center'
        should_slow_down: shouldSlowDown,
        caution_text: cautionText
      };
    }

    _dispatchSceneContext(sceneContext) {
      try {
        // 1) 导航状态机可以直接接收 scene_context
        if (window.NavigationFSM && typeof window.NavigationFSM.handleEvent === 'function') {
          window.NavigationFSM.handleEvent({
            type: 'scene_context_update',
            scene: sceneContext
          });
        }

        // 2) 任务链：如果需要减速或特别小心，可以发一个导航提示任务（低优先级）
        if (sceneContext.nav_hints && sceneContext.nav_hints.should_slow_down && sceneContext.nav_hints.caution_text) {
          if (window.taskChain && typeof window.taskChain.enqueue === 'function') {
            window.taskChain.enqueue({
              type: 'NAV_HINT',
              priority: 'MEDIUM',
              payload: {
                scene: {
                  inferred_scene_type: sceneContext.inferred_scene_type,
                  phase: sceneContext.phase
                },
                text: sceneContext.nav_hints.caution_text
              }
            });
          }
        }

        // 3) AutoRecovery 可用场景阶段监控稳定性
        if (window.AutoRecovery && typeof window.AutoRecovery.record === 'function') {
          window.AutoRecovery.record('scene_phase', sceneContext.phase, {
            inferred_scene_type: sceneContext.inferred_scene_type,
            should_slow_down: sceneContext.nav_hints.should_slow_down
          });
        }

        // 4) 如有 emotion_event，可以记录"环境状态"对情绪的影响（预留）
        if (window.emotion_event) {
          const sev = sceneContext.nav_hints.should_slow_down ? 'elevated' : 'normal';
          window.emotion_event('scene_update', sev, {
            inferred_scene_type: sceneContext.inferred_scene_type,
            phase: sceneContext.phase
          });
        }

        // 5) 如有后台日志上传，可上传结构化场景信息
        if (window.uploadLunaLog) {
          window.uploadLunaLog('scene_context', sceneContext);
        }
      } catch (e) {
        logError('SceneReasoner._dispatchSceneContext error', {
          error: e.toString(),
          stack: e.stack
        });
      }
    }

    getLastContext() {
      return this.lastContext;
    }
  }

  window.SceneReasoner = new SceneReasonerClass();

  // 全局调试函数
  window.debugSceneContext = function () {
    if (!window.SceneReasoner) return null;
    const ctx = window.SceneReasoner.getLastContext();
    logInfo('SceneReasoner lastContext', ctx);
    return ctx;
  };

  if (window.logInfo) {
    window.logInfo('SceneReasoner模块加载完成', { module: 'scene_reasoner' });
  } else {
    console.log('✅ SceneReasoner模块加载完成', { module: 'scene_reasoner' });
  }
})();


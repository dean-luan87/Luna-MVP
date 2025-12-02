// frontend/event_flow_pro.js
/**
 * EventFlowPro / 事件流 Pro 版
 * Pro 版事件流：接收 enhancedState，联动导航 / 任务链 / TTS，并把记忆变化、危险判断写入日志
 */
(function () {
  'use strict';
  
  if (window.EventFlowPro) return;

  function logInfo(msg, payload) {
    if (window.logInfo) window.logInfo(msg, payload);
    else console.log('[EventFlowPro]', msg, payload || '');
  }

  function logDebug(msg, payload) {
    if (window.logDebug) window.logDebug(msg, payload);
    else console.debug('[EventFlowPro]', msg, payload || '');
  }

  function logError(msg, payload) {
    if (window.logError) window.logError(msg, payload);
    else console.error('[EventFlowPro]', msg, payload || '');
  }

  function emitTask(task) {
    if (window.taskChain && typeof window.taskChain.enqueue === 'function') {
      window.taskChain.enqueue(task);
    } else {
      logDebug('EventFlowPro: taskChain not available, skip enqueue', task);
    }
  }

  const EventFlowPro = {
    /**
     * 主入口：由 SpatialEnginePro 调用
     * @param {Object} enhancedState
     */
    onSpaceStateEnhanced: function (enhancedState) {
      if (!enhancedState) return;

      // === 保证 NavigationFSM 已初始化 ===
      if (!window.NavigationFSM) {
        console.warn("⚠️ EventFlowPro: NavigationFSM 未初始化 → 自动创建");
        window.NavigationFSM = { initialized: true, state: "IDLE" };
      } else if (!window.NavigationFSM.initialized) {
        window.NavigationFSM.initialized = true;
        window.NavigationFSM.state = window.NavigationFSM.state || "IDLE";
        console.log("✅ NavigationFSM 自动初始化完成 (EventFlowPro)");
      }

      try {
        logDebug('EventFlowPro.onSpaceStateEnhanced', {
          scene_type: enhancedState.scene_type,
          overall_risk: enhancedState.overall_risk,
          object_count: (enhancedState.objects || []).length
        });

        // 1) 先把 enhancedState 给 MapMemoryPro
        if (window.MapMemoryPro && typeof window.MapMemoryPro.ingestEnhancedState === 'function') {
          window.MapMemoryPro.ingestEnhancedState(enhancedState, {
            placeId: 'session_default'
          });
        }

        // ✅ 1.5) SceneReasoner 场景推理（在 MapMemoryPro 之后、导航之前）
        let sceneContext = null;
        if (window.SceneReasoner && typeof window.SceneReasoner.ingestEnhancedState === 'function') {
          sceneContext = window.SceneReasoner.ingestEnhancedState(enhancedState);
        }

        // ✅ 1.6) StructureAnalyzer + TopologyBuilder + BottleneckDetector 结构推理
        let structureInfo = null;
        let topologyInfo = null;
        let bottleneckInfo = null;
        
        if (window.StructureAnalyzer && typeof window.StructureAnalyzer.analyze === 'function') {
          structureInfo = window.StructureAnalyzer.analyze(enhancedState);
          
          if (structureInfo && window.TopologyBuilder && typeof window.TopologyBuilder.build === 'function') {
            topologyInfo = window.TopologyBuilder.build(structureInfo);
            
            if (topologyInfo && window.BottleneckDetector && typeof window.BottleneckDetector.detect === 'function') {
              bottleneckInfo = window.BottleneckDetector.detect(structureInfo, topologyInfo);
            }
          }
        }

        // ✅ 1.7) PathFeasibility 路径可行性分析（在结构推理之后）
        let pathHints = null;
        if (window.PathFeasibility && typeof window.PathFeasibility.analyze === 'function') {
          const structureSnapshot = window.MapMemoryPro && typeof window.MapMemoryPro.getCurrentStructureSnapshot === 'function' 
            ? window.MapMemoryPro.getCurrentStructureSnapshot() 
            : null;
          pathHints = window.PathFeasibility.analyze(enhancedState, structureSnapshot);
        }

        // ✅ 1.8) ActionGuidance 动作级导航引擎（在获取所有信息之后）
        if (window.ActionGuidance && sceneContext && pathHints) {
          const actions = window.ActionGuidance.deriveActions(
            sceneContext,
            pathHints,
            structureInfo,
            topologyInfo,
            bottleneckInfo
          );
          if (actions && actions.length > 0) {
            window.ActionGuidance.dispatch(actions);
          }
        }

        // 2) 危险判断：如果存在高风险或关键危险对象，走统一任务链
        this._handleHazardAndRisk(enhancedState, sceneContext, pathHints);

        // 3) 导航状态机更新（带路径建议和结构信息）
        this._updateNavigationFSM(enhancedState, sceneContext, pathHints, structureInfo, topologyInfo, bottleneckInfo);

        // 4) Waypoint 进度更新
        this._updateWaypointProgress(enhancedState);

        // 5) AutoRecovery 状态记录
        this._updateAutoRecovery(enhancedState);
      } catch (e) {
        logError('EventFlowPro.onSpaceStateEnhanced error', {
          error: e.toString(),
          stack: e.stack
        });
      }
    },

    _handleHazardAndRisk: function (enhancedState, sceneContext, pathHints) {
      const risk = enhancedState.overall_risk || 'low';
      const hazard = enhancedState.primary_hazard || null;

      // 如果有主危险体，构造统一危险任务
      if (hazard && risk !== 'low') {
        // ✅ 使用 SpatialSemantic 生成危险文本
        let hazardText = '';
        if (window.SpatialSemantic && typeof window.SpatialSemantic.buildHazardText === 'function') {
          hazardText = window.SpatialSemantic.buildHazardText(hazard, enhancedState);
        }

        const hazardTask = {
          type: 'HAZARD_WARNING',
          priority: 'CRITICAL',
          payload: {
            scene_type: enhancedState.scene_type,
            risk_level: risk,
            hazard: hazard,
            enhancedState: enhancedState,
            hazard_text: hazardText  // ✅ 语义化文本
          }
        };
        emitTask(hazardTask);

        // ✅ 优先通过 MemoryAwareVoice，否则回落到 SpeechRhythm
        if (window.MemoryAwareVoice && typeof window.MemoryAwareVoice.handleTask === 'function') {
          window.MemoryAwareVoice.handleTask(hazardTask);
        } else if (window.SpeechRhythm && typeof window.SpeechRhythm.handleTask === 'function') {
          window.SpeechRhythm.handleTask(hazardTask);
        }

        logInfo('EventFlowPro: hazard detected', {
          scene_type: enhancedState.scene_type,
          risk_level: risk,
          hazard_type: hazard.type,
          distance: hazard.distance,
          motion: hazard.pro_motion || hazard.motion
        });

        if (window.emotion_event) {
          window.emotion_event('hazard_detected', risk, {
            hazard_type: hazard.type,
            scene_type: enhancedState.scene_type
          });
        }
      } else {
        // 无明显主危险体，但可以根据结构记忆温和提示
        if (window.MapMemoryPro) {
          const structure = window.MapMemoryPro.getCurrentStructureSnapshot();
          if (structure && (structure.leftWallStable || structure.rightWallStable)) {
            logDebug('EventFlowPro: structure context', {
              corridorWidthM: structure.corridorWidthM,
              leftWallStable: structure.leftWallStable,
              rightWallStable: structure.rightWallStable
            });
          }
        }
      }
    },

    _updateNavigationFSM: function (enhancedState, sceneContext, pathHints, structureInfo, topologyInfo, bottleneckInfo) {
      if (window.NavigationFSM && typeof window.NavigationFSM.handleEvent === 'function') {
        const eventData = {
          type: 'space_update_enhanced',
          spaceState: enhancedState
        };

        // ✅ 如果有场景上下文，添加到事件中
        if (sceneContext) {
          eventData.sceneContext = sceneContext;
        }

        // ✅ 如果有路径建议，添加到事件中
        if (pathHints) {
          eventData.pathHints = pathHints;
        }

        // ✅ 如果有结构信息，添加到事件中
        if (structureInfo) {
          eventData.structureInfo = structureInfo;
        }
        if (topologyInfo) {
          eventData.topologyInfo = topologyInfo;
        }
        if (bottleneckInfo) {
          eventData.bottleneckInfo = bottleneckInfo;
        }

        window.NavigationFSM.handleEvent(eventData);
      } else {
        logDebug('EventFlowPro: NavigationFSM not available');
      }

      // ✅ 如果有导航提示（场景上下文 + 路径建议），生成 NAV_HINT 任务
      if (sceneContext && pathHints) {
        let navHintText = '';
        if (window.SpatialSemantic && typeof window.SpatialSemantic.buildNavHintText === 'function') {
          navHintText = window.SpatialSemantic.buildNavHintText(sceneContext, pathHints);
        } else if (sceneContext.nav_hints && sceneContext.nav_hints.caution_text) {
          navHintText = sceneContext.nav_hints.caution_text;
        }

        if (navHintText) {
          const navHintTask = {
            type: 'NAV_HINT',
            priority: 'HIGH',
            payload: {
              text: navHintText,
              sceneContext: sceneContext,
              pathHints: pathHints,
              // ✅ 注入结构数据到 taskChain payload
              structureInfo: structureInfo,
              topologyInfo: topologyInfo,
              bottleneck: bottleneckInfo
            }
          };
          emitTask(navHintTask);

          // ✅ 优先通过 MemoryAwareVoice，否则回落到 SpeechRhythm
          if (window.MemoryAwareVoice && typeof window.MemoryAwareVoice.handleTask === 'function') {
            window.MemoryAwareVoice.handleTask(navHintTask);
          } else if (window.SpeechRhythm && typeof window.SpeechRhythm.handleTask === 'function') {
            window.SpeechRhythm.handleTask(navHintTask);
          }
        }
      }

      // ✅ 将结构数据写入 logger 发送到后台
      if (structureInfo || topologyInfo || bottleneckInfo) {
        const structureLog = {
          ts: Date.now(),
          structureInfo: structureInfo,
          topologyInfo: topologyInfo,
          bottleneckInfo: bottleneckInfo
        };

        logInfo('EventFlowPro: structure analysis', structureLog);

        // 如果有后台日志上传接口，上传结构数据
        if (window.uploadLunaLog && typeof window.uploadLunaLog === 'function') {
          window.uploadLunaLog('structure_analysis', structureLog);
        }
      }
    },

    _updateWaypointProgress: function (enhancedState) {
      if (window.WaypointManager && typeof window.WaypointManager.checkProgress === 'function') {
        window.WaypointManager.checkProgress({
          spaceState: enhancedState
        });
      } else {
        logDebug('EventFlowPro: WaypointManager not available');
      }
    },

    _updateAutoRecovery: function (enhancedState) {
      if (!window.AutoRecovery || typeof window.AutoRecovery.record !== 'function') return;

      const risk = enhancedState.overall_risk || 'low';
      let label = 'stable';
      if (risk === 'medium') label = 'elevated_risk';
      else if (risk === 'high' || risk === 'critical') label = 'high_risk';

      window.AutoRecovery.record('navigation_pro', label, {
        scene_type: enhancedState.scene_type,
        overall_risk: risk
      });
    }
  };

  window.EventFlowPro = EventFlowPro;

  if (window.logInfo) {
    window.logInfo('EventFlowPro模块加载完成', { module: 'event_flow_pro' });
  } else {
    console.log('✅ EventFlowPro模块加载完成', { module: 'event_flow_pro' });
  }
})();


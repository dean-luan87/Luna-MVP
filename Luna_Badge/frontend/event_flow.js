// frontend/event_flow.js
/**
 * 视觉 × 导航 × 语音总管线
 * 把 VisionEnhancer → EventBridge → NavigationStrategy → TTS / UI / emotion_event 串成统一的总线
 */
(function () {
  'use strict';
  
  if (window.EventFlow) return;

  const EventFlow = {
    onVisionSummary(summary) {
      if (!summary) return;

      // === 保证 NavigationFSM 已初始化 ===
      if (!window.NavigationFSM) {
        console.warn("⚠️ EventFlow: NavigationFSM 未初始化 → 自动创建");
        window.NavigationFSM = { initialized: true, state: "IDLE" };
      } else if (!window.NavigationFSM.initialized) {
        window.NavigationFSM.initialized = true;
        window.NavigationFSM.state = window.NavigationFSM.state || "IDLE";
        console.log("✅ NavigationFSM 自动初始化完成 (EventFlow)");
      }

      // 1. 日志记录
      if (window.logDebug) {
        window.logDebug('EventFlow.onVisionSummary', summary);
      }

      // 2. 危险流：如果稳定危险 → 派发 hazard 事件
      if (summary.isDangerStable && !summary.dangerSuppressed) {
        const payload = {
          type: 'vision_hazard',
          scene: summary.scene,
          riskLevel: summary.riskLevel,
          closestDanger: summary.closestDanger,
          hazards: summary.hazards
        };
        
        if (window.emitHazardEvent) {
          window.emitHazardEvent(payload);
        }
        
        if (window.emotion_event) {
          window.emotion_event('hazard_detected', 'high', payload);
        }
      }

      // 3. 导航流：始终发送导航"环境信息"，用于策略与路点系统
      const navPayload = {
        scene: summary.scene,
        riskLevel: summary.riskLevel,
        closestDanger: summary.closestDanger,
        hasDanger: summary.hasDangerFrame,
        rawDetections: summary.rawDetections
      };

      if (window.emitNavigationEvent) {
        window.emitNavigationEvent(navPayload);
      }

      // 4. AutoRecovery：视觉异常时可记录
      if (window.AutoRecovery && summary.riskLevel === 'low' && !summary.hasDangerFrame) {
        if (window.AutoRecovery.record) {
          window.AutoRecovery.record('vision', 'stable', { ts: summary.ts });
        }
      }

      // 5. SpaceEngine 空间状态处理（如果 summary 中包含 space_state）
      if (summary.space_state && window.EventFlow.onSpaceState) {
        window.EventFlow.onSpaceState(summary.space_state);
      }
    },

    onSpaceState(spaceState) {
      if (!spaceState) return;

      // === 保证 NavigationFSM 已初始化 ===
      if (!window.NavigationFSM) {
        console.warn("⚠️ EventFlow: NavigationFSM 未初始化 → 自动创建");
        window.NavigationFSM = { initialized: true, state: "IDLE" };
      } else if (!window.NavigationFSM.initialized) {
        window.NavigationFSM.initialized = true;
        window.NavigationFSM.state = window.NavigationFSM.state || "IDLE";
        console.log("✅ NavigationFSM 自动初始化完成 (EventFlow)");
      }

      // ✅ 优先调用 SpatialEnginePro（Pro 版增强层）
      if (window.SpatialEnginePro) {
        window.SpatialEnginePro.ingestSpaceState(spaceState);
        return; // Pro 版会自己处理后续流程
      }

      // 只有在 Pro 不存在时，才走旧逻辑
      if (window.logDebug) {
        window.logDebug('EventFlow.onSpaceState', {
          scene_type: spaceState.scene_type,
          overall_risk: spaceState.overall_risk,
          has_primary: !!spaceState.primary_hazard
        });
      }

      // 1) 危险事件：核心危险体 + 总体风险
      if (spaceState.primary_hazard && spaceState.overall_risk !== 'low') {
        const h = spaceState.primary_hazard;
        const payload = {
          type: 'space_hazard',
          scene_type: spaceState.scene_type,
          risk_level: spaceState.overall_risk,
          hazard: h
        };
        
        if (window.emitHazardEvent) {
          window.emitHazardEvent(payload);
        }
        
        if (window.emotion_event) {
          window.emotion_event('hazard_detected', spaceState.overall_risk, payload);
        }
      }

      // 2) 导航状态机：把空间更新丢给 NavigationFSM
      if (window.NavigationFSM && typeof window.NavigationFSM.handleEvent === 'function') {
        window.NavigationFSM.handleEvent({
          type: 'space_update',
          spaceState: spaceState
        });
      }

      // 3) 路点系统：根据空间状态检查进度
      if (window.WaypointManager && typeof window.WaypointManager.checkProgress === 'function') {
        window.WaypointManager.checkProgress({
          spaceState: spaceState
        });
      }

      // 4) 如果有地图记忆中的静态危险点，且当前整体风险为 low/medium，也可以做"记忆驱动的温和提示"
      try {
        if (window.MapMemory && spaceState.grid && spaceState.objects && spaceState.objects.length) {
          const staticHazards = [];

          for (let i = 0; i < spaceState.objects.length; i++) {
            const obj = spaceState.objects[i];
            if (obj.memory && obj.memory.is_static_hazard) {
              staticHazards.push(obj);
            }
          }

          if (staticHazards.length > 0) {
            // 记忆层面的危险，哪怕 YOLO 当前帧没报高风险，也可以轻声提醒
            if (window.logInfo) {
              window.logInfo('EventFlow: memory-driven static hazard detected', {
                count: staticHazards.length,
                examples: staticHazards.slice(0, 3)
              });
            }

            // 可以选择通过 taskChain/tts 做温和提示，这里只触发一个导航事件，具体 TTS 策略留在现有逻辑
            if (window.emitNavigationEvent) {
              window.emitNavigationEvent({
                type: 'memory_static_hazard',
                hazards: staticHazards
              });
            }
          }
        }
      } catch (e) {
        if (window.logError) {
          window.logError('EventFlow.onSpaceState memory logic error', {
            error: e.toString(),
            stack: e.stack
          });
        }
      }

      // 5) AutoRecovery 记录低/高风险状态（便于后端分析卡顿/误报）
      if (window.AutoRecovery && typeof window.AutoRecovery.record === 'function') {
        let statusLabel = 'stable';
        if (spaceState.overall_risk === 'high' || spaceState.overall_risk === 'critical') {
          statusLabel = 'high_risk';
        }
        window.AutoRecovery.record('navigation', statusLabel, {
          overall_risk: spaceState.overall_risk,
          scene_type: spaceState.scene_type
        });
      }
    }
  };

  window.EventFlow = EventFlow;
  console.log('✅ EventFlow模块加载完成', { module: 'event_flow' });
})();



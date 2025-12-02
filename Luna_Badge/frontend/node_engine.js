// node_engine.js
// 节点总控引擎：整合推理 + 记忆 + 用户修正接口

(function () {
  'use strict';

  function log(event, payload) {
    if (window.__lunaLog) {
      window.__lunaLog(event, payload);
    } else {
      // console.log('[NodeEngine]', event, payload);
    }
  }

  // 简单 region 获取方式：你可以在别处维护 window.currentRegionId
  function getCurrentRegionId() {
    if (typeof window.getCurrentRegionId === 'function') {
      return window.getCurrentRegionId();
    }
    if (window.currentRegionId) return window.currentRegionId;
    return 'default';
  }

  /**
   * 用于在每一帧视觉分析时调用
   * frame: { yoloObjects, ocrText, positionHint? }
   */
  function processFrame(frame) {
    const regionId = frame.regionId || getCurrentRegionId();
    if (!window.NodeInference || !window.NodeMemory) {
      log('node_engine_missing_dependency', {
        hasInference: !!window.NodeInference,
        hasMemory: !!window.NodeMemory
      });
      return;
    }

    const candidates = window.NodeInference.inferNodes({
      regionId,
      yoloObjects: frame.yoloObjects,
      ocrText: frame.ocrText,
      positionHint: frame.positionHint || null
    });

    const storedNodes = [];

    for (const c of candidates) {
      // 使用动态更新机制处理节点（区分固定节点和临时节点）
      let node = null;
      if (window.NodeDynamicUpdate && window.NodeDynamicUpdate.processNodeUpdate) {
        // 生成简单的视觉特征（基于 role + type + position）
        const visualFeature = `${c.role}_${c.type}_${c.position ? `${c.position.x}_${c.position.y}` : ''}`;
        node = window.NodeDynamicUpdate.processNodeUpdate(regionId, {
          type: c.type,
          role: c.role,
          confidence: c.confidence,
          position: c.position,
          source: c.source,
          meta: c.meta
        }, visualFeature);
      } else {
        // 降级：直接使用 NodeMemory
        node = window.NodeMemory.addOrUpdateNode(regionId, {
          type: c.type,
          role: c.role,
          confidence: c.confidence,
          position: c.position,
          source: c.source,
          meta: c.meta
        });
      }
      
      if (node) {
        storedNodes.push(node);
        
        // 如果是固定节点，尝试重定位
        if (!node.is_temporary && window.NodeRelocalization && window.NodeRelocalization.relocalize) {
          window.NodeRelocalization.relocalize(regionId, node, frame.positionHint);
        }
      }
    }

    if (storedNodes.length) {
      log('node_engine_frame_processed', {
        regionId,
        createdNodes: storedNodes.map(n => ({
          id: n.id,
          role: n.role,
          confidence: n.confidence,
          source: n.source
        }))
      });
      
      // ✅ MiniMap 集成：添加节点到小地图
      if (window.MiniMap && storedNodes.length > 0) {
        const sample = storedNodes.slice(0, 3); // 取前3个示例节点
        sample.forEach(n => {
          window.MiniMap.addNode({
            type: n.type,
            role: n.role,
            label: (n.meta && n.meta.displayName) || n.role || "节点"
          });
        });
      }
      
      // ✅ E4: 自动区域识别 - 输入节点特征
      if (window.ZoneAutoDetector && storedNodes.length > 0) {
        storedNodes.forEach(n => {
          window.ZoneAutoDetector.feedNode({
            label: (n.meta && n.meta.displayName) || n.role || "节点",
            role: n.role,
            type: n.type
          });
        });
      }
    }
    return storedNodes;
  }

  /**
   * 获取当前区域下的节点，给导航 / 任务链用
   */
  function getNodesForNavigation(filter) {
    const regionId = getCurrentRegionId();
    if (!window.NodeMemory) return [];
    return window.NodeMemory.getNodes(regionId, filter || {});
  }

  /**
   * 用户确认 / 修正节点（例如语音："这是挂号窗口"）
   * options: { nodeId, correct, newRole?, newName? }
   */
  function userConfirmNode(options) {
    const regionId = getCurrentRegionId();
    if (!window.NodeMemory) return null;

    const updated = window.NodeMemory.recordUserFeedback(regionId, options.nodeId, {
      correct: options.correct,
      newRole: options.newRole,
      newName: options.newName
    });

    if (updated) {
      log('node_engine_user_confirm', {
        regionId,
        node: {
          id: updated.id,
          role: updated.role,
          confidence: updated.confidence
        }
      });
    }
    return updated;
  }

  /**
   * 供上层调用：获取当前区域快照（例如日志上传 / 调试）
   */
  function getRegionSnapshot() {
    const regionId = getCurrentRegionId();
    if (!window.NodeMemory) return null;
    return window.NodeMemory.getRegionSnapshot(regionId);
  }

  // 暴露统一入口
  window.NodeEngine = {
    processFrame,
    getNodesForNavigation,
    userConfirmNode,
    getRegionSnapshot
  };

  // 为方便调用，再挂一个别名
  window.LunaNodes = window.LunaNodes || {};
  window.LunaNodes.processFrame = processFrame;
  window.LunaNodes.userConfirmNode = userConfirmNode;
  window.LunaNodes.getNodesForNavigation = getNodesForNavigation;
  window.LunaNodes.getRegionSnapshot = getRegionSnapshot;

})();


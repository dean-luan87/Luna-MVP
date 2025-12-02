// node_dynamic_update.js
// 视觉节点的动态更新机制：固定节点更新 + 临时节点管理

(function () {
  'use strict';

  function log(event, payload) {
    if (window.__lunaLog) {
      window.__lunaLog(event, payload);
    }
  }

  // 临时节点类型（不写入长期记忆）
  const TEMPORARY_NODE_TYPES = ['施工', '积水', '移动障碍', '临时摊位', 'construction', 'water', 'temporary'];
  
  // 固定节点更新阈值
  const DRIFT_THRESHOLD = 2.0; // drift_score 超过此值才更新位置
  const POSITION_TOLERANCE = 0.5; // 位置偏移容忍度（米）

  // Session 临时节点缓存
  let currentSessionId = null;
  let sessionTempNodes = [];

  function getCurrentSessionId() {
    if (!currentSessionId) {
      currentSessionId = 'session-' + Date.now();
      log('session_started', { sessionId: currentSessionId });
    }
    return currentSessionId;
  }

  /**
   * 判断节点是否为临时节点
   */
  function isTemporaryNode(node) {
    const type = (node.type || '').toLowerCase();
    const role = (node.role || '').toLowerCase();
    return TEMPORARY_NODE_TYPES.some(t => 
      type.includes(t.toLowerCase()) || role.includes(t.toLowerCase())
    );
  }

  /**
   * 处理节点更新（固定节点 vs 临时节点）
   */
  function processNodeUpdate(regionId, nodeData, visualFeature = null) {
    if (!window.NodeMemory) {
      log('node_update_no_memory', {});
      return null;
    }

    // 判断是否为临时节点
    const isTemp = isTemporaryNode(nodeData);
    nodeData.is_temporary = isTemp;

    // 如果有视觉特征，添加进去
    if (visualFeature) {
      nodeData.visual_feature = visualFeature;
    }

    // 临时节点：只加入 session 缓存，不写入长期记忆
    if (isTemp) {
      const sessionId = getCurrentSessionId();
      const tempNode = {
        ...nodeData,
        sessionId,
        detectedAt: Date.now()
      };
      sessionTempNodes.push(tempNode);
      log('temp_node_detected', { sessionId, node: tempNode });
      return tempNode;
    }

    // 固定节点：检查是否需要更新
    const existing = window.NodeMemory.getNodes(regionId, { 
      role: nodeData.role,
      type: nodeData.type 
    }).find(n => {
      // 简单匹配：同 role + 同 type + 位置相近
      if (n.role !== nodeData.role || n.type !== nodeData.type) return false;
      if (n.position && nodeData.position) {
        const dist = window.NodeMemory.calculateDistance(n.position, nodeData.position);
        return dist < 3.0; // 3米内认为是同一个节点
      }
      return false;
    });

    if (existing) {
      // 检查是否需要更新
      const needsUpdate = checkIfNeedsUpdate(existing, nodeData);
      
      if (needsUpdate) {
        // 应用更新
        const updated = applyNodeUpdate(regionId, existing.id, nodeData);
        log('node_updated_by_observation', { 
          regionId, 
          nodeId: existing.id, 
          driftScore: updated.drift_score,
          version: updated.version 
        });
        return updated;
      } else {
        // 不需要更新，只增加确认次数
        existing.confirmations = (existing.confirmations || 0) + 1;
        return existing;
      }
    } else {
      // 新节点，直接添加
      return window.NodeMemory.addOrUpdateNode(regionId, nodeData);
    }
  }

  /**
   * 检查节点是否需要更新
   */
  function checkIfNeedsUpdate(existing, newData) {
    // 检查位置偏移
    if (existing.position && newData.position) {
      const dist = window.NodeMemory.calculateDistance(existing.position, newData.position);
      if (dist > POSITION_TOLERANCE) {
        return true; // 位置偏移超过阈值
      }
    }

    // 检查视觉特征变化
    if (existing.visual_feature && newData.visual_feature) {
      if (existing.visual_feature !== newData.visual_feature) {
        return true; // 视觉特征变化
      }
    }

    // 检查 drift_score 是否超过阈值
    const currentDrift = (existing.drift_score || 0);
    if (currentDrift > DRIFT_THRESHOLD) {
      return true; // 累计偏移超过阈值
    }

    return false;
  }

  /**
   * 应用节点更新
   */
  function applyNodeUpdate(regionId, nodeId, newData) {
    const region = window.NodeMemory.ensureRegion(regionId);
    const node = region.nodes[nodeId];
    if (!node) return null;

    // 更新位置
    if (newData.position) {
      node.position = newData.position;
    }

    // 更新视觉特征
    if (newData.visual_feature) {
      node.visual_feature = newData.visual_feature;
    }

    // 增加版本号
    node.version = (node.version || 1) + 1;
    node.updatedBy = 'observation';
    node.updatedAt = Date.now();

    // 重置 drift_score（已应用更新）
    node.drift_score = 0;

    log('node_update_applied', { regionId, nodeId, version: node.version });
    return node;
  }

  /**
   * 获取当前 session 的临时节点
   */
  function getSessionTempNodes(sessionId = null) {
    const sid = sessionId || getCurrentSessionId();
    return sessionTempNodes.filter(n => n.sessionId === sid);
  }

  /**
   * 清除 session 临时节点
   */
  function clearSessionTempNodes(sessionId = null) {
    const sid = sessionId || getCurrentSessionId();
    const count = sessionTempNodes.length;
    sessionTempNodes = sessionTempNodes.filter(n => n.sessionId !== sid);
    log('session_temp_nodes_cleared', { sessionId: sid, clearedCount: count });
  }

  /**
   * 结束当前 session
   */
  function endSession() {
    if (currentSessionId) {
      log('session_ended', { sessionId: currentSessionId, tempNodesCount: sessionTempNodes.length });
      clearSessionTempNodes(currentSessionId);
      currentSessionId = null;
    }
  }

  window.NodeDynamicUpdate = {
    processNodeUpdate,
    isTemporaryNode,
    getSessionTempNodes,
    clearSessionTempNodes,
    endSession,
    getCurrentSessionId
  };

})();


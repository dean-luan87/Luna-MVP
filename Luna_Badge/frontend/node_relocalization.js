// node_relocalization.js
// 图像节点 × 地图的实时校正（Re-Localization）

(function () {
  'use strict';

  function log(event, payload) {
    if (window.__lunaLog) {
      window.__lunaLog(event, payload);
    }
  }

  // 位置校正阈值
  const POSITION_TOLERANCE = 2.0; // 米，超过此值才校正地图
  const MIN_CONFIDENCE = 0.7; // 节点置信度阈值

  // 当前估计位置
  let currentEstimatedPosition = null;
  let lastRelocalizationTime = 0;
  const RELOCALIZATION_COOLDOWN = 2000; // 2秒冷却

  /**
   * 实时校正：根据观察到的节点修正当前位置和地图
   */
  function relocalize(regionId, observedNode, cameraPosition = null) {
    if (!window.NodeMemory) {
      log('relocalize_no_memory', {});
      return null;
    }

    const now = Date.now();
    if (now - lastRelocalizationTime < RELOCALIZATION_COOLDOWN) {
      return null; // 冷却中
    }

    // 查找匹配的已记录节点
    const storedNodes = window.NodeMemory.getNodes(regionId, {
      role: observedNode.role,
      type: observedNode.type,
      minConfidence: MIN_CONFIDENCE
    });

    if (storedNodes.length === 0) {
      return null; // 没有匹配的节点
    }

    // 找到最匹配的节点（位置相近 + 角色相同）
    let bestMatch = null;
    let minDistance = Infinity;

    for (const stored of storedNodes) {
      if (!stored.position || !observedNode.position) continue;
      
      const dist = window.NodeMemory.calculateDistance(stored.position, observedNode.position);
      if (dist < minDistance) {
        minDistance = dist;
        bestMatch = stored;
      }
    }

    if (!bestMatch || minDistance > POSITION_TOLERANCE) {
      return null; // 没有足够匹配的节点
    }

    // 计算位置偏移
    const offset = {
      x: observedNode.position.x - bestMatch.position.x,
      y: observedNode.position.y - bestMatch.position.y
    };

    // 如果偏移超过阈值，应用地图校正
    if (minDistance > POSITION_TOLERANCE) {
      const adjustment = applyMapAdjustment(regionId, bestMatch, offset);
      log('relocalization_applied', {
        regionId,
        nodeId: bestMatch.id,
        offset,
        distance: minDistance,
        adjustment
      });
      lastRelocalizationTime = now;
      return adjustment;
    }

    // 偏移在容忍范围内，只更新当前位置估计
    currentEstimatedPosition = {
      x: bestMatch.position.x,
      y: bestMatch.position.y,
      confidence: bestMatch.confidence,
      nodeId: bestMatch.id
    };

    log('relocalization_position_updated', {
      regionId,
      position: currentEstimatedPosition
    });

    return { adjusted: false, position: currentEstimatedPosition };
  }

  /**
   * 应用地图调整（微调局部路径）
   */
  function applyMapAdjustment(regionId, anchorNode, offset) {
    // 简化版：只调整锚点节点附近的其他节点
    const region = window.NodeMemory.ensureRegion(regionId);
    const nodes = Object.values(region.nodes);
    const adjustedCount = 0;
    const maxAdjustDistance = 5.0; // 只调整5米内的节点

    // 找到锚点附近的节点
    const nearbyNodes = nodes.filter(n => {
      if (n.id === anchorNode.id) return false;
      if (!n.position) return false;
      const dist = window.NodeMemory.calculateDistance(anchorNode.position, n.position);
      return dist < maxAdjustDistance;
    });

    // 微调附近节点的位置（按距离加权）
    for (const node of nearbyNodes) {
      const dist = window.NodeMemory.calculateDistance(anchorNode.position, node.position);
      const weight = 1 - (dist / maxAdjustDistance); // 距离越近权重越大
      
      if (node.position) {
        node.position.x = (node.position.x || 0) + offset.x * weight * 0.3; // 只调整30%
        node.position.y = (node.position.y || 0) + offset.y * weight * 0.3;
        node.updatedAt = Date.now();
        node.adjustedBy = 'relocalization';
      }
    }

    log('map_adjustment_applied', {
      regionId,
      anchorNodeId: anchorNode.id,
      adjustedNodesCount: nearbyNodes.length,
      offset
    });

    return {
      adjusted: true,
      anchorNodeId: anchorNode.id,
      adjustedNodesCount: nearbyNodes.length,
      offset
    };
  }

  /**
   * 获取当前估计位置
   */
  function getCurrentPosition() {
    return currentEstimatedPosition;
  }

  /**
   * 设置当前估计位置（手动设置）
   */
  function setCurrentPosition(position) {
    currentEstimatedPosition = position;
    log('position_set_manually', { position });
  }

  /**
   * 快速定位：匹配摄像头画面到最近视觉节点
   */
  function quickLocalize(regionId, observedNodes) {
    if (!observedNodes || observedNodes.length === 0) return null;

    const storedNodes = window.NodeMemory.getNodes(regionId, { minConfidence: MIN_CONFIDENCE });
    if (storedNodes.length === 0) return null;

    // 找到匹配最多的节点
    let bestMatch = null;
    let maxMatches = 0;

    for (const stored of storedNodes) {
      const matches = observedNodes.filter(obs => 
        obs.role === stored.role && 
        obs.type === stored.type &&
        obs.confidence >= MIN_CONFIDENCE
      ).length;

      if (matches > maxMatches) {
        maxMatches = matches;
        bestMatch = stored;
      }
    }

    if (bestMatch && maxMatches >= 1) {
      currentEstimatedPosition = {
        x: bestMatch.position?.x || 0,
        y: bestMatch.position?.y || 0,
        confidence: bestMatch.confidence,
        nodeId: bestMatch.id
      };
      log('quick_localize_success', {
        regionId,
        nodeId: bestMatch.id,
        matches: maxMatches
      });
      return currentEstimatedPosition;
    }

    return null;
  }

  window.NodeRelocalization = {
    relocalize,
    getCurrentPosition,
    setCurrentPosition,
    quickLocalize
  };

})();


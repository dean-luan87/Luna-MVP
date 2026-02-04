// navigation_accelerator.js
// 节点 × 路线 × 视觉记忆 三合一的加速导航

(function () {
  'use strict';

  function log(event, payload) {
    if (window.__lunaLog) {
      window.__lunaLog(event, payload);
    }
  }

  // 当前导航状态
  let currentNavigation = {
    active: false,
    from: null,
    to: null,
    route: null,
    startTime: null,
    visitedNodes: [],
    currentPosition: null
  };

  /**
   * 导航初始化（瞬间定位）
   */
  function initializeNavigation(regionId, targetNodeId, options = {}) {
    if (!window.NodeMemory || !window.NodeRelocalization) {
      log('nav_init_no_dependencies', {});
      return null;
    }

    const regionId_final = regionId || (window.getCurrentRegionId ? window.getCurrentRegionId() : 'default');
    
    // 1. 匹配摄像头画面 → 最近视觉节点
    const observedNodes = options.observedNodes || [];
    let startPosition = null;

    if (observedNodes.length > 0 && window.NodeRelocalization.quickLocalize) {
      startPosition = window.NodeRelocalization.quickLocalize(regionId_final, observedNodes);
    }

    // 2. 如果视觉不确定 → 用地理位置猜测（如果有）
    if (!startPosition && options.geoPosition) {
      startPosition = {
        x: options.geoPosition.x || 0,
        y: options.geoPosition.y || 0,
        confidence: 0.5,
        source: 'geo'
      };
    }

    // 3. 加载该区域的节点图库
    const regionNodes = window.NodeMemory.getNodes(regionId_final, {});
    const targetNode = regionNodes.find(n => n.id === targetNodeId);

    if (!targetNode) {
      log('nav_init_target_not_found', { targetNodeId });
      return null;
    }

    // 4. 选择权威路线作为初选路径
    const from = startPosition ? `pos_${startPosition.x}_${startPosition.y}` : 'unknown';
    const to = targetNodeId;
    
    let route = null;
    if (window.NodeMemory.getAuthoritativePath) {
      route = window.NodeMemory.getAuthoritativePath(from, to);
    }

    // 如果没有权威路线，生成新路线
    if (!route) {
      route = generateInitialRoute(regionNodes, startPosition, targetNode);
    }

    currentNavigation = {
      active: true,
      from: from,
      to: to,
      route: route,
      startTime: Date.now(),
      visitedNodes: [],
      currentPosition: startPosition,
      regionId: regionId_final
    };

    log('nav_initialized', {
      regionId: regionId_final,
      from,
      to,
      hasAuthoritativePath: !!route && route.visitCount >= 2,
      route
    });

    return currentNavigation;
  }

  /**
   * 生成初始路线（如果没有权威路线）
   */
  function generateInitialRoute(nodes, startPos, targetNode) {
    // 简化版：直接路径（后续可以接入路径规划算法）
    const viaNodes = [];
    
    // 找到起点和终点之间的中间节点（如果有）
    if (startPos && targetNode.position) {
      const midNodes = nodes.filter(n => {
        if (!n.position) return false;
        const distToStart = window.NodeMemory.calculateDistance(startPos, n.position);
        const distToTarget = window.NodeMemory.calculateDistance(n.position, targetNode.position);
        return distToStart < 10 && distToTarget < 10; // 10米内的中间节点
      });
      viaNodes.push(...midNodes.slice(0, 3)); // 最多3个中间节点
    }

    return {
      from: startPos ? `pos_${startPos.x}_${startPos.y}` : 'unknown',
      to: targetNode.id,
      viaNodes: viaNodes.map(n => n.id),
      estimatedTime: 0,
      safetyScore: 0.7,
      smoothnessScore: 0.7
    };
  }

  /**
   * 导航进行中（动态修正）
   */
  function updateNavigation(observedNodes, cameraPosition = null) {
    if (!currentNavigation.active) return null;

    const { regionId, route } = currentNavigation;
    if (!regionId || !route) return null;

    const updates = {
      positionCorrected: false,
      newNodesDetected: [],
      mapAdjusted: false,
      routeAdjusted: false
    };

    // 1. 摄像头持续输出视觉节点
    if (observedNodes && observedNodes.length > 0) {
      // 2. 若识别到已有节点 → 修正当前位置
      for (const obsNode of observedNodes) {
        if (obsNode.role && obsNode.type) {
          // 尝试重定位
          if (window.NodeRelocalization && window.NodeRelocalization.relocalize) {
            const relocResult = window.NodeRelocalization.relocalize(regionId, obsNode, cameraPosition);
            if (relocResult && relocResult.adjusted) {
              updates.positionCorrected = true;
              updates.mapAdjusted = true;
              currentNavigation.currentPosition = relocResult.position;
            }
          }

          // 检查是否是新节点
          const storedNodes = window.NodeMemory.getNodes(regionId, {
            role: obsNode.role,
            type: obsNode.type
          });
          
          if (storedNodes.length === 0) {
            // 新节点，记录为临时节点
            if (window.NodeDynamicUpdate && window.NodeDynamicUpdate.processNodeUpdate) {
              const tempNode = window.NodeDynamicUpdate.processNodeUpdate(regionId, obsNode);
              if (tempNode && tempNode.is_temporary) {
                updates.newNodesDetected.push(tempNode);
              }
            }
          } else {
            // 已有节点，记录访问
            const nodeId = storedNodes[0].id;
            if (!currentNavigation.visitedNodes.includes(nodeId)) {
              currentNavigation.visitedNodes.push(nodeId);
            }
          }
        }
      }
    }

    // 3. 若路径偏差 → 自动修正路线
    if (updates.positionCorrected && route.viaNodes) {
      // 检查是否需要调整路线
      const adjusted = adjustRouteForDeviation(route, currentNavigation.currentPosition);
      if (adjusted) {
        updates.routeAdjusted = true;
        currentNavigation.route = adjusted;
      }
    }

    log('nav_updated', {
      updates,
      visitedNodesCount: currentNavigation.visitedNodes.length
    });

    return updates;
  }

  /**
   * 调整路线以应对偏差
   */
  function adjustRouteForDeviation(route, currentPos) {
    if (!currentPos || !route.viaNodes || route.viaNodes.length === 0) {
      return null;
    }

    // 简化版：如果当前位置偏离路线太远，重新规划中间节点
    // 这里可以接入更复杂的路径规划算法
    return route; // 暂时不调整
  }

  /**
   * 完成导航并记录路径
   */
  function completeNavigation() {
    if (!currentNavigation.active) return null;

    const { from, to, route, startTime, visitedNodes } = currentNavigation;
    const timeUsed = (Date.now() - startTime) / 1000; // 秒

    // 计算安全分和平滑分（简化版）
    const safetyScore = calculateSafetyScore(visitedNodes);
    const smoothnessScore = calculateSmoothnessScore(route, visitedNodes);

    // 记录路径
    const pathData = {
      from,
      to,
      viaNodes: visitedNodes,
      timeUsed,
      safetyScore,
      smoothnessScore
    };

    let pathRecord = null;
    if (window.NodeMemory && window.NodeMemory.recordPath) {
      pathRecord = window.NodeMemory.recordPath(pathData);
    }

    // 如果有已存在的路径，更新评分
    if (pathRecord && window.NodeMemory && window.NodeMemory.updatePathScore) {
      const existingPaths = Object.values(window.NodeMemory.paths || {}).filter(p => 
        p.from === from && p.to === to
      );
      
      if (existingPaths.length > 0) {
        // 找到最相似的路径并更新
        const similarPath = existingPaths[0];
        window.NodeMemory.updatePathScore(similarPath.pathId, {
          timeUsed,
          safetyScore,
          smoothnessScore
        });
      }
    }

    log('nav_completed', {
      from,
      to,
      timeUsed,
      safetyScore,
      smoothnessScore,
      pathRecord
    });

    // 重置导航状态
    currentNavigation = {
      active: false,
      from: null,
      to: null,
      route: null,
      startTime: null,
      visitedNodes: [],
      currentPosition: null
    };

    return pathRecord;
  }

  /**
   * 计算安全分（简化版）
   */
  function calculateSafetyScore(visitedNodes) {
    // 基于访问的节点类型计算安全分
    // 这里可以接入更复杂的风险评估
    return 0.8; // 默认值
  }

  /**
   * 计算平滑分（简化版）
   */
  function calculateSmoothnessScore(route, visitedNodes) {
    // 基于路线是否顺畅计算平滑分
    if (!route || !route.viaNodes) return 0.7;
    const matchRatio = visitedNodes.filter(id => route.viaNodes.includes(id)).length / route.viaNodes.length;
    return Math.min(1, matchRatio);
  }

  /**
   * 获取当前导航状态
   */
  function getNavigationState() {
    return { ...currentNavigation };
  }

  /**
   * 停止导航
   */
  function stopNavigation() {
    if (currentNavigation.active) {
      completeNavigation();
    }
    currentNavigation.active = false;
  }

  window.NavigationAccelerator = {
    initializeNavigation,
    updateNavigation,
    completeNavigation,
    getNavigationState,
    stopNavigation
  };

})();


/**
 * Waypoint System（路点系统）（规范要求）
 * 支持多路点导航能力（医院、地铁、商场等）
 */

(function() {
    'use strict';

    window.WaypointManager = {
        waypoints: [],
        currentIndex: 0,
        reachedWaypoints: [],
        
        /**
         * 添加路点
         */
        addWaypoint(wp) {
            if (!wp || !wp.id) {
                console.warn('⚠️ [WaypointManager] 无效的路点数据', { module: 'waypoint_system' });
                return false;
            }
            
            // 检查是否已存在
            const exists = this.waypoints.find(w => w.id === wp.id);
            if (exists) {
                console.warn(`⚠️ [WaypointManager] 路点已存在: ${wp.id}`, { module: 'waypoint_system' });
                return false;
            }
            
            // 确保有必要的字段
            const waypoint = {
                id: wp.id,
                type: wp.type || 'custom',
                label: wp.label || wp.id,
                tts_message: wp.tts_message || `到达${wp.label || wp.id}`,
                metadata: wp.metadata || {},
                order: wp.order !== undefined ? wp.order : this.waypoints.length,
                ...wp
            };
            
            this.waypoints.push(waypoint);
            
            // 按order排序
            this.waypoints.sort((a, b) => a.order - b.order);
            
            console.log(`✅ [WaypointManager] 添加路点: ${waypoint.id} (${waypoint.label})`, { module: 'waypoint_system' });
            
            return true;
        },
        
        /**
         * 清空所有路点
         */
        clearWaypoints() {
            const count = this.waypoints.length;
            this.waypoints = [];
            this.currentIndex = 0;
            this.reachedWaypoints = [];
            
            console.log(`🗑️ [WaypointManager] 已清空 ${count} 个路点`, { module: 'waypoint_system' });
        },
        
        /**
         * 获取当前路点
         */
        getCurrent() {
            if (this.waypoints.length === 0) {
                return null;
            }
            
            if (this.currentIndex >= this.waypoints.length) {
                return null;  // 所有路点已完成
            }
            
            return this.waypoints[this.currentIndex];
        },
        
        /**
         * 标记当前路点已到达
         */
        markReached(waypointId = null) {
            const targetId = waypointId || (this.getCurrent()?.id);
            
            if (!targetId) {
                console.warn('⚠️ [WaypointManager] 无法标记到达：无目标路点', { module: 'waypoint_system' });
                return false;
            }
            
            const waypoint = this.waypoints.find(w => w.id === targetId);
            if (!waypoint) {
                console.warn(`⚠️ [WaypointManager] 路点不存在: ${targetId}`, { module: 'waypoint_system' });
                return false;
            }
            
            // 检查是否已到达
            if (this.reachedWaypoints.includes(targetId)) {
                console.log(`ℹ️ [WaypointManager] 路点已标记为到达: ${targetId}`, { module: 'waypoint_system' });
                return false;
            }
            
            // 标记为已到达
            this.reachedWaypoints.push(targetId);
            
            // 如果到达的是当前路点，移动到下一个
            if (this.getCurrent()?.id === targetId) {
                this.currentIndex++;
            }
            
            console.log(`✅ [WaypointManager] 路点已到达: ${waypoint.label} (${targetId})`, { module: 'waypoint_system' });
            
            // 播报TTS消息
            if (waypoint.tts_message && window.speakText) {
                window.speakText(waypoint.tts_message, 'cheerful', false);
            }
            
            // 触发情绪事件
            if (window.emotion_event) {
                window.emotion_event('waypoint_reached', 'medium', {
                    waypoint_id: targetId,
                    waypoint_label: waypoint.label,
                    progress: this.getProgress()
                });
            }
            
            return true;
        },
        
        /**
         * 检查导航进度
         */
        checkProgress(navData) {
            if (!navData || this.waypoints.length === 0) {
                return null;
            }
            
            const currentWaypoint = this.getCurrent();
            if (!currentWaypoint) {
                // 所有路点已完成
                return {
                    completed: true,
                    progress: 1.0,
                    message: "所有路点已完成"
                };
            }
            
            // 简单的到达判断逻辑（可根据实际需求扩展）
            const { action, direction, distance, detectedObjects, signboards } = navData;
            
            // 检查1：方向匹配
            if (currentWaypoint.metadata.expectedDirection) {
                if (direction !== currentWaypoint.metadata.expectedDirection) {
                    return null;  // 方向不匹配，未到达
                }
            }
            
            // 检查2：距离判断
            if (currentWaypoint.metadata.expectedDistance !== undefined) {
                const expectedDist = currentWaypoint.metadata.expectedDistance;
                const tolerance = currentWaypoint.metadata.distanceTolerance || 5;
                if (distance && Math.abs(distance - expectedDist) > tolerance) {
                    return null;  // 距离不匹配
                }
            }
            
            // 检查3：标识牌匹配
            if (currentWaypoint.metadata.expectedSign) {
                const expectedSign = currentWaypoint.metadata.expectedSign;
                if (signboards && Array.isArray(signboards)) {
                    const found = signboards.some(sb => 
                        sb.text && sb.text.includes(expectedSign)
                    );
                    if (!found) {
                        return null;  // 标识牌不匹配
                    }
                }
            }
            
            // 检查4：设施匹配
            if (currentWaypoint.metadata.expectedFacility) {
                const expectedFacility = currentWaypoint.metadata.expectedFacility;
                if (detectedObjects && Array.isArray(detectedObjects)) {
                    const found = detectedObjects.some(obj => 
                        obj.class && obj.class.includes(expectedFacility)
                    );
                    if (!found) {
                        return null;  // 设施不匹配
                    }
                }
            }
            
            // 如果所有条件都满足（或没有条件），标记为到达
            if (action === 'stop' || (distance !== undefined && distance < 3)) {
                this.markReached(currentWaypoint.id);
                return {
                    reached: true,
                    waypoint: currentWaypoint,
                    progress: this.getProgress()
                };
            }
            
            return {
                current: currentWaypoint,
                progress: this.getProgress(),
                remaining: this.waypoints.length - this.currentIndex
            };
        },
        
        /**
         * 获取进度
         */
        getProgress() {
            if (this.waypoints.length === 0) {
                return 0;
            }
            
            return {
                current: this.currentIndex + 1,
                total: this.waypoints.length,
                percentage: Math.round(((this.currentIndex + 1) / this.waypoints.length) * 100),
                reached: this.reachedWaypoints.length,
                remaining: this.waypoints.length - this.currentIndex
            };
        },
        
        /**
         * 获取所有路点
         */
        getAllWaypoints() {
            return this.waypoints.map((wp, index) => ({
                ...wp,
                index,
                reached: this.reachedWaypoints.includes(wp.id),
                isCurrent: index === this.currentIndex
            }));
        }
    };
    
    console.log('✅ WaypointManager模块加载完成', { module: 'waypoint_system' });
})();



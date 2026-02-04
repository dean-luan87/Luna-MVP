// =====================================================
// NodeMemoryZone — v1.0
// 场景节点的本地记忆系统（按区域存储）
// =====================================================

(function () {
    "use strict";

    if (window.NodeMemoryZone) return;

    class NodeMemoryZone {
        constructor() {
            this.key = "luna_node_memory_zone_v1";
            this.data = this._load() || {};

            // 当前区域：可以由外部设置
            this.currentZone = "DEFAULT";
        }

        // ===========================
        // 存储
        // ===========================
        _load() {
            try {
                return JSON.parse(localStorage.getItem(this.key)) || {};
            } catch (err) {
                console.warn("[NodeMemoryZone] load failed", err);
                return {};
            }
        }

        _save() {
            localStorage.setItem(this.key, JSON.stringify(this.data));
        }

        // ===========================
        // 区域管理
        // ===========================
        setZone(zoneName) {
            this.currentZone = zoneName || "DEFAULT";
            if (!this.data[this.currentZone]) {
                this.data[this.currentZone] = [];
            }
            this._save();
        }

        getZone() {
            return this.currentZone;
        }

        getZoneNodes() {
            return this.data[this.currentZone] || [];
        }

        // ===========================
        // 节点合并逻辑
        // ===========================
        _isSimilarNode(a, b) {
            // 简化合并条件：标签相同 或 角色相同
            if (a.label && b.label && a.label === b.label) return true;
            if (a.role && b.role && a.role === b.role) return true;
            return false;
        }

        // ===========================
        // 添加节点（自动合并）
        // ===========================
        addNode(node) {
            if (!this.data[this.currentZone]) {
                this.data[this.currentZone] = [];
            }

            const zoneList = this.data[this.currentZone];

            for (let i = 0; i < zoneList.length; i++) {
                if (this._isSimilarNode(zoneList[i], node)) {
                    // 合并更新时间
                    zoneList[i].lastSeen = Date.now();
                    this._save();
                    return;
                }
            }

            // 新节点
            this.data[this.currentZone].push({
                role: node.role,
                type: node.type,
                label: node.label,
                lastSeen: Date.now()
            });

            this._save();
        }
    }

    window.NodeMemoryZone = new NodeMemoryZone();
    console.log("[NodeMemoryZone] 已加载");
})();


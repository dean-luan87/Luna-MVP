// frontend/node_memory.js
// 按区域存储"场景节点"的长期记忆

(function () {
  "use strict";

  if (window.NodeMemory) return;

  class NodeMemory {
    constructor() {
      this.key = "luna_node_memory_v1";
      this.data = this._load() || {};
      this.currentZone = "DEFAULT";
    }

    _load() {
      try {
        return JSON.parse(localStorage.getItem(this.key)) || {};
      } catch (err) {
        console.warn("[NodeMemory] load failed", err);
        return {};
      }
    }

    _save() {
      localStorage.setItem(this.key, JSON.stringify(this.data));
    }

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

    _isSimilarNode(a, b) {
      if (a.label && b.label && a.label === b.label) return true;
      if (a.role && b.role && a.role === b.role) return true;
      return false;
    }

    addNode(node) {
      if (!this.data[this.currentZone]) {
        this.data[this.currentZone] = [];
      }

      const zoneList = this.data[this.currentZone];
      for (let i = 0; i < zoneList.length; i++) {
        if (this._isSimilarNode(zoneList[i], node)) {
          zoneList[i].lastSeen = Date.now();
          this._save();
          return;
        }
      }

      zoneList.push({
        role: node.role,
        type: node.type,
        label: node.label,
        lastSeen: Date.now(),
      });

      this._save();
    }
  }

  window.NodeMemory = new NodeMemory();
  console.log("[NodeMemory] 已加载");
})();

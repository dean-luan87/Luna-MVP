// frontend/zone_auto_detector.js
// ZoneAutoDetector：根据节点特征自动推断当前区域

(function () {
  "use strict";

  if (window.ZoneAutoDetector) return;

  class ZoneAutoDetector {
    constructor() {
      this.currentFeatures = {};
      this.visualHints = {};
      this.behaviorProfile = {};
      this.lastUpdate = 0;
    }

    feedNode(node) {
      const key = node.label || node.role || "unknown";
      if (!this.currentFeatures[key]) {
        this.currentFeatures[key] = 0;
      }
      this.currentFeatures[key]++;
      this.lastUpdate = Date.now();
    }

    feedVisualHint(hint) {
      this.visualHints[hint] = (this.visualHints[hint] || 0) + 1;
      this.lastUpdate = Date.now();
    }

    feedBehavior(eventName) {
      this.behaviorProfile[eventName] = (this.behaviorProfile[eventName] || 0) + 1;
      this.lastUpdate = Date.now();
    }

    computeSimilarity(zoneName) {
      if (!window.NodeMemory) return 0;
      // ✅ 防御性编程：确保 data 不为 null
      if (!window.NodeMemory.data || typeof window.NodeMemory.data !== 'object') {
        return 0;
      }
      const zoneNodes = (window.NodeMemory.data[zoneName] || []);
      if (!Array.isArray(zoneNodes) || !zoneNodes.length) return 0;

      let score = 0;
      for (const zn of zoneNodes) {
        const key = zn.label || zn.role;
        if (!key) continue;
        if (this.currentFeatures[key]) score += 1;
      }
      return score / (zoneNodes.length + 3);
    }

    detectZone() {
      if (!window.NodeMemory) return null;
      // ✅ 防御性编程：确保 data 不为 null
      if (!window.NodeMemory.data || typeof window.NodeMemory.data !== 'object') {
        return null;
      }

      let bestZone = null;
      let bestScore = 0;

      for (const zoneName of Object.keys(window.NodeMemory.data)) {
        const sim = this.computeSimilarity(zoneName);
        if (sim > bestScore) {
          bestScore = sim;
          bestZone = zoneName;
        }
      }

      if (bestScore > 0.4) {
        return { zone: bestZone, score: bestScore };
      }
      return null;
    }
  }

  window.ZoneAutoDetector = new ZoneAutoDetector();
  console.log("[ZoneAutoDetector] 已加载");

  // 简单定时器：每2秒尝试自动切换区域
  setInterval(() => {
    if (!window.ZoneAutoDetector || !window.ZoneManager) return;
    const res = window.ZoneAutoDetector.detectZone();
    if (res) {
      console.log("[AutoZone] 切换区域 →", res.zone, res.score);
      window.ZoneManager.setZone(res.zone);
    }
  }, 2000);

})();

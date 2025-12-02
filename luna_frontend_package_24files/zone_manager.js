// frontend/zone_manager.js
// ZoneManager：A区 / B区 / 医院区 / 地铁区 等

(function () {
  "use strict";

  if (window.ZoneManager) return;

  class ZoneManager {
    constructor() {
      this.current = "DEFAULT";
    }

    setZone(name) {
      this.current = name;
      console.log("[ZoneManager] 切换区域:", name);

      if (window.NodeMemory) {
        window.NodeMemory.setZone(name);
      }

      if (window.MiniMap) {
        window.MiniMap.state.nodes = [];
        window.MiniMap.state.hazards = [];
      }
    }

    getZone() {
      return this.current;
    }
  }

  window.ZoneManager = new ZoneManager();
  console.log("[ZoneManager] 已加载");
})();

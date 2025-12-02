// frontend/scene_nodes.js
// 场景节点：挂号窗口、电梯、洗手间等

(function () {
  "use strict";

  if (window.SceneNodes) return;

  const logger = window.TaskLogger || {
    info: console.log,
    warn: console.warn,
    error: console.error,
  };

  class SceneNodes {
    constructor() {
      this.currentScene = null;
      this.nodeMap = {};     // { sceneName: [nodeName,...] }
      this.nodeMemory = {};  // { sceneName: { nodeName: {confirmed, meta} } }
    }

    enterScene(sceneName) {
      this.currentScene = sceneName;
      if (!this.nodeMap[sceneName]) this.nodeMap[sceneName] = [];
      if (!this.nodeMemory[sceneName]) this.nodeMemory[sceneName] = {};
      logger.info("SceneNodes", "进入场景", { sceneName });
    }

    addDetectedNode(nodeName, meta) {
      const scene = this.currentScene;
      if (!scene) return;

      if (!this.nodeMemory[scene][nodeName]) {
        logger.info("SceneNodes", "新增节点（待确认）", { scene, nodeName });
        this.nodeMemory[scene][nodeName] = {
          confirmed: false,
          meta: meta || {},
        };
      }
    }

    confirmNode(nodeName, meta) {
      const scene = this.currentScene;
      if (!scene) return;

      this.nodeMemory[scene][nodeName] = {
        confirmed: true,
        meta: meta || {},
      };

      if (!this.nodeMap[scene].includes(nodeName)) {
        this.nodeMap[scene].push(nodeName);
      }

      logger.info("SceneNodes", "用户确认节点", { scene, nodeName });
    }

    renameNode(oldName, newName) {
      const scene = this.currentScene;
      if (!scene) return;

      if (this.nodeMemory[scene][oldName]) {
        this.nodeMemory[scene][newName] = this.nodeMemory[scene][oldName];
        delete this.nodeMemory[scene][oldName];
      }

      const idx = this.nodeMap[scene].indexOf(oldName);
      if (idx >= 0) {
        this.nodeMap[scene][idx] = newName;
      }

      logger.info("SceneNodes", "节点重命名", { scene, oldName, newName });
    }

    buildTaskChainFor(nodeName) {
      return [
        { type: "SCAN_ENV", payload: {} },
        { type: "MOVE_TO_NODE", payload: { nodeName } },
        { type: "CONFIRM_ARRIVAL", payload: { nodeName } },
      ];
    }
  }

  window.SceneNodes = new SceneNodes();
})();

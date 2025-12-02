// frontend/scene_node_detector.js
// 轻量桥接：YOLO识别标签 → SceneNodes.addDetectedNode

(function () {
  "use strict";

  if (window.SceneNodeDetector) return;

  class SceneNodeDetector {
    constructor() {
      this.yoloObjects = [];
    }

    updateDetections(objects) {
      this.yoloObjects = objects || [];

      this.yoloObjects.forEach(obj => {
        const label = (obj.label || "").toLowerCase();

        if (/regist|挂号|register/.test(label)) {
          window.SceneNodes && window.SceneNodes.addDetectedNode("挂号窗口", { box: obj.box });
        }

        if (/toilet|洗手间|wc/.test(label)) {
          window.SceneNodes && window.SceneNodes.addDetectedNode("洗手间", { box: obj.box });
        }

        if (/elevator|电梯/.test(label)) {
          window.SceneNodes && window.SceneNodes.addDetectedNode("电梯", { box: obj.box });
        }
      });
    }
  }

  window.SceneNodeDetector = new SceneNodeDetector();
})();

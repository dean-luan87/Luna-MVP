// frontend/scene_pattern_reasoner.js
// 场景模式推理：记录节点序列 → 推测下一步节点

(function () {
  "use strict";

  if (window.ScenePatternReasoner) return;

  const logger = window.TaskLogger || {
    info: console.log,
    warn: console.warn,
    error: console.error,
  };

  class ScenePatternReasoner {
    constructor() {
      this.currentScene = null;
      this.currentSequence = [];
      this.patternMemory = {}; // {sceneName: {sequences: [...], stats: {...}}}
      this.observers = [];
    }

    enterScene(sceneName) {
      this.currentScene = sceneName;
      this.currentSequence = [];

      if (!this.patternMemory[sceneName]) {
        this.patternMemory[sceneName] = {
          sequences: [],
          stats: {},
          lastSuggested: null,
        };
      }

      logger.info("ScenePatternReasoner", "进入场景", { sceneName });
    }

    recordNodeArrival(nodeName) {
      if (!this.currentScene) return;

      this.currentSequence.push(nodeName);

      logger.info("ScenePatternReasoner", "抵达节点", {
        scene: this.currentScene,
        nodeName,
        stepIndex: this.currentSequence.length - 1,
      });

      this.observers.forEach(cb => cb(nodeName));
    }

    leaveScene() {
      const scene = this.currentScene;
      if (!scene || this.currentSequence.length === 0) return;

      this.patternMemory[scene].sequences.push([...this.currentSequence]);
      this._rebuildStats(scene);

      logger.info("ScenePatternReasoner", "场景离开，记录序列", {
        scene,
        sequence: this.currentSequence,
      });

      this.currentScene = null;
      this.currentSequence = [];
    }

    _rebuildStats(scene) {
      const data = this.patternMemory[scene];
      const sequences = data.sequences;
      const stats = {};

      sequences.forEach(seq => {
        for (let i = 0; i < seq.length - 1; i++) {
          const A = seq[i];
          const B = seq[i + 1];
          if (!stats[A]) stats[A] = {};
          if (!stats[A][B]) stats[A][B] = 0;
          stats[A][B]++;
        }
      });

      data.stats = stats;
      logger.info("ScenePatternReasoner", "更新转移概率", { scene, stats });
    }

    predictNext(nodeName) {
      const scene = this.currentScene;
      if (!scene) return null;

      const stats = this.patternMemory[scene].stats;
      if (!stats[nodeName]) return null;

      const candidates = stats[nodeName];
      const sorted = Object.entries(candidates).sort((a, b) => b[1] - a[1]);
      const predicted = sorted.length > 0 ? sorted[0][0] : null;

      logger.info("ScenePatternReasoner", "推测下一节点", {
        current: nodeName,
        predicted,
        candidates,
      });

      return predicted;
    }

    overwriteSequence(sceneName, newSequence) {
      this.patternMemory[sceneName] = {
        sequences: [newSequence],
        stats: {},
        lastSuggested: null,
      };
      this._rebuildStats(sceneName);

      logger.info("ScenePatternReasoner", "用户覆盖场景模式", {
        scene: sceneName,
        newSequence,
      });
    }

    getScenePattern(sceneName) {
      return this.patternMemory[sceneName] || null;
    }
  }

  window.ScenePatternReasoner = new ScenePatternReasoner();
})();




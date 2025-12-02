// frontend/node_task_bridge.js
// 把"去某个节点"转成一组任务，交给 taskChain 执行

(function () {
  "use strict";

  if (window.NodeTaskBridge) return;

  const logger = window.TaskLogger || {
    info: console.log,
    warn: console.warn,
    error: console.error,
  };

  class NodeTaskBridge {
    goToNode(nodeName) {
      if (!window.SceneNodes || !window.taskChain) return;

      const chain = window.SceneNodes.buildTaskChainFor(nodeName);
      chain.forEach(task => window.taskChain.enqueue(task));

      logger.info("NodeTaskBridge", "生成节点型任务链", {
        nodeName,
        steps: chain.length,
      });
    }
  }

  window.NodeTaskBridge = new NodeTaskBridge();
})();

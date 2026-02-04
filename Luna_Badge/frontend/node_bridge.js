// node_bridge.js
// YOLO / OCR 与 NodeEngine 的桥接层

(function () {
  'use strict';

  function log(event, payload) {
    if (window.__lunaLog) {
      window.__lunaLog(event, payload);
    } else {
      // console.log('[NodeBridge]', event, payload);
    }
  }

  /**
   * 获取当前帧的 YOLO / OCR 结果，并喂给 NodeEngine
   * 你可以在 analyzeVisualGuidance 或定时器中调用它
   */
  function handleVisionFrameForNodes() {
    if (!window.NodeEngine) {
      log('node_bridge_no_engine', {});
      return;
    }

    const yolo = window.latestYOLOResult || null;
    const ocrText = (window.latestOCRResult && window.latestOCRResult.text) || '';

    if (!yolo && !ocrText) {
      // 没有数据就不处理
      return;
    }

    const frame = {
      yoloObjects: Array.isArray(yolo) ? yolo : [],
      ocrText: ocrText || '',
      // positionHint: 后续可以接 IMU/相机位姿，现在可以先留空
      positionHint: null
    };

    const nodes = window.NodeEngine.processFrame(frame);
    if (nodes && nodes.length) {
      log('node_bridge_frame_nodes', {
        count: nodes.length,
        sample: nodes.slice(0, 3).map(n => ({
          id: n.id,
          role: n.role,
          confidence: n.confidence,
          source: n.source
        }))
      });
    }
  }

  // 暴露给全局，方便在视觉分析逻辑里调用
  window.handleVisionFrameForNodes = handleVisionFrameForNodes;

  // 如果你想自动挂钩到现有 analyzeVisualGuidance，可以在那边加一句：
  //   window.handleVisionFrameForNodes && window.handleVisionFrameForNodes();
})();


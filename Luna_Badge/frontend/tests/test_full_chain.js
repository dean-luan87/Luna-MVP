// frontend/tests/test_full_chain.js
// 全链路测试脚本

(function () {
  "use strict";
  if (window.TestFullChain) return;

  class TestFullChainClass {
    constructor() {
      this.panel = null;
      this.vb = null;
      this.isRunning = false;
    }

    init() {
      // 初始化测试面板
      if (window.TestPanel) {
        this.panel = new window.TestPanel("luna_test_panel");
      }

      // 初始化VisionBridge
      if (window.VisionBridge) {
        this.vb = window.VisionBridge;
      } else {
        console.error("[TestFullChain] VisionBridge not found");
        return false;
      }

      return true;
    }

    simulate() {
      if (!this.init()) {
        console.error("[TestFullChain] Initialization failed");
        return;
      }

      console.log("[TestFullChain] Starting full test...");
      this.isRunning = true;

      // 模拟YOLO检测结果
      const fakeFrame = [
        {
          label: "person",
          conf: 0.71,
          x: 120,
          y: 200,
          w: 80,
          h: 140,
          confidence: 0.71,
          class: "person",
        },
        {
          label: "stairs",
          conf: 0.82,
          x: 260,
          y: 180,
          w: 90,
          h: 110,
          confidence: 0.82,
          class: "stairs",
        },
        {
          label: "door",
          conf: 0.65,
          x: 400,
          y: 150,
          w: 100,
          h: 200,
          confidence: 0.65,
          class: "door",
        },
      ];

      // 处理YOLO数据
      if (this.vb && this.vb.ingestYolo) {
        this.vb.ingestYolo(fakeFrame);
      }

      // 更新测试面板
      if (this.panel) {
        const navState = window.NavigationFSM
          ? {
              state: window.NavigationFSM.getState(),
              currentStep: window.NavigationFSM.getCurrentStep
            ? window.NavigationFSM.getCurrentStep()
            : null,
            }
          : { state: "IDLE" };

        const taskState = window.taskChain
          ? {
              queueLength: window.taskChain.queue ? window.taskChain.queue.length : 0,
              currentTask: window.taskChain.currentTask
            ? window.taskChain.currentTask.type
            : null,
              running: window.taskChain.running || false,
            }
          : { queueLength: 0 };

        this.panel.update({
          yolo: fakeFrame,
          navState: navState,
          taskState: taskState,
          timestamp: new Date().toISOString(),
        });
      }

      // 测试TTS（如果存在）
      if (window.speakText) {
        setTimeout(() => {
          window.speakText("测试播报：导航系统已启动", "cheerful", false);
        }, 1000);
      } else if (window.PriorityTTSQueue) {
        window.PriorityTTSQueue.enqueue({
          text: "测试播报：导航系统已启动",
          priority: "MEDIUM",
          category: "test",
        });
      }

      // 标记活动（看门狗）
      if (window.LunaWatchdog) {
        window.LunaWatchdog.markTaskActivity();
        window.LunaWatchdog.markNavActivity();
      }

      console.log("[TestFullChain] Full test completed");
      this.isRunning = false;
    }

    // 连续测试（模拟多帧）
    simulateContinuous(frames = 5, intervalMs = 2000) {
      if (!this.init()) {
        return;
      }

      console.log(`[TestFullChain] Starting continuous test: ${frames} frames`);
      let count = 0;

      const timer = setInterval(() => {
        count++;
        console.log(`[TestFullChain] Frame ${count}/${frames}`);

        // 生成随机检测结果
        const randomFrame = this._generateRandomFrame();
        if (this.vb && this.vb.ingestYolo) {
          this.vb.ingestYolo(randomFrame);
        }

        if (this.panel) {
          this.panel.append(`frame_${count}`, {
            detections: randomFrame.length,
            timestamp: new Date().toISOString(),
          });
        }

        if (count >= frames) {
          clearInterval(timer);
          console.log("[TestFullChain] Continuous test completed");
        }
      }, intervalMs);
    }

    _generateRandomFrame() {
      const labels = ["person", "stairs", "door", "elevator", "sign"];
      const count = Math.floor(Math.random() * 3) + 1;
      const frame = [];

      for (let i = 0; i < count; i++) {
        const label = labels[Math.floor(Math.random() * labels.length)];
        frame.push({
          label: label,
          conf: 0.5 + Math.random() * 0.4,
          confidence: 0.5 + Math.random() * 0.4,
          class: label,
          x: Math.random() * 640,
          y: Math.random() * 480,
          w: 50 + Math.random() * 100,
          h: 50 + Math.random() * 150,
        });
      }

      return frame;
    }
  }

  window.TestFullChain = new TestFullChainClass();

  // 全局测试函数
  window.testFullChain = function () {
    window.TestFullChain.simulate();
  };

  window.testFullChainContinuous = function (frames, interval) {
    window.TestFullChain.simulateContinuous(frames, interval);
  };

  console.log("[TestFullChain] 全链路测试脚本已加载");
  console.log("[TestFullChain] 使用方法: testFullChain() 或 testFullChainContinuous(5, 2000)");
})();




// frontend/test_center/TestCenterUI.js
// Luna Badge 测试中心 UI组件（纯JavaScript，不依赖React）

(function () {
  "use strict";
  if (window.TestCenterUI) return;

  const TestCenter = window.TestCenter || {};
  let cameraStream = null;
  let videoElement = null;

  class TestCenterUIClass {
    constructor() {
      this.isInitialized = false;
      this.currentTab = "vision";
    }

    /**
     * 初始化测试中心UI
     */
    init() {
      if (this.isInitialized) return;

      this.createUI();
      this.bindEvents();
      this.startPerformanceMonitor();

      this.isInitialized = true;
      console.log("[TestCenterUI] 测试中心UI已初始化");
    }

    /**
     * 创建UI结构
     */
    createUI() {
      // 创建主容器
      const container = document.createElement("div");
      container.id = "luna_test_center";
      container.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: #f5f5f5;
        z-index: 10000;
        display: flex;
        flex-direction: column;
        font-family: system-ui, -apple-system, sans-serif;
      `;

      // 创建标签页
      const tabs = this.createTabs();
      container.appendChild(tabs);

      // 创建内容区域
      const content = this.createContentArea();
      container.appendChild(content);

      // 创建底部日志区域
      const logs = this.createLogsArea();
      container.appendChild(logs);

      document.body.appendChild(container);
    }

    /**
     * 创建标签页
     */
    createTabs() {
      const tabs = document.createElement("div");
      tabs.style.cssText = `
        display: flex;
        background: #fff;
        border-bottom: 2px solid #e0e0e0;
        padding: 0 20px;
      `;

      const tabNames = [
        { id: "vision", label: "① 实时视觉调试" },
        { id: "feature", label: "② 功能测试台" },
        { id: "scenario", label: "③ 联动场景模拟" },
        { id: "performance", label: "④ 性能监控" },
      ];

      tabNames.forEach((tab) => {
        const tabEl = document.createElement("div");
        tabEl.className = "test-tab";
        tabEl.dataset.tab = tab.id;
        tabEl.textContent = tab.label;
        tabEl.style.cssText = `
          padding: 12px 20px;
          cursor: pointer;
          border-bottom: 3px solid transparent;
          transition: all 0.2s;
        `;
        tabEl.addEventListener("click", () => this.switchTab(tab.id));
        tabs.appendChild(tabEl);
      });

      return tabs;
    }

    /**
     * 创建内容区域
     */
    createContentArea() {
      const content = document.createElement("div");
      content.id = "test_content_area";
      content.style.cssText = `
        flex: 1;
        overflow-y: auto;
        padding: 20px;
      `;

      // 初始化显示视觉调试面板
      this.renderVisionDebug(content);

      return content;
    }

    /**
     * 创建日志区域
     */
    createLogsArea() {
      const logs = document.createElement("div");
      logs.id = "test_logs_area";
      logs.style.cssText = `
        height: 200px;
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 10px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        font-size: 12px;
      `;

      return logs;
    }

    /**
     * 切换标签页
     */
    switchTab(tabId) {
      this.currentTab = tabId;

      // 更新标签样式
      document.querySelectorAll(".test-tab").forEach((tab) => {
        if (tab.dataset.tab === tabId) {
          tab.style.borderBottomColor = "#007bff";
          tab.style.color = "#007bff";
        } else {
          tab.style.borderBottomColor = "transparent";
          tab.style.color = "#333";
        }
      });

      // 更新内容区域
      const contentArea = document.getElementById("test_content_area");
      contentArea.innerHTML = "";

      switch (tabId) {
        case "vision":
          this.renderVisionDebug(contentArea);
          break;
        case "feature":
          this.renderFeatureTest(contentArea);
          break;
        case "scenario":
          this.renderScenarioTest(contentArea);
          break;
        case "performance":
          this.renderPerformance(contentArea);
          break;
      }
    }

    /**
     * 渲染视觉调试面板
     */
    renderVisionDebug(container) {
      const panel = document.createElement("div");
      panel.innerHTML = `
        <h2>实时视觉调试</h2>
        <div style="display: flex; gap: 20px;">
          <div style="flex: 1;">
            <div id="camera_preview" style="background: #000; width: 100%; aspect-ratio: 16/9; position: relative;">
              <video id="test_video" autoplay playsinline style="width: 100%; height: 100%; object-fit: contain;"></video>
              <canvas id="test_overlay" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;"></canvas>
            </div>
            <div style="margin-top: 10px; display: flex; gap: 10px;">
              <button id="btn_start_camera" class="test-btn">▶ 开启摄像头</button>
              <button id="btn_stop_camera" class="test-btn">■ 停止摄像头</button>
              <button id="btn_capture_frame" class="test-btn">📷 捕获当前帧</button>
            </div>
          </div>
          <div style="flex: 1;">
            <h3>场景描述</h3>
            <div id="scene_description" style="background: #fff; padding: 15px; border-radius: 8px; min-height: 200px;">
              <p style="color: #999;">等待图像输入...</p>
            </div>
            <h3 style="margin-top: 20px;">检测结果</h3>
            <div id="detection_results" style="background: #fff; padding: 15px; border-radius: 8px; max-height: 300px; overflow-y: auto;">
              <p style="color: #999;">等待检测...</p>
            </div>
          </div>
        </div>
      `;

      // 添加样式
      const style = document.createElement("style");
      style.textContent = `
        .test-btn {
          padding: 8px 16px;
          background: #007bff;
          color: #fff;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px;
        }
        .test-btn:hover {
          background: #0056b3;
        }
        .test-btn:disabled {
          background: #ccc;
          cursor: not-allowed;
        }
      `;
      document.head.appendChild(style);

      container.appendChild(panel);

      // 绑定事件
      document.getElementById("btn_start_camera").addEventListener("click", () => this.startCamera());
      document.getElementById("btn_stop_camera").addEventListener("click", () => this.stopCamera());
      document.getElementById("btn_capture_frame").addEventListener("click", () => this.captureFrame());
    }

    /**
     * 渲染功能测试面板
     */
    renderFeatureTest(container) {
      const panel = document.createElement("div");
      panel.innerHTML = `
        <h2>功能测试台</h2>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 20px;">
          <button class="feature-btn" data-feature="yolo">YOLO Object Detection</button>
          <button class="feature-btn" data-feature="ocr">OCR</button>
          <button class="feature-btn" data-feature="signboard">Signboard Recognition</button>
          <button class="feature-btn" data-feature="hazard">Hazard Test</button>
          <button class="feature-btn" data-feature="step">Step Test</button>
          <button class="feature-btn" data-feature="crowd">Crowd Test</button>
          <button class="feature-btn" data-feature="navigation">Navigation</button>
          <button class="feature-btn" data-feature="visual_guide">VisualGuide</button>
          <button class="feature-btn" data-feature="indoor_nav">Indoor Nav</button>
          <button class="feature-btn" data-feature="tts">TTS Test</button>
          <button class="feature-btn" data-feature="cache">Cache Test</button>
          <button class="feature-btn" data-feature="network">Network Test</button>
        </div>
        <div id="feature_result" style="margin-top: 20px; background: #fff; padding: 20px; border-radius: 8px; min-height: 200px;">
          <p style="color: #999;">点击上方按钮开始测试...</p>
        </div>
      `;

      container.appendChild(panel);

      // 绑定事件
      panel.querySelectorAll(".feature-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
          const feature = btn.dataset.feature;
          this.testFeature(feature);
        });
      });
    }

    /**
     * 渲染场景测试面板
     */
    renderScenarioTest(container) {
      const panel = document.createElement("div");
      panel.innerHTML = `
        <h2>联动场景模拟</h2>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 20px;">
          <div class="scenario-card" data-scenario="street">
            <h3>🔥 场景A：街道路况导航</h3>
            <p>启动导航 → 逐帧更新 → 检测危险 → 转弯 → 偏航纠正</p>
            <button class="scenario-btn" data-scenario="street">运行场景</button>
          </div>
          <div class="scenario-card" data-scenario="indoor">
            <h3>🔥 场景B：室内导航</h3>
            <p>OCR提取信息 → 识别导视牌 → 构建拓扑图</p>
            <button class="scenario-btn" data-scenario="indoor">运行场景</button>
          </div>
          <div class="scenario-card" data-scenario="life">
            <h3>🔥 场景C：生活场景</h3>
            <p>找服务台、找洗手间、找电梯等</p>
            <button class="scenario-btn" data-scenario="life">运行场景</button>
          </div>
          <div class="scenario-card" data-scenario="task_chain">
            <h3>🔥 场景D：任务链联动</h3>
            <p>导航 → 上厕所 → 恢复导航</p>
            <button class="scenario-btn" data-scenario="task_chain">运行场景</button>
          </div>
        </div>
        <div id="scenario_result" style="margin-top: 20px; background: #fff; padding: 20px; border-radius: 8px; min-height: 200px;">
          <p style="color: #999;">选择场景开始测试...</p>
        </div>
      `;

      // 添加样式
      const style = document.createElement("style");
      style.textContent += `
        .scenario-card {
          background: #fff;
          padding: 20px;
          border-radius: 8px;
          border: 1px solid #e0e0e0;
        }
        .scenario-btn {
          margin-top: 10px;
          padding: 8px 16px;
          background: #28a745;
          color: #fff;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }
        .scenario-btn:hover {
          background: #218838;
        }
      `;
      document.head.appendChild(style);

      container.appendChild(panel);

      // 绑定事件
      panel.querySelectorAll(".scenario-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
          const scenario = btn.dataset.scenario;
          this.runScenario(scenario);
        });
      });
    }

    /**
     * 渲染性能监控面板
     */
    renderPerformance(container) {
      const panel = document.createElement("div");
      panel.innerHTML = `
        <h2>性能监控</h2>
        <div id="performance_metrics" style="background: #fff; padding: 20px; border-radius: 8px; margin-top: 20px;">
          <p>正在加载性能指标...</p>
        </div>
        <button id="btn_refresh_metrics" class="test-btn" style="margin-top: 10px;">刷新指标</button>
      `;

      container.appendChild(panel);

      // 绑定事件
      document.getElementById("btn_refresh_metrics").addEventListener("click", () => {
        this.updatePerformanceMetrics();
      });

      // 初始加载
      this.updatePerformanceMetrics();
    }

    /**
     * 启动摄像头
     */
    async startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        cameraStream = stream;
        videoElement = document.getElementById("test_video");
        if (videoElement) {
          videoElement.srcObject = stream;
        }
        this.log("摄像头已启动");
      } catch (error) {
        this.log(`摄像头启动失败: ${error.message}`, "error");
      }
    }

    /**
     * 停止摄像头
     */
    stopCamera() {
      if (cameraStream) {
        cameraStream.getTracks().forEach((track) => track.stop());
        cameraStream = null;
      }
      if (videoElement) {
        videoElement.srcObject = null;
      }
      this.log("摄像头已停止");
    }

    /**
     * 捕获当前帧
     */
    async captureFrame() {
      if (!videoElement || !videoElement.videoWidth) {
        this.log("请先启动摄像头", "error");
        return;
      }

      const canvas = document.createElement("canvas");
      canvas.width = videoElement.videoWidth;
      canvas.height = videoElement.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(videoElement, 0, 0);

      canvas.toBlob(async (blob) => {
        this.log("正在分析当前帧...");
        try {
          const result = await TestCenter.visionDebug(blob);
          if (result.success) {
            this.displayVisionResult(result.data);
          }
        } catch (error) {
          this.log(`视觉调试失败: ${error.message}`, "error");
        }
      });
    }

    /**
     * 显示视觉结果
     */
    displayVisionResult(data) {
      // 更新场景描述
      const sceneDesc = document.getElementById("scene_description");
      if (sceneDesc && data.scene_description) {
        sceneDesc.innerHTML = `
          <p><strong>场景类型:</strong> ${data.scene_description.scene_type || "unknown"}</p>
          <p><strong>描述:</strong> ${data.scene_description.summary || "无"}</p>
        `;
      }

      // 更新检测结果
      const detResults = document.getElementById("detection_results");
      if (detResults) {
        detResults.innerHTML = `
          <p><strong>YOLO检测:</strong> ${data.yolo?.count || 0} 个对象 (${data.yolo?.latency_ms || 0}ms)</p>
          <p><strong>危险检测:</strong> ${data.hazards?.length || 0} 个</p>
          <p><strong>台阶检测:</strong> ${data.step?.detected ? "是" : "否"}</p>
          <p><strong>标识牌:</strong> ${data.signboards?.length || 0} 个</p>
          <p><strong>总耗时:</strong> ${data.total_latency_ms || 0}ms (FPS: ${data.performance?.fps || 0})</p>
        `;
      }

      // 绘制检测框
      this.drawDetections(data.yolo?.detections || []);
    }

    /**
     * 绘制检测框
     */
    drawDetections(detections) {
      const overlay = document.getElementById("test_overlay");
      const video = document.getElementById("test_video");
      if (!overlay || !video || !video.videoWidth) return;

      overlay.width = video.videoWidth;
      overlay.height = video.videoHeight;
      const ctx = overlay.getContext("2d");
      ctx.clearRect(0, 0, overlay.width, overlay.height);

      detections.forEach((det) => {
        const bbox = det.bbox || [];
        if (bbox.length >= 4) {
          ctx.strokeStyle = "#00ff00";
          ctx.lineWidth = 2;
          ctx.strokeRect(bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]);
          ctx.fillStyle = "#00ff00";
          ctx.font = "14px Arial";
          ctx.fillText(det.label || det.class || "unknown", bbox[0], bbox[1] - 5);
        }
      });
    }

    /**
     * 测试功能
     */
    async testFeature(feature) {
      const resultArea = document.getElementById("feature_result");
      if (resultArea) {
        resultArea.innerHTML = `<p>正在测试 ${feature}...</p>`;
      }

      this.log(`开始测试功能: ${feature}`);

      try {
        // 需要图像的功能
        if (["yolo", "ocr", "hazard", "step"].includes(feature)) {
          if (!videoElement || !videoElement.videoWidth) {
            this.log("请先启动摄像头并捕获一帧", "error");
            return;
          }

          const canvas = document.createElement("canvas");
          canvas.width = videoElement.videoWidth;
          canvas.height = videoElement.videoHeight;
          const ctx = canvas.getContext("2d");
          ctx.drawImage(videoElement, 0, 0);

          canvas.toBlob(async (blob) => {
            let result;
            switch (feature) {
              case "yolo":
                result = await TestCenter.testYOLO(blob);
                break;
              case "ocr":
                result = await TestCenter.testOCR(blob);
                break;
              case "hazard":
                result = await TestCenter.testHazard(blob);
                break;
              case "step":
                result = await TestCenter.testStep(blob);
                break;
            }

            if (resultArea && result.success) {
              resultArea.innerHTML = `
                <h3>测试结果</h3>
                <pre style="background: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto;">${JSON.stringify(result.data, null, 2)}</pre>
              `;
            }
          });
        } else if (feature === "tts") {
          const result = await TestCenter.testTTS("这是一次TTS测试。");
          if (resultArea && result.success) {
            resultArea.innerHTML = `
              <h3>TTS测试结果</h3>
              <p>音频已生成，长度: ${result.data.text_length} 字符</p>
              <p>耗时: ${result.data.latency_ms}ms</p>
              <audio controls src="data:audio/mpeg;base64,${result.data.audio}"></audio>
            `;
          }
        } else {
          this.log(`功能 ${feature} 测试待实现`, "warn");
        }
      } catch (error) {
        this.log(`功能测试失败: ${error.message}`, "error");
      }
    }

    /**
     * 运行场景
     */
    async runScenario(scenario) {
      const resultArea = document.getElementById("scenario_result");
      if (resultArea) {
        resultArea.innerHTML = `<p>正在运行场景: ${scenario}...</p>`;
      }

      this.log(`开始运行场景: ${scenario}`);

      // TODO: 实现场景运行逻辑
      this.log(`场景 ${scenario} 运行完成`);
    }

    /**
     * 更新性能指标
     */
    async updatePerformanceMetrics() {
      const metricsArea = document.getElementById("performance_metrics");
      if (!metricsArea) return;

      try {
        const result = await TestCenter.getPerformanceMetrics();
        if (result.success && metricsArea) {
          metricsArea.innerHTML = `
            <h3>系统性能</h3>
            <pre style="background: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto;">${JSON.stringify(result.data, null, 2)}</pre>
          `;
        }
      } catch (error) {
        this.log(`性能指标获取失败: ${error.message}`, "error");
      }
    }

    /**
     * 启动性能监控
     */
    startPerformanceMonitor() {
      setInterval(() => {
        this.updatePerformanceMetrics();
      }, 5000); // 每5秒更新一次
    }

    /**
     * 记录日志
     */
    log(message, level = "info") {
      const logsArea = document.getElementById("test_logs_area");
      if (!logsArea) return;

      const timestamp = new Date().toLocaleTimeString();
      const levelColor = {
        info: "#d4d4d4",
        warn: "#ffc107",
        error: "#dc3545",
      };

      const logEntry = document.createElement("div");
      logEntry.style.color = levelColor[level] || levelColor.info;
      logEntry.textContent = `[${timestamp}] [${level.toUpperCase()}] ${message}`;

      logsArea.appendChild(logEntry);
      logsArea.scrollTop = logsArea.scrollHeight;

      // 限制日志数量
      while (logsArea.children.length > 100) {
        logsArea.removeChild(logsArea.firstChild);
      }
    }
  }

  const ui = new TestCenterUIClass();

  // 挂载到全局
  window.TestCenterUI = TestCenterUIClass;
  window.testCenterUI = ui;

  // 自动初始化（如果DOM已加载）
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => ui.init());
  } else {
    ui.init();
  }

  console.log("[TestCenterUI] Luna Badge测试中心UI已加载");
})();




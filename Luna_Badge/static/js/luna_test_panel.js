// static/js/luna_test_panel.js

(function () {
  "use strict";

  function $(id) {
    return document.getElementById(id);
  }

  function appendLog(msg, level) {
    const logArea = $("logArea");
    if (!logArea) return;
    const ts = new Date().toISOString().slice(11, 23); // HH:MM:SS.mmm
    const tag = level ? `[${level}]` : "[INFO]";
    logArea.value += `${ts} ${tag} ${msg}\n`;
    logArea.scrollTop = logArea.scrollHeight;
  }

  async function callApi(url, { method = "GET", body = null, isForm = false } = {}) {
    const options = { method, headers: {} };

    if (body) {
      if (isForm) {
        options.body = body;
      } else {
        options.headers["Content-Type"] = "application/json";
        options.body = JSON.stringify(body);
      }
    }

    const start = performance.now();
    try {
      const res = await fetch(url, options);
      const json = await res.json().catch(() => ({}));
      const cost = performance.now() - start;

      if (!json || json.success === false) {
        const code = json && (json.code || (json.error && json.error.code) || "UNKNOWN_ERROR");
        const message = json && (json.message || (json.error && json.error.message) || "未知错误");
        appendLog(`API ${url} 失败，code=${code}, message=${message}`, "ERROR");
      } else {
        appendLog(`API ${url} 成功，耗时 ${cost.toFixed(1)} ms`, "OK");
      }
      return { json, cost };
    } catch (e) {
      appendLog(`API ${url} 调用异常: ${e}`, "EXCEPTION");
      return { json: null, cost: null, error: e };
    }
  }

  function setPreviewFromFileInput(inputId) {
    const fileInput = $(inputId);
    if (!fileInput || !fileInput.files || fileInput.files.length === 0) return;

    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = function (e) {
      const img = $("previewImage");
      const placeholder = $("previewPlaceholder");
      if (img) {
        img.src = e.target.result;
        img.style.display = "block";
      }
      if (placeholder) {
        placeholder.style.display = "none";
      }
    };
    reader.readAsDataURL(file);
  }

  function initTabs() {
    const tabs = document.querySelectorAll(".ltp-tab");
    const panels = {
      vision: $("panel-vision"),
      hazard: $("panel-hazard"),
      navigation: $("panel-navigation"),
      hooks: $("panel-hooks"),
    };

    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        tabs.forEach((t) => t.classList.remove("ltp-tab-active"));
        tab.classList.add("ltp-tab-active");

        const tabName = tab.getAttribute("data-tab");
        Object.keys(panels).forEach((key) => {
          if (panels[key]) {
            panels[key].classList.toggle("ltp-panel-active", key === tabName);
          }
        });
      });
    });
  }

  function initVisionPanel() {
    const visionFile = $("visionFile");
    if (visionFile) {
      visionFile.addEventListener("change", () =>
        setPreviewFromFileInput("visionFile")
      );
    }

    const btnTestVision = $("btnTestVision");
    if (btnTestVision) {
      btnTestVision.addEventListener("click", async () => {
        const fileInput = $("visionFile");
        if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
          alert("请选择一张图片");
          return;
        }
        const formData = new FormData();
        formData.append("image", fileInput.files[0]);

        const { json, cost } = await callApi("/api/recognize", {
          method: "POST",
          body: formData,
          isForm: true,
        });

        if (json && $("visionResult")) {
          $("visionResult").textContent = JSON.stringify(json, null, 2);
        }
        if ($("visionCost") && cost != null) {
          $("visionCost").textContent = `耗时：${cost.toFixed(1)} ms`;
        }
      });
    }

    const btnTestComprehensive = $("btnTestComprehensive");
    if (btnTestComprehensive) {
      btnTestComprehensive.addEventListener("click", async () => {
        const fileInput = $("visionFile");
        if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
          alert("请选择一张图片");
          return;
        }
        const formData = new FormData();
        formData.append("image", fileInput.files[0]);

        const { json } = await callApi("/api/detect/comprehensive", {
          method: "POST",
          body: formData,
          isForm: true,
        });

        if (json && $("visionResult")) {
          $("visionResult").textContent = JSON.stringify(json, null, 2);
        }
      });
    }
  }

  function initHazardPanel() {
    const hazardFile = $("hazardFile");
    if (hazardFile) {
      hazardFile.addEventListener("change", () =>
        setPreviewFromFileInput("hazardFile")
      );
    }

    const btnTestStep = $("btnTestStep");
    if (btnTestStep) {
      btnTestStep.addEventListener("click", async () => {
        const fileInput = $("hazardFile");
        if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
          alert("请选择一张图片");
          return;
        }
        const formData = new FormData();
        formData.append("image", fileInput.files[0]);

        const { json } = await callApi("/api/detect/step", {
          method: "POST",
          body: formData,
          isForm: true,
        });

        if (json && $("stepResult")) {
          $("stepResult").textContent = JSON.stringify(json, null, 2);
        }
      });
    }

    const btnTestHazard = $("btnTestHazard");
    if (btnTestHazard) {
      btnTestHazard.addEventListener("click", async () => {
        const fileInput = $("hazardFile");
        if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
          alert("请选择一张图片");
          return;
        }
        const formData = new FormData();
        formData.append("image", fileInput.files[0]);

        const { json } = await callApi("/api/detect/hazard", {
          method: "POST",
          body: formData,
          isForm: true,
        });

        if (json && $("hazardResult")) {
          $("hazardResult").textContent = JSON.stringify(json, null, 2);
        }
      });
    }
  }

  function initNavigationPanel() {
    const sceneFile = $("sceneFile");
    if (sceneFile) {
      sceneFile.addEventListener("change", () =>
        setPreviewFromFileInput("sceneFile")
      );
    }

    const btnStartNav = $("btnStartNav");
    if (btnStartNav) {
      btnStartNav.addEventListener("click", async () => {
        const dest = $("navDestination")?.value?.trim();
        if (!dest) {
          alert("请输入目的地");
          return;
        }
        const { json } = await callApi("/api/navigation/start", {
          method: "POST",
          body: { destination: dest },
        });
        if (json && $("navStatus")) {
          $("navStatus").textContent = JSON.stringify(json, null, 2);
        }
      });
    }

    const btnNavStatus = $("btnNavStatus");
    if (btnNavStatus) {
      btnNavStatus.addEventListener("click", async () => {
        const { json } = await callApi("/api/navigation/status", {
          method: "GET",
        });
        if (json && $("navStatus")) {
          $("navStatus").textContent = JSON.stringify(json, null, 2);
        }
      });
    }

    const btnPauseNav = $("btnPauseNav");
    if (btnPauseNav) {
      btnPauseNav.addEventListener("click", async () => {
        const { json } = await callApi("/api/navigation/pause", {
          method: "POST",
          body: { reason: "测试面板暂停" },
        });
        if (json && $("navStatus")) {
          $("navStatus").textContent = JSON.stringify(json, null, 2);
        }
      });
    }

    const btnResumeNav = $("btnResumeNav");
    if (btnResumeNav) {
      btnResumeNav.addEventListener("click", async () => {
        const { json } = await callApi("/api/navigation/resume", {
          method: "POST",
        });
        if (json && $("navStatus")) {
          $("navStatus").textContent = JSON.stringify(json, null, 2);
        }
      });
    }

    const btnCancelNav = $("btnCancelNav");
    if (btnCancelNav) {
      btnCancelNav.addEventListener("click", async () => {
        const { json } = await callApi("/api/navigation/cancel", {
          method: "POST",
          body: { reason: "测试面板取消" },
        });
        if (json && $("navStatus")) {
          $("navStatus").textContent = JSON.stringify(json, null, 2);
        }
      });
    }

    const btnDescribeScene = $("btnDescribeScene");
    if (btnDescribeScene) {
      btnDescribeScene.addEventListener("click", async () => {
        const fileInput = $("sceneFile");
        let formData = null;
        let useImage = false;

        if (fileInput && fileInput.files && fileInput.files.length > 0) {
          formData = new FormData();
          formData.append("image", fileInput.files[0]);
          useImage = true;
        }

        const { json } = await callApi(
          "/api/navigation/describe_scene",
          useImage
            ? { method: "POST", body: formData, isForm: true }
            : { method: "POST", body: {} }
        );

        if (json && json.data) {
          const data = json.data;
          if ($("sceneStructured")) {
            $("sceneStructured").textContent = JSON.stringify(
              data.description || data,
              null,
              2
            );
          }
          if ($("sceneSpeech")) {
            $("sceneSpeech").textContent = data.tts || data.summary || "";
          }
        } else if (json && $("sceneStructured")) {
          $("sceneStructured").textContent = JSON.stringify(json, null, 2);
        }
      });
    }

    const btnRunNavDiag = $("btnRunNavDiag");
    if (btnRunNavDiag) {
      btnRunNavDiag.addEventListener("click", () => {
        if (typeof window.runNavigationDiagnosis === "function") {
          appendLog("调用 runNavigationDiagnosis()", "DEBUG");
          try {
            const result = window.runNavigationDiagnosis();
            appendLog(
              "navigation_diagnosis 返回：" +
                JSON.stringify(result?.overall || {}, null, 2),
              "DEBUG"
            );
          } catch (e) {
            appendLog("runNavigationDiagnosis 调用异常：" + e, "ERROR");
          }
        } else {
          appendLog(
            "runNavigationDiagnosis 不存在，请确认 navigation_diagnosis.js 已加载",
            "WARN"
          );
        }
      });
    }

    const btnRunFullChain = $("btnRunFullChain");
    if (btnRunFullChain) {
      btnRunFullChain.addEventListener("click", () => {
        if (typeof window.testFullChain === "function") {
          appendLog("调用 testFullChain()", "DEBUG");
          try {
            window.testFullChain();
          } catch (e) {
            appendLog("testFullChain 调用异常：" + e, "ERROR");
          }
        } else {
          appendLog(
            "testFullChain 不存在，请确认 test_full_chain.js 已加载",
            "WARN"
          );
        }
      });
    }
  }

  function initHookPanel() {
    const hookHazardList = $("hookHazardList");
    const hookNavList = $("hookNavList");
    const hookActionList = $("hookActionList");

    const addItem = (ul, text) => {
      if (!ul) return;
      const li = document.createElement("li");
      li.textContent = text;
      ul.insertBefore(li, ul.firstChild);
      while (ul.children.length > 100) {
        ul.removeChild(ul.lastChild);
      }
    };

    // 兼容多种Hooks API格式
    if (window.Hooks) {
      // 方式1: Hooks.on() 方法
      if (typeof window.Hooks.on === "function") {
        // 危险事件
        window.Hooks.on("onHazard", (data) => {
          const d = data || {};
          const dir = d.direction || d.meta?.direction || "-";
          const dist =
            d.distance != null
              ? typeof d.distance === "number"
                ? `${d.distance.toFixed(2)}m`
                : d.distance
              : "-";
          addItem(
            hookHazardList,
            `[${new Date().toLocaleTimeString()}] type=${d.type || "-"} dir=${dir} dist=${dist}`
          );
        });

        // 导航事件
        window.Hooks.on("onNavigation", (data) => {
          const d = data || {};
          addItem(
            hookNavList,
            `[${new Date().toLocaleTimeString()}] action=${d.action || "-"} msg=${
              d.message || "-"
            }`
          );
        });

        // 动作建议
        window.Hooks.on("onActionSuggest", (data) => {
          const d = data || {};
          addItem(
            hookActionList,
            `[${new Date().toLocaleTimeString()}] hazard=${d.type || "-"} dir=${d.direction ||
              "-"} dist=${d.distance != null ? d.distance : "-"}`
          );
        });

        appendLog("Hooks 事件监听已注册（Hooks.on）", "OK");
      }
      // 方式2: Hooks.onHazard 数组
      else if (Array.isArray(window.Hooks.onHazard)) {
        window.Hooks.onHazard.push((data) => {
          const d = data || {};
          const dir = d.direction || d.meta?.direction || "-";
          const dist =
            d.distance != null
              ? typeof d.distance === "number"
                ? `${d.distance.toFixed(2)}m`
                : d.distance
              : "-";
          addItem(
            hookHazardList,
            `[${new Date().toLocaleTimeString()}] type=${d.type || "-"} dir=${dir} dist=${dist}`
          );
        });

        if (Array.isArray(window.Hooks.onNavigation)) {
          window.Hooks.onNavigation.push((data) => {
            const d = data || {};
            addItem(
              hookNavList,
              `[${new Date().toLocaleTimeString()}] action=${d.action || "-"} msg=${
                d.message || "-"
              }`
            );
          });
        }

        if (Array.isArray(window.Hooks.onActionSuggest)) {
          window.Hooks.onActionSuggest.push((data) => {
            const d = data || {};
            addItem(
              hookActionList,
              `[${new Date().toLocaleTimeString()}] hazard=${d.type || "-"} dir=${d.direction ||
                "-"} dist=${d.distance != null ? d.distance : "-"}`
            );
          });
        }

        appendLog("Hooks 事件监听已注册（数组push）", "OK");
      }
      // 方式3: EventDispatcher订阅
      else if (window.EventDispatcher && typeof window.EventDispatcher.subscribe === "function") {
        window.EventDispatcher.subscribe((event) => {
          if (event.type === "HAZARD_DETECTED" || event.type === "hazard") {
            const d = event || {};
            const dir = d.direction || "-";
            const dist = d.distance != null ? d.distance : "-";
            addItem(
              hookHazardList,
              `[${new Date().toLocaleTimeString()}] type=${d.type || "-"} dir=${dir} dist=${dist}`
            );
          } else if (event.type === "NAV_GUIDANCE" || event.type === "navigation") {
            const d = event || {};
            addItem(
              hookNavList,
              `[${new Date().toLocaleTimeString()}] action=${d.action || "-"} msg=${
                d.message || "-"
              }`
            );
          } else if (event.type === "ACTION_SUGGEST" || event.type === "action_suggest") {
            const d = event || {};
            addItem(
              hookActionList,
              `[${new Date().toLocaleTimeString()}] hazard=${d.type || "-"} dir=${d.direction ||
                "-"} dist=${d.distance != null ? d.distance : "-"}`
            );
          }
        });

        appendLog("EventDispatcher 事件监听已注册", "OK");
      }
      else {
        appendLog("Hooks 对象存在但格式未知，Hook 面板可能无法工作", "WARN");
      }
    } else {
      appendLog("Hooks 对象不存在，Hook 面板将无法工作", "WARN");
    }

    const btnClearHooks = $("btnClearHooks");
    if (btnClearHooks) {
      btnClearHooks.addEventListener("click", () => {
        if (hookHazardList) hookHazardList.innerHTML = "";
        if (hookNavList) hookNavList.innerHTML = "";
        if (hookActionList) hookActionList.innerHTML = "";
      });
    }
  }

  function initLogAndMetrics() {
    const btnClearLog = $("btnClearLog");
    if (btnClearLog) {
      btnClearLog.addEventListener("click", () => {
        const logArea = $("logArea");
        if (logArea) logArea.value = "";
      });
    }

    async function fetchMetrics() {
      const { json } = await callApi("/api/performance/metrics", {
        method: "GET",
      });
      if (!json || !json.data) return;
      const m = json.data;
      if ($("metricMemory")) $("metricMemory").textContent = m.memory_mb ?? "-";
      if ($("metricVision"))
        $("metricVision").textContent = m.vision?.avg ?? m.modules?.vision?.latency_ms ?? "-";
      if ($("metricAudio"))
        $("metricAudio").textContent = m.audio?.avg ?? m.modules?.tts?.latency_ms ?? "-";
      if ($("metricFps"))
        $("metricFps").textContent = m.fps?.current ?? m.modules?.vision?.fps ?? "-";
      if ($("metricDegrade"))
        $("metricDegrade").textContent = m.degrade_level ?? "-";
    }

    // 初次获取一次，然后每 10s 更新
    fetchMetrics();
    setInterval(fetchMetrics, 10000);
  }

  document.addEventListener("DOMContentLoaded", () => {
    appendLog("Luna 1.2.0 测试面板已加载", "OK");
    initTabs();
    initVisionPanel();
    initHazardPanel();
    initNavigationPanel();
    initHookPanel();
    initLogAndMetrics();
  });
})();




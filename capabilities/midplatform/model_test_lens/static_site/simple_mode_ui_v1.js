/**
 * Model Test Lens — Simple Mode UI v1.
 * Default: 选文件 → 选测试类型 → 开始本地测试 → 看结果.
 * Technical workflow hidden; still calls 127.0.0.1:8787 service APIs.
 */
(function (global) {
  "use strict";

  var SERVICE_BASE = "http://127.0.0.1:8787";
  var START_CMD = "bash scripts/start_local_runner_bridge.sh";

  var TEST_TYPES = [
    {
      id: "segmentation",
      label: "图片分割（MobileSAM）",
      subtitle: "识别图片中的区域边界，适合测试分割能力",
      enabled: true,
      badge: null,
      asset_type: "image",
      model_category: "segmentation",
      model_id: "mobile_sam",
      accept: "image/*"
    },
    {
      id: "slam_vio",
      label: "视频 SLAM（实验）",
      subtitle: "登记视频并生成 limited 测试结果；真实 ORB-SLAM/VINS 尚未接入",
      enabled: true,
      badge: "limited",
      asset_type: "video",
      model_category: "slam_vio",
      model_id: "orb_slam_or_vins_placeholder",
      accept: "video/*"
    },
    {
      id: "ocr",
      label: "OCR 文字识别",
      subtitle: "暂未接入本地 runner",
      enabled: false,
      badge: "暂未接入",
      asset_type: "image",
      model_category: "ocr",
      model_id: "ocr_placeholder",
      accept: "image/*"
    },
    {
      id: "asr",
      label: "ASR 语音识别",
      subtitle: "暂未接入本地 runner",
      enabled: false,
      badge: "暂未接入",
      asset_type: "audio",
      model_category: "asr",
      model_id: "asr_placeholder",
      accept: "audio/*"
    }
  ];

  var PROGRESS_STEPS = [
    { id: "check_service", label: "检查本地服务" },
    { id: "register", label: "登记测试文件" },
    { id: "create_job", label: "创建测试任务" },
    { id: "run", label: "本地模型测试中" },
    { id: "generate", label: "生成结果" },
    { id: "display", label: "展示结果" }
  ];

  var KNOWN_PATHS_BY_NAME = {
    "mobile_sam_multi_real_image_street_scene_v1_001.png":
      "capabilities/test_assets/p1/mobile_sam/multi/mobile_sam_multi_real_image_street_scene_v1_001.png",
    "mobile_sam_multi_real_image_street_scene_v1_002.png":
      "capabilities/test_assets/p1/mobile_sam/multi/mobile_sam_multi_real_image_street_scene_v1_002.png",
    "mobile_sam_multi_real_image_street_scene_v1_003.png":
      "capabilities/test_assets/p1/mobile_sam/multi/mobile_sam_multi_real_image_street_scene_v1_003.png",
    "mobile_sam_multi_real_image_street_scene_v1_004.png":
      "capabilities/test_assets/p1/mobile_sam/multi/mobile_sam_multi_real_image_street_scene_v1_004.png",
    "mobile_sam_real_local_image_street_scene_v1.png":
      "capabilities/test_assets/p1/mobile_sam/mobile_sam_real_local_image_street_scene_v1.png",
    "ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png":
      "capabilities/test_assets/p1/ocr/ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png",
    "ocr_real_image_subway_station_longtan_temple_v1_001.png":
      "capabilities/test_assets/p1/ocr/ocr_real_image_subway_station_longtan_temple_v1_001.png",
    "ocr_real_image_subway_platform_jiahuihu_v1_001.png":
      "capabilities/test_assets/p1/ocr/ocr_real_image_subway_platform_jiahuihu_v1_001.png",
    "smoke_placeholder.mp4":
      "capabilities/test_assets/model_test_lens/smoke_placeholder.mp4"
  };

  function serviceFetch(path, opts) {
    opts = opts || {};
    return fetch(SERVICE_BASE + path, {
      method: opts.method || "GET",
      headers: { "Content-Type": "application/json" },
      body: opts.body ? JSON.stringify(opts.body) : undefined
    }).then(function (r) {
      return r.json().then(function (data) {
        return { ok: r.ok, status: r.status, data: data };
      });
    });
  }

  function extOf(name) {
    if (!name || name.indexOf(".") < 0) return "";
    return name.split(".").pop().toLowerCase();
  }

  function detectAssetType(file, testType) {
    if (!file) return testType.asset_type;
    var ext = extOf(file.name);
    if (["png", "jpg", "jpeg", "webp", "gif", "bmp"].indexOf(ext) >= 0) return "image";
    if (["mp4", "mov", "avi", "mkv", "webm"].indexOf(ext) >= 0) return "video";
    if (["wav", "mp3", "m4a", "flac", "ogg"].indexOf(ext) >= 0) return "audio";
    return testType.asset_type;
  }

  function resolveLocalPath(file) {
    if (!file) return null;
    if (file._localPath) return file._localPath;
    return KNOWN_PATHS_BY_NAME[file.name] || null;
  }

  function humanError(err, stepId) {
    var msg = (err && err.message) ? err.message : String(err || "未知错误");
    if (/fetch|network|Failed to fetch|无法连接/i.test(msg)) {
      return "本地测试服务未启动。请先运行：" + START_CMD;
    }
    if (stepId === "register" && /登记|register|local_path|path/i.test(msg)) {
      return "无法定位所选文件的本机路径。请使用项目 test_assets 中的测试文件，或在「高级流程」中填写完整路径。";
    }
    if (/capabilities|服务不可用|8787/.test(msg)) {
      return "本地测试服务未启动。请先运行：" + START_CMD;
    }
    return msg;
  }

  function initSimpleModeUI(options) {
    var root = options.rootEl;
    var onEnvelope = options.onEnvelope || function () {};
    var onWorkflowArtifacts = options.onWorkflowArtifacts || function () {};
    var onSlamLimitedNotice = options.onSlamLimitedNotice || function () {};

    root.innerHTML =
      "<section class='sm-section' aria-label='simple mode local test'>" +
      "<header class='sm-header'>" +
      "<h2>本地模型测试</h2>" +
      "<p id='sm-service-banner' class='sm-service-banner' role='status'>正在检查本地测试服务…</p>" +
      "<p class='sm-boundary'>本地测试结果仅用于模型评估，不会写入事实层，也不会触发导航或语音输出。</p>" +
      "</header>" +
      "<div class='sm-file-zone'>" +
      "<p class='sm-prompt'>选择一张图片或一段视频开始测试。</p>" +
      "<label class='sm-file-btn btn btn-secondary'>选择文件" +
      "<input id='sm-file-input' type='file' accept='image/*,video/*' hidden /></label>" +
      "<p id='sm-file-meta' class='sm-file-meta muted'>尚未选择文件</p>" +
      "</div>" +
      "<fieldset class='sm-test-types' id='sm-test-types'><legend>测试类型</legend></fieldset>" +
      "<div class='sm-actions'>" +
      "<button type='button' id='sm-start' class='btn btn-primary' disabled>开始本地测试</button>" +
      "<button type='button' id='sm-recheck-service' class='btn btn-ghost'>重新检查服务</button>" +
      "</div>" +
      "<ol id='sm-progress' class='sm-progress' aria-label='测试进度'></ol>" +
      "<div id='sm-result-hint' class='sm-result-hint' hidden></div>" +
      "<div id='sm-failure' class='sm-failure' hidden></div>" +
      "<div id='sm-slam-notice' class='sm-slam-notice' hidden></div>" +
      "</section>";

    var fileInput = root.querySelector("#sm-file-input");
    var fileMeta = root.querySelector("#sm-file-meta");
    var typesHost = root.querySelector("#sm-test-types");
    var startBtn = root.querySelector("#sm-start");
    var progressHost = root.querySelector("#sm-progress");
    var failureHost = root.querySelector("#sm-failure");
    var resultHint = root.querySelector("#sm-result-hint");
    var slamNotice = root.querySelector("#sm-slam-notice");
    var serviceBanner = root.querySelector("#sm-service-banner");

    var state = {
      file: null,
      testTypeId: "segmentation",
      serviceOk: false,
      stepStatus: {}
    };

    PROGRESS_STEPS.forEach(function (step) {
      state.stepStatus[step.id] = "waiting";
    });

    function currentTestType() {
      for (var i = 0; i < TEST_TYPES.length; i++) {
        if (TEST_TYPES[i].id === state.testTypeId) return TEST_TYPES[i];
      }
      return TEST_TYPES[0];
    }

    function renderTestTypes() {
      typesHost.innerHTML = "";
      TEST_TYPES.forEach(function (tt) {
        var id = "sm-type-" + tt.id;
        var wrap = document.createElement("label");
        wrap.className = "sm-type-option" + (tt.enabled ? "" : " sm-type-disabled");
        wrap.innerHTML =
          "<input type='radio' name='sm-test-type' id='" + id + "' value='" + tt.id + "'" +
          (tt.id === state.testTypeId ? " checked" : "") +
          (tt.enabled ? "" : " disabled") + " />" +
          "<span class='sm-type-body'>" +
          "<span class='sm-type-title'>" + tt.label +
          (tt.badge ? " <em class='sm-badge'>" + tt.badge + "</em>" : "") + "</span>" +
          "<span class='sm-type-sub'>" + tt.subtitle + "</span>" +
          "</span>";
        if (tt.enabled) {
          wrap.querySelector("input").addEventListener("change", function () {
            if (this.checked) {
              state.testTypeId = tt.id;
              fileInput.accept = tt.accept;
              updateStartButton();
            }
          });
        }
        typesHost.appendChild(wrap);
      });
    }

    function renderProgress() {
      progressHost.innerHTML = PROGRESS_STEPS.map(function (step) {
        var st = state.stepStatus[step.id] || "waiting";
        return "<li class='sm-step sm-step-" + st + "' data-step='" + step.id + "'>" +
          "<span class='sm-step-icon' aria-hidden='true'></span>" +
          "<span class='sm-step-label'>" + step.label + "</span>" +
          "</li>";
      }).join("");
    }

    function setStep(stepId, status) {
      state.stepStatus[stepId] = status;
      renderProgress();
    }

    function resetProgress() {
      PROGRESS_STEPS.forEach(function (step) {
        state.stepStatus[step.id] = "waiting";
      });
      renderProgress();
      failureHost.hidden = true;
      slamNotice.hidden = true;
      if (resultHint) resultHint.hidden = true;
    }

    function setServiceBanner(ok) {
      state.serviceOk = ok;
      serviceBanner.textContent = ok
        ? "本地测试服务已连接"
        : "本地测试服务未启动 · 请运行 " + START_CMD;
      serviceBanner.className = "sm-service-banner " + (ok ? "ok" : "warn");
    }

    function checkService() {
      return serviceFetch("/api/v1/capabilities").then(function (res) {
        setServiceBanner(res.ok);
        return res.ok;
      }).catch(function () {
        setServiceBanner(false);
        return false;
      });
    }

    function updateFileMeta() {
      if (!state.file) {
        fileMeta.textContent = "尚未选择文件";
        return;
      }
      var tt = currentTestType();
      var assetType = detectAssetType(state.file, tt);
      var pathHint = resolveLocalPath(state.file);
      fileMeta.innerHTML =
        "已选择：<strong>" + state.file.name + "</strong> · " +
        (assetType === "image" ? "图片" : assetType === "video" ? "视频" : assetType) +
        (pathHint ? "" : " · <span class='warn-inline'>需为项目内已知测试文件</span>");
    }

    function updateStartButton() {
      var tt = currentTestType();
      startBtn.disabled = !state.file || !tt.enabled || !state.serviceOk;
    }

    fileInput.addEventListener("change", function (ev) {
      var f = ev.target.files && ev.target.files[0];
      state.file = f || null;
      if (f) {
        var ext = extOf(f.name);
        if (["mp4", "mov", "avi", "mkv", "webm"].indexOf(ext) >= 0) {
          state.testTypeId = "slam_vio";
        } else if (["png", "jpg", "jpeg", "webp", "gif", "bmp"].indexOf(ext) >= 0) {
          state.testTypeId = "segmentation";
        }
        renderTestTypes();
      }
      updateFileMeta();
      updateStartButton();
    });

    root.querySelector("#sm-recheck-service").addEventListener("click", function () {
      checkService().then(updateStartButton);
    });

    startBtn.addEventListener("click", function () {
      var tt = currentTestType();
      if (!tt.enabled) return;
      if (!state.file) {
        failureHost.hidden = false;
        failureHost.innerHTML = "<p><strong>请先选择文件</strong></p>";
        return;
      }

      var localPath = resolveLocalPath(state.file);
      if (!localPath) {
        failureHost.hidden = false;
        failureHost.innerHTML =
          "<p><strong>无法定位文件路径</strong></p>" +
          "<p>浏览器无法读取完整磁盘路径。请使用项目 <code>test_assets</code> 目录中的测试文件，或在「高级流程」填写本机路径。</p>";
        return;
      }

      startBtn.disabled = true;
      resetProgress();
      failureHost.hidden = true;

      var workflow = { manifest: null, jobRequest: null, runnerBridge: null, jobId: null };

      function fail(stepId, err) {
        setStep(stepId, "failed");
        failureHost.hidden = false;
        failureHost.innerHTML =
          "<p><strong>测试未能完成</strong></p>" +
          "<p>" + humanError(err, stepId) + "</p>";
        startBtn.disabled = false;
      }

      setStep("check_service", "running");
      serviceFetch("/api/v1/capabilities")
        .then(function (capRes) {
          if (!capRes.ok) throw new Error("service_unavailable");
          setStep("check_service", "done");
          setStep("register", "running");
          return serviceFetch("/api/v1/assets/register", {
            method: "POST",
            body: {
              asset_type: detectAssetType(state.file, tt),
              model_category: tt.model_category,
              requested_model_id: tt.model_id,
              browser_file_name: state.file.name,
              local_path: localPath,
              candidate_only: true
            }
          });
        })
        .then(function (regRes) {
          if (!regRes.ok) throw new Error("register_failed");
          workflow.manifest = regRes.data.asset_manifest;
          setStep("register", "done");
          setStep("create_job", "running");

          if (global.LocalAssetImportUI && global.RunnerBridgeUI) {
            workflow.jobRequest = global.RunnerBridgeUI.buildJobRequest(
              workflow.manifest, tt.model_category, tt.model_id
            );
            if (workflow.jobRequest) {
              workflow.runnerBridge = global.RunnerBridgeUI.buildRunnerBridgeRequest(workflow.jobRequest);
            }
          }

          return serviceFetch("/api/v1/jobs/create", {
            method: "POST",
            body: {
              asset_manifest: workflow.manifest,
              requested_model_category: tt.model_category,
              requested_model_id: tt.model_id
            }
          });
        })
        .then(function (jobRes) {
          if (!jobRes.ok) throw new Error("create_job_failed");
          workflow.jobId = jobRes.data.job_id;
          setStep("create_job", "done");
          setStep("run", "running");
          return serviceFetch("/api/v1/jobs/" + workflow.jobId + "/run", { method: "POST", body: {} });
        })
        .then(function (runRes) {
          if (!runRes.ok) throw new Error("run_failed");
          setStep("run", "done");
          setStep("generate", "running");
          return serviceFetch("/api/v1/jobs/" + workflow.jobId + "/result");
        })
        .then(function (resultRes) {
          if (!resultRes.ok || !resultRes.data.envelope) {
            throw new Error("no_envelope");
          }
          setStep("generate", "done");
          setStep("display", "running");

          onWorkflowArtifacts({
            assetType: tt.asset_type,
            modelCategory: tt.model_category,
            modelId: tt.model_id,
            file: state.file,
            manifest: workflow.manifest,
            jobRequest: workflow.jobRequest,
            runnerBridge: workflow.runnerBridge,
            serviceAsset: { asset_id: workflow.manifest && workflow.manifest.asset_id },
            jobId: workflow.jobId
          });

          onEnvelope(resultRes.data.envelope);

          var env = resultRes.data.envelope;
          var metrics = env.metrics || {};
          var rate = metrics.overall_success_rate;
          var rateText = typeof rate === "number" ? Math.round(rate * 100) + "%" : "—";
          if (resultHint) {
            resultHint.hidden = false;
            var hudLink = "";
            if (global.PerceptionHUDView && global.PerceptionHUDView.supportsHUD(env)) {
              hudLink = " · <a href='#' id='sm-view-hud'>查看机器人视角</a>";
            }
            resultHint.innerHTML =
              "<p><strong>测试完成</strong> · 成功率 " + rateText +
              " · <a href='#viewer-card' id='sm-scroll-results'>查看结果 ↓</a>" + hudLink + "</p>";
            var link = resultHint.querySelector("#sm-scroll-results");
            if (link) {
              link.addEventListener("click", function (ev) {
                ev.preventDefault();
                var target = document.getElementById("viewer-card");
                if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
              });
            }
            var hudBtn = resultHint.querySelector("#sm-view-hud");
            if (hudBtn) {
              hudBtn.addEventListener("click", function (ev) {
                ev.preventDefault();
                if (global.ModelTestLens && global.ModelTestLens.switchToHUDView) {
                  global.ModelTestLens.switchToHUDView();
                }
              });
            }
          }

          setTimeout(function () {
            var target = document.getElementById("viewer-card");
            if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
          }, 300);

          if (tt.id === "slam_vio") {
            var notice =
              "当前是 SLAM limited 模式：已登记视频并生成测试占位结果；" +
              "真实 ORB-SLAM/VINS 尚未接入，因此不会计算 ATE 或漂移评分。";
            slamNotice.hidden = false;
            slamNotice.innerHTML = "<p><strong>SLAM 实验模式</strong></p><p>" + notice + "</p>";
            onSlamLimitedNotice(notice);
          }

          setStep("display", "done");
          startBtn.disabled = false;
        })
        .catch(function (err) {
          var failedStep = "check_service";
          if (state.stepStatus.register === "running") failedStep = "register";
          else if (state.stepStatus.create_job === "running") failedStep = "create_job";
          else if (state.stepStatus.run === "running") failedStep = "run";
          else if (state.stepStatus.generate === "running") failedStep = "generate";
          else if (state.stepStatus.display === "running") failedStep = "display";
          fail(failedStep, err);
        });
    });

    renderTestTypes();
    renderProgress();
    checkService().then(updateStartButton);

    return {
      checkService: checkService,
      setLocalPathForFile: function (path) {
        if (state.file) state.file._localPath = path;
        updateFileMeta();
        updateStartButton();
      }
    };
  }

  function initHeadlessController(options) {
    var onEnvelope = options.onEnvelope || function () {};
    var onWorkflowArtifacts = options.onWorkflowArtifacts || function () {};
    var onSlamLimitedNotice = options.onSlamLimitedNotice || function () {};
    var onServiceStatus = options.onServiceStatus || function () {};
    var onProgress = options.onProgress || function () {};
    var onFailure = options.onFailure || function () {};

    var state = {
      file: null,
      testTypeId: "segmentation",
      serviceOk: false,
      stepStatus: {}
    };

    PROGRESS_STEPS.forEach(function (step) {
      state.stepStatus[step.id] = "waiting";
    });

    function currentTestType() {
      for (var i = 0; i < TEST_TYPES.length; i++) {
        if (TEST_TYPES[i].id === state.testTypeId) return TEST_TYPES[i];
      }
      return TEST_TYPES[0];
    }

    function setServiceBanner(ok) {
      state.serviceOk = ok;
      onServiceStatus(ok);
      return ok;
    }

    function checkService() {
      return serviceFetch("/api/v1/capabilities").then(function (res) {
        return setServiceBanner(res.ok);
      }).catch(function () {
        return setServiceBanner(false);
      });
    }

    function capabilityToTestType(capId) {
      if (capId === "slam") return "slam_vio";
      if (capId === "segmentation") return "segmentation";
      return state.testTypeId;
    }

    function setFile(file) {
      state.file = file || null;
      if (file) {
        var ext = extOf(file.name);
        if (["mp4", "mov", "avi", "mkv", "webm"].indexOf(ext) >= 0) {
          state.testTypeId = "slam_vio";
        } else if (["png", "jpg", "jpeg", "webp", "gif", "bmp"].indexOf(ext) >= 0) {
          state.testTypeId = "segmentation";
        }
      }
      return state.file;
    }

    function setCapability(capId) {
      state.testTypeId = capabilityToTestType(capId);
    }

    function canStart() {
      var tt = currentTestType();
      return !!(state.file && tt.enabled && state.serviceOk);
    }

    function setStep(stepId, status) {
      state.stepStatus[stepId] = status;
      onProgress(state.stepStatus);
    }

    function resetProgress() {
      PROGRESS_STEPS.forEach(function (step) {
        state.stepStatus[step.id] = "waiting";
      });
      onProgress(state.stepStatus);
    }

    function startTest() {
      var tt = currentTestType();
      if (!tt.enabled) return Promise.reject(new Error("test_type_disabled"));
      if (!state.file) return Promise.reject(new Error("no_file"));
      var localPath = resolveLocalPath(state.file);
      if (!localPath) return Promise.reject(new Error("no_local_path"));

      resetProgress();
      var workflow = { manifest: null, jobRequest: null, runnerBridge: null, jobId: null };

      function fail(stepId, err) {
        setStep(stepId, "failed");
        onFailure(humanError(err, stepId));
        throw err;
      }

      setStep("check_service", "running");
      return serviceFetch("/api/v1/capabilities")
        .then(function (capRes) {
          if (!capRes.ok) throw new Error("service_unavailable");
          setStep("check_service", "done");
          setStep("register", "running");
          return serviceFetch("/api/v1/assets/register", {
            method: "POST",
            body: {
              asset_type: detectAssetType(state.file, tt),
              model_category: tt.model_category,
              requested_model_id: tt.model_id,
              browser_file_name: state.file.name,
              local_path: localPath,
              candidate_only: true
            }
          });
        })
        .then(function (regRes) {
          if (!regRes.ok) throw new Error("register_failed");
          workflow.manifest = regRes.data.asset_manifest;
          setStep("register", "done");
          setStep("create_job", "running");

          if (global.LocalAssetImportUI && global.RunnerBridgeUI) {
            workflow.jobRequest = global.RunnerBridgeUI.buildJobRequest(
              workflow.manifest, tt.model_category, tt.model_id
            );
            if (workflow.jobRequest) {
              workflow.runnerBridge = global.RunnerBridgeUI.buildRunnerBridgeRequest(workflow.jobRequest);
            }
          }

          return serviceFetch("/api/v1/jobs/create", {
            method: "POST",
            body: {
              asset_manifest: workflow.manifest,
              requested_model_category: tt.model_category,
              requested_model_id: tt.model_id
            }
          });
        })
        .then(function (jobRes) {
          if (!jobRes.ok) throw new Error("create_job_failed");
          workflow.jobId = jobRes.data.job_id;
          setStep("create_job", "done");
          setStep("run", "running");
          return serviceFetch("/api/v1/jobs/" + workflow.jobId + "/run", { method: "POST", body: {} });
        })
        .then(function (runRes) {
          if (!runRes.ok) throw new Error("run_failed");
          setStep("run", "done");
          setStep("generate", "running");
          return serviceFetch("/api/v1/jobs/" + workflow.jobId + "/result");
        })
        .then(function (resultRes) {
          if (!resultRes.ok || !resultRes.data.envelope) throw new Error("no_envelope");
          setStep("generate", "done");
          setStep("display", "running");

          onWorkflowArtifacts({
            assetType: tt.asset_type,
            modelCategory: tt.model_category,
            modelId: tt.model_id,
            file: state.file,
            manifest: workflow.manifest,
            jobRequest: workflow.jobRequest,
            runnerBridge: workflow.runnerBridge,
            serviceAsset: { asset_id: workflow.manifest && workflow.manifest.asset_id },
            jobId: workflow.jobId
          });

          onEnvelope(resultRes.data.envelope);

          if (tt.id === "slam_vio") {
            onSlamLimitedNotice(
              "当前是 SLAM limited 模式：已登记视频并生成测试占位结果；" +
              "真实 ORB-SLAM/VINS 尚未接入，因此不会计算 ATE 或漂移评分。"
            );
          }

          setStep("display", "done");
          return resultRes.data.envelope;
        })
        .catch(function (err) {
          var failedStep = "check_service";
          if (state.stepStatus.register === "running") failedStep = "register";
          else if (state.stepStatus.create_job === "running") failedStep = "create_job";
          else if (state.stepStatus.run === "running") failedStep = "run";
          else if (state.stepStatus.generate === "running") failedStep = "generate";
          else if (state.stepStatus.display === "running") failedStep = "display";
          fail(failedStep, err);
        });
    }

    checkService();

    return {
      checkService: checkService,
      setFile: setFile,
      setCapability: setCapability,
      getFile: function () { return state.file; },
      canStart: canStart,
      startTest: startTest,
      setLocalPathForFile: function (path) {
        if (state.file) state.file._localPath = path;
      }
    };
  }

  global.SimpleModeUI = {
    init: initSimpleModeUI,
    initHeadless: initHeadlessController,
    TEST_TYPES: TEST_TYPES,
    SERVICE_BASE: SERVICE_BASE,
    KNOWN_PATHS_BY_NAME: KNOWN_PATHS_BY_NAME
  };
})(typeof window !== "undefined" ? window : this);

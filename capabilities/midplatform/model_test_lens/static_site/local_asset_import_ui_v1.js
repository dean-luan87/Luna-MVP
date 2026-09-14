/**
 * Model Test Lens — local asset import UI v1.
 * Registers scoped local test assets and generates manifest JSON in-browser only.
 * No model execution. No registry/fact writes. No upload.
 */
(function (global) {
  "use strict";

  var Ex = global.LocalAssetImportExamples;

  function uid(prefix) {
    return (
      prefix +
      "_" +
      Date.now().toString(36) +
      "_" +
      Math.random().toString(36).slice(2, 8)
    );
  }

  function extOf(name) {
    if (!name || name.indexOf(".") < 0) return "";
    return name.split(".").pop().toLowerCase();
  }

  function allowedModelsFor(assetType, category) {
    var map = {
      image: ["segmentation", "ocr", "depth_world", "detection_tracking", "face_expression_gesture", "multimodal_vlm"],
      video: ["slam_vio", "detection_tracking", "ocr", "segmentation", "multimodal_vlm", "face_expression_gesture"],
      frame_sequence: ["slam_vio", "detection_tracking", "ocr", "segmentation"],
      audio: ["asr", "speaker", "tts"],
      text: ["tts", "multimodal_vlm"]
    };
    var list = map[assetType] || [];
    if (category && list.indexOf(category) < 0) {
      return list.concat([category]);
    }
    return list;
  }

  function computeSha256Browser(arrayBuffer) {
    if (!global.crypto || !global.crypto.subtle) {
      return Promise.resolve({ status: "pending_runner_computation", value: null });
    }
    return global.crypto.subtle
      .digest("SHA-256", arrayBuffer)
      .then(function (buf) {
        var bytes = new Uint8Array(buf);
        var hex = "";
        for (var i = 0; i < bytes.length; i++) {
          hex += ("0" + bytes[i].toString(16)).slice(-2);
        }
        return { status: "browser_computed", value: hex };
      })
      .catch(function () {
        return { status: "pending_runner_computation", value: null };
      });
  }

  function buildManifestPreview(opts) {
    var assetType = opts.assetType;
    var file = opts.file;
    var frameSequencePath = opts.frameSequencePath || "";
    var modelCategory = opts.modelCategory;
    var personalSensitive = !!opts.personalSensitive;
    var assetId = uid("asset");
    var manifestId = uid("manifest");
    var fileName = file ? file.name : frameSequencePath || "frame_sequence_placeholder";
    var localPath = file
      ? "browser_file://" + file.name
      : frameSequencePath || "browser_placeholder://frame_sequence";
    var manifest = {
      manifest_id: manifestId,
      created_by: Ex.CREATED_BY,
      created_by_phase: Ex.CREATED_BY_PHASE_UI_PATCH,
      created_at: new Date().toISOString(),
      asset_id: assetId,
      asset_type: assetType,
      local_file_name: fileName,
      local_path_or_browser_file_name: localPath,
      local_path: localPath,
      file_name: fileName,
      file_extension: extOf(fileName),
      file_size_bytes: file && typeof file.size === "number" ? file.size : null,
      sha256_status: opts.sha256Status || "pending_runner_computation",
      sha256: opts.sha256 || undefined,
      media_metadata_status: opts.mediaMetadataStatus || "pending_runner_or_browser_computed",
      media_metadata: opts.mediaMetadata || undefined,
      source_type: "user_supplied_local_asset",
      scoped_for_model_test: true,
      allowed_models: allowedModelsFor(assetType, modelCategory),
      intended_test_type: modelCategory,
      candidate_only: true,
      personal_sensitive_flag_required: true,
      personal_sensitive_flag: personalSensitive ? true : false,
      external_url_source: false,
      live_camera_frame: false,
      live_microphone_capture: false,
      uncontrolled_dataset_source: false,
      fact_layer_source: false,
      semantic_layer_source: false,
      navigation_runtime_frame: false,
      must_not_enter_fact_layer: true,
      must_not_enter_runtime: true,
      must_not_enter_output_adapter: true,
      must_not_enter_semantic_layer: true,
      must_not_trigger_navigation_action_speech: true,
      protected: true,
      page_must_not_execute_model: true,
      model_execution_allowed: false
    };
    return manifest;
  }

  function downloadJson(filename, obj) {
    var blob = new Blob([JSON.stringify(obj, null, 2)], { type: "application/json" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.rel = "noopener";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function copyJson(obj, onDone) {
    var text = JSON.stringify(obj, null, 2);
    if (global.navigator && global.navigator.clipboard && global.navigator.clipboard.writeText) {
      global.navigator.clipboard.writeText(text).then(function () {
        if (onDone) onDone(null);
      }).catch(function (e) {
        if (onDone) onDone(e);
      });
      return;
    }
    if (onDone) onDone(new Error("clipboard_unavailable"));
  }

  function statusLabel(state) {
    if (state.runnerBridge) return "runner_bridge_ready";
    if (state.jobRequest) return "job_request_ready";
    if (state.manifest) return "manifest_ready";
    return "awaiting_asset_selection";
  }

  function initLocalAssetImportUI(options) {
    var root = options.rootEl;
    var onStateChange = options.onStateChange || function () {};
    var advancedOnly = !!options.advancedOnly;
    var state = {
      assetType: "image",
      modelCategory: "segmentation",
      modelId: Ex.DEFAULT_MODEL_ID_BY_CATEGORY.segmentation,
      file: null,
      frameSequencePath: "",
      personalSensitive: false,
      localPath: "",
      manifest: null,
      jobRequest: null,
      runnerBridge: null,
      sha256Status: "pending_runner_computation",
      statusMessage: ""
    };

    root.innerHTML =
      "<section class='lai-section' aria-label='local test asset import'>" +
      "<header class='lai-header'><h2>本地测试资产导入</h2>" +
      (advancedOnly
        ? "<p class='muted'>生成 manifest JSON（candidate-only · 不执行模型）。</p>"
        : "<p class='muted'>登记 candidate test asset，生成 manifest / job / runner bridge。本页<strong>不执行模型</strong>。</p>") +
      "</header>" +
      "<div class='lai-grid'>" +
      "<label>资产类型<select id='lai-asset-type'></select></label>" +
      "<label>目标模型类别<select id='lai-model-category'></select></label>" +
      "<label>模型 ID<input id='lai-model-id' type='text' /></label>" +
      "<label id='lai-file-label'>本地文件<input id='lai-file-input' type='file' /></label>" +
      (advancedOnly
        ? "<label>本机路径（服务登记）<input id='lai-local-path' type='text' placeholder='完整或相对路径' /></label>"
        : "") +
      "<label id='lai-frame-seq-label' class='lai-frame-seq' hidden>帧序列目录路径（占位）" +
      "<input id='lai-frame-seq-path' type='text' placeholder='例如 /path/to/frames （仅登记，不读取目录）' /></label>" +
      "<label class='lai-check'><input id='lai-sensitive-flag' type='checkbox' /> 可能含个人敏感信息（用户声明）</label>" +
      "</div>" +
      "<div class='lai-actions'>" +
      "<button type='button' id='lai-generate-manifest' class='btn btn-primary'>生成 Manifest</button>" +
      "<button type='button' id='lai-copy-manifest' class='btn btn-ghost' disabled>复制 Manifest JSON</button>" +
      "<button type='button' id='lai-download-manifest' class='btn btn-ghost' disabled>下载 Manifest（candidate-only）</button>" +
      "</div>" +
      "<div id='lai-human-summary' class='lai-human-summary'" + (advancedOnly ? " hidden" : "") + "></div>" +
      "<div id='lai-context-hints' class='lai-context-hints'" + (advancedOnly ? " hidden" : "") + "></div>" +
      "<p id='lai-status-msg' class='lai-status-msg' role='status'></p>" +
      "</section>";

    var assetSel = root.querySelector("#lai-asset-type");
    var catSel = root.querySelector("#lai-model-category");
    var modelIdInput = root.querySelector("#lai-model-id");
    var fileInput = root.querySelector("#lai-file-input");
    var frameSeqLabel = root.querySelector("#lai-frame-seq-label");
    var frameSeqPath = root.querySelector("#lai-frame-seq-path");
    var sensitiveChk = root.querySelector("#lai-sensitive-flag");
    var humanSummary = root.querySelector("#lai-human-summary");
    var contextHints = root.querySelector("#lai-context-hints");
    var statusMsg = root.querySelector("#lai-status-msg");

    Ex.ASSET_TYPES.forEach(function (t) {
      var o = document.createElement("option");
      o.value = t;
      o.textContent = t;
      assetSel.appendChild(o);
    });
    Ex.MODEL_CATEGORIES.forEach(function (c) {
      var o = document.createElement("option");
      o.value = c;
      o.textContent = c;
      catSel.appendChild(o);
    });

    function renderHumanSummary() {
      var runnerType = Ex.RUNNER_TYPE_BY_CATEGORY[state.modelCategory] || "—";
      var html =
        "<dl class='kv-list lai-kv'>" +
        "<dt>已选择文件</dt><dd>" + (state.file ? state.file.name : state.frameSequencePath || "—") + "</dd>" +
        "<dt>资产类型</dt><dd>" + state.assetType + "</dd>" +
        "<dt>目标模型类别</dt><dd>" + state.modelCategory + "</dd>" +
        "<dt>推荐 runner 类型</dt><dd><code>" + runnerType + "</code></dd>" +
        "<dt>当前状态</dt><dd><strong>" + statusLabel(state) + "</strong></dd>" +
        "</dl>" +
        "<div class='lai-next-steps'>" +
        "<p><strong>下一步：</strong></p>" +
        "<ol>" +
        "<li>复制/保存 job request 后，在<strong>独立 runner phase</strong> 中执行（需 owner approval）。</li>" +
        "<li>runner 产出 envelope 后，在上方「导入测试结果」加载 JSON 查看结果。</li>" +
        "</ol>" +
        "<p class='muted'>candidate-only · 非 fact source · 非 runtime input</p>" +
        "</div>";
      humanSummary.innerHTML = html;
    }

    function renderContextHints() {
      var lines = [];
      if (
        (state.assetType === "video" || state.assetType === "frame_sequence") &&
        state.modelCategory === "slam_vio"
      ) {
        lines = Ex.SLAM_HINT_LINES;
      } else if (
        state.assetType === "image" &&
        ["segmentation", "ocr", "depth_world", "multimodal_vlm"].indexOf(state.modelCategory) >= 0
      ) {
        lines = Ex.IMAGE_HINT_LINES;
      }
      if (!lines.length) {
        contextHints.innerHTML = "";
        contextHints.hidden = true;
        return;
      }
      contextHints.hidden = false;
      contextHints.innerHTML =
        "<div class='lai-hint-box'><h3>专用提示</h3><ul>" +
        lines.map(function (l) { return "<li>" + l + "</li>"; }).join("") +
        "</ul></div>";
    }

    function syncFileAccept() {
      var accept = Ex.FILE_ACCEPT_BY_ASSET_TYPE[state.assetType] || "";
      fileInput.accept = accept;
      var isFrameSeq = state.assetType === "frame_sequence";
      frameSeqLabel.hidden = !isFrameSeq;
      fileInput.multiple = isFrameSeq;
    }

    function notify() {
      renderHumanSummary();
      renderContextHints();
      onStateChange(state);
    }

    assetSel.addEventListener("change", function () {
      state.assetType = assetSel.value;
      state.manifest = null;
      state.jobRequest = null;
      state.runnerBridge = null;
      syncFileAccept();
      notify();
    });

    catSel.addEventListener("change", function () {
      state.modelCategory = catSel.value;
      state.modelId = Ex.DEFAULT_MODEL_ID_BY_CATEGORY[state.modelCategory] || "";
      modelIdInput.value = state.modelId;
      state.jobRequest = null;
      state.runnerBridge = null;
      notify();
    });

    modelIdInput.addEventListener("input", function () {
      state.modelId = modelIdInput.value.trim();
    });

    fileInput.addEventListener("change", function (ev) {
      var files = ev.target.files;
      state.file = files && files.length ? files[0] : null;
      if (state.assetType === "frame_sequence" && files && files.length > 1) {
        state.frameSequencePath = "browser_multi_file://" + files.length + "_frames";
      }
      state.manifest = null;
      state.jobRequest = null;
      state.runnerBridge = null;
      notify();
    });

    frameSeqPath.addEventListener("input", function () {
      state.frameSequencePath = frameSeqPath.value.trim();
      notify();
    });

    sensitiveChk.addEventListener("change", function () {
      state.personalSensitive = sensitiveChk.checked;
    });

    var localPathInput = root.querySelector("#lai-local-path");
    if (localPathInput) {
      localPathInput.addEventListener("input", function () {
        state.localPath = localPathInput.value.trim();
      });
    }

    root.querySelector("#lai-generate-manifest").addEventListener("click", function () {
      if (!state.file && state.assetType !== "frame_sequence" && state.assetType !== "text") {
        statusMsg.textContent = "请先选择本地文件。";
        statusMsg.className = "lai-status-msg error";
        return;
      }
      if (state.assetType === "frame_sequence" && !state.file && !state.frameSequencePath) {
        statusMsg.textContent = "帧序列请至少选择多文件或填写目录路径占位。";
        statusMsg.className = "lai-status-msg error";
        return;
      }

      function finalize(shaInfo, mediaMeta) {
        state.sha256Status = shaInfo.status;
        state.manifest = buildManifestPreview({
          assetType: state.assetType,
          file: state.file,
          frameSequencePath: state.frameSequencePath || state.localPath,
          modelCategory: state.modelCategory,
          personalSensitive: state.personalSensitive,
          sha256Status: shaInfo.status,
          sha256: shaInfo.value || undefined,
          mediaMetadataStatus: mediaMeta ? "browser_computed" : "pending_runner_or_browser_computed",
          mediaMetadata: mediaMeta || undefined
        });
        state.jobRequest = null;
        state.runnerBridge = null;
        if (state.localPath && state.manifest) {
          state.manifest.local_path = state.localPath;
          state.manifest.local_path_or_browser_file_name = state.localPath;
        }
        root.querySelector("#lai-copy-manifest").disabled = false;
        root.querySelector("#lai-download-manifest").disabled = false;
        statusMsg.textContent = "Manifest 已生成（仅浏览器内 preview，未上传、未执行模型）。";
        statusMsg.className = "lai-status-msg ok";
        notify();
      }

      if (state.file && global.FileReader) {
        var reader = new FileReader();
        reader.onload = function (ev) {
          var buf = ev.target.result;
          var mediaMeta = {
            byte_length: buf.byteLength || (state.file && state.file.size),
            mime_type: state.file && state.file.type ? state.file.type : undefined
          };
          computeSha256Browser(buf).then(function (shaInfo) {
            finalize(shaInfo, mediaMeta);
          });
        };
        reader.onerror = function () {
          finalize({ status: "pending_runner_computation", value: null }, null);
        };
        reader.readAsArrayBuffer(state.file);
      } else {
        finalize({ status: "pending_runner_computation", value: null }, null);
      }
    });

    root.querySelector("#lai-copy-manifest").addEventListener("click", function () {
      if (!state.manifest) return;
      copyJson(state.manifest, function (err) {
        statusMsg.textContent = err ? "复制失败（请使用下载）" : "Manifest JSON 已复制。";
        statusMsg.className = err ? "lai-status-msg error" : "lai-status-msg ok";
      });
    });

    root.querySelector("#lai-download-manifest").addEventListener("click", function () {
      if (!state.manifest) return;
      downloadJson(state.manifest.manifest_id + ".json", state.manifest);
    });

    syncFileAccept();
    modelIdInput.value = state.modelId;
    notify();

    return {
      getState: function () { return state; },
      setDebugMode: function () { /* debug handled by app.js */ }
    };
  }

  global.LocalAssetImportUI = {
    init: initLocalAssetImportUI,
    buildManifestPreview: buildManifestPreview,
    downloadJson: downloadJson,
    copyJson: copyJson,
    statusLabel: statusLabel,
    uid: uid
  };
})(typeof window !== "undefined" ? window : this);

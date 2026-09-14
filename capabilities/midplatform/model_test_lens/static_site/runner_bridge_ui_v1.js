/**
 * Model Test Lens — runner bridge UI v1.
 * Generates job request and runner bridge request in-browser only.
 * lens_may_not_execute_runner = true. No model execution.
 */
(function (global) {
  "use strict";

  var Ex = global.LocalAssetImportExamples;
  var Lai = global.LocalAssetImportUI;

  function buildJobRequest(manifest, modelCategory, modelId) {
    if (!manifest) return null;
    return {
      job_request_id: Lai.uid("job"),
      created_by_lens: true,
      created_at: new Date().toISOString(),
      asset_manifest_ref_or_inline: manifest.manifest_id,
      asset_manifest_ref: manifest.manifest_id,
      asset_manifest_inline: manifest,
      requested_model_category: modelCategory,
      requested_model_id: modelId,
      requested_test_profile: "default_candidate_test_profile_v1",
      prompt_plan_ref_or_pending: "pending_user_or_governed_prompt_plan",
      prompt_plan_ref: "pending_user_or_governed_prompt_plan",
      expected_adapter: Ex.EXPECTED_ADAPTER_BY_CATEGORY[modelCategory] || "generic_evaluation_adapter_v1",
      expected_envelope_schema: Ex.EXPECTED_ENVELOPE_SCHEMA,
      candidate_output_only: true,
      requires_runner_execution: true,
      requires_owner_approval: true,
      requires_test_board_record: true,
      runtime_allowed: false,
      output_adapter_allowed: false,
      semantic_layer_allowed: false,
      fact_write_allowed: false,
      navigation_action_speech_allowed: false,
      page_must_not_execute_model: true
    };
  }

  function buildRunnerBridgeRequest(jobRequest) {
    if (!jobRequest) return null;
    var runnerType = Ex.RUNNER_TYPE_BY_CATEGORY[jobRequest.requested_model_category] || "segmentation_runner";
    return {
      runner_bridge_request_id: Lai.uid("runner_bridge"),
      created_at: new Date().toISOString(),
      job_request_ref_or_inline: jobRequest.job_request_id,
      job_request_ref: jobRequest.job_request_id,
      job_request_inline: jobRequest,
      runner_type: runnerType,
      runner_allowed_to_execute_model: false,
      runner_execution_phase_required: true,
      runner_requires_separate_owner_approval: true,
      requires_owner_approval: true,
      runner_output_expected: {
        raw_model_output: true,
        metrics: true,
        diagnostics: true,
        candidate_outputs: true,
        test_board_refs: true
      },
      adapter_required: true,
      adapter_target_envelope: Ex.EXPECTED_ENVELOPE_SCHEMA,
      lens_may_read_runner_output: true,
      lens_may_not_execute_runner: true,
      lens_may_not_modify_runner_output: true,
      page_must_not_execute_model: true
    };
  }

  function initRunnerBridgeUI(options) {
    var root = options.rootEl;
    var getImportState = options.getImportState;
    var onStateChange = options.onStateChange || function () {};
    var statusMsgEl = options.statusMsgEl;
    var advancedOnly = !!options.advancedOnly;

    root.innerHTML =
      "<section class='rb-section' aria-label='runner bridge'>" +
      "<header class='rb-header'><h3>测试任务与 Runner Bridge</h3>" +
      "<p class='muted'>生成 job / runner bridge request（不启动 runner）。</p></header>" +
      "<div class='lai-actions'>" +
      "<button type='button' id='rb-create-job' class='btn btn-secondary'>创建 Test Job Request</button>" +
      "<button type='button' id='rb-copy-job' class='btn btn-ghost' disabled>复制 Job Request</button>" +
      "<button type='button' id='rb-download-job' class='btn btn-ghost' disabled>下载 Job Request</button>" +
      "<button type='button' id='rb-create-bridge' class='btn btn-secondary'>创建 Runner Bridge Request</button>" +
      "<button type='button' id='rb-copy-bridge' class='btn btn-ghost' disabled>复制 Bridge Request</button>" +
      "<button type='button' id='rb-download-bridge' class='btn btn-ghost' disabled>下载 Bridge Request</button>" +
      "</div>" +
      "<div id='rb-runner-status' class='rb-runner-status' aria-live='polite'></div>" +
      (advancedOnly ? "" :
        "<div class='rb-local-service' id='rb-local-service'>" +
        "<h4>本地 Runner Bridge 服务（127.0.0.1:8787）</h4>" +
        "<p class='muted'>页面不执行模型；由本地服务跑测试 runner。</p>" +
        "<div class='lai-actions'>" +
        "<button type='button' id='rb-check-service' class='btn btn-ghost'>检查服务</button>" +
        "<button type='button' id='rb-register-via-service' class='btn btn-secondary'>登记资产到服务</button>" +
        "<button type='button' id='rb-create-job-via-service' class='btn btn-secondary'>创建 Job</button>" +
        "<button type='button' id='rb-run-job-via-service' class='btn btn-primary'>运行本地测试</button>" +
        "<button type='button' id='rb-load-result-via-service' class='btn btn-ghost'>加载结果 Envelope</button>" +
        "</div>" +
        "<p id='rb-service-status' class='lai-status-msg'></p>" +
        "</div>") +
      (advancedOnly ?
        "<div class='rb-advanced-service' id='rb-advanced-service'>" +
        "<h4>服务分步操作（高级）</h4>" +
        "<div class='lai-actions'>" +
        "<button type='button' id='rb-check-service' class='btn btn-ghost'>检查服务</button>" +
        "<button type='button' id='rb-register-via-service' class='btn btn-secondary'>登记资产到服务</button>" +
        "<button type='button' id='rb-create-job-via-service' class='btn btn-secondary'>创建 Job</button>" +
        "<button type='button' id='rb-run-job-via-service' class='btn btn-secondary'>运行本地测试</button>" +
        "<button type='button' id='rb-load-result-via-service' class='btn btn-ghost'>加载结果 Envelope</button>" +
        "</div>" +
        "<p id='rb-service-status' class='lai-status-msg'></p>" +
        "</div>" : "") +
      "</section>";

    var copyJobBtn = root.querySelector("#rb-copy-job");
    var dlJobBtn = root.querySelector("#rb-download-job");
    var copyBridgeBtn = root.querySelector("#rb-copy-bridge");
    var dlBridgeBtn = root.querySelector("#rb-download-bridge");
    var statusHost = root.querySelector("#rb-runner-status");

    function renderRunnerStatus(importState) {
      var st = importState || getImportState();
      var runnerType = Ex.RUNNER_TYPE_BY_CATEGORY[st.modelCategory] || "—";
      var adapter = Ex.EXPECTED_ADAPTER_BY_CATEGORY[st.modelCategory] || "—";
      var phase = st.runnerBridge
        ? "runner_bridge_ready"
        : st.jobRequest
          ? "job_request_ready"
          : st.manifest
            ? "manifest_ready"
            : "waiting_for_manifest";
      var waiting = !st.runnerBridge;
      statusHost.innerHTML =
        "<div class='rb-status-card'>" +
        "<h4>Runner 输出状态（占位）</h4>" +
        "<dl class='kv-list'>" +
        "<dt>状态</dt><dd><strong>" + (waiting ? "waiting_for_runner_output" : "runner_bridge_request_ready") + "</strong></dd>" +
        "<dt>workflow phase</dt><dd>" + phase + "</dd>" +
        "<dt>expected_runner_type</dt><dd><code>" + runnerType + "</code></dd>" +
        "<dt>expected_adapter</dt><dd><code>" + adapter + "</code></dd>" +
        "<dt>expected_envelope</dt><dd><code>" + Ex.EXPECTED_ENVELOPE_SCHEMA + "</code></dd>" +
        "<dt>import_envelope_when_ready</dt><dd>使用页头「导入测试结果」加载 runner 产出的 envelope JSON</dd>" +
        "</dl>" +
        "<p class='muted'>lens_may_not_execute_runner = true · adapter_required = true</p>" +
        "</div>";
    }

    function setMsg(text, cls) {
      if (!statusMsgEl) return;
      statusMsgEl.textContent = text;
      statusMsgEl.className = "lai-status-msg " + (cls || "");
    }

    root.querySelector("#rb-create-job").addEventListener("click", function () {
      var st = getImportState();
      if (!st.manifest) {
        setMsg("请先生成 Manifest。", "error");
        return;
      }
      st.jobRequest = buildJobRequest(st.manifest, st.modelCategory, st.modelId);
      st.runnerBridge = null;
      copyJobBtn.disabled = false;
      dlJobBtn.disabled = false;
      copyBridgeBtn.disabled = true;
      dlBridgeBtn.disabled = true;
      setMsg("Job Request 已生成（requires_runner_execution · requires_owner_approval）。", "ok");
      renderRunnerStatus(st);
      onStateChange(st);
    });

    root.querySelector("#rb-create-bridge").addEventListener("click", function () {
      var st = getImportState();
      if (!st.jobRequest) {
        setMsg("请先生成 Job Request。", "error");
        return;
      }
      st.runnerBridge = buildRunnerBridgeRequest(st.jobRequest);
      copyBridgeBtn.disabled = false;
      dlBridgeBtn.disabled = false;
      setMsg("Runner Bridge Request 已生成（页面不执行 runner）。", "ok");
      renderRunnerStatus(st);
      onStateChange(st);
    });

    copyJobBtn.addEventListener("click", function () {
      var st = getImportState();
      if (!st.jobRequest) return;
      Lai.copyJson(st.jobRequest, function (err) {
        setMsg(err ? "复制失败" : "Job Request JSON 已复制。", err ? "error" : "ok");
      });
    });

    dlJobBtn.addEventListener("click", function () {
      var st = getImportState();
      if (!st.jobRequest) return;
      Lai.downloadJson(st.jobRequest.job_request_id + ".json", st.jobRequest);
    });

    copyBridgeBtn.addEventListener("click", function () {
      var st = getImportState();
      if (!st.runnerBridge) return;
      Lai.copyJson(st.runnerBridge, function (err) {
        setMsg(err ? "复制失败" : "Runner Bridge Request JSON 已复制。", err ? "error" : "ok");
      });
    });

    dlBridgeBtn.addEventListener("click", function () {
      var st = getImportState();
      if (!st.runnerBridge) return;
      Lai.downloadJson(st.runnerBridge.runner_bridge_request_id + ".json", st.runnerBridge);
    });

    renderRunnerStatus(getImportState());

    var SERVICE_BASE = "http://127.0.0.1:8787";
    var serviceState = { jobId: null, capabilities: null };

    function serviceMsg(text, cls) {
      var el = root.querySelector("#rb-service-status");
      if (!el) return;
      el.textContent = text;
      el.className = "lai-status-msg " + (cls || "");
    }

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

    root.querySelector("#rb-check-service").addEventListener("click", function () {
      serviceFetch("/api/v1/capabilities").then(function (res) {
        if (res.ok) {
          serviceState.capabilities = res.data;
          serviceMsg("服务可用 · " + (res.data.service_name || "runner bridge") + " · localhost-only", "ok");
        } else {
          serviceMsg("服务不可用，请先启动: python3 -m capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_server_v1", "error");
        }
      }).catch(function () {
        serviceMsg("无法连接 127.0.0.1:8787", "error");
      });
    });

    root.querySelector("#rb-register-via-service").addEventListener("click", function () {
      var st = getImportState();
      if (!st.manifest && !st.file) {
        serviceMsg("请先在上方生成 Manifest 或选择文件", "error");
        return;
      }
      var body = {
        asset_type: st.assetType,
        model_category: st.modelCategory,
        requested_model_id: st.modelId,
        browser_file_name: st.file ? st.file.name : st.manifest.local_file_name,
        local_path: st.localPath || (st.manifest ? st.manifest.local_path : null),
        candidate_only: true
      };
      serviceFetch("/api/v1/assets/register", { method: "POST", body: body }).then(function (res) {
        if (res.ok) {
          st.serviceAsset = res.data;
          serviceMsg("资产已登记: " + res.data.asset_id, "ok");
          onStateChange(st);
        } else {
          serviceMsg("登记失败: " + JSON.stringify(res.data), "error");
        }
      }).catch(function (e) {
        serviceMsg("登记请求失败", "error");
      });
    });

    root.querySelector("#rb-create-job-via-service").addEventListener("click", function () {
      var st = getImportState();
      var manifest = (st.serviceAsset && st.serviceAsset.asset_manifest) || st.manifest;
      if (!manifest) {
        serviceMsg("请先登记资产或生成 Manifest", "error");
        return;
      }
      serviceFetch("/api/v1/jobs/create", {
        method: "POST",
        body: {
          asset_manifest: manifest,
          requested_model_category: st.modelCategory,
          requested_model_id: st.modelId
        }
      }).then(function (res) {
        if (res.ok) {
          serviceState.jobId = res.data.job_id;
          serviceMsg("Job 已创建: " + res.data.job_id, "ok");
        } else {
          serviceMsg("创建 Job 失败", "error");
        }
      });
    });

    root.querySelector("#rb-run-job-via-service").addEventListener("click", function () {
      if (!serviceState.jobId) {
        serviceMsg("请先创建 Job", "error");
        return;
      }
      serviceMsg("运行中…", "");
      serviceFetch("/api/v1/jobs/" + serviceState.jobId + "/run", { method: "POST", body: {} }).then(function (res) {
        serviceMsg("运行完成 · status=" + (res.data.status || res.status), res.ok ? "ok" : "error");
        renderRunnerStatus(getImportState());
      });
    });

    root.querySelector("#rb-load-result-via-service").addEventListener("click", function () {
      if (!serviceState.jobId) {
        serviceMsg("无 Job ID", "error");
        return;
      }
      serviceFetch("/api/v1/jobs/" + serviceState.jobId + "/result").then(function (res) {
        if (res.ok && res.data.envelope && global.ModelTestLens && global.ModelTestLens.renderEnvelopeFromService) {
          global.ModelTestLens.renderEnvelopeFromService(res.data.envelope);
          serviceMsg("Envelope 已加载到结果视图", "ok");
        } else if (res.ok && !res.data.envelope) {
          serviceMsg("尚无 envelope（status=" + res.data.status + "）", "error");
        } else {
          serviceMsg("加载失败", "error");
        }
      });
    });

    return {
      renderRunnerStatus: renderRunnerStatus,
      buildJobRequest: buildJobRequest,
      buildRunnerBridgeRequest: buildRunnerBridgeRequest
    };
  }

  global.RunnerBridgeUI = {
    init: initRunnerBridgeUI,
    buildJobRequest: buildJobRequest,
    buildRunnerBridgeRequest: buildRunnerBridgeRequest
  };
})(typeof window !== "undefined" ? window : this);

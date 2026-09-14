/**
 * Luna Observation Lens — compact UI orchestrator v1.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.LunaObservationCopy || {}; };
  var I18n = function () { return global.LunaObservationLabelI18n; };
  var Ex = function () { return global.VisualOverlayExamples; };
  var VR = function () { return global.VisualOverlayRenderer; };

  var DEFAULT_VISIBLE_ITEMS = 2;

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function localizeItem(text) {
    if (!text) return text;
    return I18n() ? I18n().localizeCategoryInText(text) : text;
  }

  function renderSectionBlock(host, title, items, maxVisible) {
    maxVisible = maxVisible == null ? DEFAULT_VISIBLE_ITEMS : maxVisible;
    var filtered = (items || []).filter(Boolean).map(localizeItem);
    if (!filtered.length) return;

    var block = document.createElement("section");
    block.className = "lol-rp-section";
    block.innerHTML = "<h3>" + escapeHtml(title) + "</h3>";

    var visible = filtered.slice(0, maxVisible);
    var rest = filtered.slice(maxVisible);

    var ul = document.createElement("ul");
    ul.className = "lol-rp-list";
    visible.forEach(function (item) {
      var li = document.createElement("li");
      li.textContent = item;
      ul.appendChild(li);
    });
    block.appendChild(ul);

    if (rest.length) {
      var more = document.createElement("details");
      more.className = "lol-rp-more";
      more.innerHTML = "<summary>" + escapeHtml(Copy().expandMore || "展开更多") + "</summary>";
      var ul2 = document.createElement("ul");
      ul2.className = "lol-rp-list";
      rest.forEach(function (item) {
        var li = document.createElement("li");
        li.textContent = item;
        ul2.appendChild(li);
      });
      more.appendChild(ul2);
      block.appendChild(more);
    }

    host.appendChild(block);
  }

  function renderRightPanel(host, envelope, pkg, reasoning, options) {
    options = options || {};
    host.innerHTML =
      "<div id='lol-right-situation-host'></div>" +
      "<div id='lol-right-agent-planning-host'></div>" +
      "<div id='lol-right-attention-host'></div>" +
      "<div id='lol-right-activation-host'></div>" +
      "<div id='lol-right-dual-route-host'></div>" +
      "<div id='lol-right-queue-host'></div>" +
      "<div id='lol-right-request-host'></div>" +
      "<div id='lol-right-execution-host'></div>" +
      "<div id='lol-right-result-host'></div>" +
      "<div id='lol-right-midplatform-host'></div>" +
      "<div id='lol-right-collaboration-host'></div>" +
      "<div id='lol-right-ocr-controlled-host'></div>" +
      "<div id='lol-right-reasoning-host'></div>" +
      "<div id='lol-right-selected-host'></div>";
    var situationHost = host.querySelector("#lol-right-situation-host");
    var agentPlanningHost = host.querySelector("#lol-right-agent-planning-host");
    var attentionHost = host.querySelector("#lol-right-attention-host");
    var activationHost = host.querySelector("#lol-right-activation-host");
    var dualRouteHost = host.querySelector("#lol-right-dual-route-host");
    var queueHost = host.querySelector("#lol-right-queue-host");
    var requestHost = host.querySelector("#lol-right-request-host");
    var executionHost = host.querySelector("#lol-right-execution-host");
    var resultHost = host.querySelector("#lol-right-result-host");
    var midplatformHost = host.querySelector("#lol-right-midplatform-host");
    var collaborationHost = host.querySelector("#lol-right-collaboration-host");
    var ocrControlledHost = host.querySelector("#lol-right-ocr-controlled-host");
    var reasoningHost = host.querySelector("#lol-right-reasoning-host");
    var selectedHost = host.querySelector("#lol-right-selected-host");

    if (global.LunaSituationUnderstandingPanel) {
      global.LunaSituationUnderstandingPanel.render(situationHost, options.situationPkg, {
        onSelectAttentionHint: options.onSelectAttentionHint
      });
    } else if (situationHost) {
      situationHost.innerHTML = "";
      situationHost.hidden = true;
    }

    if (global.LunaAgentPlanningPanel) {
      global.LunaAgentPlanningPanel.render(agentPlanningHost, options.agentPlanningPkg, {});
    } else if (agentPlanningHost) {
      agentPlanningHost.innerHTML = "";
      agentPlanningHost.hidden = true;
    }

    if (global.ObservationAttentionPriorityPanel && options.attentionPkg) {
      global.ObservationAttentionPriorityPanel.render(attentionHost, options.attentionPkg, {
        selectedRegionId: options.selectedEntity && options.selectedEntity.entity_id,
        noAttentionRegionId: options.noAttentionRegionId || null,
        getEntityGlyph: options.getEntityGlyph,
        getEntityShortLabel: options.getEntityShortLabel,
        onSelectRegion: options.onSelectRegion,
        onHoverRegion: options.onHoverRegion
      });
    } else if (attentionHost) {
      attentionHost.innerHTML = "";
      attentionHost.hidden = true;
    }

    if (global.SceneTaskModelActivationPanel) {
      global.SceneTaskModelActivationPanel.render(activationHost, options.activationPkg, {
        onSelectAssignment: options.onActivationAssignmentSelect
      });
    } else if (activationHost) {
      activationHost.innerHTML = "";
      activationHost.hidden = true;
    }

    if (global.DualRoutePerceptionPanel) {
      global.DualRoutePerceptionPanel.render(dualRouteHost, options.dualRoutePkg, {});
    } else if (dualRouteHost) {
      dualRouteHost.innerHTML = "";
      dualRouteHost.hidden = true;
    }

    if (global.FollowupRunnerRouteQueuePanel && options.queuePkg) {
      global.FollowupRunnerRouteQueuePanel.render(queueHost, options.queuePkg, {
        selectedRegionId: options.selectedEntity && options.selectedEntity.entity_id,
        onSelectRegion: options.onSelectRegion,
        onHoverRegion: options.onHoverRegion,
      onQueueAction: options.onQueueAction,
      onActivationAssignmentSelect: options.onActivationAssignmentSelect,
      requestStore: options.requestStore
      });
    } else if (queueHost) {
      queueHost.innerHTML = "";
      queueHost.hidden = true;
    }

    if (global.RunnerManualTriggerRequestPanel) {
      global.RunnerManualTriggerRequestPanel.render(requestHost, options.requestPkg, {
        selectedRegionId: options.selectedEntity && options.selectedEntity.entity_id,
        onSelectRegion: options.onSelectRegion,
        onHoverRegion: options.onHoverRegion,
        onRequestAction: options.onRequestAction
      });
    } else if (requestHost) {
      requestHost.innerHTML = "";
      requestHost.hidden = true;
    }

    if (global.ControlledRunnerExecutionPanel) {
      global.ControlledRunnerExecutionPanel.render(executionHost, options.executionPkg, {
        selectedRegionId: options.selectedEntity && options.selectedEntity.entity_id,
        onSelectRegion: options.onSelectRegion,
        onHoverRegion: options.onHoverRegion,
        onExecutionAction: options.onExecutionAction
      });
    } else if (executionHost) {
      executionHost.innerHTML = "";
      executionHost.hidden = true;
    }

    if (global.ResultLayerPanel) {
      global.ResultLayerPanel.render(resultHost, options.resultPkg, {
        selectedRegionId: options.selectedEntity && options.selectedEntity.entity_id,
        onSelectRegion: options.onSelectRegion,
        onHoverRegion: options.onHoverRegion
      });
    } else if (resultHost) {
      resultHost.innerHTML = "";
      resultHost.hidden = true;
    }

    if (global.MidplatformInteractionPanel) {
      global.MidplatformInteractionPanel.render(midplatformHost, options.midplatformPkg, {
        selectedRegionId: options.selectedEntity && options.selectedEntity.entity_id
      });
    } else if (midplatformHost) {
      midplatformHost.innerHTML = "";
      midplatformHost.hidden = true;
    }

    if (global.MultiModelCollaborationPanel) {
      var activeOcrTaskIds = {};
      if (options.ocrPkg && options.ocrPkg.requests) {
        options.ocrPkg.requests.forEach(function (r) {
          if (r.admission_status !== "cancelled" && r.admission_status !== "rejected") {
            activeOcrTaskIds[r.source_ocr_task_candidate_id] = true;
          }
        });
      }
      global.MultiModelCollaborationPanel.render(collaborationHost, options.collaborationPkg, {
        activeOcrTaskIds: activeOcrTaskIds
      });
    } else if (collaborationHost) {
      collaborationHost.innerHTML = "";
      collaborationHost.hidden = true;
    }

    if (global.MobileSamOcrControlledExecutionPanel) {
      global.MobileSamOcrControlledExecutionPanel.render(ocrControlledHost, options.ocrPkg, {
        selectedRegionId: options.selectedEntity && options.selectedEntity.entity_id
      });
      if (options.onOcrAction && !ocrControlledHost._ocrBound) {
        global.MobileSamOcrControlledExecutionPanel.bindActions(ocrControlledHost, options.onOcrAction);
        ocrControlledHost._ocrBound = true;
      }
    } else if (ocrControlledHost) {
      ocrControlledHost.innerHTML = "";
      ocrControlledHost.hidden = true;
    }

    if (global.HudReasoningCompression && reasoning) {
      global.HudReasoningCompression.renderCompressedPanel(reasoningHost, reasoning, {
        onReportIssue: options.onReportIssue
      });
    } else {
      reasoningHost.innerHTML = "<h2 class='lol-rp-title'>" + Copy().rightPanelTitle + "</h2>";
      if (pkg) renderSectionBlock(reasoningHost, Copy().sections.current_task, [localizeItem(pkg.oneLiner)], 1);
    }

    if (options.selectedEntity && global.HudSelectedObjectDetail) {
      global.HudSelectedObjectDetail.render(selectedHost, options.selectedEntity, {
        showClose: true,
        onClose: options.onClearSelection || function () {},
        onMarkProblem: options.onMarkProblem
      });
    }
  }

  function renderPlaceholderRight(host) {
    host.innerHTML =
      "<h2 class='lol-rp-title'>" + Copy().rightPanelTitle + "</h2>" +
      "<p class='muted'>开始观察后，Luna 会在这里解释它看到了什么、哪里不确定、建议怎么补测。</p>";
  }

  function renderCentralEmpty(host) {
    host.innerHTML =
      "<div class='lol-canvas-empty'>" +
      "<div class='lol-canvas-empty-inner'>" +
      "<p>" + Copy().emptyCanvas + "</p>" +
      "</div></div>";
  }

  function renderOriginal(host, envelope) {
    var sourceRef = Ex().pickSourceImageRef(envelope);
    host.innerHTML =
      "<div class='lol-canvas-wrap'>" +
      "<canvas id='lol-original-canvas' class='lol-main-canvas'></canvas>" +
      "<div id='lol-canvas-warn' class='lol-canvas-warn' hidden></div></div>";
    var canvas = host.querySelector("#lol-original-canvas");
    var warn = host.querySelector("#lol-canvas-warn");
    if (!sourceRef) {
      warn.hidden = false;
      warn.textContent = "缺少原图。";
      return;
    }
    VR().loadImage(Ex().artifactUrl(sourceRef)).then(function (img) {
      var maxW = host.clientWidth - 16 || 640;
      var maxH = host.clientHeight - 16 || 480;
      var fit = VR().fitSize(img.naturalWidth, img.naturalHeight, maxW, maxH);
      canvas.width = fit.w;
      canvas.height = fit.h;
      canvas.getContext("2d").drawImage(img, 0, 0, fit.w, fit.h);
    }).catch(function () {
      warn.hidden = false;
      warn.textContent = "无法加载原图。请确认本地测试服务 (8787) 已启动。";
    });
  }

  function renderCompareCentral(host, envelope, debugMode) {
    host.innerHTML = "<div id='lol-compare-inner' class='lol-compare-inner'></div>";
    if (global.VisualCompareView) {
      global.VisualCompareView.render(host.querySelector("#lol-compare-inner"), envelope, {
        debugMode: debugMode,
        compact: true
      });
    }
  }

  function renderHudCentral(host, envelope, debugMode, hudOptions) {
    hudOptions = hudOptions || {};
    if (global.PerceptionHUDView && global.PerceptionHUDView.renderCentral) {
      return global.PerceptionHUDView.renderCentral(host, envelope, {
        debugMode: debugMode,
        layoutMode: "canvas-first",
        attentionPkg: hudOptions.attentionPkg || null,
        onEntitiesChange: hudOptions.onEntitiesChange,
        onHudCanvasReady: hudOptions.onHudCanvasReady,
        onCanvasEntitySelect: hudOptions.onCanvasEntitySelect
      });
    }
    host.innerHTML = "<p class='muted'>HUD 模块未加载。</p>";
    return null;
  }

  function renderCentral(host, envelope, viewMode, debugMode, hudOptions) {
    if (!envelope) {
      renderCentralEmpty(host);
      return null;
    }
    viewMode = viewMode || "hud";
    if (viewMode === "original") {
      renderOriginal(host, envelope);
      return null;
    }
    if (viewMode === "compare") {
      renderCompareCentral(host, envelope, debugMode);
      return null;
    }
    return renderHudCentral(host, envelope, debugMode, hudOptions);
  }

  function buildMetricsSummary(envelope, pkg, attentionPkg, queuePkg, requestPkg, executionPkg, resultPkg, ocrPkg, dualRoutePkg, activationPkg, situationPkg, agentPlanningPkg) {
    if (!envelope || !pkg) return "<span class='muted'>等待观察结果…</span>";
    var m = envelope.metrics || {};
    var riskLine = "主要风险：未发现显著失败";
    if (global.HudColorSemantics && global.PerceptionHUDView) {
      var hudPkg = global.PerceptionHUDView.buildAnnotationPackage(envelope);
      if (hudPkg.ok && hudPkg.annotation && hudPkg.annotation.entities) {
        riskLine = global.HudColorSemantics.summarizeRisk(hudPkg.annotation.entities);
      }
    }
    var success = "";
    if (m.prompt_success_count != null && I18n()) {
      success = I18n().formatPromptSuccess(m.prompt_success_count, m.prompt_attempt_count);
    } else if (m.slam) {
      success = "空间定位综合分 " + (m.slam.slam_score || "—");
    }
    var base = "综合分 <strong>" + escapeHtml(pkg.verdict.scorePercent) + "</strong>｜" +
      escapeHtml(success || pkg.verdict.statusLabel) + "｜" + escapeHtml(riskLine) +
      "｜仅模型评估";
    if (global.ObservationAttentionSummary && attentionPkg) {
      base = global.ObservationAttentionSummary.appendToMetricsSummary(base, attentionPkg);
    }
    if (global.FollowupRunnerRouteSummary && queuePkg) {
      base = global.FollowupRunnerRouteSummary.appendToMetricsSummary(base, queuePkg);
    }
    if (global.RunnerManualTriggerSummary && requestPkg) {
      base = global.RunnerManualTriggerSummary.appendToMetricsSummary(base, requestPkg);
    }
    if (global.RunnerInvocationAdmissionSummary && requestPkg) {
      base = global.RunnerInvocationAdmissionSummary.appendToMetricsSummary(base, requestPkg);
    }
    if (global.ControlledRunnerExecutionSummary && executionPkg) {
      base = global.ControlledRunnerExecutionSummary.appendToMetricsSummary(base, executionPkg);
    }
    if (global.ResultLayerSummary && resultPkg) {
      base = global.ResultLayerSummary.appendToMetricsSummary(base, resultPkg);
    }
    if (global.MobileSamOcrControlledExecutionSummary && ocrPkg) {
      base = global.MobileSamOcrControlledExecutionSummary.appendToMetricsSummary(base, ocrPkg);
    }
    if (global.LunaSituationUnderstandingSummary && situationPkg) {
      var sitLine = global.LunaSituationUnderstandingSummary.summaryLine(situationPkg);
      if (sitLine) base += "｜<span class='muted'>" + escapeHtml(sitLine) + "</span>";
    }
    if (global.LunaAgentPlanningSummary && agentPlanningPkg) {
      var planLine = global.LunaAgentPlanningSummary.summaryLine(agentPlanningPkg);
      if (planLine) base += "｜<span class='muted'>" + escapeHtml(planLine) + "</span>";
    }
    if (global.DualRoutePerceptionSummary && dualRoutePkg) {
      var drLine = global.DualRoutePerceptionSummary.summaryLine(dualRoutePkg);
      if (drLine) base += "｜<span class='muted'>" + escapeHtml(drLine) + "</span>";
    }
    if (global.SceneTaskModelActivationSummary && activationPkg) {
      var actLine = global.SceneTaskModelActivationSummary.summaryLine(activationPkg);
      if (actLine) base += "｜<span class='muted'>" + escapeHtml(actLine) + "</span>";
    }
    var scene = envelope.scene_profile_candidate;
    if (scene && scene.scene_type_candidate) {
      base += "｜<span class='muted'>scene_profile: " + escapeHtml(scene.scene_type_candidate) +
        " candidate · prompt labels are hints, not facts</span>";
    }
    return base;
  }

  global.LunaObservationCompactUI = {
    renderRightPanel: renderRightPanel,
    renderPlaceholderRight: renderPlaceholderRight,
    renderCentral: renderCentral,
    renderCentralEmpty: renderCentralEmpty,
    buildMetricsSummary: buildMetricsSummary,
    getReasoning: function (envelope) {
      if (global.PerceptionHUDView && global.PerceptionHUDView.buildAnnotationPackage) {
        var pkg = global.PerceptionHUDView.buildAnnotationPackage(envelope);
        return pkg.ok ? pkg.reasoning : null;
      }
      return null;
    }
  };
})(typeof window !== "undefined" ? window : this);

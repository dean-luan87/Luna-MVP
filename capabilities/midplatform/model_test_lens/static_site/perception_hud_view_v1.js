/**
 * Model Test Lens — Perception HUD View v1 (robot vision explainable overlay).
 * Read-only; display-only annotations; candidate-only.
 */
(function (global) {
  "use strict";

  var Ex = global.VisualOverlayExamples;
  var VR = global.VisualOverlayRenderer;
  var HUDEx = global.PerceptionHUDExamples;
  var MSAdapter = global.PerceptionHUDMobileSAMAdapter;
  var HUDRenderer = global.PerceptionHUDRenderer;
  var ReasoningPanel = global.PerceptionHUDReasoningPanel;
  var HUDControls = global.PerceptionHUDControls;
  var HudPolicy = global.HudVisualPolicy;
  var VL = global.HudAttentionVisualLanguage;

  function defaultHudState() {
    var base = HudPolicy && HudPolicy.createDefaultState
      ? HudPolicy.createDefaultState()
      : {
        showLineBox: true,
        showLabels: true,
        showUncertainty: true,
        showMaskFill: false,
        maskFillOpacity: 0.35,
        showAllAttentionMarkers: false
      };
    base.showAllAttentionMarkers = base.showAllAttentionMarkers === true;
    base.routeFilter = base.routeFilter || "all";
    return base;
  }

  function hudRenderOptions(state, maxW, maxH, extra) {
    extra = extra || {};
    return {
      maxWidth: maxW,
      maxHeight: maxH,
      showLineBox: state.showLineBox,
      showLabels: state.showLabels,
      showUncertainty: state.showUncertainty,
      showMaskFill: state.showMaskFill,
      maskFillOpacity: state.maskFillOpacity,
      highlightEntityId: state.highlightEntityId || null,
      hoverEntityId: state.hoverEntityId || null,
      attentionPkg: extra.attentionPkg || state.attentionPkg || null,
      debugMode: !!extra.debugMode,
      showDebugGuidelines: !!state.showDebugGuidelines && !!extra.debugMode,
      dimP2Opacity: state.dimP2Opacity,
      dimP3Opacity: state.dimP3Opacity,
      sceneStructureFillOpacity: state.sceneStructureFillOpacity,
      showAttentionIndicators: true,
      visualLanguageSeparation: true,
      showAttentionMarkers: state.showAttentionMarkers !== false,
      showAllAttentionMarkers: !!state.showAllAttentionMarkers,
      onHitItemsReady: extra.onHitItemsReady
    };
  }

  var _currentApi = null;

  function supportsHUD(envelope) {
    if (!envelope) return false;
    if (HUDEx && HUDEx.canGenerateHUD(envelope)) return true;
    var cat = envelope.model_category;
    var modelId = envelope.model_id;
    return cat === "segmentation" || modelId === "mobile_sam";
  }

  function buildAnnotationPackage(envelope) {
    var cat = envelope.model_category;
    var modelId = envelope.model_id;
    if (cat === "segmentation" || modelId === "mobile_sam") {
      if (!MSAdapter) return { ok: false, message: "MobileSAM HUD 适配器未加载。" };
      var result = MSAdapter.createSceneAnnotation(envelope);
      if (!result.ok) return result;
      var reasoning = MSAdapter.createReasoningPanel(envelope, result.annotation);
      return {
        ok: true,
        annotation: result.annotation,
        reasoning: reasoning,
        layers: result.layers,
        sourceImageRef: result.sourceImageRef
      };
    }
    return {
      ok: false,
      message: "当前结果缺少可生成机器人视角的标注数据。"
    };
  }

  function renderHUDView(host, envelope, options) {
    options = options || {};
    var debugMode = !!options.debugMode;

    if (!supportsHUD(envelope)) {
      host.innerHTML =
        "<section class='phud-section'>" +
        "<h3>机器人视角 HUD</h3>" +
        "<p class='muted'>当前结果缺少可生成机器人视角的标注数据。</p>" +
        "</section>";
      _currentApi = null;
      return null;
    }

    var pkg = buildAnnotationPackage(envelope);
    if (!pkg.ok) {
      host.innerHTML =
        "<section class='phud-section'>" +
        "<h3>机器人视角 HUD</h3>" +
        "<p class='phud-warning'>" + (pkg.message || "无法生成 HUD。") + "</p>" +
        "</section>";
      _currentApi = null;
      return null;
    }

    host.innerHTML =
      "<section class='phud-section' id='phud-section'>" +
      "<div class='phud-header'>" +
      "<h3>机器人视角 HUD</h3>" +
      "<p class='muted phud-subtitle'>我看到了什么 · 哪里不确定 · 建议怎么补测</p>" +
      "</div>" +
      "<div id='phud-warning' class='phud-warning' hidden></div>" +
      "<div id='phud-controls-host'></div>" +
      "<div class='phud-layout' id='phud-layout'>" +
      "<div class='phud-col phud-col-original'><h4>原图</h4><canvas id='phud-original-canvas' class='phud-canvas'></canvas></div>" +
      "<div class='phud-col phud-col-hud'><h4>机器人视觉 HUD</h4><canvas id='phud-hud-canvas' class='phud-canvas'></canvas></div>" +
      "<div class='phud-col phud-col-reasoning'><h4>系统观察 / 推理 / 建议</h4><div id='phud-reasoning-host'></div></div>" +
      "</div>" +
      "<p class='phud-hint muted'>当前结果仅用于模型评估，不会写入事实层，也不会触发导航或语音输出。</p>" +
      (debugMode ? "<details class='phud-debug-json'><summary>Scene Annotation JSON（开发者）</summary><pre id='phud-annotation-debug' class='raw-json-pre'></pre></details>" : "") +
      "</section>";

    var warningEl = host.querySelector("#phud-warning");
    var originalCanvas = host.querySelector("#phud-original-canvas");
    var hudCanvas = host.querySelector("#phud-hud-canvas");
    var reasoningHost = host.querySelector("#phud-reasoning-host");
    var entities = pkg.annotation.entities || [];
    var layers = pkg.layers || [];

    ReasoningPanel.render(reasoningHost, pkg.reasoning, { debugMode: debugMode });

    if (debugMode) {
      var dbg = host.querySelector("#phud-annotation-debug");
      if (dbg) dbg.textContent = JSON.stringify(pkg.annotation, null, 2);
    }

    var state = defaultHudState();

    var controlsApi = HUDControls.create(
      host.querySelector("#phud-controls-host"),
      state,
      function () { redraw(); },
      { debugMode: debugMode }
    );
    controlsApi.renderLayerToggles(entities, layers);

    function drawOriginal(img) {
      if (!VR) return;
      var fit = VR.fitSize(img.naturalWidth, img.naturalHeight, 400, 360);
      originalCanvas.width = fit.w;
      originalCanvas.height = fit.h;
      var ctx = originalCanvas.getContext("2d");
      ctx.drawImage(img, 0, 0, fit.w, fit.h);
    }

    function redraw() {
      var url = Ex.artifactUrl(pkg.sourceImageRef);
      VR.loadImage(url).then(function (img) {
        drawOriginal(img);
        var pairs = entities.map(function (e, i) {
          return { entity: e, layer: layers[i] };
        }).filter(function (p) {
          return p.layer && p.layer.visible !== false && !p.entity._hidden;
        });
        var visibleEntities = pairs.map(function (p) { return p.entity; });
        var visibleLayers = pairs.map(function (p) { return p.layer; });
        return HUDRenderer.renderHUDCanvas(hudCanvas, img, visibleEntities, visibleLayers,
          hudRenderOptions(state, 480, 360, { debugMode: debugMode }));
      }).then(function (meta) {
        if (meta && meta.warnings && meta.warnings.length) {
          warningEl.hidden = false;
          warningEl.textContent = "部分识别层无法读取或尺寸不一致，已尽力显示。";
        } else {
          warningEl.hidden = true;
        }
      }).catch(function (err) {
        warningEl.hidden = false;
        var msg = (err && err.message) ? String(err.message) : "";
        if (msg === "image_load_failed" || msg === "missing_url") {
          warningEl.textContent = "无法加载原图。请确认本地测试服务 (8787) 已启动，并刷新页面。";
        } else {
          warningEl.textContent = "HUD 渲染失败（" + (msg || "未知错误") + "）。请刷新页面重试。";
        }
      });
    }

    redraw();

    _currentApi = {
      redraw: redraw,
      annotation: pkg.annotation,
      reasoning: pkg.reasoning,
      switchToHUD: function () {
        var section = document.getElementById("phud-section");
        if (section) section.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    };
    return _currentApi;
  }

  function createViewModeToggle(host, onModeChange, initialMode) {
    host.innerHTML =
      "<div class='view-mode-toggle' role='tablist' aria-label='结果视图切换'>" +
      "<button type='button' class='view-mode-btn' data-mode='compare' role='tab'>普通对比</button>" +
      "<button type='button' class='view-mode-btn' data-mode='hud' role='tab'>机器人视角 HUD</button>" +
      "</div>";

    var mode = initialMode || "compare";
    var buttons = host.querySelectorAll(".view-mode-btn");

    function setMode(m) {
      mode = m;
      buttons.forEach(function (btn) {
        var active = btn.dataset.mode === mode;
        btn.classList.toggle("active", active);
        btn.setAttribute("aria-selected", active ? "true" : "false");
      });
      onModeChange(mode);
    }

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        setMode(btn.dataset.mode);
      });
    });

    setMode(mode);
    return { setMode: setMode, getMode: function () { return mode; } };
  }

  function getCurrentApi() {
    return _currentApi;
  }

  function renderCentralHUD(host, envelope, options) {
    options = options || {};
    var debugMode = !!options.debugMode;
    var canvasFirst = options.layoutMode !== "legacy";

    if (!supportsHUD(envelope)) {
      host.innerHTML =
        "<div class='lol-canvas-empty'><p class='muted'>当前结果缺少可生成机器人视角的标注数据。</p></div>";
      return null;
    }

    var pkg = buildAnnotationPackage(envelope);
    if (!pkg.ok) {
      host.innerHTML =
        "<div class='lol-canvas-empty'><p class='phud-warning'>" + (pkg.message || "无法生成 HUD。") + "</p></div>";
      return null;
    }

    host.innerHTML =
      "<div class='lol-hud-central" + (canvasFirst ? " lol-hud-canvas-first" : "") + "' id='phud-central'>" +
      "<div id='phud-warning' class='phud-warning' hidden></div>" +
      "<div id='phud-controls-host' class='lol-hud-controls-bar" + (canvasFirst ? " lol-hud-controls-compact" : "") + "'></div>" +
      "<div class='lol-hud-canvas-wrap'>" +
      "<canvas id='phud-hud-canvas' class='lol-main-canvas phud-canvas'></canvas>" +
      "</div>" +
      (canvasFirst ? "" : "<div id='phud-external-panel-host' class='hud-external-panel-host'></div>") +
      (debugMode ? "<details class='phud-debug-json'><summary>Scene Annotation JSON（开发者）</summary><pre id='phud-annotation-debug' class='raw-json-pre'></pre></details>" : "") +
      "</div>";

    var warningEl = host.querySelector("#phud-warning");
    var hudCanvas = host.querySelector("#phud-hud-canvas");
    var externalHost = canvasFirst ? null : host.querySelector("#phud-external-panel-host");
    var entities = pkg.annotation.entities || [];
    var layers = pkg.layers || [];
    var externalPanelApi = null;
    var resizeObserver = null;
    var hitItems = [];
    var displaySize = { w: 0, h: 0 };
    var canvasClickHandler = null;
    var canvasHoverHandler = null;
    var canvasLeaveHandler = null;

    if (debugMode) {
      var dbg = host.querySelector("#phud-annotation-debug");
      if (dbg) dbg.textContent = JSON.stringify(pkg.annotation, null, 2);
    }

    var state = defaultHudState();
    state.highlightEntityId = null;
    state.hoverEntityId = null;
    state.entityFilter = "all";
    state.attentionPkg = options.attentionPkg || null;

    var controlsApi = HUDControls.create(
      host.querySelector("#phud-controls-host"),
      state,
      function () {
        if (!canvasFirst) refreshExternalPanel();
        syncChipBar();
        redraw();
      },
      { debugMode: debugMode, compact: canvasFirst }
    );
    if (!canvasFirst) controlsApi.renderLayerToggles(entities, layers);

    function visiblePairs() {
      return entities.map(function (e, i) {
        return { entity: e, layer: layers[i] };
      }).filter(function (p) {
        if (!p.layer || p.layer.visible === false || p.entity._hidden) return false;
        if (controlsApi.entityPassesFilter && !controlsApi.entityPassesFilter(p.entity)) return false;
        return true;
      });
    }

    function syncChipBar() {
      if (options.onEntitiesChange) {
        options.onEntitiesChange(entities, {
          highlightEntityId: state.highlightEntityId,
          hoverEntityId: state.hoverEntityId,
          setHighlight: function (id) {
            state.highlightEntityId = id;
            redraw();
          },
          setHover: function (id) {
            state.hoverEntityId = id;
            redraw();
          }
        });
      }
    }

    function refreshExternalPanel() {
      if (!externalHost || !global.HudExternalAnnotationPanel) return;
      externalPanelApi = global.HudExternalAnnotationPanel.render(externalHost, entities, {
        filterId: state.entityFilter,
        selectedEntityId: state.highlightEntityId,
        hoverEntityId: state.hoverEntityId,
        onSelect: function (entityId) {
          state.highlightEntityId = state.highlightEntityId === entityId ? null : entityId;
          refreshExternalPanel();
          redraw();
        },
        onHover: function (entityId) {
          state.hoverEntityId = entityId;
          refreshExternalPanel();
          redraw();
        },
        onToggleHidden: function (entityId) {
          entities.forEach(function (e, i) {
            if (e.entity_id === entityId) {
              e._hidden = true;
              if (layers[i]) layers[i].visible = false;
            }
          });
          refreshExternalPanel();
          redraw();
        }
      });
    }

    function attachCanvasInteraction() {
      if (!hudCanvas || !VL) return;
      if (canvasClickHandler) hudCanvas.removeEventListener("click", canvasClickHandler);
      if (canvasHoverHandler) hudCanvas.removeEventListener("mousemove", canvasHoverHandler);
      if (canvasLeaveHandler) hudCanvas.removeEventListener("mouseleave", canvasLeaveHandler);

      function renderOpts() {
        return hudRenderOptions(state, displaySize.w, displaySize.h,
          { debugMode: debugMode, attentionPkg: state.attentionPkg });
      }

      canvasClickHandler = function (ev) {
        if (!hitItems.length) return;
        var pt = VL.canvasPoint(hudCanvas, ev.clientX, ev.clientY, displaySize.w, displaySize.h);
        var entity = VL.hitTest(hitItems, pt.x, pt.y, renderOpts());
        if (entity && options.onCanvasEntitySelect) {
          options.onCanvasEntitySelect(entity.entity_id);
        }
      };

      canvasHoverHandler = function (ev) {
        if (!hitItems.length) return;
        var pt = VL.canvasPoint(hudCanvas, ev.clientX, ev.clientY, displaySize.w, displaySize.h);
        var entity = VL.hitTest(hitItems, pt.x, pt.y, renderOpts());
        var nextId = entity ? entity.entity_id : null;
        if (state.hoverEntityId !== nextId) {
          state.hoverEntityId = nextId;
          redraw();
        }
      };

      canvasLeaveHandler = function () {
        if (state.hoverEntityId) {
          state.hoverEntityId = null;
          redraw();
        }
      };

      hudCanvas.addEventListener("click", canvasClickHandler);
      hudCanvas.addEventListener("mousemove", canvasHoverHandler);
      hudCanvas.addEventListener("mouseleave", canvasLeaveHandler);
      hudCanvas.style.cursor = "crosshair";
    }

    function redraw() {
      var wrap = host.querySelector(".lol-hud-canvas-wrap");
      var maxW = (wrap && wrap.clientWidth) ? wrap.clientWidth - 8 : 640;
      var maxH = (wrap && wrap.clientHeight) ? wrap.clientHeight - 8 : 480;
      var url = Ex.artifactUrl(pkg.sourceImageRef);
      VR.loadImage(url).then(function (img) {
        var pairs = visiblePairs();
        var visibleEntities = pairs.map(function (p) { return p.entity; });
        var visibleLayers = pairs.map(function (p) { return p.layer; });
        return HUDRenderer.renderHUDCanvas(hudCanvas, img, visibleEntities, visibleLayers,
          hudRenderOptions(state, maxW, maxH, {
            debugMode: debugMode,
            attentionPkg: state.attentionPkg,
            onHitItemsReady: function (items, w, h) {
              hitItems = items || [];
              displaySize.w = w;
              displaySize.h = h;
            }
          }));
      }).then(function (meta) {
        if (meta && meta.hitItems) {
          hitItems = meta.hitItems;
          displaySize.w = meta.width || displaySize.w;
          displaySize.h = meta.height || displaySize.h;
        }
        attachCanvasInteraction();
        if (meta && meta.warnings && meta.warnings.length) {
          warningEl.hidden = false;
          warningEl.textContent = "部分识别层无法读取或尺寸不一致，已尽力显示。";
        } else {
          warningEl.hidden = true;
        }
      }).catch(function (err) {
        warningEl.hidden = false;
        var msg = (err && err.message) ? String(err.message) : "";
        if (msg === "image_load_failed" || msg === "missing_url") {
          warningEl.textContent = "无法加载原图。请确认本地测试服务 (8787) 已启动，并刷新页面。";
        } else {
          warningEl.textContent = "HUD 渲染失败（" + (msg || "未知错误") + "）。请刷新页面重试。";
        }
      });
    }

    if (!canvasFirst) refreshExternalPanel();
    syncChipBar();
    redraw();

    if (options.onHudCanvasReady && hudCanvas) {
      options.onHudCanvasReady(hudCanvas, host.querySelector("#phud-controls-host"));
    }

    var wrapEl = host.querySelector(".lol-hud-canvas-wrap");
    if (wrapEl && global.ResizeObserver) {
      resizeObserver = new global.ResizeObserver(function () { redraw(); });
      resizeObserver.observe(wrapEl);
    } else if (wrapEl) {
      global.addEventListener("resize", redraw);
    }

    _currentApi = {
      redraw: redraw,
      annotation: pkg.annotation,
      reasoning: pkg.reasoning,
      entities: entities,
      layers: layers,
      highlightEntity: function (id) {
        state.highlightEntityId = id;
        syncChipBar();
        redraw();
      },
      hoverEntity: function (id) {
        state.hoverEntityId = id;
        redraw();
      },
      getHighlightId: function () { return state.highlightEntityId; },
      getHudCanvas: function () { return hudCanvas; },
      setAttentionPkg: function (pkg) {
        state.attentionPkg = pkg || null;
        if (controlsApi.bindAttentionPkg) controlsApi.bindAttentionPkg(pkg);
      },
      destroy: function () {
        if (resizeObserver) resizeObserver.disconnect();
        if (hudCanvas) {
          if (canvasClickHandler) hudCanvas.removeEventListener("click", canvasClickHandler);
          if (canvasHoverHandler) hudCanvas.removeEventListener("mousemove", canvasHoverHandler);
          if (canvasLeaveHandler) hudCanvas.removeEventListener("mouseleave", canvasLeaveHandler);
        }
      }
    };
    return _currentApi;
  }

  global.PerceptionHUDView = {
    supportsHUD: supportsHUD,
    buildAnnotationPackage: buildAnnotationPackage,
    render: renderHUDView,
    renderCentral: renderCentralHUD,
    createViewModeToggle: createViewModeToggle,
    getCurrentApi: getCurrentApi
  };
})(typeof window !== "undefined" ? window : this);

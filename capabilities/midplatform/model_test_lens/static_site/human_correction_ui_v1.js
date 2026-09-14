/**
 * Human Correction Layer V1 — UI orchestrator.
 * Candidate-only; does not modify envelope or model output.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.HumanCorrectionCopy || {}; };
  var Store = function () { return global.HumanCorrectionStore; };
  var Picker = function () { return global.HumanCorrectionTargetPicker; };
  var Modal = function () { return global.HumanCorrectionModal; };
  var Drawer = function () { return global.HumanCorrectionDrawer; };

  var _ctx = {
    getEnvelope: function () { return null; },
    getEntities: function () { return []; },
    onRecordsChange: function () {}
  };
  var _missingMode = false;
  var _missingStart = null;
  var _hudCanvas = null;

  function openForEntity(entity) {
    var envelope = _ctx.getEnvelope();
    if (!envelope || !entity || !Picker() || !Modal()) return;
    var target = Picker().chipTarget(entity, envelope);
    Modal().open({
      target: target,
      entity: entity,
      envelope: envelope,
      onSaved: _ctx.onRecordsChange
    });
  }

  function openForReasoning(sectionKey, text, index) {
    var envelope = _ctx.getEnvelope();
    if (!envelope || !Picker() || !Modal()) return;
    var target = Picker().reasoningTarget(sectionKey, text, envelope, index);
    Modal().open({
      target: target,
      envelope: envelope,
      prefillType: sectionKey.indexOf("risk") >= 0 ? "risk_assessment_error" :
        sectionKey.indexOf("recommend") >= 0 ? "recommendation_error" : "task_relevance_error",
      onSaved: _ctx.onRecordsChange
    });
  }

  function openForMissingRegion(region) {
    var envelope = _ctx.getEnvelope();
    if (!envelope || !Picker() || !Modal()) return;
    var target = Picker().missingRegionTarget(region, envelope);
    Modal().open({
      target: target,
      envelope: envelope,
      prefillType: "false_negative",
      user_marked_region: region,
      defaultFollowups: ["detection", "human_review"],
      onSaved: _ctx.onRecordsChange
    });
  }

  function setMissingRegionMode(on) {
    _missingMode = !!on;
    _missingStart = null;
    if (_hudCanvas) {
      _hudCanvas.classList.toggle("hc-missing-mode", _missingMode);
      _hudCanvas.style.cursor = _missingMode ? "crosshair" : "";
    }
    var btn = document.getElementById("hc-missing-region-btn");
    if (btn) {
      btn.textContent = _missingMode
        ? (Copy().buttons.cancelMissing || "取消漏识别标记")
        : (Copy().buttons.missingRegion || "标记漏识别");
      btn.classList.toggle("active", _missingMode);
    }
  }

  function canvasToImageCoords(canvas, clientX, clientY) {
    var rect = canvas.getBoundingClientRect();
    var scaleX = canvas.width / rect.width;
    var scaleY = canvas.height / rect.height;
    return {
      x: (clientX - rect.left) * scaleX,
      y: (clientY - rect.top) * scaleY
    };
  }

  function attachHudCanvas(canvas) {
    if (!canvas || canvas._hcBound) return;
    canvas._hcBound = true;
    _hudCanvas = canvas;

    canvas.addEventListener("click", function (ev) {
      if (_missingMode) return;
      var entities = _ctx.getEntities() || [];
      var pt = canvasToImageCoords(canvas, ev.clientX, ev.clientY);
      var hit = findEntityAtPoint(entities, pt);
      if (hit && typeof _ctx.onEntitySelect === "function") {
        _ctx.onEntitySelect(hit.entity_id);
      }
    });

    canvas.addEventListener("mousedown", function (ev) {
      if (!_missingMode || ev.button !== 0) return;
      _missingStart = canvasToImageCoords(canvas, ev.clientX, ev.clientY);
    });

    canvas.addEventListener("mouseup", function (ev) {
      if (!_missingMode || !_missingStart) return;
      var end = canvasToImageCoords(canvas, ev.clientX, ev.clientY);
      var dx = Math.abs(end.x - _missingStart.x);
      var dy = Math.abs(end.y - _missingStart.y);
      var region;
      if (dx < 8 && dy < 8) {
        region = { type: "point", data: [_missingStart.x, _missingStart.y] };
      } else {
        region = {
          type: "box",
          data: [
            Math.min(_missingStart.x, end.x),
            Math.min(_missingStart.y, end.y),
            Math.max(_missingStart.x, end.x),
            Math.max(_missingStart.y, end.y)
          ]
        };
      }
      _missingStart = null;
      setMissingRegionMode(false);
      openForMissingRegion(region);
    });
  }

  function findEntityAtPoint(entities, pt) {
    var best = null;
    var bestArea = Infinity;
    (entities || []).forEach(function (e) {
      if (e._hidden) return;
      var bb = e._hud_bbox || e.bbox;
      if (!bb || bb.w == null || bb.w < 4) return;
      if (pt.x >= bb.x && pt.x <= bb.x + bb.w && pt.y >= bb.y && pt.y <= bb.y + bb.h) {
        var area = bb.w * bb.h;
        if (area < bestArea) {
          bestArea = area;
          best = e;
        }
      }
    });
    return best;
  }

  function ensureMissingRegionButton(controlsHost) {
    if (!controlsHost || document.getElementById("hc-missing-region-btn")) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.id = "hc-missing-region-btn";
    btn.className = "btn btn-ghost btn-sm hc-missing-btn";
    btn.textContent = Copy().buttons.missingRegion || "标记漏识别";
    btn.addEventListener("click", function () {
      setMissingRegionMode(!_missingMode);
    });
    controlsHost.appendChild(btn);
  }

  function init(options) {
    options = options || {};
    _ctx.getEnvelope = options.getEnvelope || _ctx.getEnvelope;
    _ctx.getEntities = options.getEntities || _ctx.getEntities;
    _ctx.onEntitySelect = options.onEntitySelect;
    _ctx.onRecordsChange = options.onRecordsChange || function () {};

    if (Modal() && Modal().setOnSaved) {
      Modal().setOnSaved(_ctx.onRecordsChange);
    }

    return {
      openForEntity: openForEntity,
      openForReasoning: openForReasoning,
      openForMissingRegion: openForMissingRegion,
      attachHudCanvas: attachHudCanvas,
      ensureMissingRegionButton: ensureMissingRegionButton,
      setMissingRegionMode: setMissingRegionMode,
      renderDrawer: function (panel) {
        if (Drawer()) Drawer().render(panel);
      },
      getRecordCount: function () { return Store() ? Store().list().length : 0; }
    };
  }

  global.HumanCorrectionUI = {
    version: "human_correction_ui_v1",
    init: init,
    candidateOnly: true,
    correctionCandidateOnly: true,
    trainingSignalCandidate: true
  };
})(typeof window !== "undefined" ? window : this);

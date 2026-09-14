/**
 * SLAM Diagnostic Panels V1 — error curve, drift heatmap, failure timeline.
 * Candidate-only visualization. No model execution.
 */
(function (global) {
  "use strict";

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function layerByType(layers, type) {
    return (layers || []).find(function (l) { return l.layer_type === type; }) || null;
  }

  function colorForClass(cls) {
    if (cls === "low") return "#3ecf8e";
    if (cls === "high") return "#f07178";
    return "#f0b429";
  }

  function severityClass(sev) {
    if (sev === "critical" || sev === "high") return "sev-high";
    if (sev === "medium") return "sev-mid";
    return "sev-low";
  }

  function renderErrorCurvePanel(container, errorCurve) {
    if (!errorCurve || !errorCurve.length) {
      container.innerHTML = "<p class='muted'>No error curve data</p>";
      return;
    }
    var w = 440;
    var h = 160;
    var pad = 28;
    var errs = errorCurve.map(function (p) { return p.error; });
    var maxE = Math.max.apply(null, errs.concat([0.001]));
    var maxT = errorCurve[errorCurve.length - 1].t || errorCurve.length - 1;
    function mx(t) { return pad + (t / (maxT || 1)) * (w - 2 * pad); }
    function my(e) { return h - pad - (e / maxE) * (h - 2 * pad); }
    var path = errorCurve.map(function (p, i) {
      return (i === 0 ? "M" : "L") + mx(p.t).toFixed(1) + " " + my(p.error).toFixed(1);
    }).join(" ");
    var svg =
      "<svg class='diag-canvas' viewBox='0 0 " + w + " " + h + "' width='100%' height='160'>" +
      "<rect width='" + w + "' height='" + h + "' fill='#121820' rx='8'/>" +
      "<line x1='" + pad + "' y1='" + (h - pad) + "' x2='" + (w - pad) + "' y2='" + (h - pad) + "' stroke='#2a3548'/>" +
      "<line x1='" + pad + "' y1='" + pad + "' x2='" + pad + "' y2='" + (h - pad) + "' stroke='#2a3548'/>" +
      "<path d='" + path + "' fill='none' stroke='#4d9fff' stroke-width='2'/>" +
      "<text x='" + pad + "' y='14' fill='#8b9cb3' font-size='10'>time → error (m)</text>" +
      "<text x='" + (w - pad - 40) + "' y='" + (h - 6) + "' fill='#8b9cb3' font-size='9'>t</text>" +
      "</svg>";
    container.innerHTML = "<div class='diag-panel'><h4>误差曲线</h4>" + svg + "</div>";
  }

  function renderDriftHeatmapPanel(container, heatmap, trajLayer) {
    if (!heatmap || !heatmap.length) {
      container.innerHTML = "<p class='muted'>No drift heatmap data</p>";
      return;
    }
    var w = 440;
    var h = 200;
    var pad = 24;
    var allPts = [];
    heatmap.forEach(function (seg) {
      (seg.trajectory_segment || []).forEach(function (p) { allPts.push(p); });
    });
    if (!allPts.length && trajLayer && trajLayer.trajectory_ground_truth) {
      trajLayer.trajectory_ground_truth.forEach(function (p) { allPts.push([p[0], p[1]]); });
    }
    if (!allPts.length) {
      container.innerHTML = "<p class='muted'>No trajectory for heatmap</p>";
      return;
    }
    var xs = allPts.map(function (p) { return p[0]; });
    var ys = allPts.map(function (p) { return p[1]; });
    var minX = Math.min.apply(null, xs);
    var maxX = Math.max.apply(null, xs);
    var minY = Math.min.apply(null, ys);
    var maxY = Math.max.apply(null, ys);
    var spanX = maxX - minX || 1;
    var spanY = maxY - minY || 1;
    function mapX(x) { return pad + ((x - minX) / spanX) * (w - 2 * pad); }
    function mapY(y) { return h - pad - ((y - minY) / spanY) * (h - 2 * pad); }

    var paths = "";
    heatmap.forEach(function (seg) {
      var pts = seg.trajectory_segment || [];
      if (pts.length < 2) return;
      var d = pts.map(function (p, i) {
        return (i === 0 ? "M" : "L") + mapX(p[0]).toFixed(1) + " " + mapY(p[1]).toFixed(1);
      }).join(" ");
      paths += "<path d='" + d + "' fill='none' stroke='" + colorForClass(seg.color_class) +
        "' stroke-width='5' stroke-linecap='round' opacity='0.9'/>";
    });

    var legend =
      "<span class='hm-legend'><i style='background:#3ecf8e'></i>low</span>" +
      "<span class='hm-legend'><i style='background:#f0b429'></i>mid</span>" +
      "<span class='hm-legend'><i style='background:#f07178'></i>high</span>";

    container.innerHTML =
      "<div class='diag-panel'><h4>漂移热力图</h4>" + legend +
      "<svg class='diag-canvas' viewBox='0 0 " + w + " " + h + "' width='100%' height='200'>" +
      "<rect width='" + w + "' height='" + h + "' fill='#121820' rx='8'/>" + paths +
      "</svg></div>";
  }

  function renderFailureTimelinePanel(container, timeline) {
    if (!timeline || !timeline.length) {
      container.innerHTML = "<p class='muted'>No failure events detected</p>";
      return;
    }
    var maxT = timeline[timeline.length - 1].t || timeline.length;
    var html = "<div class='diag-panel'><h4>失败时间线</h4><ul class='timeline-list'>";
    timeline.forEach(function (ev) {
      var pct = maxT > 0 ? Math.min(100, (ev.t / maxT) * 100) : 0;
      html +=
        "<li class='timeline-item " + severityClass(ev.severity) + "'>" +
        "<span class='tl-marker' style='left:" + pct.toFixed(1) + "%'></span>" +
        "<span class='tl-time'>t=" + escapeHtml(String(ev.t)) + " f" + escapeHtml(String(ev.frame)) + "</span>" +
        "<strong>" + escapeHtml(ev.label || ev.event_type) + "</strong>" +
        "<code>" + escapeHtml(ev.event_type) + "</code></li>";
    });
    html += "</ul></div>";
    container.innerHTML = html;
  }

  function clientErrorCurveFromTrajectories(est, gt) {
    if (!est || !gt) return [];
    var n = Math.min(est.length, gt.length);
    var curve = [];
    for (var i = 0; i < n; i++) {
      var dx = est[i][0] - gt[i][0];
      var dy = est[i][1] - gt[i][1];
      var dz = (est[i][2] || 0) - (gt[i][2] || 0);
      curve.push({ frame: i, t: i * 0.1, error: Math.sqrt(dx * dx + dy * dy + dz * dz) });
    }
    return curve;
  }

  function renderAllDiagnosticPanels(host, envelope) {
    if (!host) return;
    var layers = envelope.visualization_layers || [];
    var diag = envelope.diagnostics || {};
    var diagInner = diag.diagnostics || {};

    var errorCurve = layerByType(layers, "error_curve");
    var heatmap = layerByType(layers, "drift_heatmap");
    var timeline = layerByType(layers, "failure_timeline");
    var traj = layerByType(layers, "trajectory");

    var curveData = (errorCurve && errorCurve.error_curve) || diagInner.error_curve;
    if (!curveData && traj) {
      curveData = clientErrorCurveFromTrajectories(
        traj.trajectory_estimated,
        traj.trajectory_ground_truth
      );
    }
    var heatData = (heatmap && heatmap.drift_heatmap) || diagInner.drift_heatmap;
    var tlData = (timeline && timeline.failure_timeline) || diagInner.failure_timeline;

    host.innerHTML =
      "<div id='slam-error-curve-host'></div>" +
      "<div id='slam-heatmap-host'></div>" +
      "<div id='slam-timeline-host'></div>";

    renderErrorCurvePanel(host.querySelector("#slam-error-curve-host"), curveData);
    renderDriftHeatmapPanel(host.querySelector("#slam-heatmap-host"), heatData, traj);
    renderFailureTimelinePanel(host.querySelector("#slam-timeline-host"), tlData);
  }

  global.SlamDiagnosticPanels = {
    renderErrorCurvePanel: renderErrorCurvePanel,
    renderDriftHeatmapPanel: renderDriftHeatmapPanel,
    renderFailureTimelinePanel: renderFailureTimelinePanel,
    renderAllDiagnosticPanels: renderAllDiagnosticPanels,
    layerByType: layerByType
  };
})(window);

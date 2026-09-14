/**
 * Model Insight Layer V1 — metrics → human-readable verdict & summary.
 * Candidate-only; does not grant runtime_ready.
 */
(function (global) {
  "use strict";

  var FAILURE_HUMAN_ZH = {
    drift: "轨迹出现累积漂移，长距离行走时误差会放大",
    drift_failure: "严重漂移：整体轨迹与真值偏差过大",
    short_term_drift: "短时段内误差快速上升，局部定位不稳定",
    tracking_lost: "部分帧跟踪丢失，定位曾中断",
    loop_closure_failure: "回环检测未能有效修正累积误差",
    localization_break: "定位突变：误差曲线斜率陡增",
    boundary_instability: "输出边界/轨迹段不稳定，存在反复抖动",
    under_segmentation: "分割不足：目标区域被截断或漏分",
    over_segmentation: "过度分割：掩膜超出真实物体边界",
    small_object_failure: "小目标（车辆、标识等）识别能力不足",
    misalignment: "预测结果与输入存在空间错位",
    low_confidence_collapse: "置信度崩溃：模型在部分样本上不敢给出稳定输出",
    hallucination: "存在幻觉式输出，与输入不符",
    tracking_lost: "跟踪中断，轨迹连续性受损"
  };

  var MODEL_DISPLAY_NAMES = {
    orb_slam: "空间定位",
    mobile_sam: "图像分割",
    vins: "视觉惯性定位",
    kimera: "空间定位"
  };

  var CATEGORY_LABELS = {
    slam_vio: "空间定位 / SLAM",
    segmentation: "图像分割",
    ocr: "文字识别",
    asr: "语音识别"
  };

  function categoryDisplayName(key) {
    if (!key) return "未知类别";
    if (global.LunaObservationLabelI18n && global.LunaObservationLabelI18n.mobileSamLabel) {
      return global.LunaObservationLabelI18n.mobileSamLabel(key).replace(/候选$/, "");
    }
    return String(key).replace(/_/g, " ");
  }

  function clamp01(v) {
    return Math.max(0, Math.min(1, Number(v) || 0));
  }

  function getOverallScore(envelope) {
    if (!envelope) return null;
    var m = envelope.metrics || {};
    if (m.slam && m.slam.slam_score != null) return clamp01(m.slam.slam_score);
    if (m.muep_final_score != null) return clamp01(m.muep_final_score);
    if (m.overall_success_rate != null) return clamp01(m.overall_success_rate);
    if (envelope.muep && envelope.muep.output && envelope.muep.output.metrics) {
      return clamp01(envelope.muep.output.metrics.final_score);
    }
    return null;
  }

  function getModelDisplayName(envelope) {
    if (!envelope) return "未知模型";
    var id = envelope.model_id || "";
    if (MODEL_DISPLAY_NAMES[id]) return MODEL_DISPLAY_NAMES[id];
    var cat = envelope.model_category || "";
    if (CATEGORY_LABELS[cat]) return CATEGORY_LABELS[cat];
    return id.replace(/_/g, " ") || "模型测试";
  }

  function deriveVerdict(envelope) {
    var score = getOverallScore(envelope);
    var modes = envelope.failure_modes || [];
    var qs = envelope.quality_summary || {};
    var runtimeBlocked = qs.suitable_for_runtime_admission === false;

    if (score == null) {
      return { status: "WARN", statusLabel: "待评估", score: null, scorePercent: "—" };
    }

    var critical = modes.some(function (m) {
      return /failure|lost|break|hallucination/i.test(m);
    });

    var status, statusLabel;
    if (score >= 0.78 && modes.length <= 1 && !critical) {
      status = "PASS";
      statusLabel = "可用";
    } else if (score >= 0.55 || (score >= 0.45 && modes.length <= 2)) {
      status = "WARN";
      statusLabel = "谨慎使用";
    } else {
      status = "FAIL";
      statusLabel = "不建议使用";
    }

    if (runtimeBlocked && status === "PASS") {
      status = "WARN";
      statusLabel = "研发可用 · 未进入生产";
    }

    return {
      status: status,
      statusLabel: statusLabel,
      score: score,
      scorePercent: Math.round(score * 100) + "%",
      runtimeBlocked: runtimeBlocked
    };
  }

  function humanizeFailure(mode) {
    var key = String(mode).toLowerCase().replace(/-/g, "_");
    return FAILURE_HUMAN_ZH[key] || FAILURE_HUMAN_ZH[mode] || String(mode).replace(/_/g, " ");
  }

  function topFailureModes(envelope, maxItems) {
    maxItems = maxItems || 3;
    var modes = envelope.failure_modes || [];
    if (envelope.diagnostics && envelope.diagnostics.failure_modes) {
      modes = modes.concat(envelope.diagnostics.failure_modes);
    }
    var seen = {};
    var out = [];
    modes.forEach(function (m) {
      if (!seen[m]) {
        seen[m] = true;
        out.push(humanizeFailure(m));
      }
    });
    return out.slice(0, maxItems);
  }

  function generateSlamInsights(envelope) {
    var lines = [];
    var slam = (envelope.metrics && envelope.metrics.slam) || {};
    var dm = (envelope.diagnostics && envelope.diagnostics.metrics) || {};
    var ate = slam.ate_rmse_m != null ? slam.ate_rmse_m : dm.ATE;
    var stability = slam.tracking_stability;
    var drift = slam.drift_rate;

    if (ate != null) {
      if (ate < 0.1) {
        lines.push("整体轨迹与真值吻合较好，绝对轨迹误差控制在较低水平。");
      } else if (ate < 0.2) {
        lines.push("轨迹大体可用，但存在一定累积误差，长直线路段需重点关注。");
      } else {
        lines.push("轨迹误差偏大，定位精度不足以支撑高可靠性场景。");
      }
    }

    if (stability != null) {
      if (stability >= 0.92) {
        lines.push("跟踪稳定性高，绝大多数帧保持连续定位。");
      } else if (stability >= 0.8) {
        lines.push("跟踪偶有丢失，末端或困难帧可能出现 re-localization。");
      } else {
        lines.push("跟踪稳定性不足，弱光或运动模糊场景下容易丢帧。");
      }
    }

    var timeline = (envelope.diagnostics && envelope.diagnostics.diagnostics &&
      envelope.diagnostics.diagnostics.failure_timeline) || [];
    var loopFail = timeline.some(function (e) { return e.event_type === "loop_closure_failure"; });
    var loopOk = timeline.some(function (e) { return e.event_type === "loop_closure_success"; });
    if (loopFail) {
      lines.push("回环检测未能有效拉回漂移，闭环修正能力偏弱。");
    } else if (loopOk) {
      lines.push("回环检测对误差有一定修复作用，闭环机制基本生效。");
    } else if (drift != null && drift > 0.02) {
      lines.push("漂移率偏高，越走越歪的风险需要结合 heatmap 查看起始段。");
    }

    return lines.slice(0, 3);
  }

  function generateSegmentationInsights(envelope) {
    var lines = [];
    var m = envelope.metrics || {};
    var rate = m.overall_success_rate;
    var perCat = m.per_category_average_score || {};

    if (rate != null) {
      if (rate >= 0.95) {
        lines.push("多图多 prompt 测试几乎全部成功，整体分割能力稳定。");
      } else if (rate >= 0.8) {
        lines.push("多数 prompt 可完成分割，但个别类别或场景仍有失败。");
      } else {
        lines.push("成功率偏低，当前权重或 prompt 策略需调整后再评估。");
      }
    }

    var cats = Object.keys(perCat);
    if (cats.length) {
      var sorted = cats.slice().sort(function (a, b) { return perCat[a] - perCat[b]; });
      var weak = sorted[0];
      var strong = sorted[sorted.length - 1];
      lines.push(
        "在「" + categoryDisplayName(strong) + "」类目标上表现较好，" +
        "「" + categoryDisplayName(weak) + "」类目标相对薄弱。"
      );
    }

    if ((envelope.failure_modes || []).length === 0) {
      lines.push("未记录明显失败模式，但仍为候选结果，不可直接作为产品事实。");
    } else {
      lines.push("存在已记录失败模式，建议展开指标详情查看分项结果。");
    }

    return lines.slice(0, 3);
  }

  function generateInsights(envelope) {
    if (!envelope) return ["加载测试 envelope 后，将自动生成模型结论与关键洞察。"];
    var cat = envelope.model_category || "";
    if (cat === "slam_vio" || envelope.model_id === "orb_slam") {
      return generateSlamInsights(envelope);
    }
    if (cat === "segmentation" || envelope.model_id === "mobile_sam") {
      return generateSegmentationInsights(envelope);
    }
    var v = deriveVerdict(envelope);
    return [
      "综合得分 " + v.scorePercent + "，状态：" + v.statusLabel + "。",
      (envelope.quality_summary && envelope.quality_summary.aggregate_note) ||
        "详见指标详情与中央观察画面。",
      "本结果为候选观察，不构成运行态准入或产品事实。"
    ].slice(0, 3);
  }

  function oneLineSummary(envelope) {
    var v = deriveVerdict(envelope);
    var failures = topFailureModes(envelope, 1)[0];
    var name = getModelDisplayName(envelope);
    if (v.status === "PASS") {
      return name + " 整体表现良好（" + v.scorePercent + "），可作为研发对比基线；" +
        (failures ? "需关注：" + failures : "未发现突出风险。");
    }
    if (v.status === "WARN") {
      return name + " 可用但需谨慎（" + v.scorePercent + "）。" +
        (failures ? "主要问题：" + failures : "建议结合可视化确认薄弱场景。");
    }
    return name + " 当前不建议采用（" + v.scorePercent + "）。" +
      (failures ? "核心问题：" + failures : "多项指标未达标。");
  }

  function buildInsightPackage(envelope) {
    return {
      modelDisplayName: getModelDisplayName(envelope),
      verdict: deriveVerdict(envelope),
      insights: generateInsights(envelope),
      oneLiner: oneLineSummary(envelope),
      topFailures: topFailureModes(envelope, 3),
      overallScore: getOverallScore(envelope)
    };
  }

  global.ModelInsightLayer = {
    buildInsightPackage: buildInsightPackage,
    deriveVerdict: deriveVerdict,
    generateInsights: generateInsights,
    humanizeFailure: humanizeFailure,
    topFailureModes: topFailureModes,
    getModelDisplayName: getModelDisplayName,
    getOverallScore: getOverallScore
  };
})(window);

/**
 * Luna Observation Lens — 默认界面中文显示映射 v1.
 * 仅用于 UI 展示；不修改 envelope 原始字段。
 */
(function (global) {
  "use strict";

  var MOBILE_SAM_LABELS = {
    road_sign: "路牌候选",
    left_building: "左侧建筑候选",
    building_or_large_structure: "建筑 / 大型结构候选",
    center_advertisement_screen: "中央广告屏候选",
    front_vehicle: "前方车辆候选",
    vehicle_or_small_dynamic_object: "车辆 / 小型动态目标候选",
    crosswalk_or_road_region: "斑马线 / 道路区域候选",
    road_or_crosswalk_or_large_plane: "道路 / 斑马线 / 大平面候选",
    street_facility_or_pole_or_edge_object: "街边设施 / 杆状物候选",
    sign_or_advertisement: "标识 / 广告区域候选",
    sign_or_advertisement_screen: "标识 / 广告屏候选"
  };

  var SPATIAL_PREFIX = {
    left: "左侧",
    center: "中央",
    right: "右侧",
    front: "前方",
    rear: "后方"
  };

  var MIME_LABELS = {
    "image/png": "图片",
    "image/jpeg": "图片",
    "image/jpg": "图片",
    "image/webp": "图片",
    "image/gif": "图片",
    "image/bmp": "图片",
    "video/mp4": "视频",
    "video/quicktime": "视频",
    "video/webm": "视频",
    "audio/mpeg": "音频",
    "audio/wav": "音频"
  };

  var STATUS_LABELS = {
    candidate_only: "候选结果",
    non_runtime: "非运行态",
    dev_not_prod: "研发可用 · 未进入生产",
    active_example_available: "示例可用",
    placeholder: "未接入",
    limited: "实验中"
  };

  var CAPABILITY_LABELS = {
    segmentation: "图像分割",
    mobile_sam: "图像分割",
    detection: "目标检测",
    detection_tracking: "目标检测 / 跟踪",
    ocr: "文字识别",
    slam: "空间定位 / SLAM",
    slam_vio: "空间定位 / SLAM",
    depth: "深度感知",
    depth_world: "深度感知 / 世界理解",
    asr: "语音识别",
    tts: "语音合成",
    speaker: "说话人识别",
    face: "表情 / 手势",
    face_expression_gesture: "表情 / 手势",
    vlm: "多模态理解",
    multimodal_vlm: "多模态理解"
  };

  function normalizeKey(s) {
    return String(s || "").trim().toLowerCase().replace(/\s+/g, "_");
  }

  function mobileSamLabel(raw) {
    if (!raw) return "识别区域候选";
    var key = normalizeKey(raw);
    if (MOBILE_SAM_LABELS[key]) return MOBILE_SAM_LABELS[key];
    var parts = key.split("_");
    var spatial = SPATIAL_PREFIX[parts[0]];
    if (spatial && parts.length > 1) {
      var rest = parts.slice(1).join("_");
      if (MOBILE_SAM_LABELS[rest]) return spatial + MOBILE_SAM_LABELS[rest].replace(/候选$/, "") + "候选";
    }
    var human = String(raw).replace(/_/g, " ");
    if (/候选$/.test(human)) return human;
    return human + "候选";
  }

  function mimeTypeLabel(mime) {
    if (!mime) return "本地测试资产";
    return MIME_LABELS[mime.toLowerCase()] || "本地测试资产";
  }

  function shortFileName(name) {
    if (!name) return "";
    var base = String(name).split("/").pop().split("\\").pop();
    if (base.length <= 28) return base;
    var ext = base.indexOf(".") >= 0 ? base.slice(base.lastIndexOf(".")) : "";
    return base.slice(0, 22) + "…" + ext;
  }

  function capabilityLabel(id) {
    return CAPABILITY_LABELS[normalizeKey(id)] || id;
  }

  function formatInputSummary(file, capabilityId) {
    if (!file) {
      return { title: "当前输入", line: "选择图片或视频开始观察" };
    }
    var cap = capabilityLabel(capabilityId || "segmentation");
    var typeLine = mimeTypeLabel(file.type);
    return {
      title: "当前输入",
      line: typeLine + " · 本地测试资产",
      fileShort: shortFileName(file.name),
      capabilityTitle: "当前能力",
      capabilityLine: cap + " · 可测试"
    };
  }

  function formatHudLabel(entity) {
    var raw = (entity && (entity._overlay && entity._overlay.label)) || (entity && entity.label) || "";
    var display = mobileSamLabel(raw);
    if (entity && entity.spatial_relation && entity.spatial_relation !== "unknown") {
      var sp = SPATIAL_PREFIX[entity.spatial_relation];
      if (sp && display.indexOf(sp) !== 0 && !MOBILE_SAM_LABELS[normalizeKey(raw)]) {
        display = sp + display.replace(/候选$/, "") + "候选";
      }
    }
    var percent = entity && entity.confidence != null
      ? Math.round(entity.confidence * 100) + "%"
      : "";
    return { label: display, percent: percent };
  }

  function formatPromptSuccess(success, attempt) {
    if (success == null) return "";
    return "提示测试成功 " + success + "/" + (attempt != null ? attempt : "—");
  }

  function localizeReasoningLine(text) {
    if (!text) return text;
    return String(text)
      .replace(/\bDetection\b/gi, "目标检测")
      .replace(/\bOCR\b/g, "文字识别")
      .replace(/\bYOLO\b/g, "目标检测")
      .replace(/\bMobileSAM\b/g, "图像分割模型")
      .replace(/\bprompt\b/gi, "分割提示")
      .replace(/\bcandidate\b/gi, "候选")
      .replace(/\brunner\b/gi, "本地测试服务")
      .replace(/\btracking\b/gi, "跟踪")
      .replace(/\bdepth\b/gi, "深度")
      .replace(/\bmask\b/gi, "分割区域");
  }

  function localizeCategoryInText(text) {
    var out = localizeReasoningLine(text);
    Object.keys(MOBILE_SAM_LABELS).forEach(function (k) {
      var re = new RegExp(k.replace(/_/g, "[_\\s]"), "gi");
      out = out.replace(re, MOBILE_SAM_LABELS[k].replace(/候选$/, ""));
    });
    return out;
  }

  global.LunaObservationLabelI18n = {
    STATUS: STATUS_LABELS,
    MOBILE_SAM_LABELS: MOBILE_SAM_LABELS,
    CAPABILITY_LABELS: CAPABILITY_LABELS,
    mobileSamLabel: mobileSamLabel,
    mimeTypeLabel: mimeTypeLabel,
    shortFileName: shortFileName,
    capabilityLabel: capabilityLabel,
    formatInputSummary: formatInputSummary,
    formatHudLabel: formatHudLabel,
    formatPromptSuccess: formatPromptSuccess,
    localizeReasoningLine: localizeReasoningLine,
    localizeCategoryInText: localizeCategoryInText
  };
})(typeof window !== "undefined" ? window : this);

/**
 * Human Correction Layer V1 — Chinese copy & embedded taxonomy.
 */
(function (global) {
  "use strict";

  var MODEL_ISSUE_TYPES = [
    { id: "false_positive", label: "误识别（多标了）", group: "model" },
    { id: "false_negative", label: "漏识别", group: "model" },
    { id: "wrong_label", label: "类别/标签错误", group: "model" },
    { id: "boundary_inaccurate", label: "分割边界错误", group: "model" },
    { id: "confidence_mismatch", label: "置信度不合理", group: "model" },
    { id: "duplicate_detection", label: "重复识别", group: "model" },
    { id: "priority_wrong", label: "优先级/关注度不合理", group: "model" },
    { id: "recommendation_error", label: "下一步建议不合理", group: "model" }
  ];

  var ENVIRONMENT_ISSUE_TYPES = [
    { id: "low_light", label: "光线不足", group: "environment" },
    { id: "occlusion", label: "遮挡", group: "environment" },
    { id: "motion_blur", label: "运动模糊", group: "environment" },
    { id: "reflective_glare", label: "反光/眩光", group: "environment" },
    { id: "crowded_scene", label: "场景拥挤杂乱", group: "environment" },
    { id: "small_or_far_target", label: "目标过小/过远", group: "environment" },
    { id: "background_interference", label: "背景纹理干扰", group: "environment" },
    { id: "image_quality_poor", label: "图像质量差", group: "environment" }
  ];

  var OTHER_ISSUE_TYPES = [
    { id: "unclear_need_review", label: "不确定，需人工复核", group: "other" },
    { id: "other_custom", label: "其他（见手写描述）", group: "other" }
  ];

  var CORRECTION_TYPES = MODEL_ISSUE_TYPES.concat(ENVIRONMENT_ISSUE_TYPES).concat(OTHER_ISSUE_TYPES);

  var SEVERITY = [
    { id: "low", label: "低" },
    { id: "medium", label: "中" },
    { id: "high", label: "高" },
    { id: "blocker", label: "阻断" }
  ];

  var FOLLOWUP_MODELS = [
    { id: "detection", label: "目标检测" },
    { id: "ocr", label: "文字识别" },
    { id: "slam", label: "SLAM" },
    { id: "depth", label: "深度感知" },
    { id: "human_review", label: "人工复核" },
    { id: "dataset_review", label: "数据集复核" }
  ];

  var FILTER_TABS = [
    { id: "all", label: "全部", multi: false },
    { id: "high", label: "高严重度", multi: true },
    { id: "model", label: "模型问题", multi: true },
    { id: "environment", label: "环境问题", multi: true },
    { id: "false_negative", label: "漏识别", multi: true },
    { id: "boundary_inaccurate", label: "边界错误", multi: true },
    { id: "other_custom", label: "手写标注", multi: true }
  ];

  global.HumanCorrectionCopy = {
    version: "human_correction_copy_v1",
    phaseRef: "Phase-P1-Midplatform-Model-Test-Lens-Human-Correction-Layer-UI-Execution-And-Post-Review-v1-001",
    buttons: {
      markChip: "指错",
      markProblem: "标记问题",
      reportIssue: "指出问题",
      save: "保存纠错记录",
      cancel: "取消",
      viewCorrections: "查看纠错",
      exportJson: "导出纠错记录",
      copyJson: "复制纠错 JSON",
      clearLocal: "清空本地纠错草稿",
      missingRegion: "标记漏识别",
      cancelMissing: "取消漏识别标记"
    },
    drawerTab: "纠错",
    modalTitle: "人工指错",
    boundaryNotice: "纠错记录仅用于模型评估和复测候选，不会修改原始模型结果。",
    notFactNotice: "这不是事实写入，也不是训练数据。",
    reviewNotice: "后续是否进入训练或复测，需要人工复核。",
    trainingPreviewTitle: "训练信号候选预览",
    trainingPreviewDisclaimer: "这不是训练数据，只是后续复测 / 数据集增强候选。",
    missingEnvelope: "缺少结果来源，不能生成纠错记录。",
    drawerEmpty: "暂无纠错记录。可以在对象胶囊、HUD 标注或右侧观察面板中标记问题。",
    drawerFilterHint: "筛选标签可多选；再次点击可取消。",
    statusPending: "待复核",
    modelIssueSection: "模型问题（可多选）",
    environmentIssueSection: "环境问题（可多选）",
    otherIssueSection: "其他",
    manualAnnotationLabel: "问题手写描述",
    manualAnnotationPlaceholder: "请用自己的话描述具体问题，例如：右侧白色车辆只框到一半、路牌被树遮挡看不清…",
    manualAnnotationHint: "建议填写。选了「其他」时必填。",
    modelIssues: MODEL_ISSUE_TYPES,
    environmentIssues: ENVIRONMENT_ISSUE_TYPES,
    otherIssues: OTHER_ISSUE_TYPES,
    correctionTypes: CORRECTION_TYPES,
    severityLevels: SEVERITY,
    followupModels: FOLLOWUP_MODELS,
    filterTabs: FILTER_TABS,
    filterMultiSelect: true,
    localStorageKey: "luna_observation_human_corrections_v1"
  };
})(typeof window !== "undefined" ? window : this);

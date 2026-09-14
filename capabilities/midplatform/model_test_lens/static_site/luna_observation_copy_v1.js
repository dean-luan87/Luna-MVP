/**
 * Luna Observation Lens — copy & labels v1 (中文默认界面).
 */
(function (global) {
  "use strict";

  global.LunaObservationCopy = {
    title: "Luna 观察镜",
    titleEn: "Luna Observation Lens",
    subtitle: "查看 Luna 如何看见、标注、判断和解释当前画面",
    statusCandidate: "候选结果",
    statusNonRuntime: "非运行态",
    emptyCanvas: "选择图片或视频，Luna 会在这里显示它看到的内容。",
    emptyInput: "选择图片或视频开始观察",
    boundaryLine: "结果仅供模型评估",
    serviceOk: "本地测试服务已连接",
    serviceOff: "本地测试服务未启动",
    serviceHint: "需要测试本地图片时，请运行 bash scripts/start_local_runner_bridge.sh",
    startObservation: "开始观察",
    selectFile: "选择文件",
    viewOriginal: "原图",
    viewCompare: "普通对比",
    viewHud: "机器人视角",
    advanced: "高级流程",
    developer: "开发者",
    importJson: "导入结果",
    rightPanelTitle: "Luna 观察面板",
    expandMore: "展开更多",
    expandProcess: "展开观察过程",
    expandEvidence: "查看证据链",
    candidateBadge: "候选",
    sections: {
      current_task: "当前任务",
      fact_observations: "事实观察",
      goal_judgment: "目标判断",
      risks_uncertainty: "风险与不确定",
      next_steps: "建议下一步",
      what_i_see: "事实观察",
      why_i_judge: "判断依据",
      uncertain: "风险与不确定",
      missing: "可能漏掉什么",
    },
    whiteboxPlaceholder:
      "白盒链路将在后续接入证据链、追踪路径、决策路径、门禁状态与测试记录引用。",
    drawerTabs: {
      metrics: "指标",
      objects: "对象",
      advanced: "高级",
      developer: "开发者",
      whitebox: "白盒",
      correction: "纠错",
      testboard: "记录"
    },
    inputSummary: {
      title: "当前输入",
      capabilityTitle: "当前能力"
    },
    exampleSam: "分割示例",
    exampleSlam: "空间定位示例"
  };
})(typeof window !== "undefined" ? window : this);

# Luna — Vision 外部 Supervision 适配实验 v0

**Phase**：`Phase-Vision-External-Supervision-Adapter-Experiment-001`  
**性质**：**独立 evaluation / experiment**；验证 [Roboflow Supervision](https://github.com/roboflow/supervision) 是否可作为 Luna Vision 的 **外部候选**（检测结果标准化、跟踪、zone/mask 等工程能力），**不**接入 Luna runtime 主线，**不**接管 Luna Core。

## 前置

- `Vision-VideoFrame-Minimal-Ingest-001` = GO（需 `video_frame_envelopes.jsonl` 等）。  
- `Vision-FrameTrace-StreamRegistry-001` 可并行或已完成；本实验 **不依赖** trace 产物，直接读 ingest 的第一条 envelope 即可。

## 目标（克制）

1. **Supervision availability probe**：是否可 `import supervision`、版本、`import_error`、浅层能力标志（`Detections`、polygon/mask 线索、tracker 模块线索）。  
2. **Synthetic detections**：**不**调用真实 YOLO；用 2–3 个合成 bbox 模拟检测输出。  
3. **Luna ROI proposal candidate**：`vision_roi_proposal_candidate_v0`（`proposal_source=supervision_synthetic_adapter`）。  
4. **Audit**：记录 `supervision_import_attempted`、禁止 YOLO/真实检测器/导航/中台写入等。  
5. **Verifier**：GO（Supervision 已安装）或 **CONDITIONAL_GO**（未安装但 probe + 合成 ROI + 缺口报告完整）。

## 严禁

- 接入 Luna runtime 主线、修改主线默认 Vision 模块。  
- 导航决策、MidPlatform fact、Scene Delta、WorldModel、AI interpretation。  
- 调用真实 YOLO（本 smoke **不 invoke**；可选读预存 YOLO JSON 留待后续 phase 明确）。  
- 将 Supervision 标为默认 Vision 模块（summary 中 `supervision_marked_as_default_vision_module` 必须为 false）。

## 与主线的关系

正确吸收路径：**独立实验分支验证 → Luna 自研链路与 Supervision 的 A/B 对比 → 只吸收可用模块 → 不让其接管 Luna Core**。  
目标在主线中的理论落位（设计叙述，非本 phase 实现）：  
`VideoFrame Envelope → Frame Trace → Input Governance → ROI Proposal Candidate → Supervision Adapter Candidate → Luna Vision Evidence Pack`；**禁止** `VideoFrame → Supervision → Luna 决策`。

## 实现与命令

见 `../evaluation/LUNA_EVALUATION_VISION_EXTERNAL_SUPERVISION_ADAPTER_EXPERIMENT_V0.md`。

## 建议下一跳

**Phase-Vision-Supervision-Structure-Reference-Analysis-001**：在 experiment GO 后做 Detections/tracker/zone → Luna 映射与 A/B 计划（不接主线），见 [LUNA_VISION_SUPERVISION_STRUCTURE_REFERENCE_ANALYSIS_V0.md](./LUNA_VISION_SUPERVISION_STRUCTURE_REFERENCE_ANALYSIS_V0.md)。

# LUNA Vision：视角主线最小运行链（V1）

## 1. 目标

在补模型之前，先回答一个执行面问题：

> **如果现在不新增视觉模型，只用现有能力/占位能力，视角主链“最小怎么跑起来”？**

本文件解决的是工程落地前必须统一的“运行链路语义”：

- 输入从哪里来、以什么形态进入
- 先做什么、后做什么、哪些可以并行
- 哪些情况中断/提权/降级（安全优先）
- 最终输出给谁、以什么结构交付

本文件仍然只做设计：**不写实现代码、不接入新模型、不做复杂调度器**。

## 2. 当前最小运行链总览（V1）

最小主链顺序（语义顺序；实现可并行）：

1. **输入进入**（`VisionInput`）
2. **环境识别初判**（输出 `EnvironmentState`）
3. **风险快扫**（输出 `RiskEvent`，可先于细节链完成）
4. **条件触发细节识别 / OCR**（输出 `DetailEvidence`；补充链，可被中断/降级）
5. **汇总决策**（输出 `SummaryDecision`）
6. **输出给上层语义 / 任务链 / 播报层**（交付 `summary_packet` + 白盒观测）

链路优先级：

- **风险链**：安全优先链，可中断补充链
- **环境初判**：快链，决定 gating 与限制变量
- **细节/OCR**：补充链，按条件触发，允许被中断/降级

## 3. 每一步的职责（输入 / 输出 / 目标 / 失败怎么办 / 是否可被打断）

> 说明：对象名与字段语义参考《`LUNA_VISION_MAINLINE_INTERFACES_V1.md`》，本节只定义“运行时顺序与处理策略”。

### Step 1) 输入进入

- **输入**：
  - 场景视觉：`scene_visual`（帧/片段/引用/摘要）
  - 任务上下文：`task_context_hint`（可空，但应允许传入）
  - 时间戳：`ts_ms`
- **输出**：`VisionInput`（概念对象，承载本轮输入与上下文）
- **目标**：统一入口、统一时间戳、统一证据引用，使后续层可审计
- **失败怎么办**：
  - 若无有效视觉输入：直接输出“输入不足”的 `SummaryDecision`（请求补充输入/重拍）
- **是否可被打断**：否（入口必经）

### Step 2) 环境识别初判（快链）

- **输入**：`EnvironmentInput`
- **输出**：`EnvironmentState`
- **目标**：
  - 给出 `environment_class` / `constraints[]` / `confidence`
  - 产出 `detail_gating`：是否触发 OCR/局部/放大拍照建议
- **失败怎么办**：
  - 若环境置信度低：输出 `constraints` 中包含 `environment_uncertain`
  - 允许汇总层走“澄清/补拍”分支，不强行给出确定环境
- **是否可被打断**：可降级（低延迟优先）；但不应被补充链打断

### Step 3) 风险快扫（安全优先链）

- **输入**：`RiskInput`（至少包含 `scene_visual` + `environment_state`）
- **输出**：`RiskEvent`（至少包含 `risk_level` / `risk_reasons[]` / `recommended_behavior`）
- **目标**：
  - 尽快给出安全结论（不依赖细节链完成）
  - 决定是否 `interrupt_supplementary_flows=true`
- **失败怎么办**：
  - 若风险判断不可用：保守降级为 `risk_level=caution` 并请求用户减速/停下/补充输入（具体策略由上层决定）
- **是否可被打断**：否（安全优先链不可被补充链打断）

### Step 4) 条件触发细节识别 / OCR（补充链）

- **输入**：`DetailInput`（包含 `environment_state` 与 `task_context_hint`，可带 `risk_hint`）
- **输出**：`DetailEvidence`（可包含 `ocr_result`、`detail_findings[]`、`need_zoom_capture`）
- **目标**：
  - 为“任务细节/环境补证”提供证据（OCR/局部）
  - 在不影响安全链的前提下补充可解释信息
- **失败怎么办**：
  - 若 OCR/局部失败：返回 `detail_limits`，不影响风险结论；汇总层可请求补拍
- **是否可被打断**：是（当风险层要求中断/降级，或延迟预算不足）

### Step 5) 汇总决策（统一汇总给大脑）

- **输入**：`SummaryInput`（环境 + 风险必填；细节可选）
- **输出**：`SummaryDecision`
- **目标**：
  - 按优先级合并：风险（覆盖）> 环境（限制变量）> 细节（补充）
  - 产出 `summary_packet` + `next_action_suggestion`
- **失败怎么办**：
  - 若汇总层不可用：至少透传 `risk_event` + 最小环境信息到上层（不丢安全）
- **是否可被打断**：不建议被打断（它是交付点）；但可在风险 danger 时走“只输出安全包”的短路分支

### Step 6) 输出去向（交付上层系统）

- **输出目标**（至少覆盖）：
  - **语义层**：用于生成解释性语言/对话策略（安全优先）
  - **任务链**：用于决定是否继续执行/导航/请求澄清/补拍
  - **播报/反馈层**：用于立即安全提醒或操作提示
  - **白盒观测**：用于调试、回放、审计
- **交付形态**：
  - 结构化 `summary_packet`（来自 `SummaryDecision`）
  - 附带关键观测字段（见第 7 节）

## 4. 中断 / 提权 / 降级规则（写死）

### 4.1 风险链何时中断其他流程

当满足任一条件时：

- `risk_level=danger` → 必须中断补充链（OCR/局部/放大拍照建议）
- `risk_level=caution` 且环境限制变量指向“风险快速变化”（车流/动态障碍/低光）→ 可中断或降级补充链

中断行为：

- `interrupt_supplementary_flows=true`
- 汇总层进入 `decision_priority=safety_first`

### 4.2 OCR 何时不触发（或降级）

不触发/降级条件：

- 风险链中断补充链
- 环境层置信度过低且 OCR 预期收益不明确（先补拍/澄清更划算）
- 输入质量不足（模糊/过暗/强反光），应优先提示用户补拍/放大

### 4.3 环境识别不稳时如何降级

当环境层 `confidence` 低：

- 不强行确定 `environment_class`
- 输出 `constraints` 包含 `environment_uncertain`
- 允许汇总层发起：
  - 请求补充输入（更清晰的图/更稳定的视角）
  - 或仅输出风险快扫 + 保守建议

### 4.4 当前“最小可用能力”是什么

在不新增模型的前提下，本链路的“最小可用”定义为：

- 风险快扫能持续产出最小 `risk_level`（哪怕保守）
- 环境层能给出基本限制变量（哪怕 `environment_uncertain`）
- 细节链可以完全不触发（在安全优先与延迟预算下允许缺失）
- 汇总层能够把风险优先交付给上层

## 5. 输出去向（写死）

视角主线的输出必须同时满足：

- **对上层可用**：`summary_packet` 可直接用于语义/任务/播报策略
- **对白盒可调**：每步是否触发、是否中断、是否降级可追溯

建议输出通道（概念）：

- `to_semantic_layer(summary_packet)`
- `to_task_chain(summary_packet)`
- `to_feedback_layer(summary_packet)`
- `to_whitebox_observation(observation_packet)`

## 6. 现阶段“使用现有能力”的边界（占位策略）

本阶段允许“占位”的节点：

- 环境识别：可先用轻量规则/启发式/现有可用能力产出 `EnvironmentState`（不新增模型）
- 风险快扫：可先用现有能力产出保守 `RiskEvent`
- OCR/细节：只在明确需要时触发；否则可为空（不影响最小可用）

本阶段暂不做：

- 新视觉模型接入
- 多模型并发/调度器
- 完整地图构建与全局场景重建

## 7. 白盒观测建议（最小集合）

最小观测点（用于回放/排障/对齐后续模型补位）：

- `environment_state_summary`：environment_class / constraints / confidence / gating
- `risk_event_summary`：risk_level / reasons_count / interrupt_supplementary_flows
- `detail_triggered`：是否触发 OCR/细节；若未触发，原因（风险中断/不需要/质量不足）
- `decision_summary`：decision_priority / next_action_suggestion / drop_supplementary_reason
- `runtime_flags`：是否发生中断/提权/降级（布尔 + reason）

## 8. 当前阶段不做项（写死）

- 不实现复杂调度器
- 不接新视觉模型
- 不做全包大模型路线
- 不做完整地图构建
- 不做复杂多模型并发

## 一句话收束

先把视角主线“最小怎么跑”写清楚，再决定后续每个模型具体补到哪一环。


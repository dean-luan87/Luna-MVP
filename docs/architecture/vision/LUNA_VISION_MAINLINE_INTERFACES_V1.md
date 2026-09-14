# LUNA Vision：视角主链接口与状态对象（V1）

## 1. 总体目标

在已完成《`LUNA_VISION_MAINLINE_LAYER_FLOW_V1.md`》四层逻辑设计的基础上，本文件将其推进到**工程接口层**：

- 定义四层之间的**最小输入输出对象**（字段语义写死）
- 定义层间**触发规则**（谁触发谁、谁能中断谁）
- 定义“覆盖 vs 补充”的**结果合并原则**
- 为每层预留统一的**白盒观测点**（便于后续调试与治理）

本文件仍然遵守：**不接入新模型、不写代码实现、不设计复杂调度器**。

## 2. 统一约定（跨层公共字段）

### 2.1 术语

- **快链**：低延迟优先的链路片段（gating / 快扫）
- **安全优先链**：风险/行为判断链路，可中断补充链
- **补充链**：OCR/局部细节/放大拍照建议等，可被中断/降级
- **覆盖（override）**：对同一语义维度给出更高优先级的结论（例如安全风险）
- **补充（supplement）**：提供证据与细节，不应改变更高优先级结论

### 2.2 公共字段（所有层输出对象都应包含）

下列字段用于保证“可审计、可汇总、可中断”：

- **时间戳**：`ts_ms`（必填）
- **来源与证据**：
  - `evidence_sources[]`（必填，至少 1 个）
  - `evidence_refs[]`（可选，指向 OCR/局部框/帧等的引用）
- **置信度**：`confidence`（必填，0~1；语义为“本层判断的自信度”，不是事实概率）
- **场景标签**：`scene_tags[]`（可选，但建议填；例如 `outdoor`, `road`, `low_light`）
- **中断语义**：
  - `interrupt_allowed`（必填，布尔；本层输出是否允许被更高优先级链路打断/忽略）
  - `interrupt_recommendation`（可选；例如 `interrupt_details=true`）
- **可降级语义**：
  - `degrade_allowed`（可选，布尔；允许“少做/不做”以换取安全或低延迟）
  - `degrade_reason`（可选）

> 备注：本文件只定义字段语义，不定义最终代码字段名与落地位置。

### 2.3 统一枚举建议（仅语义，不锁代码）

- `risk_level`: `safe | caution | danger`
- `decision_priority`: `safety_first | fast_path | supplementary`
- `evidence_source`（示例）：
  - `vision_scene`
  - `vision_detail`
  - `ocr`
  - `gps`
  - `memory`
  - `state`
  - `task_context`

## 3. 四层最小输入输出对象（只做文档定义）

本节用“对象”表达层间接口。对象内字段分为：**必填**与**可选**。

### 3.1 环境识别层（Environment Layer）

#### 输入对象：`EnvironmentInput`

- **必填字段**
  - `ts_ms`
  - `scene_visual`：场景视觉输入摘要（帧/片段引用或上游特征摘要）
  - `task_context_hint`：任务上下文提示（若有则填；可为空对象）
- **可选字段**
  - `gps_context`
  - `memory_context`
  - `state_context`
  - `ocr_hint`：已存在的 OCR 结果（仅补证；不要求一定有）

#### 输出对象：`EnvironmentState`

- **必填字段**
  - 公共字段（见 2.2）
  - `environment_class`：环境类别（最终枚举后定）
  - `activity_hypothesis`：活动假设（“大概率在做什么”）
  - `constraints[]`：环境限制变量（例如 `low_light`, `crowded`, `traffic_flow`）
  - `detail_gating`：细节链触发建议（见 4.1）
- **可选字段**
  - `location_hint`：位置线索（例如室外/道路/建筑入口）
  - `notes`：给后续层/汇总层的简短解释

#### 这一层不负责什么（写死）
- 不把 OCR 作为全局主导源
- 不输出安全结论（安全结论由风险层负责）

### 3.2 细节识别层（Detail Layer：OCR / 局部 / 放大拍照）

#### 输入对象：`DetailInput`

- **必填字段**
  - `ts_ms`
  - `scene_visual`（可为更高分辨率/局部裁剪请求）
  - `environment_state`（来自上一层）
  - `task_context_hint`
- **可选字段**
  - `risk_hint`：风险层快扫的提示（若已产生，可用于决定“是否值得做细节”）
  - `user_capture_capability`：是否允许/是否方便提示用户“放大拍照”

#### 输出对象：`DetailEvidence`

- **必填字段**
  - 公共字段（见 2.2）
  - `detail_findings[]`：细节发现（结构化条目，包含 text/label/region/confidence）
- **可选字段**
  - `ocr_result`：OCR 结果（结构化 + 置信度 + 区域引用）
  - `need_zoom_capture`：是否建议用户重新拍/放大拍
  - `detail_limits`：本次细节识别的限制（例如模糊/遮挡/反光）

#### 这一层不负责什么（写死）
- 不覆盖环境类别
- 不输出最终安全裁决（风险层优先）

### 3.3 风险/行为判断层（Risk & Behavior Layer）

#### 输入对象：`RiskInput`

- **必填字段**
  - `ts_ms`
  - `scene_visual`（风险快扫可使用更轻输入摘要）
  - `environment_state`
- **可选字段**
  - `detail_evidence`（若已产生，作为补证）
  - `state_context`（速度/模式/是否在车内等）

#### 输出对象：`RiskEvent`

- **必填字段**
  - 公共字段（见 2.2）
  - `risk_level`：`safe|caution|danger`
  - `risk_reasons[]`：可解释原因列表（每条包含 label + evidence_source + confidence）
  - `recommended_behavior`：建议行为（结构化/可解释）
  - `interrupt_supplementary_flows`：是否中断/降级补充链（写死：安全优先链可中断补充链）
- **可选字段**
  - `risk_region_refs[]`：风险相关区域/对象引用（例如动态障碍所在区域）
  - `escalation`：是否需要升级到更高安全策略（例如提示停下、请求更清晰输入）

#### 这一层不负责什么（写死）
- 不等待细节链完成才给出安全结论（可先快扫）
- 不把补充证据（OCR/局部）当成安全判断的必要前置

### 3.4 汇总决策层（Summary & Decision Layer）

#### 输入对象：`SummaryInput`

- **必填字段**
  - `ts_ms`
  - `environment_state`
  - `risk_event`（若 risk 快扫与正式风险输出分离，此处至少要有快扫版 risk）
  - `task_context_hint`
- **可选字段**
  - `detail_evidence`
  - `memory_context`
  - `state_context`

#### 输出对象：`SummaryDecision`

- **必填字段**
  - 公共字段（见 2.2）
  - `decision_priority`：`safety_first|fast_path|supplementary`
  - `summary_packet`：可交付给上层“语义/任务/输出系统”的统一汇总包（结构化）
  - `next_action_suggestion`：下一步建议（例如先安全提示/再补细节/请求补拍/澄清）
- **可选字段**
  - `drop_supplementary_reason`：若丢弃补充链结果，说明原因（例如被安全链中断）
  - `open_questions[]`：未决增量问题列表（供上层继续追问/规划）

## 4. 层间触发规则（谁触发谁 / 谁能中断谁 / 覆盖与补充）

### 4.1 环境层 → 细节层（OCR/局部）触发规则（gating）

环境层输出 `detail_gating`（语义）建议包含：

- `trigger_detail`（bool）
- `trigger_ocr`（bool）
- `trigger_local_zoom`（bool）
- `trigger_reason`（枚举/文本）
- `priority`（`fast_path|supplementary`）

建议触发条件（原则口径）：

- 任务上下文需要文字/标识细节（路牌/门牌/入口指示/店名）
- 环境类别指向“文字密集/标识关键”的场景（室内导视、停车场出口、道路指示）
- 环境置信度不足且 OCR 可能提供补证（但 OCR 不是主导源）

不触发/降级条件：

- 风险层已要求中断补充链（见 4.2）
- 当前输入质量不足且提示用户补拍更划算（`need_zoom_capture=true`）

### 4.2 风险层对补充链的中断规则（安全优先写死）

当满足任一条件时，风险层可设置：

- `interrupt_supplementary_flows=true`
- 并给出 `interrupt_reason`

建议条件（原则口径）：

- `risk_level=danger`：必须中断补充链，优先输出安全建议
- `risk_level=caution` 且环境限制变量表明风险可能快速变化（车流/动态障碍/低光）
- 快链延迟预算触顶：宁可少做细节，也要保持风险判断实时性

### 4.3 汇总层“只采信安全链”的规则

当满足任一条件时，汇总层可在 `SummaryDecision` 中声明：

- `decision_priority=safety_first`
- `drop_supplementary_reason=...`
- 并在 `summary_packet` 中只包含必要的环境 + 风险信息

建议条件：

- 风险层中断补充链
- 细节层结果置信度过低且可能误导（例如 OCR 低置信且与环境/风险冲突）

### 4.4 覆盖 vs 补充（合并规则）

写死优先级：

1. **风险/行为判断层（覆盖）**
   - 风险结论与行为建议对输出策略具有最高优先级
2. **环境识别层（覆盖/限制变量）**
   - 环境类别与限制变量可覆盖“细节层的解释方式”，但不覆盖风险结论
3. **细节识别层（补充）**
   - 细节结果默认只补充证据，不应改变更高优先级结论

冲突处理（原则）：

- 当细节证据与环境结论冲突：细节层以“候选证据”形式上报，不直接改写环境类别
- 当细节证据与风险结论冲突：以风险为准；细节可作为“需澄清/需补拍”的触发依据

## 5. 最小运行顺序（V1）

推荐最小顺序（允许并行，但以此为“语义顺序”）：

1. 视角输入进入（scene_visual + task_context_hint）
2. 环境识别（快链）
3. 风险快扫（安全优先链，尽量不依赖细节层）
4. 条件触发细节识别（OCR/局部/放大拍照建议）（补充链，可被中断）
5. 汇总决策（优先消费风险，其次环境，再合并细节补证）
6. 输出给上层语义/任务链（summary_packet）

## 6. 白盒观测点（每层最小集合）

为避免后续“补模型后难调”，每层至少保留以下观测点（字段名后续实现再定）：

### 6.1 环境层观测
- 输入摘要：来源（vision/gps/memory/state/ocr）是否存在
- 输出摘要：environment_class / constraints / confidence
- 触发：detail_gating（是否触发 OCR/局部）

### 6.2 细节层观测
- 输入摘要：来自 environment 的 gating 与关键限制变量
- 输出摘要：detail_findings_count / ocr_present / need_zoom_capture
- 触发：是否被风险链中断（interrupt 标记 + reason）

### 6.3 风险层观测
- 输入摘要：环境限制变量 + 视觉风险信号是否存在
- 输出摘要：risk_level / reasons_count / recommended_behavior
- 中断：interrupt_supplementary_flows + reason

### 6.4 汇总层观测
- 输入摘要：是否有 detail_evidence，风险等级
- 输出摘要：decision_priority / next_action_suggestion
- 覆盖/丢弃：drop_supplementary_reason（若有）

## 7. 当前阶段不做项（写死）

- 先不写代码实现
- 先不接模型
- 先不设计复杂调度器
- 先不决定最终字段名在代码中的实现方式

## 一句话收束

先把视角主链的接口、状态对象和触发规则写清楚，再进入后续“补模型”和“最小运行链”实现阶段。


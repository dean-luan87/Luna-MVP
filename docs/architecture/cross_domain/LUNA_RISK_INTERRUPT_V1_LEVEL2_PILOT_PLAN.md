# risk_interrupt_v1 Level 2 受限试点设计（V1）

## 0. 一句话结论（写死）

`risk_interrupt_v1` 当前**具备进入“受限 Level 2 试点设计”的资格**，但**不得直接进入全主线真实抢占实现**。本文件只定义“试点怎么试”，不做实现。

---

## 1. 试点范围（Scope）

### 1.1 风险等级（必须写死）

- **仅允许进入试点候选**：`risk_level in {high, critical}`
- **绝对禁止**：`low/medium/unknown`（包括“无 risk_summary 视为 low”）

### 1.2 抢占对象（只抢什么）

第一版试点只允许抢占“低价值、可回退、不会影响任务链语义”的输出：

- **仅允许抢占**：`prompt` / `confirmation` 类短文本（提示/确认）
- **绝对禁止抢占**：
  - 任务规划/任务执行相关输出（任何会影响用户对任务状态理解的文本）
  - 长文本解释类输出
  - 任何跨域旁路外显输出（旁路仍为 whitebox-only）

### 1.3 场景范围（极小化）

试点必须限制在极小场景范围内，建议以“环境开关 + 明确联调环境”双重限制：

- **仅允许**：联调/灰度环境 + 明确开启试点开关 + 观测链在线可抽链
- **绝对禁止**：默认路径/全量主线/无观测链/无回退演练

---

## 2. 试点对象（Pilot 대상）

### 2.1 试点能力边界（写死）

- **唯一试点能力**：`risk_interrupt_v1`
- **禁止联动晋升**：`sidewalk_nav_v1` / `retail_find_item_v1`（继续 whitebox-only，不进入 submit，不进入抢占）

### 2.2 试点前置（必须已满足）

试点设计默认依赖以下事实链已存在（已在评审中对账）：

- submit 闭环（`SpeechRequest` → `VoiceOutputPlane.submit`）
- request 真源（created/submitted/terminal 等事件）
- playback/speaking 真源（started/finished/failed/cancelled 事件；dry-run 不伪造）

若上述任一链路在目标环境不可用或无法对账，则试点**不得开启**。

---

## 3. 抢占哪些输出（Preempt Targets）

> 本节定义“候选可抢占范围”，不是实现细节。

### 3.1 最小可抢占集合（V1）

- `output_category in {"prompt", "confirmation"}`
- 文本长度上限（例如 ≤ 80 chars）以避免长输出误入
- 仅当 `playback_started` 已观测到（即 speaking 真源确认开始播）时，才允许进入“可抢占评审”（避免把 submit 当 speaking）

### 3.2 绝对不抢占集合（V1 写死）

- `dispatch_type="long_task_planning_input"` 相关输出（或任何等价的任务规划链路输出）
- 任何来自旁路的 `final_spoken_output`（当前旁路本就禁止外显）
- 任何缺少 request_id 闭合证据的输出链

---

## 4. 哪些绝对不能抢（Hard Prohibitions）

以下情况一律禁止抢占（即便 risk_level=critical）：

- speaking/playback 真源不可用、或与 request_id 无法对账
- 观测链断裂（request 不可闭合到 terminal，或 playback_result 缺失）
- 未定义中断/恢复边界的任务链相关输出
- 回退链不可执行（无法秒退到 Level 1 / Level 0）

---

## 5. 需要监控什么（Online Monitoring）

试点开启前必须写死在线监控最小指标，并保证可按 `request_id` 聚合：

### 5.1 链路闭合性（必须）

- request 侧：`request_created → request_submitted → request_terminal_observed`
- playback 侧：`playback_started/finished/failed/cancelled` 至少存在一个终态事件

### 5.2 误抢占（必须可观测）

试点设计必须定义“误抢占”的结构化口径与最小字段（即使实现后再补齐字段，也要先写死口径）：

- **误抢占定义**：不应抢占的输出被抢占，或抢占时机错误（未开始播/已播完仍抢占），或抢占导致用户体验/任务语义破坏
- **最小可聚合维度**：
  - risk_level / risk_type / confidence（来自 risk_summary_v1 投影）
  - 被抢占输出类别（prompt/confirmation）
  - 抢占决策原因码（需要在试点实现时落结构化字段）

### 5.3 失败/取消（必须）

- `request_submit_failed` / `request_submit_rejected`
- `playback_failed` / `playback_cancelled`
- 观测链断裂次数（缺失关键节点）

---

## 6. 什么时候立即回退（Rollback Rules）

### 6.1 秒退到 Level 1（写死）

触发条件（任一满足即回退）：

- 观测链无法闭合（request 或 playback 关键节点缺失）
- playback 真源不可用/漂移（出现“疑似 speaking=true 但无 playback_started”类矛盾）
- 误抢占率超过阈值（阈值由试点设计明确，建议从极低阈值起步）

回退动作（必须可执行）：

- 关闭 Level 2 试点开关（实现阶段必须提供独立开关）
- 保持 `risk_interrupt_v1` 继续停留 Level 1 whitebox-only（或直接关闭旁路开关）

### 6.2 秒退到 Level 0（写死）

触发条件（任一满足即回退）：

- 出现不可控循环抢占/安全事件/数据损坏风险
- 回退到 Level 1 后仍无法稳定（例如链路持续断裂或异常无法定位）

回退动作（组合，必须可执行）：

- 关闭 `risk_interrupt_v1`（`LUNA_ENABLE_RISK_INTERRUPT_V1=0`）
- 关闭 submit 新路径（`LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1=0`）
- 必要时回退编排层（`LUNA_DISABLE_CROSS_DOMAIN_ORCHESTRATOR_V1=1`，非必须但保留为紧急手段）

---

## 一句话收束

先把 `risk_interrupt_v1` 的 Level 2 受限试点“能抢什么/不能抢什么/怎么监控/怎么秒退”写死；只有在这些边界下，才允许进入下一阶段的试点实现。


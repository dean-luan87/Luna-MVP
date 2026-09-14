# risk_interrupt_v1 试点阶段状态复盘（V2）

## 目标

在 risk_interrupt_v1 已同时具备两条受限试点路径后，统一收口它们的：

- **边界与适用条件**
- **默认优先级**
- **回退关系与退出路径**
- **当前阶段明确禁止项**

本文件**只做复盘**，不改代码、不放宽边界、不引入新能力。

---

## 1. 当前试点形态总览（仅两种）

### 1.1 路径 A：preempt-before-submit（提交前替换）

来源：`LUNA_RISK_INTERRUPT_V1_LEVEL2_PILOT_IMPLEMENTED_NOTE.md`

- **本质**：在构造 `SpeechRequest` 前，仅替换本次将提交的 `text_candidate`（不做中断/取消）。
- **关键开关**：`LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT=1`

### 1.2 路径 B：cancel+replace（仅待执行 request）

来源：`LUNA_RISK_INTERRUPT_V1_CANCEL_REPLACE_IMPLEMENTED_NOTE.md`

- **本质**：在严格条件下，先对“待执行/未 started”的目标 request 执行 cancel；仅在观测到 `playback_cancelled` 终态后，才提交 replacement request。
- **关键开关**：`LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT=1`

---

## 2. 两条试点路径的边界对比（写死）

| 维度 | 路径 A：preempt-before-submit | 路径 B：cancel+replace（pending only） |
|---|---|---|
| **风险等级** | 仅 `high/critical` | 仅 `high/critical` |
| **允许输出类型** | 仅低价值 `prompt/confirmation` | 仅低价值 `prompt/confirmation` |
| **对执行层依赖** | **不依赖 cancel**；不需要 cancel 终态闭合 | **依赖 cancel 真能力**；必须观测到 `playback_cancelled` 终态闭合 |
| **是否涉及旧 request** | 不涉及旧 request；只影响本次 submit 的文本候选 | **涉及旧 request**：仅允许取消“待执行/未 started”的 request |
| **started playback** | 不适用（不做取消） | **明确禁止**取消已 started playback（本阶段写死） |
| **失败处理** | 不满足条件则完全不触发（保持主链提交） | 任一链路不闭合（例如 cancel 终态不可见）→ **回退到路径 A** |
| **可对账性** | `output_decision.reason = risk_interrupt_v1_level2_pilot_preempt_before_submit` | `output_decision.reason = risk_interrupt_v1_cancel_replace_pilot_evaluated`（含 `replacement_request_id` 等） |
| **回退开关** | 关 `LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT=0` | 关 `LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT=0`（秒退到路径 A） |

共同前置（两条都必须）：

- `LUNA_ENABLE_RISK_INTERRUPT_V1=1`
- `LUNA_RISK_INTERRUPT_WHITEBOX_ONLY=0`
- 仅在 `prompt/confirmation` 且风险为 `high/critical` 才允许进入试点判定

---

## 3. 当前推荐优先级（默认怎么走）

### 3.1 默认优先级（写死）

在试点同时开启的情况下，**推荐的优先级为：**

1. **优先尝试路径 B：cancel+replace（pending only）**  
   但必须满足：目标 request 可被判定为“待执行/未 started”，且 cancel 终态可闭合。
2. 若路径 B 任一条件不满足或链路不闭合，则**立即回退到路径 A：preempt-before-submit**。
3. 若路径 A 也不满足触发条件（例如风险不足/输出类型不符），则回到 **Level 1（仅白盒）** 的常规行为（不抢占、不取消）。

> 注：这里的“优先尝试”仅针对**试点内部**的选择，不意味着对外扩边界；并且**路径 B 的任何失败都不得降级为更激进的 started-playback 取消**，只能回退到路径 A。

### 3.2 哪些情况下只能走 preempt-before-submit（路径 A）

出现任一情况，路径 B **不得进入**，只能走路径 A（或不触发）：

- **没有可判定的待执行 request**（无法确定 target request_id）
- **已 started playback**（明确禁止取消）
- cancel 能力不可用（`LUNA_ENABLE_INTERRUPT_CANCEL_V1=0` 或执行层不可用）
- cancel 终态不可闭合（在允许的短时间窗内未观测到 `playback_cancelled`）

### 3.3 哪些情况下允许进入 cancel+replace（路径 B）

必须同时满足：

- 风险等级为 `high/critical`
- 输出类型为低价值 `prompt/confirmation`
- 存在明确的“待执行/未 started”的目标 request（queued 或 current-but-not-started）
- cancel 成功且可观测到 `playback_cancelled` 终态闭合

---

## 4. 明确禁止项（重复写死）

当前阶段一律禁止：

- **取消已 started playback**
- **非 `prompt/confirmation` 的输出**进入任一试点路径
- **`medium/low` 风险**触发抢占或取消
- **其他旁路**（`sidewalk_nav_v1` / `retail_find_item_v1` 等）进入真实输出链或进入 cancel 链
- **恢复/重播**
- **多 request 级联取消/编排**

---

## 5. 回退关系（从细到粗）

### 5.1 cancel+replace 失败 → 退回 preempt-before-submit

触发条件（任一即回退）：

- 目标 request 不存在或无法判定为 pending
- 目标 request 已 started
- cancel 失败
- cancel 终态不可观测（链路不闭合）

动作（写死）：

- 试点内退回路径 A（不更改其他系统开关）
- 或直接关闭 `LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT=0` 秒退

### 5.2 preempt-before-submit 不触发/异常 → 回到 Level 1

说明：

- 路径 A 本身是“提交前替换”，不涉及中断/取消；不满足条件就不触发。

动作（写死）：

- 关闭 `LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT=0` → 回到 Level 1（risk 仅白盒观测不影响真实提交）

### 5.3 直接回到 Level 0（紧急退出）

满足“试点观察与退出标准”中的 Level 0 条件时（例如观测链大面积断裂、不可控风险等），动作写死为：

- `LUNA_ENABLE_RISK_INTERRUPT_V1=0`
- `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1=0`

---

## 6. 为什么 started playback 仍然禁止（本阶段的硬理由）

当前禁止“取消已 started playback”不是因为缺少一个 API，而是因为**系统性前置还未齐**，放开会导致：

- **语义不稳定**：started 后的“中断成功/失败/部分播报”边界、以及用户听到的残留音频处理都未定义为系统事实。
- **恢复/重播未定义**：取消正在播报后下一条输出的恢复策略、任务状态（挂起/继续/放弃）未收口，容易把 cancel、interrupt、recover 混成一团。
- **观测与责任归因不足**：误中断的可观测与追责（谁发起、为何发起、对用户听到的影响）需要更强的工具化聚合面，而当前阶段只允许极小可控试点。

因此 started playback 的取消必须进入下一阶段的独立评审与设计，而不是在当前试点中“顺手放开”。

---

## 7. 当前阶段结论（只收口，不扩边界）

risk_interrupt_v1 当前阶段存在且仅存在两条受限试点路径：

1. **preempt-before-submit**：最小、最安全、无需 cancel 闭合；
2. **cancel+replace（pending only）**：更贴近真实中断的下一步，但必须满足“仅待执行 + cancel 终态闭合”。

默认策略为：**优先尝试 pending-only cancel+replace；失败立即回退到 preempt-before-submit；任一越界/不闭合都不得继续扩大。**


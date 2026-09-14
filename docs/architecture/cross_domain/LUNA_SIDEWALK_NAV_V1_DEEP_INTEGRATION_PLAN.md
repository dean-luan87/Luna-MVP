# sidewalk_nav_v1：主线深联调方案（V1）

## 1. 目标

`sidewalk_nav_v1` 已完成：模块实现、模块验证、主线边缘集成验证，并具备默认关闭/whitebox-only/风险压制的固定边界。  
本方案回答：当要把它从“边缘验证”推进到“主线深联调准备”时，应当 **怎么挂、挂在哪、第一阶段开什么级别**，以及如何保证默认零侵入与风险链优先。

为什么它是第二条进入更深主线联调的旁路能力：

- 它是“日常主路”的最小底盘：验证环境初判 + 风险压制 + 最小通行建议如何进入主线上下文与输出候选。
- `risk_interrupt_v1` 已完成 Level 1 深接入并收口，当前更合理的是把第二条旁路也推进到“深接入准备”，而不是冲 `risk_interrupt_v1` 的 Level 2。
- 它能复用风险链的压制语义，验证“非安全链如何在真实主线里被压下”。

---

## 2. 当前状态回顾（简要）

### 2.1 已实现什么

- 旁路模块：`capabilities/cross_domain/sidewalk_nav_v1/`
  - 主入口：`evaluate_sidewalk_nav_v1(...)`
  - 行为：规则占位环境初判；高风险或 `risk_interrupt_preempt` 时压下外显；写白盒 `metadata["sidewalk_nav_v1"]`
- 开关：
  - `LUNA_ENABLE_SIDEWALK_NAV_V1`（默认 0）
  - `LUNA_SIDEWALK_NAV_WHITEBOX_ONLY`（默认 1）

### 2.2 已验证到什么程度

- 模块验证：`tools/test_sidewalk_nav_v1.py`
- 主线边缘集成验证：`tools/test_sidewalk_nav_v1_integration.py`（模拟主链式 metadata 合并）

### 2.3 与风险链边界（已写死）

- 风险摘要 `risk_level in {high, critical}` → `output_suppressed_by_risk=true` 且不外显导航句
- 上层判定风险抢占时传 `risk_interrupt_preempt=True` → 同样压制
- 本模块不 import `risk_interrupt_v1`

---

## 3. 主线真实接入点候选（深联调要落“真实对象/上下文”）

### 3.1 人行道环境摘要最适合挂在哪个主线对象/上下文中

结合当前仓库已存在的主线 context 注入载体（`VoiceRuntimeContext`），以及风险链已采用“runtime_context 注入风险摘要”的演进方向，`sidewalk_nav_v1` 的推荐挂载形态也是：

- `VoiceRuntimeContext.metadata["sidewalk_nav_v1"] = { scene_summary, sidewalk_detected, sidewalk_confidence, ... }`

好处：

- 不污染 `VoiceInputEvent`（语音输入事件不应承载视觉环境态）
- 后续可自然扩展为“多来源汇总”（vision 环境层、GPS、任务链状态等）而不改旁路接口

候选对比（仅列结论）：

- **A（推荐）**：挂到 `VoiceRuntimeContext.metadata`（方向正确、可扩 runtime/speaking、与 risk_interrupt_v1 一致）
- B：挂到 `VoiceFinalTextDispatchResult.metadata`（可行，但更偏“输出结果白盒”，不利于作为上层可复用上下文）
- C：挂到 `VoiceInputEvent.metadata`（不推荐：污染输入事件本体）

### 3.2 最小导航建议应在哪一层进入真实输出候选

当前主线存在统一输出面接口与结构体（`SpeechRequest` / `VoiceOutputPlane`），但尚未形成完整 submit 实链；且 `sidewalk_nav_v1` V1 明确“不污染主链默认行为”。因此深联调第一阶段建议：

- **先不进入真实输出候选**（不生成/提交任何 `SpeechRequest`），仅把导航建议作为：
  - `VoiceRuntimeContext.metadata` 的上下文变量（供语义/任务/裁决层未来消费）
  - 以及 `VoiceFinalTextDispatchResult.metadata["sidewalk_nav_v1"]` 的白盒留痕（便于对账）

当后续 `SpeechRequest -> submit` 实链成型后，再评估是否允许把 `final_spoken_output` 作为候选输出进入裁决口（仍需受风险压制与去噪策略约束）。

### 3.3 白盒字段最终应落在哪一层

深联调阶段仍建议遵循已验证口径：

- **输出结果白盒**：`VoiceFinalTextDispatchResult.metadata["sidewalk_nav_v1"]`
- **运行态上下文**（供未来跨模块消费）：`VoiceRuntimeContext.metadata["sidewalk_nav_context_v1"]`（或复用同键，但建议区分“context vs whitebox”）

写死要求：

- 默认关闭时：不注入任何 `sidewalk_nav_v1` 字段（零侵入）
- whitebox-only：只留痕，不外显导航句

### 3.4 与 `risk_interrupt_v1` 的交界点（真实主线里怎么落地）

深联调时交界点应当落在“统一输出裁决口/提交层”附近的编排顺序，而不是让 `sidewalk_nav_v1` 自己 import 风险模块：

1. 上层汇总风险（`risk_interrupt_v1` / risk_summary）得到：
   - `risk_level`
   - `risk_interrupt_preempt`（是否需要抢占）
2. 调用 `evaluate_sidewalk_nav_v1(..., risk_interrupt_preempt=...)`
3. 若风险压制成立：
   - `sidewalk_nav_v1` 白盒照常写入
   - `final_spoken_output` 必为空（不进入候选输出）

---

## 4. 第一阶段建议接法（推荐：whitebox-only 深接入）

### 4.1 第一阶段先接 whitebox-only 还是允许进入真实输出候选？

**建议第一阶段只接 whitebox-only**，且只做“真实主线 context/metadata 挂载”，不进入真实输出候选。

原因：

- 当前缺少稳定的 speaking/runtime 与 submit 实链；把导航句推进候选输出会导致不可控的刷屏/冲突问题。
- V1 目标是验证“环境初判 + 风险压制”的上下文是否能被主线承接，而不是验证播报系统。

### 4.2 第一阶段最小改造范围（写死）

只允许 2 个最小改造：

1. 在主线分流/运行态上下文注入处（推荐 `VoiceRuntimeContext.metadata`）加入 `sidewalk_nav` 的输入与输出摘要
2. 在主线请求级 `metadata`（如 `VoiceFinalTextDispatchResult.metadata`）合并 `metadata["sidewalk_nav_v1"]`（沿用现有旁路产物键）

不要求接入任何视觉模型、不要求改写输出裁决器。

---

## 5. 主线对象最小改造清单

### 5.1 哪些现有对象需要加最小字段（候选）

- `VoiceRuntimeContext.metadata`：
  - `sidewalk_env_summary_v1`（输入：scene_candidate/path_confidence/is_outdoor 等）
  - `sidewalk_nav_v1`（输出：scene_type/sidewalk_confidence/navigation_hint/output_suppressed_by_risk 等，或分开 context 与白盒键）
- `VoiceFinalTextDispatchResult.metadata`：
  - `sidewalk_nav_v1`（白盒键；仅在能力开启时写入）

### 5.2 哪些现有层需要接一个最小 hook（候选）

- 语音主线分流结果生成处（与 `risk_interrupt_v1` 现有深接入 hook 同层级）
- 运行态 context 注入处（Core→Voice 的 context 建议在此处统一注入环境与风险摘要）

### 5.3 哪些地方绝对不要动（写死）

- 不改全局裁决器（不引入新的“导航输出抢占”）
- 不把 sidewalk_nav 逻辑散落到多个模块各自写 metadata
- 不在默认关闭时注入任何字段或触发任何计算

---

## 6. 与风险链的关系（写死）

### 6.1 高风险存在时如何被压下

满足任一条件即压制：

- `risk_level in {high, critical}`
- 或 `risk_interrupt_preempt=True`

压制结果（写死）：

- `output_suppressed_by_risk=true`
- `final_spoken_output=""`
- `navigation_hint` 可为空或仅留在白盒（当前实现：被压制时 `navigation_hint=""`）

### 6.2 可复用哪些风险链结果

- 复用统一风险等级语义（`low|medium|high|critical`）
- 复用“抢占标记”（由上层传入 `risk_interrupt_preempt`），避免模块间 import 耦合

### 6.3 当前阶段为什么不做复杂联动

因为当前阶段的目标是“深接入准备”：把上下文与白盒挂到真实主线对象上，验证零侵入与压制关系成立；复杂联动（去噪、排队、恢复、跨回合导航策略）属于后续阶段。

---

## 7. 验证与回退

### 7.1 深联调后如何验证（第一阶段）

必须验证：

- 默认关闭（`LUNA_ENABLE_SIDEWALK_NAV_V1=0`）→ 主线零侵入（无字段注入、无行为变化）
- 开启 + whitebox-only → 主线 metadata/context 出现 `sidewalk_nav_v1` 白盒键，`final_spoken_output` 为空
- 高风险/抢占标记存在 → `output_suppressed_by_risk=true` 且不外显
- 白盒字段完整率（关键键不缺失）

### 7.2 必须观察的最小指标

- whitebox 写入次数（按 session/request 统计）
- `output_suppressed_by_risk` 命中率（用于验证压制门槛是否正确）
- 环境命中率（`scene_type=outdoor_walkway` 占比）与抖动（后续才优化）

### 7.3 回退方式（写死）

- 先退到 whitebox-only：`LUNA_SIDEWALK_NAV_WHITEBOX_ONLY=1`
- 仍有问题 → 完全关闭：`LUNA_ENABLE_SIDEWALK_NAV_V1=0`
- 若风险链策略需要止血，优先遵循风险链的 Level 0/1 回退策略（安全优先）

---

## 8. 当前阶段不做项（写死）

- 不做复杂路径规划
- 不做 OCR 主导
- 不做地图构建
- 不做完整交叉路口决策
- 不做全局裁决器改造

---

## 一句话收束

先把 `sidewalk_nav_v1` 以 **whitebox-only** 方式挂到真实主线的 **runtime context + request metadata** 上，写死“风险压制优先”，验证零侵入与可观测；再决定是否允许其进入真实输出候选。


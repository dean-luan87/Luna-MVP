# risk_interrupt_v1：主线深联调方案（V1）

## 1. 目标

`risk_interrupt_v1` 已完成：模块实现、模块验证、主线边缘集成验证、以及 Level 0/1/2 运行策略收口。  
本方案进一步回答：**若要真正挂进主线**（不是“挂在旁边验证”），应该**挂在哪、怎么挂、第一阶段开什么级别**，以及如何保持默认零侵入与可回退。

为什么它是第一条进入更深联调的旁路能力：

- **安全优先**：它定义了所有旁路能力的优先级基准（安全可抢占）。
- **对统一输出裁决口验证意义最大**：它必须与“正在播报/可打断/任务提示”等运行态真实耦合。
- **价值最高**：即使只做 whitebox-only，也能显著提升可观测性与事后对账能力。

---

## 2. 当前状态回顾（简要）

### 2.1 已实现什么

- 旁路模块：`capabilities/cross_domain/risk_interrupt_v1.py`
  - 输入：`RiskInterruptEventV1` + `OutputStateSnapshot` + `TaskChainStateSnapshot`
  - 输出：`RiskInterruptDecision`（含 `final_spoken_output` 候选）+ 白盒 `metadata["risk_interrupt_v1"]`
- 抢占阈值（V1 写死）：`high|critical`
- 回退：`LUNA_RISK_INTERRUPT_WHITEBOX_ONLY=1` 可只白盒不抢占

### 2.2 已验证到什么程度

- 模块验证：`tools/test_risk_interrupt_v1.py`
- 主线边缘集成验证：`tools/test_risk_interrupt_v1_integration.py`（模拟 `VoiceFinalTextDispatchResult.metadata` 形态挂载）

### 2.3 运行策略已明确

见《`docs/architecture/cross_domain/LUNA_RISK_INTERRUPT_V1_RUNTIME_POLICY.md`》：

- Level 0：关闭（默认零侵入）
- Level 1：whitebox-only（推荐长期保留态）
- Level 2：真实抢占（谨慎短窗启用）

---

## 3. 主线真实接入点候选（需要“真实耦合”的地方）

> 关键结论：深联调必须落在 **统一输出裁决口** 附近，而不是随意挂在某个边缘脚本里。

### 3.1 风险事件从哪里进入主线（候选）

深联调阶段不新增模型来源，因此风险事件入口优先选“已有可产生风险摘要/风险事件”的上游链路。按可控性分两类：

- **候选 A（推荐，先白盒）**：由现有 runtime/vision/safety 管线在产生风险摘要时，构造 `RiskInterruptEventV1` 并提交给裁决层（先只记录，不抢占）。
- **候选 B（后续 Level 2 才考虑）**：由已验证可信的风险快扫链（规则/传感器/已验证模型）直接供给 `RiskInterruptEventV1`，允许抢占（需满足运行策略的“事件源可信”前置）。

本方案只要求：**事件进入点必须能提供 timestamp 与 risk_level 等最小字段**，并可在白盒中追溯来源。

### 3.2 输出裁决口的真实接入点在哪（候选）

仓库中存在“逻辑裁决口”定义文档《`LUNA_UNIFIED_OUTPUT_ARBITRATION_V1.md`》，以及统一输出面接口：

- `capabilities/voice/schemas/speech_request.py`：`SpeechRequest`（包含 `priority`、`interruptible`、`output_category` 等）
- `capabilities/voice/interfaces/voice_output_plane.py`：`VoiceOutputPlane.submit()`（统一发声出口边界）

因此深联调的推荐接入点是：

- 在**主线生成/提交 `SpeechRequest` 之前**（或提交时）插入 `risk_interrupt_v1` 的裁决：
  - 读取“当前输出状态”（是否 speaking、output_category、digest）
  - 若需抢占：修改/替换本轮即将提交的输出候选为风险播报候选
  - 若 whitebox-only：只记录决策与上下文，不改变提交内容

### 3.3 任务链挂起标记应落在哪一层（候选）

`risk_interrupt_v1` 当前最小挂起语义是：`TaskChainStateSnapshot.paused_by_risk=True`。  
深联调时建议的最小落点是：

- **候选 A（推荐）**：在“任务链运行态对象”的最外层（runtime/task-plane）增加 `paused_by_risk` 字段或等价标记，并由上层状态机决定如何处理“挂起/恢复”（V1 不实现自动恢复）。
- **候选 B（暂不建议）**：直接改任务计划/解析结果结构体（容易污染主链语义层/规划层）。

本阶段只需要实现：**能落一个可观测的 paused_by_risk 标记**，不要求自动恢复。

### 3.4 白盒字段最终应落在哪一层（写死建议）

白盒建议最终沉淀在“主线一次请求的统一 trace/metadata 载体”上：

- 若走语音主线：`VoiceFinalTextDispatchResult.metadata`（已在边缘验证脚本中模拟）
- 若走统一输出面：`SpeechRequest.metadata` / 或更上层 request trace

写死要求：

- Level 0：不注入任何 `risk_interrupt_v1` 字段（零侵入）
- Level 1/2：注入 `metadata["risk_interrupt_v1"]`（字段口径以模块输出为准）

---

## 4. 第一阶段建议接法（推荐：先 whitebox-only）

### 4.1 第一阶段开什么级别

**建议第一阶段只接 Level 1（whitebox-only）**，不直接开启 Level 2 抢占。

原因：

- 深联调会首次触碰真实输出链（例如 `SpeechRequest` 提交流程与 speaking 状态），先观测再动作更稳。
- Level 2 会引入“抢占/重复播报/任务链一致性”风险，而 V1 明确不做复杂恢复与排队系统。

### 4.2 第一阶段最小改造范围（写死）

仅做 3 个最小 hook：

1. **在输出候选形成处**构造 `OutputStateSnapshot`（speaking、output_category、digest）
2. **在风险摘要可得处**构造 `RiskInterruptEventV1`（risk_level/risk_type/direction_hint/distance_band/confidence/timestamp）
3. **在提交输出/裁决处**调用 `handle_risk_interrupt_v1(...)`：
   - Level 1：只把 `metadata["risk_interrupt_v1"]` 合并进主线 trace/metadata
   - 不改变最终播报内容、不改变任务执行

---

## 5. 主线对象最小改造清单（清单化）

> 下面是“深联调必需”的最小改造形态；不要求一次性全部实现代码，本方案只定义边界。

### 5.1 需要加字段（候选）

- **主线统一 metadata/trace 载体**：允许并入 `risk_interrupt_v1` 白盒键（Level 1/2 才写）
- **任务链运行态对象**：最小支持 `paused_by_risk`（仅当进入 Level 2 才真正修改任务态）

### 5.2 需要接最小 hook 的层（候选）

- **输出裁决/提交层**（靠近 `SpeechRequest` 的形成与提交）：深联调最关键 hook
- **风险事件汇合层**（能拿到 risk_level 的地方）：只读接入，构造事件

### 5.3 绝对不要动（写死）

- 不重写全局裁决器（V1 不做）  
- 不把 risk_interrupt 逻辑散落到多个模块各自“私自抢占”  
- 不在默认关闭（Level 0）时向主链注入任何字段或改变任何输出  

---

## 6. 验证与回退（深联调后的验收口径）

### 6.1 深联调后如何验证（第一阶段：Level 1）

必须验证：

- **默认关闭零侵入**：`LUNA_ENABLE_RISK_INTERRUPT_V1=0` 时，主链输出与 metadata 完全不受影响
- **whitebox-only 有记录**：`LUNA_ENABLE_RISK_INTERRUPT_V1=1` + `WHITEBOX_ONLY=1` 时，`metadata["risk_interrupt_v1"]` 字段完整可回放
- **字段完整率**：白盒中关键字段（event_timestamp/original_output/risk_event_summary/interrupt_reason 等）完整率接近 100%

### 6.2 进入 Level 2 前必须补齐的观测

在允许任何真实抢占前，必须先有：

- 抢占候选的误报率/漏报率抽样（通过白盒回放）
- speaking 状态、output_category 口径在主线上可稳定取到
- 回退开关可立即生效（可在秒级止血）

### 6.3 回退方式（写死）

按《`LUNA_RISK_INTERRUPT_V1_RUNTIME_POLICY.md`》执行：

- Level 2 出现异常 → 先退 Level 1：`LUNA_RISK_INTERRUPT_WHITEBOX_ONLY=1`
- Level 1 仍出现主链污染/异常 → 退 Level 0：`LUNA_ENABLE_RISK_INTERRUPT_V1=0`

---

## 7. 当前阶段不做项（写死）

- 不做复杂恢复（被打断任务提示如何排队/合并/重播）
- 不做自动重算/多轮编排
- 不做多风险事件融合与队列调度
- 不做全局裁决器重写

---

## 一句话收束

先把 `risk_interrupt_v1` 真正进入主线的**接入点、最小改造范围、第一阶段启用级别（优先 whitebox-only）与可回退路径**写清楚，再进入下一步“第一阶段主线接入实现”。 


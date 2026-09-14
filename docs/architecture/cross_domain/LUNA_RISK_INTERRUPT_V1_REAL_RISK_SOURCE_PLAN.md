# risk_interrupt_v1：真实风险摘要入口对接方案（V1）

## 1. 目标

`risk_interrupt_v1` 已完成“第一阶段主线接入”（Level 1 / whitebox-only）：在真实主线路径中把白盒并入 `VoiceFinalTextDispatchResult.metadata["risk_interrupt_v1"]`，且默认关闭零侵入、不改输出内容。

当前要解决的问题是：**风险事件来源仍是占位读取**（从 `VoiceInputEvent.metadata` 里读 `risk_level/risk_type/...`，多数情况下为 unknown）。  
本方案的目标是把风险事件来源升级为**主线中真实可得**的风险摘要入口，以继续保持 Level 1（只白盒），为未来 Level 2 的输入面打地基。

---

## 2. 当前占位入口回顾

### 2.1 当前读取方式（占位）

在 `capabilities/voice/runtime/voice_final_text_dispatcher.py` 的深接入 hook 中，当前尝试从：

- `VoiceInputEvent.metadata` 读取（占位键）：`risk_level` / `risk_type` / `direction_hint` / `distance_band` / `risk_confidence`

再构造 `RiskInterruptEventV1`，调用 `handle_risk_interrupt_v1(...)` 生成白盒。

### 2.2 为什么只能算占位

- **无稳定生产者**：当前主线没有任何地方稳定写入上述 risk_* 字段。
- **语义不闭合**：风险摘要不是语音输入事件天然携带的信息；把风险塞进 voice event 会导致耦合方向错误。
- **对未来 Level 2 无法对齐**：Level 2 需要“事件源可信”与“运行态可追溯”，占位字段无法证明来源与可靠性。

---

## 3. 主线真实风险摘要入口候选（当前仓库可得）

> 结论先行：当前仓库中“视角风险快扫”仍主要停留在接口/文档层（有 `VisionEvent` schema 与 Vision 运行链设计，但缺少 RiskEvent 的实际产出实现）。因此本方案的候选入口分为：
>
> - **可立即落地的主线入口（推荐先接）**：由 Core/Runtime 注入的会话级上下文（不污染 voice event）
> - **未来视角主链落地后的入口（保留对齐）**：从 Vision 的 RiskEvent/summary_packet 接入

### 3.1 候选入口 A：`VoiceRuntimeContext.metadata`（Core 注入）

仓库已有 `VoiceRuntimeContext`（`capabilities/voice/schemas/voice_runtime_context.py`），其 `metadata` 明确用于 Core→Voice 的上下文注入，占位字段包含 `output_busy_state` 等运行态信息。

可在不改 voice 输入事件的前提下，把风险摘要作为“本轮/最近一次风险快扫”的上下文注入，例如：

- `voice_runtime_context.metadata["risk_summary_v1"] = { ... }`

此入口的优点是：

- 风险摘要的“生产者”可以是 vision/safety/runtime（方向正确）
- 不污染 `VoiceInputEvent`（输入事件只描述语音输入本身）
- 未来可扩展：同一上下文也可承载 speaking 状态来源（与 Level 2 需要对齐）

### 3.2 候选入口 B：Vision 事件流（`VisionEvent.metadata`）

仓库已存在通用 `VisionEvent` schema（`capabilities/vision/schemas/vision_event.py`），适合承载风险快扫输出，例如：

- `VisionEvent(event_type="risk_summary_v1", metadata={risk_level,...})`

但当前缺口是：vision 主链的 RiskEvent/summary_packet 尚未落代码，因此该入口属于“对齐未来”的候选。

### 3.3 候选入口 C：统一输出裁决口的候选池（未来接入点）

《`docs/architecture/cross_domain/LUNA_UNIFIED_OUTPUT_ARBITRATION_V1.md`》定义了裁决口的输入池包含 vision/semantic/task/safety/runtime。  
从工程上讲，risk_interrupt 的最佳长期位置是裁决口附近的“候选输出池”层：那里天然能拿到风险摘要与当前输出状态。

但当前仓库仍处于 Stage-1/Stage-2 placeholder（`SpeechRequest`/`VoiceOutputPlane` 尚未形成实际 submit 链路），因此此入口同样属于“对齐未来”的候选。

---

## 4. 候选入口对比

| 候选入口 | 接入成本 | 与主线耦合度 | 稳定可用性（当前） | 适合先做 Level 1 白盒 | 是否给未来 Level 2 埋坑 |
|---------|----------|--------------|--------------------|------------------------|--------------------------|
| A) `VoiceRuntimeContext.metadata["risk_summary_v1"]` | 低~中（需要主线在 dispatcher 调用链上引入 context 参数） | 中（runtime 注入点） | **高**（schema 已存在） | **是（推荐）** | 低（方向正确，便于扩 speaking/runtime） |
| B) `VisionEvent(event_type=\"risk_summary_v1\")` | 中~高（需 vision 风险快扫落地/事件管线） | 低（跨域事件流） | 低（当前缺产出实现） | 否（先对齐字段即可） | 低（长期正确） |
| C) 裁决口候选池（output arbitration） | 高（需裁决器/submit 实链） | 高（核心输出链） | 低（当前无实链） | 否（不应抢跑） | 中（若现在硬接，容易把逻辑写散） |

---

## 5. 推荐入口（V1 先接哪一个）

### 推荐：候选入口 A —— `VoiceRuntimeContext.metadata["risk_summary_v1"]`

理由：

- 当前仓库已经存在标准的“runtime context 注入载体”，且语义方向正确（风险来自环境/安全，不应寄生于 voice event）。
- 可在继续保持 Level 1 / whitebox-only 的前提下，把风险摘要来源“从占位升级为真实注入”，不触碰抢占。
- 与未来 Level 2 的前置条件一致：同一 context 也可承载 speaking/output_busy_state 的真实来源。

为什么不先选其他入口：

- VisionEvent：当前缺少风险快扫的代码产出，先对齐字段命名即可，暂不适合作为“真实来源”。  
- 裁决口候选池：当前 `SpeechRequest -> submit` 实链未成型，硬接会扩大改造面并容易把逻辑写散。

---

## 6. 最小接入方式（仍只 whitebox-only）

### 6.1 风险摘要结构（建议写死为 v1）

建议定义一个最小结构（先在文档中写死口径，代码实现阶段按此透传）：

```json
{
  "risk_level": "low|medium|high|critical",
  "risk_type": "string",
  "direction_hint": "left|right|front|back|unknown",
  "distance_band": "near|medium|far|unknown",
  "confidence": 0.0,
  "timestamp_ms": 0,
  "source": "vision_risk_scan_v1|runtime_rule|sensor|unknown",
  "notes": "optional"
}
```

### 6.2 接入点形态（建议）

- 在 `dispatch_voice_final_text(...)` 的调用链上（例如 session manager / dispatcher 上层），新增可选参数 `runtime_context: VoiceRuntimeContext | None`
- 深接入 hook 优先从 `runtime_context.metadata["risk_summary_v1"]` 读取风险摘要；若不存在再回退到当前 `event.metadata` 占位读取（保持兼容，便于渐进迁移）

### 6.3 本阶段写死的行为约束

- 仍然只在 **Level 1 / whitebox-only** 时写白盒：`interrupt_applied=false`、`task_paused=false`
- 不改变任何输出文本/dispatch_type/notes
- 不改变任何任务链状态
- 不引入多来源融合（只接一个来源，必要时仅记录 source）

---

## 7. 当前阶段不做项（写死）

- 不做 Level 2 抢占
- 不做 speaking runtime 接入（只定义未来可放进 context 的口径）
- 不做任务挂起真实生效
- 不做多来源融合与事件编排
- 不强行把风险摘要塞回 `VoiceInputEvent.metadata`（避免污染语音输入对象）

---

## 一句话收束

先把 risk_interrupt_v1 的风险事件来源从 `event.metadata` 的占位读取，升级为 **`VoiceRuntimeContext.metadata["risk_summary_v1"]` 的真实注入入口**，继续保持 Level 1 / whitebox-only 的主线可观测与零侵入，再决定是否具备进入 Level 2 的前提。


# risk_interrupt_v1：主线深联调（阶段 1 / Level 1）实现说明

## 本阶段目标

把 `risk_interrupt_v1` 以 **Level 1 / whitebox-only** 方式真正挂进**真实主线分流路径**，只验证：

- 主线 `metadata` 能留痕（`risk_interrupt_v1` 白盒可对账）
- 默认关闭时零侵入
- 不改变主线输出内容/任务链状态/ speaking 行为

本阶段**不**做真实抢占（Level 2）、不做任务挂起、不做输出中断。

---

## 先做定位（真实落点）

### 1) `SpeechRequest` 的生成点

当前仓库中已定义统一输出面结构体 `SpeechRequest`（`capabilities/voice/schemas/speech_request.py`）与接口 `VoiceOutputPlane.submit()`（`capabilities/voice/interfaces/voice_output_plane.py`），但在当前主线实现中尚未形成“从 dispatcher 到 SpeechRequest 的实际生成链路”。因此本阶段选择 **先在真实已在役主线对象上落白盒**。

### 2) `VoiceOutputPlane.submit()` 的真实调用链

当前代码中 `VoiceOutputPlane` 仍为 Stage-1 placeholder（接口边界已固化），但主线尚未出现明确的 `submit()` 调用点。因此本阶段不在 `submit()` 上做 hook，避免引入不存在的耦合点。

### 3) “是否 speaking”的最小可观测来源

在 `capabilities/voice/runtime/voice_final_text_dispatcher.py` 所在的 Stage-1 分流链路中不接执行层（不播放、不连 speech_gate/audio_worker），因此主线没有可直接读取的“当前是否正在播报”运行态。本阶段采用 **可观测替代**：将 `speaking=false` 写入白盒 `original_output.speaking`，仅用于对账，不驱动任何行为。

### 4) `VoiceFinalTextDispatchResult.metadata` 的落点

本阶段选择把 `risk_interrupt_v1` 的白盒字段并入 **真实主线分流结果载体**：

- `VoiceFinalTextDispatchResult.metadata`

该载体会贯穿短链/长链/reject 三种路径，且已在边缘集成验证中被用作标准挂载形态。

---

## 实现了什么

- 在 `capabilities/voice/runtime/voice_final_text_dispatcher.py` 增加单点 hook：`_maybe_attach_risk_interrupt_v1_whitebox(...)`
  - 仅当 `LUNA_ENABLE_RISK_INTERRUPT_V1=1` 且 `LUNA_RISK_INTERRUPT_WHITEBOX_ONLY=1` 时，把 `handle_risk_interrupt_v1(...)` 生成的 `metadata["risk_interrupt_v1"]` 合并进 `VoiceFinalTextDispatchResult.metadata`
  - **不**改变 `dispatch_type` / `notes` / 任何输出文本，不改任务链
  - 深联调阶段 1 **写死拒绝** Level 2：即使 `LUNA_RISK_INTERRUPT_WHITEBOX_ONLY=0` 也不会启用抢占

---

## 怎么验证

```bash
python3 tools/test_risk_interrupt_v1_deep_integration.py
```

覆盖：

- 默认关闭 → 不出现 `metadata["risk_interrupt_v1"]`
- 开启 + whitebox-only → `metadata["risk_interrupt_v1"]` 字段完整、且 `interrupt_applied=false`/`task_paused=false`
- `dispatch_type/notes` 不被改写

---

## 与后续 Level 2 的关系

- 本阶段只解决“真实主线路径可接、可观测、零侵入”。  
- Level 2 的抢占/挂起/恢复，需要先补齐 speaking 真实运行态来源、输出裁决口的真实接入点、以及去重/恢复策略（按运行策略文档约束推进）。


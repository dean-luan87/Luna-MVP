# 最小真实联调路径（V1）— 语音主线 × Cross-Domain 旁路

## 1. 目标

### 为什么现在需要一份“最小真实联调路径”

当前仓库里已经同时具备：

- 语音输入主线（`VoiceInputEvent` → 分流）
- `VoiceRuntimeContext` 的注入入口（主线可携带 context 摘要）
- `voice_final_text_dispatcher`（短链/长链/reject 主分流）
- `cross_domain_orchestrator_v1`（三旁路统一编排入口 + 统一观察摘要）
- 三条旁路 Level 1 / whitebox-only 深接入（写入 metadata 白盒）
- `risk_interrupt_v1` 的 Level 2 准入门槛（**只定义门槛，不实现 Level 2**）

但这些事实分散在多份实现与文档中，容易造成“看起来都接了，但其实不知道真实主线到底联到了哪里”的错觉。本文件的作用是给出一张**现实地图**：**当前系统里已经真实联上的部分**到底到哪一层、以什么形态联上、边界在哪里。

### 这份文档解决什么问题

- 把“当前已经真实联上的链路”收敛为一条可复述、可对账的最小路径（按真实代码顺序）。
- 明确三条旁路在主线中的**参与点**与**输出落点**（只入白盒，不改输出）。
- 把“未联上”的缺口（submit 实链、speaking/runtime 真源、Level 2 等）一次写清，避免误推进。

---

## 2. 当前真实主线入口

### 2.1 语音输入从哪条主线进入

当前最小可运行入口是会话协调器：

- `capabilities/voice/runtime/voice_input_session_manager.py`
  - `VoiceInputSessionManager.process_final_text_with_dispatch(...)`

该入口假设“上游已判定句结束（静默≥3s）”，在 Stage-1 中不接音频执行层，只负责：

1) 路由与窗口治理：`route_voice_text(...)`（唤醒词/窗口内/任务态白名单）  
2) 组装统一事件对象：`VoiceInputEvent`  
3) 进入主分流：`dispatch_voice_final_text(...)`

### 2.2 当前哪个模块是主分流入口

主分流入口是：

- `capabilities/voice/runtime/voice_final_text_dispatcher.py`
  - `dispatch_voice_final_text(event, ..., runtime_context=...)`

它把 `VoiceInputEvent` 分成三类结果：

- `short_controlled_input`：经 `voice_input_to_bridge_decision(...)` 产出 `BridgeDecision`（占位 Core，不接执行层）
- `long_task_planning_input`：经 `run_long_input_task_planning_v1(...)` 产出 `VoiceLongInputParseResult`（不接执行层）
- `rejected_input`：结构化 reject

### 2.3 当前 runtime_context 如何参与

`VoiceRuntimeContext` 由上层（Core 或测试/联调脚本）传入：

- `VoiceInputSessionManager.process_final_text_with_dispatch(..., runtime_context=ctx)`
  - 透传到 `dispatch_voice_final_text(..., runtime_context=ctx)`
  - 再透传到 `_run_cross_domain_orchestrator_v1(..., runtime_context=ctx)`

当前 `VoiceRuntimeContext.metadata` 是三条旁路的**统一输入摘要承接面**（事实注入层），遵循：

- `docs/architecture/cross_domain/LUNA_CROSS_DOMAIN_CONTEXT_METADATA_CONVENTION_V1.md`

---

## 3. 当前真实联调链路顺序（按真实代码路径）

以下顺序是“当前已经真实联上”的最小路径（V1 事实链路），不代表未来完整形态。

### 3.1 输入进入与事件组装

- 上游句结束触发（静默≥3s，Stage-1 由上游负责触发）  
- `VoiceInputSessionManager.process_final_text_with_dispatch(...)`
  - `process_final_text(...)` 内部完成：
    - 会话窗口判断与更新（30s window）
    - 三入口路由：`capabilities/voice/bridge/voice_input_router.py::route_voice_text`
    - 组装 `VoiceInputEvent`（含 `context_resume_hint`、window 状态、白名单命中等）

### 3.2 主分流（dispatcher）

- `dispatch_voice_final_text(event, ..., runtime_context=ctx)`
  - 依据输入长度/确认态/白名单等做 short/long/reject 分流
  - **无论 short/long/reject，分支末尾都会进入 orchestrator**

### 3.3 统一编排入口（orchestrator V1）

- `voice_final_text_dispatcher.py::_run_cross_domain_orchestrator_v1(out, event=event, runtime_context=ctx)`
  - 顺序固定（写死）：`risk_interrupt_v1` → `sidewalk_nav_v1` → `retail_find_item_v1`
  - 通过开关与 whitebox-only 约束决定是否挂载每条旁路白盒
  - 运行后追加 `metadata["cross_domain_orchestrator_v1"]` 统一观察摘要（全关时不写）

### 3.4 三条旁路（Level 1 / whitebox-only）与 metadata 合并

三条旁路均在同一文件中以 hook 形式挂载：

- `voice_final_text_dispatcher.py::_maybe_attach_risk_interrupt_v1_whitebox(...)`
  - 输入：优先 `runtime_context.metadata["risk_summary_v1"]`，缺失回退 `event.metadata`
  - 输出：`VoiceFinalTextDispatchResult.metadata["risk_interrupt_v1"]`
  - 边界：写死只允许 whitebox-only；不抢占、不挂起、不改输出

- `voice_final_text_dispatcher.py::_maybe_attach_sidewalk_nav_v1_whitebox(...)`
  - 输入：`runtime_context.metadata["sidewalk_env_summary_v1"]` + `risk_summary_v1`
  - 输出：`VoiceFinalTextDispatchResult.metadata["sidewalk_nav_v1"]`
  - 边界：写死不外显（`final_spoken_output=""`、`whitebox_only=true`）；高风险信号压制时标记 `output_suppressed_by_risk=true`

- `voice_final_text_dispatcher.py::_maybe_attach_retail_find_item_v1_whitebox(...)`
  - 输入：`runtime_context.metadata["retail_env_summary_v1"]` + `find_item_intent_summary_v1` + `risk_summary_v1`
  - 输出：`VoiceFinalTextDispatchResult.metadata["retail_find_item_v1"]`
  - 边界：写死不外显（`final_spoken_output=""`、`whitebox_only=true`）；高风险信号压制时标记 `output_suppressed_by_risk=true`

### 3.5 输出结果保持现状（不接执行层）

最终输出仍然是 `VoiceFinalTextDispatchResult`（单出口），其：

- `dispatch_type / notes / bridge_decision / long_input_parse_result / rejection_result`  
  **由原主链逻辑决定**（旁路不改写）
- `metadata`  
  **附带**三旁路白盒 key（按开关）与 orchestrator 摘要 key（按“至少启用一条旁路”条件）

---

## 4. 当前已真实联上的能力（事实）

### 4.1 `risk_interrupt_v1`

- **真实参与点**：`voice_final_text_dispatcher` 分流结果生成后、统一编排入口内的第一条旁路 hook
- **当前输出落点**：`VoiceFinalTextDispatchResult.metadata["risk_interrupt_v1"]`
- **当前没真的接上什么**：
  - 没接 `SpeechRequest` 构造与 `VoiceOutputPlane.submit()` 实链
  - 没有可信 speaking/runtime 真源（仅白盒占位/替代观测）
  - 没有 Level 2 抢占、任务挂起/恢复

### 4.2 `sidewalk_nav_v1`

- **真实参与点**：同上（orchestrator 内第二条旁路 hook）
- **当前输出落点**：`VoiceFinalTextDispatchResult.metadata["sidewalk_nav_v1"]`
- **当前没真的接上什么**：
  - 不进入真实输出候选（写死 `final_spoken_output=""`）
  - 环境摘要仍是上游注入摘要位（或缺省占位），未绑定真实视觉/环境 runtime 主链

### 4.3 `retail_find_item_v1`

- **真实参与点**：同上（orchestrator 内第三条旁路 hook）
- **当前输出落点**：`VoiceFinalTextDispatchResult.metadata["retail_find_item_v1"]`
- **当前没真的接上什么**：
  - 不进入真实输出候选（写死 `final_spoken_output=""`）
  - OCR 仅为接口位/触发决策，不执行真实 OCR 任务链

---

## 5. 当前真实输出边界（写死事实）

- 三条旁路当前都**不进入真实输出候选**，不提交 `SpeechRequest`，不触发 `VoiceOutputPlane.submit()`。
- 当前真实输出内容仍由 `dispatch_voice_final_text` 的原分流产物决定（short/long/reject）。
- 三条旁路仅以 **metadata/白盒** 的形式参与真实主线：  
  - 输入来自 `VoiceRuntimeContext.metadata`（上游摘要/事实）  
  - 输出落到 `VoiceFinalTextDispatchResult.metadata`（本轮白盒留痕）

---

## 6. 当前真实未联上的部分（缺口清单）

以下是“当前主线仍未真实接上”的明确缺口（与 Level 2 准入门槛口径一致）：

- **submit 实链未接**：`SpeechRequest` 与 `VoiceOutputPlane.submit()` 仍为 Stage-1 placeholder（接口存在，主线无真实调用链）
- **speaking/runtime 未接**：主线分流链路不接执行层，缺少可信 speaking 真源
- **Level 2 未接**：`risk_interrupt_v1` 无真实抢占、无真实输出改写
- **任务链真实挂起/恢复未接**：仅白盒打标，不驱动 task chain
- **复杂 output arbitration 未接**：未形成“多候选 + 优先级 + 去重 + cooldown + 中断/恢复”的真实裁决器

---

## 7. 当前真实联调结果的价值

这条最小真实联调路径已经证明：

- **主线承接面成立**：`VoiceRuntimeContext.metadata` → 旁路读取 → `VoiceFinalTextDispatchResult.metadata` 留痕的“输入/输出白盒回路”成立。
- **编排层工程形态成立**：三旁路统一入口、固定顺序、回退开关、统一观察摘要成立。
- **零侵入可控**：默认关闭不写入旁路 key；开启也不改变 `dispatch_type/notes` 与用户可见结果。

它为下一阶段（路线 A：补真实输出链）打下的底包括：

- 一条可扩展的单点生长处（orchestrator）
- 一套可评审的准入门槛（`risk_interrupt_v1` Level 2 admission gate）
- 一份可对账的观察面（旁路白盒 + orchestrator 摘要）

---

## 8. 当前阶段不做项（写死）

- 不做未来设计展开
- 不做全局联调重构
- 不做 Level 2（真实抢占/挂起/恢复）
- 不做 speaking/runtime 接管
- 不做 submit 实链改造

---

## 一句话收束

先把当前“已经真实联上”的主线链路写清楚，再决定下一阶段是补真实输出链（submit + speaking/runtime + Level 2 准备），还是继续扩能力面。


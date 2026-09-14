# Luna Voice V1 — 单一闭环入口与最小路径（代码事实）

**文件**：`docs/architecture/voice/LUNA_VOICE_V1_MINIMAL_FLOW.md`  
**性质**：实现锚点说明（**不是**产品文案）  
**关联**：`docs/architecture/voice/LUNA_VOICE_V1_PLAN.md`

**端到端验证（当前仅覆盖 session_wake / reject）**：`tools/verify_voice_v1_minimal_flow.py`（需 `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1=1`，脚本内会设）。

---

## 工程宪法（必须钉死）

**Voice V1 只负责交互闭环，不负责发明事实。**

- Voice 可以：承载输入/输出、管理会话与时间治理状态、做格式化与**保守降级**。
- Voice 不得：擅自补充事实、编造世界状态、伪造系统能力，或在证据不足时输出“确定事实陈述”。

（与 `LUNA_VOICE_V1_PLAN.md` 中的 **No Fabrication Rule** 一致；本条强调**工程责任边界**。）

---

## 1. V1 单一闭环入口（当前最适合的真实调用链）

### 1.1 推荐单入口（对外）

- **类**：`capabilities/voice/runtime/voice_input_session_manager.py` → `VoiceInputSessionManager`
- **方法**：`process_final_text_with_dispatch(...)`
  - 内部顺序：`process_final_text(...)` → `dispatch_voice_final_text(...)`（见同文件）

这是当前仓库里**唯一**把「切段完成后的文本」一次性送进主分流并返回 `VoiceFinalTextDispatchResult` 的**稳定聚合入口**。

### 1.2 主分流

- **函数**：`capabilities/voice/runtime/voice_final_text_dispatcher.py` → `dispatch_voice_final_text(...)`

---

## 2. 「受控回复生成点」在哪里？（事实）

当前仓库**不存在**一个独立、通用的 `ReplyBuilder` / `LLMResponder` 单点。

**最小、且已落地的“可说出文本”拼装点**在：

- `voice_final_text_dispatcher.py` → **`_maybe_submit_real_output_v1(...)`**

该函数在 **`LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1` 开启**时，构造 `SpeechRequest.text_candidate`，并调用：

- `get_voice_output_plane_v1().submit(req)`

当前实现里，`text_candidate` **仅覆盖**两类极小场景（见函数内注释与分支）：

1. `rejected_input`：用 `rejection_result.reason` 作为短提示文本  
2. `short_controlled_input` 且 `bridge_decision.route == session_wake`：固定提示 **`我在。`**

> 因此：**V1 最小闭环**若要“说出去”，现阶段应优先以这两类路径为验收对象；其它分流（尤其 `long_task_planning_input`）当前**不经过**该 submit  helper 的 speak 文本拼装（见下节“占位/缺口”）。

---

## 3. 进入 `VoiceOutputPlaneV1.submit` 的最短路径（事实）

满足以下**全部**条件时，才会发生 `submit`：

1. 环境变量：`LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1=1`（truthy）  
2. `dispatch_voice_final_text` 返回的 `VoiceFinalTextDispatchResult` 命中 `_maybe_submit_real_output_v1` 支持的文本来源（见上节）  
3. `text_candidate` 非空且长度被截断到 ≤ 80（函数内硬限制）

调用链：

`VoiceInputSessionManager.process_final_text_with_dispatch`  
→ `dispatch_voice_final_text`  
→ `_run_cross_domain_orchestrator_v1`（观测/摘要，不改变“是否 submit”的最低条件）  
→ **`_maybe_submit_real_output_v1`**  
→ `get_voice_output_plane_v1().submit(SpeechRequest)`

---

## 4. 哪些环节已真实存在 vs 仍属占位/缺口

### 4.1 已真实存在（可观测、可调用）

- 输入协调与时间治理：`VoiceInputSessionManager` + `VoiceTimeGovernanceRuntime`
- 分流：`dispatch_voice_final_text`
- 输出平面锚点：`VoiceOutputPlaneV1.submit`（默认 dry-run；可切执行）
- Trace：`LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL` 等 JSONL envelope（由输出平面与观测链写入）

### 4.2 仍是占位 / 与“最小闭环说出去”未接线

- **通用回复生成**：除 `_maybe_submit_real_output_v1` 的极小分支外，没有统一的“把 dispatch 结果翻译成用户可播报文本”的单点  
- **长链**：`long_task_planning_input` 路径主要产出 `long_input_parse_result`；**当前不自动**把该结果转为 `SpeechRequest.text_candidate` 并 submit（除非未来单独接线）

---

## 5. No Fabrication Rule 在闭环中的最小落点（建议）

### 5.1 放在哪一层？

**优先落点：输出前闸门（推荐）** —— 在 **`SpeechRequest` 构造之后、`plane.submit` 之前**，或在 **`text_candidate` 最终确定之后、进入 `SpeechRequest` 之前**。

原因：

- 这是对用户“可感知输出”的**唯一统一收口**（与“是否聪明”无关，先规则化）。
- 不依赖上游是否 LLM；即使 `text_candidate` 来自 reject reason，也可做保守裁剪/标记（防止把内部 reason 直接当作对外事实陈述）。

### 5.2 为什么不先放在“模型生成前”？

模型生成前拦截属于**下一阶段**（需要统一回复生成点）。V1 当前**尚未**有统一生成点，先把闸门放在 **`_maybe_submit_real_output_v1` 的 submit 前**成本最低、边界最清晰。

### 5.3 与“Voice 不发明事实”如何对齐？

该闸门只做**保守策略**：缺证据 → 降级为「不知道/不能确定/请补充」模板；**不允许**为了体验补全未提供的事实细节。

---

## 6. 下一轮最小实现建议（只允许 1～2 个点）

1. **~~新增一个极小函数~~（已落地）**：`guard_v1_speakable_text(...)` 已在 `voice_final_text_dispatcher.py` 中实现，并由 `_maybe_submit_real_output_v1` 在构造 `SpeechRequest` 之前调用（规则版 No Fabrication Rule）。  
2. **（可选，下一轮）** 在扩展更多 `short_controlled_input` 播报路径前，保持闸门为唯一对外播报文本收口，避免扩面误接入“补全事实”。

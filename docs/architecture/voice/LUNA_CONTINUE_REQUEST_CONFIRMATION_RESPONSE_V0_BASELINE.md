# Continue Request Confirmation Response v0 — Baseline / Freeze（冻结）

**文件**：`docs/architecture/voice/LUNA_CONTINUE_REQUEST_CONFIRMATION_RESPONSE_V0_BASELINE.md`  
**性质**：Topic 04 下已落地的**最小响应模板**冻结面（不是 `resume` 行为、不是 gate 裁决变更）。  

上位约束（必须服从）：  
- `docs/architecture/voice/LUNA_CONFLICT_TOPIC_04_CONTINUE_REQUEST_HANDLING_V0.md`  
- `docs/architecture/voice/LUNA_INFORMATION_CONFIRMATION_GATE_V0_BASELINE.md`  
- `docs/architecture/voice/LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md`  
- `docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md`  
- `docs/architecture/voice/LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`  

---

## 1. 触发条件（写死）

当且仅当同时满足：

1. `result.metadata["information_confirmation_gate_v0"]` 存在  
2. `gate_passed == false`  
3. `requires_confirmation == true`（Information Confirmation Gate v0 已命中、拦截 submit）  
4. 当前用户文本（`wake_word_stripped | normalized_text | effective_raw_text`）经**最小子串匹配**命中继续用语之一：`继续`、`按我说的做`、`别停`  
5. Resource Gate 仍允许本轮出声（`allow_submit == true`）；若资源 gate 已拦截，本路径**不**额外播报（避免在资源不足时误加响应型输出）  

**不触发**：无 Information Gate 拦截、无上述继续用语、或仅 Resource Gate 场景（本 baseline 不覆盖）。

---

## 2. 唯一固定模板（写死）

全文唯一一句（与代码常量一致）：

```text
我现在还不能继续，因为关键信息还不明确。请先告诉我你指的是哪一个对象。
```

- 不脑补对象、不假装已理解指代、不承诺确认后一定执行。  
- 播报前经 `guard_v1_speakable_text(..., profile="continue_request_info_confirm")` **白名单**放行（仅允许与上述字符串完全一致）。

---

## 3. 工程边界：两类 submit（必须区分，避免误读为“绕过 gate”）

| 类型 | 含义 | 本 baseline |
|------|------|-------------|
| **执行型 submit** | 主链在 gate 放行后，通过 `_maybe_submit_real_output_v1` 等对**主链任务/会话/拒绝路径**的播报推进 | **本路径不替代**；Information Gate 拦截时 `allow_submit2 == false`，**原执行型路径仍不调用** |
| **响应型 submit** | 在 **gate 仍拦截执行型 submit** 的前提下，仅对**澄清/确认/说明**类固定句走**独立** `VoiceOutputPlane.submit`，用于交互闭环，**不表示任务继续、不表示 resume** | **本实现属于此类** |

**写死**：若见到“gate 拦了但仍 submit”，应理解为 **响应型 submit 例外路径**，不是对 Information Gate 裁决的放行，也不是任务执行恢复。

观测：`result.metadata["continue_request_response_v0"]`（`response_triggered`、`trigger_reason`、`response_type`）。

---

## 4. 代码与验证入口（改到须重跑）

| 项 | 路径 |
|----|------|
| 模板与触发判断 | `capabilities/voice/runtime/voice_continue_request_response_v0.py` |
| 响应型 submit、guard profile、`continue_request_response_v0` | `capabilities/voice/runtime/voice_final_text_dispatcher.py` |
| 本专题回归 | `tools/verify_continue_request_response_v0.py` |
| 主线与 Information Gate 回归 | `tools/verify_voice_v1_minimal_flow.py`、`tools/verify_voice_confirmation_gate_v0.py` |

改到触发条件、模板、guard 白名单、或 dispatcher 中该分支落点时，**至少**重跑上表脚本。

---

## 5. 当前明确不做的事

- 不扩展更多继续用语策略、不实现协商器  
- 不实现 `resume` / `repeat` 行为执行  
- 不修改 Information Gate / Resource Gate 的裁决逻辑  
- 不接白盒 / provenance / 视觉解释  

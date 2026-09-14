# Luna 语音时间治理 v1

## 1. 为什么 30 秒窗口与 90 秒长语音不能共用一套计时器

若用「最后活动时间」或单一 `last_activity` 同时表达：

- 「本句何时因静默结束」（约 3 秒）
- 「免唤醒会话还能保持多久」（30 秒）
- 「单次收音最长多久」（90 秒）

则会在**长语音仍进行中**时，把 30 秒会话到期误当成「可以打断当前输入」的条件，从而出现 **90 秒长语音被 30 秒会话窗口误杀** 的冲突。

因此 v1 要求：**三套机制在代码层分离**，各自计时、各自裁决，互不替代。

## 2. 三套时间机制分别负责什么

| 机制 | 实现位置 | 职责 |
|------|-----------|------|
| **SilenceEndTimer** | `VoiceSegmentTimeoutPolicy` + `SilenceEndTimer` 包装 | 用户静默 ≥ **3s** → 当前**这一段输入**结束 |
| **SessionWindowTimer** | `VoiceWakeWindowManager`（30s）+ `suspend_session_clock` | **免唤醒会话窗口**；仅在**非 capturing_input** 时裁决到期 |
| **InputCaptureTimer** | `InputCaptureTimer` | 单次输入最长 **90s**；**80s** 可发提示（占位即可） |

## 3. 四态状态机（`VoiceRuntimePhase`）

| 状态 | 含义 |
|------|------|
| `idle` | 无会话、无输入进行中，需要唤醒词 |
| `session_open` | 会话窗口已打开、当前无人说话，30s 窗口运行中 |
| `capturing_input` | 正在接收一段输入；3s 静默与 90s 上限在此态生效；**30s 会话时钟挂起** |
| `processing_after_input` | 本段已收口、即将/正在走路由与下游处理；随后回到 `session_open` |

实现：`capabilities/voice/runtime/voice_time_governance_v1.py` 中 `VoiceTimeGovernanceRuntime`。

## 4. 为什么输入结束后 30 秒窗口要「全量重置」

一段输入结束后，无论此前窗口还剩多少秒，统一从**收口时刻**起重新给 **满 30 秒**，避免「说完一大段后想再补一句」却因剩余时间过短而体验苛刻。

实现：`VoiceWakeWindowManager.reset_full_window_after_input(now)`。

## 5. 为什么 90 秒强切后允许续接

强切只表示**本段收音**已达上限，不代表用户意图结束会话。收口后仍给**新的 30 秒会话窗口**，并在 `VoiceInputEvent` 上标记：

- `is_forced_cutoff = true`
- `cutoff_reason = "max_capture_duration"`
- `continuation_allowed = true`

便于下游在「免唤醒」语义下承接上下文继续说（不要求再次唤醒）。

## 6. 当前不做什么（本轮边界）

- 不长语音模型接入、情感引擎、主链输出改造
- 80 秒提示音可仅保留占位（`tick_capturing` 返回 `warn_capture_80`）
- ASR 层需在开始/结束收音时调用 `VoiceInputSessionManager.on_capture_started` 与 `process_final_text`（见 `VoiceTimeGovernanceRuntime.tick_capturing`）

## 7. 集成要点

- **开始采集**：`VoiceInputSessionManager.on_capture_started(now)`
- **采集过程**：`VoiceTimeGovernanceRuntime.tick_capturing(now, silence_duration_sec=..., capture_duration_sec=...)`
- **一句结束**：`process_final_text(...)`；若因 90s 强切，传入 `is_forced_cutoff=True`, `cutoff_reason="max_capture_duration"`

## 8. Changeset（本轮）

### 改动对象

- `voice_wake_window_manager.py`：`session_clock_suspended`、`suspend_session_clock` / `resume_session_clock`、`reset_full_window_after_input`
- `voice_time_governance_v1.py`（新）：`VoiceRuntimePhase`、`VoiceTimeGovernanceRuntime`、`SilenceEndTimer`、`InputCaptureTimer`、`GovernanceTickResult`
- `voice_input_session_manager.py`：内置 `VoiceTimeGovernanceRuntime`；`on_capture_started`；`process_final_text` 前后 `on_before` / `on_after`；路由用 `is_window_active_for_routing`
- `voice_input_event.py`：`is_forced_cutoff`、`cutoff_reason`、`continuation_allowed`、`voice_runtime_phase`

### 测试

- `tests/test_voice_time_governance_v1.py`：覆盖规范中的 5 类场景 + 80s 提示与 idle/session_open 可观察性
- 回归：`tests/test_voice_input_mainline_v1.py`

### 结论

本轮已把 **90s 长语音输入** 与 **30s 会话窗口** 从计时与状态上分离，并在 `capturing_input` 期间挂起会话时钟，避免长语音被会话窗口误杀。

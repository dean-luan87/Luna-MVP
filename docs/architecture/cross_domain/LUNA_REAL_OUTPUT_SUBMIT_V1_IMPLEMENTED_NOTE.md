# 真实输出链最小 submit（V1）实现说明

## 改了什么

在不引入 speaking/runtime 真源、不让跨域旁路进入真实输出候选的前提下，补齐一条**最小可运行 submit 闭环**：

- 在语音主线分流产物 `VoiceFinalTextDispatchResult` 生成并经 `cross_domain_orchestrator_v1` 挂载白盒后，按开关决定是否生成 `SpeechRequest`。
- 通过一个最小 `VoiceOutputPlane` 实现真实调用 `submit()`，并将最小 observation 以 JSONL 落盘，保证可用 `request_id` 形成可验证节点。

## 落点（真实代码路径）

- 主线分流：`capabilities/voice/runtime/voice_final_text_dispatcher.py::dispatch_voice_final_text(...)`
  - 三分支（short/long/reject）在 orchestrator 后统一执行：
    - `_maybe_submit_real_output_v1(out2)`

## 开关与回退

- 默认关闭（零侵入）：`LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1` 未开启时，主线行为完全不变且不会写入 trace。
- 一键回退：设置 `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1=0`（或不设置）即回到“仅 whitebox-only、无 submit”的旧路径。

## V1 候选范围（写死）

仅允许“原主链稳定输出”的提示/确认类短文本进入 submit（V1 最小覆盖）：

- `rejected_input`：使用 `VoiceInputRejectionResult.reason` 作为提示文本（截断 ≤ 80 字）
- `short_controlled_input` 且 `BridgeRouteType.SESSION_WAKE`：固定提示 `"我在。"`

明确禁止：

- `risk_interrupt_v1` / `sidewalk_nav_v1` / `retail_find_item_v1` 进入 submit（仍为 whitebox-only）
- speaking/runtime 真源接入
- Level 2 抢占/挂起/恢复

## 输出平面（V1）

新增最小输出平面实现：

- `capabilities/voice/output/voice_output_plane_v1.py`
  - `VoiceOutputPlaneV1.submit(request: SpeechRequest) -> (accepted, reason)`
  - 默认 dry-run（不依赖本地 TTS 可执行文件），仍会写入 `submit_invoked/selection/cutover/playback` 四类节点以证明闭环成立
  - 可选执行现有 `run_tts_unified_entry(...)`（`LUNA_REAL_OUTPUT_SUBMIT_V1_EXECUTE_TTS=1`）

trace 落盘路径：

- `LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL`（默认 `logs/real_output_submit_v1.jsonl`）

## 最小观测节点（可抽链/可验证）

以 JSONL envelope 写入（字段均包含 `request_id`）：

- `submit_invoked`（`OutputSubmitObservation`）
- `selection`（`ProviderSelectionObservation`）
- `cutover`（`TTSCutoverObservation`）
- `playback`（`PlaybackObservation`，占位用于闭合终态；不等同 speaking 真源）

并在抽链器中新增对 `submit_invoked` 的归一化与 stage 展示：

- `capabilities/voice/observations/request_trace_extractor.py`

## 怎么验证

```bash
python3 tools/test_real_output_submit_v1.py
```

覆盖：

- 默认关闭：不写 trace
- 开启后：`rejected_input` 触发最小 submit 闭环，JSONL 中同一 `request_id` 可看到 `submit_invoked/selection/cutover/playback`


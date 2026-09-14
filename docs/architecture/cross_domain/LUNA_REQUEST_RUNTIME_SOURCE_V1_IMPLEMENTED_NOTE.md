# request 真源实现（V1）说明

## 改了什么

在最小 submit 闭环（V1）已成立的基础上，补齐 **request 层真状态事件**，使系统能在不接 speaking/playback 真源的前提下，明确看到：

- request 是否已创建
- 是否进入 submit（submit 是否被调用）
- submit 是否失败/被拒绝
- 是否已观测到“当前可见终态”（terminal observed）

## 真源定义（V1）

V1 将 request 生命周期定义为以下事件（均以同一 `request_id` 串联）：\n
- `request_created`：`SpeechRequest` 已构造（尚未提交）\n
- `request_submitted`：`VoiceOutputPlane.submit()` 已被调用（request 层真锚点）\n
- `request_submit_failed`：submit 失败（V1 允许为输出面内部失败或强制失败）\n
- `request_submit_rejected`：submit 被拒绝（V1 允许为输出面强制拒绝，用于回归验证）\n
- `request_terminal_observed`：已观测到“当前可见终态”（V1 允许是 provider_chain/legacy/failed_no_output/dry_run 等终态，不要求等同播放完成）

重要边界（写死）：以上事件 **不等同 speaking 真源**；speaking/playback 真源必须来自执行层 playback/result（另行建设）。\n
## 代码落点

- 事件模型：`capabilities/voice/observations/request_runtime_observation.py`
- `request_created`：在主线构造 `SpeechRequest` 时写入 JSONL envelope（`voice_final_text_dispatcher._maybe_submit_real_output_v1`）
- `request_submitted` / `request_submit_failed` / `request_submit_rejected` / `request_terminal_observed`：在输出平面 `VoiceOutputPlaneV1.submit()` 内写入（`capabilities/voice/output/voice_output_plane_v1.py`）
- 抽链支持：`capabilities/voice/observations/request_trace_extractor.py` 新增 `request_runtime` 归一化与 stage 展示

## 开关与回退

- `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1` 默认关闭：关闭时不会写入 request runtime 事件（零侵入）
- 测试专用模拟：
  - `LUNA_REAL_OUTPUT_SUBMIT_V1_FORCE_REJECT=1`：强制 submit rejected
  - `LUNA_REAL_OUTPUT_SUBMIT_V1_FORCE_FAIL=1`：强制 submit failed

## 怎么验证

```bash
python3 tools/test_request_runtime_source_v1.py
```

覆盖：

1. submit 关闭：无 request_runtime 事件
2. submit 开启且成功：同一 request_id 下至少包含 `request_created` → `request_submitted` → `request_terminal_observed`
3. submit 强制拒绝/失败：能看到对应终态事件

## 哪些还没做

- speaking/playback 真源（playback_started/finished/failed/cancelled）未实现
- 不扩 submit 候选范围
- 不让跨域旁路进入真实输出
- 不进入 Level 2（抢占/挂起/恢复）


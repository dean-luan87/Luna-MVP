# Phase-Device-001 — On-Device Log / Trace / Replay Requirements v0（设备侧可观测性最低要求冻结）

**目标**：写死设备侧日志、trace、whitebox、replay 的最低要求，确保 Device-001 验证“可追踪、可回放、可复现、可审计”。  

---

## 1) 总原则（写死）

- 每条记录必须可归因到 `run_id` 与 `frame_or_event_id`
- 每条记录必须带 `timestamp_ms` 与 `mode`
- 必须覆盖 Model/Perception/SceneTask/Fusion/Expression/Fallback 全链路
- 必须可回放：replay_record 能重放（至少按 frame/event 顺序）
- 必须 candidate-only：记录中不得出现放权或 execute/release/retry/reopen 语义

---

## 2) 最小闭环链路记录（写死）

每个闭环事件序列必须至少包含以下 stage（允许合并为单条结构化记录，但字段必须齐全）：

1. `input_event` / `replay_frame` / `controlled_live_frame`
2. `perception_signal`
3. `scene_state`
4. `task_state`
5. `fusion_decision_candidate`
6. `navigation_output_candidate`
7. `output_suppression_or_emit_candidate`
8. `whitebox_trace`
9. `replay_record`
10. `fallback_or_degraded_state`

---

## 3) 每条记录必须具备的通用字段（写死）

- `run_id`（字符串）
- `frame_or_event_id`（字符串/整数均可，但必须稳定可排序）
- `timestamp_ms`（整数）
- `mode`（见 runtime mode contract）
- `source_stage`（字符串；当前阶段名）
- `downstream_stage`（字符串；下游阶段名或 next）
- `reason_codes`（数组；至少 1 个）
- `confidence`（数值；可为 null 但应尽量提供）
- `no_execute_leakage`（bool；必须为 true）
- `closed_safe_or_candidate_only_status`（字符串；v0 允许 `"candidate_only"`）

---

## 4) 白盒/Trace 要求（写死）

必须至少记录：
- `whitebox_trace_id`
- `stage_timings_ms`（可选 dict：perception/scene/task/fusion/expression）
- `errors`（若无则空数组）
- `fallback_events`（若无则空数组）

---

## 5) Replay 要求（写死）

必须至少记录：
- `replay_record_id`
- `replay_source`（file/device/export）
- `replay_index`（递增）
- `payload_ref`（指向 frame/video slice/log chunk 的引用字符串；v0 可为占位）

---

## 6) 禁止项（Hard）

出现任一即应在验证工具中判定为 no-go：
- execute/release/retry/reopen 语义出现（任一字段字符串扫描）
- `default_on=true` 或未显式进入 controlled_live_input_mode
- 缺失 `run_id` / `timestamp_ms` / `mode` / `source_stage`（链路不可追踪）
- 缺失 replay_record（无法回放）


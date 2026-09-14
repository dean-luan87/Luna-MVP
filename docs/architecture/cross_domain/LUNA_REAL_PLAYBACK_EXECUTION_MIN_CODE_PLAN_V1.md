# 最小真实执行层实现计划（V1）

## 1. 目标

### 为什么现在该从“对齐方案”进入“最小真实执行层实现计划”

在《[LUNA_REAL_PLAYBACK_EXECUTION_ALIGNMENT_PLAN_V1.md](./LUNA_REAL_PLAYBACK_EXECUTION_ALIGNMENT_PLAN_V1.md)》中已确认关键事实：

- 当前仓库内没有现成的 `speech_gate/audio_worker` 真实执行层实现
- playback/speaking 真源要成为“真实系统事实”，必须由真实执行层产出

因此下一步不再是继续写“对齐理念”，而是把 **Playback Plane + Audio Worker** 的最小实现落点、数据贯穿、事件产出点、回退方式写清楚，使后续可以直接进入代码落地。

### 这份计划解决什么问题

- 给出**最小真实执行层**在本仓库的落地位置与模块边界（不扩功能、不做抢占/恢复）
- 写清 `request_id` 与 `audio_bytes` 的贯穿方式，保证可抽链对账
- 写清 playback 真状态事件（started/finished/failed/cancelled）由谁产出、何时产出
- 写清与当前输出链的最小接线点，以及不稳定时如何一键回退到当前“最小执行层锚点”

---

## 2. 最小执行层结构（V1）

### 2.1 Playback Plane 放在哪

建议新增一个“播放执行层入口”模块（Playback Plane），放在：

- `capabilities/voice/output/playback_plane_v1.py`（建议路径）

**最小职责**：

- 接收 `(request_id, audio_bytes, metadata)` 的播放请求
- 将请求投递给 Audio Worker 队列（不阻塞主线程）
- 负责“投递是否成功”的返回值（accepted/queue_full 等）
- **不**直接产出 `playback_started/finished/...`（这些应由 Audio Worker 执行线程产出）

### 2.2 Audio Worker 放在哪

建议新增 Audio Worker（单线程 + 单队列），放在：

- `capabilities/voice/output/audio_worker_v1.py`（建议路径）

**最小职责**：

- 单独线程/协程消费队列
- 在“真正开始播放”时写 `playback_started`
- 在“播放结束/失败/取消”时写对应终态事件
- 维护最小的“当前正在播放的 request_id”（仅用于内部一致性，不提供上层 speaking 接管）

### 2.3 与现有最小执行器的关系

当前已有：

- `capabilities/voice/output/playback_executor_v1.py`（最小执行层锚点）

V1 真实执行层落地后的策略：

- `playback_executor_v1` 保留为 **fallback**（回退锚点），默认不删
- 新执行层通过显式开关启用（默认关闭）

---

## 3. request_id 贯穿（写死）

### 3.1 request_id 从哪来

当前主线已固定以 `SpeechRequest.request_id` 作为输出链主键，且其来源为：

- `VoiceFinalTextDispatchResult.request_id`（主线分流 request_id）

该 request_id 已用于：

- request 真源事件（`request_runtime`）
- playback 真源事件（`playback_runtime`）

### 3.2 如何传到执行层

必须写死：执行层 API 的第一参数就是 `request_id`，禁止靠时间窗或文本 hash 推断。

推荐执行层调用形态：

- output plane 拿到音频后调用：`playback_plane.submit(request_id=..., audio_bytes=..., ...)`

### 3.3 如何用于 playback 事件与抽链对账

执行层产出的所有 playback 真状态事件必须包含同一 `request_id`：

- `playback_started`
- `playback_finished`
- `playback_failed`
- `playback_cancelled`

并以 JSONL envelope（建议沿用 `type="playback_runtime"`）落盘，确保 `request_trace_extractor` 可按 request_id 聚合。

---

## 4. 最小执行顺序（文字顺序）

V1 的最小闭环顺序写死为：

1) 主线生成 `SpeechRequest`（已有）  
2) `VoiceOutputPlane.submit()` 被调用（已有）  
3) `tts_unified_entry` 或等价链路返回 `audio_bytes`（仅在真实执行路径）  
4) output plane 将 `(request_id, audio_bytes)` 投递到 **Playback Plane**  
5) Playback Plane 投递到 **Audio Worker** 队列（不阻塞）  
6) Audio Worker 真正开始播放时写 `playback_started`  
7) 播放结束写 `playback_finished`；异常写 `playback_failed`；被取消写 `playback_cancelled`

---

## 5. 最小状态与事件（V1 必须支持）

V1 必须支持并写入以下事件（同一 request_id 串起）：

- `playback_started`
- `playback_finished`
- `playback_failed`
- `playback_cancelled`

事件产出点（写死）：

- 必须由 **Audio Worker 执行线程** 产出（执行层真源）
- Playback Plane 只负责投递，不得把“投递成功”冒充 started

---

## 6. 与当前输出链的接点（最小改造点）

### 6.1 audio_bytes 在哪一层交给执行层

写死：在 `VoiceOutputPlaneV1.submit()` 的真实执行路径中，拿到 `audio_bytes` 后交给执行层。

现状（参考）：

- `capabilities/voice/runtime/tts_unified_entry.py` 返回 `provider_result.audio_bytes`

最小改造建议：

- 在 `VoiceOutputPlaneV1.submit()` 内：
  - 保持 request 真源事件不变
  - 将 `audio_bytes` 投递给 playback plane
  - 由 audio worker 产出 playback 真状态事件

### 6.2 当前哪些模块需要最小改造

建议最小改动范围（实现阶段）：

- `capabilities/voice/output/voice_output_plane_v1.py`：将现有“playback_executor_v1”替换为“playback_plane_v1（真实执行层）”，并保留 fallback
- `capabilities/voice/observations/request_trace_extractor.py`：无需大改，只需确保能消费 `playback_runtime` 事件（已具备）

### 6.3 哪些地方绝对不要动（写死）

- 不扩 submit 候选范围（仍仅 prompt/confirmation 短文本）
- 不让其他旁路进入真实输出
- 不引入中断/恢复/队列优先级/跨 request 合并
- 不把 metadata/白盒当作 speaking 真状态

---

## 7. 回退方式（必须写死）

### 7.1 回退目标

当真实执行层不稳定时，必须能回退到：

- 当前最小执行层锚点 `playback_executor_v1`（或完全关闭执行层）

且保证：

- submit 闭环与 request 真源不受影响
- dry-run 纪律不被破坏（dry-run 不伪造 playback_started）

### 7.2 建议的最小回退开关矩阵（实现阶段落）

建议引入：

- `LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1=0`（默认关闭）

行为：

- `=0`：继续使用 `playback_executor_v1`（当前行为）
- `=1`：使用真实 Playback Plane + Audio Worker

回退操作：

- 一键将 `LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1=0`

---

## 8. 当前阶段不做项（再次写死）

- 不做抢占
- 不做恢复
- 不做队列优先级/调度
- 不做多设备输出
- 不做复杂缓存与持久化
- 不扩大旁路进入真实输出

---

## 一句话收束

先把 Playback Plane + Audio Worker 的最小代码落点、数据贯穿、事件产出点与回退开关写清楚，再进入“最小真实执行层代码落地”。


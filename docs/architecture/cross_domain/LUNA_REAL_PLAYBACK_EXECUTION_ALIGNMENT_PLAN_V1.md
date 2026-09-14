# 真实 playback 执行层对齐方案（V1）

## 1. 目标

在当前已具备：

- submit 闭环（`SpeechRequest` → `VoiceOutputPlane.submit()`）
- request 真源（`request_runtime` 事件）
- playback/speaking 真源（`playback_runtime` 事件，dry-run 不伪造）

的基础上，把 **playback 真源** 从“最小执行层锚点（`playback_executor_v1`）”推进到**真实执行层**（等价于 `speech_gate` / `audio_worker` 这一层级），使 speaking/playback 状态不再是“模拟执行”，而是与真实播放管线对齐的系统事实。

> 本文件只出方案，不改代码、不扩输出候选、不改 Level 2 边界。

---

## 2. 当前现状（事实）

### 2.1 已有输出链与观测

- 输出侧：`VoiceOutputPlaneV1.submit()` 已可被主线调用，且可写入 trace（JSONL envelope）
- request 真源：`request_created/request_submitted/request_terminal_observed` 等事件已存在
- playback 真源（V1）：`playback_started/finished/failed/cancelled` 事件已存在，但执行层锚点目前是 `capabilities/voice/output/playback_executor_v1.py`（最小执行器）

### 2.2 真实执行层在本仓库中的状态

在当前仓库中：

- 未发现名为 `speech_gate` / `audio_worker` 的真实执行层实现代码文件（仅存在历史修复文档 `docs/V1_8_1_AUDIO_WORKER_FIX.md` 的方案描述，但对应 `core/audio_worker.py` 等文件不在仓库内）
- `tts_unified_entry` 明确边界：**不替代 speech_gate / audio_worker**

结论：要实现“真实 playback 执行层对齐”，需要在仓库内补齐一个**最小真实执行层**（或对接到已有但当前不在仓库的执行层），并让 playback 真源事件由该层产出。

---

## 3. 对齐原则（写死）

1. **playback 真源必须来自执行层**：只有“实际开始播放/结束播放/失败/取消”的那一层才能产出 `playback_*` 真状态事件。  
2. **request_id 必须贯穿**：执行层必须以 `request_id` 为主键回填 playback 事件，禁止靠时间窗猜。  
3. **submit ≠ playback**：`request_submitted` 仅证明提交发生，不得推断 speaking=true。  
4. **默认关闭、可回退**：接线必须允许一键回退到当前“最小执行器锚点”或“仅 request 真源”。  
5. **不扩功能**：不引入复杂队列、中断/恢复、跨 request 合并；仅建立对齐锚点与事件回填。

---

## 4. 目标状态：两层真源事件（最终应长这样）

### 4.1 request 层（已具备）

由输出平面 submit 侧产出：

- `request_created`
- `request_submitted`
- `request_submit_failed` / `request_submit_rejected`
- `request_terminal_observed`（当前可见终态）

### 4.2 playback/speaking 层（需要对齐到真实执行层）

由真实执行层产出：

- `playback_started`
- `playback_finished`
- `playback_failed`
- `playback_cancelled`

并且：

- speaking=true 的唯一可靠锚点是 `playback_started`
- speaking=false 的可靠终态锚点是 `playback_finished/failed/cancelled`

---

## 5. 真实执行层对齐的最小方案（V1）

> 这里给出“最小可落地”的执行层骨架与对齐点，命名可在实现阶段再定，但职责必须一致。

### 5.1 新增/引入一个“播放执行层入口”（Playback Plane）

定义一个最小执行层入口（协议或类），接收“可播放载荷”并返回结果：

- 输入：`request_id` + `audio_bytes`（或可播放的音频句柄） + 最小 metadata（例如 output_category）
- 输出：执行结果（accepted/started/finished/failed/cancelled）与原因

该入口是 speaking 真源的**唯一写入点**：由它（或它下游）写入 `PlaybackRuntimeObservation`。

### 5.2 Audio Worker（单线程/队列）作为最小执行形态

参考 `docs/V1_8_1_AUDIO_WORKER_FIX.md` 的工程纪律（异步隔离、队列可丢弃、主循环不阻塞），V1 可采用：

- 单一后台线程
- 队列上限（可先为 1，宁可漏播，不可积压）
- 投递即返回（submit 不等待播放完成）

并明确事件回填时机：

- **入队成功**：不等于 playback_started（只意味着 accepted）
- **真正开始播放**：写 `playback_started`
- **播放结束/失败/取消**：写对应终态

### 5.3 与现有输出链的对齐位置

对齐点应当发生在：

- `VoiceOutputPlaneV1.submit()`（或其后继 output plane）的“拿到可播放音频后”  
  - 当前 `tts_unified_entry` 可产出 `audio_bytes`（provider_result.audio_bytes）
  - 之后把 `audio_bytes` 投递给真实执行层入口（Audio Worker）
  - playback 真源事件必须由执行层写入（而不是 output plane 猜测）

### 5.4 观测落盘与抽链兼容

要求执行层写入的事件满足：

- JSONL envelope 继续使用统一 trace 文件（或同一抽链入口），类型建议沿用 `playback_runtime`
- 字段必须包含：`request_id/timestamp/event/status/reason`
- 抽链器（`request_trace_extractor`）继续按 `request_id` 聚合并展示 `playback_result` stage

---

## 6. 迁移策略（从“最小执行器锚点”到“真实执行层”）

### 6.1 三阶段迁移（建议）

**Phase A：并存不切换（观测对齐）**  
- 保留 `playback_executor_v1` 作为 fallback（或测试模式）  
- 新执行层上线但默认关闭  
- 先验证 request_id 贯穿与事件闭合率

**Phase B：小流量切换（真实执行层成为真源）**  
- 开关开启后，仅在 `EXECUTE_TTS=1` 且执行层可用时走真实执行层  
- dry-run 仍不写 playback 真状态（保持当前纪律）

**Phase C：移除占位执行器（仅在稳定后）**  
- 当真实执行层长期稳定且闭合率达标，再逐步降低 `playback_executor_v1` 权重

### 6.2 回退（写死）

任一出现以下情况必须回退到 Phase A/或直接关闭：

- playback 真源事件无法闭合或与 request_id 不一致
- 线程/队列导致主循环阻塞或资源争用
- 播放失败率异常上升且无法定位

---

## 7. 当前阶段不做项（写死）

- 不做中断/恢复（先把“真实播放事件”对齐）
- 不做复杂播放队列与跨 request 合并
- 不做旁路进入真实输出
- 不扩大 submit 候选范围
- 不引入 speaking 接管决策层

---

## 一句话收束

先把 playback 真源从“最小执行器锚点”对齐到真实执行层（Audio Worker / Gate 层级），让 `playback_started/finished/failed/cancelled` 成为真正可依赖的系统事实；在此之前，不扩大任何 Level 2 边界。


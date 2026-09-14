# 最小真实执行层（Playback Plane + Audio Worker）实现说明（V1）

## 实现了什么

根据《[LUNA_REAL_PLAYBACK_EXECUTION_MIN_CODE_PLAN_V1.md](./LUNA_REAL_PLAYBACK_EXECUTION_MIN_CODE_PLAN_V1.md)》，在仓库内补齐“最小真实执行层”骨架：

- **Playback Plane**：接收 `request_id + audio_bytes`，投递到单线程 Audio Worker
- **Audio Worker**：单线程消费队列，在执行线程内产出 playback 真状态事件：
  - `playback_started`
  - `playback_finished`
  - `playback_failed`
  - `playback_cancelled`

并将其接入现有输出链：当 output plane 拿到 `audio_bytes` 后，根据开关决定走新执行层或回退到旧锚点 `playback_executor_v1`。

## 新增模块

- `capabilities/voice/output/playback_plane_v1.py`
- `capabilities/voice/output/audio_worker_v1.py`

保留兼容：

- `capabilities/voice/output/playback_executor_v1.py`（旧锚点，作为回退路径）

## 开关与回退（默认关闭）

新增开关：

- `LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1=0`（默认）

行为：

- `=0`：继续走旧锚点 `playback_executor_v1`
- `=1`：走 `playback_plane_v1` → `audio_worker_v1`（单线程/单队列）

回退：

- 直接将 `LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1=0` 即秒退旧路径
- 不影响 submit/request 真源与其他旁路边界

## 最小边界（V1 写死）

- 单线程
- 单队列（maxsize=1）
- request_id 显式贯穿（不推断）
- started/finished/failed/cancelled 四事件
- 不做抢占/恢复/优先级/多设备
- 不把“投递成功”冒充 started（started 仅在 worker 开始处理时发出）

## 代码接入点

- `capabilities/voice/output/voice_output_plane_v1.py`：
  - 在 `EXECUTE_TTS=1` 的路径拿到 `audio_bytes` 后：
    - 若 `LUNA_ENABLE_REAL_PLAYBACK_EXECUTION_V1=1` → 投递给 `playback_plane_v1`
    - 否则 → 继续走 `playback_executor_v1`

## 怎么验证

新增脚本：

```bash
python3 tools/test_real_playback_execution_v1.py
```

覆盖：

- started → finished
- 强制 failed / cancelled（通过 Audio Worker 的测试开关）

并建议继续回归：

```bash
python3 tools/test_real_output_submit_v1.py
python3 tools/test_request_runtime_source_v1.py
python3 tools/test_playback_runtime_source_v1.py
```

## 哪些还没做

- 未接入真实设备播放（目前执行层不连声卡/播放器；后续替换 Audio Worker 内部实现即可）
- 不做中断/恢复、队列治理、优先级调度
- 不扩大 Level 2 边界与旁路晋升


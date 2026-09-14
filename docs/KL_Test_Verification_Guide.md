# K/L 层测试验证指南

完成介入意图层（K）与介入内容规划层（L）的测试验证：在 ACTIVE × 视频 下确认 trace 中出现 `arbitration` → `k` → `l`，且取值符合设计。

---

## 1. 目标与前提

- **目标**：确认在「强制 ACTIVE + 足够复杂度」的跑测中，系统进入 ENGAGED，产生仲裁事件，且每条仲裁记录带有 K 层（`k.intent`）与 L 层（`l.slot_type` / `l.slot`）。
- **前提**：
  - 使用 `tools/run_active_video_test.py`（会设置 ACTIVE + **测试用强制 ENGAGED/L1**，见下）。
  - **测试模式下**：当 `TaskStateOverride` 为 ACTIVE 时，`runtime/a3_logger.py` 会强制 `rhythm=ENGAGED`、`engagement.level=L1`，因此**任意视频**都会写入 arbitration 与 K/L，便于验收。
  - 非测试模式（直接跑 main）：需视频有足够视觉复杂度，使 rhythm 自然进入 ENGAGED。

---

## 2. 推荐视频与命令

按 `docs/Test_Videos_Inventory.md`，优先用**复杂度高、易进 ENGAGED** 的视频：

| 优先级 | 视频文件 | 说明 |
|--------|----------|------|
| 1 | `test_video_complex_6m42s.mp4` | 30fps，复杂场景，最易出现 ENGAGED 与 K/L |
| 2 | `test_video_follow_crowd_crossing_6m14s_60fps.mp4` | 60fps，人群+过马路，中等复杂度 |

**建议执行（在项目根目录）：**

```bash
# 跑 120 秒，强制 ACTIVE，限时退出
python3 tools/run_active_video_test.py \
  --video test_video_complex_6m42s.mp4 \
  --seconds 120
```

若 120s 内仍无 K/L，可适当延长（例如 `--seconds 180`）或换用人群过马路视频。

---

## 3. 执行步骤

1. **清空或备份旧 trace（可选）**  
   - 若希望本次结果干净，可先备份或清空：  
     `mv logs/a3_trace.jsonl logs/a3_trace.jsonl.bak` 或直接删除。

2. **运行 ACTIVE×视频 测试**  
   - 执行上面推荐命令，等待跑满 `--seconds` 或视频结束。

3. **验收 trace**  
   - 见下节「验收标准」与「验收命令」。

---

## 4. 验收标准

在 **`logs/a3_trace.jsonl`** 中应能看到：

| 项目 | 说明 |
|------|------|
| **engagement** | 出现 `"engagement": { "level": "L1" \| "L2" \| "L3" }`（至少部分行）。 |
| **arbitration** | 出现 `"arbitration": { "winner": "...", "candidates": [...], ... }`。 |
| **k** | 与 arbitration 同条的记录中应有 `"k": { "intent": "NAV_GUIDE" \| "ENV_NOTICE" \| "TASK_ASSIST" \| "SAFETY_WARN" \| "STATUS_UPDATE" \| "NONE" }`。 |
| **l** | 与 arbitration 同条的记录中应有 `"l": { "slot_type": "...", "slot": {...} \| null }`。 |

**K 层 v0 映射**：G.winner_type → K.intent（如 NAVIGATION→NAV_GUIDE, SAFETY→SAFETY_WARN）。  
**L 层 v0**：根据 intent 与 a3_signals 输出 slot_type（如 NAV_TARGET/ENV_TARGET/TASK_TARGET/NONE）及可选的 slot。

---

## 5. 验收命令

**方式一：用现有分析脚本（含 G 与 K/L 统计）**

```bash
python3 tools/analyze_a3_trace.py logs/a3_trace.jsonl --longterm
```

查看输出中的 **「G) 多任务介入仲裁 v0」** 与 **「K/L 层 (arbitration 附带)」** 段。

**方式二：仅提取含 K/L 的仲裁行（便于快速目视）**

```bash
python3 tools/check_kl_trace.py logs/a3_trace.jsonl
```

或一行命令查看带 k、l 的条数：

```bash
python3 -c "
import json, sys
path = sys.argv[1] if len(sys.argv)>1 else 'logs/a3_trace.jsonl'
with open(path) as f:
    rows = [json.loads(l) for l in f if l.strip()]
arb = [r for r in rows if 'arbitration' in r]
with_k = sum(1 for r in arb if r.get('k'))
with_l = sum(1 for r in arb if r.get('l'))
print('arbitration 条数:', len(arb), '| 含 k:', with_k, '| 含 l:', with_l)
for r in arb[:3]:
    if r.get('k') or r.get('l'):
        print('  sample:', {k: r.get(k) for k in ('arbitration','k','l')})
"
logs/a3_trace.jsonl
```

---

## 6. 若始终看不到 K/L 的排查

1. **确认是否有 ENGAGED**  
   - 在 trace 中搜索 `"engagement"`，看是否出现 `"level":"L1"` / `L2` / `L3`。  
   - 若全程为 L0，说明未进 ENGAGED，arbitration 与 K/L 不会触发。

2. **确认 rhythm 为何未进 ENGAGED**  
   - 节律 v0 条件：**IDLE→PREPARE** 需 `ACTIVE + eligible + pal >= 0.15 + view_confidence >= 0.6`；**PREPARE→ENGAGED** 需 `pal >= 0.20` 且 PREPARE 持续 ≥2 秒。  
   - 若 trace 里 `pal`（PAL v0 horizon_difficulty）普遍很低（如 p95 < 0.20）或 `view_confidence` 均值 < 0.6，则很难进入 ENGAGED。  
   - 用 `analyze_a3_trace.py` 看 **PAL v0** 与 **view_confidence mean**，确认是否被这两项卡住。

3. **确认 eligibility**  
   - 查看 `intervention.eligible` 与 `intervention.task_state`。  
   - ACTIVE + `complexity_effective >= 0.5` 才会 eligible；eligible 后 rhythm 才可能进入 PREPARE/ENGAGED。

4. **换视频或延长时长**  
   - 优先用 **`test_video_complex_6m42s.mp4`**（复杂场景、更易出现高 PAL/复杂度）；或 `test_video_follow_crowd_crossing_6m14s_60fps.mp4`，并适当增加 `--seconds`（如 180）。

5. **确认脚本与 override**  
   - 必须通过 `run_active_video_test.py` 跑（会设置 `TaskStateOverride.set_active`）。  
   - 使用该脚本时，会同时强制 ENGAGED + L1（见 `runtime/a3_logger.py`），因此**只要用 run_active_video_test 跑，就应出现 arbitration 与 K/L**；若仍无，请检查 trace 是否写到了 `logs/a3_trace.jsonl`、或是否有其他异常。

---

## 7. 通过标准（小结）

- 使用推荐视频 + `run_active_video_test.py` 跑满至少 120 秒。
- `logs/a3_trace.jsonl` 中：
  - 存在 engagement.level ∈ {L1,L2,L3}；
  - 存在 arbitration 事件；
  - 至少有一条 arbitration 记录同时带有 `k` 与 `l`，且 `k.intent`、`l.slot_type`/`l.slot` 符合 K/L v0 设计。

满足以上即视为 **K/L 测试验证通过**。

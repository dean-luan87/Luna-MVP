# A1 v0 验收指标对照表（冻结版）

**是否进入下一步（A2）的唯一判断依据，不需要主观解释。**

---

## 一、核心目标（必须命中）

| 指标 | 通过标准 | 判定方式 |
|------|----------|----------|
| L2 是否自然出现 | ≥ 1 次 | `count(engagement.level == "L2") ≥ 1` |
| L2 连续驻留 | ≥ L2_HOLD_SECONDS（建议 3s） | 计算连续 L2 段的时长 |
| L2 抖动 | ❌ 不出现 1s 内进出 | L2 段内无 L1/L0 插入 |
| 非 force 的 L2 | 100% | trace 中无 force_engaged 标记 |

---

## 二、稳定性与克制性（必须同时满足）

| 指标 | 通过标准 | 说明 |
|------|----------|------|
| L2 占比 | 1%–10% | 过低=过保守；过高=过激进 |
| L1 仍为主态 | ≥ 70% | 系统应长期处于准备态 |
| GUARDED 不因 A1 上升 | 变化 ≤ ±5% | A1 不应改变 control 基线 |

---

## 三、执行链影响（允许但不强制）

| 指标 | 期望 | 判定 |
|------|------|------|
| ACTION_EXECUTED（非 force） | 0–2 次 | 多了说明阈值偏低 |
| BLOCKED 仍占多数 | ≥ 85% | 军工级克制 |
| FAILED / UNKNOWN | 0 | 任意出现即失败 |

---

## 四、PAL × A1 协同（只读验证）

| 指标 | 通过标准 | 含义 |
|------|----------|------|
| 进入 L2 时 PAL | ≥ PAL_L2_THRESHOLD | A1 未绕过 PAL |
| 进入 L2 时 VC | ≥ VC_L2_THRESHOLD | 视觉可信 |
| L2 进入前 PAL 连续性 | 连续 ≥ 3s | A1 时间窗生效 |

---

## 五、明确的失败信号（出现即停）

| 现象 | 结论 |
|------|------|
| L2 频繁进出（<3s） | A1 失败（时间窗失效） |
| L2 大量出现但无 PAL 支撑 | A1 失败（条件泄漏） |
| ACTION_EXECUTED 激增 | A1 失败（放大器效应） |
| 需要人为解释才能“算通过” | 直接不通过 |

---

## 最终判定规则（一句话）

只要在真实视频里看到：**L2 自然出现 ≥1 次，且连续 ≥3 秒，没有抖动，没有副作用** —— A1 即可封板。

---

## 下一步分支

- **若 A1 通过** → 进入 A2（PAL 优先级上移）
- **若 A1 不通过** → 不改结构，只微调阈值（不是回滚）

---

## 验收步骤

1. **跑真实视频（不加 force；视频无目标时需加 --simulate-active）**
   ```bash
   python3 tools/run_video_a3_trace.py --video test_video_complex_6m42s.mp4 --simulate-active
   ```
   说明：`--simulate-active` 仅模拟 ACTIVE 任务态，使 rhythm 可变为 ENGAGED，L2 仍由条件自然出现；不加 `--force-engaged`/`--force-engaged-test-l2`。

2. **自动裁决（读 trace 给通过/不通过）**
   ```bash
   python3 tools/verify_a1_acceptance.py logs/a3_trace.jsonl
   ```

3. **可选：人工看统计**
   ```bash
   python3 tools/analyze_a3_trace.py logs/a3_trace.jsonl
   python3 tools/verify_p1_v0.py logs/a3_trace.jsonl
   ```

---

## A1 参数（v0 冻结）

| 参数 | 值 |
|------|-----|
| PAL_L2_THRESHOLD | 0.19（微调自 0.22） |
| COMPLEXITY_L2_THRESHOLD | 0.5 |
| VC_L2_THRESHOLD | 0.6 |
| L2_HOLD_SECONDS | 3.0 |

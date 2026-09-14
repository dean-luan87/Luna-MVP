# B2 Runtime Trace 三条铁律（不可违背）

## 铁律 1：任何一次行为判断，必须可视

**不是"可能"，是 必须**

### 工程含义
- 任何 `impact != NO_OP` 必须 在某个 trace / timeline / 页面上看到
- 看不到 = 判断无效 = bug

### 禁止行为
- ❌ 只打 log
- ❌ 只在内部变量里存在
- ❌ 只在模型里"算过但没说"

### 当前实现验证
✅ **已实现**：所有 `impact != NO_OP` 都会：
1. 写入 `trace["impact_evaluation"]`
2. 写入 `trace["to_c_message"]`（sent: true）
3. 写入 `trace["writeback"]["timeline_written"]: true`
4. 写入 trace 文件 `traces/b2_runtime_trace_v04.jsonl`

---

## 铁律 2：任何一次判断，必须可追溯到"哪一秒、哪一帧、哪条规则"

### 工程含义
必须能回答下面 5 个问题中的任意一个：

| 问题 | 没答案的后果 |
|------|------------|
| 哪一秒发生的？ | 时间语义失效 |
| 哪一帧触发的？ | 认知连续性失效 |
| 哪个 factor 起作用？ | 感知不可控 |
| 命中了哪条规则？ | 无法修复误判 |
| 当时 B 在不在跑？ | 系统状态不可审计 |

👉 **任何一个回答不了，直接判定"系统不可用"**

### 当前实现验证
✅ **已实现**：每条 trace 都包含：

```json
{
  "time": {
    "ts": 120.02,           // ✅ 哪一秒
    "frame_id": 3599,        // ✅ 哪一帧
    "fps": 30.0,
    "human_time": "02:00.020"
  },
  "b_runtime_state": {      // ✅ B 在不在跑
    "active": true,
    "mode": "ACTIVE",
    "reason": "normal operation"
  },
  "trigger": {              // ✅ 触发信息
    "triggered": true,
    "trigger_factor": "path"
  },
  "perception": {            // ✅ 哪个 factor
    "path": {
      "score": 0.65,
      "reason": "..."
    }
  },
  "rule_evaluation": [      // ✅ 命中了哪条规则
    {
      "rule_id": "PATH_SLOW_DOWN",
      "expression": "path.score >= 0.6",
      "actual_value": 0.65,
      "threshold": 0.6,
      "hit": true
    }
  ]
}
```

---

## 铁律 3：任何一次"不作为"，也必须有理由

**这是最容易被忽略、但最致命的一条。**

### 工程含义
- 没有输出 ≠ 没有记录
- `NO_OP ≠ 什么都没发生`
- "B 没说话"本身 也是一个判断结果

### 必须存在
```json
{
  "impact": "NO_OP",
  "reason": "below threshold / gated / delegated"
}
```

否则你永远分不清：
- 系统没看到
- 系统看到了但忽略
- 系统被 gate 掉
- 系统崩了

### 当前实现验证
✅ **已实现**：所有 `NO_OP` 情况都会记录：

1. **窗口不足**：
```json
{
  "trigger": {
    "triggered": false,
    "reason": "insufficient window data"
  },
  "impact_evaluation": {},
  "to_c_message": {"sent": false, "reason": "no evidences"},
  "writeback": {"timeline_written": false, "reason": "insufficient window"}
}
```

2. **无证据**：
```json
{
  "trigger": {
    "triggered": false,
    "reason": "no evidences"
  },
  "impact_evaluation": {},
  "to_c_message": {"sent": false, "reason": "no evidences"}
}
```

3. **NO_OP（有证据但未触发）**：
```json
{
  "impact_evaluation": {
    "impact": "NO_OP",
    "main_factor": "path",
    "confidence": 0.45
  },
  "to_c_message": {
    "sent": false,
    "reason": "impact == NO_OP"
  },
  "writeback": {
    "timeline_written": false,
    "reason": "NO_OP"
  }
}
```

4. **B 未激活**：
```json
{
  "b_runtime_state": {
    "active": false,
    "mode": "GATED",
    "reason": "camera unstable"
  },
  "trigger": {
    "triggered": false,
    "reason": "B not active"
  }
}
```

---

## 工程约束

### 约束 1：所有 B2 判断函数必须支持 trace 注入

**当前状态**：✅ 已实现
- `tick()` 方法在每一步都构建 trace
- 所有判断结果都写入 trace

### 约束 2：timeline 只能来源于 trace，而不是反过来

**当前状态**：✅ 已实现
- 流程：判断 → trace → 决定是否写 timeline
- `writeback["timeline_written"]` 明确记录是否写入

### 约束 3：测试失败的第一步不是看结果，而是看 trace

**测试流程**：
1. ❌ 不先看"准不准"
2. ✅ 先看：
   - trace 是否完整
   - 是否每一秒都有状态
   - 是否有 unexplained silence
3. 再讨论判断逻辑

---

## 验证方法

### 1. 检查 trace 完整性
```bash
# 检查是否有遗漏的秒
cat traces/b2_runtime_trace_v04.jsonl | jq -r '.time.ts' | sort -n | uniq

# 检查所有 NO_OP 都有 reason
cat traces/b2_runtime_trace_v04.jsonl | jq 'select(.impact_evaluation.impact == "NO_OP") | .writeback.reason'
```

### 2. 检查可追溯性
```bash
# 检查某一秒的完整信息
cat traces/b2_runtime_trace_v04.jsonl | jq 'select(.time.ts == 120.02)'

# 检查所有触发的记录
cat traces/b2_runtime_trace_v04.jsonl | jq 'select(.trigger.triggered == true)'
```

### 3. 检查可视性
```bash
# 检查所有有 impact 的记录
cat traces/b2_runtime_trace_v04.jsonl | jq 'select(.impact_evaluation.impact != "NO_OP")'

# 检查所有写入 timeline 的记录
cat traces/b2_runtime_trace_v04.jsonl | jq 'select(.writeback.timeline_written == true)'
```

---

## 违反铁律的后果

如果发现以下情况，**立即停止开发，修复后再继续**：

1. ❌ 有 `impact != NO_OP` 但没有 trace 记录
2. ❌ trace 中缺少时间/帧/规则信息
3. ❌ `NO_OP` 没有 reason
4. ❌ 无法回答"哪一秒、哪一帧、哪条规则"中的任意一个

---

## 下一步

运行测试生成 trace：
```bash
python3 examples/test_b2_trace_generation.py --duration 20 --scenario path_change
```

然后进行"人类视角 vs B 的认知复盘"。

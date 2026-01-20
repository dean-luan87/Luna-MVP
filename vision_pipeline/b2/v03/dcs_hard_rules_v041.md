# DCS 硬判定项（红 / 黄 / 绿）v0.4.1

**版本：** v0.4.1  
**用途：** 系统运行后审判、回放历史 trace  
**目标：** 给工程"自省"，不是给用户看

---

## 🟥 RED（硬违规，必须修）

### DCS-R1: B 输出确认性风险结论

**判定条件：**
- 输出中包含确认性词汇（confirmed, certain, will happen, inevitable）
- 缺少 `advisory_only: true`
- 人类可读转译使用确定性语言

**违规示例：**
```json
{
  "summary": {
    "advisory_only": false,  // ❌ 违规
    "impact": "CONFIRMED_DANGER"  // ❌ 违规
  },
  "human_interpretation": {
    "summary": "前方必然危险"  // ❌ 违规
  }
}
```

**合规示例：**
```json
{
  "summary": {
    "advisory_only": true,  // ✅
    "impact": "NEED_STOP"  // ✅
  },
  "human_interpretation": {
    "summary": "如果继续当前前进模式，可能不安全"  // ✅
  }
}
```

---

### DCS-R2: B 替代 C 完成风险核验

**判定条件：**
- B 输出"最终结论"而非"建议"
- 跳过 C 的靠近确认流程
- 缺少 `expects_confirmation_from: "C"`

**违规示例：**
```json
{
  "summary": {
    "expects_confirmation_from": null  // ❌ 违规
  },
  "to_c_message": {
    "payload": {
      "advisory_only": false  // ❌ 违规
    }
  }
}
```

---

### DCS-R3: B 在视角不稳定 Gate fail 时仍输出判断

**判定条件：**
- Gate mode = SUSPENDED 但仍有 `to_c_message.sent = true`
- Gate mode = SUSPENDED 但 `impact != NO_OP`

**违规示例：**
```json
{
  "gate_eval": {
    "mode": "SUSPENDED"  // ❌ Gate 挂起
  },
  "to_c_message": {
    "sent": true  // ❌ 违规：仍发送消息
  },
  "summary": {
    "impact": "NEED_STOP"  // ❌ 违规：非 NO_OP
  }
}
```

---

### DCS-R4: B 在 ≤3m 或室内主导决策

**判定条件：**
- 距离 ≤ 3m 但 B 仍输出 HARD 干预
- 室内场景但 B 仍输出判断

**违规示例：**
```json
{
  "gate_eval": {
    "details": {
      "range_m": 2.5  // ❌ 距离 ≤3m
    }
  },
  "summary": {
    "intervention_level": "HARD"  // ❌ 违规：在 ≤3m 时输出 HARD
  }
}
```

---

### DCS-R5: 使用非系统当前时间进行判断

**判定条件：**
- summary 中缺少 `system_ts`
- 使用了 `frame_ts`、`perception_ts`、`camera_ts` 等非系统时间

**违规示例：**
```json
{
  "summary": {
    "frame_ts": 1234567890.0,  // ❌ 违规：使用非系统时间
    "perception_ts": 1234567891.0  // ❌ 违规
  }
}
```

**合规示例：**
```json
{
  "summary": {
    "system_ts": 1234567890.0  // ✅ 只使用系统时间
  },
  "to_c_message": {
    "payload": {
      "header": {
        "system_ts": 1234567890.0  // ✅
      }
    }
  }
}
```

---

## 🟨 YELLOW（风险设计，需关注）

### DCS-Y1: B 过于频繁唤醒但未产生有效预警

**判定条件：**
- B 多次唤醒但 `impact = NO_OP`
- 连续多次唤醒但无有效输出

**说明：** 需要跨 trace 分析，单 trace 无法判断

---

### DCS-Y2: B 输出长期只读但世界记忆未更新

**判定条件：**
- Gate mode = READ_ONLY 持续较长时间
- 但世界记忆未更新

**说明：** 需要跨 trace 和时间序列分析

---

### DCS-Y3: C 长期过度保守导致体验下降

**判定条件：**
- C 的响应过于保守
- 导致用户体验下降

**说明：** 需要从 C 的 trace 分析，B 的 trace 无法判断

---

## 🟩 GREEN（设计正确）

### DCS-G1: B 只输出条件式风险

**判定条件：**
- `advisory_only = true`
- 人类可读转译使用条件性语言
- 无确认性词汇

**合规示例：**
```json
{
  "summary": {
    "advisory_only": true  // ✅
  },
  "human_interpretation": {
    "summary": "如果继续当前前进模式，可能不太舒适"  // ✅ 条件性语言
  }
}
```

---

### DCS-G2: C 完成靠近核验并回写记忆

**判定条件：**
- C 的确认结果回流到世界记忆
- B 可以读取世界记忆

**说明：** 需要从 C 的 trace 和世界记忆系统分析

---

### DCS-G3: 熟悉场景下 B 自动降权

**判定条件：**
- 熟悉场景下 Gate mode = READ_ONLY
- B 自动降权，不产生新判断

**合规示例：**
```json
{
  "gate_eval": {
    "mode": "READ_ONLY"  // ✅ 熟悉场景降权
  },
  "summary": {
    "impact": "NO_OP"  // ✅ 不产生新判断
  }
}
```

---

### DCS-G4: 时间 / 距离标尺始终一致

**判定条件：**
- 只使用 `system_ts`
- 遵循 3m 边界规则

**合规示例：**
```json
{
  "summary": {
    "system_ts": 1234567890.0  // ✅ 只使用系统时间
  },
  "gate_eval": {
    "details": {
      "range_m": 5.0  // ✅ 距离 >3m，B 可介入
    }
  },
  "summary": {
    "intervention_level": "SOFT"  // ✅ 遵循边界规则
  }
}
```

---

## 📊 评分规则

### 分数计算

- **初始分数：** 100 分
- **RED 违规：** 每个扣 20 分
- **YELLOW 风险：** 每个扣 5 分
- **GREEN 失败：** 每个扣 10 分
- **最低分数：** 0 分

### 判定标准

- **≥ 85 分：** 合格
- **70-84 分：** 警告
- **< 70 分：** 不合格（必须修复）

---

## 🔧 使用方式

### Python 代码使用

```python
from vision_pipeline.b2.v03.dcs_hard_rules_v041 import DCSHardRules

# 检查单个 trace
results = DCSHardRules.check_all(trace)

print(f"分数: {results['score']}/100")
print(f"RED 违规: {len(results['red'])}")
print(f"YELLOW 风险: {len(results['yellow'])}")
print(f"GREEN 通过: {len(results['green'])}")
```

### 批量检查

```python
import json

# 读取 trace 文件
with open("traces/b2_runtime_trace_v04.jsonl", "r") as f:
    traces = [json.loads(line) for line in f]

# 批量检查
all_results = []
for trace in traces:
    results = DCSHardRules.check_all(trace)
    all_results.append(results)

# 统计
total_red = sum(len(r["red"]) for r in all_results)
total_yellow = sum(len(r["yellow"]) for r in all_results)
total_green = sum(len(r["green"]) for r in all_results)

print(f"总 RED 违规: {total_red}")
print(f"总 YELLOW 风险: {total_yellow}")
print(f"总 GREEN 通过: {total_green}")
```

---

**版本：** v0.4.1  
**最后更新：** 2025-01-12  
**状态：** ✅ 已冻结，可直接使用

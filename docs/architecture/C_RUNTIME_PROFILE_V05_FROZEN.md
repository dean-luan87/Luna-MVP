# C RuntimeProfile v0.5（冻结）

**Status：** FROZEN / READ-ONLY  
**版本：** v0.5  
**日期：** 2025-01-12

---

## 📋 定位

这是非常重要的一步：
从这一刻开始，B / C 共享同一套"运行纪律语言"。

---

## 1. C RuntimeProfile 完整结构

```json
{
  "event_type": "C_RUNTIME_PROFILE",
  "time": {
    "ts": 123.45,
    "frame_id": 6789
  },
  "c_runtime_profile": {
    "mode": "ACTIVE | DEGRADED | SUSPENDED",
    "control_level": "NONE | ASSIST | FULL",
    "update_interval_ms": 50,
    "blocked_by": "sensor_noise | conflict | scheduler",
    "human_reason": "前方信息冲突，C 降级执行"
  }
}
```

---

## 2. 字段逐项冻结说明

### 2.1 mode（运行态裁决）

**类型：** `string`  
**枚举值：** `"ACTIVE" | "DEGRADED" | "SUSPENDED"`  
**必填：** ✅

**语义：**
- `ACTIVE` - C 正常运行
- `DEGRADED` - C 降级运行（降低控制精度）
- `SUSPENDED` - C 暂停运行

---

### 2.2 control_level（控制级别）

**类型：** `string`  
**枚举值：** `"NONE" | "ASSIST" | "FULL"`  
**必填：** ✅

**语义：**
- `NONE` - 完全禁止控制
- `ASSIST` - 辅助控制（仅建议，不强制）
- `FULL` - 完整控制（正常执行）

---

### 2.3 update_interval_ms

**类型：** `integer`  
**单位：** 毫秒  
**必填：** ✅  
**最小值：** 1  
**典型值：** 33, 50, 100

**语义：**
- C 允许被调度执行的最小时间间隔
- C 不得自行缩短该间隔

---

### 2.4 blocked_by

**类型：** `string | null`  
**必填：** 仅在 `mode != ACTIVE` 时必填

**语义：**
- C 阻断运行的唯一原因标识

**示例值：**
- `"sensor_noise"`
- `"conflict"`
- `"scheduler"`
- `"b_interrupt"`

---

### 2.5 human_reason

**类型：** `string`  
**必填：** ✅

**语义：**
- 人类可读解释
- 用于 trace / Viewer / 审计

---

## 3. B / C 纪律裁定对比（严格对称）

| 项 | B | C |
|----|---|---|
| **核心问题** | 能不能算 | 能不能控 |
| **Gate / Mode** | GateMode | ControlMode |
| **调度** | tick_interval | update_interval |
| **RED** | 不该算却算 | 不该控却控 |
| **DCS 目标** | 防预测越权 | 防控制越权 |

---

## 4. 未来价值

👉 未来你可以：
- ✅ 用同一套 Viewer 看 B + C
- ✅ 用同一套 DCS 回审整条链路
- ✅ B / C 不再靠"相信工程师"，而靠"可审判运行"

---

## 5. 冻结声明

- ✅ 本文档在 v0.5 生命周期内只读
- ✅ 不允许在实现阶段"边写边改语义"
- ✅ 所有新增能力必须**新开版本 + 新文档**

---

## ✅ 结论

从这一刻开始，B / C 共享同一套"运行纪律语言"。

**RuntimeProfile 是唯一审判对象。**

---

**版本：** v0.5  
**状态：** FROZEN  
**最后更新：** 2025-01-12

# 🛑 BC AUTHORITY GUARD — FINAL (READ-ONLY)

**STATUS**

- **VERSION:** v1.0
- **MODE:** READ_ONLY
- **ALLOW_CHANGES:** NO
- **SOURCE_OF_TRUTH:** YES

---

## 0️⃣ Scope & Sunset（适用范围 / 修订规则）

### Applies ONLY to：

- **B / B2 / Background / Beyond**
- **B ↔ C 交互层**
- **Gate / DTL / DCS / Trace / Timeline**
- **CI / Regression / Audit**

### Does NOT apply to：

- **UI / Web 可视化**
- **离线分析**
- **纯 Demo / Simulation-only 模块**

### Revision Rule（唯一允许修改方式）：

1. **显式架构评审**
2. **版本号升级**（如 v0.5 → v0.6）
3. **使用 DCS 回审 v0.1 → 当前版本全部历史**

---

## 1️⃣ 角色冻结定义（不可更改）

### 🅱️ B（Background / Beyond）

- **B 是 未来风险的提醒者**
- **B 不确认风险**
- **B 不控制行为**
- **B 所有输出 必须是 advisory**

### 🅲 C（Close / Current）

- **C 是 唯一的风险确认者**
- **C 是 唯一的行为执行者**
- **C 允许学习 / 个性化 / 进化**

---

## 2️⃣ Non-Negotiable Violations（不可协商违规）

以下违规 **永远不可放行 / 不可降级 / 不可 A/B**：

- **B 确认风险**（确认性语义）
- **B 直接控制行为**
- **Gate = SUSPENDED 时 B 仍输出**
- **B 在 ≤3m 内输出 NEED_STOP**
- **ENV 因子触发任何行为影响**

➡️ **命中即 `ARCHITECTURE_VIOLATION`**

---

## 3️⃣ B 的唯一合法输出

### 允许的 Impact：

- `NEED_SLOW_DOWN`
- `PATH_UNCERTAIN`
- `NEED_STOP`（仅表示"可能存在高风险"）
- `NO_OP`

### 强制字段：

```python
advisory_only = True
```

---

## 4️⃣ 干预级唯一例外（极限）

B 仅在以下**全部满足**时允许 HARD 提醒：

- Gate = ACTIVE
- distance > 3m
- 高置信度结构性安全风险

### ⚠️ 即便如此：

- **仍是提醒**
- **仍是概率**
- **不确认、不控制**

---

## 5️⃣ Gate 裁决权冻结

| Gate 状态 | B | C |
|-----------|---|---|
| ACTIVE | 可提醒 | 正常 |
| READ_ONLY | 只观察 | 正常 |
| SUSPENDED | 必须沉默 | 正常 |

---

## 6️⃣ 时间 / 坐标冻结

- **B / C 仅使用系统时间**
- **使用统一坐标系**
- **禁止私有时间线**

---

## 7️⃣ 学习 / 进化冻结

| 能力 | B | C |
|------|---|---|
| 行为学习 | ❌ | ✅ |
| 个性化 | ❌ | ✅ |
| 风险确认 | ❌ | ✅ |
| 世界观察 | ✅ | ⚠️（近场） |

---

## 8️⃣ Source of Truth 声明

**BC Authority Guard 是唯一真理源**

**DCS / CI / Lint 只是机械映射**

**若冲突 → 修 DCS，不改 Guard**

---

## 9️⃣ 最终裁定

> **B 永远不是裁判，只是提醒者**  
> **C 才是现实的执行者**

---

**版本：** v1.0  
**最后更新：** 2025-01-12  
**状态：** ✅ FROZEN（只读，不可修改）

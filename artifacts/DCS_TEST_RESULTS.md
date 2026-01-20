# DCS 测试结果报告

**测试日期：** 2025-01-12  
**测试场景：** 60 秒 trace（60 个事件）

---

## 📊 测试结果

### v0.3 RED: **0**
### v0.4.1 RED: **30**
### v0.4.3 RED: **0**

---

## 🔍 详细分析

### v0.3
- **RED: 0**
- **YELLOW: 1** (missing_core_fields)
- **GREEN: 59**

**说明：**
- v0.3 没有 Gate 概念，所以不会触发 `missing_view_state_but_active` 规则
- 但这不代表 v0.3 更安全，而是因为规则设计针对的是"有 Gate 但缺少 view_state"的情况
- v0.3 的"危险"在于：**根本没有 Gate 来阻止它在没有依据时输出**

### v0.4.1
- **RED: 30** (全部是 `missing_view_state_but_active`)
- **YELLOW: 1** (missing_core_fields)
- **GREEN: 29**

**说明：**
- 50% 的事件（30 个）缺少 view_state 但 Gate 是 ACTIVE
- 这正好符合 v0.4.1 的问题：**有 Gate 但 fallback 默认 ACTIVE，缺少 view_state 时仍然允许输出**

### v0.4.3
- **RED: 0**
- **YELLOW: 1** (missing_core_fields)
- **GREEN: 59**

**说明：**
- 所有事件都有 view_state
- Gate 正常工作，不会在缺少 view_state 时进入 ACTIVE
- **v0.4.3 是否还有 missing_view_state_but_active: 否**

---

## 🎯 关键结论

### v0.4.3 是否还有 missing_view_state_but_active: **否**

v0.4.3 的所有事件都有 view_state，Gate 正常工作，不会触发 `missing_view_state_but_active` 规则。

### 最危险一代（直觉）：**v0.4.1**

**原因：**
- v0.3 虽然危险，但它"不知道自己危险"（没有 Gate）
- v0.4.1 有 Gate，但**在缺少 view_state 时仍然允许输出**，这是"知道自己应该检查但没检查"的状态
- 这种"有规则但不遵守"的状态，在实际系统中更容易造成事故

**但更准确的说法是：**
- **v0.3 最危险**（没有 Gate，没有检查机制）
- **v0.4.1 次危险**（有 Gate 但 fallback 默认 ACTIVE）
- **v0.4.3 最安全**（有 Gate 且正常工作）

---

## 📈 危险消退曲线

```
v0.3:  ████████████████████  (没有 Gate，无法检测)
v0.4.1: ████████░░░░░░░░░░  (有 Gate 但 fallback 默认 ACTIVE)
v0.4.3: █░░░░░░░░░░░░░░░░░  (Gate 正常工作)
```

**关键观察：**
- v0.3 → v0.4.1：引入了 Gate，但暴露了 fallback 问题（RED 从 0 跳到 30）
- v0.4.1 → v0.4.3：修复了 fallback 问题，RED 归零

---

**版本：** v0.4.3  
**最后更新：** 2025-01-12

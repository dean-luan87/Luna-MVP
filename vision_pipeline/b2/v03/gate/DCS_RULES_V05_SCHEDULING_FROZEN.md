# v0.5 DCS Rules – Gate Runtime Scheduling（冻结版）

**Status：** FROZEN / READ-ONLY  
**版本：** v0.5  
**日期：** 2025-01-12

---

## 📋 规则定位

本规则集只审判一件事：

> **Gate 说了什么，B 有没有照做。**

---

## 0. 规则适用范围

- ✅ **适用版本：** B2 v0.5+
- ✅ **适用对象：** Gate Runtime Profile × B 实际行为
- ❌ **不适用于：**
  - v0.4.x（不具备完整 runtime_profile）
  - B 的语义输出（impact / decision）
  - C 的导航与确认逻辑

---

## 1. RED 级规则（致命违规）

一旦触发，系统行为不可接受，必须阻断合并 / 上线

---

### 🔴 R1. gate_suspended_but_b_executed

**判定条件：**
```
gate_mode == SUSPENDED
AND
B 执行了任意感知 / 判断 / 输出逻辑
```

**违规含义：**
- Gate 已明确禁止运行
- B 仍在"偷偷干活"

**严重性：**
- ❌ 架构越权
- ❌ 调度系统失效

---

### 🔴 R2. compute_none_but_output_exists

**判定条件：**
```
runtime_profile.compute_level == NONE
AND
存在任何 B summary / impact / trace 输出
```

**违规含义：**
- Gate 已裁定"完全不运行"
- B 仍产生行为或结果

---

### 🔴 R3. tick_rate_override_by_b

**判定条件：**
```
B 实际 tick 频率 < runtime_profile.tick_interval_ms
```

**违规含义：**
- B 擅自提高运行频率
- 绕过 Gate 的算力与节奏控制

---

### 🔴 R4. future_probe_enabled_in_v05

**判定条件：**
```
runtime_profile.allow_future_probe == true
```

**违规含义：**
- v0.5 明确禁止未来预演
- 提前开启未授权能力

---

### 🔴 R5. gate_profile_missing

**判定条件：**
```
B trace / runtime 中缺失 gate_runtime_profile
```

**违规含义：**
- Gate 调度结果未进入可审计系统
- 等同于"无 Gate 运行"

---

## 2. YELLOW 级规则（高风险但可接受）

系统允许运行，但必须进入观察 / 调优清单

---

### 🟡 Y1. read_only_but_heavy_compute

**判定条件：**
```
gate_mode == READ_ONLY
AND
runtime_profile.compute_level == FULL
```

**解释：**
- 只读模式却跑满算力
- 不违规，但浪费资源 / 风险升高

---

### 🟡 Y2. tick_interval_too_dense

**判定条件：**
```
tick_interval_ms < 30ms
AND
持续时间 > 1s
```

**解释：**
- 接近或超过逐帧运行
- 可能导致功耗或稳定性问题

---

### 🟡 Y3. gate_blocked_reason_missing

**判定条件：**
```
gate_mode != ACTIVE
AND
blocked_by == null
```

**解释：**
- Gate 阻断但未说明原因
- 可审计性不足

---

## 3. GREEN 判定标准（显式合规）

以下条件全部满足：

1. ✅ gate_mode 与 B 行为一致
2. ✅ compute_level 与实际算力匹配
3. ✅ tick_interval_ms 被严格遵守
4. ✅ allow_future_probe == false
5. ✅ 所有 Gate 状态均可在 trace 中回放

---

## 4. DCS 输出结构建议（不强制）

```json
{
  "dcs_gate_summary": {
    "red": 0,
    "yellow": 1,
    "green": 128,
    "violations": ["read_only_but_heavy_compute"]
  }
}
```

---

## 5. 与现有 DCS 的关系

| 层级 | v0.4.x | v0.5 |
|------|--------|------|
| 行为越权 | ✅ | ✅ |
| 语义越权 | ✅ | ✅ |
| 调度越权 | ❌ | ✅（新增） |
| 算力审计 | ❌ | ✅ |
| 频率审计 | ❌ | ✅ |

---

## 6. 冻结声明

- ✅ 本规则集**只增不改**
- ✅ 新调度能力 → 必须：
  1. 新版本号
  2. 新 DCS 规则文件
- ✅ 不允许通过"默认值""fallback"绕过判定

---

## ✅ 最终结论

v0.5 的安全不来自"更聪明"，而来自"更守规矩"。

DCS 的职责是：
> **让任何越过 Gate 调度权力的行为，都无处藏身。**

---

**版本：** v0.5  
**状态：** FROZEN  
**最后更新：** 2025-01-12

# B2 v0.5 下一步选项

**版本：** v0.5  
**状态：** 规范已冻结  
**日期：** 2025-01-12

---

## ✅ 已完成的工作

### 1. Gate Runtime Profile 规范文档（冻结版）

- ✅ `vision_pipeline/b2/v03/gate/GATE_RUNTIME_PROFILE_V05_FROZEN.md`
- ✅ `docs/architecture/GATE_RUNTIME_PROFILE_V05_FROZEN.md`
- ✅ `vision_pipeline/b2/v03/V05_GATE_RUNTIME_PROFILE_FROZEN.md`

**文档状态：** FROZEN / READ-ONLY

---

## 🚀 下一步选项

### 选项 A：直接基于本规范输出 v0.5 Scheduler 最小 patch

**目标：**
- 实现 `runtime_profile` 结构
- 在 `tick()` 中接入 `compute_level` 和 `tick_interval_ms`
- 不引入新能力，只做调度控制

**包含内容：**
- Gate 评估器返回 `runtime_profile`
- B2 根据 `compute_level` 决定执行强度
- B2 根据 `tick_interval_ms` 控制执行频率
- 最小 patch，不破坏 v0.4.3 基线

---

### 选项 B：补一份 v0.5 的 DCS 新规则清单（只针对调度违规）

**目标：**
- 添加 v0.5 特有的 DCS 规则
- 针对调度违规的自动检测
- 集成到现有 DCS 评估器

**包含内容：**
- `gate_mode = SUSPENDED` 但 B 仍执行逻辑 → RED
- `compute_level = NONE` 但 B 仍产出 summary → RED
- `allow_future_probe = true`（v0.5 禁止）→ RED
- B 自行修改 tick 频率，无视 Gate profile → RED

---

## 📋 建议顺序

1. **先做选项 B**（DCS 新规则清单）
   - 确保有规则约束，防止实现走样
   - 规则先行，实现后行

2. **再做选项 A**（v0.5 Scheduler 最小 patch）
   - 在规则约束下实现
   - 确保实现符合规范

---

**版本：** v0.5  
**最后更新：** 2025-01-12  
**状态：** 等待选择下一步

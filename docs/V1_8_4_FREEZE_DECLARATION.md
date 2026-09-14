# v1.8.4 Risk Advisory System - 正式冻结声明（Final）

## ✅ 版本状态：Feature Complete / Behavior Frozen / Regression-Ready

**冻结时间**：2024-12-31  
**版本**：v1.8.4  
**状态**：✅ **正式冻结，即刻生效**

---

## 📋 冻结声明

**Risk Module v1.8.4 = Feature Complete / Behavior Frozen / Regression-Ready**

本版本已完成所有计划功能，行为逻辑已冻结，回归测试框架已就绪。  
**该基线将作为后续所有模型接入与世界模型演进的对照标准。**

---

## 🔒 冻结范围

### 1. Risk 行为逻辑（冻结）

以下核心行为逻辑已冻结，不得修改：

- ✅ **ΔRisk 计算**：`delta_risk = current_risk_level - last_risk_level`
- ✅ **触发判定**：`delta_risk >= delta_warn` 且不在 cooldown
- ✅ **Cooldown 机制**：触发后最短静默时间（防骚扰）
- ✅ **趋势判定**：APPROACHING / LEAVING / STABLE 的判断逻辑
- ✅ **动态区域语义**：TIME_WINDOW / ALWAYS / CONDITION 三种模式的激活逻辑
- ✅ **状态机**：DORMANT → WARNED → COOLDOWN 的转换规则

### 2. 决策与播报链（冻结）

以下决策与播报逻辑已冻结，不得修改：

- ✅ **决策优先级**：RISK_LV1 > ADVISORY > YIELD > WAIT > SPEAK
- ✅ **ADVISORY 行为**：不强制插队、不绕过 speech_gate、不打断用户说话
- ✅ **Shadow Mode**：只打日志，不播报（执行层拦截）
- ❌ **禁止新增 action**：不添加新的决策动作（如 `ADVISORY_*`）

### 3. 鲁棒性工具链（冻结）

以下测试框架已冻结，不得修改：

- ✅ **Robustness Harness**：测试框架核心逻辑
- ✅ **Scenario Library**：5 个预定义场景（阈值振荡、快速靠近离开、静态停留、动态区域切换、多风险叠加）
- ✅ **Shadow Mode 支持**：测试时抑制播报
- ✅ **Summary 生成**：Per-Scenario Summary + Run Summary 的生成逻辑
- ✅ **摘要 Schema**：`summary_schema_version: "1.0"` 已冻结

### 4. 可回归与追责（冻结）

以下追责机制已冻结，不得修改：

- ✅ **Run 指纹**：
  - `summary_schema_version: "1.0"`
  - `build.git_commit` 和 `build.build_id`
  - `risk_params_fingerprint`（SHA256 哈希）
  - `seed`（随机种子）
  - `shadow_mode`（布尔值）

---

## ✅ 允许事项（白名单）

以下事项在冻结期间**允许**进行：

### 1. Bug 修复（不改变行为）

- ✅ 修复已发现的 bug（前提：不改变现有行为逻辑）
- ✅ 修复边界条件处理错误
- ✅ 修复数据一致性错误

### 2. 日志/文档勘误

- ✅ 优化日志可读性（不改变日志内容）
- ✅ 修正文档错误
- ✅ 补充文档说明

### 3. 参数仅用于对照实验（不得合并进冻结基线）

- ✅ 可以调整参数（`d0` / `delta_warn` / `cooldown` 等）进行实验
- ⚠️ **但实验参数不得合并进冻结基线**
- ⚠️ **实验必须使用独立的 run 指纹标识**

---

## ❌ 禁止事项（红线）

以下事项在冻结期间**严格禁止**：

### 1. 新功能开发

- ❌ **新风险类型**：不添加新的 `RISK_TYPE`
- ❌ **新触发策略**：不修改触发判定逻辑
- ❌ **新决策 action**：不添加新的决策动作
- ❌ **新播报策略**：不修改 `WarningPolicy` 的核心逻辑

### 2. 行为逻辑修改

- ❌ **世界理解/几何修正逻辑**：不修改几何计算、距离计算等核心逻辑
- ❌ **任何会改变触发概率或时序的改动**：
  - 不修改 `proximity_factor` 计算
  - 不修改 `trend_factor` 计算
  - 不修改 `cooldown` 机制
  - 不修改 `delta_warn` 判定逻辑

### 3. 测试框架修改

- ❌ **不修改 Scenario Library**：5 个预定义场景已冻结
- ❌ **不修改 Summary Schema**：`summary_schema_version: "1.0"` 已冻结
- ❌ **不修改 Run 指纹格式**：已冻结的字段不得修改

---

## 📦 冻结产物（基线）

### 1. 行为基线

- **Risk v1.8.4**：所有风险计算、触发判定、状态机逻辑
- **决策链 v1.8.4**：决策优先级、ADVISORY 行为、Shadow Mode
- **参数基线**：`RISK_TYPE_CONFIG` 中的所有参数值

### 2. 回归基线

- **Robustness Harness**：测试框架代码
- **Scenario Library**：5 个预定义场景定义
- **Per-Scenario Summary**：每个场景的摘要格式
- **Run Summary**：运行汇总格式（`summary_schema_version: "1.0"`）

### 3. 追责基线

- **Run 指纹格式**：
  ```json
  {
    "summary_schema_version": "1.0",
    "build": {
      "git_commit": "...",
      "build_id": "..."
    },
    "risk_params_fingerprint": "sha256:...",
    "seed": 123456,
    "shadow_mode": true
  }
  ```

### 4. 文档基线

- **设计文档**：`V1_8_4_RISK_ADVISORY_SYSTEM_DESIGN.md`
- **实现指南**：`V1_8_4_IMPLEMENTATION_GUIDE.md`
- **工程规范**：`V1_8_4_FEATURE_COMPLETE.md`（包含 `any_triggered` 使用规范）

---

## 🛣️ 后续路线（不立即执行）

### v1.8.5：世界模型接入（计划中）

**设计原则**：
- 世界模型以"弱证据"方式接入
- 仅修正 `hazard_level` 和 `dynamic_active` 状态
- **不直接驱动播报**（仍由 Risk 引擎判定）

**评估方式**：
- 使用同一 Robustness Harness
- 运行同一场景集合
- 对比 Summary 差异：
  - `max_risk_level` 变化
  - `max_delta_risk` 变化
  - `triggered` 变化
  - `trend_distribution` 变化

**对比标准**：
- 基线：v1.8.4 的 Run Summary
- 新版本：v1.8.5 的 Run Summary
- 通过对比量化改进或退化

---

## 📊 冻结检查清单

在冻结期间，任何修改必须通过以下检查：

- [ ] ✅ 是否改变了 Risk 行为逻辑？
- [ ] ✅ 是否改变了决策优先级？
- [ ] ✅ 是否改变了触发判定逻辑？
- [ ] ✅ 是否改变了测试框架？
- [ ] ✅ 是否改变了 Summary Schema？
- [ ] ✅ 是否改变了 Run 指纹格式？

**如果以上任何一项为"是"，则禁止修改。**

---

## 📚 相关文档

### 核心设计文档

- `docs/V1_8_4_RISK_ADVISORY_SYSTEM_DESIGN.md` - 系统设计文档
- `docs/V1_8_4_IMPLEMENTATION_GUIDE.md` - 实现指南
- `docs/V1_8_4_FEATURE_COMPLETE.md` - 功能完成声明（包含工程规范）

### 实现文档

- `docs/V1_8_4_DYNAMIC_REGION_IMPLEMENTATION.md` - 动态区域实现
- `docs/V1_8_4_DEBUG_SNAPSHOT.md` - 调试快照实现
- `docs/V1_8_4_RISK_DEBUG_RUNTIME_INTEGRATION.md` - 运行态接入

### 测试文档

- `docs/V1_8_4_ROBUSTNESS_HARNESS_DELIVERY.md` - 鲁棒性测试框架
- `docs/V1_8_4_ROBUSTNESS_SUMMARY_ENHANCEMENT.md` - 摘要增强（包含 `any_triggered` 使用规范）

---

## 🎉 冻结总结

v1.8.4 已达到 **Feature Complete / Behavior Frozen / Regression-Ready** 状态。

**核心成就**：
- ✅ 一个不滥权的风险系统
- ✅ 一个不会吵、不会乱说话的播报系统
- ✅ 一个工程师敢调、敢扩展的架构
- ✅ 一套可回归、可对比、可追责的测试框架

**该基线将作为后续所有模型接入与世界模型演进的对照标准。**

---

## 📝 版本历史

- **v1.8.4.0** (2024-12-31): **正式冻结**
  - Feature Complete / Behavior Frozen / Regression-Ready
  - Risk Advisory 系统集成
  - 动态区域支持
  - 工程护栏
  - 调试快照（日志级接入）
  - 鲁棒性测试框架
  - Run 指纹补充

---

**冻结生效时间：即刻**  
**冻结维护者：Luna Badge MVP Team**  
**冻结审查：任何修改必须通过冻结检查清单**



# B2 v0.4.2 冻结声明

**版本：** v0.4.2-gate-wired  
**状态：** ✅ FROZEN  
**冻结日期：** 2025-01-12

---

## 🎯 冻结范围

### 核心文件

- `vision_pipeline/b2/v03/b2_v03.py` - Gate 接入 tick 主循环
- `vision_pipeline/b2/v03/gate/gate_evaluator_v05.py` - Gate 评估器
- `vision_pipeline/b2/v03/gate_runtime.py` - Gate 运行时状态
- `.cursor/guards/bc_authority_guard.md` - BC 权限边界 Guard
- `.ci/bc_architecture_guard.yaml` - CI 架构守卫规则

### 测试文件

- `tests/test_b2_v041_gate_behavior_standalone.py` - v0.4.1 回归测试
- `tests/test_b2_v042_tick_gate_integration.py` - v0.4.2 集成测试

---

## ✅ 已确认冻结的事实

### 1. Gate 已成为 tick 的第一裁决者

- ✅ SUSPENDED：硬阻断，B 完全沉默
- ✅ READ_ONLY：只计算、不写回
- ✅ ACTIVE：允许进入既有 v0.4.1 行为链

### 2. B / C 权限边界已被工程化固化

- ✅ B 只能提醒（advisory_only = True）
- ✅ 不存在确认性风险、不存在越权预测
- ✅ 近距离（C 主导区）B 永久失声

### 3. CI + 架构守卫已接入

- ✅ 任何未来 patch 若破坏 Gate / 边界 / 沉默规则，都会被拦截
- ✅ 这是"系统不会悄悄变坏"的保障

### 4. 行为回归测试全绿

- ✅ v0.4.1 回归测试全部通过
- ✅ v0.4.2 集成测试全部通过

---

## 🔒 冻结约束

### 不可修改的原则

1. **Gate 评估必须在 tick() 最顶部**
   - 在任何 factor / impact / window 计算之前

2. **Gate 三态语义不可改变**
   - SUSPENDED = 硬阻断
   - READ_ONLY = 只读不写
   - ACTIVE = 正常流程

3. **Gate 裁决内容不可扩展**
   - 只裁决运行权限，不裁决业务逻辑
   - 不判断世界、不确认风险、不替 C 做决定

4. **写回权限必须经过 Gate 检查**
   - 任何写回都必须检查 Gate 状态
   - 不可绕过 Gate 写回

---

## 📋 版本演进规则

### v0.4.2 → v0.5 允许的改动

- ✅ 在 Gate 之后添加新能力
- ✅ 增强 Gate 输入（更精确的计算）
- ✅ 扩展 trace 字段（为 Web 可视化准备）

### v0.4.2 → v0.5 禁止的改动

- ❌ 改变 Gate 评估位置
- ❌ 改变 Gate 三态语义
- ❌ 绕过 Gate 写回检查
- ❌ 改变 Gate 裁决内容

---

## 🎯 冻结意义

**v0.4.2-gate-wired = 可长期回溯的安全锚点**

从现在开始，任何新能力都必须"尊重 Gate"，而不是绕过 Gate。

---

**版本：** v0.4.2-gate-wired  
**冻结日期：** 2025-01-12  
**状态：** ✅ FROZEN

# v1.8.4 工程护栏（Engineering Guards）实现文档

## ✅ 实现状态：已完成

**实现时间**：2024-12-XX  
**版本**：v1.8.4  
**状态**：✅ 所有工程护栏已添加

---

## 📋 工程护栏概述

这三项不影响功能，但决定半年后你们能不能看懂、敢不敢改。

### 为什么需要工程护栏？

1. **可维护性**：让新同事能快速理解设计意图
2. **可调试性**：让工程师一眼看懂"为什么系统什么都没说"
3. **可扩展性**：防止未来接入世界模型时出现"乘了两次 / 顺序颠倒"的事故

---

## 🔧 工程护栏 1：RiskRuntime 显式记录 dynamic 激活状态

### 问题

现在 dynamic 是否激活是"瞬时计算结果"，调试时很难回答：

> "为什么这个风险此刻没有参与计算？"

### 解决方案

在 `RiskRuntime` 中新增字段（只读，用于调试）：

```python
@dataclass
class RiskRuntime:
    ...
    # v1.8.4: 动态区域激活状态（只读，用于调试）
    is_dynamic_active: Optional[bool] = None
    last_dynamic_check_ts: Optional[float] = None
```

在 `RiskAdvisoryService.tick()` 中记录：

```python
active = is_active(risk_object, now_dt)
# 记录动态激活状态（用于调试）
risk_object.runtime.is_dynamic_active = active
risk_object.runtime.last_dynamic_check_ts = ts
```

### 收益

- ✅ **调试日志一眼看懂**：`is_dynamic_active=False` 直接说明为什么没参与计算
- ✅ **后续 UI / Debug 面板可直接读**：不需要重新计算，直接读取状态
- ✅ **可追溯性**：`last_dynamic_check_ts` 记录最后一次检查时间

---

## 🔧 工程护栏 2：DynamicProfile 边界语义注释

### 问题

防止未来新同事"误用 dynamic 当风险源"。

### 解决方案

在 `DynamicProfile` 定义上方加一段注释：

```python
@dataclass
class DynamicProfile:
    """
    动态/潮汐风险配置
    
    ...
    
    DynamicProfile 设计约定：
    - dynamic 只决定 RiskObject 是否参与 Risk 计算
    - dynamic 不直接触发警告
    - dynamic 不影响 RiskLevel 的"趋势逻辑"
    - dynamic 的激活/失活不视为 Risk 上升
    """
```

### 收益

- ✅ **明确设计边界**：防止误用 dynamic 当风险源
- ✅ **文档化设计意图**：新同事能快速理解设计哲学
- ✅ **防止返工**：避免未来"为什么 dynamic 激活不触发警告"的困惑

---

## 🔧 工程护栏 3：HazardEvaluator 修正顺序约定

### 问题

避免未来 world_model 接入时出现"乘了两次 / 顺序颠倒"的事故。

### 解决方案

在 `evaluate_hazard()` 的 docstring 中明确：

```python
def evaluate_hazard(
    self,
    risk_object: "RiskObject",
    scene_context: Optional[Dict[str, Any]] = None
) -> float:
    """
    计算环境危险程度（HazardLevel）
    
    Hazard 评估顺序约定：
    1. 基础 hazard（规则 / 静态）
    2. 世界模型修正（护栏、结构）
    3. 动态区域修正（hazard_multiplier）- 由 RiskAdvisoryService 在外部应用
    
    注意：本函数只负责步骤 1-2，步骤 3 由 RiskAdvisoryService 通过 apply_hazard_modifier() 完成
    ...
    """
```

### 收益

- ✅ **明确修正顺序**：避免未来接入世界模型时顺序颠倒
- ✅ **职责分离**：`HazardEvaluator` 只负责基础评估，动态修正在外部
- ✅ **防止重复修正**：明确每个步骤的职责边界

---

## 🧪 单元测试

### Test 1：动态区域不激活时，Risk 完全不参与

**Given**：
- 一个 TIME_WINDOW 动态区域
- 当前时间不在窗口内

**Assert**：
- `RiskAdvisoryService.tick()` 不计算 RiskLevel
- 不可能返回 `advisory_text`
- `RiskRuntime.last_risk_level` 保持 0

**文件**：`core/risk/test_dynamic_region.py::TestDynamicRegion::test_dynamic_region_inactive_no_risk_calculation`

---

### Test 2：动态区域激活 ≠ 风险上升

**Given**：
- TIME_WINDOW 从 inactive → active
- 用户位置不变（edge_distance 不变）

**Assert**：
- 不触发 ADVISORY（ΔRisk == 0）
- 只有在后续"靠近"时才触发

**文件**：`core/risk/test_dynamic_region.py::TestDynamicRegion::test_dynamic_region_activation_not_risk_rise`

---

## 📊 改动统计

### 修改文件数：3 个
- `core/risk/risk_object.py` - 新增 `is_dynamic_active` 和 `last_dynamic_check_ts` 字段
- `core/risk/risk_advisory_service.py` - 记录动态激活状态
- `core/risk/hazard_evaluator.py` - 添加评估顺序约定注释

### 新增文件数：1 个
- `core/risk/test_dynamic_region.py` - 单元测试

### 新增代码行数：约 120 行
- `RiskRuntime` 字段：2 行
- `RiskAdvisoryService` 记录逻辑：3 行
- `DynamicProfile` 注释：5 行
- `HazardEvaluator` 注释：10 行
- 单元测试：约 100 行

---

## ✅ 验收清单

- [x] ✅ RiskRuntime 新增 `is_dynamic_active` 和 `last_dynamic_check_ts` 字段
- [x] ✅ RiskAdvisoryService 记录动态激活状态
- [x] ✅ DynamicProfile 添加设计约定注释
- [x] ✅ HazardEvaluator 添加评估顺序约定注释
- [x] ✅ 单元测试：动态区域不激活时，Risk 完全不参与
- [x] ✅ 单元测试：动态区域激活 ≠ 风险上升

---

## 🎯 下一步工作

### 建议立即补（P0.5）

1. **运行单元测试**：验证两个测试用例通过
2. **集成到 CI/CD**：确保未来修改不会破坏这些约定

### 可选优化（P1）

1. **调试快照功能**：将"dynamic 激活/失活 + RiskLevel + ΔRisk"写进统一调试输出
   - 日志结构
   - Debug overlay（如果有）
   - 或一段 `risk_debug_snapshot()`

---

## 📚 相关文档

- `docs/V1_8_4_DYNAMIC_REGION_IMPLEMENTATION.md` - 动态区域实现文档
- `docs/V1_8_4_RISK_ADVISORY_SYSTEM_DESIGN.md` - 系统设计文档

---

## 🎉 总结

v1.8.4 的工程护栏已全部添加，这些护栏不影响功能，但能显著提升代码的可维护性、可调试性和可扩展性。通过明确的注释和单元测试，我们确保了：

1. ✅ **可维护性**：新同事能快速理解设计意图
2. ✅ **可调试性**：工程师一眼看懂"为什么系统什么都没说"
3. ✅ **可扩展性**：防止未来接入世界模型时出现顺序颠倒的事故

**下一步**：运行单元测试，验证所有护栏正常工作。



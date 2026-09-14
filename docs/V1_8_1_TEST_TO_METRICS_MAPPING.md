# V1.8.1 测试结果 → 指标 → 灰度决策闭环

**版本**: V1.8.1  
**创建日期**: 2025-12-29  
**目标**: 建立测试结果到指标到灰度决策的完整闭环

---

## 一、测试结果如何映射到模块 6 指标

### 映射表

| 测试结果 | 对应指标 | 说明 |
|---------|---------|------|
| TC-02 通过率 | `confirm_success_rate` | CONFIRM 成功率 |
| TC-03 触发次数 | `intervene_trigger_count` | INTERVENE 触发次数 |
| TC-08 触发 | `human_help_trigger_count` | 人工求助触发次数 |
| TC-04 平均轮次 | `avg_confirm_rounds_per_scene` | 平均每场景 CONFIRM 轮数 |

### 重要说明

**测试不是"只看 Pass / Fail"，而是为后续灰度提供数值基线。**

---

## 二、灰度放量决策阈值（建议）

### 进入灰度前必须满足

**保守但安全的阈值**：

- ✅ **TC-06 / TC-07**: 100% 通过（自动化测试）
- ✅ **confirm_success_rate** ≥ 80%
- ✅ **intervene_trigger_count** 无异常飙升
- ✅ **human_help_trigger_count** ≤ 预期上限

### 阈值说明

#### confirm_success_rate ≥ 80%

**含义**: CONFIRM 成功率不低于 80%

**计算方式**:
```
confirm_success_rate = accepted / (accepted + rejected + ignored)
```

**判定**:
- ≥ 80%: 允许进入灰度
- < 80%: 需要优化 CONFIRM 逻辑

---

#### intervene_trigger_count 无异常飙升

**含义**: INTERVENE 触发次数不应异常增加

**计算方式**:
```
intervene_trigger_count = 所有 observer_level == "intervene" 的日志数量
```

**判定**:
- 与基线对比无明显异常: 允许进入灰度
- 异常飙升（> 基线 2 倍）: 需要排查原因

---

#### human_help_trigger_count ≤ 预期上限

**含义**: 人工求助触发次数不应超过预期上限

**计算方式**:
```
human_help_trigger_count = 所有 trigger_reason 包含 "human_assist" / "human_help" / "fallback" 的日志数量
```

**预期上限**:
- 建议: 每 100 次会话 ≤ 5 次人工求助触发
- 超过上限: 需要优化人工求助策略

---

## 三、灰度阶段怎么用这些指标

### 第一周：只看自动化测试

**重点**:
- ✅ TC-06 / TC-07 自动化是否 0 Fail
- ✅ 系统稳定性
- ✅ 回滚等价性

**不看**:
- ❌ 功能体验
- ❌ 用户反馈
- ❌ 业务指标

---

### 第二周：开始看指标曲线

**重点**:
- ✅ `confirm_success_rate` 曲线
- ✅ `intervene_trigger_count` 趋势
- ✅ `human_help_trigger_count` 趋势

**判定**:
- 指标稳定或改善: 继续放量
- 指标恶化: 暂停放量，排查问题

---

### 第三周：才讨论"体验好不好"

**重点**:
- ✅ 用户反馈
- ✅ 业务指标
- ✅ 功能体验

**判定**:
- 体验良好: 全量发布
- 体验不佳: 回滚或优化

---

## 四、指标计算与监控

### 指标计算函数

使用模块 6 的指标计算函数：

```python
from core.observer_mode_metrics import calculate_observer_metrics
from Luna_Badge.core.log_manager import LogManager

# 读取日志
log_manager = LogManager()
logs = log_manager.read_logs()

# 计算指标
metrics = calculate_observer_metrics(logs)

# 检查阈值
if metrics["confirm_success_rate"] >= 0.8:
    print("✅ confirm_success_rate 达标")
else:
    print("❌ confirm_success_rate 不达标，需要优化")
```

### 监控建议

**实时监控**:
- TC-06 / TC-07 自动化测试结果（CI 集成）
- 关键指标趋势（Dashboard）

**定期检查**:
- 每周汇总指标数据
- 对比基线版本
- 评估灰度进度

---

## 五、灰度决策流程

### 决策树

```
开始灰度
  ↓
第一周：自动化测试通过？
  ├─ 否 → 停止灰度，修复问题
  └─ 是 → 继续
      ↓
第二周：指标曲线正常？
  ├─ 否 → 暂停放量，排查问题
  └─ 是 → 继续
      ↓
第三周：体验良好？
  ├─ 否 → 回滚或优化
  └─ 是 → 全量发布
```

### 决策标准

| 阶段 | 判定标准 | 决策 |
|------|---------|------|
| 第一周 | TC-06/TC-07 0 Fail | 继续 / 停止 |
| 第二周 | 指标曲线正常 | 继续放量 / 暂停 |
| 第三周 | 体验良好 | 全量发布 / 回滚 |

---

## 六、示例：灰度决策记录

### 第一周决策记录

**日期**: 2025-12-29  
**阶段**: 第一周  
**判定标准**: TC-06 / TC-07 自动化是否 0 Fail

**结果**:
- ✅ TC-06: 0 Fail
- ✅ TC-07: 0 Fail

**决策**: ✅ 继续灰度

---

### 第二周决策记录

**日期**: 2026-01-05  
**阶段**: 第二周  
**判定标准**: 指标曲线是否正常

**指标数据**:
- `confirm_success_rate`: 0.85 (≥ 0.8) ✅
- `intervene_trigger_count`: 12 (无异常) ✅
- `human_help_trigger_count`: 3 (≤ 5) ✅

**决策**: ✅ 继续放量

---

### 第三周决策记录

**日期**: 2026-01-12  
**阶段**: 第三周  
**判定标准**: 体验是否良好

**评估**:
- 用户反馈: 正面
- 业务指标: 正常
- 功能体验: 良好

**决策**: ✅ 全量发布

---

## 七、总结

### 核心价值

**测试结果 → 指标 → 灰度决策** 形成完整闭环：

1. **测试阶段**: 提供数值基线
2. **灰度阶段**: 监控指标趋势
3. **决策阶段**: 基于数据决策

### 关键原则

- ✅ **第一周只看自动化测试**（TC-06 / TC-07）
- ✅ **第二周开始看指标曲线**
- ✅ **第三周才讨论体验**

---

**最后更新**: 2025-12-29  
**维护者**: V1.8.1 开发团队



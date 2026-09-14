# B/C 边界假设和代码改动清单完成报告

## ✅ 已完成

### 1. B/C Boundary Assumptions (`bc_boundary_assumptions_v1.md`)

**定位：** 边界宪法，不是设计笔记

**核心内容：**
- 7 条已审阅并接受的假设
- 每条假设包含：Assumption、Invariant、Rationale、Status、Revisit Phase
- 文档权威性等同于代码审查要求

**7 条假设：**
1. Frequency Mismatch Is Intentional
2. B Is System-Awakened, Not Self-Driven
3. B Never Confirms Risk, Only Signals It
4. Conservative C Is Acceptable in Early Phases
5. Silence Requires No Immediate Explanation
6. System Time Is the Only Time
7. B and C Evolve Orthogonally

**文档长度：** 173 行

---

### 2. Code Changes (`v04_to_v041_code_changes.md`)

**定位：** 让代码不可能违背这 7 条裁定

**核心内容：**

#### ✅ 必须做的代码改动（5 项）
1. **B Never Confirms Risk** - 移除所有"confirmed/verified/must"语义
2. **Single Intervention Class** - 硬编码 ActionImpact，禁止扩展
3. **NO_OP Must Be Silent** - NO_OP 不写入 timeline
4. **Time Consistency Validation** - B→C 消息加入系统时间，C 侧验证
5. **B Must Not Decide When to Run** - 移除任何 auto-wake/self-trigger 逻辑

#### 🚫 明确禁止的改动（4 项）
1. ❌ 让 B "确认危险"
2. ❌ 让 B 在非安全问题上强制 C
3. ❌ 让 C 向 B 请求"更确定的判断"
4. ❌ 让 B 因为"没变化"而频繁输出

**文档长度：** 267 行

---

## 🎯 关键特点

### 1. 不是靠直觉，而是靠裁定来定义 B/C
- 7 条假设是审阅并接受的
- 不是设计笔记，是边界宪法
- 任何未来变更必须明确引用此文档

### 2. 不是让代码决定边界，而是让边界约束代码
- 代码改动清单明确"必须做"和"禁止做"
- 每个改动都有具体位置和实现方式
- 包含代码审查清单和测试要求

### 3. 给未来的你留下了一份不会走样的设计锚点
- 文档有权威性（等同于安全要求）
- 变更流程明确
- 不可临时违反或"仅用于测试"

---

## 📊 文档位置

- `vision_pipeline/b2/v03/bc_boundary_assumptions_v1.md`
- `vision_pipeline/b2/v03/v04_to_v041_code_changes.md`

---

## 💡 下一步建议

**建议选择：2. 开始把这些裁定逐条映射成 DCS 的硬规则**

**理由：**
1. **自动化保护**：将边界假设映射成 DCS 规则，可以自动检测违反
2. **基础设施已就绪**：DCS 系统已经建立，只需要添加新规则
3. **预防性**：在代码改动之前就建立保护机制
4. **可追溯**：每个 DCS 规则都可以追溯到具体的边界假设

**具体可做：**
- 为每条边界假设创建对应的 DCS 规则
- 更新 `dcs_scorer.py` 添加边界检查
- 更新 `audit_runner.py` 添加边界验证规则
- 确保违反边界假设的代码无法通过 DCS 检查

---

**状态**: ✅ **边界假设文档和代码改动清单已完成**

这两个文档现在作为：
- B/C 边界的宪法级定义
- v0.4.1 代码改动的明确指南
- 未来架构决策的约束条件

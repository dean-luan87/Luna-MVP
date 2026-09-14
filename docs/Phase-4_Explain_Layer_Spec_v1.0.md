# Phase-4 Explain Layer Spec v1.0 (Frozen)

**状态：** Frozen / Non-Control / Explain-Only  
**生效范围：** Risk Phase-3 之后  
**控制权：** 无  
**修改规则：** 仅允许版本号升级，不允许语义扩展

---

## 1. 设计目标（Design Intent）
Phase-4 的唯一目标是将 Risk Phase-3 输出的“趋势信号”，转化为系统可解释、可回放、可对比的说明性产物。  
它的意义是提升：
- 可理解性（Explainability）
- 可审计性（Auditability）
- 可治理性（Governance）

---

## 2. 明确非目标（Non-Goals）
Phase-4 明确不做以下任何事情：
- ❌ 不参与任何形式的裁决
- ❌ 不影响 Authority / Ability / C / BC
- ❌ 不输出动作建议（如 STOP / HOLD / TAKEOVER）
- ❌ 不修改或反馈 Risk Phase-1/2/3 的结果
- ❌ 不引入预测、规划或因果推理

Phase-4 是 Explain / Observe / Diagnose 层，不是 Decision 层。

---

## 3. 系统位置（System Placement）
World Snapshot  
↓  
Risk Phase-1 / Phase-2 / Phase-3  
↓  
Phase-4 Explain Layer  
↓  
DebugView / Report / CI / Human Review

重要约束：
- Phase-4 只能读取
- Phase-4 不允许任何回流

---

## 4. 输入与输出

### 4.1 输入（Read-Only）
Phase-4 只允许读取：
- Risk Phase-3 输出历史：
  - acceleration
  - curvature
  - irreversibility
- 时间戳 / window 信息

禁止读取字段（硬约束）：
- decision
- selected_result
- reason
- authority
- abilities
- c_decision

### 4.2 输出（Explain-Only）
Phase-4 的输出必须满足：
- 结构化
- 只读
- 无控制语义
- 可冻结 schema

---

## 5. 核心模块定义（Frozen）

### 5.1 Module A：Trend Explanation
目的：将 Phase-3 的趋势组合映射为有限、可枚举的解释标签。

输出字段：
```
{
  "explanation_tags": [
    "RISK_ACCELERATION_PERSISTENT",
    "CURVATURE_TOWARD_RISK"
  ],
  "confidence": "HIGH"
}
```

约束：
- 标签集合必须是封闭枚举
- 单次输出标签数量 ≤ N（建议 ≤3）
- confidence 仅表示解释置信度，不表示风险程度

### 5.2 Module B：Episode Segmentation
目的：将连续风险时间线切分为人类可理解的阶段。

标准阶段集合（冻结）：
- SAFE
- BUILD_UP
- CRITICAL
- RECOVERY

输出结构：
```
{
  "episodes": [
    {
      "phase": "BUILD_UP",
      "start_ts": 123456.1,
      "end_ts": 123460.3,
      "dominant_signals": ["INCREASING", "TOWARD_RISK"]
    }
  ]
}
```

约束：
- 仅基于 Phase-3 历史信号
- 不推断未来
- 不输出“是否安全”的结论

### 5.3 Module C：Cross-Run Stability Summary
目的：比较不同运行 / 不同版本下，Phase-3 信号的稳定性变化。

关注变化类型：
- 提前 / 延后
- 放大 / 缩小
- 翻转（INCREASING ↔ DECREASING）

输出原则：
- 只描述“变化”
- 不判断“好 / 坏”
- 不给决策建议

---

## 6. 非控制声明（Non-Control Declaration）
Phase-4 Explain Layer 明确声明：
1. 本层不拥有任何决策权
2. 本层输出不得被用于直接或间接触发系统动作
3. 本层不读取任何决策结果或权限状态
4. 本层输出仅用于解释、审计与回放
5. 任何试图将 Phase-4 输出接入控制链路的行为，均视为架构违规

该声明应作为 runtime invariant / 文档硬约束存在。

---

## 7. 冻结与演进策略
- 本文档为 Spec v1.0（Frozen）
- Phase-4 的任何增强：
  - 只能新增解释标签
  - 不能改变已有语义
- 与情感引擎的映射：
  - 不在本阶段进行
  - 仅保留概念对齐可能性

---

## 8. 当前状态总结
- Phase-4 已定义但未侵入控制系统
- 可独立实现
- 可独立测试
- 可安全冻结

---

## 结论
Phase-4 是系统里最容易失控、但又必须保持克制的一层。  
正因为克制，它才是后续：
- 情感引擎
- 因果解释
- 高阶理解  
最干净、最可复用的基础层。

# Freeze Fixtures 设计规范 v1.0
（System World Snapshots for Freeze Testing）

## 0. 文档定位（非常重要）
本规范定义：
- 什么是 Freeze Fixture
- Freeze Fixture 应该表达什么
- Freeze Fixture 不允许表达什么
- Freeze Fixture 如何用于 Freeze / CI / 回放 / 对比

本规范不包含：
- 任何算法实现
- 任何阈值讨论
- 任何“期望决策结果”的断言

Freeze Fixtures 只描述“世界是什么样子”，不描述“系统应该怎么做”。

## 1. 核心定义

### 1.1 什么是 Freeze Fixture
Freeze Fixture = 一个“被官方认可的、可重复使用的世界状态切片”。

它用于回答一个问题：
在同一个世界事实下，系统未来的演进是否仍然遵守我们已经确认的理解边界？

### 1.2 Freeze Fixture 的工程地位
层级 | 是否使用 Fixture
- B（候选生成） | ✅
- C（本能） | ✅
- BC（裁决） | ✅
- Risk Layer | ✅
- RA-View | ✅
- DebugView | ✅
- CI / Freeze Test | ✅

唯一不允许使用 Fixture 的地方：
- 在线推理
- 实时控制
- 模型训练

## 2. Freeze Fixture 的语义边界（硬约束）

### 2.1 必须包含的语义层
A. 世界事实（World Facts）
- 自身状态（位置 / 速度 / 朝向）
- 已识别对象（位置 / 相对运动）
- 空间结构（区域 / 障碍 / 禁止区）

B. 系统客观状态（System Facts）
- perception_state
- calibration_state
- hardware_state
- gate（PASS / BLOCK）
- 时间戳 / frame_id

C. 上下文（Context）
- context_mode（如 NAVIGATION）
- 场景类型标签（仅描述性）

### 2.2 绝对禁止包含的内容
决策类：
- decision
- selected_result
- reason
- bc_action
- c_decision

权限 / 能力类：
- authority
- abilities
- can_recover
- allow_output

推理 / 评估结果：
- risk_level
- risk_score
- envelope_result
- confidence

Fixture 是事实，不是判断。

## 3. Freeze Fixture 的组织方式

### 3.1 基本结构（概念层）
FreezeFixture
├── meta
│   ├── fixture_id
│   ├── scenario_type
│   ├── description
│   ├── version
│   └── tags
│
├── system_snapshot
│   ├── system_facts
│   ├── self_state
│   ├── perceived_objects
│   └── environment
│
└── model_outputs
    └── candidate_actions (B 的假定候选)

注意：
model_outputs 只是为了让 BC 能完整跑通流程，它们不代表真实模型质量。

## 4. Freeze Fixture 最小集（P0）

### F-01：Clear & Safe World
语义定义：
- 环境开阔
- 无障碍
- 无相对运动
- 感知稳定

目的：
- 验证系统在“绝对安全世界”下不会制造风险
- Authority / Risk / RA-View 不应产生异常信号

标签：
["safe", "baseline", "no_risk"]

### F-02：Static Obstacle Approaching（静止 × 运动）
语义定义：
- 自身在运动
- 前方存在静止障碍 / 禁止区
- 持续逼近

目的：
- 验证 Risk Layer 的 TTC / 静态预测
- 验证“危险提前显形”但不裁决

标签：
["static_obstacle", "ttc", "one_moving"]

### F-03：Dynamic Crossing（双方运动）
语义定义：
- 自身与他人同时运动
- 轨迹在短时间窗口内交叉
- 典型 VO / 相对速度场景

目的：
- 验证 VO / Relative Motion 风险计算
- 验证 RA-View 中 Risk × Authority 的时序关系

标签：
["dynamic", "vo", "crossing"]

### F-04：Perception Unstable World
语义定义：
- perception_state = UNSTABLE
- 世界中仍然存在对象与相对运动
- 非 FAILED

目的：
- 验证 Authority 降级逻辑
- Risk 仍可只读计算
- C 行为是否保守

标签：
["unstable_perception", "degraded"]

### F-05：Hardware Failure World
语义定义：
- hardware_state = FAILED
- 世界事实仍存在（但不可靠）
- gate = BLOCK

目的：
- 验证系统是否“诚实失败”
- C 必须 REQUEST_TAKEOVER
- BC 不得输出行为

标签：
["hardware_failure", "fail_safe"]

## 5. Freeze 测试用这些 Fixtures 测什么？

### 5.1 Freeze 测试不测“正确性”
Freeze 测试不做以下断言：
- “应该停下”
- “应该减速”
- “风险值应为 X”

### 5.2 Freeze 测试只测“不变量（Invariant）”
示例（概念）：
- 同一 Fixture：
  - Risk schema_version 不变
  - DebugView 不包含 decision
  - Authority 不会无理由上升
  - RA-View 的 profile 分类不突变

## 6. Fixture 的版本与演化规则
### 6.1 Fixture 一旦冻结
- 不允许修改语义
- 不允许“悄悄加字段”
- 若必须修改：
  - 新增 fixture_id
  - 明确 deprecated 原 fixture

### 6.2 Fixture 的演化方式
世界会演化，但 Freeze Fixture 不会。

演化应体现在：
- Risk Layer 算法
- Authority 迟滞
- RA-View 解释

而不是修改世界样本。

## 7. 为什么这套设计对你特别重要
Freeze Fixtures 将成为：
- 情感引擎世界模型的最初语义锚点
- 因果系统的对照输入
- 演化算法的稳定基线

## 8. 下一步（明确建议）
1. 把这份文档存为：`docs/Freeze_Fixtures_Design_v1.0.md`
2. 生成 F-01 ~ F-05 的 JSON（不加任何判断字段）
3. 再进入 Freeze pytest 样例 / CI Gate

## Freeze Gate（Release Only）
Freeze tests are enforced as a release gate on the main branch only.
They guarantee world-model immutability and schema stability across releases.

一句总结：
Freeze Fixtures 是系统的“世界宪法附录”。

一期架构冻结文档

Frozen Architecture v1.0

适用范围：BC 自治 × 协同 × Fail-Safe 一期全部工程
状态：FROZEN（未经架构级决策，不得变更）
目标：保证系统在长期运行、升级、异常条件下 不失控、不乱动、不自杀

---

1. 架构总览（文字结构）

Hardware / OS
  ↓
Perception & Drivers
  - Camera / Sensors
  - SLAM / 定位
  - 感知健康度
  ↓
B Module
  - Prediction
  - B Autonomy
      · PROC（内部过程）
      · OUT（输出质量）
      · COLLAB（协同健康）
  ↓
Decision Capability Limiter
  - 基于 B_AutonomyState
  - 收敛 Decision 能力上限
  ↓
D2RG（Decision → Runtime Gate Adapter）
  ↓
Runtime Gate（BCP）
  - 感知稳定性
  - 校准状态
  - Reference 一致性
  - SystemMode
  ↓
Execution Chain
  - 语音 / 行为 / 导航
  ↓
Execution Receipt
  - 执行事实唯一来源
  ↓
B ← ExecutionReceipt
  - 协同退化 / 恢复证据
  ↓
B Snapshot
  - collab_health
  - collab_window_stats
  ↓
System Snapshot
  - system_health
  - recommended_action
  ↓
Policy Layer（Auto Fail-Safe）
  ↓
System Mode Controller
  - RUNTIME_STABLE
  - FAIL_SAFE

---

2. 核心架构原则（冻结）

2.1 单向因果原则
- 决策 → 执行 → 回执 → 自治 → 汇总 → 策略
- 禁止反向修改历史
- 禁止边执行边改决策

---

2.2 权限边界原则

层级	权限
B 模块	预测、自检、协同退化
决策能力层	限制 Decision 上限
D2RG	适配，不裁决
Runtime Gate	放行 / 阻断
Execution	只执行
Policy Layer	是否进入 Fail-Safe
System Controller	切换 SystemMode

任何模块越权，视为架构违规。

---

2.3 Gate 不可绕过原则
- 所有对外输出 必须经过 Runtime Gate
- Gate 的判定 必须产生 ExecutionReceipt
- 无回执 = 执行非法

---

3. 状态机冻结定义

3.1 B_AutonomyState（一期）

HEALTHY
  ↓
DEGRADED
  ↓
SUSPENDED

- 退化由 Issue / Receipt 驱动
- 恢复必须有执行成功证据
- 不允许跨级恢复

---

3.2 SystemMode（一期）

RUNTIME_STABLE
    ↓
FAIL_SAFE

- FAIL_SAFE 只能由 Policy Layer 触发
- 模块自身不得切换 SystemMode

---

3.3 PolicyState（一期）

NORMAL
  ↓
PENDING_FAIL_SAFE
  ↓
FAIL_SAFE_ACTIVE

- YELLOW 防抖
- RED 立即进入 Fail-Safe

---

4. 冻结运行规则清单（必须写入工程）
1. 感知不稳定 → BC 协同暂停，不产生对外结果
2. 感知恢复 → 必须重新校准，旧预测一律作废
3. 未完成校准 → 禁止进入 Runtime
4. Shadow 决策永不执行
5. ExecutionReceipt 是执行事实唯一来源
6. 执行失败必须反向影响 B 的协同状态
7. B 不裁决执行，只限制能力上限
8. Fail-Safe 只能由策略层触发
9. FAIL_SAFE 状态下系统必须“活着但不动作”
10. 所有状态变化必须可审计、可回放

---

5. 一期能力边界

5.1 一期 必须具备
- B 自治（PROC / OUT / COLLAB）
- Decision 能力收敛
- Runtime Gate 强约束
- Execution Receipt
- 协同退化与恢复
- System Snapshot
- 自动 Fail-Safe

---

5.2 一期 明确不做
- C 高阶自治与策略推理
- Fail-Safe 自动恢复
- 多模型博弈
- 世界模型闭环
- 模型自修改

---

6. 一期禁区（严禁实现）

以下行为 直接判定为架构违规：
- 模块直接调用 Execution
- 模块自行进入 Fail-Safe
- 无 ExecutionReceipt 的执行
- 用 if-else 代替 Runtime Gate
- 用日志代替状态机
- 用经验判断代替证据链

---

7. 可扩展但一期不实现的接口
- C_AutonomyState（完全复用 B 范式）
- Fail-Safe 自动恢复策略
- 多版本 B 并行验证
- 后台实时可视化
- 人工接管接口

---

8. 系统设计哲学（冻结说明）

本系统不是为了“尽可能聪明”，
而是为了在 错误、升级、抖动、失败 中仍然 可控、可解释、可存活。

一期冻结的是 行为边界，不是能力上限。

---

9. 冻结声明

本文档定义的一期架构、状态机、规则与边界
在二期规划完成前不得变更。

所有新增能力，必须在不破坏本冻结文档的前提下扩展。

---

结语（工程直话）

到这一步，你已经完成的不是一个“AI 功能”，
而是一个 可以长期运行、不会靠运气活着的系统骨架。

当你准备好下一步时，最自然的演进是：

二期：C 模块自治，100% 复用这套范式

你只要一句话：
“开始二期规划”
我就继续。

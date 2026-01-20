BC / C 系统运行规格文档

（System Runtime Specification · v1.0）

---

0. 文档声明（Authoritative Notice）

0.1 文档目的

本文档定义 BC / C 系统的新一代运行架构、模块职责、裁决机制与安全边界，用于指导系统实现、演进与治理。

0.2 文档地位
- 本文档优先级 高于任何历史设计文档
- 本文档是 当前系统的权威运行规格
- 历史文档暂不删除，但 不再作为实现依据
- 任一模块或实现如与本文档冲突，视为 架构缺陷

---

1. 系统运行总览（Operating Model）

1.1 核心运行思想

系统的目标不是“最优决策”，而是：

在当下环境中，在不可突破边界内，
选择代价最小、可持续、可执行的行动。

1.2 在线主循环（Online Runtime Loop）

事实输入
   ↓
候选生成（B / C）
   ↓
本能裁决（BC）
   ↓
硬安全 Gate
   ↓
执行
   ↓
事实回执

1.3 横线下系统（Off-Loop）

以下模块 不进入在线裁决链路：
- 评分系统
- 演化系统
- 后台分析
- 管理注入

它们只能：
- 观察
- 归因
- 提出候选修改

不得直接影响在线行为。

---

2. 核心模块职责划分（Role Definition）

2.1 Fact / Environment Model（事实层）

职责
- 提供当下环境的客观定性事实
- 不做策略、不做裁决

输出
- EnvironmentModel（稳定性、风险、可通行性等）

---

2.2 B 模块（认知 / 推理）

职责
- 在环境假设基本成立的前提下
- 生成高质量、可解释的候选行动

禁止行为
- 不判断是否可执行
- 不触碰安全边界
- 不处理塑形与 Override

---

2.3 C 模块（本能 / 反射）

职责
- 在高不确定、失真、紧急情况下
- 提供低依赖、短链路、可立即执行的候选

工程定位
- C 不是 B 的兜底
- 在极端情况下：
C + 语音 + Gate = 最低可用能力（MONC）

---

2.4 BC 模块（本能裁决中枢）

职责
- 汇聚 B / C 候选
- 基于环境进行裁决
- 生成运行态塑形
- 判断是否允许突破软规则

BC 不做
- 候选生成
- 规则演化
- 学习 / 打分
- 模型选择

---

2.5 Gate（硬安全）

职责
- 执行不可突破边界（Hard Boundary）
- 拦截任何越界行为

原则
- Gate 不做策略
- Gate 不优化结果

---

2.6 Execution（执行层）

职责
- 执行被允许的行动
- 返回事实回执

原则
- 不理解规则
- 不理解塑形
- 不理解 Override

---

2.7 Snapshot / Telemetry（观测层）

职责
- 记录一次裁决窗口的事实与结果
- 用于回溯、分析、演化

原则
- 不进入在线链路
- 不反向影响决策

---

3. BC 模块规格（核心章节）

3.1 BC 的工程定位

BC 是在当下环境中，对行动候选进行生存级裁决与动作优化的中枢模块。

---

3.2 BC 输入
- EnvironmentModel
- CandidateActionSet（来自 B / C）
- Hard Boundary Rules
- System Safety Signals

---

3.3 BC 输出
- ArbitrationResult（裁决结果）
- ExecutionDirective（下发给执行层）
- BCSnapshot（事后观测）

---

3.4 BC 内部裁决模型（四件事）

BC 在每一轮裁决中 只做以下四件事：
1. 环境态定性
- NORMAL / DISTORTED / COLLAPSED
2. 候选裁决
- allowed / suppressed / forbidden
3. 行为塑形（Shaping）
- 节律 / 深度 / 权限 / 输出形式
4. 例外授权（Override）
- 是否允许突破软规则或塑形

---

3.5 BC State 状态机

状态定义
- INIT
- OBSERVE
- ACTIVE
- CONSTRAINED
- OVERRIDE
- DEGRADED

核心原则
- 恢复必须经过 OBSERVE
- Override 是短暂态
- DEGRADED 为保命态

---

4. 塑形（Shaping）与 Override 规则

4.1 塑形的本质

塑形是运行态调制，不是规则，不是命令。

约束
- 必须有 TTL
- 不可叠加为永久
- 可被 Override
- 到期自动失效

---

4.2 Override 的本质

Override 是一次性裁决许可，不是新规则。

允许条件
1. 环境前提失效
2. 遵守规则代价反转
3. 不触及 Hard Boundary

约束
- 不继承
- 不记忆
- 不自动演化

---

5. BC → 执行层最小指令集

执行层只接受以下信息：
- allowed_actions
- execution_constraints
- confidence_level
- exceptional_flag
- validity_window

执行层不得缓存，不得推理，不得优化。

---

6. 规则体系与优先级（Rule Hierarchy）

6.1 规则仓分层
1. Hard Boundary（宪法层）
2. Soft Norms（默认遵守，可突破）
3. Shaping Policies（运行调制）
4. External / Backend Policies

6.2 优先级顺序（从高到低）
1. Hard Boundary
2. Authority / Safety State
3. Gate
4. BC Arbitration
5. B / C 候选
6. Execution
7. Snapshot / 演化

---

7. Fail-Safe × 上层失真 × C 接管

7.1 上层失真定义

上层失真 = 决策系统无法维持稳定、可信、可执行的输出状态。

状态：
- NORMAL
- DEGRADED
- FAIL_SAFE

---

7.2 进入 Fail-Safe 的条件
- 上层失真 FAIL_SAFE
- 硬件不可恢复故障
- 连续失败导致不可行动

Fail-Safe 行为
- 最低可用输出或沉默
- 明确告知用户不可用

---

7.3 C 接管语义
- 优先 C 候选
- 禁止长链路推理
- 禁止激进 Override
- 维持最低可用能力（MONC）

---

8. Snapshot / Telemetry 规范

8.1 Snapshot 定位

Snapshot 是裁决的事后留痕，不是反馈通道。

8.2 Snapshot 原则
- 不反向注入
- 不作为实时依据
- 不形成隐性规则

---

9. 工业系统对齐原则（预留）

本系统设计参考：
- 自动驾驶（ODD / Fail-Safe / Authority）
- 航空航天（分级控制 / 最小风险态）

AuthorityLevel × 信号 × BC 能力矩阵
作为下一阶段工作（TBD）。

---

10. 总结性宪章（写死）

系统守护的是“活下来的边界”，而不是规则本身。

规则默认遵守，但在环境前提失效时，
系统允许在不触及宪法边界的前提下，
选择代价最小的可行动作。

---

文档状态
- 状态：冻结（Frozen）
- 后续修改必须：
- 明确标注版本
- 说明变更原因
- 不得隐性演进

---

到这里，这份文档已经是可以直接灌进 Cursor、作为系统最高规格的完整文本。

你下一步如果愿意继续，我们可以基于这份已冻结文档，顺理成章地进入你刚才提到的：

AuthorityLevel × 信号 × BC 能力矩阵

那将是“控制权工程化”的最后一块拼图。

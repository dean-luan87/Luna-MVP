BC / Authority / Soft-Norm 运行宪章

（Runtime Constitution · Engineering Frozen Spec）

适用范围：
- B 模块
- BC 模块
- Authority / 本能规则模块
- C 模块暂不展开自治，仅占位

本文档为 工程最高优先级运行规格。

---

0. 文档地位声明（必须写在最前）
1. 本文档定义系统的运行逻辑、控制权分配与安全边界
2. 本文档 优先级高于所有历史设计文档
3. 与本文档冲突的实现，视为 架构缺陷
4. 本文档冻结后，任何修改必须：
- 明确版本
- 明确修改动机
- 不得隐性演进

---

1. 系统运行总体模型（统一认知）

1.1 核心目标（不是最优）

系统目标不是“最优决策”，而是：

在当前环境下，
在不可突破边界内，
选择代价最小、可持续、可执行的行为。

---

1.2 在线主链路（Online Runtime）

Environment / Fact
        ↓
Candidate Generation (B / C)
        ↓
Authority Resolution
        ↓
BC Arbitration
        ↓
Hard Safety Gate
        ↓
Execution
        ↓
Execution Feedback

---

1.3 横线下系统（Off-Loop，不得入主链）

──────────────
Snapshot / Telemetry
Scoring (User / System / Result)
Evolution / Rule Suggestion
Backend Policy Injection
──────────────

横线下系统不得直接影响在线裁决。

---

2. 模块职责边界（冻结）

2.1 B 模块（认知 / 推理）

职责
- 在环境假设成立前提下
- 生成高质量、可解释的候选行为

禁止
- 不裁决
- 不触碰安全边界
- 不做 Authority 判断
- 不 Override 规则

---

2.2 C 模块（本能 / 反射，占位）

职责
- 在高不确定 / 失真 / 紧急场景下
- 提供短链路、低依赖候选

⚠️ 本阶段 不展开 C 自治设计
仅作为候选来源存在。

---

2.3 BC 模块（本能裁决中枢）

BC 是在当下环境中，对行为候选进行生存级裁决与优化的中枢。

BC 只做四件事：
1. 环境态定性
2. 候选裁决
3. 行为塑形（Shaping）
4. 例外授权（Override）

BC 不学习、不评分、不演化。

---

2.4 Gate（硬安全）
- 执行不可突破边界（Hard Boundary）
- 不做策略
- 不做优化

---

3. AuthorityLevel（控制权）体系

3.1 AuthorityLevel 定义（冻结）

Level	名称	工程语义
A0	Manual	人工全接管
A1	Assisted	系统提示
A2	Supervised Auto	系统主导 + 关键确认
A3	Safe Auto	系统全权（ODD 内）
A4	Fail-Operational	退化但可行动（MONC）
A5	Fail-Safe	最低风险态 / 不可用

---

3.2 Authority 不是模块，是计算结果

AuthorityLevel = resolveAuthority(SystemSnapshot)

- Authority 是 纯函数结果
- 不允许模块私改
- 不允许在线学习

---

3.3 Authority 上限计算（冻结映射）

条件（任一命中）	Authority 上限
Hardware FAULT	A5
Calibration FAILED	A5
ControlDistortion = FAIL_SAFE	A5
Perception UNSTABLE（持续）	A4
ControlDistortion = DEGRADED	A4
Risk = HIGH & 非 SURVIVAL	A2
Risk = HIGH & SURVIVAL	A4
全部正常	A3

最终 Authority：

Authority = min(SystemUpperBound, UserAuthorityCap)

---

3.4 Authority → BCState 映射

Authority	BCState
A3	ACTIVE
A2	CONSTRAINED
A4	DEGRADED
A5	FAIL_SAFE
A1 / A0	OBSERVE

---

4. Authority × BC 能力裁剪（写死）

4.1 BC 能力拆分（标准）

BCAbilities {
  arbitration
  shaping
  override
  source_B
  source_C
  future_reasoning
}

---

4.2 Authority × 能力矩阵（冻结）

Authority	Arb	Shape	Override	B	C	Future
A3	✓	✓	⚠️	✓	✓	✓
A2	✓	✓(限)	⚠️(确认)	✓	✓	⚠️
A1	⚠️	✗	✗	✗	✓	✗
A4	✓(最小)	✓(tempo)	⚠️(生存)	✗	✓	✗
A5	✗	✗	✗	✗	✗	✗

---

5. Soft Norm（软规则）体系

5.1 Soft Norm 定义

Soft Norm 是 默认环境假设下的行为偏好，不是对错。

---

5.2 Soft Norm 分类（冻结）

SoftNormType =
  ABSOLUTE_FORBIDDEN   // 等同硬边界
  DEFAULT_PREFERRED    // 默认遵守，可突破
  CONTEXTUAL_OPTIONAL  // 情境启用

---

5.3 Soft Norm × Authority × Override

NormType	A3	A2	A4
ABSOLUTE_FORBIDDEN	❌	❌	❌
DEFAULT_PREFERRED	⚠️	⚠️(确认)	✓
CONTEXTUAL_OPTIONAL	✓	✓	✓

---

5.4 Override 触发条件（必须全部满足）
1. 当前环境前提失效
2. 突破规则代价 < 遵守规则代价
3. 不触及 ABSOLUTE_FORBIDDEN
4. Authority ∈ {A3, A4}

---

5.5 Override 生命周期（防锁死）

Trigger → Apply → Execute → Expire

- 不继承
- 不叠加
- 不写入长期塑形
- 必须记录 Snapshot

---

6. 塑形（Shaping）原则
- 塑形是 运行态调制
- 必须有 TTL
- 自动失效
- 可被 Override
- 不等同规则

---

7. Fail-Safe 与 C 接管语义

7.1 上层失真定义

决策系统无法维持稳定、可信、可执行输出。

状态：
- NORMAL
- DEGRADED
- FAIL_SAFE

---

7.2 Fail-Safe 行为（冻结）
- 停止裁决
- 明确告知用户
- 不假装工作

---

7.3 A4 Fail-Operational（MONC）
- C 候选优先
- 短链路
- 不做长期判断
- 保证最低可用能力

---

8. Snapshot / Telemetry（只观察）
- Snapshot 仅记录
- 不反向注入
- 不形成隐性规则
- 为评分 / 演化提供事实

---

9. 演化 / 评分系统的位置（冻结）
- 不进入在线链路
- 不控制 BC
- 只能提出建议

评分来源：
- 用户
- 系统
- 实际结果

原则：
- 单次评估无裁判权
- 时间累计生效
- 个体最优 ≠ 全局最优

---

10. 冻结结论（写死）

系统守护的是 可存活的边界，
不是规则本身。

除宪法级规则外，
所有规则在满足条件时
都允许被突破。

---

文档状态
- 状态：Frozen
- 作为工程改造基线使用

---

下一步工程节奏（给你对齐用）
1. 不动 C 自治
2. 先改 B 模块接口（对 Authority / SoftNorm 友好）
3. 重构 BC 裁决入口（Authority → 能力裁剪 → 裁决）
4. C 模块在 BC 改造完成后再优化

---

如果你愿意，下一步我可以直接做三件事之一（你选）：
1. 把这份文档拆成 B / BC 的工程 TODO 清单
2. 给出 BC 裁决入口的伪代码 / 接口骨架
3. 对照你现有工程，列“必改 / 可延后 / 暂不动”清单

你现在这一步做得非常对，先立宪，再施工。

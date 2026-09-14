B 模块自治处理动作表

B_AutonomyState → Action Mapping

这张表回答且只回答一个问题：
“当 B 处于某个自治状态时，它必须做什么、必须不做什么。”

---

一、设计前提（先写死）
1. 自治动作只作用于 B 自身
2. 自治动作不得直接影响对外输出
3. 所有动作都是“能力收敛”，不是“系统裁决”
4. 动作必须是可撤销、可恢复、可审计的

---

二、B_OverallState 定义回顾（对齐）

B_OverallState =
  HEALTHY
  DEGRADED
  SUSPENDED
  UNAVAILABLE

---

三、核心自治处理动作维度（统一动作原语）

为避免“状态一多动作就乱”，先冻结动作原语集合：

AutonomyActions =
  A1: NORMAL_OPERATION        // 正常运行
  A2: REDUCE_OUTPUT_RATE      // 降低输出频率
  A3: RAISE_UNCERTAINTY       // 提高不确定性标注
  A4: DISABLE_PARTIAL_OUTPUT  // 禁用部分预测类型
  A5: STOP_PREDICTION         // 停止预测
  A6: EXIT_COLLABORATION      // 主动退出 BC 协同
  A7: SELF_RECOVERY_ONLY      // 仅允许自恢复

⚠️ 冻结原则：
不允许出现“状态 → 模糊行为描述”
每个状态只能映射到这些动作原语的组合。

---

四、自治处理动作总表（冻结）

4.1 B_OverallState → Actions

B_OverallState    允许的自治动作          明确禁止的行为
HEALTHY           A1                      禁止任何能力收敛
DEGRADED          A2 + A3                 禁止新增预测类型
SUSPENDED         A4 + A6                 禁止参与 BC 协同
UNAVAILABLE       A5 + A6 + A7            禁止产生任何预测

---

五、逐状态精确定义（不可歧义）

🟢 HEALTHY

语义
- B 模块完全可信
- 所有预测能力可用

必须执行
- 正常频率输出
- 正常置信度计算

禁止
- 主动降级
- 自我限制能力

---

🟡 DEGRADED

语义
- B 仍可工作，但稳定性或质量存在风险
- 必须“谨慎发言”

必须执行
- 降低预测输出频率（A2）
- 提高不确定性标注（A3）

允许
- 保留核心预测能力
- 持续生成 Issue

禁止
- 新增或实验性预测
- 扩大输出覆盖范围

---

🔴 SUSPENDED

语义
- B 当前不适合参与系统协同
- 单独运行也可能带来风险

必须执行
- 禁用部分或全部预测类型（A4）
- 主动退出 BC 协同（A6）

允许
- 内部运行
- 生成自治 Issue
- 参与 Shadow / 自检流程

禁止
- 提供任何可被系统采纳的预测
- 参与 Runtime 决策路径

---

⚫ UNAVAILABLE

语义
- B 被视为不可用
- 所有对外价值暂停

必须执行
- 停止所有预测（A5）
- 退出所有协同（A6）
- 仅允许自恢复流程（A7）

允许
- 心跳
- 自检
- 恢复尝试

禁止
- 任何形式的信息生产
- 任何形式的协同行为

---

六、子状态对自治动作的影响（补充规则）

6.1 InternalProcessState 的直接影响

FAILED → 强制 UNAVAILABLE

---

6.2 OutputQualityState 的直接影响

INVALID → 至少 SUSPENDED

---

6.3 CollaborationState 的直接影响

COLLAB_SUSPENDED → 至少 SUSPENDED

---

七、状态恢复时的动作撤销规则（非常重要）

冻结恢复原则
1. 动作只能逐级撤销
2. 恢复路径与降级路径对称
3. 禁止“一步恢复全部能力”

示例恢复路径

UNAVAILABLE
 → (自检通过)
SUSPENDED
 → (观察期)
DEGRADED
 → (稳定窗口)
HEALTHY

对应动作逐步撤销：

A5/A6/A7
 → A4/A6
 → A2/A3
 → A1

---

八、动作执行的工程要求（必须写进实现）
- 每次状态变化 → 明确记录：
- State before / after
- Applied actions
- Triggering IssueCodes
- 动作执行 不可异步失败
- 动作失败 = 新 Issue（Process 类）

---

九、为什么这张表是“自治核心”

因为从这一刻开始：
- Issue 是输入
- B_AutonomyState 是中间态
- Action 是唯一允许的输出

不再允许“看情况处理”。

---

十、一句话冻结总结（可写入文档）

B 模块自治通过将自治状态映射为一组严格受限的能力收敛动作，
在不依赖系统裁决的前提下，确保任何异常情况下
“宁可不输出，也不误导”。

---

下一步自然衔接（不推进）

下一步逻辑上只剩两件事之一：
1. 定义 B 模块 IssueCode 目录（B-PROC / B-OUT / B-COLLAB）
2. 定义 Autonomy Heartbeat Monitor 的接口规范

你点哪一个，我就直接落成规范。

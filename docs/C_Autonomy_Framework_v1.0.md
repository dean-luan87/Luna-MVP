C 模块自治规范

C Autonomy Framework v1.0（Frozen）

0. 定位与边界（写死）
- C 是系统裁决者/放行者，自治目标：任何情况下不做不该做的事。
- 自治是自律与收敛，不是扩权；不得绕过 BCP Runtime Gate。
- C 自治的输出只能影响：
- C 自己是否参与协同
- C 自己的决策强度与输出策略（保守化/停止放行）
- C 自治不得直接替代系统态机（SystemMode 仍由系统层裁决），但可发出建议/事件。

---

1. 自治拆分（与你的习惯一致）

1.1 对内自治（Internal）

关注 C 自己的信息生产/裁决能力是否正常：
- 是否还能计算裁决
- 裁决链路是否一致、可解释
- 是否出现异常、卡死、资源问题、状态损坏

1.2 对外自治（External）

关注 C 与外部协同是否正常（B、系统态、输出执行链）：
- 与 B 的 Reference/时间/版本一致性
- 是否能接收 B 输出与回执
- 是否能调用 Runtime Gate 并获得一致结果
- 与执行链（语音/提示/导航）之间的调用与反馈是否正常

---

2. 四级监督结构（与 B 同构）

C 的自治监督分为四级（聚合进入检测模块+日志后台）：
1. 工作过程监督（PROC）：裁决流程是否正常运行
2. 结果产出监督（OUT）：裁决产物是否结构/语义可接受（不等于正确）
3. 自治问题处理机制（Issue Handling）：像错误码一样描述、分级、处理
4. 协同监督（COLLAB）：与 B/系统态/Runtime Gate/执行链 协同是否正常

---

3. C_AutonomyState 状态机（Issue 聚合 → State）

3.1 子状态（内部使用）

C_InternalProcessState = OK | WARNING | DEGRADED | FAILED
C_OutputQualityState   = OK | SUSPICIOUS | INVALID
C_CollaborationState   = COLLAB_OK | COLLAB_DEGRADED | COLLAB_SUSPENDED

3.2 对外总态（系统只看这个）

C_OverallState =
  HEALTHY        // 可裁决、可放行（仍受 BCP 约束）
  DEGRADED       // 仍可裁决，但强制保守化
  SUSPENDED      // 暂停参与 BC 协同（不放行）
  UNAVAILABLE    // 不可用，仅允许自恢复

3.3 聚合规则（冻结）
- 同域子状态取最坏值：
- OK < WARNING < DEGRADED < FAILED
- OK < SUSPICIOUS < INVALID
- COLLAB_OK < COLLAB_DEGRADED < COLLAB_SUSPENDED
- 总态映射（冻结原则）：
1. 任一 FAILED/INVALID/COLLAB_SUSPENDED ⇒ 至少 SUSPENDED
2. 结构性违规重复 ⇒ UNAVAILABLE
3. 恢复必须逐级，不可跨级跳回 HEALTHY

建议映射表（与 B 同构，C 的“更保守”体现在动作表，不在状态表里）：

Process	Output	Collab	C_Overall
OK	OK	OK	HEALTHY
WARNING/DEGRADED	OK	OK	DEGRADED
OK	SUSPICIOUS	OK	DEGRADED
*	INVALID	*	SUSPENDED
FAILED	*	*	SUSPENDED
*	*	COLLAB_DEGRADED	DEGRADED
*	*	COLLAB_SUSPENDED	SUSPENDED
FAILED + INVALID + 反复	*	*	UNAVAILABLE

---

4. C 自治处理动作表（State → Action）

C 与 B 最大差异点在这里：C 的自治动作必须更偏“放行收敛”，因为 C 是系统最后签字人。

4.1 动作原语集合（冻结）

C_Actions =
  C1: NORMAL_ARBITRATION         // 正常裁决
  C2: CONSERVATIVE_POLICY        // 保守策略（更高阈值、更少动作）
  C3: REDUCE_DECISION_RATE       // 降低裁决频率（节流）
  C4: DISABLE_HIGH_RISK_INTENTS  // 禁用高风险意图（警告/行为类）
  C5: STOP_ALLOWING_OUTPUT       // 停止放行（不进输出链）
  C6: EXIT_BC_COLLAB             // 退出与 B 的协同（只做最低限度本地规则）
  C7: SELF_RECOVERY_ONLY         // 仅允许自恢复（重置/回退/重校验）

4.2 总态到动作映射（冻结）

C_OverallState	必须执行	明确禁止
HEALTHY	C1	禁止额外收敛
DEGRADED	C2 + C3	禁止扩大动作范围
SUSPENDED	C4 + C5 + C6	禁止放行任何对外结果
UNAVAILABLE	C5 + C6 + C7	禁止裁决、禁止协同

解释：C 在 SUSPENDED/UNAVAILABLE 时，核心是不放行；哪怕还能“算”，也只能用于自检或 Shadow。

---

5. C 模块 IssueCode 目录（C-PROC / C-OUT / C-COLLAB）

命名规则固定：

C-{DOMAIN}-{XXX}
DOMAIN = PROC | OUT | COLLAB

5.1 C-PROC-*（工作过程）
- C-PROC-001：裁决循环连续超时（ERROR → Process DEGRADED）
- C-PROC-002：裁决流程卡死/无进展（CRITICAL → Process FAILED）
- C-PROC-003：连续内部异常（ERROR → Process DEGRADED）
- C-PROC-004：状态机非法跃迁/自相矛盾（CRITICAL → Process FAILED）
- C-PROC-005：自检失败（CRITICAL → Process FAILED）

5.2 C-OUT-*（裁决产出质量）

C 的“输出”是裁决产物（intent、risk、gate_request、explainability metadata），不是用户语音。

- C-OUT-001：裁决字段缺失/结构不完整（ERROR → Output INVALID）
- C-OUT-002：裁决数值非法（NaN/越界）（CRITICAL → Output INVALID）
- C-OUT-003：裁决结果不一致（同输入短期内反复翻转）（WARNING → Output SUSPICIOUS）
- C-OUT-004：风险等级与动作强度不匹配（例如低信心触发高风险意图）（ERROR → Output INVALID）
- C-OUT-005：可解释性元数据缺失（WARNING → Output SUSPICIOUS）

5.3 C-COLLAB-*（协同）

C 的协同对象更广：B、系统态、Runtime Gate、执行链。
- C-COLLAB-001：Reference / calibration_version 与系统不一致（ERROR → Collab DEGRADED）
- C-COLLAB-002：时间窗口不一致/漂移（ERROR → Collab DEGRADED）
- C-COLLAB-003：无法接收 B 输出或 B 输出结构异常（WARNING/ERROR → Collab DEGRADED）
- C-COLLAB-004：Runtime Gate 调用异常/返回不一致（CRITICAL → Collab SUSPENDED）
- C-COLLAB-005：执行链回执异常（例如输出失败、延迟异常）（ERROR → Collab DEGRADED）
- C-COLLAB-006：检测到旁路输出尝试（ProtocolViolation）（CRITICAL → Collab SUSPENDED，并建议系统 Fail-Safe）

---

6. C 的 Autonomy Heartbeat Monitor（复用 AHM）

完全复用你刚定的 AHM，只需换信号源与 IssueCode 前缀：

6.1 C 的最小运行信号

tick_counter / success_counter / error_counter / last_active_at

6.2 心跳类 Issue

建议：
- C-PROC-HB-001 无响应
- C-PROC-HB-002 无有效进展
- C-PROC-HB-003 异常循环
- C-PROC-HB-004 阻塞/超时

---

7. C 自治 Snapshot / Backend 上报（复用 ASR）

同构复用 B-ASR，字段替换为 C：

7.1 C_AutonomySnapshot

包含：
- C_OverallState
- 子状态（process/output/collab）
- reference_id / calibration_version / system_mode
- active_issues[]
- module_instance_id / timestamp

7.2 IssueEvent

同构：
- issue_code / level / domain / scope / event_type / timestamp
- 不含用户隐私与原始输入

---

8. 与 BCP Runtime Gate 的关系（必须写进 C 自治）
- C 自治不能放宽 BCP，只能更保守。
- 任何 C-COLLAB-004（Gate 异常）触发后：
- C 必须执行 STOP_ALLOWING_OUTPUT
- 并建议系统进入 Fail-Safe（通过事件上报，不直接改系统态）

---

9. 你当前阶段的实施策略（务实落地）

你说 C 还没开始，所以正确落地顺序是：
1. 先把 C 的自治框架（本文件）冻结，不做阈值
2. 等 C 的核心裁决管线完成后：
- 逐个 IssueCode “挂点”（hook）
- 接入 AHM 信号
- 打通 ASR 上报
3. 用 Shadow 模式跑一段，校准阈值，再启用 Runtime 约束

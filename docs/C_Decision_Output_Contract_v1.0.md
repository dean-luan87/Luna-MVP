C 裁决产物接口规范

C-DO (C Decision Output Contract)
Version: 1.0
Status: Frozen（运行时强约束）

---

0. 目标与边界（写死）

0.1 目标

C-DO 规范定义 C 模块对外可见的“裁决产物”，用于：
1. 作为 Runtime Gate 放行判断的候选输入
2. 作为 C 自治（C-OUT-*）输出质量监督的唯一锚点
3. 作为 后台审计、回放、指标统计的事实记录

0.2 边界
- C-DO 是“裁决结果结构”，不是用户输出内容本体（语音文案/完整提示词等可由上层模板系统生成）。
- C-DO 不能绕过 BCP Runtime Gate；Gate 结果永远高于 C 请求。
- C-DO 不包含隐私与原始输入内容；只包含结构化元信息与脱敏标签。

---

1. 顶层结构（冻结）

C 的每一次裁决都必须落成一个 C_DecisionOutput，由三部分构成：

C_DecisionOutput =
  DecisionCore        // 核心裁决（我想做什么、信心与风险）
  GateRequest         // 向 Runtime Gate 的放行请求（我请求放行什么）
  ExplainabilityMeta  // 可解释性元数据（我为什么这么裁决）

三者缺一不可（缺失即 C-OUT-001）。

---

2. 枚举与基础类型（冻结）

2.1 IntentType（裁决意图类型）

IntentType =
  NONE        // 不产生对外动作
  NOTIFY      // 提示类（低风险）
  WARNING     // 警告类（中/高风险）
  ACTION      // 行为引导类（最高风险，慎用）

2.2 OutputChannel（输出通道）

OutputChannel =
  LOG_ONLY
  VOICE
  HAPTIC
  UI

2.3 DecisionMode（裁决运行模式）

DecisionMode =
  RUNTIME     // 运行态裁决（可进入 Gate）
  SHADOW      // 影子态裁决（永不放行）
  FAIL_SAFE   // 降级态裁决（只允许 NONE / LOG_ONLY）

2.4 Timestamp
- 单调可比较时间戳（毫秒级即可）。

---

3. DecisionCore（核心裁决层）

3.1 定义

struct DecisionCore {
  uint64_t decision_id;          // 全局唯一或单调递增
  Timestamp decision_time;

  DecisionMode decision_mode;    // RUNTIME/SHADOW/FAIL_SAFE

  IntentType intent;             // NONE/NOTIFY/WARNING/ACTION
  OutputChannel channel;         // LOG_ONLY/VOICE/HAPTIC/UI

  double confidence;             // 0.0 ~ 1.0
  double risk_score;             // 0.0 ~ 1.0

  uint8_t intensity;             // 0 ~ 100（动作强度/语气强度）
  uint8_t urgency;               // 0 ~ 100（紧急程度）
  uint8_t verbosity;             // 0 ~ 100（信息量）
};

3.2 冻结约束（必须满足）
1. confidence、risk_score 必须存在且在合法范围（否则 C-OUT-002）。
2. intent == NONE 时：
- channel 必须为 LOG_ONLY
- intensity == 0 && urgency == 0
3. decision_mode == SHADOW 时：
- intent 可以非 NONE（用于评估），但后续 GateRequest 必须请求 不放行（见第 4 节）。
4. decision_mode == FAIL_SAFE 时：
- intent 必须为 NONE
- channel 必须为 LOG_ONLY

说明：FAIL_SAFE 下 C 仍可“计算”，但只能“记录”，不允许“影响用户”。

---

4. GateRequest（Runtime Gate 请求层）

4.1 定义

struct GateRequest {
  Timestamp request_time;

  // 强绑定上下文（用于 BCP 校验）
  uint64_t reference_id;
  uint64_t calibration_version;

  // 请求放行的意图（必须与 DecisionCore 一致或更保守）
  IntentType requested_intent;
  OutputChannel requested_channel;
  uint8_t requested_intensity;

  // 语义：请求 Gate 给出 ALLOW/BLOCK/FAIL_SAFE
  // 注意：这里是 request，不是 result
  enum class RequestedPolicy { ALLOW, BLOCK, FAIL_SAFE } requested_policy;
};

4.2 冻结约束（必须满足）
1. reference_id 与 calibration_version 必填且合法。
2. requested_intent/requested_channel/requested_intensity 必须与 DecisionCore 对齐：
- 可允许“更保守”：例如 DecisionCore.intent=WARNING，但 GateRequest.requested_intent=NOTIFY（降级请求）
- 不允许“更激进”：例如 DecisionCore.intent=NOTIFY 却请求 WARNING
3. Shadow 硬约束：
- DecisionCore.decision_mode == SHADOW ⇒ requested_policy 必须为 BLOCK
4. Fail-safe 硬约束：
- DecisionCore.decision_mode == FAIL_SAFE ⇒ requested_policy 必须为 FAIL_SAFE 或 BLOCK
5. NONE 硬约束：
- DecisionCore.intent == NONE ⇒ requested_policy 必须为 BLOCK

关键点：C 不能在 Shadow 或 Fail-safe 偷偷“请求放行”。

---

5. ExplainabilityMeta（可解释性元数据层）

5.1 定义

struct ExplainabilityMeta {
  // 影响本次裁决的自治问题（可为空，但不得缺失字段）
  std::vector<std::string> contributing_issue_codes;

  // 抽象理由标签：例如 "low_confidence" / "perception_unstable" / "policy_conservative"
  std::vector<std::string> rationale_tags;

  // 性能与审计
  double decision_latency_ms;     // >= 0
};

5.2 冻结约束
- decision_latency_ms 必须存在且非负（否则 C-OUT-002）。
- contributing_issue_codes、rationale_tags 字段可为空，但字段本身不得缺失（否则 C-OUT-001）。

---

6. 顶层对象：C_DecisionOutput

struct C_DecisionOutput {
  DecisionCore core;
  GateRequest gate;
  ExplainabilityMeta explain;
};

---

7. C-OUT-*（裁决产出监督）挂点定义（写死）

以下检测只针对 C-DO 结构与一致性，不涉及业务语义。

C-OUT-001：结构缺失

触发条件（任一）：
- core/gate/explain 任一缺失
- 任一必填字段缺失（reference_id、calibration_version、confidence、risk_score、decision_latency_ms 等）

C-OUT-002：数值非法

触发条件（任一）：
- confidence/risk_score 不在 [0,1]
- intensity/urgency/verbosity 不在 [0,100]
- latency_ms 为 NaN/Inf/负数

C-OUT-003：短期翻转异常

触发条件（示例策略）：
- 相同 reference_id + intent 在短时间窗口内反复在高/低风险、ALLOW/BLOCK 意图之间切换（阈值后置）
输出：SUSPICIOUS

C-OUT-004：风险与动作不匹配

触发条件（示例策略，阈值后置）：
- 低 confidence + 高 intent（WARNING/ACTION）
- 低 risk_score 却请求 ACTION
输出：INVALID（至少导致 C_OverallState ≥ SUSPENDED）

C-OUT-005：解释性缺失或异常

触发条件：
- 非 NONE 的 intent 但 rationale_tags 长期为空、或 latency 缺失等（策略后置）
输出：SUSPICIOUS

---

8. 与 BCP Runtime Gate 的适配关系（闭环）

C-DO 进入运行路径时的最小适配逻辑：
1. 从 C_DecisionOutput.gate 提取：
- reference_id
- calibration_version
- requested_intent（及强度/通道）
2. 构造 BCP-RG 需要的 BC_Decision（在你的体系里它是“候选决策”）
3. 调用 RuntimeGate.validate(decision, system_state)
4. 仅当 GateResult=ALLOW 才进入执行链；否则丢弃或 Fail-safe

冻结原则：
- C 的 requested_policy 是“请求”，不是结果；GateResult 永远优先。

---

9. 与 C 自治 State → Action 的关系（写死）
- 当 C_OverallState == SUSPENDED/UNAVAILABLE：
- C 仍可生成 C-DO（用于日志/自检/Shadow）
- 但 core.intent 必须被收敛到 NONE 或 decision_mode 转为 FAIL_SAFE（由自治动作实现）
- gate.requested_policy 必须为 BLOCK/FAIL_SAFE

这保证了：自治收敛是可审计的，不靠“口头约束”。

---

10. 上报与审计最小要求（与 ASR 同构）

每个 C_DecisionOutput 必须可被：
- 序列化落日志（脱敏）
- 按 decision_id 回放时间线
- 与 C_AutonomySnapshot 和 IssueEvent 对齐

禁止包含：
- 原始感知帧
- 用户隐私文本
- 可反推个人身份的细粒度数据

---

11. 一句话工程结论（写入总纲）

C-DO 将 C 的“裁决”固定为结构化事实对象，使自治监督、Gate 放行、后台回放形成闭环；
从而避免隐式逻辑、不可审计放行与状态跃迁。

---

如果你要我继续把接口彻底“落到工程可接线”，下一步就是两份对接规范（都很关键）：
1. C → RuntimeGate 适配层接口规范（把 C-DO 映射到 BCP-RG 的 BC_Decision）
2. 执行链回执（ExecutionReceipt）结构（用于 C-COLLAB-005：执行失败、延迟异常、重复触发等）

你已经说“继续”，我默认先写 (1) C → RuntimeGate 适配层接口规范。

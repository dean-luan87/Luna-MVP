BCP Runtime Gate 接口规范

BCP-RG (BC Collaboration Protocol – Runtime Gate)
Version: 1.0
Status: Frozen (运行时强约束)

---

0. 接口定位（先写死）

Runtime Gate 是系统中唯一允许“对外输出”的入口。

任何试图绕过 Runtime Gate 的输出路径：
- 视为 协议违规
- 必须在工程层被禁止或直接报错

---

1. 接口职责边界（不可扩展）

Runtime Gate 只做三件事：
1. 校验 系统状态是否合法
2. 校验 BC 协同结果是否可生效
3. 决定 是否允许进入执行 / 输出链路

Runtime Gate 明确不做的事：
- ❌ 不生成预测
- ❌ 不修正 B 的输出
- ❌ 不做策略优化
- ❌ 不提供替代行为

---

2. 核心数据结构规范

2.1 SystemRuntimeState（只读）

enum class PerceptionState {
  STABLE,
  UNSTABLE
};

enum class CalibrationState {
  UNCALIBRATED,
  CALIBRATING,
  CALIBRATED
};

enum class SystemMode {
  BOOT,
  SHADOW,
  RUNTIME_STABLE,
  FAIL_SAFE
};

enum class FaultState {
  NONE,
  SYSTEM_FAULT,
  HARDWARE_FAULT
};

struct SystemRuntimeState {
  PerceptionState perception;
  CalibrationState calibration;
  SystemMode mode;
  FaultState fault;
  uint64_t reference_id;
  uint64_t calibration_version;
};

冻结规则：
- 所有字段 不可由 B / C 直接修改
- 状态变更必须通过系统事件流

---

2.2 B_Output（强制携带 Reference）

struct B_Output {
  uint64_t reference_id;
  uint64_t calibration_version;
  double confidence;          // 0.0 ~ 1.0
  Timestamp created_at;
  Payload inference;
};

冻结规则：
- 缺失 reference_id 或 calibration_version → 非法
- Runtime Gate 不做补全

---

2.3 BC_Decision（仅 C 可提交）

struct BC_Decision {
  B_Output inference;
  DecisionIntent intent;  // 提醒 / 导航 / 警告 / 行为
};

---

3. Runtime Gate 主接口定义

3.1 接口签名（唯一入口）

enum class GateResult {
  ALLOW,
  BLOCK,
  FAIL_SAFE
};

GateResult RuntimeGate::validate(
  const BC_Decision& decision,
  const SystemRuntimeState& state
);

---

4. 判定逻辑规范（必须逐条实现）

4.1 系统态校验（优先级最高）

IF state.fault == HARDWARE_FAULT
  → FAIL_SAFE

IF state.mode != RUNTIME_STABLE
  → BLOCK

---

4.2 感知与校准校验

IF state.perception != STABLE
  → BLOCK

IF state.calibration != CALIBRATED
  → BLOCK

---

4.3 Reference 一致性校验（不可跳过）

IF decision.inference.reference_id != state.reference_id
  → BLOCK

IF decision.inference.calibration_version != state.calibration_version
  → BLOCK

---

4.4 置信度与时效校验（可配置阈值）

IF decision.inference.confidence < MIN_CONFIDENCE
  → BLOCK

IF now - decision.inference.created_at > MAX_VALID_WINDOW
  → BLOCK

---

4.5 违规升级规则（硬规则）

IF BLOCK occurs due to protocol violation
  AND violation is structural
  → FAIL_SAFE

示例（结构性违规）：
- 跨 Reference 使用预测
- 未校准状态提交决策
- Runtime 之外尝试输出

---

5. GateResult 行为语义（写死）

5.1 ALLOW
- 决策进入执行 / 输出链路
- 记录正常生效日志

5.2 BLOCK
- 决策直接丢弃
- 不触发任何对外行为
- 不提供替代输出

5.3 FAIL_SAFE
- 系统立即切换至 SystemMode::FAIL_SAFE
- 禁止 BC 协同
- 启用 C 的保守规则
- 写入不可篡改日志

---

6. Shadow 模式的工程约束

冻结规则：
- Runtime Gate 拒绝一切 Shadow 决策
- Shadow 管线 不得调用 Runtime Gate

ShadowPipe → Eval / Log
RuntimePipe → RuntimeGate → Output

---

7. 启动与校准期间的强制行为

IF state.mode == BOOT
  → RuntimeGate 永远 BLOCK

直到：
- Reference 建立
- 校准完成
- 显式切换到 RUNTIME_STABLE

---

8. 日志与审计要求（不可省略）

Runtime Gate 必须记录：
- 每一次 BLOCK / FAIL_SAFE 的原因
- 相关 reference_id / calibration_version
- 决策来源模块

这是未来你系统“自证清白”的证据链。

---

9. 接口冻结声明
- 本接口为 BC 协同唯一生效入口
- 不允许增加“旁路输出”
- 不允许通过配置关闭
- 所有版本升级必须兼容该接口语义

---

一句话工程结论（给开发看的）

只要走 Runtime Gate，就一定安全；
想绕 Runtime Gate，本身就是 Bug。

---

下一步你已经规划好了：
👉 B / C 自治文档。

我建议顺序是：
1. B 模块自治协议（预测自律）
2. C 模块自治协议（裁决自律）

你点一个，我直接写。

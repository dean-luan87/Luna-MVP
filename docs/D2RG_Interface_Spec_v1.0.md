Decision → Runtime Gate 适配层接口规范

D2RG (Decision-to-RuntimeGate Adapter)
Version: 1.0
Status: Frozen（系统基础设施）

---

0. 定位（写死）

D2RG 是系统中唯一允许“裁决意图”进入 Runtime Gate 的适配层。

它解决的问题只有一个：

把“谁做出的裁决”与“是否允许执行”彻底解耦。

---

1. 适配层的输入与输出（极简）

1.1 输入（抽象裁决对象）

D2RG 不关心裁决来自哪里，只要求输入满足最小裁决接口：

struct AbstractDecision {
  uint64_t decision_id;
  Timestamp decision_time;

  // 裁决意图（抽象）
  IntentType intent;            // NONE / NOTIFY / WARNING / ACTION
  OutputChannel channel;        // LOG_ONLY / VOICE / HAPTIC / UI
  uint8_t intensity;            // 0 ~ 100

  // 上下文绑定
  uint64_t reference_id;
  uint64_t calibration_version;

  // 决策模式
  DecisionMode decision_mode;   // RUNTIME / SHADOW / FAIL_SAFE
};

冻结原则：
- 不包含置信度、风险、解释性
- 这些属于“裁决源的自治问题”，不属于 Gate 输入

---

1.2 输出（Runtime Gate 的唯一候选输入）

struct GateCandidate {
  uint64_t decision_id;

  // 强绑定上下文
  uint64_t reference_id;
  uint64_t calibration_version;

  // 请求内容
  IntentType requested_intent;
  OutputChannel requested_channel;
  uint8_t requested_intensity;

  // 适配层给出的请求策略
  enum class RequestedPolicy {
    ALLOW,
    BLOCK,
    FAIL_SAFE
  } policy;
};

---

2. D2RG 的核心职责（不可扩展）

D2RG 只做三件事：
1. 裁剪：把裁决对象裁剪成 Gate 可理解的最小集合
2. 收敛：在 Shadow / Fail-safe 等模式下强制降级
3. 一致性校验：避免“说一套、请求另一套”

❗D2RG 不是第二个 Gate，
它不看系统态、不看感知稳定性、不做安全判断。

---

3. 抽象适配规则（冻结）

3.1 模式收敛规则（最重要）

IF decision_mode == SHADOW
  → policy = BLOCK

IF decision_mode == FAIL_SAFE
  → policy = FAIL_SAFE

解释：
- Shadow：允许“算”，但绝不允许“做”
- Fail-safe：明确请求系统进入兜底

---

3.2 NONE 意图硬约束

IF intent == NONE
  → policy = BLOCK

主动不作为也是一种裁决，但它永远不该触发执行。

---

3.3 请求一致性规则

requested_intent   = decision.intent
requested_channel  = decision.channel
requested_intensity = decision.intensity

- 不允许在适配层“增强动作”
- 只允许 等价或更保守
- 若输入不合法 → 直接 BLOCK

---

3.4 上下文强绑定规则

GateCandidate.reference_id == decision.reference_id
GateCandidate.calibration_version == decision.calibration_version

缺失或不一致：
- 不抛异常
- 直接 policy = BLOCK

---

4. D2RG 的接口定义（唯一入口）

GateCandidate adapt_to_gate(
  const AbstractDecision& decision
);

冻结要求：
- 纯函数（无副作用）
- 不访问全局状态
- 不写日志（日志由调用方负责）

---

5. D2RG 与 Runtime Gate 的边界关系

AbstractDecision
   ↓
D2RG.adapt_to_gate()
   ↓
GateCandidate
   ↓
RuntimeGate.validate(candidate, system_state)

职责边界写死：

层	负责什么
决策源	是否“想做”
D2RG	是否“可以请求”
Runtime Gate	是否“允许执行”

---

6. 为什么要单独抽这一层（工程收益）

6.1 解耦裁决来源
- C
- 规则引擎
- 回放系统
- 人工兜底

全部复用 D2RG，不碰 Gate。

6.2 防止“偷偷放行”
- 决策源即便写 Bug
- 只要走 D2RG + Gate
- 都会被 Shadow / NONE / FAIL_SAFE 收敛

6.3 后台审计极其清晰

你可以在后台明确区分：
- 决策是什么
- 请求了什么
- Gate 为什么拒绝

这是责任切割，不是技术洁癖。

---

7. 冻结声明（必须写进工程）
- 任何进入 Runtime Gate 的请求 必须经 D2RG
- 禁止决策源直接构造 GateCandidate
- 禁止在 Runtime Gate 内“猜测决策意图”

---

一句话系统总结

D2RG 是系统的“意图变压器”：
把各种裁决源的意图，压缩成 Gate 可控、可审计、可拒绝的最小请求。

---

如果你愿意继续，下一步自然是同样保持抽象、不引入 C的：
- 执行链回执（ExecutionReceipt）接口规范
—— 用于任何“执行是否真的发生/成功/重复/超时”的反馈，
也是 *-COLLAB-* Issue 的统一来源。

我可以直接继续把这份规范写完。

B / C 协同协议（BCP）
BC Collaboration Protocol v1.0

本协议定义 B 模块（认知 / 预测）与 C 模块（控制 / 裁决）之间的
通信方式、生效条件、禁止行为与状态约束。

本协议为运行时强约束协议，违反即视为系统缺陷。

---

1. 协议目标与设计原则

1.1 协议目标
- 确保 B / C 在任何系统状态下 行为可预测、结果可解释
- 防止因感知不稳定、校准失效、模块异常导致的 越权输出
- 支持系统长期演进而不引入不可控风险

1.2 核心原则（冻结）
1. 协同不等于生效
2. 预测不等于决策
3. 稳定性优先于智能性
4. 任何状态跃迁必须显式发生

---

2. 模块角色与权责边界（不可变）

2.1 B 模块（Inference Provider）

职责：
- 基于当前感知与 Reference Frame 进行推断
- 输出预测结果与不确定性描述

禁止行为：
- ❌ 不得判断系统模式
- ❌ 不得决定输出是否生效
- ❌ 不得缓存跨 Reference 的有效预测

---

2.2 C 模块（Executive Arbiter）

职责：
- 管理系统态（System Mode）
- 决定 BC 协同结果是否生效
- 执行安全兜底与降级策略

禁止行为：
- ❌ 不得生成感知或预测结果
- ❌ 不得伪造或修正 B 的推断内容
- ❌ 不得在协议禁止状态下放行输出

---

3. 协同生效的前置条件（硬门槛）

BC 协同允许通信 ≠ 允许生效。

3.1 协同生效判定条件（全部满足）

BC_Output_Allowed =
  PerceptionState == STABLE
  AND CalibrationState == CALIBRATED
  AND SystemMode == RuntimeStable
  AND NoCriticalFault == true

3.2 不满足时的统一行为
- B 继续运行，结果标记为 Non-Effective
- C 接收但 不得采纳
- 禁止任何对外输出（语音 / 行为 / 警告）

该状态定义为：

BC Collaboration Suspended

---

4. 感知稳定性约束（强制）

4.1 感知状态定义

PerceptionState = STABLE | UNSTABLE

4.2 UNSTABLE 状态冻结规则

当 PerceptionState == UNSTABLE：
- ❌ BC 联合输出不生效
- ❌ 不得触发任何外部行为
- ❌ 不得进行未来预测

这是协同挂起（Suspend），不是故障。

---

5. Reference 与预测生命周期绑定（不可绕过）

5.1 基本规则（冻结）

任何 B 输出的预测
仅在其生成时所依赖的 Reference Frame 内有效

5.2 作废条件（任一即作废）
- PerceptionState: UNSTABLE → STABLE
- Reference Frame 重建
- 校准版本变化
- 模块重启

5.3 C 的强制义务
- C 不得复用旧 Reference 下的预测
- 必须等待新校准完成后重新协同

---

6. 系统模式下的 BC 协同规则

6.1 Runtime Stable（运行态）

允许：
- BC 联合决策生效
- 输出进入执行链路

禁止：
- 使用未校准预测
- 使用 Shadow 结果

---

6.2 Shadow / Observe（影子态）

允许：
- B 正常预测
- C 同时评估新旧策略

禁止：
- ❌ Shadow 结果对外生效
- ❌ 替换 Runtime 输出

---

6.3 Fail-Safe / Degraded（降级态）

强制规则：
- BC 协同中断
- C 单独运行保守规则
- 禁止未来预测
- 禁止复杂推断

---

7. 校准与启动约束（硬安全条款）

7.1 启动流程（不可跳过）

Boot →
  Perception Self-Check →
  Reference Establish →
  BC Calibration →
  Runtime Stable

7.2 校准完成前的禁止行为
- ❌ B 预测不得生效
- ❌ C 不得触发警告
- ❌ 不得输出语音或行为

---

8. 协议违规的系统处理

8.1 违规定义（任一）
- 在 Suspend 状态放行输出
- 跨 Reference 使用预测
- 未完成校准进入 Runtime
- 越权触发外部行为

8.2 处理策略
- 标记系统为 ProtocolViolation
- 强制进入 Fail-Safe
- 记录不可篡改日志
- 禁止自动恢复到 Runtime

---

9. 协议冻结声明
- 本协议为 运行时约束协议
- 不得通过配置绕过
- 不得在子模块中隐式实现“等价替代逻辑”
- 所有升级必须兼容本协议

---

一句话工程总结（建议写在首页）

BC 可以随时计算，但只有在合法状态下才有“话语权”。

---

下一步（你已经说了，我只对齐）

接下来两份文档是自治层，而不是协同层：
1. 《B 模块自治协议》
- 预测失效管理
- 不确定性自评
- 自我退化 / 熔断
2. 《C 模块自治协议》
- 系统态裁决权
- 失败分类与恢复
- 人机责任边界

等你一句话，我可以直接把 B 自治协议先写出来，保持同样的冻结级别。

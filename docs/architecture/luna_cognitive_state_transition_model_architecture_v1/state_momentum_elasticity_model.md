# State Momentum, Elasticity and Persistence

- State Momentum：过去状态对下一候选的影响，避免每个 tick 重新初始化。
- State Elasticity：进入与退出某状态的响应速度；风险状态可快速进入、缓慢退出。
- State Persistence：同一 Luna 的 State Vector、Identity、版本和 trace 连续性。

三者是参数/约束候选，不是自动 Scheduler 或 State Runtime。它们必须绑定 Field Scope、时间窗、Evidence 和回滚策略。


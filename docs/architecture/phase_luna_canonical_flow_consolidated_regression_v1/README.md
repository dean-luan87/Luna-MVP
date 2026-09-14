# Canonical Flow Consolidated Regression v1

本包只编排三个已经完成的 synthetic controlled Runner/Verifier，并增加跨模块连续性检查。它不重新实现子模块业务逻辑，不创建新 owner，也不执行 Provider、Model、Observation、Action 或真实 runtime。

每次运行使用新的 `attempt_id`。子 Runner 输出只在内存中归一化；子 Runner 失败、JSON 无效、场景数不符或子检查失败时 fail-closed，并且不会调用该子模块 Verifier。


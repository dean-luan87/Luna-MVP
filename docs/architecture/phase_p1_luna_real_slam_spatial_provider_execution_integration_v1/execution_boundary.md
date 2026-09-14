# Execution Boundary

## Route B boundary

本阶段只允许静态审计、分类和文档记录。以下操作均未被执行：

- Python、Runner、Verifier、pytest、py_compile；
- SLAM/VIO backend、Provider 或 Model；
- Camera、video processing、ROS、Docker 或 native compilation；
- dependency installation、model/weight download 或 network request；
- Decision、Task、Action、Navigation execution、Runtime Executor 或 device control。

## 未来 Route A 必须满足

在 `LIVE_RUNTIME` 下，真实 Provider integration 才可进入 shared Runtime，且必须
由实际调用派生 `provider_invoked`、`model_invoked`（适用时）、
`provider_real_execution_attempted`、`provider_real_execution_verified` 和
`recorded_provider_result_used=false`。

SLAM 不得把 pose、trajectory、map、geometry 或 traversability candidate 直接
写入 Field 或 Current World，也不得产生 navigation truth、Decision、Task 或 Action。

## 当前结论

不存在满足上述条件的真实执行入口，因此不能建立假的 Runner/Verifier 来填补
`LIVE_RUNTIME` 链路。

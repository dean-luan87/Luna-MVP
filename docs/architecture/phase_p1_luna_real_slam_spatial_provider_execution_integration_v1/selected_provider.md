# Selected Provider / Future Candidate

## 当前 Provider

本阶段没有选定可执行的 real Provider。Canonical registry 中存在：

- capability：`spatial_mapping`
- registry model/provider key：`slam_v1`
- canonical capability ref：`capability:spatial_mapping`
- canonical provider ref（按 shared Runtime 命名约定待执行时形成）：`provider:slam_v1`
- canonical model ref：`model:slam_v1`
- model family：`slam`
- registry state：`active` / `admitted`
- candidate-only：`true`

这些是 Capability / Provider / Model governance declaration，不是可调用 backend 的
证明。当前 `slam_v1` 没有对应的真实 provider adapter、native model loader 或
Provider Runtime entrypoint。

## 最接近的未来候选

静态资产中最接近的候选是 **RTAB-Map offline/export route**，原因是仓库已有较多
RTAB trajectory、odometry、graph export 的 file loader、schema validator 和
candidate mapping。它仍不是当前 real Provider：现有实现明确禁止读取 RTAB-Map
database、接 ROS 或启动 live RTAB-Map runtime。

ORB-SLAM3、OpenVINS、VINS、Kimera 和 Hydra 目前更接近技术参考、stub 或 replay
sample，不适合作为当前阶段唯一 Provider。

## 选择边界

RTAB-Map 只是下一步调查候选，不是本阶段的 `selected_provider`，也没有得到
`REAL-RUNTIME VERIFIED` 或 `LIVE_RUNTIME` 结论。真正接入前必须重新审计 license、
native runtime、输入设备/序列、依赖、模型/配置和 session lifecycle。

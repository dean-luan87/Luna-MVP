# Error and Readiness Handling

## 当前静态状态

现有 availability matrix 将真实 SLAM path 分类为 blocked/unavailable：

- local runner unavailable；
- local weights unavailable；
- SLAM dependencies unavailable；
- camera/video runtime unauthorized；
- model/weight download unauthorized。

cached output、adapter stub 和 file replay 是合法的 controlled/recorded asset，但
不能映射成 Provider success 或 `LIVE_RUNTIME`。

## 未来 native state 的处理原则

真实 backend 接入前，不预先发明 canonical status。对 native 状态应先保留其
provider-specific 表达，再根据实际 shared contract 映射：

| 可能 native state | 当前处理 |
|---|---|
| `INITIALIZING` | 待真实 backend 审计；不能伪造 pose |
| `TRACKING` / `SUCCESS` | 仅在真实 native result 产生后映射 candidate |
| `PARTIAL` | 保留 partial/session/frame lineage；待 contract 验证 |
| `TRACKING_LOST` | 输出真实 tracking-health/error candidate；不复用最后 pose 为当前真值 |
| `NO_MAP` / `NO_POSE` | 明确无结果或 provider error semantics；不制造 spatial evidence |
| provider unavailable / model unavailable | fail closed；不进入 fake cognition success |
| malformed native output / timeout | fail closed，并保留 error category |

## 禁止

不得把没有 backend、没有输入或 tracking lost 误报为 provider success、map success、
current pose 或 navigable route。

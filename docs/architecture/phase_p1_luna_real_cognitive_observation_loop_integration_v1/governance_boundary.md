# Governance Boundary

本 Phase 复用现有 Plane G assertion set，包含 G02、G03、G04、G06、G07、G08、
G09、G13、G15、G16、G17、G18、G19、G20，以及同一组 G01/G05/G10/G11/G12/G14。
Plane G 的 live mode binding 要求真实 model/provider/live observation proof；
controlled replay 仍保持其原有禁止真实调用的语义。

始终保持：

- OCR output、RuntimeObservation 和 Evidence 是 candidate-only；
- `truth_declared=false`、`fact_admitted=false`；
- 不发生 Field mutation 或 World Truth declaration；
- A-Route/CState 到 cognitive sufficiency 后停止；
- 不执行 Decision、Task、Action、Runtime Executor 或 device control；
- Observation Gateway admission 不是 Provider 自主连续执行授权。

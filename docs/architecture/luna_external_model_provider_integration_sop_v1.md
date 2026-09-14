# Luna External Model / Provider Integration SOP

**Version:** v1.0
**Status:** `SOP_V1_ESTABLISHED`
**Established:** 2026-09-01

## 1. 定位与范围

本 SOP 是 Luna 接入外部模型、算法和感知 Provider 的长期工程标准。它规定
外部 Provider 如何作为已治理的 Capability Provider 接入，以及真实输出如何在
Runtime Governance 下变成 Observation / Evidence Candidate。

本 SOP 是可版本演进的工程标准，不是 Constitution，也不是不可修改的协议。它
不拥有 Capability Governance、cognition、World Truth、Decision、Task 或 Action
authority。Provider 的职责在产生受约束的候选输出后结束。

v1.0 的实际验证来源是：

- [YOLO11n Real Provider Execution Integration](./phase_p1_luna_real_provider_execution_integration_v1/overview.md)
- [RapidOCR / ONNXRuntime Real OCR Provider Execution Integration](./phase_p1_luna_real_ocr_provider_execution_integration_v1/overview.md)

这两个 Phase 已由用户终端完成真实运行与 Verifier 验证；本 SOP 记录的是已验证
的共同接入模式，不重新设计或改写两个 Provider 的 Runtime 行为。

## 2. Canonical 接入链

当前真实实现冻结的主链为：

```text
Observation Demand
  → Capability Requirement
  → Capability Resolution
  → Provider Resolution
  → canonical Capability / Provider / Model identity
  → ProviderRuntimeRequestV1
  → Runtime admission / execution mode
  → real Provider invocation
  → Provider native result
  → Provider-specific adapter / normalizer
  → ProviderRuntimeResultV1
  → RuntimeObservationEnvelopeV1
  → Observation Gateway
  → Evidence Candidate
  → A-Route
  → consuming cognition
  → Sufficiency / Information Gap / Stop
```

在当前代码中，Provider Runtime 的共同入口位于
`capabilities/midplatform/core/provider_runtime_to_observation_ingress/`。
YOLO 与 OCR 都复用 `ProviderRuntimeRequestV1`、`ProviderRuntimeResultV1`、
`provider_result_to_runtime_observation`、Observation Gateway 和 A-Route。
差异只位于 canonical binding seam、native invocation 和 native result adapter。

Provider native result 不得直接进入 cognition。任何 provider-specific 输出必须
先被包裹为 ProviderRuntimeResult，再生成 RuntimeObservation，经 Gateway admission
后才可作为 Evidence Candidate 被下游消费。

## 3. 共享标准与 Provider-specific 实现

### 3.1 所有 Provider 共享的标准

- Capability、Provider、Model 和 Capability Requirement 的 identity 规则；
- `ProviderRuntimeRequestV1` 与 `ProviderRuntimeResultV1`；
- Runtime admission 与 execution mode；
- `RuntimeObservationEnvelopeV1`；
- Observation Gateway 的 ingress、admission、trace 和 ownership guard；
- Evidence Candidate 边界与 `candidate_only=true`；
- `truth_declared=false`、`fact_declared=false` 的权威边界；
- trace、provenance、source 与 execution identity lineage；
- success、empty success 和 fail-closed error 语义；
- A-Route / consuming cognition 的下游所有权；
- 禁止 Field mutation、World Truth、Decision / Task / Action 和设备控制。

### 3.2 允许 Provider-specific 的部分

- native invocation API；
- model loading、native configuration 和本地依赖；
- native result schema；
- Provider 实际产生的字段，例如 bbox、polygon、text、confidence、pose；
- provider-specific adapter / normalizer；
- provider-specific empty-result 判定；
- dependency、asset cache 和 runtime availability probe。

Provider-specific 实现不得创建平行 Provider Runtime，不得绕过 Runtime Observation
或 Observation Gateway，也不得扩大 Provider 的语义 authority。

## 4. Canonical Identity SOP

不同 identity namespace 不得混用。当前标准含义如下：

| Identity | 所属 namespace | 用途 |
|---|---|---|
| Capability Requirement identity | `capability-requirement:*` | 源自 Capability / FPO 的需求与 admission 依据 |
| normalized provider requirement | `provider-requirement:*` | Provider resolution 的规范化视图与诊断 lineage |
| Capability identity | registry `capability_id`，例如 `text_recognition`、`object_detection` | 表示系统能力，不表示 Provider 或 Model |
| Provider identity | canonical `provider_ref`，例如 `provider:ocr_v1` | 表示被 Registry 选中的 Provider binding |
| Model identity | canonical `model_ref`，例如 `model:ocr_v1`，或已登记的 model asset ref | 表示执行所使用的模型/资产 |
| Provider Request identity | `provider-request:*` | 一次 ProviderRuntime 请求 |
| Provider Result identity | `provider-result:*` | 一次 native 结果的规范化结果 |
| Execution Instance identity | `execution_instance_ref` | 贯穿 request、result、observation、gateway 的一次执行实例 |
| Observation identity | `runtime-observation:*` | RuntimeObservationEnvelope 的候选观测 |
| Evidence identity | `evidence:*` | Gateway 生成的 Evidence Candidate |

特别规则：Capability Requirement 与 normalized provider requirement 不是同一
identity。历史上出现过把 `provider-requirement:*` 代入 canonical admission 的
问题；v1 将其作为防错规则，保留两者并在跨边界时使用正确的 namespace。

Canonical identity 必须来自 Capability Registry、Provider Registry、Model
Registry、Universal Capability Slot 或现有 canonical binding seam。禁止手工伪造
binding、admission ref 或把 native provider id 冒充 canonical registry id。

## 5. Execution Mode SOP

当前 canonical execution modes 为：

- `SYNTHETIC_CONTROLLED`：受控合成输入；不代表真实 Provider / Model invocation；
- `CONTROLLED_REPLAY_RUNTIME`：受控 recorded input replay；不代表本次 live invocation；
- `LIVE_RUNTIME`：本次执行实际进入 Provider runtime。

在 `LIVE_RUNTIME` 下，以下字段必须由实际路径产生并保留：

- `provider_invoked`；
- `model_invoked`（适用时）；
- `provider_real_execution_attempted`；
- `provider_real_execution_verified`；
- `recorded_provider_result_used`。

不能通过 hardcode、fixture、recorded output 或 summary 默认值伪造这些状态。
`provider_real_execution_verified` 只能在实际 invocation、结果规范化以及后续
治理检查满足后成立；Agent 或文档不能预先替代用户终端验证。

## 6. Result Normalization SOP

Provider-specific adapter / normalizer 至少应完成：

1. 捕获 native result，不重建不存在的字段；
2. 验证 native output shape；
3. 映射到 `ProviderRuntimeResultV1`；
4. 关联 request、provider、capability、model、execution instance；
5. 附加 trace / provenance / source lineage；
6. 设置 candidate-only 与 truth boundary；
7. 将结果交给 `provider_result_to_runtime_observation`；
8. 由 Gateway 生成 Evidence Candidate。

Provider 实际提供什么就保留什么。允许 field mapping、normalization、identity
wrapping、trace/provenance attachment 和 candidate semantics attachment；禁止
伪造 confidence、language、reading order、bbox、semantic interpretation、truth
或 execution success。

当前共同 Result contract 至少包含：

`provider_request_ref`、`provider_result_ref`、`execution_instance_ref`、
`capability_ref`、`provider_ref`、`model_ref`、`provider_invoked`、
`model_invoked`、`status`、`output_ref`、`raw_result_ref`、trace/provenance refs、
`candidate_only` 和 `truth_declared=false`。可获得的 confidence / quality 才能
进入 candidate 字段；不可获得时保持 `None`。

## 7. Candidate / Truth Boundary

External Provider output 统一是 Observation / Evidence Candidate，不是：

- Fact；
- World Truth 或 Current World Truth；
- Decision；
- Task；
- Action。

例如 YOLO 的 `person detected` 只能是 object evidence candidate；RapidOCR 的
`EXIT` 只能是 text evidence candidate。Provider 不得自行推导“这里就是出口”、
“用户应该从这里走”或“执行导航”。这些解释与后续 authority 属于 cognition 和
其后的治理边界。

## 8. Empty 与 Error Semantics

`ProviderRuntimeResultV1` 当前 canonical status 集合为：

`SUCCESS`、`EMPTY_SUCCESS`、`UNAVAILABLE`、`REJECTED`、`ERROR`。

状态与错误类别应分开表达：

| 实际条件 | canonical status | 规则 |
|---|---|---|
| 有合法结果 | `SUCCESS` | 只保留实际 candidate output |
| Provider / Model 已真实执行但无检测结果 | `EMPTY_SUCCESS` | `empty_result=true`；不得制造 positive Evidence |
| Provider dependency / import / availability 不可用 | `UNAVAILABLE` | fail closed；不得生成 runtime success |
| 输入缺失或无效，例如 invalid image | `REJECTED` | 通过 `error_category` 记录具体原因 |
| invocation exception、timeout、malformed native output | `ERROR` | 通过 `error_category` 保留具体错误 |

因此 `INVALID_INPUT`、`INVOCATION_ERROR`、`TIMEOUT`、`MALFORMED_OUTPUT` 等是
实际 error category 或 native runtime category，不应在没有 contract 依据时扩展
ProviderRuntimeResult status enum。

Empty success 与 provider failure 必须可区分。Empty success 可以形成明确的
execution-status candidate（当前 OCR Gateway 类型为 `ocr_empty_success`），但不
能伪造文字、检测框或语义结论。所有失败路径都不得生成 fake RuntimeObservation、
fake Evidence 或伪造 cognition success。

## 9. Trace / Provenance SOP

每个真实 Provider integration 至少保持以下 lineage：

```text
Evidence
  → RuntimeObservation
  → ProviderRuntimeResult
  → ProviderRuntimeRequest
  → Provider / Model
  → Capability Requirement / Capability Resolution
  → Source
```

同时保留 `Execution Instance`、Gateway admission、A-Route、Sufficiency /
Information Gap / Stop、provider trace 和 provenance refs。目标是可以从 Evidence
反向追踪到实际 source、request、provider/model 和需求，而不依赖 undocumented
推断或临时字段。

## 10. Forbidden Behaviors

Provider integration 禁止：

- bypass Observation Gateway；
- direct cognition mutation；
- Field mutation；
- World Truth declaration；
- Fact admission；
- Decision / Task / Action ownership；
- direct device control；
- Runtime Executor ownership；
- fake provider success 或 fake model invocation；
- recorded result pretending to be live execution；
- provider-specific parallel Runtime architecture；
- 在 normalizer 中加入未经 Provider 提供的语义解释。

## 11. New Provider Integration Checklist

- [ ] Capability 是否已存在；
- [ ] 是否确实需要新增 Capability；
- [ ] Provider 是否已注册；
- [ ] Model 是否已注册；
- [ ] Capability / Provider / Model binding 是否 canonical；
- [ ] Capability Requirement 与 normalized provider requirement 是否分离；
- [ ] Provider Runtime entrypoint 是否存在；
- [ ] Provider-specific dependency、asset 和 availability 是否明确；
- [ ] Native result schema 是否已审计；
- [ ] Provider-specific adapter / normalizer 是否存在；
- [ ] 是否复用 `ProviderRuntimeRequestV1`；
- [ ] 是否复用 `ProviderRuntimeResultV1`；
- [ ] 是否生成 `RuntimeObservationEnvelopeV1`；
- [ ] 是否经过 Observation Gateway；
- [ ] Evidence 是否 `candidate_only`；
- [ ] Empty success 是否正确表达；
- [ ] Error path 是否 fail closed；
- [ ] Trace 是否完整；
- [ ] Provenance 是否完整；
- [ ] Truth / Fact 是否被禁止；
- [ ] Decision / Task / Action 是否被禁止；
- [ ] `LIVE_RUNTIME` 是否确实进入真实执行路径；
- [ ] invocation flags 是否由真实路径派生；
- [ ] recorded result 是否未冒充 live result；
- [ ] Runner 是否存在；
- [ ] Verifier 是否存在；
- [ ] 文档是否同步；
- [ ] 用户终端是否完成真实验证。

## 12. Definition of Done

只有同时满足以下条件，Provider 才能宣称 `REAL-RUNTIME VERIFIED`：

1. Provider Runtime Request 成立；
2. Provider 实际被调用；
3. Model 实际被调用（适用时）；
4. Native Result 实际产生，或产生合法 `EMPTY_SUCCESS`；
5. `ProviderRuntimeResultV1` 成立；
6. `RuntimeObservationEnvelopeV1` 成立；
7. Observation Gateway admitted；
8. Evidence Candidate 成立，或满足合法 empty-success semantics；
9. Trace / Provenance 完整；
10. 无 Truth / Fact promotion；
11. 无非法 mutation；
12. 无 downstream Decision / Task / Action / Runtime Executor execution；
13. Verifier PASS；
14. 用户终端提供真实运行结果。

Agent、SOP 文档或静态检查不能代替第 14 项，也不能单独宣称
`REAL-RUNTIME VERIFIED`。

## 13. Reference Implementations

### Reference A — YOLO11n Real Vision Provider

Capability 类型：object detection / Vision。参考其 bounded single-frame
invocation、canonical admission、native detection adapter、Runtime Observation、
Gateway、A-Route、Cognitive State、Sufficiency / Stop 以及 candidate-only boundary。

实现与 Phase 文档：

- `capabilities/midplatform/core/provider_runtime_to_observation_ingress/real_provider_execution_engine_v1.py`
- [Phase overview](./phase_p1_luna_real_provider_execution_integration_v1/overview.md)
- [Phase runtime path](./phase_p1_luna_real_provider_execution_integration_v1/runtime_path.md)

### Reference B — RapidOCR / ONNXRuntime Real OCR Provider

Capability 类型：text recognition / OCR。canonical registry binding 为
`text_recognition` → `ocr_v1`，native implementation 为 RapidOCR / ONNXRuntime。
参考其 provider-specific native adapter、text / score / bbox candidate mapping、
empty-success handling 与错误分类。

实现与 Phase 文档：

- `capabilities/midplatform/core/provider_runtime_to_observation_ingress/real_ocr_provider_adapter_v1.py`
- `capabilities/model_ocr/rapidocr_adapter_v0.py`
- [Phase overview](./phase_p1_luna_real_ocr_provider_execution_integration_v1/overview.md)
- [OCR result mapping](./phase_p1_luna_real_ocr_provider_execution_integration_v1/ocr_result_mapping.md)

这两个 Reference 的可复制部分是 integration contract、runtime flow 和 governance
boundary，而不是未来 Provider 的 native implementation。

## 14. v1.0 明确未覆盖的类型

v1.0 已验证的是有限、请求 → invocation → result 的本地真实 Provider execution，
适用于 YOLO11n vision 与 RapidOCR OCR。它不声称已经验证：

- streaming provider；
- persistent provider；
- continuous SLAM lifecycle；
- audio streaming；
- multi-provider orchestration；
- provider fallback；
- hot swap；
- multi-model routing；
- VLM multimodal runtime；
- world model runtime。

这些是验证范围边界，不是当前 SOP 的缺陷结论。

SLAM / Spatial Provider 是计划中的下一类 integration。SLAM 可能引入 persistent
state、temporal state、continuous observation、pose / map lifecycle；只有真实
SLAM 接入暴露出当前 SOP 无法表达的需求后，才考虑形成 v1.1。

## 15. SOP Change History 与演进规则

当新的真实 Provider 暴露当前 SOP 无法表达的工程需求时：

1. 保留已验证行为；
2. 修改 SOP；
3. 提升版本；
4. 在本节记录 `version`、`date`、`trigger`、`exposed gap`、`change`、
   `compatibility impact` 和 `reference implementation`；
5. 同步受影响的 canonical docs。

禁止为了假设中的未来模型提前扩张 SOP。SOP evolution 由真实工程需求驱动。

### History

| Version | Date | Status | Trigger / source | Change | Compatibility impact |
|---|---|---|---|---|---|
| v1.0 | 2026-09-01 | `ESTABLISHED` | 已验证的 YOLO11n 与 RapidOCR real provider phases | 固化共享 Runtime、identity、normalization、candidate boundary、empty/error、trace/provenance、checklist 与 DoD | 保持既有 YOLO / RapidOCR 行为；不新增 Runtime architecture |

## 16. 维护边界

本 SOP 的更新不等于某个 Provider Phase 的重新打开，也不改变已关闭 Phase 的
历史事实。若静态审计发现实现与历史文档存在差异，应先记录差异并由后续维护工作
单独处理；不能借 SOP 标准化顺手修改已验证 Runtime。

# Compatibility with Existing Observation Requests

Repository 中已有三类相关资产：

1. 旧 `cognitive_analysis` observation request candidate；
2. FPO active-observation control 的 demand/request/capability contracts；
3. Provider-to-Observation Ingress、Vision/OCR 与 Observation Gateway runtime。

它们不是同一个语义层。历史请求回答的是 task/domain 或 execution-facing
请求；本阶段的 Cognitive Observation Demand 只回答：

```text
需要观察什么信息，服务哪个 Need / Gap / Branch / Strategy？
```

未来可由 `Capability Resolution / Perception Routing` 建立显式 adapter：

```text
Cognitive Observation Demand
  → capability/perception routing
  → domain/provider-specific Observation Request
```

本阶段不建立该 adapter，不调用 FPO、Provider、Model、OCR、Camera 或真实
Observation。特别是“文字相关信息”不等于 OCR request；OCR 仍是未来的 evidence
provider 选择问题。

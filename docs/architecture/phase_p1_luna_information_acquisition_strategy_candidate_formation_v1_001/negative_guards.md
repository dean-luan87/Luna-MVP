# Negative Guards

- 只接受 `ADMITTED` Branch；不重新运行 Branch Formation 或 Governance；
- 不从 Goal、Question、Need 字符串、keyword、substring、scenario、case 或 fixture name 生成策略；
- 无 explicit governed acquisition basis 时不猜测、不生成 candidate；
- 同一 Branch / Need 可保留多个 strategy candidates，不 winner-take-all、不排序、不赋 priority；
- `DEFERRED` / `REJECTED` Branch 不形成策略，原 Branch identity、lineage、provenance 不被修改；
- Strategy candidate 与 Information Need、Branch、Attention、Observation Demand、Capability Requirement、Task、Action 保持语义分离；
- capability class 与 opportunity 仅作为 refs 保存，不执行 resolution、feasibility、scheduling 或 acquisition；
- 不实现 Resource Merge、Strategy Coordination、Commonality、Convergence、Merge、Close、Reopen 或 Branch lifecycle；
- 不输出 camera/body movement、turn、move 或其他 physical execution command；
- 不修改 Hypothesis、Need、Required Conditions、Current World、Field、Self、Memory 或 PCN；
- 不声明 Field Truth、World Truth 或其他 Truth；
- 不调用 Provider、Model、Observation、Decision、Task 或 Action runtime；
- 不创建 autonomous child runtime；
- B-route mode candidate 不等于 A-route evidence，不写入 A-route Current World；
- 所有输入与输出保持 candidate-only、read-only、immutable semantics。

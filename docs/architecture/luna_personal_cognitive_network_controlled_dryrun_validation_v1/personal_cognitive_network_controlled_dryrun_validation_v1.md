# Personal Cognitive Network Controlled DryRun Validation v1

Status: CONTROLLED_VALIDATION_CANDIDATE

## 当前工作内容

本阶段为现有 PCN Controlled Skeleton 建立受控 DryRun Harness、12 场景期望注册、DryRun 输入输出合同、嵌套约束验证合同、资源降级验证合同、Interaction 边界验证合同、Clarification 继承验证、DryRun 结果 Schema、Runner 与 Result Verifier。

## 架构位置

- Reuse Core Skeleton: capabilities/midplatform/core/personal_cognitive_network/
- Validation Assets: docs/architecture/luna_personal_cognitive_network_controlled_dryrun_validation_v1/

## DryRun 链路

Synthetic Fixture -> PCN Skeleton Run -> Candidate Outputs -> Case Evidence -> Trace -> Result Verifier.

该链路仅验证合同一致性，不代表 Runtime 功能实现。

## 12 场景

覆盖：天气最小激活、家庭临时加班、长期重复加班、夫妻与同事并存、离婚后同事并存、会议触发历史关系、工作场共鸣、父亲与员工竞争、夫妻创业重叠共存、休眠旧友重激活、主观错误认知、资源高低降级对比。

## 嵌套约束

覆盖关系：Context↔PCN、Field↔Role、Role↔Relationship、Memory Ref↔PCN、Resource↔PCN、Interaction↔PCN、Observation Axis Ref↔Interaction。

双向约束仅表示约束与反馈，不表示双写权限。

## 资源降级

验证资源仅影响激活范围，不影响 truth，不删除 source，不删除 dormant 数据，不修改核心 field。

## Interaction Boundary

PCN 仅消费/传递 Interaction Candidate Reference。

interaction_kernel_executed=false
interaction_kernel_owned_by_pcn=false

## Known Limitations

- 不实现真实 PCN Runtime。
- 不实现 Graph Algorithm / NetworkX / GraphDB / CNN / GNN。
- 不实现 Causal / Intent / Decision / Emotion Runtime。
- 不接入真实 Memory / Field Runtime / Persistence。

## Stop Condition

完成全部 DryRun 代码资产、合同资产、映射与 verifier 后即停止；Agent 不执行 runner/verifier，等待用户终端执行。

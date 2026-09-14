# Change manifest

## Added

- Provider Governance `provider_binding_decision_v1.py`。
- Runtime Executor `runtime_allocation_execution_instance_v1.py`。
- Controlled evaluation package `provider_binding_runtime_allocation_execution_instance_controlled`。
- 本目录架构与验证文档。

## Modified

- Governance Backbone 增加 controlled mechanical-authority profile 维度，使
  authoritative mechanical records 不被误判为 runtime invocation。

## Reused / not modified

- Provider Binding/Target Preparation、Runtime Allocation/Execution Preparation、
  Runtime Grant、Provider Governance、Runtime Executor、FPO、Gateway contracts。
- cognition、Observation Demand、Capability、Routing、FPO runtime、Gateway runtime、
  Model/Provider invocation 均未改。

## Deferred

真实资源分配、Execution process/session、Provider/Model binding invocation、Gateway
ingress、Observation、Evidence、World/A reassessment，以及完整 lifecycle/reclaim。

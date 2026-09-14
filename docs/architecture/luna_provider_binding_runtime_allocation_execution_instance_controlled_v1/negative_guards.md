# Negative guards

本 phase 不做 Provider/Model selection 或 invocation、resource/slot reservation、
GPU/CPU/process allocation、session start、Gateway submission、Observation/Evidence
production、Truth/World mutation、Decision/Task/Action、ranking、scoring、winner、
fallback、semantic inference。Requester 不选择 GPU/worker；Provider Governance 不
分配资源；Runtime Executor 不改写 Demand/Capability/FPO semantics。

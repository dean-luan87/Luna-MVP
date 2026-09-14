# Controlled fixtures

Evaluation package 覆盖 35 个 cases：

- governed phase、no applicable rule、unknown owner/source、orphan rule、invalid/malformed profile/rule；
- authority/responsibility pair、missing owner、collision、owner mismatch；
- candidate-only、authority attempt、no-runtime、no-truth；
- requester/executor complexity 与 adapter semantic boundary；
- Gateway `RUNTIME_OBSERVATION_INGRESS_ADMISSION` boundary，不将 Gateway 误标为 pre-execution authority；
- unified final decision、waiting status separation、deterministic replay；
- Provider Binding Runtime Preparation reference candidate。

Provider reference 仅作为 candidate-only regression input，不形成 Binding、Allocation、Execution Instance、Session、Gateway admission 或 Provider/Model invocation。

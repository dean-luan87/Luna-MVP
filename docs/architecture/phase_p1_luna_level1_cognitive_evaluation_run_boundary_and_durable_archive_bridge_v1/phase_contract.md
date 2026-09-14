# Phase Contract

This phase implements an evaluation-only run boundary and immutable archive bridge. It must stop before real Dataset ingestion and real cognitive execution.

Allowed: reference validation, candidate composition, White-box V1 attachment, archive serialization, synthetic Runner, and static Verifier.

Forbidden: model/provider/Observation/Action/runtime execution, network, dataset download, runtime mutation, Model/Provider binding changes, new cognition owners, automatic Knowledge/Experience promotion, and treating synthetic output as cognitive PASS.

The run boundary may present controlled evaluation inputs in a future approved ingress even though Dataset Registry infrastructure remains `runtime_allowed=false`; the registry itself never becomes a runtime owner.

Completion criterion: one explicit registered sample can be linked to one Level-1 case, represented as an evaluation run candidate, assigned an explicit A-Route readiness status, attached to existing White-box V1 refs, and written immutably outside `_eval_out`/`_tmp_eval_out`, without execution.


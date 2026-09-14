# A3 Evidence Context Translation Layer Negative Guard Regression Check v1

| guard | regression assertion | required static / serialized evidence | blocker condition |
| --- | --- | --- | --- |
| Guard-1 Evidence → Fact | candidate remains `candidate_only=true`, `fact_status=not_fact`, `translation_not_executed` | candidate boundary fields | Fact/confirmed/active state or write flag |
| Guard-2 Evidence → Decision | primitive type stays in candidate types; Decision/Action flags remain false | primitive type and flags | Decision/Action primitive, command, or flag |
| Guard-3 Provenance retention | source refs and trace are non-empty and preserved | provenance/trace closure chain | missing, hidden, or replaced source/trace |
| Guard-4 Provider identity | provider is stored only under source-capability provenance and never as candidate identity | candidate ID/source-capability separation | provider/model identity becomes a Cognitive Entity |
| Guard-5 No mutation | Context/Snapshot/Field State/Memory flags remain false | serialized boundary flags | context/snapshot/state/memory mutation signal |

The existing independent Verifier must keep reading Serializer output only and must not import Runner or invoke Skeleton. Any weakening of a guard or its evidence is a blocker.

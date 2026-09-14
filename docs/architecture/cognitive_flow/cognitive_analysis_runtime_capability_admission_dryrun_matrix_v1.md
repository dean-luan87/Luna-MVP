# A3 Cognitive Analysis Runtime Capability Admission DryRun Matrix v1

| check_item | input | expected_result | failure_condition | evidence |
| --- | --- | --- | --- | --- |
| Registry reference | candidate `registry_ref` | existing L1 Registry file is reachable | missing or different Registry reference | Registry path and read-only validator result |
| Registry record boundary | Registry entries and candidate ID | record is absent; no write is attempted | duplicate ID or a claimed Registry write | `registry_record_exists=false`; `registry_write_applied=false` |
| Lifecycle consistency | candidate `lifecycle_state` | `candidate` only | any admitted/active lifecycle claim | lifecycle declaration and state-machine reference |
| Contract completeness | candidate `required_contracts` | Model/Skill, Permission, Runtime Boundary, and Output Candidate references present | required contract missing | static candidate mapping |
| Permission reference | Permission / Admission Contract reference | reference present, no grant applied | missing reference or permission grant | `permission_grant_applied=false` |
| Boundary consistency | assessment flags | no admission application, activation, Runtime execution, or authorization | any forbidden flag is true | output flags |
| Deterministic output | serialized assessment | canonical JSON is stable | serialization differs from canonical form | independent Verifier comparison |

The matrix evaluates governance readiness only. It never treats an assessment candidate as an actual L1 admission result.

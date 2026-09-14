# Cognitive Primitive Layer Skeleton Validation Matrix v1

| area | skeleton validation |
| --- | --- |
| Schema | required base fields, known primitive type, no forbidden authority field |
| Semantic boundary | candidate-only and `fact_status=not_fact` |
| Traceability | source/context references and provenance trace must be retained |
| Negative guard | no Fact/Decision/Action/State/Memory authority input or schema field |
| Permission boundary | static flags remain false; no Runtime/Provider/Field Kernel/Reducer invocation |

Validation is static and in-memory. It does not admit a Primitive or mutate a Field.


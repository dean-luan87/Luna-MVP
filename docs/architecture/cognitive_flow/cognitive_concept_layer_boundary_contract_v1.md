# Luna Cognitive Concept Layer Boundary Contract v1

## Input and Output

Input is only traceable Primitive Candidate, abstract Context reference, Relation reference, and retained provenance/trace. Output is only a traceable Concept Candidate. External raw Evidence, provider schema, model payload, Field State/Snapshot handle, Fact, Decision instruction, Action command, and Memory handle are forbidden.

## Primitive and Field Boundaries

Primitive Layer owns basic Entity/Relation/State/Event/Situation expression. Concept Layer owns Pattern/Meaning/Contextual Interpretation/Situation Understanding candidate expression. Field Kernel owns current world-state organization; Reducer owns all Field State mutation.

Concept Layer may not bypass governance into Decision, create/admit Fact, modify Field State, write Snapshot/Context, invoke Reducer, update Memory/Learning, or grant a consumer permission.

## Negative Guards

1. Primitive → Fact is forbidden.
2. Concept → Fact is forbidden.
3. Concept → Decision is forbidden.
4. Concept → Action is forbidden.
5. Concept must not modify Field State.
6. Concept must not write Memory.
7. Language Layer must not generate Concepts back into cognition.
8. Provider identity must not define Luna Concept taxonomy.

Existing L1 Traceability, Permission/Admission, Candidate I/O, and Runtime Boundary governance applies by reference. `runtime_authorized=false` remains unchanged.


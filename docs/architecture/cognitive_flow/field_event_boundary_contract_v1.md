# Field Event Boundary Contract v1

## Inputs

Permitted inputs are traceable Field View, Field Representation, Primitive, Concept, Context, and Temporal references. Raw model output, provider payload, Fact, State mutation command, Reducer command, Decision, Action, and Memory are prohibited.

## Output

Only a candidate-only Field Event may be emitted. It cannot directly enter Reducer. Admission owns candidate eligibility, duplicate/order/expiry/time sufficiency assessment, and the Candidate Event -> Admitted Event transition. Reducer receives only the admitted form.

## Permanent guards

1. Event Candidate is not Event Fact.
2. Event is not State mutation.
3. Field Kernel is not Event Authority.
4. Confidence is not Admission Authority.
5. Attention is not Event Trigger.
6. External model output cannot directly create Event.
7. Only Reducer mutates State.

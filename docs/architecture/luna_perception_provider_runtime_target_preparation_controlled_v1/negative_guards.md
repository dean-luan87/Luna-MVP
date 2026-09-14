# Negative guards

This phase does not perform Provider or Model binding, selection, ranking, scoring, fallback, activation, reservation, session start, execution-instance creation, Gateway admission, runtime admission, resource scheduling, provider/model invocation, camera/OCR/SLAM/VLM execution, evidence ingress/fusion, attention, task, decision, action, or state/memory/world mutation.

It does not infer a Provider from a capability or natural-language string, does not rematch or mutate upstream Capability Resolution, and does not merge demands. Every target must be backed by exactly one valid FPO Admission Compatibility Candidate. `candidate_only`, `read_only`, non-truth and all runtime guard flags remain explicit.

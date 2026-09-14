# Negative guards

The controlled integration verifies:

- no real provider/model invocation, network, subprocess, thread, socket, camera, OCR, YOLO, SLAM, or VLM effect;
- no provider retry, fallback, selection, or autonomous continuation;
- no semantic interpretation of opaque payloads;
- no Gateway-triggered execution;
- no evidence sufficiency decision;
- no Current World, Field, Context, Memory, Experience, Truth, Decision, Task, or Action mutation;
- `candidate_only`, `read_only`, `truth_declared=false`, and `world_truth_declared=false` boundaries;
- authority/responsibility mismatch fail-closed and preflight hard stop;
- malformed invocation, observation, Gateway input, provider, execution, and lineage references fail closed;
- Runtime Observation ≠ Gateway admission ≠ Evidence ≠ Truth.

The adapter has no semantic authority. The Gateway has runtime observation ingress authority only.

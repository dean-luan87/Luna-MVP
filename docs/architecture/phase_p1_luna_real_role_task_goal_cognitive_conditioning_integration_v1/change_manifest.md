# Change Manifest

## Added

- evaluation-only same-evidence Role/Task/Goal contrast types and definitions;
- real OCR-backed contrast engine;
- user-terminal Runner and fail-closed Verifier;
- native OCR content projection/fingerprint comparison;
- explicit Plane G reuse per contrast side.
- additive read-only Evidence-to-information support binding through Runtime ingress,
  Gateway admission, A-Route, and CState;
- fail-closed relevance/coverage consistency guards in the conditioning Verifier.

## Reused

- `RealOCRProviderExecutionEngineV1`;
- `ProviderObservationIngressCaseV1` and its explicit observation support binding;
- canonical ProviderRuntime request/result and RuntimeObservation path;
- Observation Gateway, A-Route and Cognitive State Formation;
- existing Plane G G01–G20 assertion set;
- existing role/task vocabulary from Full E2E Cognitive Logic Conformance Regression.

## Not changed

Provider Runtime、RapidOCR、Observation acquisition、Information Gap、Re-observation、
Stop 与 Plane G owner 均未修改。Cognitive State Formation input was extended additively
to carry read-only Evidence support bindings; no new scoring threshold or owner was added.
未创建 Task Manager runtime 或任何下游执行。

## Verification boundary

历史 144-check 终端结果在修复前为 PASS/GO；修复后状态为
`COGNITIVE_LOGIC_GAP_FIXED — WAITING_FOR_USER_TERMINAL_VERIFICATION`，等待重新验证。
Agent 未执行 Python、Runner、Verifier、Provider、Model、pytest 或 py_compile。

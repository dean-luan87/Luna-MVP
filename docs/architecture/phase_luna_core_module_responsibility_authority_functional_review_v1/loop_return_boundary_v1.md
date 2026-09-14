# Loop Return Boundary

Loop may return:

- Loop identity
- mechanical state
- Loop mechanical state version
- pending refs
- pause/wait records
- Requirement refs
- B request/branch/result refs
- closure status
- freeze ref
- Outcome ref
- history boundary
- trace/provenance

Loop must not generate `SUFFICIENT`, `REPLAN`, `REQUEST_MORE_EVIDENCE`, `SHOULD_CONTINUE`, `BEST_CAPABILITY`, `HYPOTHESIS_INVALID`, `BEST_PROVIDER`, or Concern split/merge judgments. Such semantics may appear only as externally supplied refs.

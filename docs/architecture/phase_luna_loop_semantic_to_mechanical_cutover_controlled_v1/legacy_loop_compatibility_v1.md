# Legacy compatibility boundary

The following legacy behavior remains for dependent fixtures and callers:

- `cognitive_loop_continuity_candidate_engine_v1._local_disposition()` — R1,
  compatibility computational source.
- `_continuity_and_resume()` — R1, compatibility computational source.
- lifecycle closure engine reason/disposition construction — R1, governed
  closure compatibility source.

None is deleted or rewritten in this phase. Retirement requires migration of
dependent fixtures/verifiers and a later controlled cutover review.


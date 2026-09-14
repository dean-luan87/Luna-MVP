# Negative Guard Audit

The regression covers LIVE_RUNTIME rejection, replay provenance/admission,
owner boundaries, revision-without-Gap/Re-observation, premature Stop,
unjustified Re-observation, post-sufficiency over-observation, archive identity
conflict semantics, and forbidden model/provider/live-observation/action/
Field/World Truth/promotion claims.

Where code contains a guard but no executable current test exists, the report
uses `GUARD_PRESENT_TEST_COVERAGE_MISSING`; it does not count the guard as
tested. Archive conflict is inspected read-only because intentionally creating
a divergent record would be destructive to the test history.

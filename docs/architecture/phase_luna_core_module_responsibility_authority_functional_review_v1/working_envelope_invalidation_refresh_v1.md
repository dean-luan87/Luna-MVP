# Working Envelope Invalidation and Refresh v1

Triggers include Grant expiry/revocation, Concern supersession/closure,
Intent or Role change, Perspective projection invalidation, Field/Context/
Current World change, Task constraint change, Safety/Permission/Resource change,
stale Evidence, and stale Diagnostics.

The Envelope may report stale, invalid, partially invalid, refresh-required,
or superseded. It stops at declaring the binding no longer current. It must
not infer REPLAN, request evidence, stop/sufficiency, or Concern closure.

Target lifecycle: source change → invalidation → new Envelope Candidate →
governance/admission validation → new Envelope Version → old version
superseded. No automatic daemon or scheduler is introduced.

# Unified final decision

Runner status is `READY_FOR_USER_VERIFICATION` and only reports that the
artifact was generated. The verifier computes the final decision through the
Governance Backbone helper. `GO` requires all functional checks, empty
contract failures, Governance preflight and postflight `PASS`, and both
cognitive and operational results `PASS`; otherwise the result is `NO_GO`.

This keeps `GRANTED` (a business authorization decision) separate from the
evaluation final decision and from runtime start.

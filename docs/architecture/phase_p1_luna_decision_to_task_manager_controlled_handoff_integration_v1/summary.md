# Summary

The integration reuses the verified cognition-to-Decision composition and
submits only selected, eligible Decision Candidates to the existing Task
Manager module. Case A creates one controlled Task state after first-cycle
cognition. Case B creates no Task handoff during the insufficient cycle and
creates one after final Sufficiency and Stop. Action remains deferred.

The admission remediation preserves the canonical `missing_trace` guard while
making its existing mapping input readable and carrying the selected Decision
trace into the Task Manager input candidate. The negative fixture now reports
rejection from the actual rejected handoff. Full runtime status remains
WAITING_FOR_USER_TERMINAL_VERIFICATION until the Runner is regenerated.

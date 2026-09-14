# Loop Grant Validation Boundary

Loop may mechanically reject commands for:

- missing/invalid grant ref;
- wrong Concern or Work scope;
- stale/mismatched Loop mechanical state version;
- revoked or expired grant;
- missing required source ref;
- duplicate command;
- invalid mechanical transition;
- cross-loop contamination.

“This work is no longer valuable,” “the evidence is sufficient,” or “the best next step is replan” are semantic/global judgments and are not Loop rejection reasons unless supplied as an external decision ref.

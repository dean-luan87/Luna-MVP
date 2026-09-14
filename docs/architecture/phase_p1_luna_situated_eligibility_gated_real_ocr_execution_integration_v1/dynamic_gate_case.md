# Dynamic Gate Case

`DYNAMIC_SITUATED_STATE_OPENS_REAL_OCR_GATE` keeps the same Goal, Intent,
Concern, Information Need, Capability Requirement, Provider, Model, and local
source image across two controlled situated states.

- `t0`: target scale is `SMALL`; derived scale condition is unsatisfied;
  Eligibility is false; no OCR invocation occurs.
- `t1`: only the situated target scale candidate changes to `ADEQUATE`;
  Eligibility becomes true; the real OCR call occurs once.

The Runner reports execution events so the Verifier can check that the gate is
evaluated before provider invocation and that the dynamic case has exactly one
real provider/model invocation.

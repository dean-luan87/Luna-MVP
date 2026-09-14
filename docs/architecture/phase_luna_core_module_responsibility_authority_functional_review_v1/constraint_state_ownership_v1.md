# Constraint State Ownership v1

| Domain | AUTHORITATIVE | CANDIDATE/REFERENCE | EXTERNAL |
|---|---|---|---|
| Safety | Brain policy, protected rules, override/revocation | risk evidence, admission result | Perception/Diagnostics/human sources |
| Permission | Brain/global policy; scoped Permission governance | identity evidence, grant/deny/ref, revocation candidate | Role/Identity/external authority |
| Resource | Brain policy, ceilings, reserves | budget/reservation/degradation candidate | Diagnostics/runtime consumption |

Local consumers may derive readiness/block status but cannot mutate policy.

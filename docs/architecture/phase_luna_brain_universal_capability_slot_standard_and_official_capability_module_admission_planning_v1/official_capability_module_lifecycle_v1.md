# Official Capability Module lifecycle

Module lifecycle is distinct from Slot lifecycle and admission stages:

`DEFINED -> AVAILABLE -> ADMISSION_CANDIDATE -> ADMITTED -> INSTALLED -> BOUND -> ACTIVE`

Possible governed states include `SUSPENDED`, `DEGRADED`, `INCOMPATIBLE`,
`RELEASED`, `RECOVERY_CANDIDATE`, `ROLLED_BACK`, and `RETIRED`.

`OFFICIAL_MODULE_AVAILABLE` does not imply admitted, installed, bound, or
active. No automatic Hive publication-to-install transition is defined.

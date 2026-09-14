# Policy / Enforcement Findings v1

The controlled consolidated regression encodes precedence as `HARD_SAFETY`, `HARD_PERMISSION`, `GRANT_VALIDITY`, `PROTECTED_RESOURCE`, `RESOURCE_OPTIMIZATION`, `LOCAL_PRIORITY` (`cross_module_checks_v1.py:14-17`). Action Governance checks permission before safety/resource readiness and Runtime Executor rechecks readiness, permission, safety, confirmation and scope before producing an execution candidate.

The audit found no proven path where local Attention/Task priority weakens a hard constraint. However, the repository contains many historical governance/planning assets and separate guarded-trial gates. Their actual active policy callers were not proven uniformly. Classification: `SUPPORTED_BUT_PARTIAL`, severity `P2`; no policy owner change.


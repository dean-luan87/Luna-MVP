# Action Result Return Boundary v1

Action Result is treated as an external candidate result, not proof of world change. The adapter preserves success, partial, failed, uncertain, unverified, and stale status without converting any status into source-state success.

- Verified effect Evidence may produce independent Current World/Field candidates.
- Successful but unverified effect produces an unverified candidate status without fabricated evidence.
- Partial, failed, and uncertain results remain qualified candidates.
- Stale Action Results are blocked from inappropriate source-state candidate creation.

Action Governance/Provider remain responsible for execution correctness. The return adapter is responsible only for mapping and lineage.


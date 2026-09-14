# Role / Perspective / Intent / Task Boundary v1

Role/Perspective changes propagate as applicability candidates:

`Role/Perspective version → Intent applicability candidate → Intent Governance
adjudication`.

Intent Governance cannot create Role identity. Task may require a Role,
permission, ownership relation, or perspective-conditioned constraint, but
cannot create or mutate Role. A Role change may affect Task readiness through
refs; it does not directly mutate Task.

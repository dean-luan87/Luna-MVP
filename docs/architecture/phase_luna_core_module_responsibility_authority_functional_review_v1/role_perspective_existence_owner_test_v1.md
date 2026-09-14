# Role / Perspective Existence and Owner Test v1

| Option | Finding |
|---|---|
| independent Role/Perspective Manager | unnecessary runtime owner at present |
| Role owned by Context | incomplete; Context supplies applicability, not identity in every case |
| Role owned by Brain | incorrect; Brain governs policy, not all identity source state |
| Role owned by Intent/Task | incorrect; both consume Role refs |
| external source state + governance contract | preferred for Role |
| one Role/Perspective owner | risks conflating identity with projection |
| split domains | preferred: source-owned Role plus derived Perspective |

The irreducible responsibility is stable Role reference and applicability
provenance plus a consistent Perspective projection contract. Current assets
do not justify a new Manager. Existing `role_refs` and `perspective_refs` in
the Working Envelope are the correct transport shape.

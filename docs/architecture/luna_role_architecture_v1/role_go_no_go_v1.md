# Role Architecture Go/No-Go

## Readiness criterion

`LUNA_ROLE_ARCHITECTURE_READY` is emitted by the user-owned V2 verifier only when Role schema, registry, activation, lifecycle, Field binding, Memory/Knowledge relations, Self/Social boundary, B interface, and negative guards are complete.

## No-go conditions

- Role exists without Field context;
- Role rewrites Identity or Constitution;
- Knowledge directly creates or activates a Role;
- Memory directly changes Role or Decision;
- Emotion creates a Role;
- B Route switches or activates a Role;
- Role Runtime, automatic learning, Emotion/Social Runtime, or Action is implemented.

The agent stops at `WAITING_FOR_USER_TERMINAL_VERIFICATION` and does not declare a final GO decision.

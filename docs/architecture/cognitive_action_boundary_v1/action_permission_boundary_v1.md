# Action Permission Boundary v1

## Permission classes

| Class | Examples | Required handling |
|---|---|---|
| Low-risk candidate | query weather, adjust observation frequency | automatic-permission candidate, still traceable |
| Medium-risk candidate | navigation support, resource reallocation | capability and constraint validation |
| High-risk candidate | payment, delete data, change environment, movement | explicit authorization candidate from Brain/User |
| Safety candidate | urgent hardware protection signal | Neural Fast Path candidate; no automatic execution here |

Permission is a candidate, not an Action. Risk classification cannot change
Goal or Decision. An Action Request without required authorization is rejected
or held for review. Provider, Capability, Runtime, and Neural cannot grant
themselves permission.

Action Permission Boundary does not control hardware, send external commands,
move a robot, make payment, delete data, or operate an external system. The
Reducer remains the sole State mutation authority.


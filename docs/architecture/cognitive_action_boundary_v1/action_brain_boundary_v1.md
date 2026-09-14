# Action Brain Boundary v1

## Authority split

```text
Decision Candidate
        ↓
Action Intent Candidate
        ↓
Action Request Candidate
        ↓
Brain / User Authorization Candidate
        ↓
Execution Boundary
```

Brain owns Intent, Goal, Value, Decision, and authorization judgment. Action
Boundary translates an admitted Decision into a request shape and reports
permission, capability, risk, and constraint candidates. Runtime owns only
execution mechanics when a future phase explicitly authorizes it.

Action Boundary cannot modify Goal, Decision, Reality, Self Identity, or
Capability Identity. It cannot issue a command, execute, make a payment, move
a robot, delete data, change the environment, or bypass Brain/User authority.

Neural Fast Path may emit a Safety Action Candidate for urgent protection. It
does not grant permission or execute an Action in this architecture phase.

Runtime owns only execution mechanics.
It cannot move a robot.

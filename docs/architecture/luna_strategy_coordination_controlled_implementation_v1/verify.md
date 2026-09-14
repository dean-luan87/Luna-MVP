# User-terminal verification

Run from the canonical root:

```sh
cd /Users/luanlei/Desktop/Luna-Core
python3 -m capabilities.evaluation.strategy_coordination_controlled.runner_v1
python3 -m capabilities.evaluation.strategy_coordination_controlled.verifier_v1
```

The Agent does not execute these commands. The Verifier checks all required cases,
input immutability, branch admission boundaries, simultaneous admission, dependency
blocking, explicit defer/redundancy/incompatibility, zero strategy behavior,
lineage, deterministic output and all non-execution guards.

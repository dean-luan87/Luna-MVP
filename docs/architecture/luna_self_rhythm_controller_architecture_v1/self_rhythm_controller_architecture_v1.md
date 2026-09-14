# Luna Self Rhythm Controller Architecture v1

## Position

Self Rhythm Controller belongs to `L2 Self Layer → Self Regulation` as an architecture-only extension. It represents how Luna should pace its own cognitive resources; it is not an emotion engine, personality system, task scheduler, or hardware controller.

## Responsibilities

The controller evaluates Self State, Resource State, Runtime Health, Capability Health, and External Demand, then emits a candidate runtime mode and resource budget hint. It does not force the runtime to accept the hint and does not choose a model or provider.

## Runtime modes

- `active`: ordinary interaction and high-priority events;
- `focus`: bounded high cognitive investment;
- `observe`: low-frequency environmental observation;
- `maintain`: health, calibration, and organization candidates;
- `recovery`: degraded/recovery-oriented operation;
- `low_power`: minimal resource consumption during long waits or scarcity.

Modes are state candidates. Constitution, Safety, Runtime Governance, and Self Regulation remain higher constraints.

## Control relationship

```text
Health Observation → Self Regulation → Self Rhythm Controller
→ Runtime Resource Adjustment Hint
```

Self Regulation handles abnormality and failure. Self Rhythm handles pacing and resource posture. Neither changes Brain rules, Identity, Value, Goal, or Constitution.

## Resource budget

Budgets cover CPU, GPU/NPU, memory, battery, storage, network, attention, and capability intensity. They are advisory envelopes, not direct controls. Runtime may reject or constrain a hint.

## Boundaries

The controller may emit mode, budget, and trace candidates. It may not modify scheduler implementation, hardware, model/provider selection, Brain decision logic, Emotion state, Social state, Learning state, or Action state.

## Verification authority

This phase is Architecture Only. Agent performs V0 static checks. User Terminal runs V2. ChatGPT performs V3 audit. No runtime behavior is implemented here.

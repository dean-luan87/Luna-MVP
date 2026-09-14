# Temporal Understanding / Neural Regulation Boundary v1

## Responsibility split

| Layer | Responsibility | Does not own |
|---|---|---|
| Temporal Understanding | describe world change, stability, trend, and temporal uncertainty candidates | tempo control, allocation, scheduling, activation |
| Situation | express how temporal change may affect the current subject and Goal | Decision or Action |
| Neural Regulation | interpret admitted Situation Risk Candidate and propose response-strength candidates | temporal facts, predictions, hardware control |
| Middleware / Hardware governance | evaluate and execute capability/resource/device constraints | cognitive priority or final judgment |

## Permitted relation

```text
Temporal Understanding Candidate
        ↓
Situation Risk Candidate
        ↓
Neural Regulation Candidate
        ↓
Tempo Adjustment Candidate
```

The final two nodes remain future governance interfaces. Temporal Understanding
does not create a Tempo Adjustment Candidate, change frequency, invoke a
Scheduler, or control hardware.

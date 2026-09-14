# Cognitive Assembly Classification Model v1

| Class | Purpose | Priority / resource posture | Interrupt relation |
|---|---|---|---|
| P0 Safety Assembly | Safety, device, environment risk understanding | Highest cognitive priority candidate; bounded core presence | May emit interrupt candidates. |
| P1 Goal Assembly | Goal-linked understanding, navigation, search | Active while relevant | May be refined by an interrupt candidate. |
| P2 Observation Assembly | Low-resource environment or user-state observation | Background candidate | Reports change candidates only. |
| P3 Learning Assembly | Experience validation and template extraction | Lowest real-time priority | No direct interruption or learning mutation. |

Classification is not a Scheduler priority or Action authority.

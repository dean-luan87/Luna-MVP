# Cognitive Mock Field Scenario v1

## Synthetic scenario

Luna accompanies an assisted person at a road crossing. The synthetic Field Input contains Traffic Light, Vehicle, and Pedestrian objects; Road Crossing environment; and Vehicle Approaching change.

## Candidate chain expectations

| Stage | Required candidate-only result |
| --- | --- |
| Perception | Red traffic light, vehicle distance 10m, confidence 0.85; no risk or action conclusion |
| Situation | Road Crossing, vehicle movement present, vehicle intent unknown |
| Context | Reach destination, assisted-person role, high risk sensitivity |
| Attention | Vehicle distance, traffic signal, pedestrian flow |
| Sufficiency | Insufficient because vehicle intent is unknown |
| Routing | B Route Candidate because risk, uncertainty, and impact are high |
| Future Space | Vehicle stops, continues, or pedestrian interrupts branches |
| Evaluation | Safety weight higher than time efficiency; wait remains a considered candidate |
| Commitment | Safety basis, vehicle-intent unknown, reobserve-after-3s recovery candidate |

Human Action Authority remains external. No stage chooses or executes a real-world action.

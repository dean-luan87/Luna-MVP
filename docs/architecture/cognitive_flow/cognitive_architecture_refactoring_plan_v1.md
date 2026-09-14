# Cognitive Architecture Refactoring and Encapsulation Plan v1

## Purpose

This Planning Only review reorganizes existing A-route cognitive modules into seven subsystem architecture views. It does not move code, change contracts, add capability, modify an architecture decision, or create Runtime behavior.

## Subsystem architecture view

```text
                    Cognitive Governance System
                               |
 -----------------------------------------------------------------
 |                 |                 |                 |
 Perception &      Context &         Attention &       Reasoning &
 Situation         Intent            Cognitive          Future
 Understanding     Understanding     Resource           Simulation
 System            System            Management         System
                                     System
 -----------------------------------------------------------------
                               |
                 Evaluation & Decision Support System
                               |
              Experience & Representation Evolution System
                               |
                         Future Adaptation
```

Field, Reducer, future Emotion, and future Hive remain independent architecture boundaries, not enclosed subsystem members.

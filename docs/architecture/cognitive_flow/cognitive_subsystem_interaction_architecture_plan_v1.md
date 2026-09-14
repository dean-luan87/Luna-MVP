# Cognitive Subsystem Interaction Architecture Plan v1

## Purpose

This Planning Only phase defines the L2 Cognitive Interaction Protocol for the seven A-route subsystem views. It specifies candidate signal flow, request-response interaction, dependency direction, authority separation, future interfaces, and orchestration boundaries without adding a capability or Runtime.

## Interaction principle

Subsystems exchange governed candidate signals and requests; they do not issue direct semantic commands to one another. A subsystem may request candidate support, return candidate output, preserve uncertainty, or decline/defer a request candidate.

## Core interaction view

```text
Field -> Perception -> Context
                     |  \
                     |   +-> Experience candidate request/response
                     +----> Attention candidate request/response
                               -> Reasoning/Future candidate request/response
                               -> Evaluation/Decision Support candidate request/response
                               -> Experience/Evolution candidate request/response
Governance reviews boundaries across every candidate exchange.
Reducer remains outside Cognitive Judgment and is the only State Mutation Authority.
```

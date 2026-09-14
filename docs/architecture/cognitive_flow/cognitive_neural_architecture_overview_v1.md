# Cognitive Neural Architecture Overview v1

## Phase and position

- Phase: `Phase-Cognitive-Neural-Architecture-Planning-v1-001`
- Execution mode: Planning Only / V0.
- Cognitive Neural Architecture is an independent information-transport, classification, governance, and adaptation layer.
- It is not Cognitive Brain, Cognitive Middleware, a Capability Provider, or a Runtime.

## Architectural purpose

The Brain forms cognitive intention; the Neural Layer carries and regulates candidate-shaped signals; Middleware resolves bounded capability; the embodied/external layer supplies raw capability results and health feedback. The Neural Layer gives these exchanges a stable signal vocabulary, compatibility boundary, trace form, and authority contract.

```mermaid
flowchart TB
    subgraph Brain[Cognitive Brain]
        context[Context]
        goal[Goal]
        attention[Attention Controller]
        workspace[Workspace]
        simulation[Simulation]
        evaluation[Evaluation / Feedback]
    end

    subgraph Neural[Cognitive Neural Architecture]
        manager[Neural Protocol Manager]
        cognitivepath[Cognitive Neural Path]
        perceptionpath[Perception Neural Path]
        reflexpath[Reflex Neural Path]
        simulationpath[Simulation Neural Path]
        taxonomy[Signal Taxonomy / Boundary Validation]
        manager --> taxonomy
        taxonomy --> cognitivepath
        taxonomy --> perceptionpath
        taxonomy --> reflexpath
        taxonomy --> simulationpath
    end

    subgraph Middleware[Cognitive Middleware Control Plane]
        cm[Capability Manager]
        rm[Resource Manager]
        eg[Evidence Gateway]
        ma[Model Adapter]
        hm[Hardware Management]
    end

    subgraph Body[Capability Provider / Hardware Body]
        providers[OCR / Vision / VLM / SLAM / ASR]
        devices[Camera / IMU / ToF / Audio / Battery / Compute]
    end

    goal --> cognitivepath
    attention --> cognitivepath
    context --> cognitivepath
    cognitivepath --> cm
    cm --> ma
    cm --> hm
    ma --> providers
    hm --> devices
    providers --> eg
    devices --> eg
    eg --> perceptionpath
    perceptionpath --> workspace
    evaluation --> cognitivepath
    devices --> reflexpath
    providers --> reflexpath
    rm --> reflexpath
    reflexpath --> attention
    simulation --> simulationpath
    simulationpath --> workspace
```

## Neural Layer authority

The Neural Layer may:

- transport signals between bounded layers;
- classify signals by type, direction, urgency, lifecycle, and authority envelope;
- validate signal boundary/compatibility/trace requirements;
- adapt signal representation through approved candidate-compatible versions;
- expose signal feedback for Brain and Middleware consumption.

The Neural Layer may not own:

- Goal Authority;
- Decision Authority;
- Truth Authority;
- Action Authority;
- Runtime execution authority;
- Reducer/State mutation authority.

## Status

`COGNITIVE_NEURAL_ARCHITECTURE_OVERVIEW_READY_WITH_NOTES`

`WAITING_FOR_USER_TERMINAL_VERIFICATION`

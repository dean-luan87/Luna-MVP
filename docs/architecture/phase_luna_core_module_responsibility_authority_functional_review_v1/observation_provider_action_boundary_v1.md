# Observation / Provider / Action Boundary v1

Observation acquires information; Action changes external/system state.
Camera capture and microphone listening are Observation. Moving a camera
actuator, speaking, sending a mutating API request or moving physically are
Action. Reading API state is Observation-like acquisition; writing API state is
Action.

Shared Provider infrastructure is allowed only when source contracts remain
explicit.

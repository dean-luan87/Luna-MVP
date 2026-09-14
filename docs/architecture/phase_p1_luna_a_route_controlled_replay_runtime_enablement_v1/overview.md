# Controlled Replay Runtime Enablement

This phase adds the smallest governed `CONTROLLED_REPLAY_RUNTIME` path to the existing canonical A-Route stack. It preserves `SYNTHETIC_CONTROLLED`, declares but rejects `LIVE_RUNTIME`, and does not integrate Evaluation, Archive, live sensors, models, Providers, or Action.

The path is:

`frozen replay refs → Observation Gateway admission → ARouteIngressRefsV1 → A-Route → Cognitive State Formation → canonical cognitive execution evidence`


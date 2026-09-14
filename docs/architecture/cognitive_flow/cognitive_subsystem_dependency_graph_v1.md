# Cognitive Subsystem Dependency Graph v1

```text
Perception & Situation
  -> Context & Intent
      <-> Attention & Resource (candidate requests/responses)
      <-> Experience & Evolution (pattern/guidance requests/responses)
      -> Reasoning & Future (candidate requests/responses)
          <-> Evaluation & Decision Support (candidate requests/responses)
              -> Experience & Evolution (outcome/feedback candidates)

Cognitive Governance reviews all subsystem-boundary candidates.
Field is a world-description foundation; Reducer is external State authority.
```

`<->` describes candidate exchange, not synchronous direct-call dependency or mutual authority. No subsystem may create a circular command, action, or State mutation path.

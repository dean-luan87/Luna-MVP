# Cognitive Attention Competition Model v1

## Competition

Multiple Attention Requests may exist at once:

```text
Attention Request A
        + Attention Request B
        + Attention Request C
                 ↓
       Attention Competition
                 ↓
        Arbitration Candidate
                 ↓
          Resource Allocation
```

Competition records each request's source, Field, Survival Impact, Goal
Relevance, Information Value, Uncertainty, Resource Cost, persistence, and
current status. It preserves losing and deferred requests; losing is not
deletion and does not imply the information is unimportant.

## Conflict boundary

Coding Attention versus Threat Attention is a competition example. Threat
Attention may request Mandatory Attention and preemption. Attention does not
decide whether the threat is real, what the user should do, or which Action to
execute. A Route and Brain retain interpretation and Decision authority.

No multi-A coordination, role competition, emotion runtime, or social field
runtime is implemented.

Attention does not decide a response. Preemption is a candidate transition;
it does not become a Decision or Action.

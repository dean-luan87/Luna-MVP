# B-CR Existence Test

| Architecture | Authority clarity | Boundedness | Observability | Replaceability | Model independence | Second-A risk | Complexity |
|---|---|---|---|---|---|---|---|
| A. Independent B module | high: A owns request/adoption | explicit grant/depth/branch/budget | strong request/result/trace | high | high | controlled by non-binding contract | medium |
| B. Internal A subroutine | medium: easy to blur A/B ownership | possible but less visible | weaker boundary | lower | high | high; can become second-A logic | low initially, high later |
| C. Generic external Provider | low for semantic responsibility | provider contract alone insufficient | execution-focused | high technically | provider-dependent | high; treats reasoning as execution | medium |

## Decision

B deserves an independent canonical module boundary because bounded contingency exploration has distinct scope, budget, safety, failure, provenance, and replaceability requirements. It must remain narrow and A-governed. This is not permission to create a second global or local cognition owner.

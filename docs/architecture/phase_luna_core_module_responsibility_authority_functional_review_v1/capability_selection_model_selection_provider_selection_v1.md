# Capability Selection vs Model Selection vs Provider Selection v1

| Selection | Meaning | Owner |
|---|---|---|
| Capability selection | functional ability appropriate for a requirement | Capability Governance, from A/Task requirement |
| Model selection | concrete governed asset fulfilling that capability mapping | Model Manager / mapping contract |
| Provider selection | runtime execution implementation | Provider Governance |

“Select capability” must never silently mean “select YOLO.” A capability may be
object detection while the Model Manager maps several assets and Provider
Governance chooses an admissible execution provider.

Runtime Admission assesses supplied implementation evidence; it does not create
a hidden model/provider selection authority.

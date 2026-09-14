# Reality Cognition System Internal Boundary Contract v1

| Internal module | Sole internal purpose | Non-penetration rule |
|---|---|---|
| World Model | describe represented external state | cannot know/choose what Luna should do |
| Self Model | describe subject capability, limitation, and state context | cannot select a choice or become Registry/Memory |
| Situation Understanding | describe current world–self–goal relation | cannot act or decide |
| Decision Formation | compare option/evaluation candidates | cannot execute or control hardware |
| Execution Boundary | describe future request/status/outcome handoff | cannot implement an Action |
| Outcome Observation | organize represented post-boundary evidence | cannot judge success or correct behavior |
| Value / Experience Feedback | form feedback and consolidation candidates | cannot modify Self, Strategy, or State directly |

Internal modules communicate through candidate contracts and trace references.
No module may skip a boundary, convert evidence into fact, mutate State, or
gain authority from its position in the system.

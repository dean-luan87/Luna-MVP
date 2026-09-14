# Legacy Loop Continuity Full Audit

| Current behavior | Semantic effect | Target owner | Loop residual | Readiness |
|---|---|---|---|---|
| `_local_disposition()` | derives SUFFICIENT/RECONSIDER/DEFER/INSUFFICIENT | A | record supplied disposition ref | R1 |
| `_continuity_and_resume()` | selects KEEP/REPLAN/SUPERSEDE/WAITING | A/Brain | resume/record supplied command | R1 |
| closure reason construction | derives semantic closure meaning | A/Brain/governance | close/freeze/archive supplied acceptance | R1 |
| closure acceptance | global closure judgment | Brain/governance | apply accepted close | R2 |
| growth guards | mixed resource/semantic judgment | A/Brain/Resource governance | record reservation/status | R1-R2 |
| capability-path status | Capability/A semantics | Capability/A | record path refs/status | R2 |
| reconsideration construction | A semantic reconsideration | A | record ref | R1 |
| state version creation | lineage/bookkeeping | Loop/State Formation split | persist own domain/version refs | R2 |

No helper is deleted in this review. No candidate is R5.

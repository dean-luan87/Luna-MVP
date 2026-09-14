# A to Loop Mechanical Mapping

| A decision | Mechanical mapping |
| --- | --- |
| Current Need selected | `RECORD_NEED_REF` |
| `SUFFICIENT` | `CLOSE` + `FREEZE_FINAL_STATE` |
| `INSUFFICIENT` | record supplied sufficiency reference |
| `REQUIRES_RECONSIDERATION` | record supplied reconsideration reference |
| `CONTINUE` | record pending candidate |
| `REQUEST_MORE_EVIDENCE` | record pending reference only; no Provider call |
| `REPLAN` | record state version and replacement Need |
| `WAIT` / `DEFER` | mechanical `WAIT` |
| `PAUSE` | mechanical `PAUSE` |
| `STOP_SUFFICIENT` | `CLOSE` + `FREEZE_FINAL_STATE` |

The Loop adapter does not infer any semantic value from stored state.

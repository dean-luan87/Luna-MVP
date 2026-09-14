# Resume semantic cutover

The legacy `_continuity_and_resume()` helper currently constructs a semantic
resume decision. In this seam its output is accepted only as a compatibility
source. A supplies one of `KEEP`, `REPLAN`, `SUPERSEDE`, `COMPLETE`, or
`WAITING` in `LoopResumeMechanicalInputV1`.

Mapping:

| supplied semantic value | mechanical command(s) |
| --- | --- |
| KEEP | `RESUME_KEEP` |
| REPLAN | `RECORD_STATE_VERSION` + `RECORD_NEED_REF` |
| SUPERSEDE | existing `SUPERSEDE_REQUIREMENT` |
| COMPLETE | `CLOSE` + `FREEZE_FINAL_STATE` |
| WAITING | `WAIT` |

`SUPERSEDE_RECORDED_REF` is the integration-level meaning; no canonical
command vocabulary is expanded.


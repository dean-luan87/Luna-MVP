# Status taxonomy

| Status | Meaning | Not meaning |
| --- | --- | --- |
| `ADMITTED` | allowed for downstream consideration | executing, scheduled, winner |
| `DEFERRED` | valid but temporarily withheld | rejected, deleted |
| `SUPPRESSED_REDUNDANT` | explicit governed duplicate suppression | semantic similarity or winner selection |
| `BLOCKED_DEPENDENCY` | explicit dependency coverage is missing | resource execution or capability resolution |
| `INCOMPATIBLE` | explicit incompatibility remains unresolved | automatic rejection or winner |

`SUPPRESSED_REDUNDANT` requires a governed relation and deterministic retained
candidate ref. `INCOMPATIBLE` marks both sides in the controlled V1 fixture; it does
not silently choose one.

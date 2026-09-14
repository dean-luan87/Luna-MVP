# Error Handling

The native adapter and normalizer preserve these distinctions:

| Runtime condition | Provider status | Evidence behavior |
|---|---|---|
| dependency/import unavailable | `UNAVAILABLE` | no runtime observation or evidence |
| engine/model initialization failure | `UNAVAILABLE` | no fake success |
| missing image path | `REJECTED` / `INVALID_IMAGE` category | no fake evidence |
| provider call exception | `ERROR` / `OCR_INVOCATION_EXCEPTION` category | no fake evidence |
| timeout raised by the provider, if supported by the environment | `ERROR` / timeout category | no fake evidence |
| malformed native output shape | `ERROR` / `MALFORMED_NATIVE_OUTPUT` | no fake evidence |
| successful call with no text | `EMPTY_SUCCESS`, `empty_result=true` | valid empty-success status candidate only |

RapidOCR currently does not expose a separate deadline parameter. The Runner
therefore does not claim timeout support; an underlying timeout exception is
still kept on the error path if one is raised. No fallback provider is invoked.

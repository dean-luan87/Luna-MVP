# Shared asset delta inventory

| Shared asset | Original consumers | Later modification | Regression risk | Required coverage |
|---|---|---|---|---|
| `authority_grant_mechanical_command_registry_v1.py` | Authority Grant, A semantic bridge, Loop cutover | Existing Brain authorities included in `KNOWN_AUTHORITIES` | semantic authority boundary or grant validation regression | AG-MECHANICAL |
| Real Input integration adapter/types | Real Input phase | Dynamic Flow compatibility → A decision references added | final downstream values could regress | REAL-INPUT and DYNAMIC-COMPATIBILITY |
| Real Capability trial adapter | Single Invocation Trial | compatibility/A metadata added after Dynamic output | provider count or evidence path could change | REAL-CAPABILITY |
| Dynamic Flow compatibility Runner/Verifier | Compatibility cutover | direct-entry bootstrap, exact source manifest, content diagnostics | entrypoint/source/content false negatives | DYNAMIC-COMPATIBILITY |

The harness does not modify these assets.

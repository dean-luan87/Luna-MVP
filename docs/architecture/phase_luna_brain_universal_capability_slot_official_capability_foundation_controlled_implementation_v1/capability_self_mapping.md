# Capability Self Minimal Mapping

`CapabilitySelfViewV1` is read-only and candidate-only. It exposes:

- current capability references
- unavailable references
- degraded references
- suspended references
- recoverable references
- historical references
- potential references

Capability Self does not own Registry state, admission, binding, installation,
activation, suspension, release, or recovery. It does not infer World Truth.

No value scoring, usage optimization, automatic acquisition, or automatic
uninstall reasoning is implemented.

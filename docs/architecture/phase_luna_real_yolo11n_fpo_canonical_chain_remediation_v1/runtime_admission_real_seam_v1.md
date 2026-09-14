# Runtime Admission Real Seam v1

The real FPO path now consumes an `ExecutableCapabilityCandidateV1` and an
explicit Runtime Admission reference/version through
`CanonicalYOLO11nBindingContextV1`.

The seam rejects missing, inconsistent, stale, or invalidated inputs. The
existing YOLO model-readiness record remains useful declaration/observed
readiness evidence, but it is not treated as a substitute for canonical
Runtime Admission.

No Runtime Admission implementation was added.


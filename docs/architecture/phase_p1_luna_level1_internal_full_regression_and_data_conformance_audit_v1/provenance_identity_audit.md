# Provenance and Identity Audit

Stable identities are Dataset, Sample, Cognitive Test Case, and fixture/source
version. Execution identities are Evaluation Run, execution instance, Plane A/G
results, White-box execution records, runtime transition refs where required,
and archive record identity.

The audit checks that reruns retain stable case linkage but receive a new
execution identity, that archive filenames correspond to the run identity,
and that prior-cycle refs are carried rather than reconstructed. It also
checks Dataset/Sample/Case, replay, admission, A-Route, White-box, Plane, and
archive provenance links.

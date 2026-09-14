# System Diagnostics Probe Boundary v1

Probe definitions declare source, scope, expected output, permission/resource
needs, timeout/freshness, and provenance. Probe execution returns an observation
or explicit failure. The probe implementation does not gain governance
authority merely by running.

Supported conceptual probe classes include Python import/version, filesystem,
device, runtime ping, model metadata/loadability, provider health, resource,
protocol fingerprint, and configuration validation. Diagnostics may classify
the result only within the declared contract. It does not install dependencies,
load models for application execution, invoke Providers, or repair the source.

Passive telemetry is accepted as source evidence with source identity and time;
it is not silently treated as current. Active probes require applicable
permission, bounded resource, side-effect, scope, timeout, and freshness
controls. A future active-probe service is deferred; no scheduler is created.

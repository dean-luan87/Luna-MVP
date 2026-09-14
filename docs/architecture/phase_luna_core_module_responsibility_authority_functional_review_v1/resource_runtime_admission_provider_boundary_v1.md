# Resource / Runtime Admission / Provider Boundary v1

Runtime Admission consumes resource facts and policy refs to form executable
or degraded candidates. Provider Admission checks invocation budget, memory,
device, session quota, latency and concurrency and reports consumption/status.

Neither owns global resource policy or resource probes.

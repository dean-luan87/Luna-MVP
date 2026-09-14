# Negative Guards

The structural verifier must fail on:

- non-candidate or authoritative trace/profile nodes;
- cognition, Field, or Current World mutation flags;
- World Truth declaration;
- Decision node creation by A/evaluation;
- Task or Action creation/execution;
- model/provider/observation execution;
- automatic Re-observation execution;
- dataset download;
- missing owner/source/provenance/version refs;
- broken cycle, parent, or hypothesis revision linkage;
- unavailable/planned measures represented as numeric zero or false;
- raw payload, binary, credential, or auth metadata leakage;
- gap refs without affected trace nodes;
- TestBoard refs treated as authoritative state.

These guards observe structure; they do not repair the failing artifact.

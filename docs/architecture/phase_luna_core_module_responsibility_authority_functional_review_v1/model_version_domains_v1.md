# Model Version Domains v1

Model semantic/version identity, weights version, manifest version, loader
version, provider adapter version, capability mapping version, runtime
instance version, and diagnostic snapshot version are separate domains.

No global model version is introduced. A mapping or runtime candidate must
preserve the relevant domain versions and provenance; a health snapshot cannot
rewrite model identity.

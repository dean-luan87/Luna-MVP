# Luna Module-First Development & Verification Cadence Rule v1

## Development Phases

1. Constitution / Protocol First — L0 constitution, L1/L2 protocol, error namespace, input/output/traceability, file-size / reuse / validate-once rules
2. Module Skeleton — responsibilities, file structure, pipeline, boundaries, protocol activation points
3. Module Fill — implementation, local helpers, data contracts, minimal docs
4. Functional Slice Test — targeted behavior checks within a module
5. Module-Level or Gate Verification — complete module, functional block, or release/final gate only

## Forbidden

- Full validation chain per small matrix
- Protocol revalidation per candidate addition
- Planning / DryRun / Post-Review chain per capability segment
- Using check stacking instead of module design

## Allowed Verification Granularity

- Complete module verification
- Complete functional logic verification
- Release gate / final gate verification

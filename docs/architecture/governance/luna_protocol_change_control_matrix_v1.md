# Luna Protocol Change Control Matrix v1

## Change Classification

| change type | minor change | major change | breaking change | mandatory governance response |
| --- | --- | --- | --- | --- |
| Schema Change | optional additive field with backward-compatible default and retained trace | required additive field or new governed object variant | remove/rename/reinterpret required field or change candidate semantics | compatibility assessment; breaking change creates new Draft version |
| Enum Change | documented additive candidate value without consumer behavior change | new value requiring declared consumer compatibility | remove/redefine existing value or permit Fact/Decision/Action/State meaning | Protocol + consumer review; migration for major/breaking |
| Boundary Change | clarified non-authority wording with no operation change | new explicit denial or narrowed allowed scope | allows prohibited operation or weakens candidate/Fact, mutation, or Runtime boundary | L0 check mandatory; weakening is blocked unless constitutional architecture changes separately |
| Permission Change | added diagnostic/reference metadata only | new governed scope requiring Permission/Admission review | self-grant, scope expansion, or bypass of admission | Permission/Admission review; no Protocol-only approval |
| Traceability Change | additive provenance field retained end-to-end | new required source/trace lifecycle element | remove, hide, replace, or silently complete provenance/trace | traceability compatibility and migration evidence |
| Runtime Impact Change | documentation-only clarification with no execution effect | future adapter/execution context dependency declaration | enables Runtime, model/network/database call, write path, or side effect | separate approved Runtime/Capability phase; not lifecycle-only change |

## Version Strategy

- **ownership:** L1 Protocol Governance owns Protocol version identity. Capability owners declare dependencies but never own or self-select an upgrade outside governance.
- **compatibility:** Active versions declare compatible predecessor/successor paths. Consumers and Capabilities must validate selected version against their declared input/output Contracts.
- **migration:** major and breaking changes require an impact inventory, compatibility matrix, traceability preservation, consumer/dependency plan, and explicit rollback plan before activation.
- **rollback:** rollback selects the previously compatible Active/Frozen version by reference; it never mutates history, rewrites evidence, or silently downgrades a Capability. If data/output meaning is incompatible, execution remains blocked pending migration remediation.

## Protocol Admission Flow

```text
Protocol Proposal
        ↓
Impact Assessment
        ↓
Authority Review
  L0 alignment → L1 Protocol review → Permission/Admission impact
        ↓
Compatibility Check
  Capability, consumer, traceability, Registry/lifecycle dependencies
        ↓
Activation Decision
  Protocol reference eligibility only
```

Admission never grants Capability Runtime execution, Permission scope, Registry write, Fact admission, Decision/Action authority, or State mutation.


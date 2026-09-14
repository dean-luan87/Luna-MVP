"""Static ownership guard for Outcome Evaluation Governance."""

CANONICAL_OWNER = "Outcome Evaluation Governance"
FORBIDDEN_MUTATION_TARGETS = (
    "Context",
    "Field",
    "Intent",
    "Decision",
    "Task",
    "Action",
    "Memory",
    "Learning",
    "Self",
    "Personality",
    "Dynamic Regulation",
)


def validate_owner_boundary(owner: str, mutation_targets: tuple[str, ...] = ()) -> tuple[str, ...]:
    issues: list[str] = []
    if owner != CANONICAL_OWNER:
        issues.append("invalid_owner")
    for target in mutation_targets:
        if target in FORBIDDEN_MUTATION_TARGETS:
            issues.append(f"forbidden_mutation_target:{target}")
    return tuple(issues)

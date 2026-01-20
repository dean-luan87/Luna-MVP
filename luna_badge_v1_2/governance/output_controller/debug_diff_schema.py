SCHEMA_VERSION = "debugdiff.v1"

REQUIRED_FIELDS = [
    "schema_version",
    "added_fields",
    "removed_fields",
    "changed_fields",
    "meta",
]

FORBIDDEN_FIELDS = {"pass", "fail", "ok", "decision", "conclusion"}

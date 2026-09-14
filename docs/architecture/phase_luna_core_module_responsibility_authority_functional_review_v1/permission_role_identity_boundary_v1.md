# Permission / Role / Identity Boundary v1

Role/Identity/Relationship may supply evidence such as `employee_of`,
`owner_of`, `caregiver_of`, `admin_of`, or user confirmation. These support
Permission evaluation but do not automatically grant Permission.

Role != Permission. Identity != Grant. Uncertain or stale identity evidence
must not produce executable permission.

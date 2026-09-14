# Decision Unknown Boundary v1

## Unknown in decision integration

Unknown must remain visible in the Decision Context Package and Brain Review.
Unknown may cause a lower confidence candidate, a request for more information,
a request for more information candidate, a safer alternative candidate, or a deferred review candidate.

```text
Unknown
   ↓
Confidence / Risk Candidate
   ↓
Brain Review
   ├── request more information
   ├── accept a candidate with explicit uncertainty
   ├── modify candidate
   └── reject candidate
```

Decision Integration cannot convert Unknown into Fact, silently remove it, or
force a Decision because the package is incomplete. Unknown resolution may
trigger a Revision Candidate, but it does not execute Action or modify Goal.

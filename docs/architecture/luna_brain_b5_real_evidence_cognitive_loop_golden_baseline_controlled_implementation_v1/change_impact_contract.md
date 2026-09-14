# Change-impact contract

Declared change domains map deterministically to required regression sets.
Negative-guard changes require `FULL_GOLDEN_BASELINE_REVIEW`. Unknown domains
also fail closed to full review. Classification does not execute a suite.

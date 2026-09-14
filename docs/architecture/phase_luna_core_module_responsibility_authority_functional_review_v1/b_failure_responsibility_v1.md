# B-CR Failure and Responsibility

## B responsibility

B is responsible for:

- violating request scope;
- incorrect bounded branch computation;
- losing provenance;
- presenting counterfactual as fact;
- exceeding branch/depth/resource limits;
- failing to report residual uncertainty;
- malformed result;
- unauthorized external execution.

## A responsibility

A is responsible for:

- incorrect decision to invoke B;
- incorrect request objective/scope;
- incorrect adoption/rejection of B output;
- treating a B candidate as authoritative truth.

## Brain responsibility

Brain owns global grant, safety, permission, resource and final-governance failures.

Failure output must remain bounded/partial and must never fabricate resolution.

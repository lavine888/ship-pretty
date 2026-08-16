# Review Output

Keep the user-facing report compact.

## During iteration

When useful, report findings in this form:

**Iteration N — score: 68 → 77**

- High leverage: hero hierarchy is still split between the headline and decorative dashboard.
- Changed: reduced dashboard dominance, narrowed copy measure, made CTA hierarchy asymmetric.
- Re-check: desktop improved; mobile still feels too tall above the fold.
- Retrieved pattern: `responsive.recompose-task-order` (or `pattern: none` when no match was useful).

## Final

Use:

**Ship Pretty: PASS — 84/100**

- Biggest improvement: one sentence describing the perceptual change.
- Verified: viewport(s) actually rendered and inspected.
- Remaining: only meaningful residual risk, if any.
- Pattern evidence: IDs retrieved, selected hypothesis, and whether its QA checks passed.

If the gate could not be verified:

**Ship Pretty: UNVERIFIED**

State exactly what prevented rendered inspection. Do not substitute confidence language for evidence.

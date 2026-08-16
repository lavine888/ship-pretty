# Taste Library

The Taste Library stores reusable design decisions, not visual skins. It exists to answer a narrow question after `Judge`:

> Given this visible problem and product context, which proven design decision is worth testing next?

## Retrieval contract

Use the catalog only after inspecting a real render. Convert observations into short signals such as `flat sidebar`, `missing loading state`, or `generic marketing copy`, then run:

```bash
python <skill-dir>/scripts/retrieve_patterns.py \
  --issues "flat sidebar, unclear hierarchy" \
  --context dashboard \
  --limit 3
```

The result is a shortlist, not an instruction to copy a product. Select at most one pattern for the next patch unless the evidence shows two independent problems. Record the selected pattern ID and the patch hypothesis in the review output.

If no pattern reaches a useful match, continue with the normal quality-gate reasoning and record `pattern: none`. Never invent a match to make the library appear useful.

## Pattern fields

Every entry in `patterns.json` must contain:

| Field | Meaning |
| --- | --- |
| `id` | Stable, lowercase identifier grouped by dimension. |
| `dimension` | `layout`, `hierarchy`, `components`, `interaction`, `motion`, `responsive`, or `microcopy`. |
| `problem` | The visible or behavioral problem the pattern addresses. |
| `decision` | The implementation-independent choice to test. |
| `why_it_works` | The causal reasoning, not an aesthetic claim. |
| `use_when` / `avoid_when` | Context boundaries. |
| `failure_modes` | Ways an agent can cargo-cult the pattern. |
| `signals` | Short phrases used by the retrieval script. |
| `qa` | Observable checks after the patch and re-render. |
| `provenance` | Where the decision came from and what is or is not verified. |

## Adding a pattern from an exported project

Treat an exported project as a teaching example, not ground truth. Before adding a pattern, create a design-forensics record containing:

1. the project context and user task;
2. the relevant rendered states and viewport sizes;
3. the repeated design decision;
4. a counterexample or boundary where it should not be used;
5. the visual or interaction evidence supporting the causal explanation;
6. a note separating transferable principle from brand, copy, color, assets, and exact implementation;
7. the benchmark or runtime check that could falsify the pattern.

Do not store proprietary screenshots, logos, exported source, exact spacing recipes, or claims that were not inspected. A pattern is ready for the catalog only when another agent can apply it to a different product without reproducing the source interface.

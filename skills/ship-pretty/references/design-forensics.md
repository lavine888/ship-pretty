# Design Forensics Record

Use this record when analyzing an exported website or app project supplied as a reference, including a Manus Website Builder export. Treat the export as a synthetic teaching example, not as design truth. The goal is to extract decisions that generalize across products, not to reproduce the source.

## Record

```yaml
source:
  name: "project or dataset label"
  origin: "where the export came from"
  license_or_permission: "known permission / unknown"
  inspected_states: [default, loading, error]
  inspected_viewports: [1440x1000, 390x844]

context:
  product_job: "what the user is trying to accomplish"
  audience: "who is doing it"
  task_pressure: "scan / compare / create / monitor / recover"

observation:
  problem: "visible problem or repeated design tension"
  evidence: ["screenshot path or runtime observation"]

decision:
  rule: "implementation-independent design decision"
  why_it_works: "causal explanation"
  use_when: ["boundary"]
  avoid_when: ["boundary"]
  failure_modes: ["how an agent could cargo-cult it"]

transfer:
  keep: ["structure, hierarchy, state logic, interaction principle"]
  discard: ["brand, exact copy, logo, exact colors, proprietary assets"]
  qa: ["observable result after applying the rule"]
  candidate_pattern_id: "dimension.short-name"
```

## Evidence standard

Do not infer a reusable rule from a single decorative detail. Prefer decisions that recur across at least two contexts, or explicitly mark a single-example hypothesis and add a falsification benchmark. A screenshot can support hierarchy, composition, density, typography, and responsive claims; it cannot by itself prove hover, loading, error recovery, keyboard reachability, or motion causality.

Before adding a pattern to the catalog:

- render the relevant state instead of reading source code alone;
- note viewport and document dimensions;
- capture the counterexample or boundary condition;
- remove source-specific identity from the wording;
- run the catalog validator;
- test retrieval with both a matching and a non-matching query.

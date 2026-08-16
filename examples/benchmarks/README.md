# Benchmark set

These fixtures are intentionally small, static HTML pages. They make visual QA reproducible without a framework, build step, API, or design-system dependency.

| Fixture | What it tests | Refined entry |
| --- | --- | --- |
| Landing Page | hero hierarchy, CTA weighting, asymmetric composition | [`examples/demo-ui/index.html`](../demo-ui/index.html) |
| Dashboard | information density, table rhythm, responsive panel stacking | [`dashboard/index.html`](dashboard/index.html) |
| Mobile | mobile-first hierarchy, reachable navigation, task scanning | [`mobile/index.html`](mobile/index.html) |

Each benchmark also includes a deliberately generic `before.html` seed. The landing-page seed is preserved at [`landing-page/before.html`](landing-page/before.html); the refined version is the canonical demo fixture above.

## Capture

From the repository root, use the bundled capture script with any Playwright-compatible Node runtime:

```bash
node scripts/capture_screenshots.mjs examples/demo-ui/index.html assets/benchmarks/landing-page/after
node scripts/capture_screenshots.mjs examples/benchmarks/dashboard/index.html assets/benchmarks/dashboard/after
node scripts/capture_screenshots.mjs examples/benchmarks/mobile/index.html assets/benchmarks/mobile/after
```

The default evidence viewports are 1440×1000 and 390×844. The before/after pair in the root README is a rendered comparison, not a code-only claim.

## Pattern retrieval

After judging a render, use the Taste Library to retrieve a small set of design decisions to test:

```bash
python skills/ship-pretty/scripts/retrieve_patterns.py \
  --issues "mobile feels cramped, primary action below fold" \
  --context mobile
```

The result is advisory. Re-render the patch and record whether the pattern's QA checks actually improved.

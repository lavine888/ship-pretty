<p align="center">
  <img src="./assets/ship-pretty-hero.png" alt="Before and after benchmark: 43 out of 100 and not ready becomes 84 out of 100 and ship it." width="100%">
</p>

# Ship Pretty

<p align="center">
  <a href="./README.md">English</a> · <a href="./README.zh-CN.md">简体中文</a>
</p>

> **AI can generate. Ship Pretty decides when it is actually ready to ship.**

AI agents can produce a working frontend and still miss the obvious: weak hierarchy, default composition, repetitive cards, and a mobile layout that only got smaller.

Ship Pretty is an Agent Skill that enforces the visual loop:

**Render → Judge → Patch → Re-render → Quality Gate**

## The proof

The hero and animation use the same landing-page fixture before and after a Ship Pretty pass. Every screenshot is a real browser render at `1440×1000`; the visual difference is the product.

> **Codex said both were done. Ship Pretty disagreed.**

![Ship Pretty reasoning loop: before, visible problems, judge, patch, after, and ship it](assets/demo.gif)

The GIF is not a crossfade. It shows the visible problems, the judgement, the patch decisions, and the second render that moves the score from **43 / 100** to **84 / 100**.

## The loop

**Render → Judge → Patch → Re-render → Gate**

The loop is the product. The screenshot is the evidence. If the frame fails, the agent returns to the highest-leverage patch instead of polishing code in the dark.

## v0.2: retrieve a design decision

The next patch should not be “add a gradient” just because the Judge found weak hierarchy. Ship Pretty now includes a small, auditable Taste Library:

**Render → Judge → Retrieve Pattern → Patch → Re-render → Gate**

Patterns describe a problem, a transferable design decision, boundaries, failure modes, provenance, and observable QA checks. They are hypotheses to test—not screenshots or brand recipes to copy.

```bash
python skills/ship-pretty/scripts/retrieve_patterns.py \
  --issues "flat sidebar, unclear hierarchy" \
  --context dashboard \
  --limit 3
```

For exported reference projects—including Manus-generated experiments—use the [design-forensics record](skills/ship-pretty/references/design-forensics.md) before adding a new pattern. The catalog currently covers layout, hierarchy, components, interaction, motion, responsive integrity, and microcopy. Static screenshots remain insufficient evidence for runtime states.

## What the skill forces

1. Establish the page goal and preserve deliberate intent.
2. Render at the relevant desktop and mobile viewports.
3. Judge the whole frame before polishing components.
4. Patch only one to three high-leverage problems.
5. Re-render and compare against the previous frame.
6. Stop only when the visual quality gate passes, or report the blocker.

The default gate is **80/100**, with no dimension below **7/10**:

| Dimension | Question |
| --- | --- |
| Hierarchy | Can the user tell what matters in under three seconds? |
| Composition | Does the frame feel intentionally structured? |
| Typography | Do type scale, measure, and weight create hierarchy? |
| Spacing & density | Does rhythm group meaning instead of padding everything equally? |
| Color & effects | Do accents and effects do structural work? |
| Specificity | Does this feel made for this product? |
| Responsive integrity | Does mobile recompose rather than merely compress? |

## Install

The installable skill package is [`skills/ship-pretty/`](skills/ship-pretty/). Install that folder through your agent's normal Skill workflow, or ask Codex to install the skill from this repository. Its entry point is [`SKILL.md`](skills/ship-pretty/SKILL.md); optional references and the static scanner stay beside it. The package follows the portable `SKILL.md` shape described in [OpenAI Academy's Using skills guide](https://openai.com/academy/skills/).

Example invocation:

```text
Use $ship-pretty on this frontend. Render desktop and mobile, identify the highest-impact visual problems, patch them, and keep looping until the quality gate passes. Show the before/after evidence.
```

## Benchmark proof

These are small, framework-free HTML fixtures so the visual evidence does not depend on a particular app stack. Each pair below is a real rendered screenshot, not a mockup.

### Landing Page

<table>
  <tr><th>WITHOUT SHIP PRETTY</th><th>WITH SHIP PRETTY</th></tr>
  <tr>
    <td><img src="./assets/benchmarks/landing-page/before/desktop.png" alt="Landing Page before Ship Pretty"></td>
    <td><img src="./assets/benchmarks/landing-page/after/desktop.png" alt="Landing Page after Ship Pretty"></td>
  </tr>
</table>

### Dashboard

<table>
  <tr><th>WITHOUT SHIP PRETTY</th><th>WITH SHIP PRETTY</th></tr>
  <tr>
    <td><img src="./assets/benchmarks/dashboard/before/desktop.png" alt="Dashboard before Ship Pretty"></td>
    <td><img src="./assets/benchmarks/dashboard/after/desktop.png" alt="Dashboard after Ship Pretty"></td>
  </tr>
</table>

### Mobile

<table>
  <tr><th>WITHOUT SHIP PRETTY</th><th>WITH SHIP PRETTY</th></tr>
  <tr>
    <td><img src="./assets/benchmarks/mobile/before/mobile.png" alt="Mobile benchmark before Ship Pretty"></td>
    <td><img src="./assets/benchmarks/mobile/after/mobile.png" alt="Mobile benchmark after Ship Pretty"></td>
  </tr>
</table>

The source fixtures and both viewport captures remain available in [`assets/benchmarks/`](assets/benchmarks/).

### Fixture index

| Benchmark | Tests | Entry |
| --- | --- | --- |
| Landing Page | hero hierarchy, CTA weighting, asymmetric composition | [`examples/demo-ui/index.html`](examples/demo-ui/index.html) |
| Dashboard | information density, release tables, panel stacking | [`examples/benchmarks/dashboard/index.html`](examples/benchmarks/dashboard/index.html) |
| Mobile | mobile-first hierarchy, task scanning, reachable navigation | [`examples/benchmarks/mobile/index.html`](examples/benchmarks/mobile/index.html) |

Each benchmark includes a deliberately generic `before.html` seed. The landing-page pair is the primary case study; dashboard and mobile are additional regression surfaces.

## Verify locally

Run the structural check and static supporting scan:

```bash
python scripts/validate_skill.py .
python skills/ship-pretty/scripts/validate_taste_library.py
python skills/ship-pretty/scripts/slop_scan.py examples
```

Capture desktop and mobile evidence with any Playwright-compatible Node runtime:

```bash
node scripts/capture_screenshots.mjs examples/benchmarks/landing-page/before.html output/benchmarks/landing-page-before
node scripts/capture_screenshots.mjs examples/demo-ui/index.html output/benchmarks/landing-page-after
node scripts/capture_screenshots.mjs examples/benchmarks/dashboard/before.html output/benchmarks/dashboard-before
node scripts/capture_screenshots.mjs examples/benchmarks/dashboard/index.html output/benchmarks/dashboard-after
node scripts/capture_screenshots.mjs examples/benchmarks/mobile/before.html output/benchmarks/mobile-before
node scripts/capture_screenshots.mjs examples/benchmarks/mobile/index.html output/benchmarks/mobile-after
python scripts/make_release_assets.py output/benchmarks assets
node scripts/make_showcase_assets.mjs
python scripts/make_reasoning_gif.py assets
```

The capture helper expects the `playwright` Node package and a Chromium browser. If they are not already available in your environment, install them locally before capturing:

```bash
npm install --no-save playwright
npx playwright install chromium
```

The capture contract is fixed at **1440×1000** and **390×844**. Screenshots are evidence; the static scanner is only an inspection prompt and cannot judge visual quality. See [`benchmarks/results.md`](benchmarks/results.md) for the latest rendered evidence and comparative scores.

## Repository shape

```text
ship-pretty/
├── README.md
├── README.zh-CN.md
├── assets/
│   ├── demo.gif
│   ├── ship-pretty-hero.png
│   ├── social-preview.png
│   └── benchmarks/              # rendered evidence
├── examples/
│   ├── demo-ui/                 # canonical refined landing fixture
│   └── benchmarks/              # dashboard + mobile fixtures and seeds
└── skills/ship-pretty/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── references/
    │   ├── design-forensics.md
    │   ├── interaction-gate.md
    │   └── taste-library/
    │       ├── pattern-schema.md
    │       └── patterns.json
    └── scripts/
        ├── retrieve_patterns.py
        └── validate_taste_library.py
```

## Contributing

The most useful contribution is a reproducible before/after case, not another list of taste rules. Include the prompt, screenshots, viewport sizes, iteration notes, and the failure mode the change catches. See [`CONTRIBUTING.md`](CONTRIBUTING.md) and the [case-study issue template](.github/ISSUE_TEMPLATE/case-study.md).

## License

MIT. See [`LICENSE`](LICENSE).

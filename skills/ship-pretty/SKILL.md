---
name: ship-pretty
description: Render, critique, retrieve transferable design patterns, and iteratively polish web interfaces until they pass a visual quality gate. Use when Codex is asked to make a UI more polished, premium, intentional, less generic, less AI-looking, closer to a visual reference, or ready to ship; when a user is dissatisfied with frontend aesthetics despite working code; when interaction or motion states need visual QA; or when visual changes need screenshot-based verification across desktop/mobile. Prefer this skill for frontend visual QA and refinement rather than initial product architecture.
---

# Ship Pretty

Treat visual quality as a loop with evidence, not a one-pass styling task.

## Non-negotiable rule

Never claim a visual improvement is complete from code inspection alone.

For any meaningful visual change:

1. Render the interface.
2. Inspect the rendered result at the relevant viewport(s).
3. Judge the result against the quality gate.
4. Fix the highest-impact visible problems.
5. Re-render.
6. Repeat until the gate passes or a real blocker prevents further progress.

If a browser, screenshot, or preview tool is unavailable, say that visual verification is blocked. Still improve the code, but do not claim the quality gate passed.

## Start by preserving intent

Before changing anything, identify:

- the page's primary user goal;
- the single most important action or message;
- the intended audience and tone if evident;
- any existing brand constraints, design tokens, component library, or reference screenshots;
- which visual properties are deliberate and should not be flattened into a new style.

Do not redesign merely to demonstrate activity. Preserve strong existing decisions.

## Choose a mode

### Independent polish

Use when no reference is supplied. Judge the interface on clarity, composition, specificity, and craft.

Read `references/quality-gate.md` and `references/anti-slop-patterns.md`.

For Chinese-language projects or teams, also read `references/quality-gate.zh-CN.md` as a localized reading aid. The English `quality-gate.md` remains the canonical rule set.

When a visible problem needs a design decision rather than a CSS tweak, read `references/taste-library/pattern-schema.md` and retrieve up to three candidate patterns with `scripts/retrieve_patterns.py`. The library provides hypotheses to test, not permission to copy a reference product.

### Reference gate

Use when the user supplies screenshots, a Figma target, an existing site, or a set of inspiration references.

Read `references/reference-mode.md` in addition to the quality gate. Infer principles, not pixels, unless the task explicitly requires pixel parity.

## Establish the baseline

Capture the current state before editing whenever practical.

Use the viewports that matter to the product. Default web baseline when unspecified:

- desktop: approximately 1440 × 1000
- mobile: approximately 390 × 844

For apps with a critical intermediate breakpoint, also inspect a tablet/narrow-desktop width.

Record a baseline score using the seven dimensions in `references/quality-gate.md`.

Do not pretend the numeric score is objective measurement. It is a forcing function for comparative judgment. The before/after reasoning matters more than fake precision.

For reproducible web evidence, use the default capture contract unless the product has a more relevant one:

- desktop: 1440 × 1000
- mobile: 390 × 844

Capture the viewport screenshots and inspect the rendered page beyond the fold when the first frame cuts off a primary section or interaction. A cropped screenshot is not automatically a defect; it is evidence that the next viewport or full-page state needs inspection. Check that the rendered document has no accidental horizontal overflow and that primary controls remain reachable.

## Run the loop

For each iteration:

### 1. Judge the whole frame first

Before zooming into components, answer:

- Where does the eye go first?
- Is that where it should go?
- What feels generic, noisy, weak, cramped, empty, or overdecorated?
- Which one change would improve the whole page rather than one widget?

Prioritize macro problems over micro polish.

### 2. Name the problem and retrieve a decision

Turn the rendered observation into short signals with context, for example `flat sidebar`, `missing loading state`, `generic marketing copy`, or `mobile feels cramped`.

For problems covered by the Taste Library, run:

```bash
python <skill-dir>/scripts/retrieve_patterns.py \
  --issues "flat sidebar, unclear hierarchy" \
  --context dashboard \
  --limit 3
```

Read the shortlisted pattern's boundaries, failure modes, and QA checks. Select at most one pattern for the next patch unless the evidence shows two independent high-impact problems. If there is no useful match, record `pattern: none` and continue with direct quality-gate reasoning. Never invent a match.

### 3. Pick only 1–3 high-impact fixes

Prefer changes with large perceptual leverage, such as:

- reworking hero or above-the-fold composition;
- strengthening information hierarchy;
- changing width, alignment, or section rhythm;
- improving the display/body typography relationship;
- reducing repetitive card chrome;
- clarifying the primary action;
- removing decorative effects that dilute focus;
- changing mobile composition rather than shrinking desktop.

Avoid shotgun edits across dozens of unrelated CSS values.

### 4. Patch with a hypothesis

For each meaningful patch, be able to state:

> This change should improve **X** because **Y**.

Examples:

- “Narrowing the copy column and increasing the display/body contrast should make the value proposition legible before the illustration competes for attention.”
- “Removing six independent card borders should let grouping come from spacing and hierarchy instead of boxes.”

### 5. Re-render and compare

Inspect the new frame beside the baseline or previous iteration.

Do not accept a patch simply because it is different. Revert or revise changes that reduce clarity, personality, or usability.

Save the before/after screenshots where a reviewer can open them. When possible, keep the viewport dimensions, fixture, and iteration number next to the evidence so another agent can reproduce the judgment.

### 6. Stop only on a real condition

Default pass condition:

- total quality score >= 80/100;
- no quality dimension below 7/10;
- no obvious responsive breakage;
- primary action/message is visually clear;
- rendered evidence is saved for the viewports that were actually inspected;
- remaining issues are genuinely low-impact.

Stop earlier only when:

- the user asked for a small bounded change;
- required assets or product decisions are missing;
- tooling prevents render verification;
- further edits would require changing product intent rather than visual execution.

## Anti-slop is not minimalism

Do not “fix AI slop” by blindly removing gradients, cards, shadows, color, animation, or personality.

The problem is not the presence of a technique. The problem is default, repetitive, unjustified use.

Read `references/anti-slop-patterns.md` before major cleanup passes.

## Use references correctly

When references are provided:

- identify shared principles across them;
- separate structural qualities from brand-specific decoration;
- preserve the user's product identity;
- avoid copying logos, proprietary illustrations, or distinctive branded assets;
- compare hierarchy, density, rhythm, type relationships, color discipline, and interaction emphasis.

See `references/reference-mode.md`.

For exported reference projects, use `references/design-forensics.md`. Extract the problem, decision, boundary, failure mode, and observable QA check. Discard brand identity, exact copy, proprietary assets, and implementation-specific values. Add a pattern to `references/taste-library/patterns.json` only after validating its schema and stating its provenance.

## Static scan is supporting evidence only

For HTML/CSS/JS/TS/TSX-heavy projects, optionally run:

```bash
python <skill-dir>/scripts/slop_scan.py <project-or-source-dir>
```

Use its findings as prompts for inspection. Never fail a design solely because the scanner reports a pattern.

A gradient can be excellent. A rounded card can be excellent. The scanner cannot see intent.

## Interaction and motion

When the interface contains meaningful controls, async work, disclosure, navigation, or motion, read `references/interaction-gate.md` and inspect the relevant runtime states. Cover default/focus, pending, success, error/recovery, empty, disabled, and expanded/collapsed states where applicable. A polished default screenshot is not evidence that the interaction is ready.

Use this rule for motion:

> Motion must explain state, hierarchy, causality, or continuity. If it explains none of these, delete it.

Record state evidence separately from static screenshot scores. Do not award an interaction or motion pass from source inspection alone.

## Final response

Use the compact structure in `references/review-output.md`.

Always report:

- what changed at the perceptual level;
- the final gate result;
- which viewports were actually inspected;
- any remaining visual risk or unverified area.

Do not dump a giant checklist unless the user asks for it.

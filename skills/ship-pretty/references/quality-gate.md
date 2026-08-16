# Visual Quality Gate

Use this rubric for comparative visual judgment. Score the rendered interface, not intentions in the source code.

## Scoring

Score each dimension from 1–10.

### 1. Hierarchy

Ask:

- Is the first point of attention deliberate?
- Can a new user understand the main message/action quickly?
- Are primary, secondary, and tertiary elements visibly distinct?
- Is emphasis scarce enough to mean something?

Failure signals: five things shouting at once, weak CTA, giant headline with equally loud decoration, every label bold.

### 2. Composition

Ask:

- Does the frame feel intentionally composed as a whole?
- Is there useful asymmetry, grouping, or visual direction?
- Do sections have distinct roles and rhythm?
- Is content arranged by meaning rather than by available components?

Failure signals: component pile, endless centered stack, three-card grid by reflex, every section using the same wrapper pattern.

### 3. Typography

Ask:

- Is there a clear display/body relationship?
- Are line length and line height comfortable?
- Are weights and sizes doing semantic work?
- Does the type feel appropriate to the product tone?

Failure signals: one font size scale used mechanically, over-wide paragraphs, too many semibold labels, giant gradient headline carrying all personality.

### 4. Spacing & density

Ask:

- Does spacing create groups and transitions?
- Is density appropriate for the task?
- Are all sections padded the same amount out of habit?
- Is whitespace active rather than merely empty?

Failure signals: `p-6` everywhere, equal gaps between unequal concepts, huge dead zones, cramped controls inside spacious marketing shells.

### 5. Color & effects

Ask:

- Is color hierarchy disciplined?
- Are accents reserved for meaningful moments?
- Do shadows, blur, gradients, glass effects, and borders improve structure?
- Does the page still work if decorative effects are mentally removed?

Failure signals: glow behind every hero, gradient text plus gradient button plus gradient border, shadows used to create hierarchy that spacing should create.

### 6. Specificity

Ask:

- Does the interface feel designed for this exact product and audience?
- Are visual metaphors, data, content, and controls specific?
- Could the same UI be relabeled as an AI SaaS, crypto app, project manager, or analytics tool with minimal changes?

Failure signals: generic “supercharge your workflow” hero, interchangeable feature cards, decorative dashboard screenshots unrelated to the core product.

### 7. Responsive integrity

Ask:

- Does mobile recompose priorities rather than just shrink them?
- Are important controls reachable and legible?
- Do line breaks, image crops, grids, and hierarchy still make sense?
- Does any breakpoint expose accidental overflow or awkward empty space?

Failure signals: desktop two-column layout crushed into mobile, giant hero text wrapping into six lines, horizontal scroll, floating CTA covering content.

## Pass condition

Default:

- convert each 1–10 dimension to an equal-weight score out of 100;
- total >= 80;
- every dimension >= 7;
- no obvious visual or responsive defect.

## Severity language

Use three levels only:

- **Blocker** — visibly prevents the interface from feeling coherent or usable.
- **High leverage** — fixing it materially improves the whole frame.
- **Polish** — worthwhile after the major structure is right.

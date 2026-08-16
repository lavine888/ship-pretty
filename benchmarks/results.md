# Rendered benchmark results

These scores are comparative judgments from the captured renders, not objective design measurements. The rubric converts seven 1–10 dimensions to a total out of 100; the final page must also have no horizontal overflow.

## Primary case: Landing Page

| Dimension | Before | After |
| --- | ---: | ---: |
| Hierarchy | 4 | 9 |
| Composition | 5 | 8 |
| Typography | 5 | 8 |
| Spacing & density | 5 | 8 |
| Color & effects | 4 | 8 |
| Specificity | 3 | 9 |
| Responsive integrity | 4 | 9 |
| **Total** | **43/100** | **84/100** |

Observed change: the centered hero / equal-card stack became a product-specific split composition with an explicit quality-gate panel, one primary action, and a mobile single-column recomposition.

Evidence:

- Before: `assets/benchmarks/landing-page/before/{desktop,mobile}.png`
- After: `assets/benchmarks/landing-page/after/{desktop,mobile}.png`
- Capture: 1440×1000 and 390×844; rendered page heights were 1000/1602 before and 1151/1762 after; both had `scrollWidth === viewportWidth`.

## Additional regression surfaces

| Benchmark | Desktop | Mobile | What was checked |
| --- | ---: | ---: | --- |
| Dashboard | 81/100 | 81/100 | metrics, release rows, decision log, stacked mobile panels |
| Mobile | 84/100 | 86/100 | task scanning, progress, reachable bottom navigation |

The Dashboard and Mobile scores are first-pass benchmark baselines for future agent runs; they are not claims that the fixtures are universally optimal. Their refined renders are stored under `assets/benchmarks/`.

## Capture evidence

The capture script reports viewport size, rendered document size, and horizontal overflow. The latest run completed with no overflow at any of the six fixtures × two viewports:

```text
landing-page/before  desktop 1440x1000  page=1440x1000
landing-page/before  mobile  390x844    page=390x1602
landing-page/after   desktop 1440x1000  page=1440x1151
landing-page/after   mobile  390x844    page=390x1762
dashboard/before     desktop 1440x1000  page=1440x1000
dashboard/before     mobile  390x844    page=390x1016
dashboard/after      desktop 1440x1000  page=1440x1000
dashboard/after      mobile  390x844    page=390x1472
mobile/before        desktop 1440x1000  page=1440x1000
mobile/before        mobile  390x844    page=390x844
mobile/after         desktop 1440x1000  page=1440x1030
mobile/after         mobile  390x844    page=390x844
```

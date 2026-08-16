# Interaction and Motion Gate

Static screenshots are necessary evidence, not complete evidence, for an interactive interface. Use this gate when the page has controls, asynchronous work, expandable regions, navigation, or motion.

## State coverage

Inspect only states relevant to the product, but cover the primary task across:

- default and focus-visible;
- hover or pressed where applicable;
- loading or pending;
- success or completion;
- error and recovery;
- empty;
- disabled;
- expanded and collapsed for disclosure controls.

For each inspected state record:

| Question | Pass signal |
| --- | --- |
| Can the user tell what changed? | The state change is visible in the same task context. |
| Can the user tell what to do next? | Copy or affordance gives a concrete next action. |
| Can the user recover? | Failure and empty states explain a safe recovery path. |
| Does hierarchy survive? | Feedback is prominent enough without taking over unrelated content. |
| Is the control reachable? | Keyboard focus, touch target, and mobile placement remain usable. |

## Motion rule

Motion must explain state, hierarchy, causality, or continuity. If an animation explains none of these, remove it or reduce it to a non-blocking transition. Verify reduced-motion behavior and make sure interrupted motion does not hide the resulting state.

Do not award an interaction or motion pass because a page looks polished in its default screenshot. Save runtime evidence or explicitly report the state as unverified.

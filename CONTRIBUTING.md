# Contributing

Ship Pretty should improve through evidence, not taste-law accumulation.

Good contributions include:

- a before/after interface pair with the prompt and iteration notes;
- a quality-gate change that catches a real failure mode;
- a counterexample showing when an anti-slop heuristic should not fire;
- a deterministic helper that improves render verification or comparison;
- compatibility fixes for Agent Skills-capable coding tools.

For visual changes, include rendered evidence at the relevant viewport sizes. The repository's default capture contract is 1440×1000 and 390×844; run `python scripts/validate_skill.py .` and the static scan before opening a case. A clean static scan is not a visual pass.

Please avoid adding long lists of fashionable design opinions without a reproducible example.

# Image references translated to native code

The built-in image generator created one standalone widescreen reference for every slide. The opening four were regenerated with stricter Canvas/SVG constraints. The selected twenty are `slide-01.png` through `slide-20.png`. `prompts.json` and `opening-refinement-prompts.json` preserve the complete prompts. The gallery is at `/design-references/` on the local server.

The images supply composition and hierarchy. They are not runtime slide backgrounds, data sources, or exact chart renderings. All live numbers come from the workbook. Known generated-image mistakes were corrected in implementation: histogram class labels, normality percentages on skewed data, cancellation versus return labels, the CLT simulation's sample size versus the complete dataset's t-test, revenue denominators and the direction of the revenue advantage.

| Slide | Code translation | Continuous motion |
|---|---|---|
| 1 | Orthographic globe, geographic paths, parcel polygons | Orbiting parcels, moving geography and twinkling stars |
| 2 | Native line-art cart, order stream and rupee counters | Real order parcels fall in and cancelled parcels bounce out |
| 3 | Geographic pins, counts, schematic quadratic routes | Parcels travel between city pins |
| 4 | Six native conveyor paths merging into two groups | Conveyor motion, parcel sorting and smooth merge geometry |
| 5 | Actual-row dot histogram and empirical ogive | Class reading highlight and cumulative-curve tracer |
| 6 | Actual distribution and fixed mean/median markers | A large basket tugs on the mean metaphor |
| 7 | Mean ± SD capsules, spread comparison | Measuring parcel, moving ruler and marker emphasis |
| 8 | Order-share × cancellation-rate rectangles and r gauges | Parcel flow and correlation-point emphasis |
| 9 | Persistent one-dot-per-row grid with denominator filters | Magnifier scans actual eligible orders and reads their metadata |
| 10 | Exact binomial stems and threshold input | Probability tracer and moving parcel checkpoint |
| 11 | Actual-data bootstrap-style resampling demonstration | Means continually arrive in a rolling 1,800-mean window |
| 12 | Student t null density, observed and critical values | Null-curve tracer and parcel feedback |
| 13 | Normal null density, rate comparison and observed z | Distribution tracer and outlying parcel movement |
| 14 | Exact observed/expected contingency table | Each cell's contribution is highlighted in sequence |
| 15 | Value-weighted revenue stacks and denominator switch | Revenue flow and a parcel return loop |
| 16 | Computed forest plot and adjustment filters | Parcel passes through category, value and quantity filters |
| 17 | Category-level descriptive excess ranking | Parcel cancellation route emphasizes the initial pilot focus |
| 18 | Four open editorial columns with owner/action | Confirmation stamp, basket, receipt and experiment animation |
| 19 | Four sliders, scenario arithmetic and contribution ceiling | An offer token responds to the current incentive ceiling |
| 20 | Closing globe, return route and open parcel | Orbit motion and twinkling stars close the journey |

`index.html` is self-contained: native JavaScript, Canvas, inline SVG and CSS. No runtime libraries. The same row-particle objects, positions and velocities survive navigation. Guides crossfade while the particles morph, avoiding slide-specific canvas resets. Motion uses elapsed time. Reduced-motion users receive static diagrams. Story, Paper and Midnight themes adjust native chart colours as well as HTML text and surfaces; browser storage remembers the selection.

The offline authoring files are `scripts/scene-v2.js`, `scripts/motion-theme-v3.js` and `scripts/reimagine.py`. The latter assembles the final single-file deck while preserving the latest embedded data. `scripts/build_deck.py` independently recomputes workbook statistics using SciPy and statsmodels. Neither authoring process is needed to run the presentation.

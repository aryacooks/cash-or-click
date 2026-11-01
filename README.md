# Cash or click?

Live presentation: https://aryacooks.github.io/cash-or-click/

A self-contained, 20-slide HTML presentation built with native JavaScript, Canvas, SVG and CSS. No runtime libraries or build step. All order data and geographic geometry are embedded in `index.html`; Google Fonts are optional and have local fallbacks.

Run locally:

```sh
python3 -m http.server 5173 --bind 127.0.0.1
```

Open http://127.0.0.1:5173. Use Next/Back, left/right arrows, Page Up/Down, Home/End, or the slide index. N opens presenter notes; F toggles fullscreen. Each analytical slide offers its calculation details. Range controls retain their normal keyboard behaviour. Reduced-motion preferences are respected. The theme menu offers Story (the original act-based colours), Paper, and Midnight; the choice persists in browser storage. Every slide has an ongoing concept-specific animation. The CLT keeps sampling from the workbook into a rolling window of up to 1,800 means.

## Data and methods

Source: `amazon_synthetic_1500_orders.xlsx`, **Orders** sheet. This is fully synthetic educational data, not actual Amazon operating performance. `scripts/build_deck.py` recomputes the statistics from the workbook and replaces the embedded data block in the presentation. Its offline analysis dependencies are in `requirements-analysis.txt`; these are not needed to run the deck.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-analysis.txt
.venv/bin/python scripts/build_deck.py
```

All cancellation rates use all orders in the relevant payment group. Return rates divide returned by non-cancelled orders. Sample SD uses n−1. Quartiles use NumPy's linear interpolation. The cancellation z-test pools the null proportion; Welch's test is one-tailed. Chi-square is the uncorrected Pearson test of payment group × four statuses. Logistic regression controls for category, order value and quantity.

**Revenue denominators matter.** Settled orders exclude In Transit: ₹71.5 COD versus ₹83.7 Prepaid kept per ₹100 settled. With all orders placed in the denominator, delivered revenue so far is ₹68.1 versus ₹77.8; unresolved orders are not labelled lost. The settled ceiling is about ₹212 of revenue per shifted buyer, or ₹32 at an assumed 15% margin. The all-placed ceiling using delivered revenue so far is about ₹166, or ₹25 at 15%. These are illustrative scenarios assuming a nudge can reproduce the observed retention gap. Fees, delivery costs, partial refunds, salvage, confirmation costs and causal selection effects are not estimated.

## Design references

`design-references/` contains the image-generated slide references and prompt set. The presentation translates these references into editable type, procedural diagrams and interactive charts. Reference images are not used as flattened slide backgrounds. Geography is derived from Natural Earth; maps provide schematic context.

The original supplied presentation is preserved as `original-deck.html`. The pre-reimagination implementation is retained in `design-references/before-reimagination.html`.

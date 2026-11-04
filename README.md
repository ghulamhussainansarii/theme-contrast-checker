# Theme Contrast Checker — WCAG Contrast Checker for Shopify Themes and Web Accessibility

**One-line description:** A free, dependency-free WCAG contrast checker that gives the AA and AAA contrast ratio for any foreground and background colour, for Shopify themes, e-commerce stores, and web developers.

**Keywords:** WCAG contrast checker, accessibility contrast ratio, AA AAA checker, Shopify theme accessibility, text contrast checker, colour contrast ratio.

## Structured summary

- **What it is:** A small Python tool, plus a no-install web demo, that checks text contrast between two theme colours.
- **Who it is for:** Shopify theme developers, e-commerce store owners, and web developers who need readable text colours.
- **What it outputs:** A contrast ratio from 1.00 to 21.00, and PASS/FAIL for AA normal, AA large, AAA normal, and AAA large text.
- **What it does NOT do:** It does not audit a whole website, check images or non-text contrast, or guarantee legal compliance. It checks the colour pairs you give it, nothing more.
- **Market, stated qualitatively only:** Accessibility checks are a real, ongoing need for theme and store owners — readable text affects customers, and WCAG AA is the usual target for web content. This project makes that one check quick and repeatable. No market size, revenue, download, or user numbers are claimed for this project.

## Honest status

Created on 2026-11-04. This is a new project. It has no users, no downloads, no stars, and no measured reach or impact yet. Any future reach will be reported only when it is actually measured.

## What it does

- Parses hex colours: `#RGB`, `#RRGGBB`, with or without `#`.
- Computes relative luminance and the WCAG contrast ratio.
- Reports AA and AAA pass/fail for normal and large text.
- Checks one pair on the command line, or a batch of pairs from a JSON file.
- Includes a static web demo (`docs/index.html`) with the same logic in JavaScript, so you can check colours without installing Python.

## Install

No dependencies. Python 3.9 or later only.

```bash
# No install step is required to run it from this folder:
python3 -m theme_contrast_checker.cli '#333333' '#ffffff'
```

## Usage: single pair

```bash
python3 -m theme_contrast_checker.cli '#000000' '#ffffff'
```

Real output from running that command:

```
Name                 FG        BG        Ratio  AA    AA-L  AAA   AAA-L
-----------------------------------------------------------------------
                     #000000   #ffffff   21.00  PASS  PASS  PASS  PASS

AA normal: all PASS (1 pair(s) checked)
```

A failing pair:

```bash
python3 -m theme_contrast_checker.cli '#777777' '#777777'
```

Real output:

```
Name                 FG        BG        Ratio  AA    AA-L  AAA   AAA-L
-----------------------------------------------------------------------
                     #777777   #777777    1.00  FAIL  FAIL  FAIL  FAIL

AA normal: some FAIL (1 pair(s) checked)
```

Exit codes: `0` if every pair passes AA normal, `1` if any pair fails AA normal, `2` on an input error.

## Usage: batch mode

Create a JSON file, for example `examples/pairs.json`:

```json
[
  {"name": "Body", "foreground": "#333333", "background": "#ffffff"},
  {"name": "Black on white", "foreground": "#000000", "background": "#ffffff"},
  {"name": "Same colour", "foreground": "#777777", "background": "#777777"}
]
```

Run it:

```bash
python3 -m theme_contrast_checker.cli --batch examples/pairs.json
```

Real output from running that command:

```
Name                 FG        BG        Ratio  AA    AA-L  AAA   AAA-L
-----------------------------------------------------------------------
Body                 #333333   #ffffff   12.63  PASS  PASS  PASS  PASS
Black on white       #000000   #ffffff   21.00  PASS  PASS  PASS  PASS
Same colour          #777777   #777777    1.00  FAIL  FAIL  FAIL  FAIL

AA normal: some FAIL (3 pair(s) checked)
```

The batch exits with code `1` here because one pair fails AA normal, which is the intended behaviour for a checker.

## Web demo: responsive on all devices

Open `docs/index.html` in any browser. No build step, no external dependencies, no data leaves your device.

- Mobile (~360px): single-column layout, full-width inputs and buttons, no horizontal scroll.
- Tablet: comfortable two-column colour inputs, same content, no horizontal scroll.
- Desktop: centred content up to 720px wide.
- Tap targets are at least 44px high, and text stays readable at small widths.
- The demo uses the same contrast logic as the Python CLI (`docs/contrast.js`), and shows the same AA/AAA results.

What was actually tested for the demo: unit tests, CLI runs, and JavaScript/Python logic parity on the same pairs (see below). A real-phone check has not been done yet — that remains for a real device, and is not claimed here.

## Use cases

- **Shopify theme accessibility:** Check body, heading, button, and footer colours before publishing a theme.
- **E-commerce stores:** Check sale badges, prices, and navigation text on product and checkout pages.
- **Web developers:** Check a design system's colour pairs in a repeatable batch, for example in a theme review.

## FAQ

**What is a contrast ratio?**
A contrast ratio is a number from 1.00 to 21.00 that describes how different two colours look. Higher means easier to read. Black on white is 21.00, and two identical colours are 1.00.

**What is the difference between AA and AAA?**
AA is the usual WCAG target, and AAA is stricter. A pair can pass AA and still fail AAA, because AAA needs a higher ratio.

**What ratio do I need for normal vs large text?**
For AA, normal text needs 4.5 or higher, and large text needs 3.0 or higher. For AAA, normal text needs 7.0 or higher, and large text needs 4.5 or higher.

**How do I use the batch mode?**
Put your colour pairs in a JSON list, as shown above, then run the CLI with `--batch` and the file name. The tool prints one table row per pair, with AA and AAA results.

## Tests

Run the tests with:

```bash
python3 -m unittest discover -s tests -v
```

Result at delivery: 16 tests, all passing (`Ran 16 tests ... OK`).

## Logic parity: Python vs web demo

Same pairs, same results, verified at delivery:

| Pair | Python ratio | JavaScript ratio |
| --- | --- | --- |
| Black on white | 21.0 | 21 |
| Same colour #777777 | 1.0 | 1 |
| #333333 on white | 12.63 | 12.63 |
| #5a5a5a on white | 6.9 | 6.9 |

The web demo produced no console errors in its logic check (logic run in Node for parity); full browser console testing on a real device is still outstanding.

## Project layout

```
theme_contrast_checker/
  contrast.py      # hex parsing, luminance, contrast ratio, AA/AAA checks
  cli.py           # single-pair and batch CLI
  __init__.py      # public exports
tests/
  test_contrast.py # ratio, luminance, boundaries, invalid input
  test_cli.py      # single pair and batch CLI paths
docs/
  index.html       # responsive web demo
  contrast.js      # same logic in JavaScript
examples/
  pairs.json       # batch example
README.md
LICENSE            # MIT, author Muhammad Ghulam Hussain
pyproject.toml
.gitignore
```

## License

MIT, author Muhammad Ghulam Hussain. See `LICENSE`.

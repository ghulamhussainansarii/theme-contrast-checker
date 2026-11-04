"""Command-line interface for theme-contrast-checker.

Usage:
    python -m theme_contrast_checker.cli #ffffff #000000
    python -m theme_contrast_checker.cli --batch pairs.json

Batch JSON: a list of objects, each with a name (optional) and
foreground/background colours, e.g.
    [{"name": "Body", "foreground": "#333333", "background": "#ffffff"}]

Exit codes: 0 if every pair passes AA normal, 1 if any pair fails
AA normal, 2 on a usage/input error.
"""

import argparse
import json
import sys

from .contrast import check


def _flag(ok):
    return "PASS" if ok else "FAIL"


def format_row(result, name=""):
    """One table row for a check() result dict."""
    return (
        f"{name:<20} {result['foreground']:<9} {result['background']:<9} "
        f"{result['ratio']:>5.2f}  {_flag(result['aa_normal']):<4}  "
        f"{_flag(result['aa_large']):<4}  {_flag(result['aaa_normal']):<4}  "
        f"{_flag(result['aaa_large']):<4}"
    )


HEADER = (
    f"{'Name':<20} {'FG':<9} {'BG':<9} {'Ratio':>5}  "
    f"{'AA':<4}  {'AA-L':<4}  {'AAA':<4}  {'AAA-L':<4}"
)


def _pair_from_entry(entry):
    if not isinstance(entry, dict):
        raise ValueError("each batch entry must be an object")
    fg = entry.get("foreground", entry.get("fg", entry.get("foreground_color")))
    bg = entry.get("background", entry.get("bg", entry.get("background_color")))
    if fg is None or bg is None:
        raise ValueError(f"batch entry needs foreground and background: {entry!r}")
    return entry.get("name", ""), fg, bg


def load_batch(path):
    """Load and check every pair in a batch JSON file."""
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("batch JSON must be a list of colour pairs")
    results = []
    for entry in data:
        name, fg, bg = _pair_from_entry(entry)
        results.append((name, check(fg, bg)))
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="theme-contrast-checker",
        description="Check WCAG text contrast for theme colours.",
    )
    parser.add_argument("foreground", nargs="?", help="foreground hex colour, e.g. #333333")
    parser.add_argument("background", nargs="?", help="background hex colour, e.g. #ffffff")
    parser.add_argument("--batch", metavar="FILE", help="JSON file with colour pairs to check")
    args = parser.parse_args(argv)

    try:
        if args.batch:
            if args.foreground or args.background:
                parser.error("use either a single pair or --batch, not both")
            results = load_batch(args.batch)
        elif args.foreground and args.background:
            results = [("", check(args.foreground, args.background))]
        else:
            parser.error("provide a foreground and background colour, or --batch FILE")
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print(HEADER)
    print("-" * len(HEADER))
    for name, result in results:
        print(format_row(result, name))
    all_aa = all(result["aa_normal"] for _, result in results)
    print(f"\nAA normal: {'all PASS' if all_aa else 'some FAIL'} ({len(results)} pair(s) checked)")
    return 0 if all_aa else 1


if __name__ == "__main__":
    raise SystemExit(main())

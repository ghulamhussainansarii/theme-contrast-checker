"""WCAG contrast calculations (stdlib only).

Implements the WCAG 2.x relative-luminance and contrast-ratio formulas.
"""

__all__ = ["parse_hex", "relative_luminance", "contrast_ratio", "check"]


def parse_hex(value):
    """Parse a hex colour into an (r, g, b) tuple of ints 0-255.

    Accepts '#RGB', '#RRGGBB', 'RGB' and 'RRGGBB' (case-insensitive).
    Raises ValueError for anything else.
    """
    if not isinstance(value, str):
        raise ValueError("colour must be a string, e.g. '#ffffff'")
    text = value.strip().lstrip("#")
    if len(text) == 3:
        text = "".join(ch * 2 for ch in text)
    if len(text) != 6:
        raise ValueError(f"invalid hex colour: {value!r} (expected #RGB or #RRGGBB)")
    try:
        r = int(text[0:2], 16)
        g = int(text[2:4], 16)
        b = int(text[4:6], 16)
    except ValueError:
        raise ValueError(f"invalid hex colour: {value!r}") from None
    return (r, g, b)


def _linear(channel):
    """Convert one sRGB channel (0-255) to its linear-light value."""
    c = channel / 255.0
    if c <= 0.03928:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    """Relative luminance of an (r, g, b) tuple, in the range 0-1."""
    r, g, b = rgb
    return 0.2126 * _linear(r) + 0.7152 * _linear(g) + 0.0722 * _linear(b)


def contrast_ratio(foreground, background):
    """WCAG contrast ratio between two hex colours, in the range 1-21."""
    fg_lum = relative_luminance(parse_hex(foreground))
    bg_lum = relative_luminance(parse_hex(background))
    lighter, darker = max(fg_lum, bg_lum), min(fg_lum, bg_lum)
    return (lighter + 0.05) / (darker + 0.05)


def check(foreground, background):
    """Check one pair and return a result dict with ratio and pass/fail.

    Thresholds (WCAG 2.x):
    - AA normal text: 4.5, AA large text: 3.0
    - AAA normal text: 7.0, AAA large text: 4.5
    """
    ratio = contrast_ratio(foreground, background)
    return {
        "foreground": foreground,
        "background": background,
        "ratio": round(ratio, 2),
        "aa_normal": ratio >= 4.5,
        "aa_large": ratio >= 3.0,
        "aaa_normal": ratio >= 7.0,
        "aaa_large": ratio >= 4.5,
    }

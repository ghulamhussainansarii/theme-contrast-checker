// WCAG contrast logic, mirroring theme_contrast_checker/contrast.py exactly.
// Same formulas and thresholds: 0.03928 linearisation threshold,
// AA normal 4.5, AA large 3.0, AAA normal 7.0, AAA large 4.5.
function parseHex(value) {
  if (typeof value !== "string") throw new Error("colour must be a string");
  let text = value.trim().replace(/^#/, "");
  if (text.length === 3) text = text.split("").map((c) => c + c).join("");
  if (text.length !== 6 || !/^[0-9a-fA-F]{6}$/.test(text)) {
    throw new Error("invalid hex colour: " + value);
  }
  return [
    parseInt(text.slice(0, 2), 16),
    parseInt(text.slice(2, 4), 16),
    parseInt(text.slice(4, 6), 16),
  ];
}
function linear(channel) {
  const c = channel / 255;
  return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
}
function luminance(rgb) {
  return 0.2126 * linear(rgb[0]) + 0.7152 * linear(rgb[1]) + 0.0722 * linear(rgb[2]);
}
function contrastRatio(fg, bg) {
  const a = luminance(parseHex(fg));
  const b = luminance(parseHex(bg));
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
}
function checkContrast(fg, bg) {
  const ratio = contrastRatio(fg, bg);
  return {
    ratio: Math.round(ratio * 100) / 100,
    aa_normal: ratio >= 4.5,
    aa_large: ratio >= 3.0,
    aaa_normal: ratio >= 7.0,
    aaa_large: ratio >= 4.5,
  };
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = { parseHex, luminance, contrastRatio, checkContrast };
}

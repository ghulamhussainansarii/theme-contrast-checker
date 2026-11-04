"""Unit tests for the WCAG contrast calculations."""

import unittest

from theme_contrast_checker.contrast import (
    check,
    contrast_ratio,
    parse_hex,
    relative_luminance,
)


class TestParseHex(unittest.TestCase):
    def test_full_hex_with_hash(self):
        self.assertEqual(parse_hex("#ffffff"), (255, 255, 255))

    def test_full_hex_without_hash(self):
        self.assertEqual(parse_hex("000000"), (0, 0, 0))

    def test_short_hex_expands(self):
        self.assertEqual(parse_hex("#fff"), (255, 255, 255))
        self.assertEqual(parse_hex("#f00"), (255, 0, 0))

    def test_invalid_hex_raises(self):
        for bad in ["#gg0000", "#12345", "#1234567", "", "red", 123, None]:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    parse_hex(bad)


class TestContrastRatio(unittest.TestCase):
    def test_black_white_is_21(self):
        self.assertAlmostEqual(contrast_ratio("#000000", "#ffffff"), 21.0, places=2)

    def test_same_colour_is_1(self):
        self.assertAlmostEqual(contrast_ratio("#336699", "#336699"), 1.0, places=2)

    def test_order_does_not_matter(self):
        self.assertAlmostEqual(
            contrast_ratio("#ffffff", "#000000"),
            contrast_ratio("#000000", "#ffffff"),
            places=2,
        )

    def test_luminance_bounds(self):
        self.assertAlmostEqual(relative_luminance((0, 0, 0)), 0.0, places=2)
        self.assertAlmostEqual(relative_luminance((255, 255, 255)), 1.0, places=2)


class TestCheckBoundaries(unittest.TestCase):
    def test_aa_and_aaa_for_black_on_white(self):
        result = check("#000000", "#ffffff")
        self.assertEqual(result["ratio"], 21.0)
        self.assertTrue(result["aa_normal"])
        self.assertTrue(result["aa_large"])
        self.assertTrue(result["aaa_normal"])
        self.assertTrue(result["aaa_large"])

    def test_same_colour_fails_everything(self):
        result = check("#777777", "#777777")
        self.assertEqual(result["ratio"], 1.0)
        self.assertFalse(result["aa_normal"])
        self.assertFalse(result["aa_large"])
        self.assertFalse(result["aaa_normal"])
        self.assertFalse(result["aaa_large"])

    def test_boundary_ratios(self):
        # A pair just above AA normal (4.5) but below AAA normal (7.0).
        result = check("#5a5a5a", "#ffffff")
        self.assertGreaterEqual(result["ratio"], 4.5)
        self.assertLess(result["ratio"], 7.0)
        self.assertTrue(result["aa_normal"])
        self.assertFalse(result["aaa_normal"])


if __name__ == "__main__":
    unittest.main()

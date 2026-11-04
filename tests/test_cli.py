"""Unit tests for the CLI, including the batch path."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from theme_contrast_checker.cli import load_batch, main


class TestCliBatch(unittest.TestCase):
    def _write_batch(self, pairs):
        tmp = tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False, encoding="utf-8"
        )
        with tmp as handle:
            json.dump(pairs, handle)
        return tmp.name

    def test_load_batch_returns_results(self):
        path = self._write_batch(
            [
                {"name": "Body", "foreground": "#000000", "background": "#ffffff"},
                {"name": "Same", "foreground": "#777777", "background": "#777777"},
            ]
        )
        results = load_batch(path)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][0], "Body")
        self.assertEqual(results[0][1]["ratio"], 21.0)
        self.assertEqual(results[1][1]["ratio"], 1.0)

    def test_main_batch_all_pass_exits_zero(self):
        path = self._write_batch(
            [{"name": "Body", "foreground": "#000000", "background": "#ffffff"}]
        )
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["--batch", path])
        self.assertEqual(code, 0)
        self.assertIn("21.00", out.getvalue())
        self.assertIn("all PASS", out.getvalue())

    def test_main_batch_failing_pair_exits_one(self):
        path = self._write_batch(
            [{"name": "Same", "foreground": "#777777", "background": "#777777"}]
        )
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["--batch", path])
        self.assertEqual(code, 1)
        self.assertIn("some FAIL", out.getvalue())

    def test_main_single_pair(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["#000000", "#ffffff"])
        self.assertEqual(code, 0)
        self.assertIn("21.00", out.getvalue())

    def test_main_invalid_colour_exits_two(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["#zzzzzz", "#ffffff"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()

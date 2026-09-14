import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from parser import classify_result, parse_report


class ResultClassifierTests(unittest.TestCase):
    def test_comparator_is_preserved(self):
        result = classify_result("<5", "/HPF")
        self.assertEqual(result["kind"], "quantity")
        self.assertEqual(result["value"], 5.0)
        self.assertEqual(result["comparator"], "<")
        self.assertEqual(result["unit_source"], "/HPF")

    def test_interval_is_not_collapsed(self):
        result = classify_result("0-2", "/HPF")
        self.assertEqual(result["kind"], "interval")
        self.assertEqual(result["low"], 0.0)
        self.assertEqual(result["high"], 2.0)

    def test_ordinal(self):
        result = classify_result("1+", None)
        self.assertEqual(result["kind"], "ordinal")
        self.assertEqual(result["source_text"], "1+")

    def test_negative_is_categorical_not_missing(self):
        result = classify_result("Negative", None)
        self.assertEqual(result["kind"], "categorical")
        self.assertEqual(result["source_text"], "Negative")


class ParserTests(unittest.TestCase):
    def test_pipe_layout(self):
        text = """\
SUBJECT=subject-synthetic-stage03-001
SPECIMEN=Urine
COLLECTED=2026-09-13T23:30:00Z
ISSUED=2026-09-14T00:00:00Z
STATUS=final
TEST | RESULT | UNIT | REFERENCE | FLAG
SYNTH_WBC | <5 | /HPF | SYNTH_RANGE |
"""
        report = parse_report(text)
        self.assertEqual(len(report.rows), 1)
        self.assertEqual(report.rows[0].result_text, "<5")
        self.assertEqual(report.rows[0].unit, "/HPF")

    def test_malformed_row_fails_instead_of_guessing(self):
        text = """\
TEST | RESULT | UNIT | REFERENCE | FLAG
SYNTH_BAD | value | unit
"""
        report = parse_report(text)
        self.assertEqual(len(report.rows), 0)
        self.assertTrue(report.parse_errors)


if __name__ == "__main__":
    unittest.main()

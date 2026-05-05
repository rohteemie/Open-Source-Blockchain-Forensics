"""Tests for report output helpers."""

import os
import tempfile
import unittest

from blockchain_forensics.output import build_output, write_report


class TestReportOutput(unittest.TestCase):
    def test_write_csv_report(self) -> None:
        payload = build_output(
            address="addr",
            provider="blockstream",
            clusters={"root": ["a", "b"]},
            evidence={"root": 2},
            scores={"root": 0.4},
            tx_count=1,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.csv")
            write_report(path, payload, "csv")
            self.assertTrue(os.path.exists(path))

    def test_write_text_report(self) -> None:
        payload = build_output(
            address="addr",
            provider="blockstream",
            clusters={"root": ["a", "b"]},
            evidence={"root": 2},
            scores={"root": 0.4},
            tx_count=1,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.txt")
            write_report(path, payload, "text")
            self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()

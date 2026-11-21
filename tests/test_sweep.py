"""Scenario catalog runner smoke test."""
import csv
import tempfile
import unittest
from pathlib import Path
from ofdm_image.sweep import sweep_csv

class TestSweep(unittest.TestCase):
    def test_grid_is_complete_and_csv_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "cases.csv"
            rows = sweep_csv(output, byte_count=48, seed=42)
            self.assertEqual(len(rows), 45)
            keys = {(r["modulation"], r["nfft"], r["sample_snr_db"]) for r in rows}
            self.assertEqual(len(keys), 45)
            with output.open(newline="") as f:
                saved = list(csv.DictReader(f))
            self.assertEqual(len(saved), 45)
            for row in rows:
                self.assertGreaterEqual(float(row["ber"]), 0)
                self.assertLessEqual(float(row["ber"]), 1)
                self.assertGreater(float(row["waveform_power"]), 0)

if __name__ == "__main__":
    unittest.main()

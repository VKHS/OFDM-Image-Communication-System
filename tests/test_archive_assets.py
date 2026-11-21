"""Check that committed archived assets actually exist and remain grouped correctly."""
from pathlib import Path
from zipfile import ZipFile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ArchiveAssets(unittest.TestCase):
    def test_original_image_sweep(self):
        p = ROOT / "figures/historical/image_outputs"
        self.assertEqual(len(list(p.glob("*.jpg"))), 80)
        for mode in ("QPSK", "16PSK", "16QAM"):
            for n in (16, 32, 64):
                for snr in (0, 5, 10, 15, 20, 25, 30):
                    self.assertTrue((p / f"result_{mode}-SNR{snr}-N{n}.jpg").is_file())
        for n in (16, 32, 64):
            self.assertTrue((p / f"result_BER_nfft_{n}.jpg").is_file())

    def test_saved_inputs(self):
        for name in ("lena.jpg", "lenna.png", "Lenna_(test_image).png"):
            self.assertTrue((ROOT / "assets/input_images" / name).is_file())

    def test_archived_simulink_zip(self):
        with ZipFile(ROOT / "archive/archived_simulink_models.zip") as archive:
            model_names = [x for x in archive.namelist() if x.endswith((".slx", ".mdl"))]
            self.assertEqual(len(model_names), 47)

    def test_archived_report_figures_zips(self):
        archive_parts = sorted((ROOT / "archive").glob("report_figures_??.zip"))
        self.assertEqual(len(archive_parts), 6)
        with_files = 0
        for part in archive_parts:
            with ZipFile(part) as archive:
                with_files += sum(x.lower().endswith((".png", ".jpg", ".jpeg", ".emf")) for x in archive.namelist())
        self.assertEqual(with_files, 155)

    def test_original_matlab_and_diagrams(self):
        self.assertEqual(len(list((ROOT / "matlab/legacy").rglob("*.m"))), 16)
        self.assertGreaterEqual(len(list((ROOT / "figures/new_design").glob("*.svg"))), 13)

if __name__ == "__main__":
    unittest.main()

"""CPU-only, deterministic numerical validation: no MATLAB/FPGA required."""
import unittest
import numpy as np
from ofdm_image.core import constellation, bits_to_indices, indices_to_bits, transmit_receive

class TestOFDM(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bits = np.unpackbits(np.arange(256, dtype=np.uint8))

    def test_bit_label_inverse(self):
        for width in (2, 4, 8):
            tail = self.bits[:len(self.bits) // width * width]
            np.testing.assert_array_equal(indices_to_bits(bits_to_indices(tail, width), width), tail)

    def test_constellation_size_and_energy(self):
        for modulation, points in (("QPSK", 4), ("16PSK", 16), ("16QAM", 16), ("256QAM", 256)):
            c = constellation(modulation)
            self.assertEqual(len(c), points)
            self.assertAlmostEqual(float(np.mean(np.abs(c) ** 2)), 1.0, places=12)
            self.assertEqual(len(np.unique(c)), points)

    def test_nine_noiseless_full_carrier_links(self):
        for mode in ("QPSK", "16PSK", "16QAM"):
            for n in (16, 32, 64):
                with self.subTest(mode=mode, nfft=n):
                    r = transmit_receive(self.bits, mode, n, float("inf"))
                    self.assertEqual(r["ber"], 0)
                    self.assertEqual(r["evm_rms"], 0)
                    np.testing.assert_array_equal(r["bits"], self.bits)

    def test_cp_off_and_on(self):
        for cp in (0, 4, 16):
            r = transmit_receive(self.bits, "16QAM", 64, float("inf"), cp_len=cp)
            np.testing.assert_array_equal(r["bits"], self.bits)
            self.assertEqual(r["cp_len"], cp)

    def test_48_of_64_active_carriers(self):
        for mode in ("QPSK", "16PSK", "16QAM"):
            r = transmit_receive(self.bits, mode, 64, float("inf"), cp_len=16, active_bins=48)
            np.testing.assert_array_equal(r["bits"], self.bits)

    def test_padding_round_trip(self):
        bits = self.bits[:91]
        r = transmit_receive(bits, "16QAM", 64, float("inf"), active_bins=48)
        self.assertEqual(r["padding_bits"], 192-91)
        np.testing.assert_array_equal(r["bits"], bits)

    def test_deterministic_awgn(self):
        a = transmit_receive(self.bits, "16QAM", 64, 8.0, seed=712)
        b = transmit_receive(self.bits, "16QAM", 64, 8.0, seed=712)
        self.assertEqual(a["ber"], b["ber"])
        self.assertEqual(a["evm_rms"], b["evm_rms"])
        self.assertAlmostEqual(a["noise_power"] / a["waveform_power"], 10**(-8/10))

    def test_noisy_link_errors(self):
        r = transmit_receive(self.bits, "16QAM", 64, -5, seed=42)
        self.assertGreater(r["ber"], 0)

    def test_optional_adc(self):
        r = transmit_receive(self.bits, "QPSK", 16, float("inf"), adc_bits=12)
        self.assertEqual(len(r["bits"]), len(self.bits))

    def test_invalid_parameters(self):
        for args in (dict(nfft=30), dict(cp_len=80), dict(active_bins=100), dict(adc_bits=1)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                transmit_receive(self.bits, **args)

if __name__ == "__main__":
    unittest.main()

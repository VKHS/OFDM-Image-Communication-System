# MATLAB experiments

**Project author: Vahab Khalili.**

The MATLAB numerical reference in this folder is independent of the historical Simulink source files.

| Source | Purpose |
|---|---|
| `run_ofdm_reference.m` | Fully reversible image → modulation → IFFT → AWGN → FFT → decision → image |
| `test_smoke.m` | Nine ideal-channel reconstruction assertions |
| `run_reference_demo.m` | Convenient entry point and per-scenario console output |
| `run_full_suite.m` | 63 cases, reconstructed images, BER/EVM/power CSV, BER curves and an image gallery |

## Commands (MATLAB)

```matlab
addpath('matlab');
test_smoke();
run('matlab/run_reference_demo.m');
T = run_full_suite('assets/input_images/lenna.png','results/matlab');
```

Without the separately supplied original image, `run_full_suite()` generates a deterministic synthetic input and executes all scenarios. The suite saves `63` images (3 modulation schemes × 3 FFT sizes × 7 sample-domain SNR levels), as well as the `case_metrics.csv`, `BER_sweep.png`, and `image_gallery.png`. These are generated **when MATLAB is run**; they are not represented as committed historical results.

The **original 16 MATLAB .m files and two .asv support files are now preserved in [matlab/legacy](legacy)**; the original 42 model files are contained in [the versioned Simulink archive](../archive/archived_simulink_models.zip). The new MATLAB reference and sweep code have not been executed here because MATLAB is not available in this environment.

## Historical image inputs

The original archive contains `lena.jpg` (225×225) and `lenna.png` / `Lenna_(test_image).png` (512×512), plus other inputs. To use them here, place the actual assets under `assets/input_images/` following the [archive import guide](../docs/ARCHIVE_IMPORT.md).

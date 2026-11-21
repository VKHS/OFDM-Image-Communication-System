# Imported original assets and extraction guide

**Project author: Vahab Khalili.**

The original source files are now preserved directly inside the GitHub repository:

- [Historical Lena and OFDM results (80 JPG)](../figures/historical/image_outputs)
- [Browsable result matrix](HISTORICAL_RESULTS.md)
- [Original image inputs](../assets/input_images)
- [Original MATLAB scripts](../matlab/legacy)
- [42 Simulink/legacy models plus five support files](../archive/archived_simulink_models.zip)
- [155 original extracted report images: parts 01–06](../archive)
- [49 supplementary design/reference outputs in one ZIP](../archive/new_design_and_recomputed_figures.zip)
- [Model inventory](../models/MODEL_INVENTORY.csv)
- [Figure inventory](../figures/ARCHIVED_FIGURE_INDEX.csv)

To unpack the models from the repository root:

```bash
python -m zipfile -e archive/archived_simulink_models.zip .
```

Extract report_figures_01.zip through report_figures_06.zip in the same way to restore the report_figures folder. The larger offline master ZIP additionally preserves embedded EMF report media and a PDF atlas.

Note that GitHub import establishes preservation, **not** reproducible execution of historical MATLAB/Simulink models. The new Python reference has separate CI and the newly authored MATLAB reference has not been executed in this environment.
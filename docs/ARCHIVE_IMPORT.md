# Bringing the full historical source package into a local checkout

**Author: Vahab Khalili.**

The earlier consolidated project package contains archived MATLAB/Simulink models, MATLAB scripts, source images, source-inventory records, 400+ indexed figure assets and a figure atlas. **Those binary assets were not uploaded by the initial GitHub connection update.** This document makes the missing import explicit rather than linking nonexistent repository files.

## Suggested permanent directory locations

```text
archive/
  models/            MATLAB/Simulink .slx and .mdl files
  matlab/            Original .m scripts
  inputs/            Sample input images / .mat data
  historical_figures/ Saved reconstruction and BER figures
  figure_atlas/      PDF atlas and original image media
```

The source ZIP provided separately with the project can be extracted locally, with the corresponding model and figure directories transferred into these destinations. Keep the archival model content byte-for-byte unchanged and record SHA-256 checksums for each file. Do not convert a screenshot to a fictional HDL source or represent a legacy model as having passed GitHub CI.

## Large-file considerations

If the archive is committed to Git, GitHub recommends keeping individual files well below its hard per-file limit. For large media assets, Git LFS is preferable. Avoid committing caches or duplicate output archives alongside their extracted contents.

## Verification separation

The numerical reference tests in `tests/` continue to run without MATLAB or the historical bundle. A separate MATLAB CI job should be enabled only where licenses, MATLAB releases, and model preload requirements have been confirmed.

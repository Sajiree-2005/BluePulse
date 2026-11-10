# Real audio sources (links verified by search on 8 Nov 2026; I could NOT download any audio from the build environment)

| Class | Source | Link | Access / licence |
|---|---|---|---|
| **blast** | BombDetect (ZSL/UCL, Williams et al. 2026) | Paper (open access): https://zslpublications.onlinelibrary.wiley.com/doi/10.1002/rse2.70093 · Code: https://github.com/ben-williams-ai/Bomb-Fishing | Code is open source per Yale E360. **Whether labelled audio is in the repo is unverified: open it. If not, email the authors (Ben Williams, UCL/ZSL) and ask for labelled clips.** |
| blast (background) | Tanzania blast-fishing study (SoundSort) | https://northridgegroup.wp.st-andrews.ac.uk/detecting-illegal-fishing-in-tanzania/ | Describes method; no data download seen |
| **vessel** | ShipsEar (Univ. of Vigo) | https://underwaternoise.atlanttic.uvigo.es/ | Sample files downloadable on the site; **full database by email request** (contact on the page). 90 recordings, 11 vessel types |
| vessel | DS3500 (ShipsEar-derived, 16 kHz segments) | search "DS3500 ship radiated noise dataset" on ModelScope (a mirror page lists CC BY) | **Verify the licence and original source yourself** |
| vessel | DeepShip (47 h, 265 ships) | cited as public in https://arxiv.org/pdf/2407.13264 | **Find the download link in that paper's references**; I could not verify a URL |
| **ambient / background / some biology** | NOAA NCEI Passive Acoustic Data (SanctSound) | Console: https://console.cloud.google.com/storage/browser/noaa-passive-bioacoustic/sanctsound/audio · Portal: https://www.ncei.noaa.gov/products/passive-acoustic-data · CLI: `gsutil -m cp -r gs://noaa-passive-bioacoustic/...` | Free, public. Citation DOI in each ReadMe. **Unlabelled**: treat as ambient |
| biology (coral reef) | Not found | Search Zenodo for "coral reef soundscape", "snapping shrimp", "reef fish chorus" with CC licences | **You must find and check one** |

## Workflow
1. Download a small amount of each (a few hundred 3 s clips per class is enough to start).
2. `python ml/prepare_clips.py --src <folder> --label vessel --site shipsear` (also `blast`, `ambient`, `biology`, `environmental_noise`).
3. `python ml/build_manifest.py` (adds clearly-marked synthetic blasts).
4. Colab: `ml/train_ast.py` then `ml/export_onnx.py`.
5. Write every source, link, licence and date into `DATA_CARD.md`.

## Facts to cite in documentation and demos (from the sources above)
BombDetect study: 3,567 verified incidents in 3,650+ hours of audio over 16 months (483 days), HydroMoth recorder at 17 m depth, detection radius almost 17 km, about one blast every 62 minutes, human review reduced more than 50 times, peak 9-10 am and fewer on Fridays.

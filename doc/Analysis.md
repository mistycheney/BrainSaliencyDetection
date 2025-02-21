Figures and plots are in [dropbox](https://www.dropbox.com/sh/42cl7qb27i3c0sx/AAA1WXbFP8W5EzAFQguUSu1ba?dl=0).

# Population variability

- deviation vector from mean position
- RMS variation distance in 3D, as well as in rostral-caudal, dorsal-ventral and lateral medial axes.
- non-isotropy of variation

`registration/update_atlas.ipynb`

# Registration Error

### Compared to ChAT labels

For the two ChAT brains (CHATM2, CHATM3), the registration error is measured for every motor nuclei by comparing every aligned atlas structure volume with the structure volume manually demarcated based on ChAT markers, in terms of:
- error in 3-D centroid position
- Jaccard overlap index

The metrics are computed in `registration/evaluate_registration_metrics_v2_compute_deviation_vs_ChAT.ipynb`. 
Results for local registration are stored at:
`Registration/compare_with_CHAT/measurements/local_registration_metrics_allStacks_allStructures_allLevels.json`

### Compared to human expert annotations

For the three brains with human annotation (MD585,MD589,MD594), the registration error is measured by comparing every aligned atlas structure volume to manually demarcated structure volume, in terms of:
- error in 3-D centroid position
- Jaccard overlap index
- average per-voxel probability value difference

The computation is implemented in `registration/evaluate_registration_metrics_v2_compute_deviation_vs_expert.ipynb`. Results are stored at:
- after global registration:
`Registration/compare_vs_expert_annotation/measurements/global_registration_metrics_allStacks_allStructures_allLevels_withBestAlignBaseline.json`
- after local registration:
`Registration/compare_vs_expert_annotation/measurements/local_registration_metrics_allStacks_allStructures_allLevels_withBestAlignBaseline.json`


# Human Correction

### Quantify human correction
`registration/analyze_human_correction.ipynb`
  
### Global to local difference
`registration/update_atlas.ipynb`

### local to human difference
`registration/update_atlas.ipynb`

# Registration Confidence

- z-score for global and local registration
- peak width in most uncertain direction:
- peak width in most certain direction:

`registration/measure_confidence_v4.ipynb`

`/home/yuncong/Dropbox/BrainProjectFiguresByTopic/Registration/confidence/measurements/peakradius_max_normalized_allstacks_allstructures_allsteps_allpools.json`



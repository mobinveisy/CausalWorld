# Real-world capture protocol

## Goal
Create matched counterfactual pairs where the **only intended physical change is hidden mass of object B**.

## Rig
- smartphone at 120 fps preferred (60 fps minimum)
- fixed tripod
- straight, level, low-friction surface
- repeatable launcher for object A
- object A with fixed mass
- object B with identical external shell for every trial
- hidden internal weights inside B
- same ArUco ID on B for every mass
- calibration ruler in the motion plane

## Recommended masses
Train: 150, 200, 300, 400, 500 g  
Interpolation: 250 g  
Extrapolation: 650 g

Adjust if collision effects are too small/large.

## Conditions per training mass
- 3 launcher speeds
- 3 starting positions
- 10 repeats

= 90 clips / mass, 450 clips for five training masses.

For held-out masses, use the same launcher/position grid and at least 5-10 repeats.

## Matched pair
A factual and counterfactual clip share `pair_id` when:
- same camera
- same launcher setting
- same initial positions
- same object shells
- same marker IDs
- recorded in the same session

Only hidden B mass changes.

## Anti-leakage
Never let mass correlate with:
- color
- marker ID
- background
- day/session
- camera angle
- file naming exposed to the model

## Pipeline
1. Track:
`python real_video/track_aruco.py ...`
2. Calibrate:
`python real_video/calibrate_scale.py --known-meters 0.50 --pixel-distance 812`
3. Convert:
`python real_video/csv_to_states.py ...`
4. QC plot:
`python real_video/qc_plot.py ...`
5. Add to manifest.

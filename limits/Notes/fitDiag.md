# Notes for FitDiagnostics
-- These notes are more aimed at plotting, see GoF notes for submitting

run fit diagnositics with the right tag
prepareModels/SubmitAllFitDiagnostic.sh
more info in GoF notes

plotting scripts for 1d and 2d rerolled are in this vim session

to get covariance quality values:
use the right tag in:
source ./FitDiagnostics/copyFilesLocal.sh

and use right tag in:
source ./FitDiagnostics/covQual/getVals.sh
outputfiles are saved in:
./FitDiagnostics/covQual/covQual_<tag>_b.txt

register in vim to clean the output:
set @q=dd02dtFdt24ldtM2dtMi fdfihDjddkJj


For Plotting:
scripts/plotting/PlotFitDiagnosticsSHAPES.py

for distrbution of events for different binning
plotting/PlotFitDiagnosticsSHAPES_NumEvents.py

copying files from eos to local lpc space:
FitDiagnostics/copyFilesLocal.sh

# 2023 Sep 26

rerolling scripts added
scripts/plotting/RerollEvents.py
run with
source ./scripts/plotting/Reroll.sh

- adding 1d eventDist plots for lowStatsCut_5ev tag
- now also running with harder cuts 10ev (no bins with less than ~10 events)

have to run this first (pick the more granual binning for next steps, 100 bins are for looking at the plots)

scripts/plotting/PlotFitDiagnosticsSHAPES_NumEvents_comp_5ev.py
it saves txt files of the num of events for different cuts
then run:
scripts/plotting/FitDiag_EventDist_compare3_5ev.py
from
source ./scripts/plotting/compareEventDist3_5ev.sh


# 2023 Dec11

tag 2023Dec7_binMYx2_addMX650_10ev

after adding mX=650 mass points
ran jobs using notes in GoF.md

copied files from eos to local lpc space:
FitDiagnostics/copyFilesLocal.sh

syncing jobs to local mac in folder plotting/FitDiag_2023Dec

!used for unblinding step 3
update tag and run:
for unrolled plots:
python scripts/plotting/PlotFitDiagnosticsSHAPES.py
for 2d pulls of the 1d ratio:
(renamed the output directory to SHAPES_1D_* in stead of plots_*SHAPES)

!used for unblinding step 3
./scripts/plotting/runAllFitDiag2Dpull.sh
which runs:
scripts/plotting/FitDiag2Dpull.py

---
The reroll plots the background model with an upper limit on the z axis of 10 events
- this was used for determining the bins to cut in the lower left part of the mX-mY plane
reroll:
./scripts/plotting/Reroll.sh
which runs:
scripts/plotting/RerollEvents.py

---
used for investigating the number of events in each bin in the background
python scripts/plotting/PlotFitDiagnosticsSHAPES_NumEvents_comp.py
output folder: 'plots_2023Jul5_nonClosureMCStats2_SRvs2023Jul5_binMYx2_ncMCStats_SREventDist'

python scripts/plotting/FitDiag_EventDist_compare3.py --year 2016 --monitor mean
output folder: 'EventDist_2023Sep'

---



# 2023 Dec 12

python scripts/plotting/PlotFitDiagnosticsSHAPES.py
./scripts/plotting/runAllFitDiag2Dpull.sh
scripts/plotting/FitDiag2Dpull.py

- Definition of pull
    - set as (data-bkg) / sigma
    - clarify what sigma is used

- set as (data-bkg) / sigma
- show uncertainty on data and background in the unrolled plots
- add better bin labels on the unrolled plots

quote from Arne:

Could you please clarify your definition of "pull"?
It seems to be something like "(bkg - data) / sigma", while one is used to look at (data-bkg) / sigma", please move to the latter.
Also, please clarify what sigma is used here and
show the uncertainty in the data and background
    using error bars and shaded/hatched bands where applicable.

In addition, please
add some indication in the unrolled distributions that show the mY and mX a given bin corresponds to
(e.g., repeating bins on the x-axis to indicate one dimension and vertical lines that separate one slice from another).

At the same time, please proceed to the final step of unblinding,
"Derive observed limits (and post-fit expected limits) and signal strength/significance for the largest excess observed" as described on the twiki.


# 2024 Jan 24

working on printing pull difference between b-only fit and s+b fit
submitted fit diagnostics for two highest local significance points (see GoF.vim session)

source ./FitDiagnostics/copyFilesLocal.sh
source scripts/plotting/comparePulls_2024Jan24.sh

- for largest signficance points, plotting:

python scripts/plotting/PlotFitDiagnosticsSHAPES_LocalSignfPoints.py


./scripts/plotting/runAllFitDiag2Dpull_LocalSignfPoints.sh
scripts/plotting/FitDiag2Dpull_LocalSignfPoints.py

# 2024 Apr 16

for CMSweek slides, needed a zoom version of the plot:
./scripts/plotting/runAllFitDiag2Dpull_LocalSignfPoints.sh
scripts/plotting/FitDiag2Dpull_LocalSignfPoints_pullZoom_2024Apr16.py

# 2024 Oct 3

look at largest deficit points
Ran fit diagnostics - as described above 2024 Jan24

added 3 mass points (largest deficits) to this file
and changed to mass group0
also adjusted y setrangeuser (should only impact the negative values)

python3 scripts/plotting/PlotFitDiagnosticsSHAPES_LocalSignfPoints.py



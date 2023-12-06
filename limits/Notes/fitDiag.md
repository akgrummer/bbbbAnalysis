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
bbbbAnalysis/scripts/plotting/PlotFitDiagnosticsSHAPES.py

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




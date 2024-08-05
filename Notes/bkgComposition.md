
for original plots:
scripts/privateScript/StackPlots.C

new plots for full, 3b,4b, and mY around 90 versions:
scripts/privateScript/StackPlots_mY90GeV.C

uses:
root -l -b scripts/privateScript/StackPlots_mY90GeV.C

run all parameter checks with:
./scripts/runBkgCompPlots.sh

ran the script twice.
First time with save values set to TRUE in the shell script
and set mininum to 1e-5:
if (mYlabel.Contains(91)) theBackgroundStack->SetMinimum(0.00001);
else if (mYlabel.Contains(100)) theBackgroundStack->SetMinimum(0.00001);
else theBackgroundStack->SetMinimum(0.00001);

Second time with save values set to FALSE in the shell script
and set mininum to 1e-5, 1e-4, and 1e-3 for differen mY cuts:
if (mYlabel.Contains(91)) theBackgroundStack->SetMinimum(0.00001);
else if (mYlabel.Contains(100)) theBackgroundStack->SetMinimum(0.0001);
else theBackgroundStack->SetMinimum(0.001);

# 2024 Jun 24

rerun and compare slices of mX, plotted with mY on the horizontal axis

tag="2024Jun21_vars_mY90_mX340"
tag="2024Jun21_vars_mY90_mX488"
tag="2024Jun21_vars_mY90_mX648"
tag="2024Jun21_vars_mY90_mX960"
tag="2024Jun21_vars_mY90_mX340to1216"
tag="2024Jun21_vars_mY90_mX340_3b"
tag="2024Jun21_vars_mY90_mX488_3b"
tag="2024Jun21_vars_mY90_mX648_3b"
tag="2024Jun21_vars_mY90_mX960_3b"
tag="2024Jun21_vars_mY90_mX340to1216_3b"




# 2024 Jun27

Adding Z+jets background
has to be in UL


./scripts/runBkgCompPlots_Zjets.sh
ran values for the mX cuts,

run scripts/cleanBkgCompVals.sh to clean bkg vals




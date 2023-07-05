# Add HourGlass Uncertainty to the unrolled plots

- applied after the unrolling step
- code is in:
    - scripts/add_hourglass_unc.C
    - hourglassUnc/Makefile

compile with: make
in bbbbAnalysis/hourglassUnc
vim-session/hourglassUnc.vim

Lots of warnings of type:
"This should not happen!!!"
this is also from unrolling code from Fabio.


for VR plotting (only plotting)
    use
    - scripts/add_hourglass_unc_VR.C
    make add_hourglass_unc_VR

for VR for preparing HISTs for Limits and GoF
    use
    - scripts/add_hourglass_unc_VR_forLimits.C
    need the TARGET name (run from hourglassUnc/)
    make add_hourglass_unc_VR_forLimits

    differences from the nominal are the region pointed to in the outPlotter.root file
    and the tag where I copied the outPlotter_massgroup* files

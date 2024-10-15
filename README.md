# bbbbAnalysis

## Install instructions

Mileage may vary for these instructions. These were performed on LPC cluster using scientific linux 7 OS. (Prior to the introduction of el8 or el9).
Using a slc7 image in singularity has been necessary for continued use of some scripts in the repo.

```
cmsrel CMSSW_10_2_5
cd CMSSW_10_2_5/src
cmsenv
git cms-addpkg PhysicsTools/KinFitter CommonTools/Utils CondFormats/JetMETObjects CondFormats/Serialization FWCore/MessageLogger FWCore/Utilities JetMETCorrections/Modules
scram b -j 8
git clone https://github.com/fravera/bbbbAnalysis.git
git checkout mlBranch
```

## Setup and compile
```
# from bbbbAnalysis/
cmsenv
source scripts/setup.sh # only needed once for every new shell
make exe -j # compiles and makes everything under test/ executable
````

## Make a skim of NanoAOD
For data:
```
skim_ntuple.exe --input inputFiles/2016_NMSSM_XYH_bbbb_Datasets/BTagCSV_Data.txt --cfg config/Resonant_NMSSM_bbbb/skim_2016Resonant_NMSSM_XYH_bbbb.cfg --is-data --output test_NMSSM_XYH_bbbb_Data.root --maxEvts 1000000
````
For fast sim signal
```
skim_ntuple.exe --cfg config/Resonant_NMSSM_bbbb/skim_2016Resonant_NMSSM_XYH_bbbb_Fast.cfg --input inputFiles/2016_NMSSM_XYH_bbbb_Datasets/NMSSM_XYH_bbbb_MX_700_NANOAOD_v7.txt --output test_NMSSM_XYH_bbbb_MC.root --is-signal --xs=1 --puWeight weights/2016_NMSSM_XYH_bbbb_weights/NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_PUweights.root --maxEvt 100000
```

## Fill histograms from skims
```
fill_histograms.exe config/Resonant_NMSSM_bbbb/MXless1000_MYgreater140/plotter_2016Resonant_NMSSM_XYH_bbbb.cfg
````

## Make plots
"NOT WORKING FOR RESONANT ANALYSIS"
Use the ``plotter/plotter.py`` script. Styles (line colors, etc.) for the processes are defined in ``plotter/styles/plotStyles.py``
Inside the script, the subset of processes to run on is defined through ``bkgToPlot`` and  ``sigToPlot``.
Several cmd line options available to configure the plot, it's practical to make a script that produces all the plots.
Example:
```
source do_all_plots.sh
````

## Machine learning skims using pandas dataframes
Probably you may need to instull some updates of libraries, run
```
pip install --user --upgrade matplotlib
pip install --user --upgrade scikit-learn
pip install --user --upgrade hep-ml
```

Edit in the mlskim_NMSSM_XYH_bbbb/config/<file> the cuts, variable, samples and weight name
```
python mlskim_NMSSM_XYH_bbbb/BuildBackgroundModel.py --config=mlskim_NMSSM_XYH_bbbb/config/outputskim_2016.cfg
````
this will crate a folder with the model within BackgroundModels
Now you can run the next step that will create the a new branch in the origina tree containing the weigths for the BDT weights
```
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BackgroundModels/Reweight_<weightName>
```

Note: weight name must be unique otherwise you will not be able to create the new branch in the tree
make sure you hhave write permission on the input skims
Remember to apply the weight to the fill histogram to use the while filling the plots

## Unroll 2D HH_m vs H2_m plot:
./scripts/Unroll2Dplots 2016DataPlots_NMSSM_XYH_bbbb_Fast/outPlotter.root data_BTagCSV_dataDriven selectionbJets_SignalRegion HH_m_H2_m selectionbJets_ControlRegionBlinded selectionbJets_SideBandBlinded


## Produce ratio plots to check BDT reweight model:
root -l
.L privateTools/RatioPlot.C+
RatioAll()

## Create datacards for limits
cd limits
edit CreateAllDatacards.sh
source CreateAllDatacards.sh

## Running combine
Log on a CentOS 7 machine (lxplus, cmslpc-sl7) and install combine following the instructions [here](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/#for-end-users-that-dont-need-to-commit-or-do-any-development)

After installing it, from the HiggsAnalysis/CombinedLimit directory do
ln -s <path_to_bbbbAnalysis>/limits limits

Scripts for running combine are under ``limits``.

# 2024 Oct. Organization of the whole analysis chain

Navigating this repo is possible through the use of vim sessions.
These sessions may be found in the folders:

`vim-sessions/` and `limits/vim-sessions/'

The major steps of the analysis are in the sessions listed below. If you don't use vim-sessions these files may be opened with any text editor to extract the list of important files for that analysis step.

In addition to these sessions there are files containing specific notes for each major analysis step. These are in the directories `Notes` and `limits/Notes`. Most vim-sessions open (or point someone to) to the relevant notes file.

#### skimming
- skimming_MoreSignals.vim
- skimming_ZjetsSamples.vim

#### BDT
- BDT.vim
- BDT-Uncertainties.vim
- Sess_BDToffshell.vim


#### fill hists
- fillHists.vim
- plotting.vim

#### unroll hists
- Unroll.vim
- unrollPlots.vim
- Unroll-FullPlane.vim

#### misc.
- NormUnc.vim
- bkgComposition.vim
- hourglassUnc.vim
- createPseudoDatasets.vim
- pairingEfficiency.vim
- selfBias.vim


#### limits:

- running limits: `limits/vim-sessions/limits.vim`
- running goodness of fit tests: `limits/vim-sessions/GoF.vim`
- running fit diagnostics: `limits/vim-sessions/FitDiagnostics.vim`
- compiling, plotting, studying results: `limits/vim-sessions/produceResults.vim`
- global significance: `limits/vim-sessions/LEE.vim`







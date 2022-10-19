version of matplotlib is too old in the setup commands. 
version is 1.5.2 - determined using <AidanTest.py> 
which just prints the version:
import matplotlib
print(matplotlib.__version__)

replaced "density" with "normed" in 10 locations in modules/plotter.py
and one instance in modules/bdtreweighter.py

*********
Build Background commands
from:
/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis
run:
python mlskim_NMSSM_XYH_bbbb/BuildBackgroundModel.py --config mlskim_NMSSM_XYH_bbbb/config/outputskim_2016_Full_kinFit.cfg
python mlskim_NMSSM_XYH_bbbb/BuildBackgroundModel.py --config mlskim_NMSSM_XYH_bbbb/config/outputskim_2017_Full_kinFit.cfg
python mlskim_NMSSM_XYH_bbbb/BuildBackgroundModel.py --config mlskim_NMSSM_XYH_bbbb/config/outputskim_2018_Full_kinFit.cfg


*********
test making plots
*********

python mlskim_NMSSM_XYH_bbbb/makeplots.py --config mlskim_NMSSM_XYH_bbbb/config/outputskim_2017_Full_kinFit.cfg

*********
*********
Apply Background commands

python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BackgroundModels/Reweight_fullSubmission_2016_v27_PtRegressedAndHigherLevel_kinFit_nTree_500_aidan_2021Dec8/
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BackgroundModels/Reweight_fullSubmission_2017_v27_PtRegressedAndHigherLevel_kinFit_nTree_500_aidan_2021Dec8/
python mlskim_NMSSM_XYH_bbbb/ApplyBackgroundModel.py --dir BackgroundModels/Reweight_fullSubmission_2018_v27_PtRegressedAndHigherLevel_kinFit_nTree_500_aidan_2021Dec8/

*********
---- Copy files on eos from Fabio ---
*********
need to have the following command for copying from one user to another:
export EOS_MGM_URL=root://cmseos.fnal.gov


python mlskim_NMSSM_XYH_bbbb/makeplots.py --config mlskim_NMSSM_XYH_bbbb/config/outputskim_2017_Full_kinFit.cfg

/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/config/Resonant_NMSSM_bbbb/selectionCfg_2017Resonant_NMSSM_XYH_bbbb_all.cfg


eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2017_v27/SKIM_BTagCSV_Data/filelist/ /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2017_v27/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2017_v27/SKIM_BTagCSV_Data/output/ /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2017_v27/

eosls /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2016_v27/SKIM_BTagCSV_Data/
eosls /store/user/fravera/bbbb_ntuples/fullSubmission_2018_v27/SKIM_JetHT_Data/

eosmkdir /store/user/agrummer/bbbb_ntuples/fullSubmission_2016_v27
eosmkdir /store/user/agrummer/bbbb_ntuples/fullSubmission_2016_v27/SKIM_BTagCSV_Data
eosmkdir /store/user/agrummer/bbbb_ntuples/fullSubmission_2018_v27/
eosmkdir /store/user/agrummer/bbbb_ntuples/fullSubmission_2018_v27/SKIM_JetHT_Data

eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2016_v27/SKIM_BTagCSV_Data/ /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2016_v27/

eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2018_v27/SKIM_JetHT_Data/ /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2018_v27/

eosls /store/user/agrummer/bbbb_ntuples/fullSubmission_2016_v27/SKIM_BTagCSV_Data
eosls /store/user/agrummer/bbbb_ntuples/fullSubmission_2017_v27/SKIM_BTagCSV_Data
eosls /store/user/agrummer/bbbb_ntuples/fullSubmission_2018_v27/SKIM_JetHT_Data

eos cp -r /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2017_v27/filelist/ /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2017_v27/SKIM_BTagCSV_Data/

eos root://cmseos.fnal.gov mv /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2017_v27/output/ /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2017_v27/SKIM_BTagCSV_Data/ 

eosrm -r /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2017_v27/filelist/

eosrm -r /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2016_v27/SKIM_BTagCSV_Data
eosrm -r /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2017_v27/SKIM_BTagCSV_Data
eosrm -r /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2018_v27/SKIM_JetHT_Data

eosrm -r /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2016_v27
eosrm -r /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2017_v27
eosrm -r /eos/uscms/store/user/agrummer/bbbb_ntuples/fullSubmission_2018_v27


eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2016_v27/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2017_v27/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2018_v27/ /eos/uscms/store/user/agrummer/bbbb_ntuples/

<!-- eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2016_v27/ /eos/uscms/store/user/agrummer/bbbb_ntuples/ -->
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2016_v27_Total_down/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2016_v27_Total_up/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2016_v27_bjer_down/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2016_v27_bjer_up/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2016_v27_jer_down/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2016_v27_jer_up/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
<!-- eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2017_v27/ /eos/uscms/store/user/agrummer/bbbb_ntuples/ -->
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2017_v27_Total_down/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2017_v27_Total_up/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2017_v27_bjer_down/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2017_v27_bjer_up/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2017_v27_jer_down/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2017_v27_jer_up/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
<!-- eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2018_v27/ /eos/uscms/store/user/agrummer/bbbb_ntuples/ -->
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2018_v27_Total_down/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2018_v27_Total_up/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2018_v27_bjer_down/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2018_v27_bjer_up/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2018_v27_jer_down/ /eos/uscms/store/user/agrummer/bbbb_ntuples/
eos cp -r /eos/uscms/store/user/fravera/bbbb_ntuples/fullSubmission_2018_v27_jer_up/ /eos/uscms/store/user/agrummer/bbbb_ntuples/

eosls /eos/uscms/store/user/agrummer/bbbb_ntuples/
*********
*********
plotting (from Fabio) after applying BDT weights and preparing for Combine:

2021 Dec 8 and 9
fill_histograms.exe config/Resonant_NMSSM_bbbb/plotter_2017Resonant_NMSSM_XYH_bbbb_Full_quicktest_2021Dec8.cfg
cd 2017DataPlots_NMSSM_XYH_bbbb_dataDrivenStudies_aidan/
root -l outPlotter.root


fill_histograms.exe config/Resonant_NMSSM_bbbb/plotter_2018Resonant_NMSSM_XYH_bbbb_Full_quicktest_2021Dec8.cfg
fill_histograms.exe config/Resonant_NMSSM_bbbb/plotter_2016Resonant_NMSSM_XYH_bbbb_Full_quicktest_2021Dec8.cfg

the systematic weights (uncertainties) are in this file:
config/Resonant_NMSSM_bbbb/selectionCfg_2017Resonant_NMSSM_XYH_bbbb_all.cfg
the binning is also in this file

unroll 2d histogram plots
(plots in the control region)
scripts/UnrollAllSubdirControlTest.sh
scripts/Unroll2DplotsSubRangeControlTest.cc

copied and then modified from 
scripts/UnrollAllSubdirValidationTest.sh
scripts/Unroll2DplotsSubRangeValidationTest.cc

source ./scripts/UnrollAllSubdirControlTest.sh 2016

Produce plots for validation of BKG model in VR now modified for CR
root -l
.L scripts/modifyPlotForControlTest.C+
void modifyAllPlotForControlTest(std::string tag = "NMSSM_XYH_bbbb_dataDrivenStudies_aidan")

run combine from 
cmsrel CMSSW_10_2_13

followed instructions from here;
https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/#for-end-users-that-dont-need-to-commit-or-do-any-development

cd nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/

limits/prepareModels/SubmitFullRunIILimits.py
/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/limits/prepareModels/SubmitFullRunIILimits.py

python prepareModels/SubmitFullRunIILimits.py --tag <tag_name> --year RunII --group auto --unblind 
python prepareModels/SubmitFullRunIILimits.py --tag aidanTag2 --year RunII --group auto --unblind

the config files for running the limits are here:
limits/prepareModels/config/LimitsConfig_2016.cfg
limits/prepareModels/config/LimitsConfig_2017.cfg
limits/prepareModels/config/LimitsConfig_2018.cfg

in the output log files - 
in /uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/limits/jobsLimits_aidanTag2/
with file names *.stdout
look for AsymptoticLimits 

this is the list of samples to run (commented all out except 5, Dec 14)
/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/limits/prepareModels/listOfSamples.txt

this produces the limits plts
/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/limits/produceAllResults.sh

need to change the weight in all years for this file:
/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/config/Resonant_NMSSM_bbbb/selectionCfg_2017Resonant_NMSSM_XYH_bbbb_all.cfg


xrdcp root://cms-xrd-global.cern.ch//store/user/fravera/bbbb_limits/<tag>/HistogramFiles_<year>/outPlotter_<year>_<signalName>.root DatacardFolder_<year>

datacard_<year>_<signal>.txt

xrdcp root://cms-xrd-global.cern.ch//store/user/fravera/bbbb_limits/<tag>/HistogramFiles_<year>/outPlotter_<year>_<signalName>.root DatacardFolder_<year>

copy these files using a shell script, one by one, on to lxplus:
xrdcp root://cms-xrd-global.cern.ch//store/user/agrummer/bbbb_limits/aidan_2021Dec15/HistogramFiles_2016 ./
look up the file names on lpc:
eosls /store/user/agrummer/bbbb_limits/aidan_2021Dec15/HistogramFiles_2017

convert the datacard to a workspace
text2workspace.py datacard_2017_sig_NMSSM_bbbb_MX_1000_MY_300.txt

run the limits
combine datacard_2017_sig_NMSSM_bbbb_MX_1000_MY_300.root -M AsymptoticLimits --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH

combine -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_1000_MY_300.root --algo=KS --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH -n AidanName
combine -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_1000_MY_300.root --algo=KS -t 1000 -s 1524

run on the grid (condor):
combineTool.py -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_1000_MY_300.root --algo=KS -t 1000 -s 1524 --job-mode condor --task-name goodnessOfFit_test --sub-opts='+JobFlavour="tomorrow"'

    signals = sig_NMSSM_bbbb_MX_700_MY_300, sig_NMSSM_bbbb_MX_500_MY_200, sig_NMSSM_bbbb_MX_900_MY_400, sig_NMSSM_bbbb_MX_1400_MY_600, sig_NMSSM_bbbb_MX_1800_MY_800, sig_NMSSM_bbbb_MX_300_MY_125, sig_NMSSM_bbbb_MX_300_MY_150, sig_NMSSM_bbbb_MX_600_MY_400, sig_NMSSM_bbbb_MX_700_MY_500, sig_NMSSM_bbbb_MX_800_MY_600, sig_NMSSM_bbbb_MX_900_MY_250, sig_NMSSM_bbbb_MX_1000_MY_300, sig_NMSSM_bbbb_MX_1200_MY_200 
text2workspace.py datacard_2017_sig_NMSSM_bbbb_MX_1000_MY_300.txt
text2workspace.py datacard_2017_sig_NMSSM_bbbb_MX_1200_MY_200.txt
text2workspace.py datacard_2017_sig_NMSSM_bbbb_MX_1400_MY_600.txt
text2workspace.py datacard_2017_sig_NMSSM_bbbb_MX_1800_MY_800.txt
text2workspace.py datacard_2017_sig_NMSSM_bbbb_MX_300_MY_125.txt
text2workspace.py datacard_2017_sig_NMSSM_bbbb_MX_300_MY_150.txt
text2workspace.py datacard_2017_sig_NMSSM_bbbb_MX_500_MY_200.txt
text2workspace.py datacard_2017_sig_NMSSM_bbbb_MX_600_MY_400.txt
text2workspace.py datacard_2017_sig_NMSSM_bbbb_MX_700_MY_300.txt
text2workspace.py datacard_2017_sig_NMSSM_bbbb_MX_700_MY_500.txt
text2workspace.py datacard_2017_sig_NMSSM_bbbb_MX_800_MY_600.txt
text2workspace.py datacard_2017_sig_NMSSM_bbbb_MX_900_MY_250.txt
text2workspace.py datacard_2017_sig_NMSSM_bbbb_MX_900_MY_400.txt
combineTool.py -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_1200_MY_200.root --algo=KS -t 1000 -s 1524 -n MX_1200_MY_200 --job-mode condor --task-name goodnessOfFit_MX_1200_MY_200 --sub-opts='+JobFlavour="tomorrow"'
combineTool.py -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_1800_MY_800.root --algo=KS -t 1000 -s 1524 -n MX_1800_MY_800 --job-mode condor --task-name goodnessOfFit_MX_1800_MY_800 --sub-opts='+JobFlavour="tomorrow"'
combineTool.py -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_1400_MY_600.root --algo=KS -t 1000 -s 1524 -n MX_1400_MY_600 --job-mode condor --task-name goodnessOfFit_MX_1400_MY_600 --sub-opts='+JobFlavour="tomorrow"'
combineTool.py -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_300_MY_125.root --algo=KS -t 1000 -s 1524 -n MX_300_MY_125 --job-mode condor --task-name goodnessOfFit_MX_300_MY_125 --sub-opts='+JobFlavour="tomorrow"'
combineTool.py -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_300_MY_150.root --algo=KS -t 1000 -s 1524 -n MX_300_MY_150 --job-mode condor --task-name goodnessOfFit_MX_300_MY_150 --sub-opts='+JobFlavour="tomorrow"'
combineTool.py -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_500_MY_200.root --algo=KS -t 1000 -s 1524 -n MX_500_MY_200 --job-mode condor --task-name goodnessOfFit_MX_500_MY_200 --sub-opts='+JobFlavour="tomorrow"'
combineTool.py -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_600_MY_400.root --algo=KS -t 1000 -s 1524 -n MX_600_MY_400 --job-mode condor --task-name goodnessOfFit_MX_600_MY_400 --sub-opts='+JobFlavour="tomorrow"'
combineTool.py -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_700_MY_300.root --algo=KS -t 1000 -s 1524 -n MX_700_MY_300 --job-mode condor --task-name goodnessOfFit_MX_700_MY_300 --sub-opts='+JobFlavour="tomorrow"'
combineTool.py -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_700_MY_500.root --algo=KS -t 1000 -s 1524 -n MX_700_MY_500 --job-mode condor --task-name goodnessOfFit_MX_700_MY_500 --sub-opts='+JobFlavour="tomorrow"'
combineTool.py -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_800_MY_600.root --algo=KS -t 1000 -s 1524 -n MX_800_MY_600 --job-mode condor --task-name goodnessOfFit_MX_800_MY_600 --sub-opts='+JobFlavour="tomorrow"'
combineTool.py -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_900_MY_250.root --algo=KS -t 1000 -s 1524 -n MX_900_MY_250 --job-mode condor --task-name goodnessOfFit_MX_900_MY_250 --sub-opts='+JobFlavour="tomorrow"'
combineTool.py -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_900_MY_400.root --algo=KS -t 1000 -s 1524 -n MX_900_MY_400 --job-mode condor --task-name goodnessOfFit_MX_900_MY_400 --sub-opts='+JobFlavour="tomorrow"'
combineTool.py -M GoodnessOfFit datacard_2017_sig_NMSSM_bbbb_MX_1000_MY_300.root --algo=KS -t 1000 -s 1524 -n MX_1000_MY_300 --job-mode condor --task-name goodnessOfFit_MX_1000_MY_300 --sub-opts='+JobFlavour="tomorrow"'

MX_1000_MY_300: 0.0055899 
MX_1200_MY_200: 0.00406811 
MX_1400_MY_600: 0.00406816
MX_1800_MY_800: 
MX_300_MY_125: 
MX_300_MY_150: 0.00527359
MX_500_MY_200: 
MX_600_MY_400: 
MX_700_MY_300: 0.0029242 
MX_700_MY_500: 0.00432785 
MX_800_MY_600: 0.00389836 
MX_900_MY_250: 0.00558995 
MX_900_MY_400: 0.00595663 
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

*********
*********
plotting (from Fabio) after applying BDT weights and preparing for Combine:

fill_histograms.exe config/Resonant_NMSSM_bbbb/plotter_2017Resonant_NMSSM_XYH_bbbb_Full_quicktest_2021Dec8.cfg
cd 2017DataPlots_NMSSM_XYH_bbbb_dataDrivenStudies_aidan/
root -l outPlotter.root
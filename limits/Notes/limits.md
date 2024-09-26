# Notes for limits

- need to edit
(1) `directory` in the LimitConfig (`folder` does not matter)
(2) sample list to run all mass points, (point to a different list inside: prepareModels/SubmitFullRunIILimits.py - name is repeated 2 times)
(3) the tag in the command, controlling the output folder name


python prepareModels/SubmitFullRunIILimits.py --tag <tag_name> --year RunII --group auto
python prepareModels/SubmitFullRunIILimits.py --tag 2023Feb28 --year RunII --group auto

python prepareModels/SubmitFullRunIILimits.py --tag <tag_name> --year RunII --group auto --unblind



This is what I ran for limits (impacts option includes the expected limit)
python prepareModels/SubmitFullRunIILimits.py --tag 2022Nov22_bJetScoreLoose_shapes2  --year RunII --group auto --impacts
python prepareModels/SubmitFullRunIILimits.py --tag 2023Feb28  --year RunII --group auto --impacts

python prepareModels/SubmitFullRunIILimits.py --tag 2023Feb28_hourglass --year RunII --group auto --impacts

For Validation Region test (only made the histos and datacards by commenting out the combine commands - put back to normal now) :
python prepareModels/SubmitFullRunIILimits.py --tag 2023Feb28_hourglass_VR_ws --year RunII --group auto



# To Check jobs:
python scripts/getTaskStatus.py --dir CondorJobs/jobsLimits_2023Feb28/ --long
python scripts/getTaskStatus.py --dir CondorJobs/jobsLimits_2023Feb28_hourglass/ --long

These are still running:
- sig_NMSSM_bbbb_MX_1600_MY_90
- sig_NMSSM_bbbb_MX_1600_MY_100
- sig_NMSSM_bbbb_MX_1600_MY_125
- sig_NMSSM_bbbb_MX_1600_MY_300



Test locally:
- python prepareModels/prepareHistos.py --config prepareModels/config/LimitsConfig_$1.cfg --signal $n
	`python prepareModels/prepareHistos.py --config prepareModels/config/LimitsConfig_2016.cfg --signal sig_NMSSM_bbbb_MX_600_MY_400 --group 1`
	`python prepareModels/prepareHistos.py --config prepareModels/config/LimitsConfig_2017.cfg --signal sig_NMSSM_bbbb_MX_600_MY_400 --group 1`
	`python prepareModels/prepareHistos.py --config prepareModels/config/LimitsConfig_2018.cfg --signal sig_NMSSM_bbbb_MX_600_MY_400 --group 1`

# 2023 Sep 27
produceAllResults can be used
- to merge the limit results
- plot the limit results
- compare 2 limit results

ALSO CHANGE THE Limits Config files!

python prepareModels/SubmitFullRunIILimits.py --tag 2023Jul5_binMYx2_ncMCStats_lowStatsCut_10ev_SR --year RunII --group auto --impacts
python prepareModels/SubmitFullRunIILimits.py --tag 2023Jul5_binMYx2_ncMCStats_lowStatsCut_5ev_SR --year RunII --group auto --impacts
python prepareModels/SubmitFullRunIILimits.py --tag 2023Jul5_nonClosureMCStats2_SR --year RunII --group auto --impacts

python scripts/getTaskStatus.py --dir CondorJobs/jobsLimits_2023Jul5_binMYx2_ncMCStats_lowStatsCut_5ev_SR/ --long

# 2023 Dec 4

SEE notes for limits above

Submit limits:
tag="2023Nov1_binMYx2_add2017Sig_10ev"; region="SR"; python prepareModels/SubmitFullRunIILimits.py --tag ${tag}_${region} --year RunII --group auto --impacts
tag="2023Nov1_binMYx2_add2017Sig_10ev"; region="SR"; python scripts/getTaskStatus.py --dir CondorJobs/jobsLimits_${tag}_${region}/ --long

produceAllResults can be used
- to merge the limit results
- plot the limit results
- compare 2 limit results

# 2023 Dec 8

add MX 650 mass points to the sample list:
prepareModels/listOfSamples.txt

updated config files `directory` parameter

submit with:
tag="2023Dec7_binMYx2_addMX650_10ev"; region="SR"; python prepareModels/SubmitFullRunIILimits.py --tag ${tag}_${region} --year RunII --group auto --impacts
tag="2023Dec7_binMYx2_addMX650_10ev"; region="SR"; python scripts/getTaskStatus.py --dir CondorJobs/jobsLimits_${tag}_${region}/ --long

add MX 650 to group 1 in
prepareModels/SubmitFullRunIILimits.py
- line 37: mXandGroup variable definition

ran these jobs twice :/
hope there weren't race conditions - but should be fine. logs look the same
```
>>> Too many logs found for job sig_NMSSM_bbbb_MX_700_MY_60  (resubmitted?) , returning last
>>> Too many logs found for job sig_NMSSM_bbbb_MX_700_MY_70  (resubmitted?) , returning last
>>> Too many logs found for job sig_NMSSM_bbbb_MX_700_MY_80  (resubmitted?) , returning last
>>> Too many logs found for job sig_NMSSM_bbbb_MX_700_MY_90  (resubmitted?) , returning last
```

# 2023 Dec 12

remove mX=1600, mY mass below 200GeV from sample list

tag="2023Dec7_binMYx2_addMX650_10ev_rmSigs"; region="SR"; python prepareModels/SubmitFullRunIILimits.py --tag ${tag}_${region} --year RunII --group auto --impacts
tag="2023Dec7_binMYx2_addMX650_10ev_rmSigs"; region="SR"; python scripts/getTaskStatus.py --dir CondorJobs/jobsLimits_${tag}_${region}/ --long

tag="2023Dec7_binMYx2_addMX650_10ev_rmSigs"; region="VR"; python prepareModels/SubmitFullRunIILimits.py --tag ${tag}_${region} --year RunII --group auto --impacts
tag="2023Dec7_binMYx2_addMX650_10ev_rmSigs"; region="VR"; python scripts/getTaskStatus.py --dir CondorJobs/jobsLimits_${tag}_${region}/ --long


# 2023 Dec 14

tag="2023Dec7_binMYx2_addMX650_10ev_unblind"; region="SR"; python prepareModels/SubmitFullRunIILimits.py --tag ${tag}_${region} --year RunII --group auto --impacts --unblind
tag="2023Dec7_binMYx2_addMX650_10ev_unblind"; region="SR"; python scripts/getTaskStatus.py --dir CondorJobs/jobsLimits_${tag}_${region}/ --long

tag="2023Dec7_binMYx2_addMX650_10ev_unblind"; region="VR"; python prepareModels/SubmitFullRunIILimits.py --tag ${tag}_${region} --year RunII --group auto --impacts --unblind
tag="2023Dec7_binMYx2_addMX650_10ev_unblind"; region="VR"; python scripts/getTaskStatus.py --dir CondorJobs/jobsLimits_${tag}_${region}/ --long

# 2023 Dec 14

tag="2023Dec7_binMYx2_addMX650_10ev_unblind_signif"; region="SR"; python prepareModels/SubmitFullRunIIsignificance.py --tag ${tag}_${region} --year RunII --group auto --unblind
tag="2023Dec7_binMYx2_addMX650_10ev_unblind_signif"; region="SR"; python scripts/getTaskStatus.py --dir CondorJobs/Significance/jobsSignificance_${tag}_${region}/ --long

tag="2023Dec7_binMYx2_addMX650_10ev_unblind_signif_all"; region="SR"; python prepareModels/SubmitFullRunIIsignificance.py --tag ${tag}_${region} --year RunII --group auto --unblind
tag="2023Dec7_binMYx2_addMX650_10ev_unblind_signif_all"; region="SR"; python scripts/getTaskStatus.py --dir CondorJobs/Significance/jobsSignificance_${tag}_${region}/ --long

## run for the pvals

add --pval flag to the combine command in the python submission script (two places, lines 266 and 279)

tag="2023Dec7_binMYx2_addMX650_10ev_unblind_signif_all_pval"; region="SR"; python prepareModels/SubmitFullRunIIsignificance.py --tag ${tag}_${region} --year RunII --group auto --unblind
tag="2023Dec7_binMYx2_addMX650_10ev_unblind_signif_all_pval"; region="SR"; python scripts/getTaskStatus.py --dir CondorJobs/Significance/jobsSignificance_${tag}_${region}/ --long


# 2023 Dec 19

ifile=datacard_2018_sig_NMSSM_bbbb_MX_700_MY_400.txt; xrdcp root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Dec7_binMYx2_addMX650_10ev_unblind_signif_all_SR/HistogramFiles_2018/${ifile} ./${ifile}
ifile=outPlotter_2018_sig_NMSSM_bbbb_MX_700_MY_400.root; xrdcp root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Dec7_binMYx2_addMX650_10ev_unblind_signif_all_SR/HistogramFiles_2018/${ifile} ./${ifile}

python prepareModels/makeDatacardsAndWorkspaces.py --config prepareModels/config/LimitsConfig_2018.cfg  --no-comb --signal sig_NMSSM_bbbb_MX_700_MY_400 --bkgNorm 1.040 --folder ${PWD}


toys=2; iter=1; seed=12345; combine -M HybridNew datacard2018_selectionbJets_SignalRegion.root --LHCmode LHC-significance  --saveToys --fullBToys --saveHybridResult -T ${toys} -i ${iter} -s ${seed}
combine -M HybridNew datacard.txt --LHCmode LHC-significance --readHybridResult --grid=input.root [--pvalue ]
combine -M HybridNew datacard2018_selectionbJets_SignalRegion.root --LHCmode LHC-significance --readHybridResult --grid=higgsCombineTest.HybridNew.mH120.123456.root

combine -M Significance datacard2018_selectionbJets_SignalRegion.root

# 2024 Jan 29

run limits for pseudo datasets to cross check local excesses
creation of psuedo datasets in bbbbAnalysis directory, vim session createPseudoDatatset.vim


## change config files and input sample list to one sig for each command:

copy 700,400:
year=2016; mkdir VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx700_my400_2; cp VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2023Dec7_binMYx2_addMX650_10ev_SR/outPlotter_massGroup1.root VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx700_my400_2
year=2017; mkdir VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx700_my400_2;cp VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2023Dec7_binMYx2_addMX650_10ev_SR/outPlotter_massGroup1.root VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx700_my400_2
year=2018;mkdir VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx700_my400_2; cp VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2023Dec7_binMYx2_addMX650_10ev_SR/outPlotter_massGroup1.root VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx700_my400_2

rm data hist 700,400:
year=2016; rootrm VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx700_my400_2/outPlotter_massGroup1.root:data_BTagCSV/selectionbJets_SignalRegion/data_BTagCSV_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled
year=2017; rootrm VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx700_my400_2/outPlotter_massGroup1.root:data_BTagCSV/selectionbJets_SignalRegion/data_BTagCSV_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled
year=2018; rootrm VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx700_my400_2/outPlotter_massGroup1.root:data_BTagCSV/selectionbJets_SignalRegion/data_BTagCSV_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled

copy 650,350:
year=2016; mkdir VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx650_my350_2;cp VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2023Dec7_binMYx2_addMX650_10ev_SR/outPlotter_massGroup1.root VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx650_my350_2
year=2017; mkdir VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx650_my350_2;cp VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2023Dec7_binMYx2_addMX650_10ev_SR/outPlotter_massGroup1.root VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx650_my350_2
year=2018; mkdir VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx650_my350_2;cp VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2023Dec7_binMYx2_addMX650_10ev_SR/outPlotter_massGroup1.root VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx650_my350_2

rm data hist 650,350:
year=2016; rootrm VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx650_my350_2/outPlotter_massGroup1.root:data_BTagCSV/selectionbJets_SignalRegion/data_BTagCSV_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled
year=2017; rootrm VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx650_my350_2/outPlotter_massGroup1.root:data_BTagCSV/selectionbJets_SignalRegion/data_BTagCSV_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled
year=2018; rootrm VarPlots/rootHists/fullSubmission_2022Nov/${year}DataPlots_2024Jan26_psuedoData_checkExcessLimits_mx650_my350_2/outPlotter_massGroup1.root:data_BTagCSV/selectionbJets_SignalRegion/data_BTagCSV_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled

memory limit for condor jobs set to 1024M

sig_tag="mx700_my400_sigX100"; tag="2024Jan26_psuedoData_checkExcessLimits_${sig_tag}_unblind"; region="SR"; python prepareModels/SubmitFullRunIILimits.py --tag ${tag}_${region} --year RunII --group auto --impacts --unblind
sig_tag="mx650_my350_sigX100"; tag="2024Jan26_psuedoData_checkExcessLimits_${sig_tag}_unblind"; region="SR"; python prepareModels/SubmitFullRunIILimits.py --tag ${tag}_${region} --year RunII --group auto --impacts --unblind


tag="2023Dec7_binMYx2_addMX650_10ev_unblind_repeat"; region="SR"; python prepareModels/SubmitFullRunIILimits.py --tag ${tag}_${region} --year RunII --group auto --impacts --unblind

sig_tag="mx700_my400_2"; tag="2024Jan26_psuedoData_checkExcessLimits_${sig_tag}_unblind"; region="SR"; python prepareModels/SubmitFullRunIILimits.py --tag ${tag}_${region} --year RunII --group auto --impacts --unblind

sig_tag="mx700_my400_2"; tag="2024Jan26_psuedoData_checkExcessLimits_${sig_tag}_unblind_sigX10"; region="SR"; python prepareModels/SubmitFullRunIILimits.py --tag ${tag}_${region} --year RunII --group auto --impacts --unblind

sig_tag="mx650_my350_2"; tag="2024Jan26_psuedoData_checkExcessLimits_${sig_tag}_unblind_sigX10"; region="SR"; python prepareModels/SubmitFullRunIILimits.py --tag ${tag}_${region} --year RunII --group auto --impacts --unblind

# 2024 Sep 24:

rerun significance for largest deficit (400,250)
removed --pval option in combine commands: in prepareModels/SubmitFullRunIIsignificance.py
also run the largest excess - to make sure the same limit is produced

tag="2023Dec7_binMYx2_addMX650_10ev_unblind_signif_mX400mY250"; region="SR"; python3 prepareModels/SubmitFullRunIIsignificance.py --tag ${tag}_${region} --year RunII --group auto --unblind
tag="2023Dec7_binMYx2_addMX650_10ev_unblind_signif_mX400mY250"; region="SR"; python3 scripts/getTaskStatus.py --dir CondorJobs/Significance/jobsSignificance_${tag}_${region}/ --long

other changes for this run:

changed to cmssw 10_2_13 (instead of picking up the environment version)
and scram slc7_amd64_gcc700
(still using old style of compiling cmssw in this script, unfortunately.)

moved back to non- full plane directory in all three config files
/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/2018DataPlots_2023Dec7_binMYx2_addMX650_10ev_SR

submitted from b2el9 (no image) but used t3el7submit file to condor
moved print statements to be python3 style
changed package names:

line 160-161
from:
from  ConfigParser import *
to:
from StringIO import StringIO
from:
from  configparser import *
to:
from io import StringIO
from:
cfgparser.readfp(StringIO(signalConfiguration))
to:
cfgparser.read_file(StringIO(signalConfiguration))

updated print statements int he task status script

# 2024 Sep 25


followup on yesterday. adding options to combine command and repeat significance runs for largest excess and largest deficit
in: prepareModels/SubmitFullRunIIsignificance.py
to allow significance values to be negative
--uncapped 1 --rMin=-20


tag="2023Dec7_binMYx2_addMX650_10ev_unblind_signif_mX400mY250_AllowNeg"; region="SR"; python3 prepareModels/SubmitFullRunIIsignificance.py --tag ${tag}_${region} --year RunII --group auto --unblind
tag="2023Dec7_binMYx2_addMX650_10ev_unblind_signif_mX400mY250_AllowNeg"; region="SR"; python3 scripts/getTaskStatus.py --dir CondorJobs/Significance/jobsSignificance_${tag}_${region}/ --long


to check the values used
limit->Scan() in these files:


root -l root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Dec7_binMYx2_addMX650_10ev_unblind_signif_all_SR/HistogramFiles_RunII/Limit_RunII_sig_NMSSM_bbbb_MX_400_MY_250_syst.root
root -l root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Dec7_binMYx2_addMX650_10ev_unblind_signif_mX400mY250_SR/HistogramFiles_RunII/Limit_RunII_sig_NMSSM_bbbb_MX_400_MY_250_syst.root

root -l root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Dec7_binMYx2_addMX650_10ev_unblind_signif_all_SR/HistogramFiles_RunII/Limit_RunII_sig_NMSSM_bbbb_MX_700_MY_400_syst.root
root -l root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Dec7_binMYx2_addMX650_10ev_unblind_signif_mX400mY250_SR/HistogramFiles_RunII/Limit_RunII_sig_NMSSM_bbbb_MX_700_MY_400_syst.root


root -l root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Dec7_binMYx2_addMX650_10ev_unblind_signif_mX400mY250_AllowNeg_SR/HistogramFiles_RunII/Limit_RunII_sig_NMSSM_bbbb_MX_400_MY_250_syst.root
root -l root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Dec7_binMYx2_addMX650_10ev_unblind_signif_mX400mY250_AllowNeg_SR/HistogramFiles_RunII/Limit_RunII_sig_NMSSM_bbbb_MX_700_MY_400_syst.root



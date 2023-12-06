# Notes for limits

- need to edit
(1) `directory` in the LimitConfig (`folder` does not matter)
(2) sample list to run all mass points,
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


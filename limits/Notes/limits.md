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


# To Check jobs:
python scripts/getTaskStatus.py --dir CondorJobs/jobsLimits_2023Feb28/ --long

These are still running:
- sig_NMSSM_bbbb_MX_1600_MY_90
- sig_NMSSM_bbbb_MX_1600_MY_100
- sig_NMSSM_bbbb_MX_1600_MY_125
- sig_NMSSM_bbbb_MX_1600_MY_300


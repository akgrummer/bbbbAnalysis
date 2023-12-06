#!/bin/bash

# [cmslpc117 Dec06 10:49:51 bbbbAnalysis]$ grep -irl -e "Server responded with an error" -e "matrix is singular" -e "zombie" CondorJobs/skimming/
# grep -irl -e "Server responded with an error" -e "matrix is singular" -e "zombie" CondorJobs/skimming/
resubJobs=(CondorJobs/skimming/jobs_moreSignals_mX650_mY70_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-70_2016/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY100_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-100_2016/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY190_2016_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-190_2016/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY190_2016_Total_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-190_2016/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY190_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-190_2016/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY250_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-250_2016/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY300_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-300_2016/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY350_2016_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-350_2016/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY350_2016_Total_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-350_2016/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY350_2016_jer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-350_2016/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY350_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-350_2016/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY350_2016_bjer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-350_2016/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2016_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2016/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2016_bjer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2016/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY500_2016_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-500_2016/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY500_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-500_2016/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY60_2017_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-60_2017/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY100_2017_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-100_2017/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY100_2017_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-100_2017/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY100_2017_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-100_2017/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY100_2017_jer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-100_2017/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY100_2017_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-100_2017/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY100_2017_bjer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-100_2017/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2017/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2017/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2017_jer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2017/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2017_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2017/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY190_2017_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-190_2017/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY190_2017_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-190_2017/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY190_2017_bjer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-190_2017/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY60_2018/SKIM_NMSSM_XToYHTo4B_MX-650_MY-60_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY60_2018/SKIM_NMSSM_XToYHTo4B_MX-650_MY-60_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY60_2018_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-60_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY60_2018_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-60_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY60_2018_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-60_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY80_2018/SKIM_NMSSM_XToYHTo4B_MX-650_MY-80_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY80_2018_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-80_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY80_2018_bjer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-80_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018_Total_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018_jer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018_bjer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY150_2018/SKIM_NMSSM_XToYHTo4B_MX-650_MY-150_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY150_2018_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-150_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY150_2018_jer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-150_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY150_2018_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-150_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY350_2018_Total_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-350_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY350_2018_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-350_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY350_2018_jer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-350_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY350_2018_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-350_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_Total_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_jer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_bjer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
)

# grep -irl -e "Server responded with an error" -e "matrix is singular" -e "zombie" CondorJobs/skimming/
resubJobs2=( CondorJobs/skimming/jobs_moreSignals_mX650_mY70_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-70_2016/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY100_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-100_2016/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY190_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-190_2016/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY250_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-250_2016/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY300_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-300_2016/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY350_2016_jer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-350_2016/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY500_2016_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-500_2016/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY60_2017_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-60_2017/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY100_2017_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-100_2017/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY60_2018/SKIM_NMSSM_XToYHTo4B_MX-650_MY-60_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY60_2018_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-60_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY80_2018/SKIM_NMSSM_XToYHTo4B_MX-650_MY-80_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY80_2018_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-80_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018_bjer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY150_2018/SKIM_NMSSM_XToYHTo4B_MX-650_MY-150_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY150_2018_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-150_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY350_2018_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-350_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_Total_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_jer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_bjer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
)

# grep -irl -e "Server responded with an error" -e "zombie" CondorJobs/skimming/
resubJobs3=( CondorJobs/skimming/jobs_moreSignals_mX650_mY60_2018_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-60_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018_bjer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY150_2018/SKIM_NMSSM_XToYHTo4B_MX-650_MY-150_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY350_2018_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-350_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_Total_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_Total_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_jer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
)

# grep -irl -e "Server responded with an error" -e "zombie" CondorJobs/skimming/
resubJobs4=( CondorJobs/skimming/jobs_moreSignals_mX650_mY60_2018_bjer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-60_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY125_2018_bjer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-125_2018/job_0.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_Total_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_jer_up/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_jer_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh \
)

# grep -irl -e "Server responded with an error" -e "zombie" CondorJobs/skimming/
resubJobs5=( CondorJobs/skimming/jobs_moreSignals_mX650_mY450_2018_Total_down/SKIM_NMSSM_XToYHTo4B_MX-650_MY-450_2018/job_1.sh )

echo "Number of jobs: " "${#resubJobs5[@]}"
# ls "${resubJobs[1]}"
# for var in "${resubJobs[@]}" ; do
### BACKUP OLD JOBS (update file name in all 4 lines..:/ )
for var in "${resubJobs5[@]}" ; do
    printf "%s\n" "${var}"
    thedir=$(dirname "${var}")
    mkdir -p badMoreSignalJobs5/${thedir}/
    mv "${var}"_*.log badMoreSignalJobs5/${thedir}/
    mv "${var}"_*.stderr badMoreSignalJobs5/${thedir}/
    mv "${var}"_*.stdout badMoreSignalJobs5/${thedir}/
done

for var in "${resubJobs5[@]}" ; do
    printf "%s\n" "${var}"
    ./scripts/t3submit "${var}"
done


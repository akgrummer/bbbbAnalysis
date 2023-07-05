TAG="2023Feb28_hourglass_VR_ws"

TAGIDS=(1 2 3 4 5)
for YEAR in 2016 2017 2018; do
    for TAGID in ${TAGIDS[@]}; do
        python scripts/getTaskStatus.py --dir CondorJobs/jobsLimits_${TAG}_${YEAR}_${TAGID}/ --long
    done;
done

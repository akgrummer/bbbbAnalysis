#!/bin/bash


# tags=("2024Jun21_vars_mY90_mX340")
# tags+=("2024Jun21_vars_mY90_mX488")
# tags+=("2024Jun21_vars_mY90_mX488")
# tags+=("2024Jun21_vars_mY90_mX648")
# tags+=("2024Jun21_vars_mY90_mX960")
# tags+=("2024Jun21_vars_mY90_mX340to1216")
# tags+=("2024Jun21_vars_mY90_mX340_3b")
# tags+=("2024Jun21_vars_mY90_mX488_3b")
# tags+=("2024Jun21_vars_mY90_mX648_3b")
# tags+=("2024Jun21_vars_mY90_mX960_3b")
# tags+=("2024Jun21_vars_mY90_mX340to1216_3b")

# tags=("2024Jun27_vars_Zjets")
# tags+=("2024Jun27_vars_Zjets_3b")
# tags+=("2024Jun27_vars_Zjets_mY90pm10")
# tags+=("2024Jun27_vars_Zjets_mY90pm10_3b")
# tags+=("2024Jun27_vars_mY90_Zjets_mX340")
# tags+=("2024Jun27_vars_mY90_Zjets_mX488")
# tags+=("2024Jun27_vars_mY90_Zjets_mX648")
# tags+=("2024Jun27_vars_mY90_Zjets_mX960")
# tags+=("2024Jun27_vars_mY90_Zjets_mX340to1216")
# tags+=("2024Jun27_vars_mY90_Zjets_mX340_3b")
# tags+=("2024Jun27_vars_mY90_Zjets_mX488_3b")
# tags+=("2024Jun27_vars_mY90_Zjets_mX648_3b")
# tags+=("2024Jun27_vars_mY90_Zjets_mX960_3b")
# tags+=("2024Jun27_vars_mY90_Zjets_mX340to1216_3b")
#

tags=("2024Jun30_vars_Zjets")
tags+=("2024Jun30_vars_Zjets_3b")
tags+=("2024Jun30_vars_Zjets_mY90pm10")
tags+=("2024Jun30_vars_Zjets_mY90pm10_3b")
tags+=("2024Jun30_vars_mY90_Zjets_mX340")
tags+=("2024Jun30_vars_mY90_Zjets_mX488")
tags+=("2024Jun30_vars_mY90_Zjets_mX648")
tags+=("2024Jun30_vars_mY90_Zjets_mX960")
tags+=("2024Jun30_vars_mY90_Zjets_mX340to1216")
tags+=("2024Jun30_vars_mY90_Zjets_mX340_3b")
tags+=("2024Jun30_vars_mY90_Zjets_mX488_3b")
tags+=("2024Jun30_vars_mY90_Zjets_mX648_3b")
tags+=("2024Jun30_vars_mY90_Zjets_mX960_3b")
tags+=("2024Jun30_vars_mY90_Zjets_mX340to1216_3b")
years=("2016")
years+=("2016preVFP")
years+=("2017")
years+=("2018")

# echo "${tags[@]}"
#
# for tag in "${tags[@]}"; do
#     echo ${tag};
#     for year in  "${years[@]}"; do
#         echo ${year};
#         echo "python scripts/getTaskStatus.py --dir CondorJobs/jobsFill_fullSubmission_${year}_BDTweights_${tag}/ --long";
#         python scripts/getTaskStatus.py --dir CondorJobs/jobsFill_fullSubmission_${year}_BDTweights_${tag}/ --long;
#     done
# done

for tag in "${tags[@]}"; do
    echo ${tag};
    source ./scripts/mergeHistograms.sh ${tag}
done

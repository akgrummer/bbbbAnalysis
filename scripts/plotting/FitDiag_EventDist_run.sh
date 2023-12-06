for year in 2016 2017 2018; do
    for monitor in "lt1" "lt5" "lt10" "mean"; do
        python ~/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/plotting/FitDiag_EventDist_compare3.py --year ${year} --monitor ${monitor}
    done;
done

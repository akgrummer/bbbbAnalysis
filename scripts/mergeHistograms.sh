# for arc chair question -
# tag=2023Feb22_Mxgt800 # check the mx and my relationship by cutting on mx at 800 and making two sets of plots
# tag=2023Feb22_Mxlt800 # check the mx and my relationship by cutting on mx at 800 and making two sets of plots
# tag=2023Feb22_Mygt140lt190 # check the mx and my relationship by cutting on mx at 800 and making two sets of plots
# tag=2023Feb27_TrigCut_5 # check how many events pass cut at trig threshold
# tag=2023Feb28_3 # Full Submission with pt and ht cuts that match the HLT trigger thresholds, the _3 is to include the Higgs variables in the output (I should not have removed them)
tag=$1 # Full Submission with pt and ht cuts that match the HLT trigger thresholds, the _3 is to include the Higgs variables in the output (I should not have removed them)

# python ./scripts/mergeHistograms.py --tag fullSubmission_2016_BDTweights_${tag}
# python ./scripts/mergeHistograms.py --tag fullSubmission_2017_BDTweights_${tag}
# python ./scripts/mergeHistograms.py --tag fullSubmission_2018_BDTweights_${tag}
# source ./scripts/renameFullSubmissions.sh ${tag}

python ./scripts/mergeHistograms.py --tag varSubmission_2016_BDTweights_${tag}
python ./scripts/mergeHistograms.py --tag varSubmission_2017_BDTweights_${tag}
python ./scripts/mergeHistograms.py --tag varSubmission_2018_BDTweights_${tag}
source ./scripts/renameFullSubmissions.sh ${tag}


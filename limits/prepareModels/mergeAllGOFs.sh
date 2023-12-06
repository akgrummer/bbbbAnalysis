# TAG="2023Feb28_hourglass_VR_ws"
# TAG="2023Feb28_VR"
# TAG="2023Feb28_trim_VR"
# TAG="2023Feb28_trim"
# TAG="2023Feb28_hourglass_unc"
# TAG="2023Jul5_VR"
# TAG="2023Jul5_SR"
# TAG="2023Jul5_doubleMCStats_VR"
# TAG="2023Jul5_1p5MCStats_VR"
# TAG="2023Jul5_newMinimizer_VR"
# TAG="2023Jul5_newMinimizer_SR"
# TAG="2023Jul5_binMYx2_VR" #
# TAG="2023Jul5_binMYx2_SR" #
# TAG="2023Jul5_nonClosureMCStats2_VR" #
# TAG="2023Jul5_nonClosureMCStats2_SR" #
# TAG="2023Jul5_binMYx2_ncMCStats_VR" #
# TAG="2023Jul5_binMYx2_ncMCStats_lowStatsCut_5ev_SR"
TAG="2023Jul5_binMYx2_ncMCStats_lowStatsCut_10ev_SR"
# TAG="2023Jul5_binMYx2_ncMCStats_SR" #
# TAG="2023Jul5_VR"
# TAG="2023Jul5_binX4_SR"
# TAG="2023Jul5_binX4_VR"
# YEAR=2016
# SAMPLES="prepareModels/listOfSamples.txt"
SAMPLES="prepareModels/listOfSamples_10points.txt"
ALGO="saturated"

# if back here - need to rerun 2023Jul5_VR to produde the csv file from plotGOF_aidan (after fix for excluding sig0 - tested on sublist sample
# for YEAR in 2016 2017 2018; do
#     python prepareModels/mergeGOFs.py --tag ${TAG} --year ${YEAR} --algo ${ALGO} --samplelist ${SAMPLES}
# done
# for YEAR in 2016 2017 2018; do
#     python an-scripts/plotGOF_aidan.py --tag ${TAG} --year ${YEAR} --algo ${ALGO} --samplelist ${SAMPLES}
# done
# for YEAR in 2016 2017 2018; do
#     python scripts/plotting/GOF_2d_plots.py --tag ${TAG} --year ${YEAR} --algo ${ALGO}
#     python scripts/plotting/GOF_2d_plots.py --tag ${TAG} --year ${YEAR} --algo ${ALGO} --zoom "zoom"
#     python scripts/plotting/GOF_2d_plots.py --tag ${TAG} --year ${YEAR} --algo ${ALGO} --zoom "zoom2"
# done

## FOR BACKGROUND ONLY FITS (BELOW HERE) SIG==0
# for YEAR in 2016 2017 2018; do
#   python prepareModels/mergeGOFs_sig0.py --tag ${TAG} --year ${YEAR} --algo ${ALGO} --samplelist ${SAMPLES}
# done
# for YEAR in 2016 2017 2018; do
#   python an-scripts/plotGOF_aidan_sig0.py --tag ${TAG} --year ${YEAR} --algo ${ALGO} --samplelist ${SAMPLES}
# done
# for YEAR in 2016 2017 2018; do
#     python scripts/plotting/GOF_1d_sig0.py --tag ${TAG} --year ${YEAR} --algo ${ALGO}
# done
#
# TAG1="2023Jul5_VR"
# TAG1="2023Jul5_SR"
# TAG2="2023Jul5_binX4_VR"
# TAG2="2023Jul5_doubleMCStats_VR"
# TAG2="2023Jul5_1p5MCStats_VR"
# TAG2="2023Jul5_newMinimizer_VR"
# TAG2="2023Jul5_newMinimizer_SR"
# TAG2="2023Jul5_newMinimizer_SR"
# TAG2="2023Jul5_nonClosureMCStats_VR" #
# TAG2="2023Jul5_nonClosureMCStats_SR" #
# TAG2="2023Jul5_binMYx2_VR" #
# TAG2="2023Jul5_binMYx2_SR" #
# TAG2=${TAG}
# TAG2="2023Jul5_nonClosureMCStats2_VR" #
# TAG2="2023Jul5_nonClosureMCStats2_SR" #
# for YEAR in 2016 2017 2018; do
    # python scripts/plotting/GOF_1d_sig0_compare.py --tag ${TAG1} --tag2 ${TAG2} --year ${YEAR} --algo ${ALGO}
# done

# TAG1="2023Jul5_VR"
# TAG2="2023Jul5_nonClosureMCStats2_VR" #
# TAG3="2023Jul5_binMYx2_ncMCStats_VR" #
# TAG1="2023Jul5_SR"
# TAG2="2023Jul5_nonClosureMCStats2_SR" #
# TAG3="2023Jul5_binMYx2_ncMCStats_SR" #
TAG1="2023Jul5_nonClosureMCStats2_SR" #
TAG2="2023Jul5_binMYx2_ncMCStats_SR" #
# TAG3="2023Jul5_binMYx2_ncMCStats_lowStatsCut_5ev_SR"
TAG3="2023Jul5_binMYx2_ncMCStats_lowStatsCut_10ev_SR"
for YEAR in 2016 2017 2018; do
    python scripts/plotting/GOF_1d_sig0_compare3.py --tag ${TAG1} --tag2 ${TAG2} --tag3 ${TAG3} --year ${YEAR} --algo ${ALGO}
done

# TAG1="2023Jul5_SR"
# # TAG2="2023Jul5_binX4_SR"
# for YEAR in 2016 2017 2018; do
#     python scripts/plotting/GOF_1d_sig0_compare.py --tag ${TAG1} --tag2 ${TAG2} --year ${YEAR} --algo ${ALGO}
# done

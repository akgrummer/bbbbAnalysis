# TAG="2023Feb28_hourglass_VR_ws"
# TAG="2023Feb28_VR"
# TAG="2023Feb28_trim_VR"
# TAG="2023Feb28_trim"
TAG="2023Feb28_hourglass_unc"
YEAR=2016
SAMPLES="prepareModels/listOfSamples.txt"
ALGO="saturated"

for YEAR in 2016 2017 2018; do
    python prepareModels/mergeGOFs.py --tag ${TAG} --year ${YEAR} --algo ${ALGO} --samplelist ${SAMPLES}
done
for YEAR in 2016 2017 2018; do
    python an-scripts/plotGOF_aidan.py --tag ${TAG} --year ${YEAR} --algo ${ALGO} --samplelist ${SAMPLES}
done
for YEAR in 2016 2017 2018; do
    python scripts/plotting/GOF_2d_plots.py --tag ${TAG} --year ${YEAR} --algo ${ALGO}
    python scripts/plotting/GOF_2d_plots.py --tag ${TAG} --year ${YEAR} --algo ${ALGO} --zoom "zoom"
    python scripts/plotting/GOF_2d_plots.py --tag ${TAG} --year ${YEAR} --algo ${ALGO} --zoom "zoom2"
done


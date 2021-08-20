TAG="fullSubmission_v46"

for i in {0..4}; do
    python prepareModels/SubmitFullRunIILimits.py --tag $TAG --year RunII --group $i;
done

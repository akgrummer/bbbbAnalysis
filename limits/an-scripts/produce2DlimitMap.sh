# TAG="2023Dec7_binMYx2_addMX650_10ev_unblind_SR"
TAG="2023Dec7_binMYx2_addMX650_10ev_unblind_signif_all_SR"
# g++  -std=c++17 -I `root-config --incdir`  -o an-scripts/PlotSignificanceFromCondor an-scripts/PlotSignificanceFromCondor.cc `root-config --libs` -O3
g++  -std=c++17 -I `root-config --incdir`  -o an-scripts/Plot2DSignificanceMap       an-scripts/Plot2DSignificanceMap.C        `root-config --libs` -O3
#
# # makes the base plots in a root file (used just the impact version):
# ./an-scripts/PlotSignificanceFromCondor $TAG
#
# # makes: CentralLimitMap_RunII_TheoryComparison.png
./an-scripts/Plot2DSignificanceMap ${TAG}


# ran hadd over the significance files in eos - lost the command in history though
# years=( "RunII" "2016" "2017" "2018" )
# for ayear in "${years[@]}"; do
#     python an-scripts/PlotSignficanceDist.py --tag ${TAG} --year ${ayear}
# done


#!/bin/bash

atag="2023Dec7_binMYx2_addMX650_10ev_unblind_SR"

option=""

years=( "2016" "2017" "2018" "RunII" )
for ayear in "${years[@]}"; do
    python an-scripts/PlotLimitMean.py --tag ${atag} --year ${ayear} --systematics
    python an-scripts/PlotLimitMean.py --tag ${atag} --year ${ayear} --systematics --use2sig
done
ayear="RunII"
python an-scripts/PlotLimitMean.py --tag ${atag} --year ${ayear} --systematics --listX
python an-scripts/PlotLimitMean.py --tag ${atag} --year ${ayear} --systematics --listX --use2sig

# option="_freezeBKGnorm"
# option="_statOnly"
# python PlotLimitMean.py --input LimitPlots_${atag}${option}/Limits_${atag}.root --year 2016 --systematics
# python PlotLimitMean.py --input LimitPlots_${atag}${option}/Limits_${atag}.root --year 2017 --systematics
# python PlotLimitMean.py --input LimitPlots_${atag}${option}/Limits_${atag}.root --year 2018 --systematics
# python PlotLimitMean.py --input LimitPlots_${atag}${option}/Limits_${atag}.root --year RunII --systematics

# python PlotLimitMean.py --input LimitPlots_${atag}${option}/Limits_${atag}.root --year 2016 --freezeBKGnorm
# python PlotLimitMean.py --input LimitPlots_${atag}${option}/Limits_${atag}.root --year 2017 --freezeBKGnorm
# python PlotLimitMean.py --input LimitPlots_${atag}${option}/Limits_${atag}.root --year 2018 --freezeBKGnorm
# python PlotLimitMean.py --input LimitPlots_${atag}${option}/Limits_${atag}.root --year RunII --freezeBKGnorm

# python PlotLimitMean.py --input LimitPlots_${atag}${option}/Limits_${atag}.root --year 2016
# python PlotLimitMean.py --input LimitPlots_${atag}${option}/Limits_${atag}.root --year 2017
# python PlotLimitMean.py --input LimitPlots_${atag}${option}/Limits_${atag}.root --year 2018
# python PlotLimitMean.py --input LimitPlots_${atag}${option}/Limits_${atag}.root --year RunII


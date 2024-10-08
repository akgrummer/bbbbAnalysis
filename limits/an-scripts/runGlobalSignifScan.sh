# ./an-scripts/LEE_getMinSigma.cc
# ./an-scripts/LEE_getMaxSigma.cc
# g++  -std=c++17 -I `root-config --incdir`  -o an-scripts/exe/LEE_getMinSigma an-scripts/LEE_getMinSigma.cc `root-config --libs` -O3
# g++  -std=c++17 -I `root-config --incdir`  -o an-scripts/exe/LEE_getMaxSigma an-scripts/LEE_getMaxSigma.cc `root-config --libs` -O3

# signFile="lee_sign_all_neg.root"
signFile="lee_sign_all_2024Oct7_noFreq.root"
oDir="studies/LEE/2024Oct7_noFreq/"

mkdir -p ${oDir}

if [ ${2} = "min" ]; then
    echo ${1}_1_2k_min.txt

    ./an-scripts/exe/LEE_getMinSigma ${signFile} 1 2001 >> ${oDir}${1}_1_2k_min.txt &
    ./an-scripts/exe/LEE_getMinSigma ${signFile} 2001 4001 >> ${oDir}${1}_2k_4k_min.txt &
    ./an-scripts/exe/LEE_getMinSigma ${signFile} 4001 6001 >> ${oDir}${1}_4k_6k_min.txt &
    ./an-scripts/exe/LEE_getMinSigma ${signFile} 6001 8001 >> ${oDir}${1}_6k_8k_min.txt &
    ./an-scripts/exe/LEE_getMinSigma ${signFile} 8001 10001 >> ${oDir}${1}_8k_10k_min.txt &
elif [ ${2} = "max" ]; then
    echo ${1}_1_2k_max.txt

    ./an-scripts/exe/LEE_getMaxSigma ${signFile} 1 2001 >> ${oDir}${1}_1_2k_max.txt &
    ./an-scripts/exe/LEE_getMaxSigma ${signFile} 2001 4001 >> ${oDir}${1}_2k_4k_max.txt &
    ./an-scripts/exe/LEE_getMaxSigma ${signFile} 4001 6001 >> ${oDir}${1}_4k_6k_max.txt &
    ./an-scripts/exe/LEE_getMaxSigma ${signFile} 6001 8001 >> ${oDir}${1}_6k_8k_max.txt &
    ./an-scripts/exe/LEE_getMaxSigma ${signFile} 8001 10001 >> ${oDir}${1}_8k_10k_max.txt &
fi




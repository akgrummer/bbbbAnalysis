yearList=(
    2016
    2017
    2018
)


for year in "${yearList[@]}"; do
    python prepareModels/runFullSelfBiasTest.py --config prepareModels/config/SelfBiasTest_${year}.cfg --signal sig_NMSSM_bbbb_MX_300_MY_125   --injRange 5
    python prepareModels/runFullSelfBiasTest.py --config prepareModels/config/SelfBiasTest_${year}.cfg --signal sig_NMSSM_bbbb_MX_400_MY_80    --injRange 2 
    python prepareModels/runFullSelfBiasTest.py --config prepareModels/config/SelfBiasTest_${year}.cfg --signal sig_NMSSM_bbbb_MX_600_MY_125   --injRange 3
    python prepareModels/runFullSelfBiasTest.py --config prepareModels/config/SelfBiasTest_${year}.cfg --signal sig_NMSSM_bbbb_MX_700_MY_300   --injRange 4
    python prepareModels/runFullSelfBiasTest.py --config prepareModels/config/SelfBiasTest_${year}.cfg --signal sig_NMSSM_bbbb_MX_900_MY_500   --injRange 3
    python prepareModels/runFullSelfBiasTest.py --config prepareModels/config/SelfBiasTest_${year}.cfg --signal sig_NMSSM_bbbb_MX_1000_MY_125  --injRange 1
    python prepareModels/runFullSelfBiasTest.py --config prepareModels/config/SelfBiasTest_${year}.cfg --signal sig_NMSSM_bbbb_MX_1200_MY_800  --injRange 2 
    python prepareModels/runFullSelfBiasTest.py --config prepareModels/config/SelfBiasTest_${year}.cfg --signal sig_NMSSM_bbbb_MX_1400_MY_500  --injRange 1
    python prepareModels/runFullSelfBiasTest.py --config prepareModels/config/SelfBiasTest_${year}.cfg --signal sig_NMSSM_bbbb_MX_1600_MY_300  --injRange 6
    python prepareModels/runFullSelfBiasTest.py --config prepareModels/config/SelfBiasTest_${year}.cfg --signal sig_NMSSM_bbbb_MX_1600_MY_1000 --injRange 6
    python prepareModels/runFullSelfBiasTest.py --config prepareModels/config/SelfBiasTest_${year}.cfg --signal sig_NMSSM_bbbb_MX_1800_MY_600  --injRange 6
    python prepareModels/runFullSelfBiasTest.py --config prepareModels/config/SelfBiasTest_${year}.cfg --signal sig_NMSSM_bbbb_MX_1800_MY_1400 --injRange 6
done

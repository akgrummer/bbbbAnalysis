t3submit=/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/t3submit
tar -zcf  bbbbAnalysis.tar.gz mlskim_NMSSM_XYH_bbbb/ bin/ lib/ config/ data/ weights/ 
xrdcp -f -s bbbbAnalysis.tar.gz root://cmseos.fnal.gov//store/user/agrummer/bbbb_BDT/
rm bbbbAnalysis.tar.gz 
t3submit BDTgridSubmit/trialGridSubmit_2022Apr14.sh 2020 2017

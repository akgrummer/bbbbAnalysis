cd to the folder to tar, then:
tar --exclude='./src/bbbbAnalysis' --exclude='./src/AN-20-080' -zcvf ../cmssw10_2_5.tar.gz .
- needed once: eosmkdir /store/user/agrummer/cmssw_builds
xrdcp -f -s  cmssw10_2_5.tar.gz root://cmseos.fnal.gov//store/user/agrummer/cmssw_builds/cmssw10_2_5.tar.gz

# Notes for running the global significance study

## Toy generation

from ./prepareModels/SubmitGoF.py script:
```python
" --fixedSignalStrength={0}".format(args.fixsig)
```

from ./prepareModels/make_biastest.sh
```bash
combine -M GenerateOnly -t ${NTOYS} \
 --dataset data_obs --rMin $RLIMITMIN --rMax $RLIMITMAX --setParameters r=${SIGSTRENGTH},myscale=0 \
 --saveToys -n _inj_${SIGSTRENGTH}_toys \
 --freezeParameters r,myscale \
 ${DATACARD}
 ```

 ```bash
combine -M GenerateOnly -t ${NTOYS} \
 --dataset data_obs --rMin $RLIMITMIN --rMax $RLIMITMAX --setParameters r=${SIGSTRENGTH},myscale=0 \
 --saveToys -n _inj_${SIGSTRENGTH}_toys \
 --freezeParameters r,myscale \
 ${DATACARD}
 ```

```python
 writeln(outScript, 'combine %s -M AsymptoticLimits --rMax 30 %s --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH %s' % (workspaceName,blindFlag,theRealCombineCommand))
```
workspace name is the root file created from the datacard.
don't need blind flag for this toy generation
read combine command is for running impact of freezeParameters for different nuisance parameters


```bash
ntoys=1
workspaceName=
combine ${workspaceName} -M GenerateOnly -t ${ntoys} -m 125.0 --rMin 0 --rMax 0\
    --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH
    --setParameters r=0\
    --freezeParameters r\
    --saveToys -n _ntoys_${ntoys} \
```

## Plan

- unroll full plane (each year)
- throw background only toys (100) for full plane
    - this requires a normalization uncertainty on the full plane
    - need to make workspace (one per year) for full plane
    - making the workspaces - needs dedicated scripts.
- reroll toys for full plane
- split and unroll into mass groups
- copy them in to the original mass group root files as 'fake data' replacing the data
- for each toy do a likelihood scan (over original mass points)
    - if needed interpolate more signals and fill in the likelihood scan.
    - do combination of 3 years as normal (toy to toy?)
- compute Euler characteristic equation using the likelihood scans
- compute N1,N2 and global significance of the two excesses.


## April 1

prepareModels/SubmitWorkspaces_fullPlane.py
also had to add an option to prepareHistos.py for group='all'


## Apr 2

### !!!!In order to Run Workspaces on the grid:!!!!
1. Need to have limits config up to date.
2. Need to have the prepareModels/listOfSamples.txt ready
3. Need to used the correct tag in the prepareModels/SubmitAllWorkspaces_fullPlane.sh
- make sure normalization values are correct in both Workspaces submit and GOF submit scripts

scripts:
./prepareModels/SubmitAllWorkspaces_fullPlane.sh
prepareModels/SubmitWorkspaces_fullPlane.py
prepareModels/prepareHistos.py (edited lines 83-84)
prepareModels/listOfSamples_LEE.txt

prepareModels/config/LimitsConfig_2016.cfg
prepareModels/config/LimitsConfig_2017.cfg
prepareModels/config/LimitsConfig_2018.cfg

submited one job with
request_memory = 1024M

ran 152 (main signals)
with 512M

### !!! generate toys

prepareModels/SubmitGenerateToys.py
./prepareModels/SubmitAllGenerateOnly.sh



```bash
ntoys=1
workspaceName=
combine ${workspaceName} -M GenerateOnly -t ${ntoys} -m 125.0 --rMin 0 --rMax 0\
    --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH
    --setParameters r=0\
    --freezeParameters r\
    --saveToys -n _ntoys_${ntoys} \
```

mkdir DatacardFolder_2016
mkdir DatacardFolder_2017
mkdir DatacardFolder_2018
mkdir DatacardFolder_RunII
xrdcp -s -f root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits//2023Dec7_binMYx2_addMX650_10ev_fullPlane_SR/HistogramFiles_2016/datacard_2016_sig_NMSSM_bbbb_MX_650_MY_350.root DatacardFolder_2016/datacard2016_selectionbJets_SignalRegion.root
xrdcp -s -f root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits//2023Dec7_binMYx2_addMX650_10ev_fullPlane_SR/HistogramFiles_2017/datacard_2017_sig_NMSSM_bbbb_MX_650_MY_350.root DatacardFolder_2017/datacard2017_selectionbJets_SignalRegion.root
xrdcp -s -f root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits//2023Dec7_binMYx2_addMX650_10ev_fullPlane_SR/HistogramFiles_2018/datacard_2018_sig_NMSSM_bbbb_MX_650_MY_350.root DatacardFolder_2018/datacard2018_selectionbJets_SignalRegion.root
xrdcp -s -f root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Dec7_binMYx2_addMX650_10ev_fullPlane_SR/HistogramFiles_RunII/datacard_RunII_sig_NMSSM_bbbb_MX_650_MY_350.root DatacardFolder_RunII/datacardRunII_selectionbJets_SignalRegion.root

combine DatacardFolder_2016/datacard2016_selectionbJets_SignalRegion.root -M GenerateOnly --toysFrequentist -m 125 -t 100 --saveToys --expectSignal=0
combine DatacardFolder_RunII/datacardRunII_selectionbJets_SignalRegion.root -M GenerateOnly --toysFrequentist -m 125 -t 100 --saveToys --expectSignal=0

combine DatacardFolder_2016/datacard2016_selectionbJets_SignalRegion.root -M Significance --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH
combine DatacardFolder_2017/datacard2017_selectionbJets_SignalRegion.root -M Significance --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH
combine DatacardFolder_2018/datacard2018_selectionbJets_SignalRegion.root -M Significance --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH
combine DatacardFolder_RunII/datacardRunII_selectionbJets_SignalRegion.root -M Significance --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH

combine DatacardFolder_2016/datacard2016_selectionbJets_SignalRegion.root -M Significance --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH -D higgsCombineTest.GenerateOnly.mH125.123456.root:toys/toy_95



## root files -- add info

scripts/LEE_addInfoToSignifTrees.cc
g++  -std=c++17 -I `root-config --incdir`  -o an-scripts/PlotLimitsFromCondor an-scripts/PlotLimitsFromCondor.cc `root-config --libs` -O3
g++  -std=c++17 -I `root-config --incdir`  -o an-scripts/Plot2DLimitMap       an-scripts/Plot2DLimitMap.C        `root-config --libs` -O3

g++  -std=c++17 -I `root-config --incdir`  -o an-scripts/exe/LEE_addInfoToSignifTree an-scripts/LEE_addInfoToSignifTree.cc `root-config --libs` -O3

combine DatacardFolder_2016/datacard2016_selectionbJets_SignalRegion.root  -n _test_1 -M Significance --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH -D higgsCombineTest.GenerateOnly.mH125.123456.root:toys/toy_100
Usage: ./an-scripts/LEE_addInfoToSignifTree <iofile> <mX> <mY> <toyNum>
./an-scripts/LEE_addInfoToSignifTree higgsCombineTest.Significance.mH120.root 650 350 95
./an-scripts/LEE_addInfoToSignifTree higgsCombineTest2.Significance.mH120.root 650 350 100







./prepareModels/SubmitAllGenerateOnly.sh
trying to test that things work with RunII workspace now...

xrdcp -s -f root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits//2023Dec7_binMYx2_addMX650_10ev_fullPlane_SR/genToysFiles_RunII/GenToys_RunII_ntoys2_id0.root GenToys_RunII_ntoys2_id0.root


combine DatacardFolder_RunII/datacardRunII_selectionbJets_SignalRegion.root  -n _RunII_test_1 -M Significance --X-rtd  MINIMIZER_analytic --X-rtd  FAST_VERTICAL_MORPH -D GenToys_RunII_ntoys2_id0.root:toys/toy_1





prepareModels/SubmitLEEsignificance.py
./prepareModels/SubmitAllLEEsignificance.sh

# Checking the output:

hadd myTarget.root `xrdfsls -u /store/user/username/rootFiles | grep '\.root'`
hadd lee_sign_all.root `xrdfsls -u /store/user/agrummer/bbbb_limits/2023Dec7_binMYx2_addMX650_10ev_fullPlane_SR/LEEsignFiles_RunII | grep '\.root'`
- this took forEVER for all toys (1hr?)


limit->Draw("limit:toyNum", "sim==1&&mX==650", "colz")
limit->Draw("limit", "sim==0")
limit->Draw("mY:mX", "sim==0", "colz")


# April 4:

ran 250 toys x 40 jobs (tagid)
(uses one in put sig file, but the signal strength is set to 0)
required Memory=2048
in /uscms_data/d3/agrummer/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/t3submit
500 toy jobs hit the memory limit of 2048

./prepareModels/SubmitAllGenerateOnly.sh

(uses all analysis signal points - but no interpolation points):
if an-scripts/LEE_addInfoToSignifTree.cc is updated need to recompile with:
g++  -std=c++17 -I `root-config --incdir`  -o an-scripts/exe/LEE_addInfoToSignifTree an-scripts/LEE_addInfoToSignifTree.cc `root-config --libs` -O3
Used memory 512:

./prepareModels/SubmitAllLEEsignificance.sh

to loop over branches:
g++  -std=c++17 -I `root-config --incdir`  -o an-scripts/exe/LEE_getMaxSigma an-scripts/LEE_getMaxSigma.cc `root-config --libs` -O3
an-scripts/LEE_getMaxSigma.cc

in screen:
./an-scripts/exe/LEE_getMaxSigma lee_sign_all.root >> lee_global_sign.txt &

# Error checking:

grep -ir "error" CondorJobs/GenerateOnly | grep -v "Messages of type"
grep -ir "error" CondorJobs/LEEsignificance | grep -v "Messages of type"

[cmslpc105 Apr05 10:14:07 limits]$ grep -ir "error" CondorJobs/LEEsignificance |grep -v "Messages of type"
CondorJobs/LEEsignificance/jobsLimits_2023Dec7_binMYx2_addMX650_10ev_fullPlane_SR_RunII_0/job_sig_NMSSM_bbbb_MX_1200_MY_300.sh_31426491.stdout:tar: Error is not recoverable: exiting now
- Reran this job - no error on the tar the second time and root file looked clean


# rerun limits in the full plane

prepareModels/SubmitFullRunIILimits_fullPlane.py
./prepareModels/SubmitAllLimits_fullPlane.sh


grep -ir "error" CondorJobs/Limits_fullPlane | grep -v "Messages of type"






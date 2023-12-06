edmCopyPickMerge inputFiles=first.root,second.root,third.root outputFile=output.root maxSize=100

edmCopyPickMerge inputFiles=/store/mc/RunIISummer20UL17NanoAODv2/NMSSM_XtoHYto4b_MX_1000_MY_150_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v8-v1/260000/63421650-960B-E34E-98CA-DC6DD0493059.root outputFile=output.root maxSize=100

edmProvDump root://cmsxrootd-site.fnal.gov//store/mc/RunIISummer20UL17NanoAODv2/NMSSM_XtoHYto4b_MX_1000_MY_150_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v8-v1/260000/63421650-960B-E34E-98CA-DC6DD0493059.root > EdmProvDump.txt


# Worked:
rucio list-file-replicas --pfn --rse T2_DE_DESY cms:/store/mc/RunIISummer20UL17NanoAODv2/NMSSM_XtoHYto4b_MX_1000_MY_150_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v8-v1/260000/63421650-960B-E34E-98CA-DC6DD0493059.root

rucio list-file-replicas cms:/store/mc/RunIISummer20UL17NanoAODv2/NMSSM_XtoHYto4b_MX_1000_MY_150_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v8-v1/260000/63421650-960B-E34E-98CA-DC6DD0493059.root

rucio list-file-replicas --pfn --rse T1_US_FNAL_Disk cms:/store/mc/RunIISummer20UL17NanoAODv2/NMSSM_XtoHYto4b_MX_1000_MY_150_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v8-v1/260000/63421650-960B-E34E-98CA-DC6DD0493059.root

rucio list-rses |grep FNAL
T1_US_FNAL_Disk_Test
T1_US_FNAL_Tape_Test
T1_US_FNAL_Disk
T3_US_FNALLPC_Temp
T1_US_FNAL_Disk_Temp
T3_US_FNALLPC_Test
T1_US_FNAL_Tape
T3_US_FNALLPC


#didn't work:
list-datasets-rse
rucio list-file-replicas list-datasets-rse cms:/store/mc/RunIISummer20UL17NanoAODv2/NMSSM_XtoHYto4b_MX_1000_MY_150_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v8-v1/260000/63421650-960B-E34E-98CA-DC6DD0493059.root


rucio download --rse T2_DE_DESY cms:/store/mc/RunIISummer20UL17NanoAODv2/NMSSM_XtoHYto4b_MX_1000_MY_150_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v8-v1/260000/63421650-960B-E34E-98CA-DC6DD0493059.root

rucio download --rse T1_US_FNAL_Disk cms:/store/mc/RunIISummer20UL17NanoAODv2/NMSSM_XtoHYto4b_MX_1000_MY_150_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v8-v1/260000/63421650-960B-E34E-98CA-DC6DD0493059.root



xrdfs root://cmsxrootd.fnal.gov/ ls -l /store/test/xrootd/T1_US_FNAL_Disk/store/mc/RunIISummer20UL17NanoAODv2/NMSSM_XtoHYto4b_MX_1000_MY_150_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v8-v1/260000/63421650-960B-E34E-98CA-DC6DD0493059.root



dasgoclient --query="dataset=/*NMSSM*MX_1000_MY_150" --format=plain
dasgoclient --help
dasgoclient file block=/Cosmics/Run2010B-TkAlCosmics0T-v1/ALCARECO#* site=T1_US_FNAL
dasgoclient -query="dataset=/store/mc/RunIIFall17NanoAODv7/NMSSM_XToYHTo4B_MX-1000_MY-150_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/*/*"


/NMSSM_XToYHTo4B_MX-1000_MY-150_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v2/NANOAODSIM

rucio list-files cms:/store/mc/RunIIFall17NanoAODv7/NMSSM_XToYHTo4B_MX-1000_MY-150_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v2/70000/0EBEC861-7313-8E43-97D8-03A58730BA43.root
rucio list-files cms:/store/mc/RunIIFall17NanoAODv7/NMSSM_XToYHTo4B_MX-1000_MY-150_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v2/70000/*.root


%s/^.*\(\/store.*root\).*$/\1/g
g!/\/store.*root/d
%!uniq


rucio download --rse T2_DE_DESY cms:/store/mc/RunIISummer20UL17NanoAODv2/NMSSM_XtoHYto4b_MX_1000_MY_150_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v8-v1/260000/63421650-960B-E34E-98CA-DC6DD0493059.root

rucio download --rse T1_US_FNAL_Disk cms:/store/mc/RunIISummer20UL17NanoAODv2/NMSSM_XtoHYto4b_MX_1000_MY_150_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_mc2017_realistic_v8-v1/260000/63421650-960B-E34E-98CA-DC6DD0493059.root



/NMSSM_XToYHTo4b_MX-900_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_RP_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM
/NMSSM_XToYHTo4b_MX-900_TuneCUETP8M1_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_RP_102X_mcRun2_asymptotic_v8-v1/100000/B49FB79A-321D-B54A-A2C7-4705D08BB10D.root
root://cmsxrootd.fnal.gov//store/mc/RunIISummer16NanoAODv7/NMSSM_XToYHTo4b_MX-900_TuneCUETP8M1_13TeV-madgraph-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_RP_102X_mcRun2_asymptotic_v8-v1/100000/B49FB79A-321D-B54A-A2C7-4705D08BB10D.root

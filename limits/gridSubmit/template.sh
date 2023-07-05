#!/bin/bash

{ # start of redirection..., keep stderr and stdout in a single file, it's easier

# tar -zcf test.tar.gz prepareModels/
# xrdpc -f -s
# xrdcp -s test.tar.gz root://cmseos.fnal.gov/store/user/agrummer/bbbb_limits/gof_2023Jun6/combine_tar/test.tar.gz
# t3SubmitScript = '/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/scripts/t3submit'

SCRAM_VER=slc7_amd64_gcc700
CMSSW_VERSION=CMSSW_10_2_13
EOSLINK="root://cmseos.fnal.gov/"
EOSDIR="/store/user/${USER}/bbbb_limits/"
TAG="gof_2023Jun6"
TAR_NAME="test.tar.gz"
TAR_EOS_DEST="${EOSLINK}${EOSDIR}${TAG}/combine_tar/$TAR_NAME"

echo "... starting job on " `date` #Date/time of start of job
echo "... running on: `uname -a`" #Condor job is running on this node
echo "... system software: `cat /etc/redhat-release`" #Operating System on that node
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=${SCRAM_VER}
echo "SCRAM_ARCH="${SCRAM_ARCH}
eval `scramv1 project CMSSW ${CMSSW_VERSION}`
cd ${CMSSW_VERSION}/src
eval `scramv1 runtime -sh`
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.2.0
scramv1 b clean; scramv1 b
echo "... retrieving bbbb executables tarball"
xrdcp -f -s ${TAR_EOS_DEST} # force overwrite CMSSW tar
echo "... uncompressing bbbb executables tarball"
tar -xzf ${TAR_NAME}
rm ${TAR_NAME}
echo "... retrieving filelist"
export CPP_BOOST_PATH=/cvmfs/sft.cern.ch/lcg/views/LCG_89/x86_64-slc6-gcc62-opt
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:./lib:${CPP_BOOST_PATH}/lib

echo "RUN JOBS HERE"

cd ${_CONDOR_SCRATCH_DIR}
rm -rf ${CMSSW_VERSION}
echo "... job finished with status $?"
echo "... finished job on " `date`
echo "... exiting script"
} 2>&1 # end of redirection

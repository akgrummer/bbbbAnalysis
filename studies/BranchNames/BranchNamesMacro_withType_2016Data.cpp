// g++ BranchNamesMacro_withType.cpp -o BranchNamesMacro_withType `root-config --glibs --cflags`
//this codes was not tested - the type information is included in the GetTitle call
#include "TCut.h"
#include "TString.h"
#include "TFile.h"
#include "TTree.h"
#include "TLegend.h"
#include "TVector3.h"
#include "TH1.h"
#include "TBranch.h"
#include "TCanvas.h"
#include <iostream>
#include <dirent.h>
#include <TChain.h>
#include <algorithm>
#include <fstream>
using namespace std;
void BranchNamesMacro(TString ifName){
// TFile* myfile = new TFile(ifName,"read");
// TString ifile = "root://cmseos.fnal.gov//store/user/agrummer/bbbb_ntuples/fullSubmission_2016_v27/SKIM_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_90/output/bbbbNtuple_0.root"
TString ifile = "root://cmseos.fnal.gov//store/user/agrummer/bbbb_ntuples/fullSubmission_2016_v27/SKIM_BTagCSV_Data/output/bbbbNtuple_98.root"
TFile* myfile = new TFile(ifile,"read");
TTree* myTree = (TTree*) myfile->Get("bbbbTree");
// TTree* myTreeEV = (TTree*) myfile->Get("EventInfo");
TObjArray *mycopy = myTree->GetListOfBranches(); 
// TObjArray *mycopy = myTree->GetListOfBranches()->Clone(); 
mycopy->SetOwner(kFALSE); 
mycopy->Sort();

// TObjArray *mycopyEV = myTreeEV->GetListOfBranches();
// mycopyEV->SetOwner(kFALSE);
// mycopyEV->Sort();

// for(int i = 0; i < array->GetEntries(); ++i) { cout << array->At(i)->GetName() << '\n'; }
TString ofileName("");
ofileName = ifName;
ofileName.Remove(0,ifName.Last('/')+1);
ofileName.ReplaceAll(".root","");
// ofileName.ReplaceAll(ifName, "")
// TString odName = "/afs/cern.ch/user/a/agrummer/www/bmumu/valSignOff/BranchNames/";
// TString odName = "/afs/cern.ch/user/a/agrummer/www/bmumu2020/nTupleBranchNames/";
TString odName = "/uscms/home/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/studies/BranchNames/";
ofileName = odName + ofileName;

ofstream myTextfile;
myTextfile.open (ofileName + "_bbbbTree.txt");
// myfile << "a  b\n";
for(int i = 0; i < mycopy->GetEntries(); ++i) { 
    myTextfile << mycopy->At(i)->GetName() << " "<< mycopy->At(i)->GetTitle() << '\n'; 
}

myTextfile.close();

// ofstream myTextfileEV;
// myTextfileEV.open (ofileName + "_EventInfo.txt");
// // myfile << "a  b\n";
// for(int i = 0; i < mycopyEV->GetEntries(); ++i) {
    // myTextfileEV << mycopyEV->At(i)->GetName() << " "<< mycopyEV->At(i)->GetTitle() << '\n';
// }

// myTextfileEV.close();
// return 0;
}

int main(int argc, char* argv[])
{
  TString ifName;
  if (argc>1) ifName = TString(argv[1]);
  BranchNamesMacro(ifName);
  return 0;
}


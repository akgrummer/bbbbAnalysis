#include "Riostream.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TH2D.h"
#include "TLine.h"
#include "TCanvas.h"
#include "TROOT.h"
#include <stdlib.h>
#include <map>
#include <tuple>
#include <vector>
#include <fstream>
#include <algorithm>
#include <stdio.h>

// g++  -std=c++17 -I `root-config --incdir`  -o an-scripts/exe/LEE_addInfoToSignifTree an-scripts/LEE_addInfoToSignifTree.cc `root-config --libs` -O3

int main(int argc, char** argv)
{
    if(argc!=6)
    {
        std::cout<<"Usage: ./an-scripts/LEE_addInfoToSignifTree <iofile> <mX> <mY> <toyNum> <sim>"<<std::endl;
        exit(EXIT_FAILURE);
    }
    // simulation code - 0: data, 1: MC sim, 2: interpolated

    TString ioFileName = argv[1];
    TString mXname = argv[2];
    TString mYname = argv[3];
    TString toyName = argv[4];
    TString simCode = argv[5];
    int toyNum = toyName.Atoi();
    int mX = mXname.Atoi();
    int mY = mYname.Atoi();
    int sim = simCode.Atoi();
    std::cout<<"i am integer: "<<toyNum<<std::endl;
    std::cout<<"i am tstring: "<<toyName<<std::endl;
    std::unique_ptr<TFile> ioFile( TFile::Open(ioFileName, "UPDATE") );
    // auto tree = ioFile->Get<TTree>("limit");
    TTree *tree = (TTree*)ioFile->Get("limit");
    TBranch *b_toyNum = tree->Branch("toyNum",&toyNum,"toyNum/I");
    TBranch *b_mX = tree->Branch("mX",&mX,"mX/I");
    TBranch *b_mY = tree->Branch("mY",&mY,"mY/I");
    TBranch *b_sim = tree->Branch("sim",&sim,"sim/I");
    Long64_t nentries = tree->GetEntries();
    // std::cout<<"entries: "<<nentries<<std::endl;
    tree->GetEntry(0);
    b_toyNum->Fill();
    b_mX->Fill();
    b_mY->Fill();
    b_sim->Fill();
    // tree->Print();
    tree->Write();
}

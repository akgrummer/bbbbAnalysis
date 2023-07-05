#ifndef HISTFILECLASS_H
#define HISTFILECLASS_H
#include <iostream>
#include <range/v3/all.hpp>

#include <TStyle.h>
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TChain.h>
#include <TCut.h>
#include <TString.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TF1.h>
#include <TLatex.h>
#include <TCanvas.h>
#include <TPad.h>
#include <Rtypes.h>
#include <RtypesCore.h>
#include <TLegend.h>
#include <TH1.h>

class HistFile{
    public:
    HistFile(TString, std::string, std::vector<std::string>, TString, TString );
    ~HistFile();
    TString avar;
    TTree *itree;
    TChain *chain;
    TFile *ofile;
    TFile *ifile;
    int nselected;
    TString TempString;

    TString branchName;
    TString htitle;
    TString hname;
    TString hweightName;
    TString hregionName;
    TCut hcut;
    TCut hweight;
    ranges::span<Double_t> bins;
    void SaveHist(TString);
    void SetBranch( TString );
    void SetBins( ranges::span<Double_t>);
    void SetCutData(TCut , TString);
    void SetWeightData(TString, TString);
    bool first = true;
    int histcnt = 0;

    private:
    std::string ipath;
};
#endif


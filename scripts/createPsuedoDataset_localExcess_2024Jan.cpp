#include <iostream>
#include <map>
#include "Riostream.h"
#include "TFile.h"
#include "TH1F.h"
#include "TH1D.h"
#include "TH2F.h"
#include "TString.h"
#include "TMath.h"

void createPsuedoDataset_localExcess_2024Jan(int year, TString sig_tag, TString sig_name){

    TString tag="2024Jan26_psuedoData_checkExcessLimits_"+sig_tag;
    // sig_tag="mx650_my350";
    TString tagDir = "fullSubmission_2022Nov/";

    TString iodir = "VarPlots/rootHists/" + tagDir + Form("%d", year) + "DataPlots_" + tag +"/";
    TString iofilename="outPlotter_massGroup1.root";

    TFile *iofile = new TFile(iodir+iofilename, "UPDATE");

    TString bkg_name="data_BTagCSV_dataDriven_kinFit";
    TString data_name="data_BTagCSV";
    // TString sig_name="sig_NMSSM_bbbb_MX_700_MY_400";

    TString region="selectionbJets_SignalRegion";
    TString varname="HH_kinFit_m_H2_m_Rebinned_Unrolled";

    TH1F *hbkg=(TH1F*)iofile->Get(bkg_name+"/"+region+"/"+bkg_name+"_"+region+"_"+varname);
    TH1F *hsig=(TH1F*)iofile->Get(sig_name+"/"+region+"/"+sig_name+"_"+region+"_"+varname);

    TH1F* hpseudodata   = (TH1F*) hbkg->Clone(data_name+"_"+region+"_"+varname);
    hsig->Scale(10);
    hpseudodata->Add(hsig);

    iofile->cd(data_name+"/"+region);
    hpseudodata->Write();

}

int main(int argc, char *argv[])
{
    std::vector<int> yearList {2016, 2017, 2018};
    TString sig_tag = argv[1];
    TString sig_name = argv[2];
    for(const auto year : yearList)
    {
        createPsuedoDataset_localExcess_2024Jan(year, sig_tag, sig_name);
    }
    return 0;
}


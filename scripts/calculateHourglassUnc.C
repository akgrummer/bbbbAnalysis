#include <iostream>
#include "Riostream.h"
#include "TFile.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TString.h"
#include "TMath.h"

using namespace std;

void calculate_HG_BKGshape(int year)
{
    TString tagDir = "fullSubmission_2022Nov/";
    TString tag= "2023Feb28_3";
    TString tagNew= "2023Feb28_3";
    TFile *ofile;
    TString odir = "./hists/";
    TString ofilename = "hourglass_test"+std::to_string(year)+".root";
    TString ifilename = "../VarPlots/rootHists/" + tagDir + Form("%d", year) + "DataPlots_" + tag + "/outPlotter.root";
    TFile *ifile = new TFile(ifilename, "READ");
    TString dataset          = "data_BTagCSV_dataDriven_kinFit"    ;
    TString region           = "selectionbJets_SignalRegion"       ;
    TString regionVR         = "selectionbJets_ValidationRegionBlinded"       ;
    TString varname          = "HH_kinFit_m_H2_m";

    TH2F *h1=(TH2F*)ifile->Get(dataset+"/"+region+"/"+dataset+"_"+region+"_"+varname);
    TH2F* h1up   = (TH2F*) h1->Clone("h1up");
    h1up->SetTitle("hour glass unc up");
    TH2F* h1down = (TH2F*) h1->Clone("h1down");
    h1down->SetTitle("hour glass unc down");
    for(int yBin = 1; yBin<=h1->GetNbinsY(); ++yBin)
    {
        for(int xBin=1; xBin<=h1->GetNbinsX(); ++xBin){
            // if (TMath::IsNaN(h1->GetXaxis()->GetBinCenter(yBin))){continue;}
            if (62<h1->GetYaxis()->GetBinCenter(yBin) && h1->GetYaxis()->GetBinCenter(yBin)<188)
            {
                h1up->SetBinContent(  xBin, yBin, h1->GetBinContent(xBin, yBin)*1.1   );
                h1down->SetBinContent( xBin, yBin, h1->GetBinContent(xBin, yBin)*0.9 );
            }
        }
    }

    TH1D *h1_x = h1->ProjectionX("h1_x"); h1_x->SetLineColor(kBlue+2);
    TH1D *h1_y = h1->ProjectionY("h1_y"); h1_y->SetLineColor(kBlue+2);
    TH1D *h1up_x = h1up->ProjectionX("h1up_x"); h1up_x->SetLineColor(kRed+2);
    TH1D *h1up_y = h1up->ProjectionY("h1up_y"); h1up_y->SetLineColor(kRed+2);
    TH1D *h1down_x = h1down->ProjectionX("h1down_x"); h1down_x->SetLineColor(kGreen+2);
    TH1D *h1down_y = h1down->ProjectionY("h1down_y"); h1down_y->SetLineColor(kGreen+2);

    ofile = new TFile(odir+ofilename, "RECREATE");
    h1->Write();
    h1_x->Write();
    h1_y->Write();
    h1up->Write();
    h1up_x->Write();
    h1up_y->Write();
    h1down->Write();
    h1down_x->Write();
    h1down_y->Write();
    ofile->Close();

}

int main()
{
    std::vector<int> massesGroupList {0, 1, 2, 3, 4};
    std::vector<int> yearList {2016, 2017, 2018};

    for(const auto year : yearList)
    {
        calculate_HG_BKGshape(year);
    }
    return 0;
}


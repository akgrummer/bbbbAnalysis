#include <iostream>
#include <map>
#include "Riostream.h"
#include "TFile.h"
#include "TH1F.h"
#include "TH1D.h"
#include "TH2F.h"
#include "TString.h"
#include "TMath.h"

using namespace std;

float higgsMass = 120;
float mYmin =    0.;
float mYmax = 2400.;
float mXmin;
float mXmax;
bool firstTime = true;

//-------------------------------------------------------------------------------------------------------------------------------------//

bool isNeededBin(TH2F *the2Dplot, uint xBin, uint yBin)
{
    float mX = the2Dplot->GetXaxis()->GetBinCenter(xBin);
    float mY = the2Dplot->GetYaxis()->GetBinCenter(yBin);
    if(mY < mYmin || mY > mYmax) return false;

    // if( (mX - mY > higgsMass) && (mX - mY < higgsMass + konigsbergLine) )
    // {
    //     return true;
    // }
    if( mX - mY < higgsMass)  return false;
    if( mX > 1200 && mY < 80) return false;
    if( mX > mXmax) return false;
    if( mX < mXmin) return false;


    return true;
}

//-------------------------------------------------------------------------------------------------------------------------------------//
//-------------------------------------------------------------------------------------------------------------------------------------//

void FillRebinnedPlot (TH2F *the2DsourcePlot, TH2F *the2DtargetPlot)
{

    for(int xBin = 1; xBin <= the2DsourcePlot->GetNbinsX(); xBin++)
    {
        for(int yBin = 1; yBin <= the2DsourcePlot->GetNbinsY(); yBin++)
        {
            int newXBin = the2DtargetPlot->GetXaxis()->FindBin(the2DsourcePlot->GetXaxis()->GetBinCenter(xBin));
            int newYBin = the2DtargetPlot->GetYaxis()->FindBin(the2DsourcePlot->GetYaxis()->GetBinCenter(yBin));
            the2DtargetPlot->SetBinContent(newXBin,newYBin, the2DsourcePlot->GetBinContent(xBin,yBin));
            the2DtargetPlot->SetBinError  (newXBin,newYBin, the2DsourcePlot->GetBinError(xBin,yBin));
        }
    }
}

//-------------------------------------------------------------------------------------------------------------------------------------//
//-------------------------------------------------------------------------------------------------------------------------------------//

TH1D* UnrollPlot(TH2F* the2Dplot)
{
    uint nXbin = the2Dplot->GetNbinsX();
    uint nYbin = the2Dplot->GetNbinsY();
    // uint numberOfBins = nXbin*nYbin;
    // float theBinArray[numberOfBins+1];
    // theBinArray[0] = the2Dplot->GetXaxis()->GetBinLowEdge(1);

    uint totalNumberOfBins = 0;
    for(uint yBin=1; yBin<=nYbin; ++yBin)
    {
        for(uint xBin=1; xBin<=nXbin; ++xBin)
        {
            if(isNeededBin(the2Dplot, xBin, yBin)) ++totalNumberOfBins;
        }
    }
    if(firstTime)
    {
        std::cout<<"Total number of bins = " << totalNumberOfBins << std::endl;
        firstTime = false;
    }
    std::string unRolledPlotName = std::string(the2Dplot->GetName()) + "_Unrolled";
    TH1D *the1Dplot = new TH1D(unRolledPlotName.data(),unRolledPlotName.data(),totalNumberOfBins,0, totalNumberOfBins);
    the1Dplot->SetDirectory(0);

    uint newBinNumber = 1;
    for(uint yBin = 1; yBin <= nYbin; yBin++)
    {
        for(uint xBin = 1; xBin <= nXbin; xBin++)
        {
            // float mX = the2Dplot->GetXaxis()->GetBinCenter(xBin);
            // float mY = the2Dplot->GetYaxis()->GetBinCenter(yBin);
            if(!isNeededBin(the2Dplot, xBin, yBin)) continue;

            float value = the2Dplot->GetBinContent(xBin,yBin);
            float error = the2Dplot->GetBinError(xBin,yBin);
            if(value == 0)
            {
                std::cout<<"This should never happen!!!"<<std::endl;
                value = 1e-5;
                error = 1e-5;
            }
            // if(!isBkg)
            // {
            //     value*=0.9;
            //     error*=0.9;
            // }
            the1Dplot->SetBinContent(newBinNumber, value);
            the1Dplot->SetBinError(newBinNumber++, error);
        }
    }
    return the1Dplot;
}

//-------------------------------------------------------------------------------------------------------------------------------------//
void calculate_HG_BKGshape(int year)
{
    TString tagDir = "fullSubmission_2022Nov/";
    TString tag= "2023Feb28_3";
    TString odir = "./hists/";
    TString ifilename = "../VarPlots/rootHists/" + tagDir + Form("%d", year) + "DataPlots_" + tag + "/outPlotter.root";
    // TString ofilename = "hourglass_test_unrolled"+std::to_string(year)+".root";
    TFile *ifile = new TFile(ifilename, "READ");
    TString dataset          = "data_BTagCSV_dataDriven_kinFit"    ;
    // TString region           = "selectionbJets_SignalRegion"       ;
    TString region           = "selectionbJets_ValidationRegionBlinded"       ;
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

    std::map<int, std::pair<float, float>> theMassGroupList;
    theMassGroupList[0] = std::make_pair(212.,  800.);
    theMassGroupList[1] = std::make_pair(300., 1000.);
    theMassGroupList[2] = std::make_pair(450., 1200.);
    theMassGroupList[3] = std::make_pair(600., 1600.);
    theMassGroupList[4] = std::make_pair(950., 2320.);

    for(const auto& massGroup : theMassGroupList){
        mXmin    = massGroup.second.first ;
        mXmax    = massGroup.second.second;
        // mXmin = 450.;
        // mXmax = 1200;

        TString tagNew= "2023Feb28_3_hourglass_unc";
        TString ofilename = Form("hists/hourglassUnc_VR_%d.root", year);
        // TFile *ofile = new TFile(odir+ofilename, "UPDATE");
        TFile *ofile = new TFile(ofilename, "RECREATE");

        TString h1_rebinned_name = dataset+"_"+region+"_"+varname + "_Rebinned";
        TH2F* h1_rebinned = (TH2F*) h1->Clone(h1_rebinned_name);
        h1_rebinned->Reset();

        FillRebinnedPlot(h1, h1_rebinned);
        TH1D* h1_unrolled = UnrollPlot(h1_rebinned);

        TString h1up_rebinned_name = dataset+  "_hourglass_up" +"_"+region+"_"+varname + "_Rebinned";
        TH2F* h1up_rebinned = (TH2F*) h1->Clone(h1up_rebinned_name);
        h1up_rebinned->Reset();

        FillRebinnedPlot(h1up, h1up_rebinned);
        TH1D* h1up_unrolled = UnrollPlot(h1up_rebinned);
        h1up_unrolled->SetLineColor(kRed+2);

        TString h1down_rebinned_name = dataset + "_hourglass_down" +"_"+region+"_"+varname + "_Rebinned";
        TH2F* h1down_rebinned = (TH2F*) h1->Clone(h1down_rebinned_name);
        h1down_rebinned->Reset();

        FillRebinnedPlot(h1down, h1down_rebinned);
        TH1D* h1down_unrolled = UnrollPlot(h1down_rebinned);
        h1down_unrolled->SetLineColor(kGreen+2);

        TH1D *h1_x = h1->ProjectionX("HH_kinFit_m"); h1_x->SetLineColor(kBlue+2);
        TH1D *h1_y = h1->ProjectionY("H2_m"); h1_y->SetLineColor(kBlue+2);
        TH1D *h1up_x = h1up->ProjectionX("HH_kinFit_m_hourglass_up"); h1up_x->SetLineColor(kRed+2);
        TH1D *h1up_y = h1up->ProjectionY("H2_m_hourglass_up"); h1up_y->SetLineColor(kRed+2);
        TH1D *h1down_x = h1down->ProjectionX("HH_kinFit_m_hourglass_down"); h1down_x->SetLineColor(kGreen+2);
        TH1D *h1down_y = h1down->ProjectionY("H2_m_hourglass_down"); h1down_y->SetLineColor(kGreen+2);

        h1->Write();
        h1_x->Write();
        h1_y->Write();
        h1up->Write();
        h1up_x->Write();
        h1up_y->Write();
        h1down->Write();
        h1down_x->Write();
        h1down_y->Write();
        h1_unrolled->Write();
        ofile->mkdir(dataset + "_hourglass_up");
        ofile->mkdir(dataset + "_hourglass_up" + "/" + region);
        ofile->mkdir(dataset + "_hourglass_down");
        ofile->mkdir(dataset + "_hourglass_down" + "/" + region );

        ofile->cd(dataset + "_hourglass_up" + "/" + region );
        h1up_unrolled->Write();
        ofile->cd(dataset + "_hourglass_down" + "/" + region );
        h1down_unrolled->Write();
        ofile->Close();
    }

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


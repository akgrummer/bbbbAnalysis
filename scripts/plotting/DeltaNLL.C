
#include "Riostream.h"
#include "TFile.h"
#include "TH2D.h"
#include "TLine.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TLatex.h"
#include "TROOT.h"
#include "TTree.h"
#include "TString.h"
#include "TStyle.h"
#include "TGraphAsymmErrors.h"
#include <map>
#include <tuple>
#include <vector>
#include <fstream>
#include <algorithm>


// g++  -std=c++17 -I `root-config --incdir`  -o ../scripts/plotting/DeltaNLL ../scripts/plotting/DeltaNLL.C `root-config --libs` -O3
// ../scripts/plotting/DeltaNLL


void makePlot(TString ifileName, TString ofileName){

    std::unique_ptr<TFile> myFile( TFile::Open(ifileName));
    auto mytree = myFile->Get<TTree>("limit");

    TCanvas* theCanvas = new TCanvas("c1", "c1", 800, 800);
    gPad->SetTickx(1);
    gPad->SetTicky(1);
    gPad->SetMargin(0.16,0.05,0.12,0.05);
    gStyle->SetOptTitle(0);

    mytree->Draw("2*deltaNLL:r");
    mytree->SetMarkerStyle(20);
    mytree->SetMarkerSize(1.2);
    mytree->Draw("2*deltaNLL:r", "quantileExpected>=0", "same");

    mytree->SetMarkerStyle(5);
    mytree->SetMarkerSize(1.2);
    mytree->SetMarkerColor(2);
    mytree->Draw("2*deltaNLL:r", "quantileExpected==-1", "same");

    auto CMSlabel = new TLatex();
    CMSlabel->SetTextFont(63);
    CMSlabel->SetTextSize( 30 );
    // CMSlabel->DrawLatexNDC(0.16, 0.96, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}");
    CMSlabel->DrawLatexNDC(0.22, 0.88, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}");

    CMSlabel->SetTextFont(43);
    CMSlabel->SetTextSize(25);
    TString yearLabel="138 fb^{-1} (13 TeV)";
    CMSlabel->DrawLatexNDC(0.585, 0.96, yearLabel);

    CMSlabel->SetTextFont(43);
    CMSlabel->SetTextSize(25);
    CMSlabel->DrawLatexNDC(0.22, 0.84, ofileName);


    TString SaveName = "studies/DeltaNLL/"+ofileName+".pdf";
    theCanvas->SaveAs(SaveName);
    delete theCanvas;
    delete mytree;
}

int main(int argc, char** argv)
{
    TString ifile1 = "root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Dec7_binMYx2_addMX650_10ev_unblind_deltaNLL_neg20_SR/HistogramFiles_RunII/Limit_RunII_sig_NMSSM_bbbb_MX_400_MY_250_syst.root";
    TString ofile1 = "mX400mY250";

    TString ifile2 = "root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Dec7_binMYx2_addMX650_10ev_unblind_deltaNLL_SR/HistogramFiles_RunII/Limit_RunII_sig_NMSSM_bbbb_MX_700_MY_400_syst.root";
    TString ofile2 = "mX700mY400";

    makePlot(ifile1, ofile1);
    makePlot(ifile2, ofile2);


    return 0;
}





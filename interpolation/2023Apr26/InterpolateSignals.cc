#include "RooWorkspace.h"
#include "RooPlot.h"
#include "RooRealVar.h"
#include "RooArgList.h"
#include "TVectorD.h"
#include "RooMomentMorphND.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TH2F.h"
#include "RooDataHist.h"
#include "RooHistPdf.h"
#include "RooAddPdf.h"
#include "TRandom.h"
#include "TFile.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TPaveStats.h"
#include "TRatioPlot.h"

// g++ -std=c++17 -g -o3 -fPIC -I `root-config --incdir` -c RooMomentMorphND_local.cpp -o RooMomentMorphND_local.o && g++  -std=c++17 -g -I `root-config --incdir` -lRooFit -lRooFitCore -o TestInterpolatorHist2D2D TestInterpolatorHist2D2D.cc `root-config --libs` -O3 RooMomentMorphND_local.o  && ./TestInterpolatorHist2D2D 2

using namespace RooFit;

void TestInterpolatorHist2D2D(int year)
{
int numberOfGridBins = 1;
float mXtarget=1000.; float mYtarget=150.;

    TString filename = "";
    // filename.Form("../../VarPlots/rootHists/fullSubmission_2022Nov/%dDataPlots_2023Feb28_3/outPlotter.root", year);
    TString tag;
    tag.Form("%dDataPlots_2023Dec7_binMYx2_addMX650_10ev",year);
    // filename.Form("../../VarPlots/rootHists/fullSubmission_2022Nov/%dDataPlots_2023Feb28_3/outPlotter.root", year);
    filename = "../../VarPlots/rootHists/fullSubmission_2022Nov/"+tag+"/outPlotter.root";
    TFile *ifile = new TFile( filename, "READ");
    TString ofilename = "";
    // ofilename.Form("hists/InterpHists_%d_newGrid.root", year);
    ofilename.Form("hists/InterpHists_%d_2023Dec19.root", year);
    TFile *ofile = new TFile( ofilename, "RECREATE");
    TString sigRegion  = "selectionbJets_SignalRegion";
    TString varname = "HH_kinFit_m_H2_m";

    TString sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","1000","125");
    TH2F *sig_low_low=(TH2F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname);
    // sig_low_low->Scale(1./sig_low_low->Integral());
    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","1000","200");
    TH2F *sig_low_high=(TH2F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname);
    // sig_low_high->Scale(1./sig_low_high->Integral());
    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","1100","125");
    TH2F *sig_high_low=(TH2F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname);
    // sig_high_low->Scale(1./sig_high_low->Integral());
    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","1100","200");
    TH2F *sig_high_high=(TH2F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname);
    // sig_high_high->Scale(1./sig_high_high->Integral());
    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","1000","150");
    TH2F *sig_real=(TH2F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname);
    // sig_real->Scale(1./sig_real->Integral());

	RooArgList variableList;

	RooRealVar mXreco("mXreco", "m_{Xreco}", sig_low_low->GetXaxis()->GetXmin(), sig_low_low->GetXaxis()->GetXmax(), "GeV");
	RooRealVar mYreco("mYreco", "m_{Yreco}", sig_low_low->GetYaxis()->GetXmin(), sig_low_low->GetYaxis()->GetXmax(), "GeV");
	variableList.add(mXreco);
	variableList.add(mYreco);

	RooDataHist data_sig_low_low("data_sig_low_low", "data_sig_low_low", variableList, sig_low_low);
	RooHistPdf  pdf_low_low("pdf_low_low", "pdf_low_low", variableList, data_sig_low_low );

	RooDataHist data_sig_low_high("data_sig_low_high", "data_sig_low_high", variableList, sig_low_high);
	RooHistPdf  pdf_low_high("pdf_low_high", "pdf_low_high", variableList, data_sig_low_high );

	RooDataHist data_sig_high_low("data_sig_high_low", "data_sig_high_low", variableList, sig_high_low);
	RooHistPdf  pdf_high_low("pdf_high_low", "pdf_high_low", variableList, data_sig_high_low );

	RooDataHist data_sig_high_high("data_sig_high_high", "data_sig_high_high", variableList, sig_high_high);
	RooHistPdf  pdf_high_high("pdf_high_high", "pdf_high_high", variableList, data_sig_high_high );


// 	TH2F* histGaussian_mXlow_mYlow = new TH2F("histGaussian_mXlow_mYlow", "histGaussian_mXlow_mYlow", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
// 	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXlow_mYlow->Fill(gRandom->Gaus(mXlow, mXlowSigma), gRandom->Gaus(mXlow, mXlowSigma));
// 	RooDataHist dh2Gaussian_mXlow_mYlow("dh2Gaussian_mXlow_mYlow", "dh2Gaussian_mXlow_mYlow", variableList, histGaussian_mXlow_mYlow);
// 	RooHistPdf  pdfGaussian_mXlow_mYlow("pdfGaussian_mXlow_mYlow", "pdfGaussian_mXlow_mYlow", variableList, dh2Gaussian_mXlow_mYlow );
//
// 	TH2F* histGaussian_mXlow_mYhigh = new TH2F("histGaussian_mXlow_mYhigh", "histGaussian_mXlow_mYhigh", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
// 	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXlow_mYhigh->Fill(gRandom->Gaus(mXlow, mXlowSigma), gRandom->Gaus(mXhigh, mXhighSigma));
// 	RooDataHist dh2Gaussian_mXlow_mYhigh("dh2Gaussian_mXlow_mYhigh", "dh2Gaussian_mXlow_mYhigh", variableList, histGaussian_mXlow_mYhigh);
// 	RooHistPdf  pdfGaussian_mXlow_mYhigh("pdfGaussian_mXlow_mYhigh", "pdfGaussian_mXlow_mYhigh", variableList, dh2Gaussian_mXlow_mYhigh );
//
// 	TH2F* histGaussian_mXhigh_mYlow = new TH2F("histGaussian_mXhigh_mYlow", "histGaussian_mXhigh_mYlow", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
// 	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXhigh_mYlow->Fill(gRandom->Gaus(mXhigh, mXhighSigma), gRandom->Gaus(mXlow, mXlowSigma));
// 	RooDataHist dh2Gaussian_mXhigh_mYlow("dh2Gaussian_mXhigh_mYlow", "dh2Gaussian_mXhigh_mYlow", variableList, histGaussian_mXhigh_mYlow);
// 	RooHistPdf  pdfGaussian_mXhigh_mYlow("pdfGaussian_mXhigh_mYlow", "pdfGaussian_mXhigh_mYlow", variableList, dh2Gaussian_mXhigh_mYlow );
//
// 	TH2F* histGaussian_mXhigh_mYhigh = new TH2F("histGaussian_mXhigh_mYhigh", "histGaussian_mXhigh_mYhigh", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
// 	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXhigh_mYhigh->Fill(gRandom->Gaus(mXhigh, mXhighSigma), gRandom->Gaus(mXhigh, mXhighSigma));
// 	RooDataHist dh2Gaussian_mXhigh_mYhigh("dh2Gaussian_mXhigh_mYhigh", "dh2Gaussian_mXhigh_mYhigh", variableList, histGaussian_mXhigh_mYhigh);
// 	RooHistPdf  pdfGaussian_mXhigh_mYhigh("pdfGaussian_mXhigh_mYhigh", "pdfGaussian_mXhigh_mYhigh", variableList, dh2Gaussian_mXhigh_mYhigh );

	RooBinning binningX(numberOfGridBins, 1000, 1100);
	RooBinning binningY(numberOfGridBins, 125, 200);
	// RooBinning binningX(2, mXlow, mXhigh);
	// RooBinning binningY(2, mXlow, mXhigh);
	// RooBinning binningX(2,0,1);
	// RooBinning binningY(2,0,1);

	RooMomentMorphND::Grid theGrid(binningX,binningY);
    // RooArgList pdfs;
    // pdfs.add(gaussian_mXlow_mYlow);
    // pdfs.add(gaussian_mXmed_mYlow );
    // pdfs.add(gaussian_mXlow_mYmed );
    // pdfs.add(gaussian_mXlow_mYhigh);
    // pdfs.add(gaussian_mXmed_mYhigh);
    // pdfs.add(gaussian_mXhigh_mYmed);
    // pdfs.add(gaussian_mXhigh_mYlow );
    // pdfs.add(gaussian_mXhigh_mYhigh);

    theGrid.addPdf(pdf_low_low  , 0, 0);
    theGrid.addPdf(pdf_low_high  , 0, 1);
    theGrid.addPdf(pdf_high_low  , 1, 0);
    theGrid.addPdf(pdf_high_high  , 1, 1);

    // theGrid.addPdf(pdfGaussian_mXlow_mYlow  , 0, 0);
    // theGrid.addPdf(pdfGaussian_mXlow_mYmed  , 0, 1);
    // theGrid.addPdf(pdfGaussian_mXlow_mYhigh , 0, 2);
    // theGrid.addPdf(pdfGaussian_mXmed_mYlow  , 1, 0);
    // theGrid.addPdf(pdfGaussian_mXmed_mYmed  , 1, 1);
    // theGrid.addPdf(pdfGaussian_mXmed_mYhigh , 1, 2);
    // theGrid.addPdf(pdfGaussian_mXhigh_mYlow , 2, 0);
    // theGrid.addPdf(pdfGaussian_mXhigh_mYmed , 2, 1);
    // theGrid.addPdf(pdfGaussian_mXhigh_mYhigh, 2, 2);

	RooArgList alphaTargetList;
	RooRealVar alphaTargetX("alphaTargetX", "alphaTargetX",sig_low_low->GetXaxis()->GetXmin(), sig_low_low->GetXaxis()->GetXmax());
	alphaTargetX.setVal(mXtarget);
	alphaTargetList.add(alphaTargetX);
	RooRealVar alphaTargetY("alphaTargetY", "alphaTargetY", sig_low_low->GetYaxis()->GetXmin(), sig_low_low->GetYaxis()->GetXmax());
	alphaTargetY.setVal(mYtarget);
	alphaTargetList.add(alphaTargetY);

	std::cout<< __PRETTY_FUNCTION__ << __LINE__ << std::endl;
	RooMomentMorphND sig_morph("morph", "morph", alphaTargetList, variableList, theGrid, RooMomentMorphND::Linear);
	std::cout<< __PRETTY_FUNCTION__ << __LINE__ << std::endl;
	sig_morph.useHorizontalMorphing(true);
	std::cout<< __PRETTY_FUNCTION__ << __LINE__ << std::endl;

	// TH2F* histGaussian_mXmean_mYmean = new TH2F("histGaussian_mXmean_mYmean", "histGaussian_mXmean_mYmean", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	TH2F* sig_interp = (TH2F*) sig_low_low->Clone("sig_interp");
    sig_interp->Reset();
    sig_interp->SetTitle("interpolated mX 1000, mY 150");
	std::cout<< __PRETTY_FUNCTION__ << __LINE__ << std::endl;
	sig_morph.fillHistogram(sig_interp,variableList);
	std::cout<< __PRETTY_FUNCTION__ << __LINE__ << std::endl;
    sig_interp->Scale(sig_real->Integral()/sig_interp->Integral());

	// sig_interp->Scale(entriesNumber);
	sig_interp->SetMarkerColor(kRed);

	// gROOT->SetBatch(true);
    TCanvas c1;
    // gStyle->SetOptStat();
    // sig_low_low->Draw("colz");
    sig_low_low->Write();
    // TPaveStats *st = (TPaveStats*)sig_low_low->FindObject("stats");
    // st->SetX1NDC(0.2); //new x start position
    // st->SetX2NDC(0.4); //new x end position
	// c1.SaveAs(Form("plots/%d/sig_%d_low_low.pdf", year, year));
    // sig_low_high->Draw("colz");
    sig_low_high->Write();
	// // c1.SaveAs(Form("plots/%d/sig_%d_low_high.pdf", year, year));
    // sig_high_low->Draw("colz");
    sig_high_low->Write();
	// c1.SaveAs(Form("plots/%d/sig_%d_high_low.pdf", year, year));
    // sig_high_high->Draw("colz");
    sig_high_high->Write();
	// c1.SaveAs(Form("plots/%d/sig_%d_high_high.pdf", year, year));
    // histGaussian_mXmed_mYlow  ->Draw("same");
    // histGaussian_mXlow_mYmed  ->Draw("same");
    //histGaussian_mXlow_mYhigh ->Draw("same");
    // histGaussian_mXmed_mYhigh ->Draw("same");
    // histGaussian_mXhigh_mYmed ->Draw("same");
    // histGaussian_mXmed_mYmed ->Draw("same");
    //jhistGaussian_mXhigh_mYlow ->Draw("same");
    //histGaussian_mXhigh_mYhigh->Draw("same");
    //sig_low_low->Draw("colz");
    // sig_interp->Draw("colz");
    sig_interp->Write();
	// c1.SaveAs(Form("plots/%d/sig_%d_morph.pdf", year, year));

    TH1D *xprojInterp = sig_interp->ProjectionX("xproj_interp");
	xprojInterp->SetLineColor(kRed);
    xprojInterp->SetTitle("Xproj of interp MC 1000, 150");
    xprojInterp->Write();
    TH1D *yprojInterp = sig_interp->ProjectionY("yproj_interp");
    yprojInterp->SetTitle("Yproj of interp MC 1000, 150");
    yprojInterp->Write();
	yprojInterp->SetLineColor(kRed);

    // sig_real->Draw("colz");
    sig_real->Write();
	// c1.SaveAs(Form("plots/%d/sig_%d_real_1000_150.pdf", year, year));

    TH1D *xproj = sig_real->ProjectionX("xproj_real");
    xproj->SetTitle("Xproj of real MC 1000, 150");
    //xproj->SetLineColor(2);
    xproj->Write();
    TH1D *yproj = sig_real->ProjectionY("yproj_real");
    yproj->SetTitle("Yproj of real MC 1000, 150");
    //yproj->SetLineColor(2);
    yproj->Write();

// 	TH2F* xproj_ratio_1d = (TH2F*) xprojInterp->Clone("xproj_ratio_1d");
//     xproj_ratio_1d->Divide(xproj);
//     xproj->SetTitle("ratio of xproj");
//     xproj_ratio_1d->Write();
//
// 	TH2F* yproj_ratio_1d = (TH2F*) yprojInterp->Clone("yproj_ratio_1d");
//     yproj_ratio_1d->Divide(yproj);
//     yproj->SetTitle("ratio of yproj");
//     yproj_ratio_1d->Write();
//
//     TRatioPlot *xratioPlot = new TRatioPlot(xprojInterp, xproj);
//     // xratioPlot->Draw();
//     // xratioPlot->GetLowerRefGraph()->SetMinimum(0.5);
//     // xratioPlot->GetLowerRefGraph()->SetMaximum(1.5);
//     xratioPlot->Write();
//     TRatioPlot *yratioPlot = new TRatioPlot(yprojInterp, yproj);
    // yratioPlot->Draw();
    // yratioPlot->GetLowerRefGraph()->SetMinimum(0.5);
    // yratioPlot->GetLowerRefGraph()->SetMaximum(1.5);
//     yratioPlot->Write();

// 	TH2F* sig_ratio = (TH2F*) sig_interp->Clone("sig_ratio");
//     sig_ratio->SetTitle("ratio to produced MC at mX 1000, mY 150");
//     sig_ratio->Divide(sig_real);
//     sig_ratio->Draw("colz");
//     sig_ratio->Write();
//     sig_ratio->GetZaxis()->SetRangeUser(0,5);
//     sig_ratio->SetTitle("ratio to produced MC at mX 1000, mY 150 - z axis zoomed");
// 	c1.SaveAs(Form("plots/%d/sig_%d_ratio_zoomZ5.pdf", year, year));
//     sig_ratio->GetZaxis()->SetRangeUser(0,2);
//     sig_ratio->SetTitle("ratio to produced MC at mX 1000, mY 150 - z axis zoomed to max 2");
// 	c1.SaveAs(Form("plots/%d/sig_%d_ratio_zoomZ2.pdf", year, year));
ofile->Close();
	// gROOT->SetBatch(false);

}

int main(int argc, char** argv)
{
	ROOT::EnableThreadSafety();
    gSystem->ResetSignal(kSigSegmentationViolation, kTRUE);

	if(argc == 1){
        cout<<"please enter valid command line arguments"<<endl;
        return EXIT_FAILURE;
    }

    cout<<"Year: "<<argv[1]<<endl;
	TestInterpolatorHist2D2D(atoi(argv[1]));

	return EXIT_SUCCESS;
}

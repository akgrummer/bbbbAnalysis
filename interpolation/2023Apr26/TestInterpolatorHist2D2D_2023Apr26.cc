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

// g++ -std=c++17 -g -o3 -fPIC -I `root-config --incdir` -c RooMomentMorphND_local.cpp -o RooMomentMorphND_local.o && g++  -std=c++17 -g -I `root-config --incdir` -lRooFit -lRooFitCore -o TestInterpolatorHist2D2D TestInterpolatorHist2D2D.cc `root-config --libs` -O3 RooMomentMorphND_local.o  && ./TestInterpolatorHist2D2D 2

using namespace RooFit;

float TestInterpolatorHist2D2D(int numberOfGridBins, float mXtarget=50., float mYtarget=200.)
{

	float mXrecoMin =   0.;
	float mXrecoMax = 400.;
	int entriesNumber = 5000;
	int numberOfBins  = 100;


	RooArgList variableList;

	RooRealVar mXreco("mXreco", "m_{Xreco}", mXrecoMin, mXrecoMax, "GeV");
	RooRealVar mYreco("mYreco", "m_{Yreco}", mXrecoMin, mXrecoMax, "GeV");
	variableList.add(mXreco);
	variableList.add(mYreco);

	float mXlow       = 50.;
	float mXlowSigma  = mXlow/10.;
	float mXmed       = 175.;
	float mXmedSigma  = mXmed/10.;
	float mXhigh      = 300.;
	float mXhighSigma = mXhigh/10.;

	TH2F* histGaussian_mXlow_mYlow = new TH2F("histGaussian_mXlow_mYlow", "histGaussian_mXlow_mYlow", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXlow_mYlow->Fill(gRandom->Gaus(mXlow, mXlowSigma), gRandom->Gaus(mXlow, mXlowSigma));
	RooDataHist dh2Gaussian_mXlow_mYlow("dh2Gaussian_mXlow_mYlow", "dh2Gaussian_mXlow_mYlow", variableList, histGaussian_mXlow_mYlow);
	RooHistPdf  pdfGaussian_mXlow_mYlow("pdfGaussian_mXlow_mYlow", "pdfGaussian_mXlow_mYlow", variableList, dh2Gaussian_mXlow_mYlow );

	TH2F* histGaussian_mXlow_mYmed = new TH2F("histGaussian_mXlow_mYmed", "histGaussian_mXlow_mYmed", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXlow_mYmed->Fill(gRandom->Gaus(mXlow, mXlowSigma), gRandom->Gaus(mXmed, mXmedSigma));
	RooDataHist dh2Gaussian_mXlow_mYmed("dh2Gaussian_mXlow_mYlow", "dh2Gaussian_mXlow_mYlow", variableList, histGaussian_mXlow_mYlow);
	RooHistPdf  pdfGaussian_mXlow_mYmed("pdfGaussian_mXlow_mYmed", "pdfGaussian_mXlow_mYmed", variableList, dh2Gaussian_mXlow_mYmed );

	TH2F* histGaussian_mXmed_mYlow = new TH2F("histGaussian_mXmed_mYlow", "histGaussian_mXmed_mYlow", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXmed_mYlow->Fill(gRandom->Gaus(mXmed, mXmedSigma), gRandom->Gaus(mXlow, mXlowSigma));
	RooDataHist dh2Gaussian_mXmed_mYlow("dh2Gaussian_mXmed_mYlow", "dh2Gaussian_mXmed_mYlow", variableList, histGaussian_mXmed_mYlow);
	RooHistPdf  pdfGaussian_mXmed_mYlow("pdfGaussian_mXmed_mYlow", "pdfGaussian_mXmed_mYlow", variableList, dh2Gaussian_mXmed_mYlow );

	TH2F* histGaussian_mXlow_mYhigh = new TH2F("histGaussian_mXlow_mYhigh", "histGaussian_mXlow_mYhigh", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXlow_mYhigh->Fill(gRandom->Gaus(mXlow, mXlowSigma), gRandom->Gaus(mXhigh, mXhighSigma));
	RooDataHist dh2Gaussian_mXlow_mYhigh("dh2Gaussian_mXlow_mYhigh", "dh2Gaussian_mXlow_mYhigh", variableList, histGaussian_mXlow_mYhigh);
	RooHistPdf  pdfGaussian_mXlow_mYhigh("pdfGaussian_mXlow_mYhigh", "pdfGaussian_mXlow_mYhigh", variableList, dh2Gaussian_mXlow_mYhigh );

	TH2F* histGaussian_mXmed_mYhigh = new TH2F("histGaussian_mXmed_mYhigh", "histGaussian_mXmed_mYhigh", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXmed_mYhigh->Fill(gRandom->Gaus(mXmed, mXmedSigma), gRandom->Gaus(mXhigh, mXhighSigma));
	RooDataHist dh2Gaussian_mXmed_mYhigh("dh2Gaussian_mXmed_mYhigh", "dh2Gaussian_mXmed_mYhigh", variableList, histGaussian_mXmed_mYhigh);
	RooHistPdf  pdfGaussian_mXmed_mYhigh("pdfGaussian_mXmed_mYhigh", "pdfGaussian_mXmed_mYhigh", variableList, dh2Gaussian_mXmed_mYhigh );

	TH2F* histGaussian_mXhigh_mYmed = new TH2F("histGaussian_mXhigh_mYmed", "histGaussian_mXhigh_mYmed", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXhigh_mYmed->Fill(gRandom->Gaus(mXhigh, mXhighSigma), gRandom->Gaus(mXmed, mXmedSigma));
	RooDataHist dh2Gaussian_mXhigh_mYmed("dh2Gaussian_mXhigh_mYmed", "dh2Gaussian_mXhigh_mYmed", variableList, histGaussian_mXhigh_mYmed);
	RooHistPdf  pdfGaussian_mXhigh_mYmed("pdfGaussian_mXhigh_mYmed", "pdfGaussian_mXhigh_mYmed", variableList, dh2Gaussian_mXhigh_mYmed );

	TH2F* histGaussian_mXmed_mYmed = new TH2F("histGaussian_mXmed_mYmed", "histGaussian_mXmed_mYmed", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXmed_mYmed->Fill(gRandom->Gaus(mXmed, mXmedSigma), gRandom->Gaus(mXmed, mXmedSigma));
	RooDataHist dh2Gaussian_mXmed_mYmed("dh2Gaussian_mXmed_mYmed", "dh2Gaussian_mXmed_mYmed", variableList, histGaussian_mXmed_mYmed);
	RooHistPdf  pdfGaussian_mXmed_mYmed("pdfGaussian_mXmed_mYmed", "pdfGaussian_mXmed_mYmed", variableList, dh2Gaussian_mXmed_mYmed );

	TH2F* histGaussian_mXhigh_mYlow = new TH2F("histGaussian_mXhigh_mYlow", "histGaussian_mXhigh_mYlow", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXhigh_mYlow->Fill(gRandom->Gaus(mXhigh, mXhighSigma), gRandom->Gaus(mXlow, mXlowSigma));
	RooDataHist dh2Gaussian_mXhigh_mYlow("dh2Gaussian_mXhigh_mYlow", "dh2Gaussian_mXhigh_mYlow", variableList, histGaussian_mXhigh_mYlow);
	RooHistPdf  pdfGaussian_mXhigh_mYlow("pdfGaussian_mXhigh_mYlow", "pdfGaussian_mXhigh_mYlow", variableList, dh2Gaussian_mXhigh_mYlow );

	TH2F* histGaussian_mXhigh_mYhigh = new TH2F("histGaussian_mXhigh_mYhigh", "histGaussian_mXhigh_mYhigh", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXhigh_mYhigh->Fill(gRandom->Gaus(mXhigh, mXhighSigma), gRandom->Gaus(mXhigh, mXhighSigma));
	RooDataHist dh2Gaussian_mXhigh_mYhigh("dh2Gaussian_mXhigh_mYhigh", "dh2Gaussian_mXhigh_mYhigh", variableList, histGaussian_mXhigh_mYhigh);
	RooHistPdf  pdfGaussian_mXhigh_mYhigh("pdfGaussian_mXhigh_mYhigh", "pdfGaussian_mXhigh_mYhigh", variableList, dh2Gaussian_mXhigh_mYhigh );

	RooBinning binningX(numberOfGridBins, mXlow, mXhigh);
	RooBinning binningY(numberOfGridBins, mXlow, mXhigh);
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

    theGrid.addPdf(pdfGaussian_mXlow_mYlow  , 0, 0);
    theGrid.addPdf(pdfGaussian_mXlow_mYhigh  , 0, 1);
    theGrid.addPdf(pdfGaussian_mXhigh_mYlow  , 1, 0);
    theGrid.addPdf(pdfGaussian_mXhigh_mYhigh  , 1, 1);

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
	RooRealVar alphaTargetX("alphaTargetX", "alphaTargetX", 0., 400.);
	alphaTargetX.setVal(mXtarget);
	alphaTargetList.add(alphaTargetX);
	RooRealVar alphaTargetY("alphaTargetY", "alphaTargetY", 0., 400.);
	alphaTargetY.setVal(mYtarget);
	alphaTargetList.add(alphaTargetY);

	std::cout<< __PRETTY_FUNCTION__ << __LINE__ << std::endl;
	RooMomentMorphND gaussian_mXmean_mYmean("morph", "morph", alphaTargetList, variableList, theGrid, RooMomentMorphND::Linear);
	std::cout<< __PRETTY_FUNCTION__ << __LINE__ << std::endl;
	gaussian_mXmean_mYmean.useHorizontalMorphing(true);
	std::cout<< __PRETTY_FUNCTION__ << __LINE__ << std::endl;

	TH2F* histGaussian_mXmean_mYmean = new TH2F("histGaussian_mXmean_mYmean", "histGaussian_mXmean_mYmean", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	std::cout<< __PRETTY_FUNCTION__ << __LINE__ << std::endl;
	gaussian_mXmean_mYmean.fillHistogram(histGaussian_mXmean_mYmean,variableList);
	std::cout<< __PRETTY_FUNCTION__ << __LINE__ << std::endl;

	histGaussian_mXmean_mYmean->Scale(entriesNumber);
	histGaussian_mXmean_mYmean->SetMarkerColor(kRed);

	gROOT->SetBatch(true);
    TCanvas c1;
    histGaussian_mXmean_mYmean->Draw(      );
    histGaussian_mXlow_mYlow  ->Draw("same");
    // histGaussian_mXmed_mYlow  ->Draw("same");
    // histGaussian_mXlow_mYmed  ->Draw("same");
    histGaussian_mXlow_mYhigh ->Draw("same");
    // histGaussian_mXmed_mYhigh ->Draw("same");
    // histGaussian_mXhigh_mYmed ->Draw("same");
    // histGaussian_mXmed_mYmed ->Draw("same");
    histGaussian_mXhigh_mYlow ->Draw("same");
    histGaussian_mXhigh_mYhigh->Draw("same");
	c1.SaveAs("testHist2D2D.pdf");
	gROOT->SetBatch(false);

	return histGaussian_mXmean_mYmean->GetMean(2);
}

int main(int argc, char** argv)
{
	ROOT::EnableThreadSafety();
    gSystem->ResetSignal(kSigSegmentationViolation, kTRUE);

	if(argc == 1) return EXIT_FAILURE;

    cout<<argv[2]<<endl;
	TestInterpolatorHist2D2D(atoi(argv[1]), atof(argv[2]), atof(argv[3]));

	return EXIT_SUCCESS;
}

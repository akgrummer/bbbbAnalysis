#include "RooWorkspace.h"
#include "RooPlot.h"
#include "RooRealVar.h"
#include "RooArgList.h"
#include "TVectorD.h"
#include "RooMomentMorphND_local.h"
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

float TestInterpolatorHist2D2D(int numberOfGridBins=1, float mXtarget=200., float mYtarget=200.)
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
	float mXmean      = 175.;
	float mXmeanSigma = mXmean/10.;
	float mXhigh      = 300.;
	float mXhighSigma = mXhigh/10.;

	TH2F* histGaussian_mXlow_mYlow = new TH2F("histGaussian_mXlow_mYlow", "histGaussian_mXlow_mYlow", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXlow_mYlow->Fill(gRandom->Gaus(mXlow, mXlowSigma), gRandom->Gaus(mXlow, mXlowSigma));
	RooDataHist dh2Gaussian_mXlow_mYlow("dh2Gaussian_mXlow_mYlow", "dh2Gaussian_mXlow_mYlow", variableList, histGaussian_mXlow_mYlow);
	RooHistPdf  pdfGaussian_mXlow_mYlow("pdfGaussian_mXlow_mYlow", "pdfGaussian_mXlow_mYlow", variableList, dh2Gaussian_mXlow_mYlow );
	RooRealVar normGaussian_mXlow_mYlow("normGaussian_mXlow_mYlow", "normGaussian_mXlow_mYlow", 0.5 * entriesNumber, 1.5 * entriesNumber);
	RooAddPdf gaussian_mXlow_mYlow("gaussian_mXlow_mYlow", "gaussian_mXlow_mYlow", RooArgList(pdfGaussian_mXlow_mYlow), RooArgList(normGaussian_mXlow_mYlow));

	TH2F* histGaussian_mXlow_mYhigh = new TH2F("histGaussian_mXlow_mYhigh", "histGaussian_mXlow_mYhigh", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXlow_mYhigh->Fill(gRandom->Gaus(mXlow, mXlowSigma), gRandom->Gaus(mXhigh, mXhighSigma));
	RooDataHist dh2Gaussian_mXlow_mYhigh("dh2Gaussian_mXlow_mYhigh", "dh2Gaussian_mXlow_mYhigh", variableList, histGaussian_mXlow_mYhigh);
	RooHistPdf  pdfGaussian_mXlow_mYhigh("pdfGaussian_mXlow_mYhigh", "pdfGaussian_mXlow_mYhigh", variableList, dh2Gaussian_mXlow_mYhigh );
	RooRealVar normGaussian_mXlow_mYhigh("normGaussian_mXlow_mYhigh", "normGaussian_mXlow_mYhigh", 0.5 * entriesNumber, 1.5 * entriesNumber);
	RooAddPdf gaussian_mXlow_mYhigh("gaussian_mXlow_mYhigh", "gaussian_mXlow_mYhigh", RooArgList(pdfGaussian_mXlow_mYhigh), RooArgList(normGaussian_mXlow_mYhigh));


	TH2F* histGaussian_mXhigh_mYlow = new TH2F("histGaussian_mXhigh_mYlow", "histGaussian_mXhigh_mYlow", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXhigh_mYlow->Fill(gRandom->Gaus(mXhigh, mXhighSigma), gRandom->Gaus(mXlow, mXlowSigma));
	RooDataHist dh2Gaussian_mXhigh_mYlow("dh2Gaussian_mXhigh_mYlow", "dh2Gaussian_mXhigh_mYlow", variableList, histGaussian_mXhigh_mYlow);
	RooHistPdf  pdfGaussian_mXhigh_mYlow("pdfGaussian_mXhigh_mYlow", "pdfGaussian_mXhigh_mYlow", variableList, dh2Gaussian_mXhigh_mYlow );
	RooRealVar normGaussian_mXhigh_mYlow("normGaussian_mXhigh_mYlow", "normGaussian_mXhigh_mYlow", 0.5 * entriesNumber, 1.5 * entriesNumber);
	RooAddPdf gaussian_mXhigh_mYlow("gaussian_mXhigh_mYlow", "gaussian_mXhigh_mYlow", RooArgList(pdfGaussian_mXhigh_mYlow), RooArgList(normGaussian_mXhigh_mYlow));

	TH2F* histGaussian_mXhigh_mYhigh = new TH2F("histGaussian_mXhigh_mYhigh", "histGaussian_mXhigh_mYhigh", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussian_mXhigh_mYhigh->Fill(gRandom->Gaus(mXhigh, mXhighSigma), gRandom->Gaus(mXhigh, mXhighSigma));
	RooDataHist dh2Gaussian_mXhigh_mYhigh("dh2Gaussian_mXhigh_mYhigh", "dh2Gaussian_mXhigh_mYhigh", variableList, histGaussian_mXhigh_mYhigh);
	RooHistPdf  pdfGaussian_mXhigh_mYhigh("pdfGaussian_mXhigh_mYhigh", "pdfGaussian_mXhigh_mYhigh", variableList, dh2Gaussian_mXhigh_mYhigh );
	RooRealVar normGaussian_mXhigh_mYhigh("normGaussian_mXhigh_mYhigh", "normGaussian_mXhigh_mYhigh", 0.5 * entriesNumber, 1.5 * entriesNumber);
	RooAddPdf gaussian_mXhigh_mYhigh("gaussian_mXhigh_mYhigh", "gaussian_mXhigh_mYhigh", RooArgList(pdfGaussian_mXhigh_mYhigh), RooArgList(normGaussian_mXhigh_mYhigh));

	RooBinning binningX(numberOfGridBins, mXlow, mXhigh);
	RooBinning binningY(numberOfGridBins, mXlow, mXhigh);

	RooMomentMorphND_local::Grid theGrid(binningX,binningY);
	theGrid.addPdf(gaussian_mXlow_mYlow  ,                0,                0);
	theGrid.addPdf(gaussian_mXlow_mYhigh ,                0, numberOfGridBins);
	theGrid.addPdf(gaussian_mXhigh_mYlow , numberOfGridBins,                0);
	theGrid.addPdf(gaussian_mXhigh_mYhigh, numberOfGridBins, numberOfGridBins);

	RooArgList alphaTargetList;
	RooRealVar alphaTargetX("alphaTargetX", "alphaTargetX", 0., 400.);
	alphaTargetX.setVal(mXtarget);
	alphaTargetList.add(alphaTargetX);
	RooRealVar alphaTargetY("alphaTargetY", "alphaTargetY", 0., 400.);
	alphaTargetY.setVal(mYtarget);
	alphaTargetList.add(alphaTargetY);

	std::cout<< __PRETTY_FUNCTION__ << __LINE__ << std::endl;
	RooMomentMorphND_local gaussian_mXmean_mYmean("morph", "morph", alphaTargetList, variableList, theGrid, RooMomentMorphND_local::Linear);
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
    histGaussian_mXlow_mYhigh ->Draw("same");
    histGaussian_mXhigh_mYlow ->Draw("same");
    histGaussian_mXhigh_mYhigh->Draw("same");
	c1.SaveAs("testHist2D2D.pdf");
	gROOT->SetBatch(false);

	return histGaussian_mXmean_mYmean->GetMean(2);
}

void scanTest()
{
	std::map<float,std::vector<std::pair<float, float>>> massValues;

	for(int xMass = 50; xMass <=300; xMass+=50)
	{
		massValues[xMass] = std::vector<std::pair<float, float>>();
		// std::cout<< "X mass = " << xMass << std::endl;
		for(int yMass = 50; yMass <=300; yMass+=50)
		{
			// std::cout<<  yMass << "\t" << TestInterpolatorHist2D2D(xMass, yMass) << std::endl;
			massValues[xMass].push_back(std::make_pair<float,float>(yMass,TestInterpolatorHist2D2D(xMass, yMass)));
		}
	}

	for(const auto& xMassPoint : massValues)
	{
		std::cout<< "X mass = " << xMassPoint.first << std::endl;
		for(const auto& yMassPoint : xMassPoint.second)
		{
			std::cout<< yMassPoint.first << "\t" << yMassPoint.second << std::endl;
		}
	}

	return;
}

int main(int argc, char** argv)
{
	ROOT::EnableThreadSafety();
    gSystem->ResetSignal(kSigSegmentationViolation, kTRUE);

	if(argc !=2) return EXIT_FAILURE;

	TestInterpolatorHist2D2D(atoi(argv[1]));

	return EXIT_SUCCESS;
}

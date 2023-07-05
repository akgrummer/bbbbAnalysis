#include "RooWorkspace.h"
#include "RooPlot.h"
#include "RooRealVar.h"
#include "RooArgList.h"
#include "TVectorD.h"
#include "RooMomentMorph.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TH1D.h"
#include "RooDataHist.h"
#include "RooHistPdf.h"
#include "RooAddPdf.h"
#include "TRandom.h"
#include "TSystem.h"

using namespace RooFit;

void TestInterpolatorHist()
{
	float mXrecoMin =   0.;
	float mXrecoMax = 400.;
	int entriesNumber = 5000;
	int numberOfBins  = 50;

	RooRealVar mXreco("mXreco", "m_{Xreco}", 0., 400., "GeV");

	TH1D* histGaussianAlpha0 = new TH1D("histGaussianAlpha0", "histGaussianAlpha0", numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussianAlpha0->Fill(gRandom->Gaus(50., 15.));
	RooDataHist dh1GaussianAlpha0("dh1GaussianAlpha0", "dh1GaussianAlpha0", mXreco, histGaussianAlpha0);
	RooHistPdf  pdfGaussianAlpha0("pdfGaussianAlpha0", "pdfGaussianAlpha0", mXreco, dh1GaussianAlpha0 );
	RooRealVar normGaussianAlpha0("normGaussianAlpha0", "normGaussianAlpha0", 0.5 * entriesNumber, 1.5 * entriesNumber);
	RooAddPdf gaussianAlpha0("gaussianAlpha0", "gaussianAlpha0", RooArgList(pdfGaussianAlpha0), RooArgList(normGaussianAlpha0));

	TH1D* histGaussianAlpha1 = new TH1D("histGaussianAlpha1", "histGaussianAlpha1", numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussianAlpha1->Fill(gRandom->Gaus(300., 40.));
	RooDataHist dh1GaussianAlpha1("dh1GaussianAlpha1", "dh1GaussianAlpha1", mXreco, histGaussianAlpha1);
	RooHistPdf  pdfGaussianAlpha1("pdfGaussianAlpha1", "pdfGaussianAlpha1", mXreco, dh1GaussianAlpha1 );
	RooRealVar normGaussianAlpha1("normGaussianAlpha1", "normGaussianAlpha1", 0.5 * entriesNumber, 1.5 * entriesNumber);
	RooAddPdf gaussianAlpha1("gaussianAlpha1", "gaussianAlpha1", RooArgList(pdfGaussianAlpha1), RooArgList(normGaussianAlpha1));


	RooArgList pdfs;
	RooArgList parameters; //will be the mass points

	//Addind gaussian 0 which corresponds to alpha 0
	pdfs.add(gaussianAlpha0);
	RooRealVar alphaMin("alphaMin", "alphaMin", 0., 1.);
	alphaMin.setVal(0);
	parameters.add(alphaMin);

	//Addind gaussian 1 which corresponds to alpha 1
	pdfs.add(gaussianAlpha1);
	RooRealVar alphaMax("alphaMax", "alphaMax", 0., 1.);
	alphaMax.setVal(1);
	parameters.add(alphaMax);

	RooRealVar alphaTarget("alphaTarget", "alphaTarget", 0., 1.);
	alphaTarget.setVal(0.5);

	RooArgList variableList;
	variableList.add(mXreco);
	RooMomentMorph gaussianAlpha05("morph","morph",alphaTarget,variableList,pdfs, parameters,RooMomentMorph::Linear);
	TH1D* histGaussianAlpha05 = new TH1D("histGaussianAlpha05", "histGaussianAlpha05", numberOfBins, mXrecoMin, mXrecoMax);
	gaussianAlpha05.fillHistogram(histGaussianAlpha05, mXreco, entriesNumber);
    histGaussianAlpha05->SetLineColor(kRed);

	gROOT->SetBatch(true);
    TCanvas c1;
    histGaussianAlpha0 ->Draw() ;
    histGaussianAlpha1 ->Draw("same") ;
    histGaussianAlpha05->Draw("same hist") ;
	c1.SaveAs("testHist.pdf");
	gROOT->SetBatch(false);

}

int main(int argc, char** argv)
{
	ROOT::EnableThreadSafety();
    gSystem->ResetSignal(kSigSegmentationViolation, kTRUE);

	TestInterpolatorHist();

	return EXIT_SUCCESS;
}


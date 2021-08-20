#include "RooWorkspace.h"
#include "RooPlot.h"
#include "RooRealVar.h"
#include "RooArgList.h"
#include "TVectorD.h"
#include "RooMomentMorph.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TH2D.h"
#include "RooDataHist.h"
#include "RooHistPdf.h"
#include "RooAddPdf.h"
#include "TRandom.h"

using namespace RooFit;

void TestInterpolatorHist2D()
{
	float mXrecoMin =   0.;
	float mXrecoMax = 400.;
	int entriesNumber = 5000;
	int numberOfBins  = 50;

	RooRealVar mXreco("mXreco", "m_{Xreco}", mXrecoMin, mXrecoMax, "GeV");
	RooRealVar mYreco("mYreco", "m_{Yreco}", mXrecoMin, mXrecoMax, "GeV");

	RooArgList variableList;
	variableList.add(mXreco);
	variableList.add(mYreco);


	TH2D* histGaussianAlpha0 = new TH2D("histGaussianAlpha0", "histGaussianAlpha0", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussianAlpha0->Fill(gRandom->Gaus(50., 15.), gRandom->Gaus(50., 15.));
	RooDataHist dh2GaussianAlpha0("dh2GaussianAlpha0", "dh2GaussianAlpha0", variableList, histGaussianAlpha0);
	RooHistPdf  pdfGaussianAlpha0("pdfGaussianAlpha0", "pdfGaussianAlpha0", variableList, dh2GaussianAlpha0 );
	RooRealVar normGaussianAlpha0("normGaussianAlpha0", "normGaussianAlpha0", 0.5 * entriesNumber, 1.5 * entriesNumber);
	RooAddPdf gaussianAlpha0("gaussianAlpha0", "gaussianAlpha0", RooArgList(pdfGaussianAlpha0), RooArgList(normGaussianAlpha0));

	TH2D* histGaussianAlpha1 = new TH2D("histGaussianAlpha1", "histGaussianAlpha1", numberOfBins, mXrecoMin, mXrecoMax, numberOfBins, mXrecoMin, mXrecoMax);
	for (int i = 0; i < entriesNumber; ++i) histGaussianAlpha1->Fill(gRandom->Gaus(300., 40.), gRandom->Gaus(300., 40.));
	RooDataHist dh2GaussianAlpha1("dh2GaussianAlpha1", "dh2GaussianAlpha1", variableList, histGaussianAlpha1);
	RooHistPdf  pdfGaussianAlpha1("pdfGaussianAlpha1", "pdfGaussianAlpha1", variableList, dh2GaussianAlpha1 );
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

	RooMomentMorph gaussianAlpha05("morph","morph",alphaTarget,variableList,pdfs, parameters,RooMomentMorph::Linear);
    TH2D *histGaussianAlpha05 = (TH2D*)gaussianAlpha05.createHistogram("mXreco:mYreco", numberOfBins, numberOfBins);
	histGaussianAlpha05->Scale(entriesNumber);
	histGaussianAlpha05->SetMarkerColor(kRed);
    
	gROOT->SetBatch(true);
    TCanvas c1;
    histGaussianAlpha0 ->Draw() ;
    histGaussianAlpha1 ->Draw("same") ;
    histGaussianAlpha05->Draw("same hist") ;
	c1.SaveAs("testHist2D.pdf");
	gROOT->SetBatch(false);

}
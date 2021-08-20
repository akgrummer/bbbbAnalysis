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

using namespace RooFit;

std::string getPlotName(int mX, int mY)
{
    std::string plotName = "sig_NMSSM_bbbb_MX_" + std::to_string(mX) + "_MY_" + std::to_string(mY) + "/selectionbJets_SignalRegion/sig_NMSSM_bbbb_MX_" + std::to_string(mX) + "_MY_" + std::to_string(mY) + "_selectionbJets_SignalRegion_HH_kinFit_m_H2_m";
    return plotName;
}

template<typename Hist>
Hist* getHistogramFromFile(TFile& inputFile, std::string histogramName)
{
    Hist* histogram = (Hist*)inputFile.Get(histogramName.data());
    if(histogram == nullptr)
    {
        std::cout<< "Histogram " << histogramName << " does not exist" << std::endl;
        return nullptr;
    }
    histogram->SetDirectory(0);

    return histogram;
}

void TestInterpolatorHist2D2DReal()
{
	int year=2016;
	int plotVersion=21;
	int mXtestPoint=700;
	int mYtestPoint=300;
    std::string plotInputFileName  = "../DataPlots_fullSubmission_" + std::to_string(year) + "_v" + std::to_string(plotVersion) + "/outPlotter.root";
    TFile plotInputFile(plotInputFileName.data());
	
	float mXrecoMin =   0.;
	float mXrecoMax = 2500.;

	RooRealVar mXreco("mXreco", "m_{Xreco}", mXrecoMin, mXrecoMax, "GeV");
	RooRealVar mYreco("mYreco", "m_{Yreco}", mXrecoMin, mXrecoMax, "GeV");

	RooArgList variableList;
	variableList.add(mXreco);
	variableList.add(mYreco);

	TH2F* histGaussianAlpha0_0 = getHistogramFromFile<TH2F>(plotInputFile,getPlotName(1000,200));
	histGaussianAlpha0_0->Scale(1./histGaussianAlpha0_0->Integral());
	RooDataHist dh2GaussianAlpha0_0("dh2GaussianAlpha0_0", "dh2GaussianAlpha0_0", variableList, histGaussianAlpha0_0);
	RooHistPdf  pdfGaussianAlpha0_0("pdfGaussianAlpha0_0", "pdfGaussianAlpha0_0", variableList, dh2GaussianAlpha0_0 );
	RooRealVar normGaussianAlpha0_0("normGaussianAlpha0_0", "normGaussianAlpha0_0", 0.5, 1.5);
	RooAddPdf gaussianAlpha0_0("gaussianAlpha0_0", "gaussianAlpha0_0", RooArgList(pdfGaussianAlpha0_0), RooArgList(normGaussianAlpha0_0));

	TH2F* histGaussianAlpha0_1 = getHistogramFromFile<TH2F>(plotInputFile,getPlotName(1000,800));
	histGaussianAlpha0_1->Scale(1./histGaussianAlpha0_1->Integral());
	RooDataHist dh2GaussianAlpha0_1("dh2GaussianAlpha0_1", "dh2GaussianAlpha0_1", variableList, histGaussianAlpha0_1);
	RooHistPdf  pdfGaussianAlpha0_1("pdfGaussianAlpha0_1", "pdfGaussianAlpha0_1", variableList, dh2GaussianAlpha0_1 );
	RooRealVar normGaussianAlpha0_1("normGaussianAlpha0_1", "normGaussianAlpha0_1", 0.5, 1.5);
	RooAddPdf gaussianAlpha0_1("gaussianAlpha0_1", "gaussianAlpha0_1", RooArgList(pdfGaussianAlpha0_0), RooArgList(normGaussianAlpha0_0));


	TH2F* histGaussianAlpha1_0 = getHistogramFromFile<TH2F>(plotInputFile,getPlotName(2000,200));
	histGaussianAlpha1_0->Scale(1./histGaussianAlpha1_0->Integral());
	RooDataHist dh2GaussianAlpha1_0("dh2GaussianAlpha1_0", "dh2GaussianAlpha1_0", variableList, histGaussianAlpha1_0);
	RooHistPdf  pdfGaussianAlpha1_0("pdfGaussianAlpha1_0", "pdfGaussianAlpha1_0", variableList, dh2GaussianAlpha1_0 );
	RooRealVar normGaussianAlpha1_0("normGaussianAlpha1_0", "normGaussianAlpha1_0", 0.5, 1.5);
	RooAddPdf gaussianAlpha1_0("gaussianAlpha1_0", "gaussianAlpha1_0", RooArgList(pdfGaussianAlpha1_0), RooArgList(normGaussianAlpha1_0));

	TH2F* histGaussianAlpha1_1 = getHistogramFromFile<TH2F>(plotInputFile,getPlotName(2000,800));
	histGaussianAlpha1_1->Scale(1./histGaussianAlpha1_1->Integral());
	RooDataHist dh2GaussianAlpha1_1("dh2GaussianAlpha1_1", "dh2GaussianAlpha1_1", variableList, histGaussianAlpha1_1);
	RooHistPdf  pdfGaussianAlpha1_1("pdfGaussianAlpha1_1", "pdfGaussianAlpha1_1", variableList, dh2GaussianAlpha1_1 );
	RooRealVar normGaussianAlpha1_1("normGaussianAlpha1_1", "normGaussianAlpha1_1", 0.5, 1.5);
	RooAddPdf gaussianAlpha1_1("gaussianAlpha1_1", "gaussianAlpha1_1", RooArgList(pdfGaussianAlpha1_1), RooArgList(normGaussianAlpha1_1));

	RooRealVar alphaTargetX("alphaTargetX", "alphaTargetX", 0., 2000.);
	alphaTargetX.setVal(1500.);
	RooRealVar alphaTargetY("alphaTargetY", "alphaTargetY", 0., 2000.);
	alphaTargetY.setVal(500.);

	RooBinning binningX(1, 1000, 2000);
	RooBinning binningY(1, 200, 800);

	RooMomentMorphND::Grid theGrid(binningX,binningY);
	theGrid.addPdf(gaussianAlpha0_0, 0, 0);
	theGrid.addPdf(gaussianAlpha0_1, 0, 1);
	theGrid.addPdf(gaussianAlpha1_0, 1, 0);
	theGrid.addPdf(gaussianAlpha1_1, 1, 1);

	RooArgList alphaTargetList;
	alphaTargetList.add(alphaTargetX);
	alphaTargetList.add(alphaTargetY);

	RooMomentMorphND gaussianAlpha05_05("morph", "morph", alphaTargetList, variableList, theGrid, RooMomentMorphND::Linear);
	gaussianAlpha05_05.useHorizontalMorphing(true);

	TH2F* theInterpolatedPlot = static_cast<TH2F*>(histGaussianAlpha0_0->Clone("InterlatedPlot"));
	theInterpolatedPlot->SetDirectory(0);
	theInterpolatedPlot->Reset("ICES");

	gaussianAlpha05_05.fillHistogram(theInterpolatedPlot, variableList);
	theInterpolatedPlot->Scale(0.1/theInterpolatedPlot->Integral());
	theInterpolatedPlot->SetMarkerColor(kRed);
    
	gROOT->SetBatch(true);
    TCanvas c1;
    histGaussianAlpha0_0 ->Scale(0.1);
	histGaussianAlpha0_0 ->SetMarkerColor(kBlue);
    histGaussianAlpha0_0 ->Draw() ;
	histGaussianAlpha0_1 ->Scale(0.1);
	histGaussianAlpha0_1 ->SetMarkerColor(kGreen);
    histGaussianAlpha0_1 ->Draw("same") ;
	histGaussianAlpha1_0 ->Scale(0.1);
	histGaussianAlpha1_0 ->SetMarkerColor(kOrange);
    histGaussianAlpha1_0 ->Draw("same") ;
	histGaussianAlpha1_1 ->Scale(0.1);
	histGaussianAlpha1_1 ->SetMarkerColor(kViolet);
    histGaussianAlpha1_1 ->Draw("same") ;
    theInterpolatedPlot  ->Draw("same") ;
	c1.SaveAs("testHist2D2DReal.pdf");
	gROOT->SetBatch(false);

}
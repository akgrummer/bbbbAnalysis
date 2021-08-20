#include "RooWorkspace.h"
#include "RooPlot.h"
#include "RooRealVar.h"
#include "RooArgList.h"
#include "TVectorD.h"
#include "RooMomentMorph.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "TROOT.h"

using namespace RooFit;

void TestInterpolator2(){
	RooRealVar mXreco("mXreco", "m_{Xreco}", 0., 400., "GeV");
	RooRealVar mean1("mean1", "mean1", 50., 50.);
	mean1.setVal(50.);
	RooRealVar sigma1("sigma1", "sigma1", 15., 15.);
	sigma1.setVal(15.);
	RooGaussian gaussianAlpha0("gaussianAlpha0","gaussianAlpha0", mXreco, mean1, sigma1);

	RooRealVar mean2("mean2", "mean2", 300., 300.);
	mean2.setVal(300.);
	RooRealVar sigma2("sigma2", "sigma2", 40., 40.);
	sigma2.setVal(40.);
	RooGaussian gaussianAlpha1("gaussianAlpha1","gaussianAlpha1", mXreco, mean2, sigma2);

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
    RooPlot* frame = mXreco.frame();
    gaussianAlpha0 .plotOn(frame,LineColor(kBlue),LineStyle(kSolid));
    gaussianAlpha1 .plotOn(frame,LineColor(kBlue),LineStyle(kSolid));
    gaussianAlpha05.plotOn(frame,LineColor(kRed) ,LineStyle(kDashed));

	gROOT->SetBatch(true);
    TCanvas c1;
    frame->Draw() ;
	c1.SaveAs("test2.pdf");
	gROOT->SetBatch(false);

}
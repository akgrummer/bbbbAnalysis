#include "RooWorkspace.h"
#include "RooPlot.h"
#include "RooRealVar.h"
#include "RooArgList.h"
#include "TVectorD.h"
#include "RooMomentMorph.h"
#include "TCanvas.h"

using namespace RooFit;

void TestInterpolator(){
	// //	#Make statistical model
	// RooWorkspace* w = new RooWorkspace("w");
	// w->factory("Exponential::e(x[-5,15],tau[-.15,-3,0])");
    // RooRealVar* x = w->var("x");
	// w->factory("mu[0,10]");
	// RooRealVar* mu = w->var("mu");
	// RooPlot* frame = x->frame();
	// RooArgList pdfs;
	// TVectorD paramVec =	TVectorD(5);
	// for(int i=0; i<5; ++i){
	// 	w->factory(Form("Gaussian::g%d(x,mu%d[%d,-3,5],sigma[0.5, 0, 2])", i, i,i));
	// 	w->factory(Form("SUM::model%d(s[50,0,100]*g%d,b[100,0,1000]*e)",i,i));
	// 	w->Print() ;
    //     RooAbsPdf* pdf = w->pdf(Form("model%d",i));
	// 	pdf->plotOn(frame);
	// 	pdfs.add(*pdf);
	// 	paramVec[i]=i;
	// }
	// pdfs.Print();
	// RooRealVar* mu2 = w->var("mu");
	// RooArgList varlist;
	// varlist.add(*x);
	// RooMomentMorph* morph = new RooMomentMorph("morph","morph",*mu2,varlist,pdfs, paramVec,RooMomentMorph::Linear);

	// w->import(*morph);
	// morph->Print("v");

	// w->Print();

	// for (int i=0; i<5; ++i){
	// 	mu2->setVal(.8+i);
	// 	mu2->Print();
	// 	morph->plotOn(frame, RooFit::LineColor(kRed));
	// }
    // TCanvas c1;
	// frame->Draw();
	// c1.SaveAs("test.pdf");

	RooWorkspace* w = new RooWorkspace("w", 1);
    w->factory("RooGaussian::gaussian1(obs[0,400],50,15)");
    RooAbsPdf* gaussian1 = w->pdf("gaussian1");
    w->factory("RooGaussian::gaussian2(obs,300,40)");
    RooAbsPdf* gaussian2 = w->pdf("gaussian2");
    w->factory("RooMomentMorph::morphpdf(alpha[0,1],obs,{gaussian1,gaussian2},{0,1})");

    RooRealVar* alpha = w->var("alpha");
    alpha->setVal(0.5);
    RooAbsPdf* morphpdf = w->pdf("morphpdf");

    RooRealVar* obs = w->var("obs");
    RooPlot* frame = obs->frame();

    gaussian1->plotOn(frame,LineColor(kBlue),LineStyle(kSolid));
    gaussian2->plotOn(frame,LineColor(kBlue),LineStyle(kSolid));
    morphpdf ->plotOn(frame,LineColor(kRed),LineStyle(kDashed));
    TCanvas c1;
    frame->Draw() ;
	c1.SaveAs("test.pdf");

}
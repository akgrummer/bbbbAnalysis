#include "RooWorkspace.h"
#include "RooPlot.h"
#include "RooRealVar.h"
#include "RooArgList.h"
#include "TVectorD.h"
#include "RooMomentMorph.h"
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

int main(){
	//	#Make statistical model
    TCanvas *c1;
	RooWorkspace *w = new RooWorkspace("w");
	w->factory("Exponential::e(x[-5,15],tau[-.15,-3,0])");
	RooRealVar *x = w->var("x");
	w->factory("mu[0,10]");
	RooRealVar *mu = w->var("mu");
	RooPlot* frame = x->frame();
	RooArgList pdfs;
	TVectorD paramVec =	TVectorD(5);
	for(int i=0; i<5; ++i){
		w->factory(Form("Gaussian::g%d(x,mu%d[%d,-3,5],sigma[0.5, 0, 2])", i, i,i));
		w->factory(Form("SUM::model%d(s[50,0,100]*g%d,b[100,0,1000]*e)",i,i));
		w->Print() ;
		auto pdf = w->pdf(Form("model%d",i));
		pdf->plotOn(frame);
		pdfs.add(*pdf);
		paramVec[i]=i;
	}
	pdfs.Print();
	mu = w->var("mu");
	RooArgList varlist;
	varlist.add(*x);
	RooMomentMorph *morph = new RooMomentMorph("morph","morph",*mu,varlist,pdfs, paramVec,RooMomentMorph::Linear);

	w->import(*morph);
	morph->Print("v");

	w->Print();

	for (int i=0; i<5; ++i){
		mu->setVal(.8+i);
		mu->Print();
		morph->plotOn(frame, RooFit::LineColor(kRed));
	}
	frame->Draw();
	c1->SaveAs("test.pdf");

}

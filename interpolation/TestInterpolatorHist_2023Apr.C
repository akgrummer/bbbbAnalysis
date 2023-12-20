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
#include "TFile.h"
#include "TH2F.h"

using namespace RooFit;
using namespace std;

void TestInterpolatorHist(int year)
{
    TString filename = "";
    TString ofilename = "";
    TString sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","900","150");
    TString sigRegion  = "selectionbJets_SignalRegion";
    TString varname = "HH_kinFit_m_H2_m";

    // get the 2d mX vs mY to reference the mX binning
    TString tag;
    tag.Form("%dDataPlots_2023Dec7_binMYx2_addMX650_10ev",year);
    // filename.Form("../VarPlots/rootHists/fullSubmission_2022Nov/%dDataPlots_2023Feb28_3/outPlotter.root", year);
    filename = "../VarPlots/rootHists/fullSubmission_2022Nov/"+tag+"/outPlotter.root";
    TFile *ifileref = new TFile( filename, "READ");
    TH2F *ref2D=(TH2F*)ifileref->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname); //the actual point doesnt matter, just using binning
    cout<< ref2D->GetXaxis()->GetXmin()<< "to"<<  ref2D->GetXaxis()->GetXmax()<< endl;

    // filename.Form("interp1d/%d/outPlotter_massGroup2.root", year);
    filename = "../VarPlots/rootHists/fullSubmission_2022Nov/"+tag+"_SR/outPlotter_massGroup2.root";
    TFile *ifile = new TFile( filename, "READ");
    // ofilename.Form("hists/InterpHists_1D_nparams150_wo456%d.root", year);
    ofilename.Form("hists/InterpHists_1D_%d_2023Dec19.root", year);
    TFile *ofile = new TFile( ofilename, "RECREATE");


    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","900","150");
    TH1F *sig_low=(TH1F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname +"_Rebinned_Unrolled");
    // sig_low->Rebin(2);

    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","1100","150");
    TH1F *sig_high=(TH1F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname+"_Rebinned_Unrolled");
    // sig_high->Rebin(2);

    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","1000","150");
    TH1F *sig_real=(TH1F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname+"_Rebinned_Unrolled");

    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","400","150");
    TH1F *sig_400=(TH1F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname+"_Rebinned_Unrolled");

    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","500","150");
    TH1F *sig_500=(TH1F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname+"_Rebinned_Unrolled");

    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","600","150");
    TH1F *sig_600=(TH1F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname+"_Rebinned_Unrolled");

    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","700","150");
    TH1F *sig_700=(TH1F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname+"_Rebinned_Unrolled");

    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","800","150");
    TH1F *sig_800=(TH1F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname+"_Rebinned_Unrolled");

    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","1200","150");
    TH1F *sig_1200=(TH1F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname+"_Rebinned_Unrolled");

    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","1400","150");
    TH1F *sig_1400=(TH1F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname+"_Rebinned_Unrolled");

    sigDir =Form("sig_NMSSM_bbbb_MX_%s_MY_%s","1600","150");
    TH1F *sig_1600=(TH1F*)ifile->Get(sigDir+"/"+sigRegion+"/"+sigDir+"_"+sigRegion+"_"+varname+"_Rebinned_Unrolled");

    //--------------------------------------------------
    // variable to search for
	// RooRealVar mXreco("mXreco", "m_{Xreco}", sig_low->GetXaxis()->GetXmin(), sig_low->GetXaxis()->GetXmax(), "GeV");
	RooRealVar mXreco("mXreco", "m_{Xreco}", 0, 355, "GeV");
	RooArgList variableList;
	variableList.add(mXreco);

    cout<<"create pdfs... "<<endl;
    //--------------------------------------------------
    //Create PDFs
	RooDataHist data_sig_low("data_sig_low", "data_sig_low", mXreco, sig_low);
	RooHistPdf  pdf_low_temp("pdf_low", "pdf_low", mXreco, data_sig_low );
	RooRealVar pdf_low_norm("pdf_low_norm", "pdf_low_norm", 0.5 * sig_low->GetEntries(), 1.5 * sig_low->GetEntries());
	RooAddPdf pdf_low("pdf_low", "pdf_low", RooArgList(pdf_low_temp), RooArgList(pdf_low_norm));

	RooDataHist data_sig_high("data_sig_high", "data_sig_high", mXreco, sig_high);
	RooHistPdf  pdf_high_temp("pdf_high", "pdf_high", mXreco, data_sig_high );
	RooRealVar pdf_high_norm("pdf_high_norm", "pdf_high_norm", 0.5 * sig_high->GetEntries(), 1.5 * sig_high->GetEntries());
	RooAddPdf pdf_high("pdf_high", "pdf_high", RooArgList(pdf_high_temp), RooArgList(pdf_high_norm));

	RooDataHist data_sig_400("data_sig_400", "data_sig_400", mXreco, sig_400);
	RooHistPdf  pdf_400_temp("pdf_400", "pdf_400", mXreco, data_sig_400 );
	RooRealVar pdf_400_norm("pdf_400_norm", "pdf_400_norm", 0.5 * sig_400->GetEntries(), 1.5 * sig_400->GetEntries());
	RooAddPdf pdf_400("pdf_400", "pdf_400", RooArgList(pdf_400_temp), RooArgList(pdf_400_norm));

	RooDataHist data_sig_500("data_sig_500", "data_sig_500", mXreco, sig_500);
	RooHistPdf  pdf_500_temp("pdf_500", "pdf_500", mXreco, data_sig_500 );
	RooRealVar pdf_500_norm("pdf_500_norm", "pdf_500_norm", 0.5 * sig_500->GetEntries(), 1.5 * sig_500->GetEntries());
	RooAddPdf pdf_500("pdf_500", "pdf_500", RooArgList(pdf_500_temp), RooArgList(pdf_500_norm));

	RooDataHist data_sig_600("data_sig_600", "data_sig_600", mXreco, sig_600);
	RooHistPdf  pdf_600_temp("pdf_600", "pdf_600", mXreco, data_sig_600 );
	RooRealVar pdf_600_norm("pdf_600_norm", "pdf_600_norm", 0.5 * sig_600->GetEntries(), 1.5 * sig_600->GetEntries());
	RooAddPdf pdf_600("pdf_600", "pdf_600", RooArgList(pdf_600_temp), RooArgList(pdf_600_norm));

	RooDataHist data_sig_700("data_sig_700", "data_sig_700", mXreco, sig_700);
	RooHistPdf  pdf_700_temp("pdf_700", "pdf_700", mXreco, data_sig_700 );
	RooRealVar pdf_700_norm("pdf_700_norm", "pdf_700_norm", 0.5 * sig_700->GetEntries(), 1.5 * sig_700->GetEntries());
	RooAddPdf pdf_700("pdf_700", "pdf_700", RooArgList(pdf_700_temp), RooArgList(pdf_700_norm));

	RooDataHist data_sig_800("data_sig_800", "data_sig_800", mXreco, sig_800);
	RooHistPdf  pdf_800_temp("pdf_800", "pdf_800", mXreco, data_sig_800 );
	RooRealVar pdf_800_norm("pdf_800_norm", "pdf_800_norm", 0.5 * sig_800->GetEntries(), 1.5 * sig_800->GetEntries());
	RooAddPdf pdf_800("pdf_800", "pdf_800", RooArgList(pdf_800_temp), RooArgList(pdf_800_norm));

	RooDataHist data_sig_1200("data_sig_1200", "data_sig_1200", mXreco, sig_1200);
	RooHistPdf  pdf_1200_temp("pdf_1200", "pdf_1200", mXreco, data_sig_1200 );
	RooRealVar pdf_1200_norm("pdf_1200_norm", "pdf_1200_norm", 0.5 * sig_1200->GetEntries(), 1.5 * sig_1200->GetEntries());
	RooAddPdf pdf_1200("pdf_1200", "pdf_1200", RooArgList(pdf_1200_temp), RooArgList(pdf_1200_norm));

	RooDataHist data_sig_1400("data_sig_1400", "data_sig_1400", mXreco, sig_1400);
	RooHistPdf  pdf_1400_temp("pdf_1400", "pdf_1400", mXreco, data_sig_1400 );
	RooRealVar pdf_1400_norm("pdf_1400_norm", "pdf_1400_norm", 0.5 * sig_1400->GetEntries(), 1.5 * sig_1400->GetEntries());
	RooAddPdf pdf_1400("pdf_1400", "pdf_1400", RooArgList(pdf_1400_temp), RooArgList(pdf_1400_norm));

	RooDataHist data_sig_1600("data_sig_1600", "data_sig_1600", mXreco, sig_1600);
	RooHistPdf  pdf_1600_temp("pdf_1600", "pdf_1600", mXreco, data_sig_1600 );
	RooRealVar pdf_1600_norm("pdf_1600_norm", "pdf_1600_norm", 0.5 * sig_1600->GetEntries(), 1.5 * sig_1600->GetEntries());
	RooAddPdf pdf_1600("pdf_1600", "pdf_1600", RooArgList(pdf_1600_temp), RooArgList(pdf_1600_norm));

    cout<<"here"<<endl;
    //--------------------------------------------------
    // Add pdfs to a list (pdfs) and make a list of their mx values (parameters)
	RooArgList pdfs;
	RooArgList parameters; //will be the mass points

    // pdfs.add(pdf_400);
    // RooRealVar alpha_400("alpha_400", "alpha_400",ref2D->GetXaxis()->GetXmin(), ref2D->GetXaxis()->GetXmax());
    // //RooConstVar alpha_400("alphaTargetX", "alphaTargetX", 400);
    // alpha_400.setVal(400);
    // parameters.add(alpha_400);

    // pdfs.add(pdf_500);
    // RooRealVar alpha_500("alpha_500", "alpha_500",ref2D->GetXaxis()->GetXmin(), ref2D->GetXaxis()->GetXmax());
    // //RooConstVar alpha_500("alphaTargetX", "alphaTargetX", 500);
    // alpha_500.setVal(500);
    // parameters.add(alpha_500);

    // pdfs.add(pdf_600);
    // RooRealVar alpha_600("alpha_600", "alpha_600",ref2D->GetXaxis()->GetXmin(), ref2D->GetXaxis()->GetXmax());
    // //RooConstVar alpha_600("alphaTargetX", "alphaTargetX", 600);
    // alpha_600.setVal(600);
    // parameters.add(alpha_600);

	// pdfs.add(pdf_700);
	// RooRealVar alpha_700("alpha_700", "alpha_700",ref2D->GetXaxis()->GetXmin(), ref2D->GetXaxis()->GetXmax());
	// //RooConstVar alpha_700("alphaTargetX", "alphaTargetX", 700);
	// alpha_700.setVal(700);
	// parameters.add(alpha_700);

	// pdfs.add(pdf_800);
	// RooRealVar alpha_800("alpha_800", "alpha_800",ref2D->GetXaxis()->GetXmin(), ref2D->GetXaxis()->GetXmax());
	// //RooConstVar alpha_800("alphaTargetX", "alphaTargetX", 800);
	// alpha_800.setVal(800);
	// parameters.add(alpha_800);

    pdfs.add(pdf_low);
    // RooRealVar alpha_low("alpha_low", "alpha_low",ref2D->GetXaxis()->GetXmin(), ref2D->GetXaxis()->GetXmax());
    // RooRealVar alpha_low("alpha_low", "alpha_low",900,1100);
    // RooConstVar alpha_low("alphaTargetX", "alphaTargetX", 900);
    // alpha_low.setVal(900);
    const RooRealVar alpha_low("alpha_low", "alpha_low",900, "GeV");
    parameters.add(alpha_low);

	pdfs.add(pdf_high);
	// RooRealVar alpha_high("alpha_high", "alpha_high",ref2D->GetXaxis()->GetXmin(), ref2D->GetXaxis()->GetXmax());
	// RooRealVar alpha_high("alpha_high", "alpha_high",900,1100);
	// RooConstVar alpha_high("alphaTargetX", "alphaTargetX", 1100);
    const RooRealVar alpha_high("alpha_low", "alpha_low",1100, "GeV");
	// alpha_high.setVal(1100);
	parameters.add(alpha_high);


	// pdfs.add(pdf_1200);
	// RooRealVar alpha_1200("alpha_1200", "alpha_1200",ref2D->GetXaxis()->GetXmin(), ref2D->GetXaxis()->GetXmax());
	// //RooConstVar alpha_1200("alphaTargetX", "alphaTargetX", 1200);
	// alpha_1200.setVal(1200);
	// parameters.add(alpha_1200);

// 	pdfs.add(pdf_1400);
// 	RooRealVar alpha_1400("alpha_1400", "alpha_1400",ref2D->GetXaxis()->GetXmin(), ref2D->GetXaxis()->GetXmax());
// 	//RooConstVar alpha_1400("alphaTargetX", "alphaTargetX", 1400);
// 	alpha_1400.setVal(1400);
// 	parameters.add(alpha_1400);
//
// 	pdfs.add(pdf_1600);
// 	RooRealVar alpha_1600("alpha_1600", "alpha_1600",ref2D->GetXaxis()->GetXmin(), ref2D->GetXaxis()->GetXmax());
// 	//RooConstVar alpha_1600("alphaTargetX", "alphaTargetX", 1600);
// 	alpha_1600.setVal(1600);
// 	parameters.add(alpha_1600);

    //--------------------------------------------------
    // Set the target value
	// RooRealVar alphaTarget("alphaTarget", "alphaTarget",ref2D->GetXaxis()->GetXmin(), ref2D->GetXaxis()->GetXmax());
	 RooRealVar alphaTarget("alphaTarget", "alphaTarget",900,1100);
	alphaTarget.setVal(1000);

    cout<<"here last -2"<<endl;
    //--------------------------------------------------
    // Perform interpolation with morph
	RooMomentMorph sig_morph("morph","morph",alphaTarget,variableList,pdfs, parameters,RooMomentMorph::Linear);
    cout<<"here last -1"<<endl;
	TH1F* sig_interp = (TH1F*) sig_low->Clone("sig_interp");
    sig_interp->Reset();
    sig_interp->SetTitle("interpolated mX 1000, mY 150");
	//std::cout<< __PRETTY_FUNCTION__ << __LINE__ << std::endl;
	sig_morph.fillHistogram(sig_interp, mXreco);
	//std::cout<< __PRETTY_FUNCTION__ << __LINE__ << std::endl;
    sig_interp->SetLineColor(kRed);
    sig_interp->Scale(sig_real->Integral()/sig_interp->Integral());

    cout<<"here last"<<endl;
	//gROOT->SetBatch(true);
    sig_real->Write();
    sig_low->Write();
    sig_high->Write();
    sig_interp->Write();
    // TCanvas c1;
    // histGaussianAlpha0 ->Draw() ;
    // histGaussianAlpha1 ->Draw("same") ;
    // histGaussianAlpha05->Draw("same hist") ;
	// c1.SaveAs("testHist.pdf");
    ofile->Close();
	//gROOT->SetBatch(false);

}

int main(int argc, char** argv)
{
	ROOT::EnableThreadSafety();
    gSystem->ResetSignal(kSigSegmentationViolation, kTRUE);

	if(argc == 1){
        cout<<"please enter valid command line arguments"<<endl;
        return EXIT_FAILURE;
    }

	TestInterpolatorHist(atoi(argv[1]));

	return EXIT_SUCCESS;
}


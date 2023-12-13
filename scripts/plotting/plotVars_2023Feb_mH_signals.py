import ROOT
from ROOT import TFile, TH1F, TH2F, TCanvas, gStyle, gPad, gDirectory, TLatex, gROOT, PyConfig, TMath, kBlue, TLine, TPad, TLegend, TGraph, TBox, kThermometer, THStack
from ROOT import kRed
# PyConfig.IgnoreCommandLineOptions = False
import numpy as np
import re
import os
from VariableDicts import varInfo

def rootplot( h1, year, region, var, tag, odir):
    #### get the histograms:
    #  print("number of bins, 3b: ", h1.GetSize())
    #  print("a bin error %.4f"%(h1.GetBinError(50)))
    h1 = h1.Clone("h1copy")

    #### normalize the histograms
    #  h1.Sumw2()
    h1area = h1.Integral(0,-1)
    #  print("a bin error %.4f"%(h1.GetBinError(50)))
    # for i in range(h1.GetSize()):
        # h1.SetBinContent(i, h1.GetBinContent(i)/h1.GetBinWidth(i))
    h1.Scale(1./h1.Integral())
    #### define the canvas
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title

    c1.SetMargin(0.12,0.05,0.12,0.09) #left,right,bottom,top
    c1.SetTicks(1,1)

    #### draw histograms in upper pad
    h1.SetLineColor(kRed+2)
    h1.SetLineWidth(2)
    h1.Draw("hist")
    #xaxis

    mXval = tag.split("MX_")[1]
    mXval = mXval.split("_")[0]
    mYval = tag.split("MY_")[1]
    mYval = mYval.split("_")[0]
    # print("mX value", float(mXval))
    h1.GetXaxis().SetRangeUser(varInfo[var]['xlow'], varInfo[var]['xhigh'])
    h1.GetXaxis().SetLabelSize(0.04)
    h1.GetXaxis().SetTitleSize(0.04)
    h1.GetXaxis().SetTitle(varInfo[var]['XaxisTitle'] )
    #yaxis
    h1.GetYaxis().SetTitle(varInfo[var]['YaxisTitle'] )
    h1.GetYaxis().SetLabelSize(0.04)
    h1.GetYaxis().SetTitleSize(0.04)
    h1.GetYaxis().SetTitleOffset(1.3)
    h1.GetYaxis().SetTickLength(0.02)
    yrangeFactor = 1.3
    if var == "HH_kinFit_m": yrangeFactor = 1.57

    CMSlabel = TLatex()
    #  CMSlabel.SetTextSize( 0.08 )
    #  CMSlabel.DrawTextNDC(0.7, 0.85, "CMS Internal")
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 30 )
    CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")

    plotlabels = TLatex()
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    #  labelText = "mX = %.0f GeV, mY = %.0f GeV"%(mXval,mYval)
    labelText = ""
    plotlabels.DrawLatexNDC(0.5, 0.93, "mX = {}, mY = {}".format(mXval, mYval))
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(16)
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(14)
    # plotlabels.DrawLatexNDC(0.8, 0.85, "gen matched")
    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(20)
    plotlabels.DrawTextNDC(0.88, 0.93, year)
    plotlabels.SetTextFont(43)
    plotlabels.SetTextSize(14)
    plotlabels.SetTextAlign(32);
    plotlabels.DrawLatexNDC(0.45, 0.87, "without kinFit Mean = {0:.2f}".format(h1.GetMean()))
    plotlabels.DrawLatexNDC(0.45, 0.84, "without kinFit Std. Dev. = {0:.2f}".format(h1.GetStdDev()))


    #### define legend
    leg = TLegend(0.7,0.75,0.95,0.89)
    leg.AddEntry(h1, "without kinFit", "l")
    leg.SetBorderSize(0) # remove the border
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.025)
    leg.SetFillStyle(0) # make the legend background transparent
    leg.Draw()

    odir = odir
    if not (os.path.exists(odir)): os.makedirs(odir)
    c1.SaveAs("%s/%s%s_%s.pdf"%( odir   ,year, var, tag ))

def makeplotsForRegion(dir_region, region, odir, year, ifileTag):
    if "2022Jan26" in ifileTag:
        idir = "DataPlots_fullSubmission_{0}_v34_aidan_{1}".format(year, ifileTag) # outPlotter.root is the same for CR and VR (normal binning)
        print(idir)
    else:
        idir = "VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}".format(year,ifileTag) # outPlotter.root is the same for CR and VR (normal binning)
    odir = odir + year
    myfile = TFile.Open(idir + "/outPlotter.root")
    dir_ttbar_3b = "ttbar_3b"
    dir_ttbar_3b_weights = "ttbar_3bScaled"
    dir_ttbar_4b = "ttbar"
    dir_data_3b = "data_BTagCSV_3btag"
    dir_data_4b = "data_BTagCSV"
    dir_data_3b_weights = "data_BTagCSV_dataDriven_kinFit"
    dir_data_3b_weights_down = "data_BTagCSV_dataDriven_kinFit_down"
    dir_data_3b_weights_up = "data_BTagCSV_dataDriven_kinFit_up"
    dir_QCD = "QCD"

    dir_sig_MX_600_MY_400 = "sig_NMSSM_bbbb_MX_600_MY_400" # signal
    dir_sig_MX_300_MY_60 = "sig_NMSSM_bbbb_MX_300_MY_60" # signal
    dir_sig_MX_300_MY_150 = "sig_NMSSM_bbbb_MX_300_MY_150" # signal
    dir_sig_3b_weights = "sig_NMSSM_bbbb_MX_600_MY_400_3bScaled"

    dir_sig_MX_400_MY_150   = "sig_NMSSM_bbbb_MX_400_MY_150" # signal
    dir_sig_MX_500_MY_200   = "sig_NMSSM_bbbb_MX_500_MY_200" # signal
    dir_sig_MX_700_MY_150   = "sig_NMSSM_bbbb_MX_700_MY_200" # signal
    dir_sig_MX_900_MY_700   = "sig_NMSSM_bbbb_MX_900_MY_700" # signal
    dir_sig_MX_1000_MY_200  = "sig_NMSSM_bbbb_MX_1000_MY_200" # signal
    dir_sig_MX_1000_MY_700  = "sig_NMSSM_bbbb_MX_1000_MY_700" # signal
    dir_sig_MX_1200_MY_500  = "sig_NMSSM_bbbb_MX_1200_MY_500" # signal
    dir_sig_MX_1600_MY_1200 = "sig_NMSSM_bbbb_MX_1600_MY_1200" # signal
    #  varlist = [ "H1_b1_ptRegressed", "H1_b2_ptRegressed", "H1_b1_kinFit_ptRegressed", "H1_b2_kinFit_ptRegressed", "H2_b1_ptRegressed", "H2_b2_ptRegressed", "H1_b1_deepCSV", "H1_b2_deepCSV", "H2_b1_deepCSV", "H2_b2_deepCSV", "H1_pt", "H1_kinFit_pt", "H2_pt", "HH_m", "HH_kinFit_m", "HH_pt", "HH_kinFit_pt", "H1_m", "H2_m", "H1_eta", "H1_kinFit_eta", "H2_eta", "H1_bb_DeltaR", "H1_kinFit_bb_DeltaR", "H2_bb_DeltaR", "H1_H2_sphericity", "FourBjet_sphericity", "distanceFromDiagonal" ]
    #  varlist = [ "H1_b1_kinFit_ptRegressed", "H1_b2_kinFit_ptRegressed", "H2_b1_ptRegressed", "H2_b2_ptRegressed", "H1_kinFit_pt", "H2_pt", "HH_kinFit_m", "HH_kinFit_pt", "H2_m", "H1_kinFit_eta", "H2_eta", "H1_kinFit_bb_DeltaR", "H2_bb_DeltaR", "distanceFromDiagonal" ]
    #  "H1_kinFit_m",
    varlist = [ "H1_m", "H2_m", "HH_kinFit_m"]
    varlist2D = [ "H1_m_H2_m", "HH_m_H2_m", "HH_kinFit_m_H2_m" ]

    #  masspoint_list = [ "MX_1800_MY_800" ]
    masspoint_list = "MX_600_MY_400"
    sigdirHeader = "sig_NMSSM_bbbb_"
##################################################
#  # data plots
    varname1 = "H1_m"
    signalDirList = [dir_sig_MX_400_MY_150  , dir_sig_MX_500_MY_200  , dir_sig_MX_700_MY_150  , dir_sig_MX_900_MY_700  , dir_sig_MX_1000_MY_200 , dir_sig_MX_1000_MY_700 , dir_sig_MX_1200_MY_500 , dir_sig_MX_1600_MY_1200,
                     "sig_NMSSM_bbbb_MX_600_MY_60",
                     "sig_NMSSM_bbbb_MX_600_MY_70",
                     "sig_NMSSM_bbbb_MX_600_MY_80",
                     "sig_NMSSM_bbbb_MX_600_MY_90",
                     "sig_NMSSM_bbbb_MX_600_MY_100",
                     "sig_NMSSM_bbbb_MX_600_MY_125",
                     "sig_NMSSM_bbbb_MX_600_MY_150",
                     "sig_NMSSM_bbbb_MX_600_MY_200",
                     "sig_NMSSM_bbbb_MX_600_MY_250",
                     "sig_NMSSM_bbbb_MX_600_MY_300",
                     "sig_NMSSM_bbbb_MX_600_MY_400",
                     "sig_NMSSM_bbbb_MX_650_MY_60",
                     "sig_NMSSM_bbbb_MX_650_MY_70",
                     "sig_NMSSM_bbbb_MX_650_MY_80",
                     "sig_NMSSM_bbbb_MX_650_MY_90",
                     "sig_NMSSM_bbbb_MX_650_MY_100",
                     "sig_NMSSM_bbbb_MX_650_MY_125",
                     "sig_NMSSM_bbbb_MX_650_MY_150",
                     "sig_NMSSM_bbbb_MX_650_MY_190",
                     "sig_NMSSM_bbbb_MX_650_MY_250",
                     "sig_NMSSM_bbbb_MX_650_MY_300",
                     "sig_NMSSM_bbbb_MX_650_MY_350",
                     "sig_NMSSM_bbbb_MX_650_MY_400",
                     "sig_NMSSM_bbbb_MX_650_MY_450",
                     "sig_NMSSM_bbbb_MX_650_MY_500",
                     "sig_NMSSM_bbbb_MX_700_MY_60",
                     "sig_NMSSM_bbbb_MX_700_MY_70",
                     "sig_NMSSM_bbbb_MX_700_MY_80",
                     "sig_NMSSM_bbbb_MX_700_MY_90",
                     "sig_NMSSM_bbbb_MX_700_MY_100",
                     "sig_NMSSM_bbbb_MX_700_MY_125",
                     "sig_NMSSM_bbbb_MX_700_MY_150",
                     "sig_NMSSM_bbbb_MX_700_MY_200",
                     "sig_NMSSM_bbbb_MX_700_MY_250",
                     "sig_NMSSM_bbbb_MX_700_MY_300",
                     "sig_NMSSM_bbbb_MX_700_MY_400",
                     ]
    for sigDir in signalDirList:
    #  varname = "H1_b1_kinFit_ptRegressed"
        myfile.cd(sigDir+"/"+dir_region)
        h1 = gDirectory.Get(sigDir+"_"+dir_region+"_"+varname1)
        rootplot( h1, year, region, varname1, sigDir, odir )

# ********************
#run pyROOT in batch mode  - ie don't show graphics!
#
gROOT.SetBatch(True)
# odir = "VarPlots/2023Feb21_signalMH/"
odir = "VarPlots/2023Dec7_signalMH/"
odiro = odir
years = ["2016","2017","2018"]
# !!!!!!!!!!! CAREFUL using Signal Region! !!!!!!!!!!! only for MC
# ##################################################
# for data
# directories = ["selectionbJets_ControlRegionBlinded", "selectionbJets_ValidationRegionBlinded", "selectionbJets_SignalRegion"]
# regionTag = ["CR", "VR", "SR"]
# directories = ["selectionbJets_ControlRegionBlinded", "selectionbJets_ValidationRegionBlinded"]
directories = ["selectionbJets_SignalRegion"]
regionTag = ["SR"]
# iTags = ["2022Jul7_fullBDT_bJetScoreLoose"]
# iTags = ["2022Nov14_bJetScoreLoose_shapes2"]
# iTags = ["2023Feb21_genMatched"]
iTags = ["2023Dec7_binMYx2_addMX650_10ev"]
for iTag in iTags:
   for year in years:
       for i, directory in enumerate(directories):
           makeplotsForRegion(directory, regionTag[i], odir+iTag+"/", year, iTag)
# ##################################################

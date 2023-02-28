import ROOT
from ROOT import TFile, TH1F, TH2F, TCanvas, gStyle, gPad, gDirectory, TLatex, gROOT, PyConfig, TMath, kBlue, TLine, TPad, TLegend, TGraph, TBox, kThermometer, THStack, TGraphAsymmErrors 
from ROOT import kRed 
# PyConfig.IgnoreCommandLineOptions = False
import numpy as np
import re
import os
from VariableDicts import varInfo
import sys
import math

def rootplot_2Dhist(h1,year,region, odir, tag):
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    gStyle.SetPalette(kThermometer)
    gPad.SetTicks(1,1)
    gPad.SetMargin(0.12,0.16,0.12,0.09) #left,right,bottom,top
    #  p1.SetMargin(0.12,0.05,0.05,0.09) #left,right,bottom,top
    #  p2.SetMargin(0.12,0.05,0.38,0.05) #left,right,bottom,top

    h1.Draw("COLZ1")
    if(year == "2016"): h1.GetZaxis().SetRangeUser(0.85, 1.0)
    if(year == "2017"): h1.GetZaxis().SetRangeUser(0.94, 1.0)
    if(year == "2018"): h1.GetZaxis().SetRangeUser(0.94, 1.0)
    h1.GetZaxis().SetTitle("trigger pT selections / analysis selections")
    h1.GetZaxis().SetTitleOffset(1.3)
    h1.GetXaxis().SetTitle("m_{X} [GeV]")
    h1.GetYaxis().SetTitle("m_{Y} [GeV]")
    CMSlabel = TLatex()
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 30 )
    CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
    plotlabels = TLatex()
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    #  labelText = "mX = %.0f GeV, mY = %.0f GeV"%(mXval,mYval)
    labelText = ""
    if "VR" in region:    labelText = labelText + "Validation Region"
    if "CR" in region:    labelText = labelText + "Control Region"
    if "SR" in region:    labelText = labelText + "Signal Region"
    plotlabels.DrawLatexNDC(0.60, 0.93, labelText)
    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(20)
    plotlabels.DrawTextNDC(0.83, 0.93, year)

    c1.SaveAs("%s/%s%s_mXvsmY_%s.pdf"%(odir, region, year,tag))
  
    del c1
    del h1

def makePlotsPerYear(year):
  ifileTag = "2022Nov14_bJetScoreLoose_shapes2"
  ifileTag2 = "2023Feb27_TrigCut_5"
  odir = "VarPlots/2023Feb27_trigCuts/"
  tag = ifileTag2
  years = ["2016", "2017", "2018"]
  h2dCR = ROOT.TH2D( "h2dCR", "HistCR ", 11, MXbins, 19, MYbins);
  h2dVR = ROOT.TH2D( "h2dVR", "HistVR ", 11, MXbins, 19, MYbins);
  h2dSR = ROOT.TH2D( "h2dSR", "HistSR ", 11, MXbins, 19, MYbins);
  idir = "VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}".format(year,ifileTag) # outPlotter.root is the same for CR and VR (normal binning)
  idir2 = "VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}".format(year,ifileTag2) # outPlotter.root is the same for CR and VR (normal binning)
  directories = ["selectionbJets_ControlRegionBlinded", "selectionbJets_ValidationRegionBlinded", "selectionbJets_SignalRegion"]
  varname = "HH_kinFit_m"
  myfile = TFile.Open(idir + "/outPlotter.root")
  myfile2 = TFile.Open(idir2 + "/outPlotter.root")
  for i, sigDir in enumerate(signals):
      myfile.cd(sigDir+"/"+directories[0])
      hCR = gDirectory.Get(sigDir+"_"+directories[0]+"_"+varname)
      myfile.cd(sigDir+"/"+directories[1])
      hVR = gDirectory.Get(sigDir+"_"+directories[1]+"_"+varname)
      myfile.cd(sigDir+"/"+directories[2])
      hSR = gDirectory.Get(sigDir+"_"+directories[2]+"_"+varname)

      myfile2.cd(sigDir+"/"+directories[0])
      hCR2 = gDirectory.Get(sigDir+"_"+directories[0]+"_"+varname)
      myfile2.cd(sigDir+"/"+directories[1])
      hVR2 = gDirectory.Get(sigDir+"_"+directories[1]+"_"+varname)
      myfile2.cd(sigDir+"/"+directories[2])
      hSR2 = gDirectory.Get(sigDir+"_"+directories[2]+"_"+varname)
      # print(sigDir)
      if (year == "2017" and sigDir =="sig_NMSSM_bbbb_MX_1000_MY_150"): continue
      h2dCR.Fill(signalsMX[i], signalsMY[i], hCR2.GetEntries()/hCR.GetEntries())
      h2dVR.Fill(signalsMX[i], signalsMY[i], hVR2.GetEntries()/hVR.GetEntries())
      h2dSR.Fill(signalsMX[i], signalsMY[i], hSR2.GetEntries()/hSR.GetEntries())

  rootplot_2Dhist(h2dCR,year, "CR", odir, tag)
  rootplot_2Dhist(h2dVR,year, "VR", odir, tag)
  rootplot_2Dhist(h2dSR,year, "SR", odir, tag)
  del h2dCR, h2dVR, h2dSR 

##################################################
gROOT.SetBatch(True)


signals      = ["sig_NMSSM_bbbb_MX_400_MY_60", "sig_NMSSM_bbbb_MX_400_MY_70", "sig_NMSSM_bbbb_MX_400_MY_80", "sig_NMSSM_bbbb_MX_400_MY_90", "sig_NMSSM_bbbb_MX_400_MY_100", "sig_NMSSM_bbbb_MX_400_MY_125", "sig_NMSSM_bbbb_MX_400_MY_150", "sig_NMSSM_bbbb_MX_400_MY_200", "sig_NMSSM_bbbb_MX_400_MY_250", "sig_NMSSM_bbbb_MX_500_MY_60", "sig_NMSSM_bbbb_MX_500_MY_70", "sig_NMSSM_bbbb_MX_500_MY_80", "sig_NMSSM_bbbb_MX_500_MY_90", "sig_NMSSM_bbbb_MX_500_MY_100", "sig_NMSSM_bbbb_MX_500_MY_125", "sig_NMSSM_bbbb_MX_500_MY_150", "sig_NMSSM_bbbb_MX_500_MY_200", "sig_NMSSM_bbbb_MX_500_MY_250", "sig_NMSSM_bbbb_MX_500_MY_300", "sig_NMSSM_bbbb_MX_600_MY_60", "sig_NMSSM_bbbb_MX_600_MY_70", "sig_NMSSM_bbbb_MX_600_MY_80", "sig_NMSSM_bbbb_MX_600_MY_90", "sig_NMSSM_bbbb_MX_600_MY_100", "sig_NMSSM_bbbb_MX_600_MY_125", "sig_NMSSM_bbbb_MX_600_MY_150", "sig_NMSSM_bbbb_MX_600_MY_200", "sig_NMSSM_bbbb_MX_600_MY_250", "sig_NMSSM_bbbb_MX_600_MY_300", "sig_NMSSM_bbbb_MX_600_MY_400", "sig_NMSSM_bbbb_MX_700_MY_60", "sig_NMSSM_bbbb_MX_700_MY_70", "sig_NMSSM_bbbb_MX_700_MY_80", "sig_NMSSM_bbbb_MX_700_MY_90", "sig_NMSSM_bbbb_MX_700_MY_100", "sig_NMSSM_bbbb_MX_700_MY_125", "sig_NMSSM_bbbb_MX_700_MY_150", "sig_NMSSM_bbbb_MX_700_MY_200", "sig_NMSSM_bbbb_MX_700_MY_250", "sig_NMSSM_bbbb_MX_700_MY_300", "sig_NMSSM_bbbb_MX_700_MY_400", "sig_NMSSM_bbbb_MX_700_MY_500", "sig_NMSSM_bbbb_MX_800_MY_60", "sig_NMSSM_bbbb_MX_800_MY_70", "sig_NMSSM_bbbb_MX_800_MY_80", "sig_NMSSM_bbbb_MX_800_MY_90", "sig_NMSSM_bbbb_MX_800_MY_100", "sig_NMSSM_bbbb_MX_800_MY_125", "sig_NMSSM_bbbb_MX_800_MY_150", "sig_NMSSM_bbbb_MX_800_MY_200", "sig_NMSSM_bbbb_MX_800_MY_250", "sig_NMSSM_bbbb_MX_800_MY_300", "sig_NMSSM_bbbb_MX_800_MY_400", "sig_NMSSM_bbbb_MX_800_MY_500", "sig_NMSSM_bbbb_MX_800_MY_600", "sig_NMSSM_bbbb_MX_900_MY_60", "sig_NMSSM_bbbb_MX_900_MY_70", "sig_NMSSM_bbbb_MX_900_MY_80", "sig_NMSSM_bbbb_MX_900_MY_90", "sig_NMSSM_bbbb_MX_900_MY_100", "sig_NMSSM_bbbb_MX_900_MY_125", "sig_NMSSM_bbbb_MX_900_MY_150", "sig_NMSSM_bbbb_MX_900_MY_200", "sig_NMSSM_bbbb_MX_900_MY_250", "sig_NMSSM_bbbb_MX_900_MY_300", "sig_NMSSM_bbbb_MX_900_MY_400", "sig_NMSSM_bbbb_MX_900_MY_500", "sig_NMSSM_bbbb_MX_900_MY_600", "sig_NMSSM_bbbb_MX_900_MY_700", "sig_NMSSM_bbbb_MX_1000_MY_60", "sig_NMSSM_bbbb_MX_1000_MY_70", "sig_NMSSM_bbbb_MX_1000_MY_80", "sig_NMSSM_bbbb_MX_1000_MY_90", "sig_NMSSM_bbbb_MX_1000_MY_100", "sig_NMSSM_bbbb_MX_1000_MY_125", "sig_NMSSM_bbbb_MX_1000_MY_150", "sig_NMSSM_bbbb_MX_1000_MY_200", "sig_NMSSM_bbbb_MX_1000_MY_250", "sig_NMSSM_bbbb_MX_1000_MY_300", "sig_NMSSM_bbbb_MX_1000_MY_400", "sig_NMSSM_bbbb_MX_1000_MY_500", "sig_NMSSM_bbbb_MX_1000_MY_600", "sig_NMSSM_bbbb_MX_1000_MY_700", "sig_NMSSM_bbbb_MX_1000_MY_800", "sig_NMSSM_bbbb_MX_1100_MY_90", "sig_NMSSM_bbbb_MX_1100_MY_100", "sig_NMSSM_bbbb_MX_1100_MY_125", "sig_NMSSM_bbbb_MX_1100_MY_150", "sig_NMSSM_bbbb_MX_1100_MY_200", "sig_NMSSM_bbbb_MX_1100_MY_250", "sig_NMSSM_bbbb_MX_1100_MY_300", "sig_NMSSM_bbbb_MX_1100_MY_400", "sig_NMSSM_bbbb_MX_1100_MY_500",
                "sig_NMSSM_bbbb_MX_1100_MY_600", "sig_NMSSM_bbbb_MX_1100_MY_700", "sig_NMSSM_bbbb_MX_1100_MY_800", "sig_NMSSM_bbbb_MX_1100_MY_900", "sig_NMSSM_bbbb_MX_1200_MY_90", "sig_NMSSM_bbbb_MX_1200_MY_100", "sig_NMSSM_bbbb_MX_1200_MY_125", "sig_NMSSM_bbbb_MX_1200_MY_150", "sig_NMSSM_bbbb_MX_1200_MY_200", "sig_NMSSM_bbbb_MX_1200_MY_250", "sig_NMSSM_bbbb_MX_1200_MY_300", "sig_NMSSM_bbbb_MX_1200_MY_400", "sig_NMSSM_bbbb_MX_1200_MY_500", "sig_NMSSM_bbbb_MX_1200_MY_600", "sig_NMSSM_bbbb_MX_1200_MY_700", "sig_NMSSM_bbbb_MX_1200_MY_800", "sig_NMSSM_bbbb_MX_1200_MY_900", "sig_NMSSM_bbbb_MX_1200_MY_1000", "sig_NMSSM_bbbb_MX_1400_MY_90", "sig_NMSSM_bbbb_MX_1400_MY_100", "sig_NMSSM_bbbb_MX_1400_MY_125", "sig_NMSSM_bbbb_MX_1400_MY_150", "sig_NMSSM_bbbb_MX_1400_MY_200", "sig_NMSSM_bbbb_MX_1400_MY_250", "sig_NMSSM_bbbb_MX_1400_MY_300", "sig_NMSSM_bbbb_MX_1400_MY_400", "sig_NMSSM_bbbb_MX_1400_MY_500", "sig_NMSSM_bbbb_MX_1400_MY_600", "sig_NMSSM_bbbb_MX_1400_MY_700", "sig_NMSSM_bbbb_MX_1400_MY_800", "sig_NMSSM_bbbb_MX_1400_MY_900", "sig_NMSSM_bbbb_MX_1400_MY_1000", "sig_NMSSM_bbbb_MX_1400_MY_1200", "sig_NMSSM_bbbb_MX_1600_MY_90", "sig_NMSSM_bbbb_MX_1600_MY_100", "sig_NMSSM_bbbb_MX_1600_MY_125", "sig_NMSSM_bbbb_MX_1600_MY_150", "sig_NMSSM_bbbb_MX_1600_MY_200", "sig_NMSSM_bbbb_MX_1600_MY_250", "sig_NMSSM_bbbb_MX_1600_MY_300", "sig_NMSSM_bbbb_MX_1600_MY_400", "sig_NMSSM_bbbb_MX_1600_MY_500", "sig_NMSSM_bbbb_MX_1600_MY_600", "sig_NMSSM_bbbb_MX_1600_MY_700", "sig_NMSSM_bbbb_MX_1600_MY_800", "sig_NMSSM_bbbb_MX_1600_MY_900", "sig_NMSSM_bbbb_MX_1600_MY_1000", "sig_NMSSM_bbbb_MX_1600_MY_1200", "sig_NMSSM_bbbb_MX_1600_MY_1400"]
signalsMX      = np.array([400, 400, 400, 400, 400, 400, 400, 400, 400, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 600, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 900, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100,
                1100, 1100, 1100, 1100, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1400, 1400, 1400, 1400, 1400, 1400, 1400, 1400, 1400, 1400, 1400, 1400, 1400, 1400, 1400, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600, 1600])
MXbins = np.unique(signalsMX)
MXbins = (MXbins[1:] + MXbins[:-1]) / 2
# MXbins = np.diff(signalsMX)
signalsMY      = np.array([60, 70, 80, 90, 100, 125, 150, 200, 250, 60, 70, 80, 90, 100, 125, 150, 200, 250, 300, 60, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400, 60, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400, 500, 60, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400, 500, 600, 60, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400, 500, 600, 700, 60, 70, 80, 90, 100, 125, 150, 200, 250, 300, 400, 500, 600, 700, 800, 90, 100, 125, 150, 200, 250, 300, 400, 500,
                600, 700, 800, 900, 90, 100, 125, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 90, 100, 125, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 90, 100, 125, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1400])
MYbins = np.sort(np.unique(signalsMY))
MYbins = (MYbins[1:] + MYbins[:-1]) / 2
#print(np.array(signals).shape[0])
#print(signalsMX.shape[0])
#print(signalsMY.shape[0])
# MXbins = np.unique(MXbins)
# MXbins[0] = MXbins[0]-100
# MXbins[-1] = MXbins[-1]+200
MXbins = np.insert(MXbins,0,350)
MXbins = np.append(MXbins,1700)
MXbins = np.array(MXbins, dtype='float64')
MYbins = np.insert(MYbins,0,55)
MYbins = np.append(MYbins,1500)
MYbins = np.array(MYbins, dtype='float64')
#print(MXbins.shape[0])
#print(MYbins.shape[0])
#print(signalsMX)
#print(signalsMY)
#print(MXbins)
#print(MYbins)

##################################################

# year = 2017
# sigDir = "sig_NMSSM_bbbb_MX_600_MY_400" # signal
# idir = "VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}".format(year,ifileTag) # outPlotter.root is the same for CR and VR (normal binning)
# idir2 = "VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}".format(year,ifileTag2) # outPlotter.root is the same for CR and VR (normal binning)
# directories = ["selectionbJets_ControlRegionBlinded", "selectionbJets_ValidationRegionBlinded", "selectionbJets_SignalRegion"]
# varname = "HH_kinFit_m"
# myfile = TFile.Open(idir + "/outPlotter.root")
# myfile2 = TFile.Open(idir2 + "/outPlotter.root")
# with open("SignalEvents_TrigCut2017.txt","w") as ofile:
#      ofile.write("sig, CR, VR, SR, CR_TrigCut, VR_TrigCut, SR_TrigCut, CR_ratio, VR_ratio, SR_ratio\n")
#      # for sigDir in signals:
#      # sigDir = "sig_NMSSM_bbbb_MX_600_MY_400" # signal
#      for sigDir in signals:
#        if (sigDir =="sig_NMSSM_bbbb_MX_1000_MY_150"): continue
#        myfile.cd(sigDir+"/"+directories[0])
#        hCR = gDirectory.Get(sigDir+"_"+directories[0]+"_"+varname)
#        myfile.cd(sigDir+"/"+directories[1])
#        hVR = gDirectory.Get(sigDir+"_"+directories[1]+"_"+varname)
#        myfile.cd(sigDir+"/"+directories[2])
#        hSR = gDirectory.Get(sigDir+"_"+directories[2]+"_"+varname)
#  
#        myfile2.cd(sigDir+"/"+directories[0])
#        hCR2 = gDirectory.Get(sigDir+"_"+directories[0]+"_"+varname)
#        myfile2.cd(sigDir+"/"+directories[1])
#        hVR2 = gDirectory.Get(sigDir+"_"+directories[1]+"_"+varname)
#        myfile2.cd(sigDir+"/"+directories[2])
#        hSR2 = gDirectory.Get(sigDir+"_"+directories[2]+"_"+varname)
#  
#        ofile.write("{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}\n".format(sigDir, 
#                                                                 hCR.GetEntries(),hVR.GetEntries(),hSR.GetEntries(),
#                                                                 hCR2.GetEntries(),hVR2.GetEntries(),hSR2.GetEntries(),
#                                                                 hCR2.GetEntries()/hCR.GetEntries(), hVR2.GetEntries()/hVR.GetEntries() , hSR2.GetEntries()/hSR.GetEntries() ))
# 
# mx_Bins = [ 350,  450,  500,  550,  600,  650,  700,  750,  800,  850,  900,  950, 1000, 1050,
     # 1100, 1150, 1200, 1300, 1400, 1500, 1700]
# my_Bins = [  55,   65,   75,   85,   95,  112,  137,  155,  175,  180,  225,  230,  275,  280,
      # 330,  350,  380,  445,  450,  495,  545,  550,  645,  650,  750,  850,  950, 1100,
       # 1300, 1500]
# h2d = ROOT.TH2D("h2d", "h2d title", 40, 0.0, 2.0, 30, -1.5, 3.5);

# region = "SR"



makePlotsPerYear("2016")
makePlotsPerYear("2017")
makePlotsPerYear("2018")

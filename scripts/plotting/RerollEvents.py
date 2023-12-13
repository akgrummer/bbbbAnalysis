import ROOT
from ROOT import TFile, TH1F, TH2F, TCanvas, gStyle, gPad, gDirectory, TLatex, gROOT, PyConfig, TMath, kBlue, TLine, TPad, TLegend, TGraph, TBox, kThermometer, THStack, TGraphAsymmErrors
from ROOT import kRed
import numpy as np
import re
import os
from VariableDicts import varInfo
import sys
import math
import argparse
import csv

def rootplot_2Dhist(h1, year, odir, tag, descriptionLabel):
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    gStyle.SetPalette(kThermometer)
    gPad.SetTicks(1,1)
    gPad.SetMargin(0.12,0.16,0.12,0.09) #left,right,bottom,top
    #  p1.SetMargin(0.12,0.05,0.05,0.09) #left,right,bottom,top
    #  p2.SetMargin(0.12,0.05,0.38,0.05) #left,right,bottom,top

    h1.Draw("COLZ1")
    # if(year == "2016"): h1.GetZaxis().SetRangeUser(0., .1)
    # if(year == "2017"): h1.GetZaxis().SetRangeUser(0., .1)
    # if("pull" in descriptionLabel): h1.GetZaxis().SetRangeUser(-8., 8)
    if("Background" in descriptionLabel and int(args.massGroup) <= 1): h1.GetZaxis().SetRangeUser(0., 10.5)
    if("Background" in descriptionLabel and int(args.massGroup) == 2): h1.GetZaxis().SetRangeUser(0., 10.5)
    if("Background" in descriptionLabel and int(args.massGroup) == 3): h1.GetZaxis().SetRangeUser(0., 10.5)
    if("Background" in descriptionLabel and int(args.massGroup) == 4): h1.GetZaxis().SetRangeUser(0., 10.5)
    # h1.GetZaxis().SetRangeUser(zmin, zmax)
    h1.GetZaxis().SetTitle("Events / Bin")
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
    labelText + "Signal Region"
    # else:    labelText = labelText + "Signal Region"
    plotlabels.DrawLatexNDC(0.2, 0.84, "Mass Group {}".format(args.massGroup))
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(16)
    plotlabels.DrawLatexNDC(0.2, 0.8, descriptionLabel)
    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(20)
    plotlabels.DrawTextNDC(0.7, 0.93, year)

    if not os.path.isdir("Reroll/{0}".format(tag.split("_massGroup")[0])):
        os.mkdir("Reroll/{0}".format(tag.split("_massGroup")[0]))
    if not os.path.isdir("Reroll/{0}/{1}".format(tag.split("_massGroup")[0],year)):
        os.mkdir("Reroll/{0}/{1}".format(tag.split("_massGroup")[0], year))
    c1.SaveAs("Reroll/{0}/{1}/{2}_{1}.pdf".format(tag.split("_massGroup")[0], year, tag))

    del c1
    del h1

def rootplot_1Dhist(h1, year, odir, tag, descriptionLabel):
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    gPad.SetTicks(1,1)
    gPad.SetMargin(0.12,0.09,0.12,0.09) #left,right,bottom,top

    h1.Draw("hist")
    h1.GetXaxis().SetTitle("pull")
    h1.GetXaxis().SetRangeUser(-3., 3.)
    h1.GetYaxis().SetTitle("entries")
    CMSlabel = TLatex()
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 30 )
    CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
    plotlabels = TLatex()
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    #  labelText = "mX = %.0f GeV, mY = %.0f GeV"%(mXval,mYval)
    labelText = ""
    labelText + "Validation Region"
    # else:    labelText = labelText + "Signal Region"
    plotlabels.DrawLatexNDC(0.2, 0.84, "Mass Group {}".format(args.massGroup))
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(16)
    plotlabels.DrawLatexNDC(0.2, 0.8, descriptionLabel)
    plotlabels.DrawTextNDC(0.2, 0.76, "Mean: {:0.4f}".format(h1.GetMean()))
    plotlabels.DrawTextNDC(0.2, 0.72, "Std. Dev.: {:.4f}".format(h1.GetStdDev()))
    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(20)
    plotlabels.DrawTextNDC(0.7, 0.93, year)

    if not os.path.isdir("Reroll/{0}".format(tag)):
        os.mkdir("Reroll/{0}".format(tag))
    if not os.path.isdir("Reroll/{0}/{1}".format(tag,year)):
        os.mkdir("Reroll/{0}/{1}".format(tag, year))
    c1.SaveAs("Reroll/{0}/{1}/{0}_{1}.pdf".format(tag, year))
    del c1
    del h1

def makePlotsPerYear(year, pvalFile, labels, inputFile):
  tag = labels[1]
  year = labels[2]
  # sig = "sig_NMSSM_bbbb_MX_1200_MY_300"
  massGroup = labels[3]
  sig = labels[4]

  inCombine = ROOT.TFile(inputFile)
  # inCombine.cd("data_BTagCSV/selectionbJets_SignalRegion");
  # hdataIN = inCombine.Get("data_BTagCSV/selectionbJets_SignalRegion/data_BTagCSV_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled");
  inCombine.cd("data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion");
  hbkgIN = inCombine.Get("data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion/data_BTagCSV_dataDriven_kinFit_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled");
  h2d_INbkg = ROOT.TH2D( "h2d_INbkg", "Hist_INbkg ", nbins_mX, MXbins, nbins_mY, MYbins );

  bkgVal = ROOT.Double(0)
  with open(ifile) as csvfile:
      binMapping = csv.reader(csvfile, delimiter=',')
      for i,mapmX,mapmY in binMapping:
          bkgVal = hbkgIN.GetBinContent(int(i))
          h2d_INbkg.Fill(float(mapmX),float(mapmY), bkgVal)

  rootplot_2Dhist(h2d_INbkg, year, iodir, tag + "_bkgIN_massGroup" + args.massGroup, "Background Model")
  del h2d_INbkg

##################################################
gROOT.SetBatch(True)
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--tag'  ,  dest = 'tag'   ,  help = 'production tag'  ,  default = ""  ,  required = False  )
parser.add_argument('--year'  ,  dest = 'year'   ,  help = 'production tag'  ,  default = ""  ,  required = False  )
parser.add_argument('--group'  ,  dest = 'massGroup'   ,  help = 'production tag'  ,  default = ""  ,  required = False  )

args = parser.parse_args()
# MXbins = np.diff(signalsMX)
# bins
nbins_mY=35
nbins_mX=33


MYbins     = np.array([36, 51, 62, 70, 78, 86, 94, 102, 110, 122, 140, 156, 172, 188, 204, 228, 260, 292, 324, 356, 388, 444, 508, 572, 636, 700, 764, 892, 1020, 1148, 1276, 1404, 1564, 1820, 2076, 2204], dtype='float64')
MXbins     = np.array([212, 228, 244, 260, 276, 292, 308, 324, 340, 360, 392, 424, 456, 488, 520, 552, 584, 616, 648, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216, 1296, 1424, 1552, 1680, 1808, 1936], dtype='float64')
# MYbins = np.array([36, 45, 51, 57, 62, 66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 122, 132, 140, 148, 156, 164, 172, 180, 188, 196, 204, 212, 228, 244, 260, 276, 292, 308, 324, 340, 356, 372, 388, 412, 444, 476, 508, 540, 572, 604, 636, 668, 700, 732, 764, 828, 892, 956, 1020, 1084, 1148, 1212, 1276, 1340, 1404, 1468, 1564, 1692, 1820, 1948, 2076, 2204], dtype='float64')
# MXbins = np.array([212, 228, 244, 260, 276, 292, 308, 324, 340, 360, 392, 424, 456, 488, 520, 552, 584, 616, 648, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216, 1296, 1424, 1552, 1680, 1808, 1936, 2064, 2192, 2320], dtype='float64')

# zmin = 0.
# zmax=1.0
tag = args.tag
ogTag=tag.replace("_VR","")
ogTag=ogTag.replace("_SR","")
print(ogTag)
print(tag)
# tag ="2023Jul5_binMYx2_ncMCStats_lowStatsCut"
inputFile = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}/outPlotter_massGroup{2}.root".format(args.year, tag, args.massGroup)
iodir = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}/".format(args.year, ogTag)
ifile = iodir + "outPlotter_UnrollLocation_massGroup{0}.txt".format(args.massGroup)

sigs = ["sig_NMSSM_bbbb_MX_400_MY_125", "sig_NMSSM_bbbb_MX_700_MY_60", "sig_NMSSM_bbbb_MX_900_MY_600", "sig_NMSSM_bbbb_MX_1200_MY_300", "sig_NMSSM_bbbb_MX_1600_MY_125"]
# histosFile = "root://cmseos.fnal.gov//store/user/agrummer/bbbb_limits/2023Jul5_VR/HistogramFiles_{0}/outPlotter_{0}_{1}.root".format(args.year, sigs[int(args.massGroup)])
# sig= "sig_NMSSM_bbbb_MX_400_MY_125"
# # labels = ["prefit", "2016", "Mass Group 0", sig]
# tag = "2023Jul5_VR"
# # tag = "2023Jul5_SR"
# years=["2016", "2017", "2018"]
# allfittypes= ["fit_b", "fit_s", "prefit"]
# for afittype in allfittypes:
#     for year in years:
#         for i, sig in enumerate(sigs):
#             labels = [afittype, tag, year, "Mass Group {}".format(i), sig]
#             makePlot(labels)
labels = ["fit_b", tag, args.year, "Mass Group {}".format(args.massGroup), sigs[int(args.massGroup)]]
makePlotsPerYear("{}".format(args.year), ifile, labels, inputFile)


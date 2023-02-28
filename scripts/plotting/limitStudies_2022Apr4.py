from ROOT import TFile, TH1F, TH2F, TCanvas, gStyle, gPad, gDirectory, TLatex, gROOT, PyConfig, TMath, kBlue, TLine, TPad, TLegend, TGraph, TBox
from ROOT import kRed, kGreen, kBlack, kYellow
# PyConfig.IgnoreCommandLineOptions = False
import numpy as np
import re
import os
from VariableDicts import varInfo


# ********************
#run pyROOT in batch mode  - ie don't show graphics!
# 
gROOT.SetBatch(True)
# ********************

c1 = TCanvas('c1', 'c1',800,600)
gStyle.SetOptStat(0) # remove the stats box
gStyle.SetOptTitle(0) # remove the title
gPad.SetTicks(1,1)
gPad.SetMargin(0.12,0.12,0.05,0.09) #left,right,bottom,top

h = TH1F("adsf", "asdf", 2, 0, 1)
h.GetXaxis().SetBinLabel(1,"PHYSICS")
h.SetBinContent(1,1)
h.SetBinErrorUp(1,2)
h.SetBinErrorDown(1,-0.5)
h.SetFillColor(kYellow)
h.GetXaxis().SetBinLabel(2,"CALIBRATION")
h.SetBinContent(2,0.5)
h.SetBinError(2,1)
#  h.Fill("CALIBRATION", 0)
#  h.Fill("PHYSICS", 0)
#  h.Fill("PHYSICS", 1)

h.Draw("p E2")

CMSlabel = TLatex()
#  CMSlabel.SetTextSize( 0.08 )
#  CMSlabel.DrawTextNDC(0.7, 0.85, "CMS Internal")
CMSlabel.SetTextFont(63)
CMSlabel.SetTextSize( 30 )
CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")

c1.SaveAs("limitStudiesPlot.pdf")

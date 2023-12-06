import ROOT
from ROOT import TLatex, TLegend, TH1D, TMath
import os
import math
import csv
import sys

ROOT.gROOT.SetBatch(True)
def makePlot(labels, ibinMap):
  fittype=labels[0]
  tag = labels[1]
  year = labels[2]
  # sig = "sig_NMSSM_bbbb_MX_1200_MY_300"
  massGroup = labels[3]
  sig = labels[4]

  # fFit = ROOT.TFile( "FitDiagnostics/{0}/fitDiagnostics2016.root".format("test"))
  # fName = "FitDiagnostics/{0}/{1}/FitDiagnostics_{1}_{2}_id0_sig0.root".format(tag, year, sig)
  # fFit = ROOT.TFile(fName)
  # fitName = "selectionbJets_SignalRegion_CMS_th1x_{0}".format(fittype)
  # theFit = fFit.Get(fitName)

  # fFit.cd("shapes_{0}/selectionbJets_SignalRegion".format(fittype));
  # grDataShape = fFit.Get("shapes_{0}/selectionbJets_SignalRegion/data".format(fittype))
  # hBkgShape = fFit.Get("shapes_{0}/selectionbJets_SignalRegion/data_BTagCSV_dataDriven_kinFit".format(fittype))

  ifile = ROOT.TFile(inputFile)
  ifile.cd("data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion");
  hbkgIN = ifile.Get("data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion/data_BTagCSV_dataDriven_kinFit_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled");
  n_EventsDist = hbkgIN.GetBinContent(hbkgIN.GetMaximumBin())
  hBkgShape_EventsDist = ROOT.TH1D( "hBkgShape_EventsDist", "hBkgShape_EventsDist", int(n_EventsDist), 0, n_EventsDist);
  # hBkgShape_EventsDist = ROOT.TH1D( "hBkgShape_EventsDist", "hBkgShape_EventsDist", 100, 1, n_EventsDist);

  with open(ibinMap) as csvfile:
      binMapping = csv.reader(csvfile, delimiter=',')
      for index,mapmX,mapmY in binMapping:
          i = int(index)
          bkgVal =  hbkgIN.GetBinContent(i)
          # if (125-20<float(mapmY) and float(mapmY)<125+20): continue
          hBkgShape_EventsDist.Fill(bkgVal)

  #### define the canvas
  c1 = ROOT.TCanvas('c1', 'c1',800,600)
  ROOT.gStyle.SetOptStat(0) # remove the stats box
  ROOT.gStyle.SetOptTitle(0) # remove the title

  hBkgShape_EventsDist.Draw("hist")
  # hError.Draw("samef")
  # hBkg.Draw("same l")
  #xaxis
  hBkgShape_EventsDist.GetXaxis().SetRangeUser(0, n_EventsDist+1)
  # axis.SetLimits(xMin, xMax)
  # hBkg.GetXaxis().SetRangeUser(xMin, xMax)
  # hBkgShape_EventsDist.GetXaxis().SetLabelSize(0.)
  # hBkgShape_EventsDist.GetXaxis().SetTitleSize(0.)
  #yaxis
  hBkgShape_EventsDist.GetYaxis().SetTitle("Entries/bin")
  hBkgShape_EventsDist.GetYaxis().SetLabelSize(0.05)
  hBkgShape_EventsDist.GetYaxis().SetTitleSize(0.05)
  hBkgShape_EventsDist.GetYaxis().SetTitleOffset(1.1)
  hBkgShape_EventsDist.GetYaxis().SetTickLength(0.02)
  hBkgShape_EventsDist.GetXaxis().SetTitle("Num. of Events")
  hBkgShape_EventsDist.GetXaxis().SetLabelSize(0.05)
  hBkgShape_EventsDist.GetXaxis().SetTitleSize(0.05)

  hBkgShape_EventsDist.SetLineWidth(2)
  # hError.SetLineColor(0)

  #### define legend
  legName1 = "Orig. Binning"
  if ("binMYx2" in tag): legName1 = "mY bins x2"
  leg = TLegend(0.2,0.75,0.45,0.89)
  leg.AddEntry(hBkgShape_EventsDist, legName1, "l")
  leg.SetBorderSize(0) # remove the border
  leg.SetLineColor(0)
  leg.SetFillColor(0)
  leg.SetTextSize(0.035)
  leg.SetFillStyle(0) # make the legend background transparent
  leg.Draw()

  CMSlabel = TLatex()
  CMSlabel.SetTextFont(63)
  CMSlabel.SetTextSize( 30 )
  CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
  plotlabels = TLatex()
  plotlabels.SetTextFont(63)
  plotlabels.SetTextSize(20)
  #  labelText = "mX = %.0f GeV, mY = %.0f GeV"%(mXval,mYval)
  labelText = ""
  if "VR" in tag:    labelText = labelText + "Validation Region"
  if "CR" in tag:    labelText = labelText + "Control Region"
  if "SR" in tag:    labelText = labelText + "Signal Region"
  plotlabels.DrawLatexNDC(0.60, 0.93, labelText)
  plotlabels = ROOT.TLatex()
  plotlabels.SetTextFont(53)
  plotlabels.SetTextSize(20)
  plotlabels.DrawTextNDC(0.83, 0.93, year)
  plotlabels.SetTextFont(43)
  plotlabels.SetTextSize(20)
  plotlabels.DrawLatexNDC(0.55, 0.85,"Background Model, before fit")
  plotlabels.DrawLatexNDC(0.65, 0.81,massGroup)
  # plotlabels.DrawLatexNDC(0.65, 0.77,labels[2])

  # hBkg.GetXaxis().SetLimits(xMin, xMax)
  # hError.GetXaxis().SetLimits(xMin, xMax)
  ROOT.gPad.Modified()
  ROOT.gPad.Update()

  # ROOT.gPad.Modified()
  # ROOT.gPad.Update()
  odir = "FitDiagnostics/plots_{0}EventDist".format(tag)
  if (not os.path.exists(odir)):
      os.mkdir(odir)
  odir = "FitDiagnostics/plots_{0}EventDist/{1}/".format(tag,fittype)
  if (not os.path.exists(odir)):
      os.mkdir(odir)
  odir = "FitDiagnostics/plots_{0}EventDist/{1}/{2}/".format(tag,fittype,year)
  if (not os.path.exists(odir)):
      os.mkdir(odir)
  saveName = "{0}fitRatio{1}_{2}.pdf".format(odir, sig, year)
  c1.SaveAs(saveName)
  del c1

  # root [15] selectionbJets_SignalRegion_CMS_th1x_prefit->getObject(0)->GetName()
  # (const char *) "h_selectionbJets_SignalRegion"
  # root [16] selectionbJets_SignalRegion_CMS_th1x_prefit->getObject(1)->GetName()
  # (const char *) "pdf_binselectionbJets_SignalRegion_Norm[CMS_th1x]_errorband"
  # root [17] selectionbJets_SignalRegion_CMS_th1x_prefit->getObject(2)->GetName()
  # (const char *) "pdf_binselectionbJets_SignalRegion_Norm[CMS_th1x]_Comp[shapeSig*]"
  # root [18] selectionbJets_SignalRegion_CMS_th1x_prefit->getObject(3)->GetName()
  # (const char *) "pdf_binselectionbJets_SignalRegion_Norm[CMS_th1x]_Comp[shapeBkg*]"
  # root [19] selectionbJets_SignalRegion_CMS_th1x_prefit->getObject(4)->GetName()
  # (const char *) "pdf_binselectionbJets_SignalRegion_Norm[CMS_th1x]"
  # root [20] selectionbJets_SignalRegion_CMS_th1x_prefit->getObject(5)->GetName()
  # (const char *) "h_selectionbJets_SignalRegion"

BinRanges = [0,100,200,300,400,500,600, 700, 800]
sigs = ["sig_NMSSM_bbbb_MX_400_MY_125", "sig_NMSSM_bbbb_MX_700_MY_60", "sig_NMSSM_bbbb_MX_900_MY_600", "sig_NMSSM_bbbb_MX_1200_MY_300", "sig_NMSSM_bbbb_MX_1600_MY_125"]
# tag = "2023Jul5_VR"
# tag="2023Jul5_nonClosureMCStats2_SR" #
tag="2023Jul5_binMYx2_ncMCStats_SR" #
years=["2016", "2017", "2018"]
allfittypes= ["fit_b"]
for afittype in allfittypes:
    for year in years:
        if ("binMYx2" in tag):
            iodir = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_2023Jul5_binMYx2_ncMCStats/".format(year)
        elif("nonClosureMCStats2" in tag):
            iodir = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_2023Jul5_loc/".format(year)
        else:
            print("Exiting. Make sure to have the correct bin mapping")
            sys.exit()
        for i, sig in enumerate(sigs):
            labels = [afittype, tag, year, "Mass Group {}".format(i), sig]
            ifile = iodir + "outPlotter_UnrollLocation_massGroup{0}.txt".format(i)
            inputFile = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}/outPlotter_massGroup{2}.root".format(year, tag, i)
# labels = ["prefit", tag, year, "Mass Group {}".format(0), sig]
            makePlot(labels, ifile)
            # for i in range(1, len(BinRanges)):
            #   makePlot(labels, BinRanges[i-1],BinRanges[i])


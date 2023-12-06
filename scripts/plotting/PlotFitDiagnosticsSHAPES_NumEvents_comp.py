import ROOT
from ROOT import TLatex, TLegend, TH1D, TMath
import os
import math
import csv
import sys

ROOT.gROOT.SetBatch(True)
def makePlot(labels, ibinMap1, ibinMap2, inputFile1, inputFile2):
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

  ifile1 = ROOT.TFile(inputFile1)
  ifile1.cd("data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion");
  hbkgIN1 = ifile1.Get("data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion/data_BTagCSV_dataDriven_kinFit_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled");
  n_EventsDist1 = hbkgIN1.GetBinContent(hbkgIN1.GetMaximumBin())
  hBkgShape_EventsDist1 = ROOT.TH1D( "hBkgShape_EventsDist", "hBkgShape_EventsDist", int(n_EventsDist1), 0, n_EventsDist1);
  # hBkgShape_EventsDist1 = ROOT.TH1D( "hBkgShape_EventsDist", "hBkgShape_EventsDist",100, 1, n_EventsDist1);
  ifile2 = ROOT.TFile(inputFile2)
  ifile2.cd("data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion");
  hbkgIN2 = ifile2.Get("data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion/data_BTagCSV_dataDriven_kinFit_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled");
  n_EventsDist2 = hbkgIN2.GetBinContent(hbkgIN2.GetMaximumBin())
  hBkgShape_EventsDist2 = ROOT.TH1D( "hBkgShape_EventsDist", "hBkgShape_EventsDist", int(n_EventsDist2), 0, n_EventsDist2);
  # hBkgShape_EventsDist2 = ROOT.TH1D( "hBkgShape_EventsDist", "hBkgShape_EventsDist", 100, 1, n_EventsDist2);
  cnt1_all=0
  cnt2_all=0
  cnt1_lt1=0
  cnt2_lt1=0
  cnt1_lt5=0
  cnt2_lt5=0
  cnt1_lt10=0
  cnt2_lt10=0

  with open(ibinMap1) as csvfile:
     binMapping = csv.reader(csvfile, delimiter=',')
     for index,mapmX,mapmY in binMapping:
          cnt1_all+=1
          i = int(index)
          bkgVal =  hbkgIN1.GetBinContent(i)
          # if (125-20<float(mapmY) and float(mapmY)<125+20): continue
          hBkgShape_EventsDist1.Fill(bkgVal)
          if(bkgVal<10):
              cnt1_lt10+=1
              if(bkgVal<5):
                  cnt1_lt5+=1
                  if(bkgVal<1): cnt1_lt1+=1

  with open(ibinMap2) as csvfile:
      binMapping = csv.reader(csvfile, delimiter=',')
      for index,mapmX,mapmY in binMapping:
          cnt2_all+=1
          i = int(index)
          bkgVal =  hbkgIN2.GetBinContent(i)
          # if (125-20<float(mapmY) and float(mapmY)<125+20): continue
          hBkgShape_EventsDist2.Fill(bkgVal)
          # if(bkgVal<1): print("mYx2 binning", mapmX, mapmY)
          if(bkgVal<10):
              cnt2_lt10+=1
              if(bkgVal<5):
                  cnt2_lt5+=1
                  if(bkgVal<1): cnt2_lt1+=1

  #### define the canvas
  c1 = ROOT.TCanvas('c1', 'c1',800,600)
  ROOT.gStyle.SetOptStat(0) # remove the stats box
  ROOT.gStyle.SetOptTitle(0) # remove the title

  hBkgShape_EventsDist2.Draw("hist")
  hBkgShape_EventsDist1.Draw("hist same")
  hBkgShape_EventsDist2.Draw("hist same")
  # hError.Draw("samef")
  # hBkg.Draw("same l")
  #xaxis
  hBkgShape_EventsDist1.GetXaxis().SetRangeUser(0, n_EventsDist2+1)
  hBkgShape_EventsDist2.GetXaxis().SetRangeUser(0, n_EventsDist2+1)
  maxYrange = hBkgShape_EventsDist1.GetBinContent(hBkgShape_EventsDist1.GetMaximumBin())
  hBkgShape_EventsDist1.GetYaxis().SetRangeUser(0, maxYrange*1.2)
  hBkgShape_EventsDist2.GetYaxis().SetRangeUser(0, maxYrange*1.2)
  # axis.SetLimits(xMin, xMax)
  # hBkg.GetXaxis().SetRangeUser(xMin, xMax)
  # hBkgShape_EventsDist.GetXaxis().SetLabelSize(0.)
  # hBkgShape_EventsDist.GetXaxis().SetTitleSize(0.)
  #yaxis
  hBkgShape_EventsDist1.GetYaxis().SetTitle("Entries/bin")
  hBkgShape_EventsDist1.GetYaxis().SetLabelSize(0.05)
  hBkgShape_EventsDist1.GetYaxis().SetTitleSize(0.05)
  hBkgShape_EventsDist1.GetYaxis().SetTitleOffset(1.1)
  hBkgShape_EventsDist1.GetYaxis().SetTickLength(0.02)
  hBkgShape_EventsDist1.GetXaxis().SetTitle("Num. of Events")
  hBkgShape_EventsDist1.GetXaxis().SetLabelSize(0.05)
  hBkgShape_EventsDist1.GetXaxis().SetTitleSize(0.05)
  hBkgShape_EventsDist2.GetYaxis().SetTitle("Entries/bin")
  hBkgShape_EventsDist2.GetYaxis().SetLabelSize(0.05)
  hBkgShape_EventsDist2.GetYaxis().SetTitleSize(0.05)
  hBkgShape_EventsDist2.GetYaxis().SetTitleOffset(1.1)
  hBkgShape_EventsDist2.GetYaxis().SetTickLength(0.02)
  hBkgShape_EventsDist2.GetXaxis().SetTitle("Num. of Events")
  hBkgShape_EventsDist2.GetXaxis().SetLabelSize(0.05)
  hBkgShape_EventsDist2.GetXaxis().SetTitleSize(0.05)

  hBkgShape_EventsDist1.SetLineWidth(2)
  hBkgShape_EventsDist2.SetLineWidth(2)
  hBkgShape_EventsDist1.SetLineColor(ROOT.kRed+2)
  hBkgShape_EventsDist2.SetLineColor(ROOT.kBlue+2)
  # hError.SetLineColor(0)

  #### define legend
  legName1 = "Orig. Binning"
  legName2 = "mY bins x2"
  leg = TLegend(0.2,0.75,0.45,0.89)
  leg.AddEntry(hBkgShape_EventsDist1, legName1, "l")
  leg.AddEntry(hBkgShape_EventsDist2, legName2, "l")
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
  mXval = sig.split("MX_")[1].split("_MY_")[0]
  mYval = sig.split("MX_")[1].split("_MY_")[1]
  ofileMean1.write("{0},{1},{2:.4f}\n".format(mXval, mYval, hBkgShape_EventsDist1.GetMean()))
  ofileMean2.write("{0},{1},{2:.4f}\n".format(mXval, mYval, hBkgShape_EventsDist2.GetMean()))
  ofilelt1_1.write("{0},{1},{2:.4f}\n".format(mXval, mYval, float(cnt1_lt1)/float(cnt1_all)))
  ofilelt1_2.write("{0},{1},{2:.4f}\n".format(mXval, mYval, float(cnt2_lt1)/float(cnt2_all)))
  ofilelt5_1.write("{0},{1},{2:.4f}\n".format(mXval, mYval, float(cnt1_lt5)/float(cnt1_all)))
  ofilelt5_2.write("{0},{1},{2:.4f}\n".format(mXval, mYval, float(cnt2_lt5)/float(cnt2_all)))
  ofilelt10_1.write("{0},{1},{2:.4f}\n".format(mXval, mYval, float(cnt1_lt10)/float(cnt1_all)))
  ofilelt10_2.write("{0},{1},{2:.4f}\n".format(mXval, mYval, float(cnt2_lt10)/float(cnt2_all)))
  odir = "FitDiagnostics/plots_{0}vs{1}EventDist".format(tag1, tag2)
  if (not os.path.exists(odir)):
      os.mkdir(odir)
  odir = "FitDiagnostics/plots_{0}vs{1}EventDist/{2}/".format(tag1, tag2,fittype)
  if (not os.path.exists(odir)):
      os.mkdir(odir)
  odir = "FitDiagnostics/plots_{0}vs{1}EventDist/{2}/{3}/".format(tag1, tag2,fittype,year)
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
tag1="2023Jul5_nonClosureMCStats2_SR" #
tag2="2023Jul5_binMYx2_ncMCStats_SR" #
years=["2016", "2017", "2018"]
monitor= "mean"
allfittypes= ["fit_b"]
odir_EventDist="FitDiagnostics/EventDist_2023Sep"
for afittype in allfittypes:
    for year in years:
        iodir1 = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_2023Jul5_loc/".format(year)
        iodir2 = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_2023Jul5_binMYx2_ncMCStats/".format(year)
        with open("{0}/{1}_{3}_{2}.txt".format(odir_EventDist, "mean", year, tag1), "w") as ofileMean1,\
                open("{0}/{1}_{3}_{2}.txt".format(odir_EventDist, "mean", year, tag2), "w") as ofileMean2,\
                open("{0}/{1}_{3}_{2}.txt".format(odir_EventDist, "lt1", year, tag1), "w") as ofilelt1_1,\
                open("{0}/{1}_{3}_{2}.txt".format(odir_EventDist, "lt1", year, tag2), "w") as ofilelt1_2,\
                open("{0}/{1}_{3}_{2}.txt".format(odir_EventDist, "lt5", year, tag1), "w") as ofilelt5_1,\
                open("{0}/{1}_{3}_{2}.txt".format(odir_EventDist, "lt5", year, tag2), "w") as ofilelt5_2,\
                open("{0}/{1}_{3}_{2}.txt".format(odir_EventDist, "lt10", year, tag1), "w") as ofilelt10_1,\
                open("{0}/{1}_{3}_{2}.txt".format(odir_EventDist, "lt10", year, tag2), "w") as ofilelt10_2:
            for i, sig in enumerate(sigs):
                labels = [afittype, tag1, year, "Mass Group {}".format(i), sig]
                ibinfile1 = iodir1 + "outPlotter_UnrollLocation_massGroup{0}.txt".format(i)
                ibinfile2 = iodir2 + "outPlotter_UnrollLocation_massGroup{0}.txt".format(i)
                inputFile1 = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}/outPlotter_massGroup{2}.root".format(year, tag1, i)
                inputFile2 = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}/outPlotter_massGroup{2}.root".format(year, tag2, i)
# labels = ["prefit", tag, year, "Mass Group {}".format(0), sig]
                makePlot(labels, ibinfile1, ibinfile2, inputFile1, inputFile2)
                # for i in range(1, len(BinRanges)):
                #   makePlot(labels, BinRanges[i-1],BinRanges[i])


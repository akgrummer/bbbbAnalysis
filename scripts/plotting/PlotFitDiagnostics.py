import ROOT
from ROOT import TLatex, TLegend
import os


ROOT.gROOT.SetBatch(True)
def makePlot(labels,xMin, xMax):
  fittype=labels[0]
  tag = labels[1]
  year = labels[2]
  # sig = "sig_NMSSM_bbbb_MX_1200_MY_300"
  massGroup = labels[3]
  sig = labels[4]

  bkgFlag = ""
  if ("fit_b" in fittype):
      bkgFlag = "_bonly"
  rooFitObjects = {
      "data": "h_selectionbJets_SignalRegion",
      "fitError": "pdf_binselectionbJets_SignalRegion{0}_Norm[CMS_th1x]_errorband".format(bkgFlag),
      "sigFit": "pdf_binselectionbJets_SignalRegion{0}_Norm[CMS_th1x]_Comp[shapeSig*]".format(bkgFlag),
      "bkgFit": "pdf_binselectionbJets_SignalRegion{0}_Norm[CMS_th1x]_Comp[shapeBkg*]".format(bkgFlag),
      "sigPlusBkgFit": "pdf_binselectionbJets_SignalRegion{0}_Norm[CMS_th1x]".format(bkgFlag)
      }
  print(labels)
  print(fittype)
  # fFit = ROOT.TFile( "FitDiagnostics/{0}/fitDiagnostics2016.root".format("test"))
  fName = "FitDiagnostics/{0}/{1}/FitDiagnostics_{1}_{2}_id0_sig0.root".format(tag, year, sig)
  fFit = ROOT.TFile(fName)
  fitName = "selectionbJets_SignalRegion_CMS_th1x_{0}".format(fittype)
  print(fitName)
  theFit = fFit.Get(fitName)
  i=1
  hData = theFit.findObject(rooFitObjects["data"])
  hDataError = theFit.findObject(rooFitObjects["data"])
  hError = theFit.findObject(rooFitObjects["fitError"])
  hBkg = theFit.findObject(rooFitObjects["bkgFit"])

  # hDataPoints = hData.GetN()
  # if (xMax<hDataPoints):
    # for i in range(xMax, hDataPoints):
      # hData.RemovePoint(i)
      # hBkg.RemovePoint(i)
      # hError.RemovePoint(i)
  # if (xMin>0):
    # for i in range(0,xMin):
      # hData.RemovePoint(i)
      # hBkg.RemovePoint(i)
      # hError.RemovePoint(i)

  #### define the canvas
  c1 = ROOT.TCanvas('c1', 'c1',800,600)
  ROOT.gStyle.SetOptStat(0) # remove the stats box
  ROOT.gStyle.SetOptTitle(0) # remove the title

  #### define the upper and lower pads
  p1 = ROOT.TPad("p1", "p1", 0., 0.3, 1., 1.0, 0, 0, 0)
  p1.SetMargin(0.12,0.05,0.05,0.09) #left,right,bottom,top
  p1.SetTicks(1,1)
  p1.Draw()

  p2 = ROOT.TPad("p2", "p2", 0., 0.05, 1., 0.3, 0, 0, 0)
  p2.SetMargin(0.12,0.05,0.38,0.05) #left,right,bottom,top
  p2.SetTicks(1,1)
  p2.Draw()

  p1.cd()
  # p1.DrawFrame(xMin,0,xMax,350);
  hData.Draw()
  hError.Draw("samef")
  hBkg.Draw("same l")
  hData.Draw("same p")
  #hDataError.Draw("same e")
  #xaxis
  hData.GetXaxis().SetRangeUser(xMin, xMax)
  # axis = hData.GetXaxis()
  # axis.SetLimits(xMin, xMax)
  hData.GetXaxis().SetLabelSize(0.)
  hData.GetXaxis().SetTitleSize(0.)
  # hBkg.GetXaxis().SetRangeUser(xMin, xMax)
  hBkg.GetXaxis().SetLabelSize(0.)
  hBkg.GetXaxis().SetTitleSize(0.)
  #yaxis
  hData.GetYaxis().SetTitle("Entries/bin")
  hData.GetYaxis().SetLabelSize(0.05)
  hData.GetYaxis().SetTitleSize(0.05)
  hData.GetYaxis().SetTitleOffset(1.1)
  hData.GetYaxis().SetTickLength(0.02)
  hBkg.GetYaxis().SetTitle("Entries/bin")
  hBkg.GetYaxis().SetLabelSize(0.05)
  hBkg.GetYaxis().SetTitleSize(0.05)
  hBkg.GetYaxis().SetTitleOffset(1.1)
  hBkg.GetYaxis().SetTickLength(0.02)

  hData.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
  hData.SetMarkerSize(0.7)
  hData.SetMarkerColor(1)
  hData.SetLineColor(1)
  hData.SetLineWidth(1)
  hError.SetLineColor(0)

  #### define legend
  leg = TLegend(0.2,0.75,0.45,0.89)
  leg.AddEntry(hData, "Data", "ep")
  leg.AddEntry(hBkg, "Background Fit", "l")
  leg.AddEntry(hError, "Fit Error", "f")
  #  leg.AddEntry(h1, "3b ttbar", "l")
  #  leg.AddEntry(h2, "4b ttbar", "l")
  # leg.AddEntry(h1, "3b Signal MC", "l")
  # leg.AddEntry(h2, "4b Signal MC", "l")
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
  fitLabel = ""
  if ("_b" in fittype):
      fitLabel = "Background Only Fit"
  if ("_s" in fittype):
      fitLabel = "Fit with Signal"
  if ("pre" in fittype):
      fitLabel = "PreFit"
  plotlabels.DrawLatexNDC(0.65, 0.85,fitLabel)
  plotlabels.DrawLatexNDC(0.65, 0.81,massGroup)
  # plotlabels.DrawLatexNDC(0.65, 0.77,labels[2])

#   hDataError.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
#   hDataError.SetMarkerSize(0)
#   hDataError.SetMarkerColor(1)
#   hDataError.SetLineColor(1)
#   hDataError.SetLineWidth(1)

  # hBkg.GetXaxis().SetLimits(xMin, xMax)
  # hError.GetXaxis().SetLimits(xMin, xMax)
  # hData.GetXaxis().SetLimits(xMin, xMax)
  ROOT.gPad.Modified()
  ROOT.gPad.Update()
  # hData.Sumw2()

  # hData.Divide(hBkg)
  # hData.Draw()
  # hData.Draw("same l")

  p2.cd()
  # p2.DrawFrame(xMin,-10,xMax,10);
  hNew = theFit.residHist(rooFitObjects["data"], rooFitObjects["bkgFit"], True)
  hNewPoints = hNew.GetN()
  # if (xMax<hNewPoints):
  #   for i in range(xMax, hNewPoints):
  #     hNew.RemovePoint(i)
  # if (xMin>0):
  #   for i in range(0,xMin):
  #     hNew.RemovePoint(i)
  hNew.Draw()
  # hNew.Draw("same B")
  hNew.Draw("same p")
  hNew.GetXaxis().SetLabelSize(0.15)
  hNew.GetXaxis().SetLabelOffset(0.05)
  hNew.GetYaxis().SetLabelSize(0.12)
  hNew.GetYaxis().SetNdivisions(503)
  hNew.GetXaxis().SetTickLength(0.1)
  hNew.GetXaxis().SetTitleSize(.16)
  hNew.GetXaxis().SetTitleOffset(1.1)
  hNew.GetXaxis().SetTitle("Unrolled Bins (mX-mY)")
  hNew.GetYaxis().SetTickLength(0.03)
  hNew.GetYaxis().SetTitleSize(.12)
  hNew.GetYaxis().SetTitleOffset(0.5)
  hNew.GetYaxis().SetTitle("pull")
  hNew.SetFillColor(38)

  hNew.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
  hNew.SetMarkerSize(0.7)
  hNew.SetMarkerColor(1)
  hNew.SetLineColor(1)
  # hNew.SetLineWidth(0)
  hNew.GetXaxis().SetRangeUser(xMin,xMax)
  # hNew.GetXaxis().SetLimits(xMin, xMax)
  # axis2 = hNew.GetXaxis()
  # axis2.SetLimits(xMin, xMax)
  # ROOT.gPad.Modified()
  # ROOT.gPad.Update()
  odir = "FitDiagnostics/plots_{0}".format(tag)
  if (not os.path.exists(odir)):
      os.mkdir(odir)
  odir = "FitDiagnostics/plots_{0}/{1}/".format(tag,fittype)
  if (not os.path.exists(odir)):
      os.mkdir(odir)
  odir = "FitDiagnostics/plots_{0}/{1}/{2}/".format(tag,fittype,year)
  if (not os.path.exists(odir)):
      os.mkdir(odir)
  saveName = "{0}fitRatio{1}_{2}_bin{3}to{4}.pdf".format(odir, sig, year, xMin,xMax)
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

BinRanges = [0,100,200,300,400,500,600]
sigs = ["sig_NMSSM_bbbb_MX_400_MY_125", "sig_NMSSM_bbbb_MX_700_MY_60", "sig_NMSSM_bbbb_MX_900_MY_600", "sig_NMSSM_bbbb_MX_1200_MY_300", "sig_NMSSM_bbbb_MX_1600_MY_125"]
# sig= "sig_NMSSM_bbbb_MX_400_MY_125"
# labels = ["prefit", "2016", "Mass Group 0", sig]
tag = "2023Jul5_VR"
# tag = "2023Jul5_SR"
years=["2016", "2017", "2018"]
allfittypes= ["fit_b", "fit_s", "prefit"]
for afittype in allfittypes:
    for year in years:
        for i, sig in enumerate(sigs):
            labels = [afittype, tag, year, "Mass Group {}".format(i), sig]
# labels = ["prefit", tag, year, "Mass Group {}".format(0), sig]
            for i in range(1, len(BinRanges)):
              makePlot(labels, BinRanges[i-1],BinRanges[i])

#
# afittype = "fit_b"
# year = "2016"
# sig = "sig_NMSSM_bbbb_MX_400_MY_125"
# labels = [afittype, tag, year, "Mass Group {}".format(0), sig]
# for i in range(1, len(BinRanges)):
#     makePlot(labels, BinRanges[i-1],BinRanges[i])


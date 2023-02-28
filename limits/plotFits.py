import ROOT


ROOT.gROOT.SetBatch(True)
def makePlot(labels, locations, xMin, xMax):
  rooFitObjects = {
      "data": "h_selectionbJets_SignalRegion",
      "fitError": "pdf_binselectionbJets_SignalRegion{}_Norm[CMS_th1x]_errorband".format(locations[3]),
      "sigFit": "pdf_binselectionbJets_SignalRegion{}_Norm[CMS_th1x]_Comp[shapeSig*]".format(locations[3]),
      "bkgFit": "pdf_binselectionbJets_SignalRegion{}_Norm[CMS_th1x]_Comp[shapeBkg*]".format(locations[3]),
      "sigPlusBkgFit": "pdf_binselectionbJets_SignalRegion{}_Norm[CMS_th1x]".format(locations[3])
      }
  fFit = ROOT.TFile( "{}fitDiagnostics{}.root".format(locations[1],locations[2]))
  theFit = fFit.Get("selectionbJets_SignalRegion_CMS_th1x_{}".format(locations[0]))
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
  plotlabels = ROOT.TLatex()
  plotlabels.SetTextFont(43)
  plotlabels.SetTextSize(20)
  plotlabels.DrawLatexNDC(0.65, 0.85,labels[0])
  plotlabels.DrawLatexNDC(0.65, 0.81,labels[1])
  plotlabels.DrawLatexNDC(0.65, 0.77,labels[2])

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
  hNew.GetYaxis().SetTitleOffset(0.3)
  hNew.GetYaxis().SetTitle("pull")
  hNew.SetFillColor(38)

  hNew.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
  hNew.SetMarkerSize(0.7)
  hNew.SetMarkerColor(1)
  hNew.SetLineColor(1)
  # hNew.SetLineWidth(0)
  hNew.GetXaxis().SetRangeUser(xMin,xMax)
  hNew.GetYaxis().SetRangeUser(-5,10)
  # hNew.GetXaxis().SetLimits(xMin, xMax)
  # axis2 = hNew.GetXaxis()
  # axis2.SetLimits(xMin, xMax)
  # ROOT.gPad.Modified()
  # ROOT.gPad.Update()

  saveName = "{}_{}_bin{}to{}.pdf".format(locations[0], locations[2], xMin, xMax)
  c1.SaveAs(locations[1]+saveName)
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
Group = 1
year = 2016
# fitSelect = "Prefit"
# rooFitName = "prefit"
# rooName = ""
# fitSelect = "Background Fit"
# rooFitName = "fit_b"
# rooName = "__model_bonly_"
fitSelect = "Signal+Bkg Fit"
rooFitName = "fit_s"
rooName = ""
labels = [fitSelect, "{}".format(year), "Mass Group {}".format(Group)]
locations = [rooFitName,"localCombineRuns/CombineGoF_2022Oct24_Group{}/".format(Group), "{}Group{}FD".format(year,Group), rooName]
# "fit_b"
# "fit_s"
for i in range(1, len(BinRanges)):
  makePlot(labels, locations, BinRanges[i-1],BinRanges[i])


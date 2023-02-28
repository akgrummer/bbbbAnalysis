from ROOT import TFile, TH1F, TH2F, TCanvas, gStyle, gPad, gDirectory, TLatex, gROOT, PyConfig, TMath, kBlue, TLine, TPad, TLegend, TGraph, TBox, kThermometer
from ROOT import kRed 
# PyConfig.IgnoreCommandLineOptions = False
import numpy as np
import re
import os
from VariableDicts import varInfo

def rootplot_2Dhist(h2d, var1, var2, odir, tag, region, xRange=None, yRange=None, zRange=None):
    h2d = h2d.Clone("h2dCopy")
    odir = odir + "/" + region
    if not (os.path.exists(odir)): os.makedirs(odir) 
    ofileName = "%s/histograms.root"%(odir)
    ofile = TFile.Open ( ofileName, "UPDATE" )
    def CreatePlot(h1, tag):
        c1 = TCanvas('c1', 'c1',800,600)
        gStyle.SetOptStat(0) # remove the stats box
        gStyle.SetOptTitle(0) # remove the title
        gStyle.SetPalette(kThermometer)
        gPad.SetTicks(1,1)
        gPad.SetMargin(0.12,0.16,0.12,0.09) #left,right,bottom,top
        #  p1.SetMargin(0.12,0.05,0.05,0.09) #left,right,bottom,top
        #  p2.SetMargin(0.12,0.05,0.38,0.05) #left,right,bottom,top

        h1.Draw("COLZ1")
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
        h1.GetXaxis().SetTitle(varInfo[var1]['XaxisTitle'])
        h1.GetYaxis().SetTitle(varInfo[var2]['XaxisTitle'])
        # h1.GetZaxis().SetTitle(varInfo[var2]['ZaxisTitle'])

        if(tag is not None and "ratio" in tag):
            if zRange is not None:
                h1.GetZaxis().SetRangeUser(zRange[0],zRange[1])
            h1.GetZaxis().SetTitle("Ratio [target (4b) / model (3b)]")
            plotlabels.SetTextFont(43)
            plotlabels.SetTextSize(16)
            plotlabels.DrawTextNDC(0.3, 0.84, "3b Data reweighted")
        elif(tag is not None and "sigma" in tag):
            #  h1.GetZaxis().SetRangeUser(0,3)
            if zRange is not None:
                h1.GetZaxis().SetRangeUser(zRange[0],zRange[1])
            #  h1.GetZaxis().SetRangeUser(3, 4.)
            #  h1.GetZaxis().SetRangeUser(2, 4.)
            #  h1.GetZaxis().SetRangeUser(1.5, 4.)
            #  h1.GetZaxis().SetRangeUser(-2,2)
            #  h1.GetZaxis().SetRangeUser(-1.5,1.5)
            h1.GetZaxis().SetTitle("Sigma (4b,3b)")
            plotlabels.SetTextFont(43)
            plotlabels.SetTextSize(16)
            plotlabels.DrawTextNDC(0.3, 0.84, "3b Data reweighted")
            #  h1.GetXaxis().SetRangeUser(varInfo[var1]['xlow'],varInfo[var1]['xhigh'])
            #  h1.GetYaxis().SetRangeUser(varInfo[var2]['xlow'],varInfo[var2]['xhigh'])
        elif(tag is not None and "model" in tag):
            #  h1.GetZaxis().SetRangeUser(0.,2.1)
            if zRange is not None:
                h1.GetZaxis().SetRangeUser(zRange[0],zRange[1])
            h1.GetZaxis().SetTitle("3b data (model) Events")
            plotlabels.SetTextFont(43)
            plotlabels.SetTextSize(16)
            plotlabels.DrawTextNDC(0.3, 0.84, "3b Data reweighted")
            #  h1.GetXaxis().SetRangeUser(varInfo[var1]['xlow'],varInfo[var1]['xhigh'])
            #  h1.GetYaxis().SetRangeUser(varInfo[var2]['xlow'],varInfo[var2]['xhigh'])
        elif(tag is not None and "target" in tag):
            if zRange is not None:
                h1.GetZaxis().SetRangeUser(zRange[0],zRange[1])
            h1.GetZaxis().SetTitle("4b data (target) Events")
            plotlabels.SetTextFont(43)
            plotlabels.SetTextSize(16)
            plotlabels.DrawTextNDC(0.3, 0.84, "4b Data")
            #  h1.GetXaxis().SetRangeUser(varInfo[var1]['xlow'],varInfo[var1]['xhigh'])
            #  h1.GetYaxis().SetRangeUser(varInfo[var2]['xlow'],varInfo[var2]['xhigh'])
        elif(tag is "sig4b"):
            if zRange is not None:
                h1.GetZaxis().SetRangeUser(zRange[0],zRange[1])
            else:
                h1.GetZaxis().SetRangeUser(0.,.08)
            plotlabels.SetTextFont(43)
            plotlabels.SetTextSize(16)
            plotlabels.DrawTextNDC(0.3, 0.84, "Signal MC, 4b Events")
            #  h1.GetZaxis().SetTitle("Sig. MC Events")
            #  h1.GetXaxis().SetRangeUser(varInfo[var1]['xlow'],varInfo[var1]['xhigh'])
            #  h1.GetYaxis().SetRangeUser(varInfo[var2]['xlow'],varInfo[var2]['xhigh'])
        elif(tag is "sig4b3bratio"):
            if zRange is not None:
                h1.GetZaxis().SetRangeUser(zRange[0],zRange[1])
            #  h1.GetZaxis().SetRangeUser(0.,.08)
            plotlabels.SetTextFont(43)
            plotlabels.SetTextSize(16)
            plotlabels.DrawTextNDC(0.3, 0.84, "Signal MC, Ratio: 4b/3b ")
            #  h1.GetZaxis().SetTitle("Sig. MC Events")
            #  h1.GetXaxis().SetRangeUser(varInfo[var1]['xlow'],varInfo[var1]['xhigh'])
            #  h1.GetYaxis().SetRangeUser(varInfo[var2]['xlow'],varInfo[var2]['xhigh'])

        elif(tag is "sig3b"):
            if zRange is not None:
                h1.GetZaxis().SetRangeUser(zRange[0],zRange[1])
            else:
                h1.GetZaxis().SetRangeUser(0.,.008)
            plotlabels.SetTextFont(43)
            plotlabels.SetTextSize(16)
            plotlabels.DrawTextNDC(0.3, 0.84, "Signal MC, 3b Events")
            #  h1.GetZaxis().SetTitle("Sig. MC Events")
            #  if "CR" in region: h1.GetZaxis().SetRangeUser(0.,.08)
            #  if "VR" in region: h1.GetZaxis().SetRangeUser(0.,170.)
            #  if "SR" in region: h1.GetZaxis().SetRangeUser(0.,1000.)
            #  h1.GetXaxis().SetRangeUser(varInfo[var1]['xlow'],varInfo[var1]['xhigh'])
            #  h1.GetYaxis().SetRangeUser(varInfo[var2]['xlow'],varInfo[var2]['xhigh'])
        elif(tag is "QCD"):
            if "CR" in region: h1.GetZaxis().SetRangeUser(0.,600.)
            if "VR" in region: h1.GetZaxis().SetRangeUser(0.,170.)
            if "SR" in region: h1.GetZaxis().SetRangeUser(0.,1000.)
            h1.GetZaxis().SetTitle("QCD Events")
        elif(tag is "ttbar"):
            if "CR" in region: h1.GetZaxis().SetRangeUser(0.,8.)
            if "VR" in region: h1.GetZaxis().SetRangeUser(0.,8.)
            if "SR" in region: h1.GetZaxis().SetRangeUser(0.,40.)
            h1.GetZaxis().SetTitle("ttbar Events")
        if xRange is not None:
            h1.GetXaxis().SetRangeUser(xRange[0], xRange[1])
        else:
            h1.GetXaxis().SetRangeUser(varInfo[var1]['xlow'],varInfo[var1]['xhigh'])
        if yRange is not None:
            h1.GetYaxis().SetRangeUser(yRange[0], yRange[1])
        else:
            h1.GetYaxis().SetRangeUser(varInfo[var2]['xlow'],varInfo[var2]['xhigh'])
        c1.SaveAs("%s/mXvsmY_%s.pdf"%(odir,tag))
        del c1
    
    CreatePlot(h2d,tag)
    h2d.Write()
    del h2d
    ofile.Close()

#  def rootplot_2samp_ratio( h1, h2, year, region, var, tag, odir, href, ks2D, ks2DMaxDist ):
def rootplot_2samp_ratio( h1, h2, year, region, var, tag, odir, href, plotlabel ):
    #### get the histograms:
    h1 = h1.Clone("h1copy")
    h2 = h2.Clone("h2copy")
    href = href.Clone("hrefcopy")

    #### normalize the histograms
    #  h1.Sumw2()
    #  h2.Sumw2()
    h1area = h1.Integral()
    h2area = h2.Integral()
    #  print("a bin error %.4f"%(h1.GetBinError(50)))
    #  h1.Scale(1./h1.Integral())
    #  h2.Scale(1./h2.Integral())
    #  href.Scale(1./href.Integral())
    #### define the canvas
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    
    #### define the upper and lower pads
    p1 = TPad("p1", "p1", 0., 0.3, 1., 1.0, 0, 0, 0)
    p1.SetMargin(0.12,0.05,0.05,0.09) #left,right,bottom,top
    p1.SetTicks(1,1)
    p1.Draw()

    p2 = TPad("p2", "p2", 0., 0.05, 1., 0.3, 0, 0, 0)
    p2.SetMargin(0.12,0.05,0.38,0.05) #left,right,bottom,top
    p2.SetTicks(1,1)
    p2.Draw()

    #### draw histograms in upper pad
    p1.cd()
    h1.SetLineColor(kRed+2)
    h1.SetLineWidth(2)
    h2.SetLineColor(kBlue+2)
    h2.SetLineWidth(2)
    h1.Draw("hist")
    h2.Draw("hist same")
    #xaxis
    # h1.GetXaxis().SetRangeUser(varInfo[var]['xlowRange'],varInfo[var]['xhighRange'])
    h1.GetXaxis().SetRangeUser(0,450)
    h1.GetXaxis().SetLabelSize(0.)
    h1.GetXaxis().SetTitleSize(0.)
    # h2.GetXaxis().SetRangeUser(varInfo[ar]['xlowRange'],varInfo[var]['xhighRange'])
    h2.GetXaxis().SetRangeUser(0,450)
    h2.GetXaxis().SetLabelSize(0.)
    h2.GetXaxis().SetTitleSize(0.)
    #yaxis
    h1.GetYaxis().SetTitle("Events/bin")
    h1.GetYaxis().SetLabelSize(0.05)
    h1.GetYaxis().SetTitleSize(0.05)
    h1.GetYaxis().SetTitleOffset(1.1)
    h1.GetYaxis().SetTickLength(0.02)
    h2.GetYaxis().SetTitle(varInfo[var]['YaxisTitle'])
    h2.GetYaxis().SetLabelSize(0.05)
    h2.GetYaxis().SetTitleSize(0.05)
    h2.GetYaxis().SetTitleOffset(1.1)
    h2.GetYaxis().SetTickLength(0.02)
    #  if h2.GetMaximum()>h1.GetMaximum():
    yrangeFactor = 1.3
    if var == "HH_kinFit_m": yrangeFactor = 1.57
    h1.GetYaxis().SetRangeUser(0,np.max( [ h1.GetMaximum(), h2.GetMaximum(), href.GetMaximum() ] )*yrangeFactor)
    
    ### KStest and AD test
    ksval = "KS Test: %.4f"%h1.KolmogorovTest(h2)
    # print("KS test, UO %e"%h1.KolmogorovTest(h2, "UO"))
    ksvalMaxDist= "KS Test, Max Dist.: %.4f"%h1.KolmogorovTest(h2, "M")
    # print("KS test, normalized %e"%h1.KolmogorovTest(h2, "N"))
    ksvalX = "KS Test, pseudoX: %.4f"%h1.KolmogorovTest(h2, "X")
    # print("AD test %e"%h1.AndersonDarlingTest(h2))
    # print("AD test, normalized %e"%h1.AndersonDarlingTest(h2, "T"))
    CMSlabel = TLatex()
    #  CMSlabel.SetTextSize( 0.08 )
    #  CMSlabel.DrawTextNDC(0.7, 0.85, "CMS Internal")
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 30 )
    CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")

    KSlabel = TLatex()
    KSlabel.SetTextFont( 43 )
    KSlabel.SetTextSize( 12 )
    KSlabel.DrawTextNDC(0.72, 0.7, ksval)
    KSlabel.DrawTextNDC(0.72, 0.66, ksvalMaxDist)
    KSlabel.DrawTextNDC(0.72, 0.62, ksvalX)

    plotlabels = TLatex()
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    #  labelText = "mX = %.0f GeV, mY = %.0f GeV"%(mXval,mYval)
    labelText = ""
    if "VR" in region:    labelText = labelText + "Validation Region"
    if "CR" in region:    labelText = labelText + "Control Region"
    plotlabels.DrawLatexNDC(0.65, 0.93, labelText)
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(16)
    if "weights" in tag:    plotlabels.DrawTextNDC(0.72, 0.75, "3b reweighted")
    if "orig" in tag:    plotlabels.DrawTextNDC(0.72, 0.75, "before 3b reweighting")
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(14)
    # plotlabels.DrawLatexNDC(0.35, 0.85, "Mass Cut around mX=600, mY=400")
    plotlabels.DrawLatexNDC(0.35, 0.85, plotlabel)
    plotlabels.SetTextFont(43)
    plotlabels.SetTextSize(12)
    plotlabels.DrawLatexNDC(0.15, 0.85, "3b Integral: %0.4f"%(h1area))
    plotlabels.DrawLatexNDC(0.15, 0.81, "4b Integral: %0.4f"%(h2area))
    #  plotlabels.SetTextFont( 42 )
    #  plotlabels.SetTextSize( 0.03 )
    #  plotlabels.DrawLatexNDC(0.15, 0.77, "mX-mY 2D KS Test: %0.4f"%(ks2D))
    #  plotlabels.DrawLatexNDC(0.15, 0.73, "mX-mY 2D KS Test Max Dist.: %0.4f"%(ks2DMaxDist))

    #  plotlabels.DrawLatexNDC(0.35, 0.81, "BDT trained in mass window")
    #  plotlabels.DrawLatexNDC(0.35, 0.81, "BDT trained in mass window, with ptX")
    #  plotlabels.DrawLatexNDC(0.35, 0.81, "BDT trained in mass window, using only mX and mY")
    #  plotlabels.DrawLatexNDC(0.35, 0.81, "BDT trained in mass window, without mX and mY")
    #
    #  plotlabels.SetTextFont(63)
    #  plotlabels.SetTextSize(20)
    #  plotlabels.DrawLatexNDC(0.35, 0.78, "TTBAR")
    #  plotlabels.DrawLatexNDC(0.35, 0.78, "Signal MC")
    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(20)
    plotlabels.DrawTextNDC(0.88, 0.93, year)

    #### define legend
    leg = TLegend(0.7,0.79,0.95,0.89)
    #  leg.AddEntry(h1, "3b data (bkg. model)", "l")
    #  leg.AddEntry(h2, "4b data (target)", "l")
    #  leg.AddEntry(h1, "3b ttbar", "l")
    #  leg.AddEntry(h2, "4b ttbar", "l")
    leg.AddEntry(h1, "3b Signal MC", "l")
    leg.AddEntry(h2, "4b Signal MC", "l")
    leg.SetBorderSize(0) # remove the border
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.035)
    leg.SetFillStyle(0) # make the legend background transparent
    leg.Draw()

    #### draw the ratio hist in lower pad
    p2.cd()
    hErrors = h1.Clone("hErrors")
    #  for i in xrange( b)
    h3 = h2.Clone("h3")
    h3.Divide(h1)
    h4 = h1.Clone("h4")
    #  print("number of bins, 3b: ", h1.GetSize())
    #  print("a bin error %.4f"%(h1.GetBinError(50)))
    for i in range(h1.GetSize()):
        h4.SetBinContent(i, 1+h1.GetBinError(i))
        #  print(h1.GetBinError(i))
    h3.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
    h3.SetMarkerSize(0.7)
    h3.SetMarkerColor(1)
    h3.SetLineColor(1)
    h4.SetFillColor(17)
    h4.SetLineColor(17)
    h4.SetBarWidth(1.)
    h3.Draw("p") # draw as data points
    #  h4.Draw("line same")

    LineAtOne = TLine(varInfo[var]['xlowRange'],1.,varInfo[var]['xhighRange'],1.) #x1,y1,x2,y2
    LineAtOne.SetLineWidth(2)
    LineAtOne.SetLineColor(1)
    LineAtOne.SetLineStyle(9)
    LineAtOne.Draw()
    h3.GetYaxis().SetRangeUser(varInfo[var]['xlowRatioRange'],varInfo[var]['xhighRatioRange'])
    h4.GetYaxis().SetRangeUser(varInfo[var]['xlowRatioRange'],varInfo[var]['xhighRatioRange'])
    h3.GetXaxis().SetLabelSize(0.15)
    h3.GetXaxis().SetLabelOffset(0.05)
    h3.GetYaxis().SetLabelSize(0.12)
    h3.GetYaxis().SetNdivisions(503)
    h3.GetXaxis().SetTickLength(0.1)
    h3.GetXaxis().SetTitleSize(.16)
    h3.GetXaxis().SetTitleOffset(1.1)
    h3.GetXaxis().SetTitle(varInfo[var]['XaxisTitle'])
    h3.GetYaxis().SetTickLength(0.03)
    h3.GetYaxis().SetTitleSize(.12)
    h3.GetYaxis().SetTitleOffset(0.3)
    h3.GetYaxis().SetTitle("target / model")
    odir = odir + "/" + region
    if not (os.path.exists(odir)): os.makedirs(odir) 
    #  odirpng = odir + "/png"
    #  if not (os.path.exists(odirpng)): os.makedirs(odirpng)
    c1.SaveAs("%s/%s_%s.pdf"%( odir   , var, tag ))
    #  c1.SaveAs("%s/%s_%s.png"%( odirpng, var, tag ))

def makeplotsForRegion(dir_region, region, odir, year, ifileTag, plotlabel):
    #  idir = "2017DataPlots_NMSSM_XYH_bbbb_dataDrivenStudies_aidan_2021Dec15"
    #  idir = "DataPlots_fullSubmission_2016_v34_aidan_rebinnned_2021Dec23_VR"
    # full mass region, full BDT
    #  idir = "DataPlots_fullSubmission_%s_v34_aidan_2022Jan26_VR"%(year) # outPlotter.root is the same for CR and VR (normal binning)
    # mass window restriction, full BDT
    #  idir = "%sDataPlots_2022Feb2_masswindow"%(year)
    #  BDT in mass window
    #  idir = "VarPlots/rootHists/%sDataPlots_2022Feb8_BDTmasscut"%(year)
    # BDT in mass window, BDT with ptX
    #  idir = "VarPlots/rootHists/%sDataPlots_2022Feb8_BDTmasscut_ptX"%(year)
    # BDT in mass window, BDT using only mX,mY
    #  idir = "VarPlots/rootHists/%sDataPlots_2022Mar2_only_mXmY"%(year) # outPlotter.root is the same for CR and VR (normal binning)
    # BDT in mass window, BDT without mX,mY
    #  idir = "VarPlots/rootHists/%sDataPlots_2022Mar2_without_mXmY"%(year) # outPlotter.root is the same for CR and VR (normal binning)
    # TTBAR closure plots (in Mass Window):
    #  idir = "VarPlots/rootHists/%sDataPlots_2022Mar4_fullBDT_withTTBAR"%(year) # outPlotter.root is the same for CR and VR (normal binning)
    #  idir = "VarPlots/rootHists/%sDataPlots_2022Mar4_fullBDT_withTTBAR_allvars"%(year) # outPlotter.root is the same for CR and VR (normal binning)
    # TTBAR closure plots with and *without* 3b wieghts (in Mass Window):
    #  idir = "VarPlots/rootHists/%sDataPlots_2022Mar4_fullBDT_withTTBAR_allvars_3b"%(year) # outPlotter.root is the same for CR and VR (normal binning)
    # TTBAR closure plots with and *without* 3b wieghts, with Signal MC and Signal MC- 3b scaled
    #  idir = "VarPlots/rootHists/%sDataPlots_2022Mar4_fullBDT_withTTBAR_MassWindow_3b_sig"%(year) # outPlotter.root is the same for CR and VR (normal binning)
    #no ttbar:
    #  idir = "VarPlots/rootHists/%sDataPlots_2022Mar17_fullBDT_TTBAR_MassWindow_data"%(year) # outPlotter.root is the same for CR and VR (normal binning)
    # full mass window, btag loose selection on 4th jet in 3b jets

    #  idir = "DataPlots_fullSubmission_%s_v34_aidan_2022Jan26_VR"%(year, ifileTag) # outPlotter.root is the same for CR and VR (normal binning)
    if "2022Jan26" in ifileTag:
        idir = "DataPlots_fullSubmission_{0}_v34_aidan_{1}".format(year, ifileTag) # outPlotter.root is the same for CR and VR (normal binning)
        print(idir)
    #  idir = "VarPlots/rootHists/fullSubmission_2022July/{0}DataPlots_2022Jul7_fullBDT_bJetScoreLoose"%(year) # outPlotter.root is the same for CR and VR (normal binning)
    else:
        idir = "VarPlots/rootHists/fullSubmission_2022July/{0}DataPlots_{1}".format(year,ifileTag) # outPlotter.root is the same for CR and VR (normal binning)
        #  idir = "VarPlots/rootHists/fullSubmission_2022July/%sDataPlots_2022Jul14_fullBDT_bJetScore1p5"%(year) # outPlotter.root is the same for CR and VR (normal binning)
        #  idir = "VarPlots/rootHists/fullSubmission_2022July/{0}DataPlots_{1}"%(year,ifileTag) # outPlotter.root is the same for CR and VR (normal binning)
    #  odir = odir + "MassWindow/"
    #  odir = odir + "All/"
    odir = odir + year
    myfile = TFile.Open(idir + "/outPlotter.root")
    dir_ttbar_3b = "ttbar_3b"
    dir_ttbar_3b_weights = "ttbar_3bScaled"
    dir_ttbar_4b = "ttbar"
    dir_data_3b = "data_BTagCSV_3btag"
    dir_data_4b = "data_BTagCSV"
    dir_data_3b_weights = "data_BTagCSV_dataDriven_kinFit" 
    dir_QCD = "QCD"
    #  varname = "_HH_kinFit_m_H2_m"
        
    dir_sig_MX_600_MY_400 = "sig_NMSSM_bbbb_MX_600_MY_400" # signal
    dir_sig_MX_300_MY_60 = "sig_NMSSM_bbbb_MX_300_MY_60" # signal
    dir_sig_MX_300_MY_150 = "sig_NMSSM_bbbb_MX_300_MY_150" # signal
    dir_sig_3b_weights = "sig_NMSSM_bbbb_MX_600_MY_400_3bScaled"
    #  varlist = [ "H1_b1_ptRegressed", "H1_b2_ptRegressed", "H1_b1_kinFit_ptRegressed", "H1_b2_kinFit_ptRegressed", "H2_b1_ptRegressed", "H2_b2_ptRegressed", "H1_b1_deepCSV", "H1_b2_deepCSV", "H2_b1_deepCSV", "H2_b2_deepCSV", "H1_pt", "H1_kinFit_pt", "H2_pt", "HH_m", "HH_kinFit_m", "HH_pt", "HH_kinFit_pt", "H1_m", "H2_m", "H1_eta", "H1_kinFit_eta", "H2_eta", "H1_bb_DeltaR", "H1_kinFit_bb_DeltaR", "H2_bb_DeltaR", "H1_H2_sphericity", "FourBjet_sphericity", "distanceFromDiagonal" ]
    #  varlist = [ "H1_b1_kinFit_ptRegressed", "H1_b2_kinFit_ptRegressed", "H2_b1_ptRegressed", "H2_b2_ptRegressed", "H1_kinFit_pt", "H2_pt", "HH_kinFit_m", "HH_kinFit_pt", "H2_m", "H1_kinFit_eta", "H2_eta", "H1_kinFit_bb_DeltaR", "H2_bb_DeltaR", "distanceFromDiagonal" ]
    #  "H1_kinFit_m",
    varlist = [ "H2_m", "HH_kinFit_m"]
    varlist2D = [ "H1_m_H2_m", "HH_m_H2_m", "HH_kinFit_m_H2_m" ]

    #  masspoint_list = [ "MX_1800_MY_800" ]
    masspoint_list = "MX_600_MY_400"
    sigdirHeader = "sig_NMSSM_bbbb_"
    #  sigDirectory = "selectionbJets_SignalRegion"
    #  for masspoint in masspoint_list:
    #  myfile.cd(sigdirHeader+masspoint+"/"+sigDirectory)
    #  tag = "test"
    #  h_sig = gDirectory.Get(sigdirHeader+masspoint+"_"+sigDirectory+varname)

##################################################
# for QCD and ttbar mx vs my 2D hists
##################################################
    #  myfile.cd(dir_QCD+"/"+dir_region)
    #  h_3b_mXmY2D_QCD = gDirectory.Get(dir_QCD+"_"+dir_region+"_"+"HH_kinFit_m_H2_m")
    #  rootplot_2Dhist(h_3b_mXmY2D_QCD, "HH_kinFit_m", "H2_m", odir, "QCD", region)
    #  myfile.cd(dir_ttbar+"/"+dir_region)
    #  h_3b_mXmY2D_ttbar = gDirectory.Get(dir_ttbar+"_"+dir_region+"_"+"HH_kinFit_m_H2_m")
    #  rootplot_2Dhist(h_3b_mXmY2D_ttbar, "HH_kinFit_m", "H2_m", odir, "ttbar", region)
##################################################

##################################################
# for signal ratios
##################################################
    myfile.cd(dir_sig_MX_600_MY_400 +"/"+dir_region)
    h_sig_MX_600_MY_400  = gDirectory.Get(dir_sig_MX_600_MY_400 +"_"+dir_region+"_"+"HH_kinFit_m_H2_m")
    myfile.cd(dir_sig_MX_300_MY_150+"/"+dir_region)
    h_sig_MX_300_MY_150  = gDirectory.Get(dir_sig_MX_300_MY_150 +"_"+dir_region+"_"+"HH_kinFit_m_H2_m")
    myfile.cd(dir_sig_MX_300_MY_60+"/"+dir_region)
    h_sig_MX_300_MY_60  = gDirectory.Get(dir_sig_MX_300_MY_60 +"_"+dir_region+"_"+"HH_kinFit_m_H2_m")
    #  rootplot_2Dhist(h_sig, "HH_kinFit_m_massWindow", "H2_m_massWindow", odir, "sig4b", region)
    rootplot_2Dhist(h_sig_MX_600_MY_400, "HH_kinFit_m", "H2_m", odir, "sig4b_600_MY_400", region)
    rootplot_2Dhist(h_sig_MX_600_MY_400, "HH_kinFit_m", "H2_m", odir, "sig4b_600_MY_400_zoom", region, xRange=[0.,450.], yRange=[0.,400.])
    rootplot_2Dhist(h_sig_MX_300_MY_150, "HH_kinFit_m", "H2_m", odir, "sig4b_300_MY_150", region)
    rootplot_2Dhist(h_sig_MX_300_MY_150, "HH_kinFit_m", "H2_m", odir, "sig4b_300_MY_150_zoom", region, xRange=[0.,450.], yRange=[0.,400.])
    rootplot_2Dhist(h_sig_MX_300_MY_60, "HH_kinFit_m", "H2_m", odir, "sig4b_300_MY_60", region)
    rootplot_2Dhist(h_sig_MX_300_MY_60, "HH_kinFit_m", "H2_m", odir, "sig4b_300_MY_60_zoom", region, xRange=[0.,450.], yRange=[0.,400.])
    #  myfile.cd(dir_sig_3b_weights+"/"+dir_region)
    #  h_sig_3b = gDirectory.Get(dir_sig_3b_weights+"_"+dir_region+"_"+"HH_kinFit_m_H2_m")
    #  rootplot_2Dhist(h_sig_3b, "HH_kinFit_m_massWindow", "H2_m_massWindow", odir, "sig3b", region)
    #  h_ratio = h_sig.Clone("h4b3bRatio")
    #  h_ratio.Divide(h_sig_3b)
    #  rootplot_2Dhist(h_ratio, "HH_kinFit_m_massWindow", "H2_m_massWindow", odir, "sig4b3bratio", region)
##################################################

##################################################
# for 2D histo ratios 4b/3b
# ##################################################
    #  myfile.cd(dir_data_3b+"/"+dir_region)
    #  h_3b_mXmY2D = gDirectory.Get(dir_data_3b+"_"+dir_region+"_"+"HH_kinFit_m_H2_m")
    #  rootplot_2Dhist(h_3b_mXmY2D, "HH_kinFit_m_massWindow", "H2_m_massWindow", odir, "", region)

    myfile.cd(dir_data_3b_weights+"/"+dir_region)
    h_3b_weights_mXmY2D = gDirectory.Get(dir_data_3b_weights+"_"+dir_region+"_"+"HH_kinFit_m_H2_m")
    rootplot_2Dhist(h_3b_weights_mXmY2D, "HH_kinFit_m", "H2_m", odir, "model", region)
    rootplot_2Dhist(h_3b_weights_mXmY2D, "HH_kinFit_m", "H2_m", odir, "model_massWindow", region, xRange=[0.,400.], yRange=[0.,500.])

    myfile.cd(dir_data_4b+"/"+dir_region)
    h_4b_mXmY2D = gDirectory.Get(dir_data_4b+"_"+dir_region+"_"+"HH_kinFit_m_H2_m")
    rootplot_2Dhist(h_4b_mXmY2D, "HH_kinFit_m", "H2_m", odir, "target", region)
    rootplot_2Dhist(h_4b_mXmY2D, "HH_kinFit_m", "H2_m", odir, "target_massWindow", region, xRange=[0.,400.], yRange=[0.,500.])

    h_ratio = h_4b_mXmY2D.Clone("h4b3bRatio")
    h_ratio.Divide(h_3b_weights_mXmY2D)
    rootplot_2Dhist(h_ratio, "HH_kinFit_m", "H2_m", odir, "ratio_threshold", region, zRange=[1.3,2.1])
    rootplot_2Dhist(h_ratio, "HH_kinFit_m", "H2_m", odir, "ratio_threshold_massWindow", region, xRange=[300.,400.], yRange=[100.,500.], zRange=[1.3,2.1])
    rootplot_2Dhist(h_ratio, "HH_kinFit_m", "H2_m", odir, "ratio", region, zRange=[0.,8.])
    rootplot_2Dhist(h_ratio, "HH_kinFit_m", "H2_m", odir, "ratio_massWindow", region, zRange=[0.,2.5], xRange=[0.,400.], yRange=[0.,500.])

    hsigma = h_4b_mXmY2D.Clone("hsigma")
    #  for i in range(1,hsigma.GetSize()-1):
    h_4b_mXmY2D.Add(h_3b_weights_mXmY2D,-1)
    #  herr = h_4b_mXmY2D.Clone("herr")
    for i in range(h_4b_mXmY2D.GetNcells()):
       if h_4b_mXmY2D.GetBinError(i) != 0:
           hsigma.SetBinContent(i,h_4b_mXmY2D.GetBinContent(i)/h_4b_mXmY2D.GetBinError(i))
    #  for i in range(0,hsigma.GetNcells()):
       #  hError.SetBinContent(i,h_ratio.GetBinError(i))
       #  #  hsigma.SetBinContent(i, abs(h_ratio.GetBinContent(i)-1))
       #  hsigma.SetBinContent(i, h1.GetBinContent(i)-1)
    #  hsigma.Divide(hError)
    rootplot_2Dhist(hsigma, "HH_kinFit_m", "H2_m", odir, "sigma_abs", region, zRange=[-2.5,2.5])
    rootplot_2Dhist(hsigma, "HH_kinFit_m", "H2_m", odir, "sigma_abs_massWindow", region, zRange=[-2.5,2.5], xRange=[0.,400.], yRange=[0.,500.])
           #  h1.GetZaxis().SetRangeUser(3, 4.)
           #  h1.GetZaxis().SetRangeUser(2, 4.)
           #  h1.GetZaxis().SetRangeUser(1.5, 4.)
           #  h1.GetZaxis().SetRangeUser(-2,2)
           #  h1.GetZaxis().SetRangeUser(-1.5,1.5)
    #  rootplot_2Dhist(hsigma, "HH_kinFit_m_massWindow", "H2_m_massWindow", odir, "sigma_abs_thresh_2", region)
    #  rootplot_2Dhist(hsigma, "HH_kinFit_m_massWindow", "H2_m_massWindow", odir, "sigma_abs_thresh_1p5", region)
    #  rootplot_2Dhist(hsigma, "HH_kinFit_m_massWindow", "H2_m_massWindow", odir, "sigma_thresh_2", region)
    #  rootplot_2Dhist(hsigma, "HH_kinFit_m_massWindow", "H2_m_massWindow", odir, "sigma_thresh_1p5", region)
# ##################################################
# 
#     #  myfile.cd(dir_data_3b+"/"+dir_region)
#     #  h_3b_mXmY2D = gDirectory.Get(dir_data_3b+"_"+dir_region+"_"+"HH_kinFit_m_H2_m")
#     #  myfile.cd(dir_data_3b_weights+"/"+dir_region)
#     #  h_3b_weights_mXmY2D = gDirectory.Get(dir_data_3b_weights+"_"+dir_region+"_"+"HH_kinFit_m_H2_m")
#     #  myfile.cd(dir_data_4b+"/"+dir_region)
#     #  h_4b_mXmY2D = gDirectory.Get(dir_data_4b+"_"+dir_region+"_"+"HH_kinFit_m_H2_m")
# 
#     #  h_3b_weights_mXmY2D.Scale(h_4b_mXmY2D.Integral()/h_3b_weights_mXmY2D.Integral())
#     #  ksval_2D = h_3b_mXmY2D.KolmogorovTest(h_4b_mXmY2D, "D")
#     #  ksvalMaxDist_2D = h_3b_mXmY2D.KolmogorovTest(h_4b_mXmY2D, "M")
#     #  ksvalX_2D = "KS Test, pseudoX = %.4f"%h_3b_mXmY2D.KolmogorovTest(h_4b_mXmY2D, "X")
# 
#     #  ksval_2D_weights = h_3b_weights_mXmY2D.KolmogorovTest(h_4b_mXmY2D, "ND")
#     #  ksvalMaxDist_2D_weights = h_3b_weights_mXmY2D.KolmogorovTest(h_4b_mXmY2D, "M")
#     #  ksvalX_2D_weights = "KS Test, pseudoX = %.4f"%h_3b_mXmY2D.KolmogorovTest(h_4b_mXmY2D, "X")
# 
##################################################
#  # data plots
    for varname in varlist:
    #  varname = "H1_b1_kinFit_ptRegressed"
        myfile.cd(dir_data_3b+"/"+dir_region)
        h_3b = gDirectory.Get(dir_data_3b+"_"+dir_region+"_"+varname)
        myfile.cd(dir_data_3b_weights+"/"+dir_region)
        h_3b_weights = gDirectory.Get(dir_data_3b_weights+"_"+dir_region+"_"+varname)
        #  print("h_3b_weights bin error %.4f"%(h_3b_weights.GetBinError(50)))
        myfile.cd(dir_data_4b+"/"+dir_region)
        h_4b = gDirectory.Get(dir_data_4b+"_"+dir_region+"_"+varname)
        #  rootplot_2samp_ratio( h_3b        , h_4b, year, region, varname, "orig"   , odir, h_3b_weights, ksval_2D, ksvalMaxDist_2D)
        #  rootplot_2samp_ratio( h_3b_weights, h_4b, year, region, varname, "weights", odir, h_3b,         ksval_2D_weights, ksvalMaxDist_2D_weights )
        rootplot_2samp_ratio( h_3b        , h_4b, year, region, varname, "orig"   , odir, h_3b_weights , plotlabel)
        rootplot_2samp_ratio( h_3b_weights, h_4b, year, region, varname, "weights", odir, h_3b         , plotlabel)
##################################################
    #  #ttbar plots
    #  for varname in varlist:
    #  #  varname = "H1_b1_kinFit_ptRegressed"
        #  myfile.cd(dir_ttbar_3b + "/" + dir_region)
        #  h_3b = gDirectory.Get(dir_ttbar_3b+"_"+dir_region+"_"+varname)
        #  #  print("Integral: %0.4f"% (h_3b_weights.Integral("width")))
        #  #  print("Entries: %0.4f"% (h_3b_weights.GetEntries()))
        #  myfile.cd(dir_ttbar_3b_weights+"/"+dir_region)
        #  h_3b_weights = gDirectory.Get(dir_ttbar_3b_weights+"_"+dir_region+"_"+varname)
        #  myfile.cd(dir_ttbar_4b+"/"+dir_region)
        #  h_4b = gDirectory.Get(dir_ttbar_4b+"_"+dir_region+"_"+varname)
        #  #  print("Integral: %0.4f"% (h_3b_weights.Integral("width")))
        #  #  print("Entries: %0.4f"% (h_3b_weights.GetEntries()))
        #  rootplot_2samp_ratio( h_3b        , h_4b, year, region, varname, "orig"   , odir, h_3b_weights )
        #  rootplot_2samp_ratio( h_3b_weights, h_4b, year, region, varname, "weights", odir, h_3b         )
##################################################

##################################################
    # signal MC
    #  for varname in varlist:
    #  #  varname = "h1_b1_kinfit_ptregressed"
        #  myfile.cd(dir_sig_3b_weights+"/"+dir_region)
        #  h_3b_weights = gdirectory.get(dir_sig_3b_weights+"_"+dir_region+"_"+varname)
        #  myfile.cd(dir_sig +"/"+dir_region)
        #  h_4b = gDirectory.Get(dir_sig +"_"+dir_region+"_"+varname)
        #  #  print("Integral: %0.4f"% (h_3b_weights.Integral()))
        #  rootplot_2samp_ratio( h_3b_weights, h_4b, year, region, varname, "weights"   , odir, h_3b_weights )
        #  #  rootplot_2samp_ratio( h_3b        , h_4b, year, region, varname, "orig"   , odir, h_3b_weights )
        #  #  rootplot_2samp_ratio( h_3b_weights, h_4b, year, region, varname, "weights", odir, h_3b         )
##################################################

# ********************
#run pyROOT in batch mode  - ie don't show graphics!
# 
gROOT.SetBatch(True)
# ********************
# MOVED `studies/plotting2021Dec13 to `VarPlots/plotting2021Dec13`
# odir = "studies/plotting2021Dec13/plots2021Dec16_2"
# odir = "studies/plotting2021Dec13/plots2021Dec17"
#  odir = "studies/plotting2021Dec13/plots2021Dec23"
#  odir = "studies/plotting2021Dec13/plots2022Jan27"
#  odir = "studies/plotting2021Dec13/plots2022Jan28"
#  odir = "studies/varPlots/plots2022Feb2/"

#  odir = "VarPlots/FullMassRegionFullBDT2022Jan26/" # the 2022Jan26 doesn't have all of the variables in the branches, need to rerun fillhistograms.exe without the mass window cut
#  odir = "VarPlots/New2022Feb9/"
#  odir = "VarPlots/FullBDT2022Feb2/"
#  odir = "VarPlots/BDTmasscut_2022Feb8/"
#  odir = "VarPlots/BDTmasscut_ptX_2022Feb8/"
#  odir = "VarPlots/FullBDT2022Feb11/"
#  odir = "VarPlots/FullBDT2022Mar9/"
#  odir = "VarPlots/sig_2D_2022Mar24/"
#  odir = "VarPlots/data_2D_2022Mar25/"
#  odir = "VarPlots/data_2D_2022Apr4/"
#  odir = "VarPlots/2022Jun22/"
# odir = "VarPlots/2022July29/"
#  odir = "VarPlots/2022Aug12/"
# odir = "VarPlots/2022Aug30/"
odir = "VarPlots/2022Sep27_mx300slice/"
#  odir = "VarPlots/BDTmasscut_2022Feb11/"
#  odir = "VarPlots/BDTmasscut_ptX_2022Feb11/"
#  odir = "VarPlots/FullBDTandMassWindow2022Mar3/"
#  odir = "VarPlots/BDTmasscut_only_mXmY2022Mar3/"
#  odir = "VarPlots/BDTmasscut_without_mXmY2022Mar3/"
#  odir = "VarPlots/TTbarClosure2022Mar4/"
#  odir = "VarPlots/TTbarClosure2022Mar7/"
#  odir = "VarPlots/TTbarClosure2022Mar9/"
#  odir = "VarPlots/SignalClosure2022Mar7/"
odiro = odir
#  if not (os.path.exists(odir)): os.makedirs(odir)
years = ["2016","2017","2018"]
#  years = ["2018"]
# !!!!!!!!!!! CAREFUL using Signal Region! !!!!!!!!!!! only for MC
#  directories = ["selectionbJets_SignalRegion"]
#  regionTag = ["SR"]
# !!!!!!!!!!! CAREFUL using Signal Region! !!!!!!!!!!! only for MC
# ##################################################
# for data
directories = ["selectionbJets_ControlRegionBlinded", "selectionbJets_ValidationRegionBlinded"]
regionTag = ["CR", "VR"]
#  iTag="2022Jan26_VR"
#  iTag="2022Jul7_fullBDT_bJetScoreLoose"
#  iTag="2022Jul14_fullBDT_bJetScore1p5"
# iTags = ["2022Jan26_VR", "2022Jul7_fullBDT_bJetScoreLoose", "2022Jul14_fullBDT_bJetScore1p5"]
# iTags = {"2022Sep14_Mx300_bJetLoose_3": "212<mX<400 GeV; depth 4, leafs=300",  "2022Jul7_fullBDT_bJetScoreLoose":  "full mass plane; depth 4, leafs=300", "2022Sep14_Mx300_bJetLoose_mx280cut":  "280<mX<400 GeV; depth 4, leafs=300",  "2022Sep14_Mx300_bJetLoose_depth2_leafs50":  "212<mX<400 GeV; depth 2, leafs=50"}
iTags = {
        "2022Sep14_Mx300_bJetLoose_3": "212<mX<400 GeV; depth 4, leafs=300", 
        "2022Jul7_fullBDT_bJetScoreLoose":  "full mass plane; depth 4, leafs=300",
        "2022Sep14_Mx300_bJetLoose_mx280cut":  "280<mX<400 GeV; depth 4, leafs=300",
        "2022Sep14_Mx300_bJetLoose_depth2_leafs50":  "212<mX<400 GeV; depth 2, leafs=50", 
        "2022Sep14_Mx300_bJetLoose_depth4_leafs50_3": "212<mX<400 GeV; depth 4, leafs=50"
}
  #  "2022Sep14_Mx300_bJetLoose_depth4_leafs50_3": "212<mX<400 GeV; depth 4, leafs=50"
for iTag, plotlabel in iTags.items():
   for year in years:
       for i, directory in enumerate(directories):
           #  odir = "studies/plotting2021Dec13/plots2022Jan27/%s"%(year)
           #  year = "2016"
           #  directory = "selectionbJets_ControlRegionBlinded"
           #  makeplotsForRegion(directory, "CR", odir,year)
           #  directory = "selectionbJets_ValidationRegionBlinded"
           makeplotsForRegion(directory, regionTag[i], odir+iTag+"/", year, iTag, plotlabel)
# ##################################################
################################################
#  for MC
#  !!!!!!!!!!! CAREFUL using Signal Region! !!!!!!!!!!! only for MC
#  directories = ["selectionbJets_ControlRegionBlinded", "selectionbJets_ValidationRegionBlinded", "selectionbJets_SignalRion"]
#  regionTag = ["CR", "VR", "SR"]
#  #  iTag="2022Jan26_VR"
#  #  iTag="2022Jul7_fullBDT_bJetScoreLoose"
#  iTag="2022Jul14_fullBDT_bJetScore1p5"
#  for year in years:
    #  # for i, directory in enumerate(directories):
    #  # odir = "studies/plotting2021Dec13/plots2022Jan27/%s"%(year)
    #  # year = "2016"
    #  # directory = "selectionbJets_ControlRegionBlinded"
    #  # makeplotsForRegion(directory, "CR", odir,year)
    #  directory = "selectionbJets_SignalRegion"
    #  makeplotsForRegion(directory, regionTag[2], odir+iTag+"/", year, iTag)


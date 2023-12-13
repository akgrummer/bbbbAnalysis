import ROOT
from ROOT import TFile, TH1F, TH2F, TCanvas, gStyle, gPad, gDirectory, TLatex, gROOT, PyConfig, TMath, kBlue, TLine, TPad, TLegend, TGraph, TBox, kThermometer, THStack
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
        mXval = tag.split("MX_")[1]
        mXval = mXval.split("_")[0]
        mYval = tag.split("MY_")[1]
        mYval = mYval.split("_")[0]
        labelText = "mX = %.0f GeV, mY = %.0f GeV"%(float(mXval),float(mYval))
        plotlabels.DrawLatexNDC(0.20, 0.8, labelText)
        labelText=""
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
def rootplot_2samp_ratio( h1, h2, year, region, var, tag, odir, href ):
    #### get the histograms:
    h4 = h2.Clone("h4")
    #  print("number of bins, 3b: ", h1.GetSize())
    #  print("a bin error %.4f"%(h1.GetBinError(50)))
    for i in range(h1.GetSize()):
        if (h4.GetBinContent(i)>0): h4.SetBinError(i,h4.GetBinError(i)/h4.GetBinContent(i))
        else: h4.SetBinError(i,0)
        # h4.SetBinContent(i,1)

    h3 = h2.Clone("h3")
    for i in range(h3.GetSize()):
        if (h3.GetBinContent(i)>0): h3.SetBinError(i,h3.GetBinError(i)/h3.GetBinContent(i))
        else: h3.SetBinError(i,0)
        h3.SetBinContent(i,1)
    h1 = h1.Clone("h1copy")
    h2 = h2.Clone("h2copy")
    href = href.Clone("hrefcopy")

    #### normalize the histograms
    #  h1.Sumw2()
    #  h2.Sumw2()
    h1area = h1.Integral(0,-1)
    h2area = h2.Integral(0,-1)
    #  print("a bin error %.4f"%(h1.GetBinError(50)))
    for i in range(h1.GetSize()):
        h1.SetBinContent(i, h1.GetBinContent(i)/h1.GetBinWidth(i))
        h2.SetBinContent(i, h2.GetBinContent(i)/h2.GetBinWidth(i))
    h1.Scale(1./h1.Integral())
    h2.Scale(1./h2.Integral())
    href.Scale(1./href.Integral())
    #### define the canvas
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title

    c1.SetMargin(0.12,0.05,0.12,0.09) #left,right,bottom,top
    c1.SetTicks(1,1)

    #### draw histograms in upper pad
    h1.SetLineColor(kRed+2)
    h1.SetLineWidth(2)
    h2.SetLineColor(kBlue+2)
    h2.SetLineWidth(2)
    h1.Draw("hist")
    h2.Draw("hist same")
    #xaxis

    mXval = tag.split("MX_")[1]
    mXval = mXval.split("_")[0]
    mYval = tag.split("MY_")[1]
    mYval = mYval.split("_")[0]
    # print("mX value", float(mXval))
    h1.GetXaxis().SetRangeUser(0, float(mXval)+float(mXval)*0.4)
    h1.GetXaxis().SetLabelSize(0.04)
    h1.GetXaxis().SetTitleSize(0.04)
    h1.GetXaxis().SetTitle(varInfo[var]['XaxisTitle'] )
    # h2.GetXaxis().SetRangeUser(varInfo[var]['xlowRange'],varInfo[var]['xhighRange'])
    h2.GetXaxis().SetLabelSize(0.04)
    h2.GetXaxis().SetTitleSize(0.04)
    h2.GetXaxis().SetTitle(varInfo[var]['XaxisTitle'] )
    #yaxis
    h1.GetYaxis().SetTitle(varInfo[var]['YaxisTitle'] + "/(bin width)")
    h1.GetYaxis().SetLabelSize(0.04)
    h1.GetYaxis().SetTitleSize(0.04)
    h1.GetYaxis().SetTitleOffset(1.3)
    h1.GetYaxis().SetTickLength(0.02)
    h2.GetYaxis().SetTitle(varInfo[var]['YaxisTitle']+"/(bin width)")
    h2.GetYaxis().SetLabelSize(0.04)
    h2.GetYaxis().SetTitleSize(0.04)
    h2.GetYaxis().SetTitleOffset(1.1)
    h2.GetYaxis().SetTickLength(0.02)
    #  if h2.GetMaximum()>h1.GetMaximum():
    yrangeFactor = 1.3
    if var == "HH_kinFit_m": yrangeFactor = 1.57
    #  h1.GetYaxis().SetRangeUser(0,np.max( [ h1.GetMaximum(), h2.GetMaximum(), href.GetMaximum() ] )*yrangeFactor)
    h1.GetYaxis().SetRangeUser(0,np.max( [ h2.GetMaximum()] )*yrangeFactor)

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
    if "weights" in tag:
        plotlabels.DrawTextNDC(0.72, 0.70, "3b reweighted")
        print(year +labelText+ "3b Reweightied Integral: %0.4f, 4b Integral: %0.4f "%(h1area, h2area))
    if "orig" in tag:
        plotlabels.DrawTextNDC(0.72, 0.70, "before 3b reweighting")
        print(year+labelText+ "3b orig Integral: %0.4f, 4b Integral: %0.4f "%(h1area, h2area))
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(14)
    #  plotlabels.DrawLatexNDC(0.35, 0.85, "Mass Cut around mX=600, mY=400")
    plotlabels.SetTextFont(43)
    plotlabels.SetTextSize(15)
    plotlabels.SetTextAlign(32);
    plotlabels.DrawLatexNDC(0.45, 0.85, "without kinFit Mean = {0:.2f}".format(h1.GetMean()))
    plotlabels.DrawLatexNDC(0.45, 0.81, "with kinFit Mean = {0:.2f}".format(h2.GetMean()))
    plotlabels.DrawLatexNDC(0.45, 0.77, "without kinFit Std. Dev. = {0:.2f}".format(h1.GetStdDev()))
    plotlabels.DrawLatexNDC(0.45, 0.73, "with kinFit Std. Dev. = {0:.2f}".format(h2.GetStdDev()))
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
    leg = TLegend(0.7,0.75,0.95,0.89)
    leg.AddEntry(h1, "without kinFit", "l")
    leg.AddEntry(h2, "with kinFit", "l")
    #  leg.AddEntry(h1, "3b ttbar", "l")
    #  leg.AddEntry(h2, "4b ttbar", "l")
    # leg.AddEntry(h1, "3b Signal MC", "l")
    # leg.AddEntry(h2, "4b Signal MC", "l")
    leg.SetBorderSize(0) # remove the border
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.025)
    leg.SetFillStyle(0) # make the legend background transparent
    leg.Draw()

    odir = odir + "/" + region
    if not (os.path.exists(odir)): os.makedirs(odir)
    #  odirpng = odir + "/png"
    #  if not (os.path.exists(odirpng)): os.makedirs(odirpng)
    c1.SaveAs("%s/%s_%s.pdf"%( odir   , var, tag ))
    #  c1.SaveAs("%s/%s_%s.png"%( odirpng, var, tag ))

def makeplotsForRegion(dir_region, region, odir, year, ifileTag):
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
        # idir = "VarPlots/rootHists/fullSubmission_2022July/{0}DataPlots_{1}".format(year,ifileTag) # outPlotter.root is the same for CR and VR (normal binning)
        idir = "VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}".format(year,ifileTag) # outPlotter.root is the same for CR and VR (normal binning)
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
    dir_data_3b_weights_down = "data_BTagCSV_dataDriven_kinFit_down"
    dir_data_3b_weights_up = "data_BTagCSV_dataDriven_kinFit_up"
    dir_QCD = "QCD"
    #  varname = "_HH_kinFit_m_H2_m"

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
    varname1 = "HH_m"
    varname2 = "HH_kinFit_m"
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
                     "sig_NMSSM_bbbb_MX_1000_MY_150",
                     ]
    # for sigDir in signalDirList:
    # #  varname = "H1_b1_kinFit_ptRegressed"
    #     myfile.cd(sigDir+"/"+dir_region)
    #     h1 = gDirectory.Get(sigDir+"_"+dir_region+"_"+varname1)
    #     h2 = gDirectory.Get(sigDir+"_"+dir_region+"_"+varname2)
    #     rootplot_2samp_ratio( h1, h2, year, region, varname2, sigDir, odir, h2 )
##################################################
    # signal MC
    varlist2D = "HH_kinFit_m_H2_m"
    # for varname in varlist:
    for sigDir in signalDirList:
        myfile.cd(sigDir +"/"+dir_region)
        h_4b = gDirectory.Get(sigDir+"_"+dir_region+"_"+varlist2D)
        rootplot_2Dhist( h_4b,  "HH_kinFit_m","H2_m", odir, sigDir,  region, xRange=[300,1000], yRange=[0,800])
        if ("MX_1000" in sigDir): rootplot_2Dhist( h_4b,  "HH_kinFit_m","H2_m", odir, sigDir,  region, xRange=[300,1400], yRange=[0,400])
        #  rootplot_2samp_ratio( h_3b        , h_4b, year, region, varname, "orig"   , odir, h_3b_weights )
        #  rootplot_2samp_ratio( h_3b_weights, h_4b, year, region, varname, "weights", odir, h_3b         )
##################################################

gROOT.SetBatch(True)
odir = "VarPlots/2023Dec7_signal_2d/"
odiro = odir
years = ["2016","2017","2018"]
#  years = ["2018"]
# !!!!!!!!!!! CAREFUL using Signal Region! !!!!!!!!!!! only for MC
#  directories = ["selectionbJets_SignalRegion"]
#  regionTag = ["SR"]
# !!!!!!!!!!! CAREFUL using Signal Region! !!!!!!!!!!! only for MC
# ##################################################
# for data
# directories = ["selectionbJets_ControlRegionBlinded", "selectionbJets_ValidationRegionBlinded", "selectionbJets_SignalRegion"]
# regionTag = ["CR", "VR", "SR"]
# directories = ["selectionbJets_ControlRegionBlinded", "selectionbJets_ValidationRegionBlinded"]
directories = ["selectionbJets_SignalRegion"]
regionTag = ["SR"]
#  iTag="2022Jan26_VR"
#  iTag="2022Jul7_fullBDT_bJetScoreLoose"
#  iTag="2022Jul14_fullBDT_bJetScore1p5"
# iTags = ["2022Jan26_VR", "2022Jul7_fullBDT_bJetScoreLoose", "2022Jul14_fullBDT_bJetScore1p5"]
#  iTags = ["2022Sep14_Mx300_bJetLoose_3"]
# iTags = ["2022Jul7_fullBDT_bJetScoreLoose"]
# iTags = ["2022Nov14_bJetScoreLoose_shapes2"]
iTags = ["2023Dec7_binMYx2_addMX650_10ev"]
for iTag in iTags:
   for year in years:
       for i, directory in enumerate(directories):
           #  odir = "studies/plotting2021Dec13/plots2022Jan27/%s"%(year)
           #  year = "2016"
           #  directory = "selectionbJets_ControlRegionBlinded"
           #  makeplotsForRegion(directory, "CR", odir,year)
           #  directory = "selectionbJets_ValidationRegionBlinded"
           makeplotsForRegion(directory, regionTag[i], odir+iTag+"/", year, iTag)
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


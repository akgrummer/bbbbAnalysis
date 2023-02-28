from ROOT import TFile, TH1F, TH2F, TCanvas, gStyle, gPad, gDirectory, TLatex, gROOT, PyConfig, TMath, kBlue, TLine, TPad, TLegend, TGraph, TBox
from ROOT import kRed, kGreen, kBlack, TObject 
# PyConfig.IgnoreCommandLineOptions = False
import numpy as np
import pandas as pd
import re
import os
from VariableDicts import varInfo

def rootplot_2samp_ratio( h1, h2, year, region, var, tag, odir, hsig, href ):
    #### get the histograms:
    h1 = h1.Clone("h1copy")
    h2 = h2.Clone("h2copy")
    hsig = hsig.Clone("hsigcopy")

    #### normalize the histograms
    #  h1.Sumw2()
    #  h2.Sumw2()
    #  hsig.Sumw2()
    #  href.Sumw2()
    h1area = h1.Integral()
    h2area = h2.Integral()
    #  print("a bin error %.4f"%(h1.GetBinError(50)))
    #  h1.Scale(1./h1.Integral())
    #  h2.Scale(1./h2.Integral())
    #  hsig.Scale(1./hsig.Integral())
    if("_sig" in tag):
        hsig.Scale(h2.Integral()/hsig.Integral())
        hsig.Scale(0.15)
    hsigarea = hsig.Integral()
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
    if("_sig" in tag): hsig.SetLineColor(kGreen+2)
    if("_ttbar" in tag): hsig.SetLineColor(kBlack)
    hsig.SetLineWidth(2)
    h1.Draw("hist")
    h2.Draw("hist same")
    hsig.Draw("hist same")
    #xaxis
    h1.GetXaxis().SetRangeUser(varInfo[var]['xlowRange'],varInfo[var]['xhighRange'])
    h1.GetXaxis().SetLabelSize(0.)
    h1.GetXaxis().SetTitleSize(0.)
    h2.GetXaxis().SetRangeUser(varInfo[var]['xlowRange'],varInfo[var]['xhighRange'])
    h2.GetXaxis().SetLabelSize(0.)
    h2.GetXaxis().SetTitleSize(0.)
    hsig.GetXaxis().SetRangeUser(varInfo[var]['xlowRange'],varInfo[var]['xhighRange'])
    hsig.GetXaxis().SetLabelSize(0.)
    hsig.GetXaxis().SetTitleSize(0.)
    #yaxis
    h1.GetYaxis().SetTitle(varInfo[var]['YaxisTitle'])
    h1.GetYaxis().SetLabelSize(0.05)
    h1.GetYaxis().SetTitleSize(0.05)
    h1.GetYaxis().SetTitleOffset(1.1)
    h1.GetYaxis().SetTickLength(0.02)
    h2.GetYaxis().SetTitle(varInfo[var]['YaxisTitle'])
    h2.GetYaxis().SetLabelSize(0.05)
    h2.GetYaxis().SetTitleSize(0.05)
    h2.GetYaxis().SetTitleOffset(1.1)
    h2.GetYaxis().SetTickLength(0.02)
    hsig.GetYaxis().SetTitle(varInfo[var]['YaxisTitle'])
    hsig.GetYaxis().SetLabelSize(0.05)
    hsig.GetYaxis().SetTitleSize(0.05)
    hsig.GetYaxis().SetTitleOffset(1.1)
    hsig.GetYaxis().SetTickLength(0.02)
    #  if h2.GetMaximum()>h1.GetMaximum():
    yrangeFactor = 1.3
    if var == "HH_kinFit_m": yrangeFactor = 1.57
    h1.GetYaxis().SetRangeUser(0,np.max( [ h1.GetMaximum(), h2.GetMaximum(), hsig.GetMaximum(), href.GetMaximum() ] )*yrangeFactor)
    
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
    #  KSlabel.DrawTextNDC(0.72, 0.62, ksvalX)

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
    #  if "weights" in tag:    plotlabels.DrawTextNDC(0.72, 0.75, "3b reweighted")
    #  if "orig" in tag:    plotlabels.DrawTextNDC(0.72, 0.75, "before 3b reweighting")
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(14)
    plotlabels.DrawLatexNDC(0.35, 0.85, "Mass Cut around mX=600, mY=400")
    plotlabels.SetTextFont(43)
    plotlabels.SetTextSize(12)
    plotlabels.DrawLatexNDC(0.15, 0.85, "3b Integral: %0.4f"%(h1area))
    plotlabels.DrawLatexNDC(0.15, 0.81, "4b Integral: %0.4f"%(h2area))
    if ("_sig" in tag): plotlabels.DrawLatexNDC(0.15, 0.77, "Sig. Integral: %0.4f, %0.2f of 4b"%(hsigarea, hsigarea/h2area))
    elif("_ttbar" in tag): plotlabels.DrawLatexNDC(0.15, 0.77, "TTBAR Integral: %0.4f"%(hsigarea))
    #  plotlabels.SetTextFont( 42 )
    #  plotlabels.SetTextSize( 0.03 )
    #  plotlabels.DrawLatexNDC(0.15, 0.77, "mX-mY 2D KS Test: %0.4f"%(ks2D))
    #  plotlabels.DrawLatexNDC(0.15, 0.73, "mX-mY 2D KS Test Max Dist.: %0.4f"%(ks2DMaxDist))

    #  plotlabels.DrawLatexNDC(0.35, 0.81, "BDT trained in mass window")
    #  plotlabels.DrawLatexNDC(0.35, 0.81, "BDT trained in mass window, with ptX")
    #  plotlabels.DrawLatexNDC(0.35, 0.81, "BDT trained in mass window, using only mX and mY")
    #  plotlabels.DrawLatexNDC(0.35, 0.81, "BDT trained in mass window, without mX and mY")
    if("ttbarAdj" in tag): plotlabels.DrawLatexNDC(0.35, 0.81, "TTBAR adjusted background")
    #
    #  plotlabels.SetTextFont(63)
    #  plotlabels.SetTextSize(20)
    #  plotlabels.DrawLatexNDC(0.35, 0.78, "TTBAR")
    #  plotlabels.DrawLatexNDC(0.35, 0.78, "Signal MC")
    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(20)
    plotlabels.DrawTextNDC(0.88, 0.93, year)

    #### define legend
    leg = TLegend(0.7,0.74,0.95,0.89)
    leg.AddEntry(h1, "3b data (bkg. model)", "l")
    leg.AddEntry(h2, "4b data (target)", "l")
    if ("_sig" in tag): leg.AddEntry(hsig, "Signal", "l")
    if ("_ttbar" in tag): leg.AddEntry(hsig, "ttbar", "l")
    #  leg.AddEntry(h1, "3b ttbar", "l")
    #  leg.AddEntry(h2, "4b ttbar", "l")
    #  leg.AddEntry(h1, "3b Signal MC", "l")
    #  leg.AddEntry(h2, "4b Signal MC", "l")
    leg.SetBorderSize(0) # remove the border
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.035)
    leg.SetFillStyle(0) # make the legend background transparent
    leg.Draw()

    #### draw the ratio hist in lower pad
    p2.cd()
    #  hErrors = h1.Clone("hErrors")
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
    h_Sigma = h3.Clone("h_Sigma")
    hError = h3.Clone("hError")
    for i in range(1,hsig.GetSize()-1):
        hError.SetBinContent(i,h3.GetBinError(i))
        h_Sigma.SetBinContent(i, h3.GetBinContent(i)-1)
    h_Sigma.Divide(hError)
    #  h3.Draw("p") # draw as data points
    h_Sigma.Draw("hist p") # draw as data points
    #  h4.Draw("line same")

    #  LineAtOne = TLine(varInfo[var]['xlowRange'],1.,varInfo[var]['xhighRange'],1.) #x1,y1,x2,y2
    #  LineAtOne.SetLineWidth(2)
    #  LineAtOne.SetLineColor(1)
    #  LineAtOne.SetLineStyle(9)
    #  LineAtOne.Draw()
    Line3sigma = TLine(varInfo[var]['xlowRange'],1.5,varInfo[var]['xhighRange'],1.5) #x1,y1,x2,y2
    Line3sigma.SetLineWidth(1)
    Line3sigma.SetLineColor(67)
    Line3sigma.SetLineStyle(9)
    Line3sigma.Draw()
    Linem3sigma = TLine(varInfo[var]['xlowRange'],-1.5,varInfo[var]['xhighRange'],-1.5) #x1,y1,x2,y2
    Linem3sigma.SetLineWidth(1)
    Linem3sigma.SetLineColor(67)
    Linem3sigma.SetLineStyle(9)
    Linem3sigma.Draw()
    h_Sigma.GetYaxis().SetRangeUser(varInfo[var]['xlowRatioRange'],varInfo[var]['xhighRatioRange'])
    h4.GetYaxis().SetRangeUser(varInfo[var]['xlowRatioRange'],varInfo[var]['xhighRatioRange'])
    h_Sigma.GetXaxis().SetLabelSize(0.15)
    h_Sigma.GetXaxis().SetLabelOffset(0.05)
    h_Sigma.GetYaxis().SetLabelSize(0.12)
    h_Sigma.GetYaxis().SetNdivisions(503)
    h_Sigma.GetXaxis().SetTickLength(0.1)
    h_Sigma.GetXaxis().SetTitleSize(.16)
    h_Sigma.GetXaxis().SetTitleOffset(1.1)
    h_Sigma.GetXaxis().SetTitle(varInfo[var]['XaxisTitle'])
    h_Sigma.GetYaxis().SetTickLength(0.03)
    h_Sigma.GetYaxis().SetTitleSize(.12)
    h_Sigma.GetYaxis().SetTitleOffset(0.3)
    #  h3.GetYaxis().SetTitle("target / model")
    h_Sigma.GetYaxis().SetTitle("Sigma (4b,3b)")
    odir = odir + "/" + region
    if not (os.path.exists(odir)): os.makedirs(odir) 
    #  odirpng = odir + "/png"
    #  if not (os.path.exists(odirpng)): os.makedirs(odirpng)
    c1.SaveAs("%s/%s_%s.pdf"%( odir   , var, tag ))
    #  c1.SaveAs("%s/%s_%s.png"%( odirpng, var, tag ))

def reorderHistBins(h_in,binThreshold, ratioThreshold):
    df = pd.DataFrame(columns = ["bin", "value0", "error0"])
    for i in range(1, h_in[0][0].GetSize()-1):# range adjusted to avoid looking at underflow and overflow
        temporary_df = pd.DataFrame([[i, h_in[0][0].GetBinContent(i),h_in[0][0].GetBinError(i)]], columns=['bin', 'value0','error0'])
        df = df.append(temporary_df, ignore_index=True)
    for k in range(1, len(h_in)):
        for j in range(len(h_in[k])):
            df_temp2 = pd.DataFrame(columns = ["value%i"%(100*j+k), 'error%i'%(100*j+k)])
            for i in range(1, h_in[k][j].GetSize()-1):# range adjusted to avoid looking at underflow and overflow
                temporary_df = pd.DataFrame([[h_in[k][j].GetBinContent(i), h_in[k][j].GetBinError(i)]], columns=['value%i'%(100*j+k), 'error%i'%(100*j+k)])
                df_temp2 = df_temp2.append(temporary_df, ignore_index=True)
            df = pd.concat([df,df_temp2], axis=1)
    #  print(df.loc[:]["value0"].to_string())
    df = df.sort_values(by=['value0'], ascending=False)
    df = df.reset_index(drop=True)
    #  print(df)
    for k in range(1, len(h_in)):
        for j in range(len(h_in[k])):
            h_in[k][j].Reset("ICESM")
            for i in range(1, h_in[k][j].GetSize()-1):# range adjusted to avoid looking at underflow and overflow
                if ((i<=binThreshold or binThreshold == -1) and df.loc[i-1]["value1"]<ratioThreshold and df.loc[i-1]["value1"]>(0-ratioThreshold) ):
                    h_in[k][j].SetBinContent(i,df.loc[i-1]["value%i"%(100*j+k)])
                    h_in[k][j].SetBinError(i,df.loc[i-1]["error%i"%(100*j+k)])
                else:
                    h_in[k][j].SetBinContent(i,0)
                    h_in[k][j].SetBinError(i,0)
    return h_in

def compareUnrolled(dir_region, region, year, massGroup, odir, varname, itag, binThreshold,ratioThreshold):
    odir = odir +year
    histname = "HH_kinFit_m_H2_m_Rebinned_Unrolled"
    ifileName = ""
    if ("VR" in region): ifileName = "VarPlots/rootHists/%sDataPlots_2022Mar17_fullBDT_TTBAR_MassWindow_data_VR/outPlotter_massGroup%i.root"%(year,massGroup)
    if("CR" in region): ifileName = "VarPlots/rootHists/%sDataPlots_2022Mar17_fullBDT_TTBAR_MassWindow_data/outPlotter_massGroup%i.root"%(year,massGroup)
    #  ifileName = "VarPlots/rootHists/%sDataPlots_2022Mar17_fullBDT_TTBAR_MassWindow_data/outPlotter_massGroup0.root"%(year)
    #  ofileName = ifileName.replace("2022Mar17_fullBDT_TTBAR_MassWindow_data", "2022Mar25_binsReordered")
    #  ofileName = ifileName.replace("2022Mar17_fullBDT_TTBAR_MassWindow_data", "2022Mar25_binsReordered")
    #  ofileName = ifileName.replace("2022Mar17_fullBDT_TTBAR_MassWindow_data", "2022Mar29_binsReordered"+itag)
    #  ofileName = ifileName.replace("2022Mar17_fullBDT_TTBAR_MassWindow_data", "2022Mar29_DATAbinsReordered"+itag)
    ofileName = ifileName.replace("2022Mar17_fullBDT_TTBAR_MassWindow_data", "2022Apr1_binsReordered_sigma"+itag)
    ofileDir = ofileName.rsplit('/', 1)[0]
    if not (os.path.exists(ofileDir)): os.makedirs(ofileDir) 
    #  print (ifileName)
    #  print (ofileName)
    #  print (ofileDir)
    ifile = TFile.Open(ifileName)
    ofile = TFile.Open(ofileName, "RECREATE")

    ## dir names
    dir_ttbar_3b = "ttbar_3b"
    dir_ttbar_3b_weights = "ttbar_3bScaled"
    dir_ttbar_4b = "ttbar"
    dir_ttbar_up = "ttbar_up"
    dir_ttbar_down = "ttbar_down"
    dir_data_3b = "data_BTagCSV_3btag"
    dir_data_4b = "data_BTagCSV"
    dir_3bScaled = "data_BTagCSV_dataDriven_kinFit" 
    dir_QCD = "QCD"
    #  varname = "_HH_kinFit_m_H2_m"
    dir_sig = "sig_NMSSM_bbbb_MX_600_MY_400" # signal
    dir_sig_3b_weights = "sig_NMSSM_bbbb_MX_600_MY_400_3bScaled"

    ## variable names
    #  varlist = [ "H1_b1_ptRegressed", "H1_b2_ptRegressed", "H1_b1_kinFit_ptRegressed", "H1_b2_kinFit_ptRegressed", "H2_b1_ptRegressed", "H2_b2_ptRegressed", "H1_b1_deepCSV", "H1_b2_deepCSV", "H2_b1_deepCSV", "H2_b2_deepCSV", "H1_pt", "H1_kinFit_pt", "H2_pt", "HH_m", "HH_kinFit_m", "HH_pt", "HH_kinFit_pt", "H1_m", "H2_m", "H1_eta", "H1_kinFit_eta", "H2_eta", "H1_bb_DeltaR", "H1_kinFit_bb_DeltaR", "H2_bb_DeltaR", "H1_H2_sphericity", "FourBjet_sphericity", "distanceFromDiagonal" ]
    #  varlist = [ "H1_b1_kinFit_ptRegressed", "H1_b2_kinFit_ptRegressed", "H2_b1_ptRegressed", "H2_b2_ptRegressed", "H1_kinFit_pt", "H2_pt", "HH_kinFit_m", "HH_kinFit_pt", "H2_m", "H1_kinFit_eta", "H2_eta", "H1_kinFit_bb_DeltaR", "H2_bb_DeltaR", "distanceFromDiagonal" ]
    #  "H1_kinFit_m",
    varlist = [ "H2_m", "HH_kinFit_m"]
    varlist2D = [ "H1_m_H2_m", "HH_m_H2_m", "HH_kinFit_m_H2_m" ]
#get histograms
    #  #  ifile.cd(dir_3bScaled+"/"+dir_region)
    #  h_3b_weights = ifile.Get(dir_3bScaled+"/"+dir_region+"/"+dir_3bScaled+"_"+dir_region+"_"+histname)
    #  #  ifile.cd(dir_3bScaled+"_"+dir_ttbar_down+"/"+dir_region)
    #  h_bkgModel_ttbar_down = ifile.Get(dir_3bScaled+"_"+dir_ttbar_down+"/"+dir_region+"/"+dir_3bScaled+"_"+dir_ttbar_down+"_"+dir_region+"_"+histname)
    #  #  ifile.cd(dir_data_4b+"/"+dir_region)
    #  h_4b = ifile.Get(dir_data_4b+"/"+dir_region+"/"+dir_data_4b+"_"+dir_region+"_"+histname)
    #  #  ifile.cd(dir_sig+"/"+dir_region)
    #  h_sig = ifile.Get(dir_sig+"/"+dir_region+"/"+dir_sig+"_"+dir_region+"_"+histname)
    #  #  ifile.cd(dir_ttbar_3b_weights+"/"+dir_region)
    #  h_ttbar = ifile.Get(dir_ttbar_3b_weights+"/"+dir_region+"/"+dir_ttbar_3b_weights+"_"+dir_region+"_"+histname)
    #  ihists = [h_sig_NMSSM_bbbb_MX_600_MY_400, h_data_BTagCSV, h_data_BTagCSV_3btag, h_data_BTagCSV_dataDriven_kinFit, h_data_BTagCSV_dataDriven_kinFit_up, h_sig_NMSSM_bbbb_MX_600_MY_400_jes_Total_up, h_sig_NMSSM_bbbb_MX_600_MY_400_jes_Total_down, h_sig_NMSSM_bbbb_MX_600_MY_400_jer_up, h_sig_NMSSM_bbbb_MX_600_MY_400_jer_down, h_sig_NMSSM_bbbb_MX_600_MY_400_bjer_up, h_sig_NMSSM_bbbb_MX_600_MY_400_bjer_down, h_ggF_Hbb, h_VBF_Hbb, h_sig_NMSSM_bbbb_MX_600_MY_400_3bScaled, h_ttbar, h_ZH, h_ttbar_3bScaled, h_data_BTagCSV_dataDriven_kinFit_down, h_ttbar_3b, h_ZZ, h_ttH, h_WH, h_QCD, h_data_BTagCSV_dataDriven_kinFit_ttbar_up, h_data_BTagCSV_dataDriven_kinFit_ttbar_down]
    #  idirs = ["sig_NMSSM_bbbb_MX_600_MY_400", "data_BTagCSV", "data_BTagCSV_3btag", "data_BTagCSV_dataDriven_kinFit", "data_BTagCSV_dataDriven_kinFit_up", "sig_NMSSM_bbbb_MX_600_MY_400_jes_Total_up", "sig_NMSSM_bbbb_MX_600_MY_400_jes_Total_down", "sig_NMSSM_bbbb_MX_600_MY_400_jer_up", "sig_NMSSM_bbbb_MX_600_MY_400_jer_down", "sig_NMSSM_bbbb_MX_600_MY_400_bjer_up", "sig_NMSSM_bbbb_MX_600_MY_400_bjer_down", "ggF_Hbb", "VBF_Hbb", "sig_NMSSM_bbbb_MX_600_MY_400_3bScaled", "ttbar", "ZH", "ttbar_3bScaled", "data_BTagCSV_dataDriven_kinFit_down", "ttbar_3b", "ZZ", "ttH", "WH", "QCD", "data_BTagCSV_dataDriven_kinFit_ttbar_up", "data_BTagCSV_dataDriven_kinFit_ttbar_down"]

    idirs = ["data_BTagCSV", "data_BTagCSV_3btag", "data_BTagCSV_dataDriven_kinFit", "data_BTagCSV_dataDriven_kinFit_up", "ggF_Hbb", "VBF_Hbb", "sig_NMSSM_bbbb_MX_600_MY_400_3bScaled", "ttbar", "ZH", "ttbar_3bScaled", "data_BTagCSV_dataDriven_kinFit_down", "ttbar_3b", "ZZ", "ttH", "WH", "QCD", "data_BTagCSV_dataDriven_kinFit_ttbar_up", "data_BTagCSV_dataDriven_kinFit_ttbar_down"] 
    sigDir = "sig_NMSSM_bbbb_MX_600_MY_400"
    sigSystDirs = ["sig_NMSSM_bbbb_MX_600_MY_400_jes_Total_up", "sig_NMSSM_bbbb_MX_600_MY_400_jes_Total_down", "sig_NMSSM_bbbb_MX_600_MY_400_jer_up", "sig_NMSSM_bbbb_MX_600_MY_400_jer_down", "sig_NMSSM_bbbb_MX_600_MY_400_bjer_up", "sig_NMSSM_bbbb_MX_600_MY_400_bjer_down"] 
    if year =="2018":
        sigHistNames = ["HH_kinFit_m_H2_m_Rebinned_Unrolled", "HH_kinFit_m_H2_m_PUWeight_up_Rebinned_Unrolled", "HH_kinFit_m_H2_m_PUWeight_down_Rebinned_Unrolled", "HH_kinFit_m_H2_m_bJetUp_Rebinned_Unrolled", "HH_kinFit_m_H2_m_bJetDown_Rebinned_Unrolled", "HH_kinFit_m_H2_m_cJetUp_Rebinned_Unrolled", "HH_kinFit_m_H2_m_cJetDown_Rebinned_Unrolled", "HH_kinFit_m_H2_m_lightJetUp_Rebinned_Unrolled", "HH_kinFit_m_H2_m_lightJetDown_Rebinned_Unrolled", "HH_kinFit_m_H2_m_triggerUp_Rebinned_Unrolled", "HH_kinFit_m_H2_m_triggerDown_Rebinned_Unrolled"]
    else:
        sigHistNames = ["HH_kinFit_m_H2_m_Rebinned_Unrolled", "HH_kinFit_m_H2_m_PUWeight_up_Rebinned_Unrolled", "HH_kinFit_m_H2_m_PUWeight_down_Rebinned_Unrolled", "HH_kinFit_m_H2_m_bJetUp_Rebinned_Unrolled", "HH_kinFit_m_H2_m_bJetDown_Rebinned_Unrolled", "HH_kinFit_m_H2_m_cJetUp_Rebinned_Unrolled", "HH_kinFit_m_H2_m_cJetDown_Rebinned_Unrolled", "HH_kinFit_m_H2_m_lightJetUp_Rebinned_Unrolled", "HH_kinFit_m_H2_m_lightJetDown_Rebinned_Unrolled", "HH_kinFit_m_H2_m_triggerUp_Rebinned_Unrolled", "HH_kinFit_m_H2_m_triggerDown_Rebinned_Unrolled", "HH_kinFit_m_H2_m_L1PreFiringWeight_Up_Rebinned_Unrolled", "HH_kinFit_m_H2_m_L1PreFiringWeight_Dn_Rebinned_Unrolled"]

#  skipped:
#  data_BTagCSV_dataDriven_kinFit_upRefined
#  data_BTagCSV_dataDriven_kinFit_downRefined
    ihists = []
    ihists_sig = []
    ihists_sig_syst = []
    ihists_sig_studyRegion = []
    ihists_sig_syst_studyRegion = []
    sig_region = "selectionbJets_SignalRegion"
# data hists
    for i in range(len(idirs)):
        h_temp = ifile.Get(idirs[i]+"/"+dir_region+"/"+idirs[i]+"_"+dir_region+"_"+histname)
        ihists.append(h_temp)
    # signal hists - in study region and sig region
    for j in range(len(sigHistNames)):
        h_temp = ifile.Get(sigDir+"/"+dir_region+"/"+sigDir+"_"+dir_region+"_"+sigHistNames[j])
        ihists_sig_studyRegion.append(h_temp)
        h_temp = ifile.Get(sigDir+"/"+sig_region+"/"+sigDir+"_"+sig_region+"_"+sigHistNames[j])
        ihists_sig.append(h_temp)
    # signal Systematic histograms - in study region and signal region
    for i in range(len(sigSystDirs)):
        h_temp = ifile.Get(sigSystDirs[i]+"/"+dir_region+"/"+sigSystDirs[i]+"_"+dir_region+"_"+histname)
        ihists_sig_syst_studyRegion.append(h_temp)
        h_temp = ifile.Get(sigSystDirs[i]+"/"+sig_region+"/"+sigSystDirs[i]+"_"+sig_region+"_"+histname)
        ihists_sig_syst.append(h_temp)

    ##################################################
    # give histogram names
    h_4b = ihists[0]
    h_3b_weights = ihists[2]
    h_bkgModel_ttbar_up = ihists[16]
    h_bkgModel_ttbar_down = ihists[17]
    h_sig = ihists_sig[0]
    h_ttbar = ihists_sig[7]
    #  h_4b_norm = h_4b.Clone("hratio")
    #  h_3b_weights_norm = h_3b_weights.Clone("hratio")
    hratio = h_4b.Clone("hratio")
    hratio.Divide(h_3b_weights)
    hsigma = hratio.Clone("hsigma")
    hError = hratio.Clone("hError")
    for i in range(1,hsigma.GetSize()-1):
        hError.SetBinContent(i,hratio.GetBinError(i))
        hsigma.SetBinContent(i, hratio.GetBinContent(i)-1)
    hsigma.Divide(hError)


    ##################################################
    # reorder the histograms
    #  h_sig = reorderHistBins([h_sig])
    #  h_sig,h_3b_weights,h_4b = reorderHistBins([h_sig,h_3b_weights,h_4b])
    #  binThreshold=-1
    #  binThreshold=20
    # reorder on signal hist
    # threshold on ratio
    #  reorderHistBins([[ihists_sig[0]], [hratio], ihists, ihists_sig_studyRegion, ihists_sig, ihists_sig_syst, ihists_sig_syst_studyRegion], binThreshold,ratioThreshold)
    # threshold on sigma
    reorderHistBins([[ihists_sig[0]], [hsigma], ihists, ihists_sig_studyRegion, ihists_sig, ihists_sig_syst, ihists_sig_syst_studyRegion], binThreshold,ratioThreshold)
    # reorder on 4b hist
    #  reorderHistBins([[ihists[0]], [hratio], ihists, ihists_sig_studyRegion, ihists_sig, ihists_sig_syst, ihists_sig_syst_studyRegion], binThreshold,ratioThreshold)
    # reorder on 4b hist
    #  reorderHistBins([[ihists[2]], [hratio], ihists, ihists_sig_studyRegion, ihists_sig, ihists_sig_syst, ihists_sig_syst_studyRegion], binThreshold,ratioThreshold)

    ##################################################
    # save plots
    #  rootplot_2samp_ratio( ihists[2], ihists[0],  year, region, varname, ""+itag   , odir, ihists_sig[0], ihists[] )
    rootplot_2samp_ratio( h_3b_weights, h_4b,  year, region, varname, "orig_sig"+itag   , odir, h_sig, h_bkgModel_ttbar_down )
    #  rootplot_2samp_ratio( h_bkgModel_ttbar_down, h_4b,  year, region, varname, "ttbarAdj_sig"+itag   , odir, h_sig, h_3b_weights )
    #  rootplot_2samp_ratio( h_3b_weights, h_4b,  year, region, varname, "orig_ttbar"+itag   , odir, h_ttbar, h_bkgModel_ttbar_down )
    #  rootplot_2samp_ratio( h_bkgModel_ttbar_down, h_4b,  year, region, varname, "ttbarAdj_ttbar"+itag   , odir, h_ttbar, h_3b_weights )

    #  ##################################################
    #save histograms
    # data hists - study region
    for i in range(len(ihists)):
        ofile.cd()
        ofile.mkdir(idirs[i]+"/"+dir_region)
        ofile.cd(idirs[i]+"/"+dir_region)
        ihists[i].Write()

    # data hists - signal region (copy of signal region)
    for i in range(len(ihists)):
        ofile.cd()
        ofile.mkdir(idirs[i]+"/"+sig_region)
        ofile.cd(idirs[i]+"/"+sig_region)
        ihists[i].SetName(idirs[i]+"_"+sig_region+"_"+histname)
        ihists[i].SetTitle(idirs[i]+"_"+sig_region+"_"+histname)
        ihists[i].Write()

    # sig hists is study region
    ofile.cd()
    ofile.mkdir(sigDir +"/"+dir_region)
    ofile.cd(sigDir +"/"+dir_region)
    for i in range(len(ihists_sig_studyRegion)):
        ihists_sig_studyRegion[i].Write()

    # sig hists is signal region
    ofile.cd()
    ofile.mkdir(sigDir +"/"+sig_region)
    ofile.cd(sigDir +"/"+sig_region)
    for i in range(len(ihists_sig)):
        ihists_sig[i].Write()

    # sig systematic hists in study region
    for i in range(len(ihists_sig_syst_studyRegion)):
        ofile.cd()
        ofile.mkdir(sigSystDirs[i]+"/"+dir_region)
        ofile.cd(sigSystDirs[i]+"/"+dir_region)
        ihists_sig_syst_studyRegion[i].Write()

    # sig systematic hists in signal region
    for i in range(len(ihists_sig_syst)):
        ofile.cd()
        ofile.mkdir(sigSystDirs[i]+"/"+sig_region)
        ofile.cd(sigSystDirs[i]+"/"+sig_region)
        ihists_sig_syst[i].Write()
    #  #################################################

    ofile.Close()
    ifile.Close()

# ********************
#run pyROOT in batch mode  - ie don't show graphics!
# 
gROOT.SetBatch(True)
# ********************
#  odir = "VarPlots/UnrolledPlots_2022Mar23_reordered/"
#  odir = "VarPlots/UnrolledPlots_2022Mar28_reordered/"
#  odir = "VarPlots/UnrolledPlots_2022Mar28_reordered_lt1p3ratio/"
#  odir = "VarPlots/UnrolledPlots_2022Mar28_reordered_lt1p2ratio/"
#  odir = "VarPlots/UnrolledPlots_2022Mar28_DATAreordered/"
#  odir = "VarPlots/UnrolledPlots_2022Mar28_3bDATAreordered/"
odir = "VarPlots/UnrolledPlots_2022Apr1_reordered_sigma/"
#  year = "2016"
#  region = "VR"
#  region = "CR"
#  directories = ["selectionbJets_ControlRegionBlinded", "selectionbJets_ValidationRegionBlinded"]
#  itag = "fullrange"
#  directory = "selectionbJets_ControlRegionBlinded"
#  directory = "selectionbJets_ValidationRegionBlinded"
#  compareUnrolled(directory, region, year, odir)
#  varname = "massUnrolled"
#  varname = "massUnrolled_subrange5"
#  varname = "massUnrolled_subrange20"
#  itag = "_vrRange"
#  itag "_20bins"
#  itag "_5bins"
####################################################################################################
#  years = ["2016","2017","2018"]
#  years = ["2016"]
#  regions = [["CR", "selectionbJets_ControlRegionBlinded"], ["VR", "selectionbJets_ValidationRegionBlinded"]]
# plotting studies:
#  itag = ""
#  for year in years:
    #  region = regions[0]
    #  varname = "massUnrolled_CR"
    #  compareUnrolled(region[1], region[0], year, odir,varname,itag)
#  studies = [[ "massUnrolled",  "_vrRange"],[ "massUnrolled_subrange5", "_5bins"], [ "massUnrolled_subrange20", "_20bins"]]
#  for year in years:
    #  for region in regions:
        #  for study in studies:
            #  varname = study[0]
            #  itag = study[1]
            #  if "VR" in region and "vr" in itag: itag = ""
            #  compareUnrolled(region[1], region[0], year, odir,varname,itag)
####################################################################################################
####for Saving Hists in root file###################################################################
years = ["2016","2017","2018"]
#  years = ["2016"]
#  regions = [["CR", "selectionbJets_ControlRegionBlinded", "massUnrolled_CR"], ["VR", "selectionbJets_ValidationRegionBlinded", "massUnrolled"]]
#  regions = [["CR", "selectionbJets_ControlRegionBlinded"], ["VR", "selectionbJets_ValidationRegionBlinded"]]
regions = [["CR", "selectionbJets_ControlRegionBlinded"], ["VR", "selectionbJets_ValidationRegionBlinded"]]
#  regions = [["CR", "selectionbJets_ControlRegionBlinded"]]
#  massGroups = [0,1,2,3,4]
massGroups = [0]
itag = ""
binThreshold=-1
#  ratioThreshold=1.3
#  ratioThreshold=0.3
#  ratioThreshold=3
#  ratioThreshold=2
ratioThreshold=1.5
#  ratioThreshold=1.2
#  ratioThreshold=100.
#  compareUnrolled(regions[1][1], regions[1][0], "2016", 0, odir,regions[1][2],itag)
##test study:
#  compareUnrolled(regions[1][1], regions[1][0], "2017", 0, odir,"massUnrolled",itag, binThreshold,ratioThreshold)

##################################################
#  for year in years:
    #  for massGroup in massGroups:
        #  for region in regions:
            #  #  if "CR" in region[0]: varname = "massUnrolled_CR"
            #  if "CR" in region[0]: varname = "massUnrolled"
            #  elif "VR" in region[0]: varname = "massUnrolled"
            #  compareUnrolled(region[1], region[0], year, massGroup, odir,varname,itag, binThreshold,ratioThreshold)

##################################################
#  full set of studies:
itag = itag+"_lt%ssigma"%(ratioThreshold)
itag = itag.replace(".", "p")
for year in years:
    for massGroup in massGroups:
        region = regions[0]
        varname = "massUnrolled_CR"
        compareUnrolled(region[1], region[0], year, massGroup, odir,varname,itag, binThreshold,ratioThreshold)
studies = [[ "massUnrolled",  "_vrRange", -1],[ "massUnrolled_subrange5", "_5bins", 5], [ "massUnrolled_subrange20", "_20bins", 20]]
for year in years:
    for region in regions:
        for massGroup in massGroups:
            for study in studies:
                varname = study[0]
                itag = study[1]
                if "VR" in region and "vr" in itag: itag = ""
                binThreshold=study[2]
                #  varname = region[2]
                itag = itag+"_lt%ssigma"%(ratioThreshold)
                itag = itag.replace(".", "p")
                compareUnrolled(region[1], region[0], year, massGroup, odir,varname,itag,binThreshold, ratioThreshold)
                print("Completed %s %s mass group %i"%(region[0], year, massGroup))
####################################################################################################

#  region = regions[0]
#  compareUnrolled(region[1], region[0], years[0], odir, varname, itag)
  #  compareUnrolled(ifileName, year, odir)


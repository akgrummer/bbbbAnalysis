from ROOT import TFile,TH1F,TH2F,TCanvas,gStyle,gPad,gDirectory,TLatex,gROOT,PyConfig,TMath,kBlue,TLine,TPad, TLegend,TGraph,TBox
# PyConfig.IgnoreCommandLineOptions = False
import numpy as np
import re
import os

def hBinSubset(h,binx1,binx2,biny1,biny2):
    x1 = h.GetXaxis().GetBinLowEdge(binx1)
    x2 = h.GetXaxis().GetBinLowEdge(binx2)+h.GetXaxis().GetBinWidth(binx2)
    y1 = h.GetYaxis().GetBinLowEdge(biny1)
    y2 = h.GetYaxis().GetBinLowEdge(biny2)+h.GetYaxis().GetBinWidth(biny2)
    n1 = binx1+binx2+1
    n2 = biny1+biny2+1;

    nbinsx = h.GetNbinsX();
    nbinsy = h.GetNbinsY();

    hs = TH2F(h.GetName(), h.GetTitle(), n1, x1, x2, n2, y1, y2)

    for i in range(1, nbinsx+1):
        for j in range(1,nbinsy+1):
            content = h.GetBinContent(i,j)
            x = h.GetXaxis().GetBinCenter(i)
            y = h.GetYaxis().GetBinCenter(j)
            hs.Fill(x, y, content)

def drawSignalSlice(h1,tag, odir, masspoint):
    h1 = h1.Clone()
    # print("my mass point is: ",re.search("MX_(.*?)_",masspoint).group(1))
    mXval = float(re.search("MX_(.*?)_",masspoint).group(1))
    binNum = h1.GetXaxis().FindBin(mXval)
    binsY = [36, 45, 51, 57, 62, 66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 122, 132, 140, 148, 156, 164, 172, 180, 188, 196, 204, 212, 228, 244, 260, 276, 292, 308, 324, 340, 356, 372, 388, 412, 444, 476, 508, 540, 572, 604, 636, 668, 700, 732, 764, 828, 892, 956, 1020, 1084, 1148, 1212, 1276, 1340, 1404, 1468, 1564, 1692, 1820, 1948, 2076, 2204]
    # binsx = [212, 228, 244, 260, 276, 292, 308, 324, 340, 360, 392, 424, 456, 488, 520, 552, 584, 616, 648, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216, 1296, 1424, 1552, 1680, 1808, 1936, 2064, 2192, 2320]
    hOneDsig = TH1F( "OneD2plot", "OneD2plot", h1.GetNbinsY(), np.asarray(binsY, 'f'))
    hOneDsig_plusBin  = TH1F( "hOneDsig_plusBin", "hOneDsig_plusBin", h1.GetNbinsY(), np.asarray(binsY, 'f'))
    hOneDsig_minusBin = TH1F( "hOneDsig_minusBin", "hOneDsig_minusBin", h1.GetNbinsY(), np.asarray(binsY, 'f'))
    for iy in range(1, h1.GetNbinsY()+1):
        hOneDsig.SetBinContent(iy,h1.GetBinContent(binNum, iy))
        hOneDsig_plusBin.SetBinContent(iy,h1.GetBinContent(binNum+1, iy))
        hOneDsig_minusBin.SetBinContent(iy,h1.GetBinContent(binNum-1, iy))
    # c2 = TCanvas('c2', 'c2',800,600)
    # gStyle.SetOptStat(0) # remove the stats box
    # gStyle.SetOptTitle(0) # remove the title
    # gPad.SetTicks(1,1)
    # gPad.SetMargin(0.16,0.05,0.12,0.09) #left,right,bottom,top    
    hOneDsig = histDecorations( hOneDsig         , 1, 1 )         
    hOneDsig_plusBin = histDecorations( hOneDsig_plusBin , 2, 2 )
    hOneDsig_minusBin = histDecorations( hOneDsig_minusBin, 4, 4 )
    # hOneDsig.GetXaxis().SetRangeUser(0,mXval - 100)
    hOneDsig.GetYaxis().SetTitle("Entries")
    hOneDsig.GetXaxis().SetTitle("m_{Y} [GeV]")
    hOneDsig_plusBin.GetYaxis().SetTitle("Entries")
    hOneDsig_plusBin.GetXaxis().SetTitle("m_{Y} [GeV]")
    hOneDsig_minusBin.GetYaxis().SetTitle("Entries")
    hOneDsig_minusBin.GetXaxis().SetTitle("m_{Y} [GeV]")
    # hOneDsig.Draw("e1x0")
    # hOneDsig.Draw("same hist")
    # hOneDsig_plusBin.Draw("same hist")
    # hOneDsig_plusBin.Draw("same e1x0")
    # hOneDsig_minusBin.Draw("same hist")   
    # hOneDsig_minusBin.Draw("same e1x0")   
    # CMSlabel = TLatex()
    # CMSlabel.SetTextSize( 0.05 )
    # CMSlabel.DrawLatexNDC(0.2, 0.92, "CMS #scale[0.8]{#font[52]{Work In Progress}}")
    # mXlabel = TLatex()
    # mXlabel.SetTextSize( 0.03 )
    # labelText = "mX = %.0f GeV"%(mXval)
    # if "VR" in tag:    labelText = labelText + " #font[42]{Validation Region}"
    # if "CR" in tag:    labelText = labelText + " #font[42]{Control Region}"
    # mXlabel.DrawLatexNDC(0.55, 0.92, labelText)
    # if "weights" in tag:    mXlabel.DrawTextNDC(0.2, 0.86, "3b reweighted")
    # if "orig" in tag:    mXlabel.DrawTextNDC(0.2, 0.86, "before 3b reweighting")
    # oneDdir = "OneDplots"
    # path = "%s/%s"%(odir,oneDdir)
    # if not (os.path.exists(path)): os.makedirs(path) 
    # if not "orig" in tag: c2.SaveAs("%s/%s/sigSlice_%s_%.0f.pdf"%(odir,oneDdir,tag,mXval))
    return hOneDsig, hOneDsig_plusBin, hOneDsig_minusBin

def makemyplots(h1,tag, odir,ksval,ksvalMaxDist,ksvalX,year):
    h1 = h1.Clone()
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    gPad.SetTicks(1,1)
    gPad.SetMargin(0.16,0.16,0.12,0.09) #left,right,bottom,top
    h1.Draw("COLZ1")
    CMSlabel = TLatex()
    CMSlabel.SetTextSize( 0.05 )
    CMSlabel.DrawLatexNDC(0.2, 0.92, "CMS #scale[0.8]{#font[52]{Work In Progress}}")
    KSlabel = TLatex()
    KSlabel.SetTextFont( 42 )
    KSlabel.SetTextSize( 0.03 )
    if "_VR_" in tag:    KSlabel.DrawLatexNDC(0.2, 0.86, "#font[62]{Validation Region}")
    if "_CR_" in tag:    KSlabel.DrawLatexNDC(0.2, 0.86, "#font[62]{Control Region}")
    if "weights" in tag:    KSlabel.DrawTextNDC(0.2, 0.82, "reweighted")
    if "orig" in tag:    KSlabel.DrawTextNDC(0.2, 0.82, "before reweighting")
    KSlabel.DrawTextNDC(0.4, 0.86, year)
    if not ksval<0: KSlabel.DrawTextNDC(0.2, 0.8, ksval)
    if not ksvalMaxDist<0: KSlabel.DrawTextNDC(0.2, 0.76, ksvalMaxDist)
    if not ksvalX<0: KSlabel.DrawTextNDC(0.2, 0.72, ksvalX)
    #*************
    # save the plot
    path = "%s/"%(odir)
    if not (os.path.exists(path)): os.makedirs(path) 
    #  c1.SaveAs("%s/mXvsmY_%s.pdf"%(odir,tag))
    # c1.SaveAs("%s/mXvsmY_%s.png"%(odir,tag))
    del c1,h1

def getKSTestRoot(h1,h2):
    h1 = h1.Clone()
    h2 = h2.Clone()
    # *************
    # kstests
    ksval = "KS Test = %.4f"%h1.KolmogorovTest(h2)
    ksvalMaxDist= "KS Test, Max Dist. = %.4f"%h1.KolmogorovTest(h2, "M")
    ksvalX = "KS Test, pseudoX = %.4f"%h1.KolmogorovTest(h2, "X")
    # *************
    return ksval,ksvalMaxDist,ksvalX

def histDecorations(h1, mColor=1, lColor=1):
    h1.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
    h1.SetMarkerSize(0.08)
    h1.SetMarkerColor(mColor)
    h1.SetLineColor(lColor)
    h1.SetLineWidth(1)
    return h1

def setRangeAndSizes(h1,hRef,firstBin,lastBin):
    h1.GetXaxis().SetRangeUser(hRef.GetBinLowEdge(firstBin),hRef.GetBinCenter(lastBin))
    h1.GetYaxis().SetLabelSize(0.08)
    h1.GetYaxis().SetTitleSize(0.08)
    h1.GetYaxis().SetTitleOffset(0.5)
    h1.GetXaxis().SetLabelSize(0.08)
    h1.GetXaxis().SetTitleSize(0.08)

def FindFirstBinContent(h,initialval):
    nbinsx = h.GetXaxis().GetNbins()
    for binx in range(1,nbinsx+1):
        if not (h.GetBinContent(binx) == 0): 
            if initialval is 0: return binx 
            elif binx<=initialval: return binx
            else: return initialval
    return 0 

def FindLastBinContent(h,initialval):
    nbinsx = h.GetXaxis().GetNbins()
    for binx in reversed(range(1,nbinsx+1)):
        if not (h.GetBinContent(binx) == 0): 
            if initialval is -1: return binx
            elif binx>=initialval: return binx 
            else: return initialval
    return -1 

def getOneDPlotwithSig(hOneD,firstBin,lastBin,tag, odir,h_sig,masspoint,year):
    hOneD = hOneD.Clone()
    hOneDsig, hOneDsig_plusBin, hOneDsig_minusBin = drawSignalSlice(h_sig,tag,odir,masspoint)
    mXval = float(re.search("MX_(.*?)_",masspoint).group(1))
    mYval = float(masspoint.split("MY_",1)[1])
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    #### define the upper and lower pads
    p1 = TPad("p1", "p1", 0., 0.4, 1., 1.0, 0, 0, 0)
    p1.SetMargin(0.12,0.05,0.05,0.12) #left,right,bottom,top
    p1.SetTicks(1,1)
    p1.Draw()
    p2 = TPad("p2", "p2", 0., 0., 1., 0.4, 0, 0, 0)
    p2.SetMargin(0.12,0.05,0.2,0.05) #left,right,bottom,top
    p2.SetTicks(1,1)
    p2.Draw()
    ########################################
    p1.cd()
    hOneD.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
    hOneD.SetMarkerSize(0.7)
    hOneD.SetMarkerColor(1)
    hOneD.SetLineColor(1)
    hOneD.SetMarkerStyle(8)
    hOneD.SetLineColor(1)
    hOneD.SetLineWidth(1)
    # hOneD.GetXaxis().SetRangeUser(0,mXval - 100)
    hOneD.GetXaxis().SetRangeUser(hOneD.GetBinLowEdge(firstBin),hOneD.GetBinCenter(lastBin))
    Line_at0 = TLine(hOneD.GetBinLowEdge(firstBin),0,hOneD.GetBinCenter(lastBin),0)# x1, y1, x2, y2
    Line_sig1 = TLine(hOneD.GetBinLowEdge(firstBin),1,hOneD.GetBinCenter(lastBin),1)# x1, y1, x2, y2
    Line_sigm1 = TLine(hOneD.GetBinLowEdge(firstBin),-1,hOneD.GetBinCenter(lastBin),-1) # x1, y1, x2, y2
    Line_sig2 = TLine(hOneD.GetBinLowEdge(firstBin),2,hOneD.GetBinCenter(lastBin),2) # x1, y1, x2, y2
    Line_sigm2 = TLine(hOneD.GetBinLowEdge(firstBin),-2,hOneD.GetBinCenter(lastBin),-2) # x1, y1, x2, y2
    # print("my value: %s, %s"%(FindFirstBinContent(hOneD),hOneD.GetBinContent(FindFirstBinContent(hOneD))))
    Line_at0.SetLineColor(15)
    Line_sig1.SetLineColor(66)
    Line_sigm1.SetLineColor(66)
    Line_sig2.SetLineColor(62)
    Line_sigm2.SetLineColor(62)
    hOneD.GetYaxis().SetTitle("(target - model) / error")
    hOneD.GetYaxis().SetTitleOffset(0.8)
    hOneD.GetXaxis().SetTitle("m_{Y} [GeV]")
    hOneD.Draw("ple")
    hOneD.GetYaxis().SetLabelSize(0.06)
    hOneD.GetYaxis().SetTitleSize(0.06)
    hOneD.GetXaxis().SetLabelSize(0.)
    hOneD.GetXaxis().SetTitleSize(0.)
    maxval =hOneD.GetMaximum() 
    minval =hOneD.GetMinimum() 
    maxbin = hOneD.GetMaximumBin() 
    minbin = hOneD.GetMinimumBin() 
    maxbinerror  = hOneD.GetBinError(maxbin)
    minbinerror  = hOneD.GetBinError(minbin)
    Line_at0.Draw("same")
    if not (maxval+maxbinerror<1.5): Line_sig1.Draw("same")
    if not (minval-minbinerror>-1.5): Line_sigm1.Draw("same")
    if not (maxval+maxbinerror<2.5): Line_sig2.Draw("same")
    if not (minval-minbinerror>-2.5): Line_sigm2.Draw("same")
    hOneD.Draw("ple same")
    b = TBox() 
    b.SetLineColor(0)
    b.SetFillColor(2)
    b.SetFillStyle(3004)
    hOneD.GetYaxis().SetRangeUser(1.1*(minval-minbinerror), 1.6*(maxval+maxbinerror))
    legUp = TLegend(0.75,0.75,0.87,0.83)
    regionText = ""
    if "VR" in tag:
        b.DrawBox(105,1.1*(minval-minbinerror),145,1.6*(maxval+maxbinerror))
        legUp.AddEntry(b, "Blinded region", "f")
        regionText = "VR"
    if "CR" in tag:
        b.DrawBox(95,1.1*(minval-minbinerror),155,1.6*(maxval+maxbinerror))
        legUp.AddEntry(b, "Blinded + Val. region", "f")
        regionText = "CR"
    legUp.AddEntry(Line_sig1, "#pm #sigma", "l")
    legUp.AddEntry(Line_sig2, "#pm 2#sigma", "l")
    legUp.SetBorderSize(0) # remove the border
    legUp.SetLineColor(0)
    legUp.SetFillColor(0)
    legUp.SetTextSize(0.035)
    legUp.SetFillStyle(0) # make the legend background transparent
    legUp.Draw()
    CMSlabel = TLatex()
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 30 )
    CMSlabel.DrawLatexNDC(0.12, 0.92, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
    mXlabel = TLatex()
    mXlabel.SetTextFont()
    mXlabel.SetTextSize( 0.05 )
    labelText = "mX = %.0f GeV, mY = %.0f GeV"%(mXval,mYval)
    if "VR" in tag:    labelText = labelText + " #font[42]{Validation Region}"
    if "CR" in tag:    labelText = labelText + " #font[42]{Control Region}"
    mXlabel.DrawLatexNDC(0.45, 0.92, labelText)
    if "weights" in tag:    mXlabel.DrawTextNDC(0.15, 0.81, "3b reweighted")
    if "orig" in tag:    mXlabel.DrawTextNDC(0.15, 0.81, "before 3b reweighting")
    mXlabel.DrawTextNDC(0.32, 0.81, year)
    binLabel = TLatex() 
    binLabel.SetTextFont(42)
    binLabel.SetTextSize( 0.05 )
    if "_binCenter" in tag: binLabel.DrawLatexNDC(0.4,0.81,"#bf{Center} bin for mX = %.0f GeV"%mXval)
    if "_binAbove" in tag: binLabel.DrawLatexNDC(0.4,0.81,"One bin #bf{above} of mX = %.0f GeV"%mXval)
    if "_binBelow" in tag: binLabel.DrawLatexNDC(0.4,0.81,"One bin #bf{below} of mX = %.0f GeV"%mXval)
    ###################
    p2.cd()
    setRangeAndSizes(hOneDsig,hOneD,firstBin,lastBin)
    setRangeAndSizes(hOneDsig_plusBin,hOneD,firstBin,lastBin)
    setRangeAndSizes(hOneDsig_minusBin,hOneD,firstBin,lastBin)
    # if "_binCenter" in tag: 
        # hOneDsig.Draw("e1x0")
        # hOneDsig_plusBin.Draw("same e1x0")
        # hOneDsig_minusBin.Draw("same e1x0")
    # if "_binAbove" in tag: 
        # hOneDsig_plusBin.Draw("e1x0")
        # hOneDsig.Draw("same e1x0")
        # hOneDsig_minusBin.Draw("same e1x0")
    # if "_binBelow" in tag: 
        # hOneDsig_minusBin.Draw("e1x0")
        # hOneDsig.Draw("same e1x0")
        # hOneDsig_plusBin.Draw("same e1x0")
    if "_binCenter" in tag: 
        #  hOneDsig.Draw("e1x0")
        #  hOneDsig_plusBin.Draw("same e1x0")
        #  hOneDsig_minusBin.Draw("same e1x0")
        #  hOneDsig_plusBin.Draw("same hist")
        #  hOneDsig_minusBin.Draw("same hist")
        hOneDsig2 = hOneDsig.Clone()
        hOneDsig2.SetLineWidth(2)
        #  hOneDsig2.Draw("same hist")
        hOneDsig2.Draw("hist")
    if "_binAbove" in tag: 
        #  hOneDsig_plusBin.Draw("e1x0")
        hOneDsig_plusBin2 = hOneDsig_plusBin.Clone()
        hOneDsig_plusBin2.SetLineWidth(2)
        #  hOneDsig_plusBin2.Draw("same hist")
        hOneDsig_plusBin2.Draw("hist")
    if "_binBelow" in tag: 
        #  hOneDsig_minusBin.Draw("e1x0")
        hOneDsig_minusBin2 = hOneDsig_minusBin.Clone()
        hOneDsig_minusBin2.SetLineWidth(2)
        #  hOneDsig_minusBin2.Draw("same hist")
        hOneDsig_minusBin2.Draw("hist")
    #### define legend
    if mXval == 300.: leg = TLegend(0.2,0.65,0.35,0.84)
    else: leg = TLegend(0.65,0.65,0.8,0.84)
    leg.SetHeader("Signal MC")
    if "_binCenter" in tag: leg.AddEntry(hOneDsig, "Center bin for mX = %.0f GeV"%mXval, "l")
    if "_binAbove" in tag: leg.AddEntry(hOneDsig_plusBin, "One bin above of mX = %.0f GeV"%mXval, "l")
    if "_binBelow" in tag: leg.AddEntry(hOneDsig_minusBin, "One bin below of mX = %.0f GeV"%mXval, "l")
    leg.SetBorderSize(0) # remove the border
    leg.SetLineColor(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.05)
    leg.SetFillStyle(0) # make the legend background transparent
    leg.Draw()
    ###################
    # input("Press Enter to continue...")
    oneDdir = "OneDplots"
    path = "%s/%s"%(odir,oneDdir)
    if not (os.path.exists(path)): os.makedirs(path) 
    path = "%s/%s"%(path,masspoint)
    if not (os.path.exists(path)): os.makedirs(path) 
    path = "%s/%s"%(path,regionText)
    if not (os.path.exists(path)): os.makedirs(path) 
    #  if not "orig" in tag: c1.SaveAs("%s/%s/%s/%s/mXvsmY_%s_%.0f.pdf"%(odir,oneDdir,masspoint,regionText,tag,mXval))
    if not "orig" in tag: c1.SaveAs("%s/%s/%s/%s/mXvsmY_%s_%.0f.png"%(odir,oneDdir,masspoint,regionText,tag,mXval))

def getOneDPlot(h1, mXval,tag, odir,h_sig,masspoint):
    h1 = h1.Clone()
    binNum = h1.GetXaxis().FindBin(mXval)
    binsY = [36, 45, 51, 57, 62, 66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 122, 132, 140, 148, 156, 164, 172, 180, 188, 196, 204, 212, 228, 244, 260, 276, 292, 308, 324, 340, 356, 372, 388, 412, 444, 476, 508, 540, 572, 604, 636, 668, 700, 732, 764, 828, 892, 956, 1020, 1084, 1148, 1212, 1276, 1340, 1404, 1468, 1564, 1692, 1820, 1948, 2076, 2204]
    # binsx = [212, 228, 244, 260, 276, 292, 308, 324, 340, 360, 392, 424, 456, 488, 520, 552, 584, 616, 648, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216, 1296, 1424, 1552, 1680, 1808, 1936, 2064, 2192, 2320]
    hOneD = TH1F( "OneDplot", "OneDplot", h1.GetNbinsY(), np.asarray(binsY, 'f'))
    for iy in range(1, h1.GetNbinsY()+1):
        hOneD.SetBinContent(iy,h1.GetBinContent(binNum, iy))
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    gPad.SetTicks(1,1)
    # gPad.SetMargin(0.16,0.05,0.12,0.09) #left,right,bottom,top    
    hOneD.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
    hOneD.SetMarkerSize(0.7)
    hOneD.SetMarkerColor(1)
    hOneD.SetLineColor(1)
    hOneD.SetMarkerStyle(8)
    hOneD.SetLineColor(1)
    hOneD.SetLineWidth(1)
    # hOneD.GetXaxis().SetRangeUser(0,mXval - 100)
    firstBin =FindFirstBinContent(hOneD) 
    firstBin = firstBin -1
    lastBin =FindLastBinContent(hOneD) 
    lastBin =lastBin +1
    hOneD.GetXaxis().SetRangeUser(hOneD.GetBinLowEdge(firstBin),hOneD.GetBinCenter(lastBin))
    Line_sig1 = TLine(hOneD.GetBinLowEdge(firstBin),1,hOneD.GetBinCenter(lastBin),1)# x1, y1, x2, y2
    Line_sigm1 = TLine(hOneD.GetBinLowEdge(firstBin),-1,hOneD.GetBinCenter(lastBin),-1) # x1, y1, x2, y2
    Line_sig2 = TLine(hOneD.GetBinLowEdge(firstBin),2,hOneD.GetBinCenter(lastBin),2) # x1, y1, x2, y2
    Line_sigm2 = TLine(hOneD.GetBinLowEdge(firstBin),-2,hOneD.GetBinCenter(lastBin),-2) # x1, y1, x2, y2
    # print("my value: %s, %s"%(FindFirstBinContent(hOneD),hOneD.GetBinContent(FindFirstBinContent(hOneD))))
    Line_sig1.SetLineColor(kBlue)
    Line_sigm1.SetLineColor(kBlue)
    Line_sig2.SetLineColor(kBlue)
    Line_sigm2.SetLineColor(kBlue)
    hOneD.GetYaxis().SetTitle("(target - model) / error")
    hOneD.GetXaxis().SetTitle("m_{Y} [GeV]")
    hOneD.Draw("ple")
    maxval =hOneD.GetMaximum() 
    minval =hOneD.GetMinimum() 
    maxbin = hOneD.GetMaximumBin() 
    minbin = hOneD.GetMinimumBin() 
    maxbinerror  = hOneD.GetBinError(maxbin)
    minbinerror  = hOneD.GetBinError(minbin)
    if not (maxval+maxbinerror<1.5): Line_sig1.Draw("same")
    if not (minval-minbinerror>-1.5): Line_sigm1.Draw("same")
    if not (maxval+maxbinerror<2.5): Line_sig2.Draw("same")
    if not (minval-minbinerror>-2.5): Line_sigm2.Draw("same")
    CMSlabel = TLatex()
    CMSlabel.SetTextSize( 0.05 )
    CMSlabel.DrawLatexNDC(0.2, 0.92, "CMS #scale[0.8]{#font[52]{Work In Progress}}")
    mXlabel = TLatex()
    mXlabel.SetTextSize( 0.03 )
    labelText = "mX = %.0f GeV"%(mXval)
    if "VR_" in tag:    labelText = labelText + " #font[42]{Validation Region}"
    if "CR_" in tag:    labelText = labelText + " #font[42]{Control Region}"
    mXlabel.DrawLatexNDC(0.55, 0.92, labelText)
    if "weights" in tag:    mXlabel.DrawTextNDC(0.2, 0.86, "3b reweighted")
    if "orig" in tag:    mXlabel.DrawTextNDC(0.2, 0.86, "before 3b reweighting")
    oneDdir = "OneDplots"
    path = "%s/%s"%(odir,oneDdir)
    # if not (os.path.exists(path)): os.makedirs(path) 
    # if not "orig" in tag: c1.SaveAs("%s/%s/mXvsmY_%s_%.0f.pdf"%(odir,oneDdir,tag,mXval))

def prepareRatios(h1,h2,tag, odir,h_sig,masspoint,year):
    h1 = h1.Clone()
    # h1.Sumw2()
    h2 = h2.Clone()
    # h2.Sumw2()
    #  h3 = h1.Clone("ratio")
    #  h3.Divide(h2)
    #  h3.GetZaxis().SetTitle("Ratio [model/target]")
    #  ksval, ksvalMaxDist, ksvalX = getKSTestRoot(h1,h2)
    #  h4 = h1.Clone("h1error")
    #  h4.GetZaxis().SetTitle("3b data "+tag+" Errors")
    #  h5 = h2.Clone("h2error")
    #  h5.GetZaxis().SetTitle("4b data Errors")
    #  #    for ix in range(1, h1.GetNbinsX()+1):#root bin convention - first bin starts at 1
    #  #        for iy in range(1, h1.GetNbinsY()+1):
    #  #            h4.SetBinError(ix,iy,0.)
    #  #            h4.SetBinContent(ix,iy,0.)
    #  #            h5.SetBinError(ix,iy,0.)
    #  #            h5.SetBinContent(ix,iy,0.)
    #  for ix in range(1, h1.GetNbinsX()+1):#root bin convention - first bin starts at 1
        #  for iy in range(1, h1.GetNbinsY()+1):
            #  h4.SetBinContent(ix,iy,h1.GetBinErrorUp(ix,iy))
            #  h5.SetBinContent(ix,iy,h2.GetBinErrorUp(ix,iy))
    #  h5.GetZaxis().SetRangeUser(0,17)
    #  h6 = h3.Clone("RatioOverError")
    #  h6test = h3.Clone("RatioOverErrorTest")
    #  # for ix in range(1, h1.GetNbinsX()+1):#root bin convention - first bin starts at 1
    #  #     for iy in range(1, h1.GetNbinsY()+1):
    #  #         h6.SetBinError(ix,iy,0.)
    #  #         h6.SetBinContent(ix,iy,0.)
    #  #         h6test.SetBinError(ix,iy,0.)
    #  #         h6test.SetBinContent(ix,iy,0.)
    #  for ix in range(1, h1.GetNbinsX()+1):#root bin convention - first bin starts at 1
        #  for iy in range(1, h1.GetNbinsY()+1):
            #  if not h3.GetBinContent(ix, iy)==0:
                #  h6.SetBinContent(ix,iy,h3.GetBinContent(ix,iy)/h3.GetBinErrorUp(ix,iy))
                #  h6test.SetBinContent(ix,iy,h3.GetBinContent(ix,iy)/TMath.Sqrt(((h1.GetBinErrorUp(ix,iy)/h1.GetBinContent(ix,iy))**2)+((h2.GetBinErrorUp(ix,iy)/h2.GetBinContent(ix,iy))**2)))
    #  h6.GetZaxis().SetTitle("Ratio [model/target] / error")
    #  h6test.GetZaxis().SetTitle("Ratio [model/target] / error")
    # h5.GetZaxis().SetRangeUser(0,17)
    # ksvalErr, ksvalMaxDistErr, ksvalXErr = getKSTestRoot(h4,h5)
    # h1.Divide(h4)
    # h2.Divide(h5)
    h7 =h2.Clone("sigma")
    h8 =h1.Clone("sigmaOverError")
    #  h9 =h1.Clone("sigmaOverError_test")
    h7.Add(h1,-1.)
    h7.GetZaxis().SetTitle("target - model")
    for ix in range(1, h1.GetNbinsX()+1):#root bin convention - first bin starts at 1
        for iy in range(1, h1.GetNbinsY()+1):
            if not h7.GetBinContent(ix, iy)==0:
                h8.SetBinContent(ix,iy,h7.GetBinContent(ix,iy)/h7.GetBinErrorUp(ix,iy))
                h8.SetBinError(ix,iy,0)
            # else: h8.SetBinContent(ix,iy,h7.GetBinContent(ix,iy)) 
            #  if not h7.GetBinContent(ix, iy)==0: h9.SetBinContent(ix,iy,h7.GetBinContent(ix,iy)/TMath.Sqrt((h1.GetBinError(ix,iy)**2)+(h2.GetBinError(ix,iy)**2)))
    h8.GetZaxis().SetTitle("(target - model) / error")
    #  h9.GetZaxis().SetTitle("(target - model) / error")
            # else: h9.SetBinContent(ix,iy,h7.GetBinContent(ix,iy)) 
    # h7.GetZaxis().SetRangeUser(0,9)
    # ksvalRatioErr, ksvalMaxDistRatioErr, ksvalXRatioErr = getKSTestRoot(h1,h2)
    # print("get n bins: ",h1.GetNbinsX())
    # print("get n bins Y: ",h1.GetNbinsY())
    # for i in range(36):
    #     print(h1.GetBinErrorUp(12,i),h1.GetBinErrorLow(12,i), h2.GetBinErrorUp(12,i), h2.GetBinErrorLow(12,i))
    # h3.GetXaxis().SetTitle("")
    # h3.GetYaxis().SetTitle()
    # h3.GetZaxis().SetTitle()
    # makemyplots ( h3 , "ratio_"+tag , ksval , ksvalMaxDist , ksvalX )
    #  makemyplots ( h4 , "3bErrors_"+tag , odir, -1 , -1 , -1,year )
    #  makemyplots ( h5 , "4bErrors_"+tag , odir, -1 , -1 , -1,year )
    # makemyplots ( h6 , "RatioOverError_"+tag , -1 , -1 , -1 )
    # makemyplots ( h6test , "RatioOverErrorTest_"+tag , -1 , -1 , -1 )
    #  makemyplots ( h7 , "Sub_"+tag , odir, -1 , -1 , -1 ,year)
    makemyplots ( h8 , "SubOverError_"+tag , odir, -1 , -1 , -1,year )
    # makemyplots ( h9 , "SubOverErrorTest_"+tag , -1 , -1 , -1 )   
    #################################################
    mXval = float(re.search("MX_(.*?)_",masspoint).group(1))
    mYval = float(masspoint.split("MY_",1)[1])
    binNum = h8.GetXaxis().FindBin(mXval)
    if "_binAbove" in tag: binNum += 1
    if "_binBelow" in tag: binNum -= 1
    binsY = [36, 45, 51, 57, 62, 66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 122, 132, 140, 148, 156, 164, 172, 180, 188, 196, 204, 212, 228, 244, 260, 276, 292, 308, 324, 340, 356, 372, 388, 412, 444, 476, 508, 540, 572, 604, 636, 668, 700, 732, 764, 828, 892, 956, 1020, 1084, 1148, 1212, 1276, 1340, 1404, 1468, 1564, 1692, 1820, 1948, 2076, 2204]
    # binsx = [212, 228, 244, 260, 276, 292, 308, 324, 340, 360, 392, 424, 456, 488, 520, 552, 584, 616, 648, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216, 1296, 1424, 1552, 1680, 1808, 1936, 2064, 2192, 2320]
    hOneD = TH1F( "OneDplot", "OneDplot", h8.GetNbinsY(), np.asarray(binsY, 'f'))
    hOneDabove = TH1F( "OneDplotabove", "OneDplotabove", h8.GetNbinsY(), np.asarray(binsY, 'f'))
    hOneDbelow = TH1F( "OneDplotbelow", "OneDplotbelow", h8.GetNbinsY(), np.asarray(binsY, 'f'))
    for iy in range(1, h8.GetNbinsY()+1):
        hOneD.SetBinContent(iy,h8.GetBinContent(binNum, iy))
        hOneDabove.SetBinContent(iy,h8.GetBinContent(binNum+1, iy))
        hOneDbelow.SetBinContent(iy,h8.GetBinContent(binNum-1, iy))
        if(h8.GetBinContent(binNum, iy))!=0:
            hOneD.SetBinError(iy,0.000001)
            hOneDabove.SetBinError(iy,0.000001)
            hOneDbelow.SetBinError(iy,0.000001)
    firstBin=0
    lastBin=-1
    firstBin =FindFirstBinContent(hOneD,firstBin) 
    firstBin =FindFirstBinContent(hOneDabove,firstBin) 
    firstBin =FindFirstBinContent(hOneDbelow,firstBin) 
    lastBin =FindLastBinContent(hOneD,lastBin) 
    lastBin =FindLastBinContent(hOneDabove,lastBin) 
    lastBin =FindLastBinContent(hOneDbelow,lastBin) 
    if firstBin is not 0: firstBin = firstBin -1
    if lastBin is not -1: lastBin =lastBin +1
    getOneDPlotwithSig(hOneD,firstBin,lastBin,tag+"_binCenter",odir,h_sig,masspoint,year)
    getOneDPlotwithSig(hOneDabove,firstBin,lastBin,tag+"_binAbove",odir,h_sig,masspoint,year)
    getOneDPlotwithSig(hOneDbelow,firstBin,lastBin,tag+"_binBelow",odir,h_sig,masspoint,year)
    #  del h1,h2,h3,h4,h5,h6,h6test,h7,h8,h9,hOneD,hOneDabove,hOneDbelow
    del h1,h2,h8,hOneD,hOneDabove,hOneDbelow

def makeplotsForRegion(dir_region, tag, odir, year):
    #  idir = "2017DataPlots_NMSSM_XYH_bbbb_dataDrivenStudies_aidan_2021Dec15"
    #  idir = "DataPlots_fullSubmission_2016_v34_aidan_rebinnned_2021Dec23_VR"
    idir = "DataPlots_fullSubmission_%s_v34_aidan_2022Jan26_VR"%(year)
    myfile = TFile.Open(idir + "/outPlotter.root")
    dir_data_3b = "data_BTagCSV_3btag"
    dir_data_4b = "data_BTagCSV"
    dir_data_3b_weights = "data_BTagCSV_dataDriven_kinFit" 
    histname = "_HH_kinFit_m_H2_m"
    myfile.cd(dir_data_3b+"/"+dir_region)
    h_3b = gDirectory.Get(dir_data_3b+"_"+dir_region+histname)
    myfile.cd(dir_data_3b_weights+"/"+dir_region)
    h_3b_weights = gDirectory.Get(dir_data_3b_weights+"_"+dir_region+histname)
    myfile.cd(dir_data_4b+"/"+dir_region)
    h_4b = gDirectory.Get(dir_data_4b+"_"+dir_region+histname)
        
    #  masspoint_list = ["MX_700_MY_300"]
    #  masspoint_list = ["MX_700_MY_300" , "MX_500_MY_200" , "MX_900_MY_400" , "MX_1400_MY_600" , "MX_1800_MY_800" , "MX_300_MY_125" , "MX_300_MY_150" , "MX_600_MY_400" , "MX_700_MY_500" , "MX_800_MY_600" , "MX_900_MY_250" , "MX_1000_MY_300" , "MX_1200_MY_200"]
    masspoint_list = [
        "MX_300_MY_60", "MX_300_MY_70", "MX_300_MY_80", "MX_300_MY_90", "MX_300_MY_100", "MX_300_MY_125", "MX_300_MY_150", "MX_400_MY_60", "MX_400_MY_70", "MX_400_MY_80", "MX_400_MY_90", "MX_400_MY_100", "MX_400_MY_125", "MX_400_MY_150", "MX_400_MY_200", "MX_400_MY_250", "MX_500_MY_60", "MX_500_MY_70", "MX_500_MY_80", "MX_500_MY_90", "MX_500_MY_100", "MX_500_MY_125", "MX_500_MY_150", "MX_500_MY_200", "MX_500_MY_250", "MX_500_MY_300", "MX_600_MY_60", "MX_600_MY_70", "MX_600_MY_80", "MX_600_MY_90", "MX_600_MY_100", "MX_600_MY_125", "MX_600_MY_150", "MX_600_MY_200", "MX_600_MY_250", "MX_600_MY_300", "MX_600_MY_400", "MX_700_MY_60", "MX_700_MY_70", "MX_700_MY_80", "MX_700_MY_90", "MX_700_MY_100", "MX_700_MY_125", "MX_700_MY_150", "MX_700_MY_200", "MX_700_MY_250", "MX_700_MY_300", "MX_700_MY_400", "MX_700_MY_500", "MX_800_MY_60", "MX_800_MY_70", "MX_800_MY_80", "MX_800_MY_90", "MX_800_MY_100", "MX_800_MY_125", "MX_800_MY_150", "MX_800_MY_200", "MX_800_MY_250", "MX_800_MY_300", "MX_800_MY_400", "MX_800_MY_500", "MX_800_MY_600", "MX_900_MY_60", "MX_900_MY_70", "MX_900_MY_80", "MX_900_MY_90", "MX_900_MY_100", "MX_900_MY_125", "MX_900_MY_150", "MX_900_MY_200", "MX_900_MY_250", "MX_900_MY_300", "MX_900_MY_400", "MX_900_MY_500", "MX_900_MY_600", "MX_900_MY_700", "MX_1000_MY_60", "MX_1000_MY_70", "MX_1000_MY_80", "MX_1000_MY_90", "MX_1000_MY_100", "MX_1000_MY_125", "MX_1000_MY_150", "MX_1000_MY_200", "MX_1000_MY_250", "MX_1000_MY_300", "MX_1000_MY_400", "MX_1000_MY_500", "MX_1000_MY_600", "MX_1000_MY_700", "MX_1000_MY_800", "MX_1100_MY_90", "MX_1100_MY_100", "MX_1100_MY_125", "MX_1100_MY_150", "MX_1100_MY_200", "MX_1100_MY_250", "MX_1100_MY_300", "MX_1100_MY_400", "MX_1100_MY_500", "MX_1100_MY_600", "MX_1100_MY_700", "MX_1100_MY_800", "MX_1100_MY_900", "MX_1200_MY_90", "MX_1200_MY_100", "MX_1200_MY_125", "MX_1200_MY_150", "MX_1200_MY_200", "MX_1200_MY_250", "MX_1200_MY_300", "MX_1200_MY_400", "MX_1200_MY_500", "MX_1200_MY_600", "MX_1200_MY_700", "MX_1200_MY_800", "MX_1200_MY_900", "MX_1200_MY_1000", "MX_1400_MY_90", "MX_1400_MY_100", "MX_1400_MY_125", "MX_1400_MY_150", "MX_1400_MY_200", "MX_1400_MY_250", "MX_1400_MY_300", "MX_1400_MY_400", "MX_1400_MY_500", "MX_1400_MY_600", "MX_1400_MY_700", "MX_1400_MY_800", "MX_1400_MY_900", "MX_1400_MY_1000", "MX_1400_MY_1200", "MX_1600_MY_90", "MX_1600_MY_100", "MX_1600_MY_125", "MX_1600_MY_150", "MX_1600_MY_200", "MX_1600_MY_250", "MX_1600_MY_300", "MX_1600_MY_400", "MX_1600_MY_500", "MX_1600_MY_600", "MX_1600_MY_700", "MX_1600_MY_800", "MX_1600_MY_900", "MX_1600_MY_1000", "MX_1600_MY_1200", "MX_1600_MY_1400", "MX_1800_MY_90", "MX_1800_MY_100", "MX_1800_MY_125", "MX_1800_MY_150", "MX_1800_MY_200", "MX_1800_MY_250", "MX_1800_MY_300", "MX_1800_MY_400", "MX_1800_MY_500", "MX_1800_MY_600", "MX_1800_MY_700", "MX_1800_MY_800", "MX_1800_MY_900", "MX_1800_MY_1000", "MX_1800_MY_1200", "MX_1800_MY_1400", "MX_1800_MY_1600", "MX_2000_MY_90", "MX_2000_MY_100", "MX_2000_MY_125", "MX_2000_MY_150", "MX_2000_MY_200", "MX_2000_MY_250",\
        "MX_2000_MY_300", "MX_2000_MY_400", "MX_2000_MY_500", "MX_2000_MY_600", "MX_2000_MY_700", "MX_2000_MY_800", "MX_2000_MY_900", "MX_2000_MY_1000", "MX_2000_MY_1200", "MX_2000_MY_1400", "MX_2000_MY_1600", "MX_2000_MY_1800" ]
    #  masspoint_list = [ "MX_1800_MY_800"]
    sigdirHeader = "sig_NMSSM_bbbb_"
    sigDirectory = "selectionbJets_SignalRegion"
    for masspoint in masspoint_list:
        myfile.cd(sigdirHeader+masspoint+"/"+sigDirectory)
        h_sig = gDirectory.Get(sigdirHeader+masspoint+"_"+sigDirectory+histname)
        prepareRatios(h_3b,h_4b,tag+"_orig", odir,h_sig,masspoint, year)
        prepareRatios(h_3b_weights,h_4b,tag+"_weights", odir,h_sig,masspoint, year)

# ********************
#run pyROOT in batch mode  - ie don't show graphics!
# 
gROOT.SetBatch(True)
# ********************
# odir = "studies/plotting2021Dec13/plots2021Dec16_2"
# odir = "studies/plotting2021Dec13/plots2021Dec17"
#  odir = "studies/plotting2021Dec13/plots2021Dec23"
#  odir = "studies/plotting2021Dec13/plots2022Jan27"
odir = "studies/plotting2021Dec13/plots2022Jan28"
path = "%s/"%(odir)
if not (os.path.exists(path)): os.makedirs(path) 
years = ["2016","2017","2018"]
for year in years:
    #  odir = "studies/plotting2021Dec13/plots2022Jan27/%s"%(year)
#  year = "2016"
    odir = "studies/plotting2021Dec13/plots2022Jan28/%s"%(year)
    directory = "selectionbJets_ControlRegionBlinded"
    makeplotsForRegion(directory, "CR", odir,year)
    directory = "selectionbJets_ValidationRegionBlinded"
    makeplotsForRegion(directory, "VR",odir,year)

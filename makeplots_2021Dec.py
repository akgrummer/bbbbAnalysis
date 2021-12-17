from ROOT import TFile,TH1F,TH2F,TCanvas,gStyle,gPad,gDirectory,TLatex,gROOT,PyConfig,TMath
# PyConfig.IgnoreCommandLineOptions = False
import numpy as np

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

def makemyplots(h1,tag, odir,ksval,ksvalMaxDist,ksvalX):
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
    if not ksval<0: KSlabel.DrawTextNDC(0.2, 0.8, ksval)
    if not ksvalMaxDist<0: KSlabel.DrawTextNDC(0.2, 0.76, ksvalMaxDist)
    if not ksvalX<0: KSlabel.DrawTextNDC(0.2, 0.72, ksvalX)
    #*************
    # save the plot
    c1.SaveAs("%s/mXvsmY_%s.pdf"%(odir,tag))
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

def getOneDPlotwithOtherPlots(h1, mXval,tag, odir):
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
    gPad.SetMargin(0.16,0.05,0.12,0.09) #left,right,bottom,top    
    hOneD.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
    hOneD.SetMarkerSize(0.7)
    hOneD.SetMarkerColor(1)
    hOneD.SetLineColor(1)
    hOneD.SetMarkerStyle(8)
    hOneD.SetLineColor(1)
    hOneD.SetLineWidth(1)
    hOneD.GetXaxis().SetRangeUser(0,mXval - 100)
    hOneD.GetYaxis().SetTitle("(target - model) / error")
    hOneD.GetXaxis().SetTitle("m_{Y} [GeV]")
    hOneD.Draw("ple")
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
    if not "orig" in tag: c1.SaveAs("%s/%s/mXvsmY_%s_%.0f.pdf"%(odir,oneDdir,tag,mXval))

def getOneDPlot(h1, mXval,tag, odir):
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
    gPad.SetMargin(0.16,0.05,0.12,0.09) #left,right,bottom,top    
    hOneD.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
    hOneD.SetMarkerSize(0.7)
    hOneD.SetMarkerColor(1)
    hOneD.SetLineColor(1)
    hOneD.SetMarkerStyle(8)
    hOneD.SetLineColor(1)
    hOneD.SetLineWidth(1)
    hOneD.GetXaxis().SetRangeUser(0,mXval - 100)
    hOneD.GetYaxis().SetTitle("(target - model) / error")
    hOneD.GetXaxis().SetTitle("m_{Y} [GeV]")
    hOneD.Draw("ple")
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
    if not "orig" in tag: c1.SaveAs("%s/%s/mXvsmY_%s_%.0f.pdf"%(odir,oneDdir,tag,mXval))

def prepareRatios(h1,h2,tag, odir):
    h1 = h1.Clone()
    h1.Sumw2()
    h2 = h2.Clone()
    h2.Sumw2()
    h3 = h1.Clone("ratio")
    h3.Divide(h2)
    h3.GetZaxis().SetTitle("Ratio [model/target]")
    ksval, ksvalMaxDist, ksvalX = getKSTestRoot(h1,h2)
    h4 = h1.Clone("h1error")
    h4.GetZaxis().SetTitle("3b data "+tag+" Errors")
    h5 = h2.Clone("h2error")
    h5.GetZaxis().SetTitle("4b data Errors")
    #    for ix in range(1, h1.GetNbinsX()+1):#root bin convention - first bin starts at 1
    #        for iy in range(1, h1.GetNbinsY()+1):
    #            h4.SetBinError(ix,iy,0.)
    #            h4.SetBinContent(ix,iy,0.)
    #            h5.SetBinError(ix,iy,0.)
    #            h5.SetBinContent(ix,iy,0.)
    for ix in range(1, h1.GetNbinsX()+1):#root bin convention - first bin starts at 1
        for iy in range(1, h1.GetNbinsY()+1):
            h4.SetBinContent(ix,iy,h1.GetBinErrorUp(ix,iy))
            h5.SetBinContent(ix,iy,h2.GetBinErrorUp(ix,iy))
    h5.GetZaxis().SetRangeUser(0,17)
    h6 = h3.Clone("RatioOverError")
    h6test = h3.Clone("RatioOverErrorTest")
    # for ix in range(1, h1.GetNbinsX()+1):#root bin convention - first bin starts at 1
    #     for iy in range(1, h1.GetNbinsY()+1):
    #         h6.SetBinError(ix,iy,0.)
    #         h6.SetBinContent(ix,iy,0.)
    #         h6test.SetBinError(ix,iy,0.)
    #         h6test.SetBinContent(ix,iy,0.)
    for ix in range(1, h1.GetNbinsX()+1):#root bin convention - first bin starts at 1
        for iy in range(1, h1.GetNbinsY()+1):
            if not h3.GetBinContent(ix, iy)==0:
                h6.SetBinContent(ix,iy,h3.GetBinContent(ix,iy)/h3.GetBinErrorUp(ix,iy))
                h6test.SetBinContent(ix,iy,h3.GetBinContent(ix,iy)/TMath.Sqrt(((h1.GetBinErrorUp(ix,iy)/h1.GetBinContent(ix,iy))**2)+((h2.GetBinErrorUp(ix,iy)/h2.GetBinContent(ix,iy))**2)))
    h6.GetZaxis().SetTitle("Ratio [model/target] / error")
    h6test.GetZaxis().SetTitle("Ratio [model/target] / error")
    # h5.GetZaxis().SetRangeUser(0,17)
    # ksvalErr, ksvalMaxDistErr, ksvalXErr = getKSTestRoot(h4,h5)
    # h1.Divide(h4)
    # h2.Divide(h5)
    h7 =h2.Clone("sigma")
    h8 =h1.Clone("sigmaOverError")
    h9 =h1.Clone("sigmaOverError_test")
    h7.Add(h1,-1.)
    h7.GetZaxis().SetTitle("target - model")
    for ix in range(1, h1.GetNbinsX()+1):#root bin convention - first bin starts at 1
        for iy in range(1, h1.GetNbinsY()+1):
            if not h7.GetBinContent(ix, iy)==0: h8.SetBinContent(ix,iy,h7.GetBinContent(ix,iy)/h7.GetBinErrorUp(ix,iy))
            # else: h8.SetBinContent(ix,iy,h7.GetBinContent(ix,iy)) 
            if not h7.GetBinContent(ix, iy)==0: h9.SetBinContent(ix,iy,h7.GetBinContent(ix,iy)/TMath.Sqrt((h1.GetBinError(ix,iy)**2)+(h2.GetBinError(ix,iy)**2)))
    h8.GetZaxis().SetTitle("(target - model) / error")
    h9.GetZaxis().SetTitle("(target - model) / error")
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
    makemyplots ( h4 , "3bErrors_"+tag , odir, -1 , -1 , -1 )
    makemyplots ( h5 , "4bErrors_"+tag , odir, -1 , -1 , -1 )
    # makemyplots ( h6 , "RatioOverError_"+tag , -1 , -1 , -1 )
    # makemyplots ( h6test , "RatioOverErrorTest_"+tag , -1 , -1 , -1 )
    makemyplots ( h7 , "Sub_"+tag , odir, -1 , -1 , -1 )
    makemyplots ( h8 , "SubOverError_"+tag , odir, -1 , -1 , -1 )
    # makemyplots ( h9 , "SubOverErrorTest_"+tag , -1 , -1 , -1 )
    getOneDPlot(h8,300.,tag,odir)
    getOneDPlot(h8,400.,tag,odir)
    getOneDPlot(h8,800.,tag,odir)
    getOneDPlot(h8,1000.,tag,odir)
    del h1,h2,h3,h4,h5,h6,h6test,h7,h8,h9

def makeplotsForRegion(dir_region, tag, odir):
    idir = "2017DataPlots_NMSSM_XYH_bbbb_dataDrivenStudies_aidan"
    myfile = TFile.Open(idir + "/outPlotter.root")
    # myfile.cd("sig_NMSSM_bbbb_"+tag+"/selectionbJets_SignalRegion")
    dir_data_3b = "data_BTagCSV_3btag"
    dir_data_4b = "data_BTagCSV"
    dir_data_3b_weights = "data_BTagCSV_dataDriven_kinFit" 
    myfile.cd(dir_data_3b+"/"+dir_region)
    h_3b = gDirectory.Get(dir_data_3b+"_"+dir_region+"_HH_m_H2_m")
    myfile.cd(dir_data_3b_weights+"/"+dir_region)
    h_3b_weights = gDirectory.Get(dir_data_3b_weights+"_"+dir_region+"_HH_m_H2_m")
    myfile.cd(dir_data_4b+"/"+dir_region)
    h_4b = gDirectory.Get(dir_data_4b+"_"+dir_region+"_HH_m_H2_m")
        
    sigdir = "sig_NMSSM_bbbb_MX_700_MY_300"
    #sigdir = "sig_NMSSM_bbbb_MX_500_MY_200"
    #sigdir = "sig_NMSSM_bbbb_MX_900_MY_400"
    #sigdir = "sig_NMSSM_bbbb_MX_1400_MY_600"
    #sigdir = "sig_NMSSM_bbbb_MX_1800_MY_800"
    #sigdir = "sig_NMSSM_bbbb_MX_300_MY_125"
    #sigdir = "sig_NMSSM_bbbb_MX_300_MY_150"
    #sigdir = "sig_NMSSM_bbbb_MX_600_MY_400"
    #sigdir = "sig_NMSSM_bbbb_MX_700_MY_500"
    #sigdir = "sig_NMSSM_bbbb_MX_800_MY_600"
    #sigdir = "sig_NMSSM_bbbb_MX_900_MY_250"
    #sigdir = "sig_NMSSM_bbbb_MX_1000_MY_300"
    #sigdir = "sig_NMSSM_bbbb_MX_1200_MY_200" 


    prepareRatios(h_3b,h_4b,tag+"_orig", odir)
    prepareRatios(h_3b_weights,h_4b,tag+"_weights", odir)


# ********************
#run pyROOT in batch mode  - ie don't show graphics!
# 
gROOT.SetBatch(True)
# ********************
# odir = "studies/plotting2021Dec13/plots2021Dec16_2"
odir = "studies/plotting2021Dec13/plots2021Dec17"
directory = "selectionbJets_ControlRegionBlinded"
makeplotsForRegion(directory, "CR", odir)
directory = "selectionbJets_ValidationRegionBlinded"
makeplotsForRegion(directory, "VR",odir)
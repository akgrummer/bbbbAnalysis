import ROOT
from ROOT import TLatex, TLegend, TH1D,gDirectory,TLine, TBox
import os
import math
import csv
import sys


bkgNormPerMassGroupDictionary = {
    "2016" : { "0" : "1.022", "1" :  "1.022", "2" :  "1.018", "3" :  "1.018", "4" :  "1.042", "none" : "1.010"},
    "2017" : { "0" : "1.015", "1" :  "1.015", "2" :  "1.017", "3" :  "1.013", "4" :  "1.019", "none" : "1.010"},
    "2018" : { "0" : "1.046", "1" :  "1.039", "2" :  "1.033", "3" :  "1.024", "4" :  "1.012", "none" : "1.010"},
}

ROOT.gROOT.SetBatch(True)
def makePlot(labels,xMin, xMax, globalMaxVal,massMap):
    fittype=labels[0]
    totalFit=False
    if ("total" in fittype):
        totalFit=True
        fittype="fit_s"
    tag = labels[1]
    year = labels[2]
    # sig = "sig_NMSSM_bbbb_MX_1200_MY_300"
    massGroup = labels[3]
    sig = labels[4]
    mXval = sig.split("MX_")[1].split("_MY_")[0]
    mYval = sig.split("MX_")[1].split("_MY_")[1]

    # fFit = ROOT.TFile( "FitDiagnostics/{0}/fitDiagnostics2016.root".format("test"))
    fName = "FitDiagnostics/{0}/{1}/FitDiagnostics_{1}_{2}_id0_sig0.root".format(tag, year, sig)
    fFit = ROOT.TFile(fName)
    fitName = "selectionbJets_SignalRegion_CMS_th1x_{0}".format(fittype)
    theFit = fFit.Get(fitName)

    fFit.cd("shapes_{0}/selectionbJets_SignalRegion".format(fittype));
    grDataShape = fFit.Get("shapes_{0}/selectionbJets_SignalRegion/data".format(fittype))
    hBkgShape = fFit.Get("shapes_{0}/selectionbJets_SignalRegion/data_BTagCSV_dataDriven_kinFit".format(fittype))
    if (totalFit): hBkgShape = fFit.Get("shapes_{0}/selectionbJets_SignalRegion/total".format(fittype))
    hCov=fFit.Get("shapes_{0}/selectionbJets_SignalRegion/total_covar".format(fittype))
    hSigShape = fFit.Get("shapes_{0}/selectionbJets_SignalRegion/{1}".format(fittype,sig))
    if ("fit_b" in fittype): hSigShape = fFit.Get("shapes_{0}/selectionbJets_SignalRegion/{1}".format("prefit",sig)) # plot the prefit distribution for to compare with background only dist

    inputHistsFileName = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}/outPlotter_massGroup{2}.root".format(year, tag, massGroup)
    inFile = ROOT.TFile(inputHistsFileName)
    dir_shape_nom = "data_BTagCSV_dataDriven_kinFit"
    dir_shape_down = "data_BTagCSV_dataDriven_kinFit_downRefined"
    dir_shape_up = "data_BTagCSV_dataDriven_kinFit_upRefined"
    dir_region = "selectionbJets_SignalRegion"
    varname = "HH_kinFit_m_H2_m_Rebinned_Unrolled"
    inFile.cd( dir_shape_nom+"/"+dir_region )
    hShapeNom = gDirectory.Get( dir_shape_nom+"_"+dir_region+"_"+varname )
    inFile.cd( dir_shape_down+"/"+dir_region )
    hShapeDown = gDirectory.Get( dir_shape_down+"_"+dir_region+"_"+varname )
    inFile.cd( dir_shape_up+"/"+dir_region )
    hShapeUp     = gDirectory.Get( dir_shape_up+"_"+dir_region+"_"+varname )



    hNewPoints = grDataShape.GetN()
    hDataShape = ROOT.TH1D( "hData", "hData", hNewPoints, 0, hNewPoints);
    hpullShape = ROOT.TH1D( "hpull", "hpull", hNewPoints, 0, hNewPoints);
    for i in range(1,hNewPoints+1):
        dataVal = grDataShape.Eval(float(i)-0.5)
        dataErr = grDataShape.GetErrorY(i-1)
        bkgVal =    hBkgShape.GetBinContent(i)
        if ("fit_b" in fittype):
            # bkgErr = hBkgShape.GetBinError(i)
            # bkgErr = hCov.GetBinContent(i,i)
            # hBkgShape.SetBinError(i,bkgErr)
            # pull = (dataVal-bkgVal)/math.sqrt(bkgErr**2+dataErr**2)
            pull = (dataVal-bkgVal)/math.sqrt(dataErr**2)
        elif("prefit" in fittype):
            # bkgErr = math.sqrt(hBkgShape.GetBinContent(i))
            bkgErr = hBkgShape.GetBinError(i)
            shapeErr=hShapeUp.GetBinContent(i)-hBkgShape.GetBinContent(i)
            normErr=bkgVal * ( float(bkgNormPerMassGroupDictionary[str(year)][str(massGroup)]) - 1 )
            # pull = (dataVal-bkgVal)/math.sqrt(dataErr**2)
            pull = (dataVal-bkgVal)/math.sqrt(dataErr**2+bkgErr**2+shapeErr**2+normErr**2)
            # if("2017" in year and 0 == massGroup and xMax<205): print(i, dataVal, bkgVal, dataErr, bkgErr, shapeErr, pull)
        elif("fit_s" in fittype):
            pull = (dataVal-bkgVal)/math.sqrt(dataErr**2)
        else:
            print("need to define errors for this fit type first")
            sys.exit()
        hDataShape.SetBinContent(i, dataVal)
        hDataShape.SetBinError(i, dataErr)
        hpullShape.SetBinContent(i, pull)
        # hpullShape.SetBinError(i, dataErr)
        # if("2016" in year and 0 == massGroup): print(dataVal, bkgVal, dataErr, bkgErr, math.sqrt(bkgVal), pull)
        # if("2017" in year and 0 == massGroup and xMin==200 and fittype=="fit_b"): print(i, dataVal, bkgVal, dataErr, bkgErr, pull)


    hDataError=hDataShape.Clone()
    hBkgError=hBkgShape.Clone()

    #### define the canvas
    c1 = ROOT.TCanvas('c1', 'c1',800,600)
    ROOT.gStyle.SetOptStat(0) # remove the stats box
    ROOT.gStyle.SetOptTitle(0) # remove the title

    #### define the upper and lower pads
    p1 = ROOT.TPad("p1", "p1", 0., 0.45, 1., 1.0, 0, 0, 0)
    p1.SetMargin(0.12,0.05,0.05,0.09) #left,right,bottom,top
    p1.SetTicks(1,1)
    p1.Draw()

    psig = ROOT.TPad("psig", "psig", 0., 0.3, 1., 0.45, 0, 0, 0)
    psig.SetMargin(0.12,0.05,0.09,0.05) #left,right,bottom,top
    psig.SetTicks(1,1)
    psig.Draw()

    p2 = ROOT.TPad("p2", "p2", 0., 0.05, 1., 0.3, 0, 0, 0)
    p2.SetMargin(0.12,0.05,0.38,0.05) #left,right,bottom,top
    p2.SetTicks(1,1)
    p2.Draw()

    p3 = ROOT.TPad("p3", "p3", 0., 0.05, 1., 0.3, 0, 0, 0)
    p3.SetMargin(0.12,0.05,0.38,0.05) #left,right,bottom,top
    p3.SetTicks(1,1)
    p3.Draw()

    p1.cd()
    # p1.DrawFrame(xMin,0,xMax,350);
    # hDataShape.Draw()
    hBkgShape.Draw("hist")
    hDataError.Draw("e2 same")
    hDataError.SetFillColor(45)
    hDataError.SetFillStyle(3144)
    hDataError.SetLineColor(0)
    if("prefit" in fittype):
        hBkgError.Draw("e1 same")
        hBkgError.SetFillColor(4)
        hBkgError.SetFillStyle(1001)
        hBkgError.SetLineColor(1)
        hBkgError.SetLineWidth(2)

    hBkgShape.Draw("hist same")
    hDataShape.Draw("hist same")
    # hShapeDown.Draw("hist same")
    # hShapeUp.Draw("hist same")


    # hError.Draw("samef")
    # hBkg.Draw("same l")
    # hDataShape.Draw("same p")
    #hDataShapeError.Draw("same e")
    #xaxis
    hBkgShape.GetXaxis().SetRange(xMin, xMax-1)
    hDataShape.GetXaxis().SetRange(xMin, xMax-1)
    yMax = max(hBkgShape.GetMaximum(), hDataShape.GetMaximum(), globalMaxVal)
    globalMaxVal=yMax
    # yMax = hDataShape.GetMaximum()
    axisScaleFactor=1.55
    if(massGroup==4): axisScaleFactor=1.65
    hBkgShape.GetYaxis().SetRangeUser(0, yMax*axisScaleFactor)
    hDataShape.GetYaxis().SetRangeUser(0, yMax*axisScaleFactor)
    # axis = hDataShape.GetXaxis()
    # axis.SetLimits(xMin, xMax)
    hDataShape.GetXaxis().SetLabelSize(0.)
    hDataShape.GetXaxis().SetTitleSize(0.)
    # hBkg.GetXaxis().SetRangeUser(xMin, xMax)
    hBkgShape.GetXaxis().SetLabelSize(0.)
    hBkgShape.GetXaxis().SetTitleSize(0.)
    #yaxis
    hDataShape.GetYaxis().SetTitle("Entries/bin")
    hDataShape.GetYaxis().SetLabelSize(0.05)
    hDataShape.GetYaxis().SetTitleSize(0.05)
    hDataShape.GetYaxis().SetTitleOffset(1.1)
    hDataShape.GetYaxis().SetTickLength(0.02)
    hBkgShape.GetYaxis().SetTitle("Entries/bin")
    hBkgShape.GetYaxis().SetLabelSize(0.05)
    hBkgShape.GetYaxis().SetTitleSize(0.05)
    hBkgShape.GetYaxis().SetTitleOffset(1.1)
    hBkgShape.GetYaxis().SetTickLength(0.02)

    hDataShape.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
    hDataShape.SetMarkerSize(0.7)
    hDataShape.SetMarkerColor(1)
    hDataShape.SetLineColor(ROOT.kRed+2)
    hDataShape.SetLineWidth(2)
    hBkgShape.SetLineColor(ROOT.kBlue+2)
    if(totalFit): hBkgShape.SetLineColor(ROOT.kYellow+2)
    hBkgShape.SetLineWidth(2)

    # hError.SetLineColor(0)
    # hShapeUp.SetLineColor(ROOT.kGreen+2)
    # hShapeUp.SetLineWidth(2)
    # hShapeDown.SetLineColor(ROOT.kGreen+2)
    # hShapeDown.SetLineWidth(2)
    # hShapeNom.SetLineColor(ROOT.kYellow+2)
    # hShapeNom.SetLineWidth(2)

    CMSlabel = TLatex()
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 30 )
    CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
    plotlabels = TLatex()
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    #  labelText = "mX = %.0f GeV, mY = %.0f GeV"%(mXval,mYval)
    labelText = ""
    if "VR" in tag:      labelText = labelText + "Validation Region"
    if "CR" in tag:      labelText = labelText + "Control Region"
    if "SR" in tag:      labelText = labelText + "Signal Region"
    plotlabels.DrawLatexNDC(0.60, 0.93, labelText)
    plotlabels = ROOT.TLatex()
    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(20)
    plotlabels.DrawTextNDC(0.83, 0.93, year)
    plotlabels.SetTextFont(43)
    plotlabels.SetTextSize(20)
    fitLabel = ""
    plotlabels.SetTextSize(18)
    if ("_b" in fittype):
        fitLabel = "Background Only Fit"
    if ("_s" in fittype):
        fitLabel = "Fit with Signal"
    if ("pre" in fittype):
        fitLabel = "Pre-fit"
    plotlabels.SetTextSize(14)
    plotlabels.SetTextFont(53)
    plotlabels.DrawLatexNDC(0.45, 0.93,"mX={0},mY={1}".format(mXval, mYval))
    plotlabels.DrawLatexNDC(0.8, 0.83,"Mass Group {}".format(massGroup))
    plotlabels.SetTextSize(20)
    plotlabels.SetTextFont(63)
    plotlabels.SetTextAlign(31)
    plotlabels.DrawLatexNDC(0.78, 0.83,fitLabel)
    # plotlabels.DrawLatexNDC(0.65, 0.77,labels[2])

#       hDataShapeError.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
#       hDataShapeError.SetMarkerSize(0)
#       hDataShapeError.SetMarkerColor(1)
#       hDataShapeError.SetLineColor(1)
#       hDataShapeError.SetLineWidth(1)

    # hBkg.GetXaxis().SetLimits(xMin, xMax)
    # hError.GetXaxis().SetLimits(xMin, xMax)
    # hDataShape.GetXaxis().SetLimits(xMin, xMax)
    ROOT.gPad.Modified()
    ROOT.gPad.Update()
    # hDataShape.Sumw2()

    # hDataShape.Divide(hBkg)
    # hDataShape.Draw()
    # hDataShape.Draw("same l")

    p2.cd()
    # p2.DrawFrame(xMin,-10,xMax,10);
    # hNew = theFit.residHist(rooFitObjects["data"], rooFitObjects["bkgFit"], True)
    # hNew = ROOT.TH1D( "hratio", "hratio", hNewPoints, 0, hNewPoints);
    # if (xMax<hNewPoints):
    #       for i in range(xMax, hNewPoints):
    #           hNew.RemovePoint(i)
    # if (xMin>0):
    # hNew = hDataShape.Clone("hNew")
    # # for i in range(0,hNewPoints):
    #           #f if hBkgShape.GetBinContent(i) !=0: hNew.SetBinContent(i, hDataShape.Eval(i)/hBkgShape.GetBinContent(i))
    # hNew.Divide(hBkgShape)
    # hpullShape.Draw("p")
    hpullShape.Draw("")
    # hNew.Draw("same B")
    # hpullShape.Draw("same p")
    hpullShape.GetYaxis().SetLabelSize(0.12)
    hpullShape.GetYaxis().SetNdivisions(503)
    hpullShape.GetXaxis().SetTickLength(0.1)
    hpullShape.GetXaxis().SetTitleSize(.16)
    hpullShape.GetXaxis().SetTitleOffset(1.2)
    hpullShape.GetXaxis().SetTitle("Unrolled Bins (mX bin centers)")
    hpullShape.GetYaxis().SetTickLength(0.03)
    hpullShape.GetYaxis().SetTitleSize(.12)
    hpullShape.GetYaxis().SetTitleOffset(0.4)
    if ( "prefit" in fittype ): hpullShape.GetYaxis().SetTitle("pull #[]{#frac{data-bkg}{#sqrt{#sigma_{data}^{2}+#sigma_{bkg}^{2}}}}")
    elif ( "fit_" in fittype ): hpullShape.GetYaxis().SetTitle("pull #[]{#frac{data-bkg}{#sigma_{data}}}")
    if(totalFit): hpullShape.GetYaxis().SetTitle("pull #[]{#frac{data-fit}{#sigma_{data}}}")
    hpullShape.SetFillColor(32)
    hpullShape.SetLineColor(1)

    hpullShape.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
    hpullShape.SetMarkerSize(0.7)
    hpullShape.SetMarkerColor(1)
    # hpullShape.SetLineColor(1)
    # hNew.SetLineWidth(0)
    hpullShape.GetXaxis().SetRange(xMin,xMax-1)
    if("VR" in tag): hpullShape.GetYaxis().SetRangeUser(-2.8,2.8)
    else: hpullShape.GetYaxis().SetRangeUser(-5,5)
    # else: hpullShape.GetYaxis().SetRangeUser(-3.6,3.6)
    # hpullShape.GetYaxis().SetRangeUser(0.,2.)
    # hNew.GetXaxis().SetLimits(xMin, xMax)
    # axis2 = hNew.GetXaxis()
    # axis2.SetLimits(xMin, xMax)
    # ROOT.gPad.Modified()
    # ROOT.gPad.Update()
    # hShapeNom.Draw("hist same")

    hpullShape2 = hpullShape.Clone()
    totalBins=len(massMap.keys())
    # print(xMax/100, totalBins/100)
    if (xMax/100 <= totalBins/100): divisions=99
    else: divisions = totalBins % 100
    # else: divisions = 25
    subdivisions=2
    ticks = 100*subdivisions + divisions
    psig.cd()

    ySigMax = hSigShape.GetMaximum()
    ySigMin = hSigShape.GetMinimum()
    hSigShape.GetXaxis().SetRange(xMin, xMax-1)
    hSigShape.SetLineColor(ROOT.kGreen+2)
    hSigShape.SetLineWidth(2)


    hSigShape.Draw("hist")

    hSigShape.GetYaxis().SetLabelSize(0.16)
    hSigShape.GetYaxis().SetNdivisions(503)
    hSigShape.GetXaxis().SetTickLength(0.1)
    hSigShape.GetXaxis().SetTitleOffset(1.2)
    hSigShape.GetYaxis().SetTitle("Entries/bin")
    hSigShape.GetXaxis().SetTitle("")
    hSigShape.GetYaxis().SetTickLength(0.02)
    hSigShape.GetYaxis().SetTitleSize(.16)
    hSigShape.GetYaxis().SetTitleOffset(0.3)

    # if (massGroup==0 and ): hSigShape.GetYaxis().SetRangeUser( ySigMax*1.2)
    # else:
    if(ySigMax<0.001): hSigShape.GetYaxis().SetRangeUser(ySigMin*1.2, 3)
    else: hSigShape.GetYaxis().SetRangeUser(0, ySigMax*1.2)
    hSigShape.GetXaxis().SetLabelSize(0.)
    hSigShape.GetXaxis().SetNdivisions(ticks);

    p3.cd()
    p3.SetFillStyle(4000)
    hpullShape2.Draw("")
    hpullShape2.GetXaxis().SetLabelSize(0.)
    hpullShape2.GetXaxis().SetNdivisions(ticks);
    p2.cd()

    mYlines = TLine(0.,0.,0.,yMax)
    mYlines.SetLineWidth(1)
    mYlines.SetLineColor(1)
    mYlines.SetLineStyle(7)
    mYlabels = TLatex()
    mYlabels.SetTextFont(43)
    mYlabels.SetTextSize(14)
    p1.cd()
    rightBox = TBox()
    boxColor=0
    rightBox.SetFillColor(boxColor)
    # rightBox.SetFillColorAlpha(2,0.4)
    rightBox.SetLineColor(boxColor)
    rightBox.SetLineWidth(2)
    rightBox.SetFillStyle(1001)
    # rightBox.DrawBox(-0.9,yMax,1.5,yMax*1.545)
    # rightBox.DrawBox(xMin-0.9,yMax,xMin+1.5,yMax*1.545)# box at 0
    # rightBox.DrawBox(xMax-3.5,yMax,xMax-1.1,yMax*1.545)# box at 100
    # rightBox.DrawBox(totalBins-1.5,yMax,totalBins+0.9,yMax*1.545)# box for last bins set
    p2.cd()
    lastmY=0
    # for i in range(1,hNewPoints+1):
    for i in range(xMin,xMax):
        # if xMax<i: break
        if(i==0 or totalBins<i): continue
        thismX=massMap[i][0]
        thismY=massMap[i][1]
        # hpullShape.GetXaxis().SetBinLabel(i, "mX={},mY={}".format(thismX,thismY))
        hpullShape.GetXaxis().SetBinLabel(i, "mX={}".format(thismX))
        if lastmY != thismY:
            # rightBox.DrawBox(90,yMax, 100, yMax*1.55)
            p1.cd(); mYlines.DrawLine(i-1,0.05*yMax,i-1,yMax*1.22); psig.cd(); mYlines.DrawLine(i-1,0.05*ySigMax,i-1,ySigMax*1.2); p3.cd(); mYlines.DrawLine(i-1,0.95*-5,i-1,0.95*5); p2.cd()
            if (massGroup==4):
                # if ((i-xMin)==1 and 2<xMin): lastmY = thismY; continue
                if (65<divisions):
                    mYlabels.SetTextAlign(23); mYlabels.SetTextAngle(90); p1.cd(); mYlabels.DrawLatex(i, yMax*1.2, "mY={}".format(thismY)); p2.cd()
                else:
                    if ((i-xMin)==0): lastmY = thismY; continue
                    # mYlabels.SetTextAlign(11); mYlabels.SetTextAngle(90); p1.cd(); mYlabels.DrawLatex(i, yMax*1.2, "mY={}".format(thismY)); p2.cd()
                    p1.cd(); mYlabels.SetTextAngle(0); mYlabels.SetTextAlign(21); mYlabels.DrawLatex(i, yMax*1.3, "mY={}".format(thismY)); p2.cd()
            else:
                # if (0<(i-xMin) and (i-xMin)<3 and 2<xMin): lastmY = thismY; continue
                if(massGroup==1 and (i==301)): lastmY = thismY; continue
                if(massGroup==2 and (i==101 or i==203)): lastmY = thismY; continue
                if(massGroup==3 and (i==299)): lastmY = thismY; continue
                if (1<(i-xMin) and i<xMin+5 and divisions>98): p1.cd();rightBox.DrawBox(xMin-0.9,yMax*1.05,xMin+1.5,yMax*1.35); p2.cd()# box at 0
                elif(divisions<99): p1.cd(); rightBox.DrawBox(totalBins-1.3,yMax*1.05,totalBins+0.9,yMax*1.35); p2.cd()# box for last bins set
                if ( (i < xMin+5 and 65<divisions)  or xMax-15 < i  or totalBins-15 < i ):
                    if(65<divisions): mYlabels.SetTextAlign(23);
                    else: mYlabels.SetTextAlign(22);
                    mYlabels.SetTextAngle(90); p1.cd(); mYlabels.DrawLatex(i, yMax*1.2, "mY={}".format(thismY)); p2.cd()
                else: p1.cd(); mYlabels.SetTextAngle(0); mYlabels.SetTextAlign(11); mYlabels.DrawLatex(i, yMax*1.2, "mY={}".format(thismY)); p2.cd()
            lastmY = thismY

    hpullShape.GetXaxis().SetLabelSize(0.06)
    hpullShape.GetXaxis().SetLabelOffset(0.03)
    hDataShape.GetXaxis().SetNdivisions(ticks);
    hBkgShape.GetXaxis().SetNdivisions(ticks);
    hpullShape.GetYaxis().SetTitleFont(13)


    # p1.cd(); rightBox.DrawBox(0.05,0.05,5,0.5); p2.cd();
    p1.cd()
    #### define legend
    leg = TLegend(0.14,0.75,0.60,0.89)
    leg.SetNColumns(2);
    leg.AddEntry(hDataShape, "Data", "l")
    leg.AddEntry(hDataError, "Data unc. (stat.)", "f")
    if(totalFit): leg.AddEntry(hBkgShape, "Sig.+Bkg Fit", "l")
    else: leg.AddEntry(hBkgShape, "Bkg.", "l")
    if ( "prefit" in fittype ): leg.AddEntry(hBkgError, "Bkg. unc. (stat&shape&non-closure&norm)", "e")
    if ( not "fit_s" in fittype ): leg.AddEntry(hSigShape, "Sig. (prefit)", "l")
    else: leg.AddEntry(hSigShape, "Sig. (fit)", "l")
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




    odir = "FitDiagnostics/SHAPES_1D_{0}_updated_localSignfPoints/".format(tag)
    if (not os.path.exists(odir)):
        os.mkdir(odir)
    odir = "{0}{1}/".format(odir,year)
    if (not os.path.exists(odir)):
        os.mkdir(odir)
    odir = "{0}{1}{2}/".format(odir,"massGroup", massGroup)
    if (not os.path.exists(odir)):
        os.mkdir(odir)
    if (totalFit): odir = "{0}{1}/".format(odir,"total")
    else: odir = "{0}{1}/".format(odir,fittype)
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
    return globalMaxVal

# BinRanges = [0,100,200,300,400,500,600,700,800]
# BinRanges = [0,100]
BinRanges = [0,101,201,301,401,501]
# sigs = ["sig_NMSSM_bbbb_MX_400_MY_125"]
# sigs = ["sig_NMSSM_bbbb_MX_650_MY_350", "sig_NMSSM_bbbb_MX_700_MY_400"]
sigs = ["sig_NMSSM_bbbb_MX_400_MY_250", "sig_NMSSM_bbbb_MX_600_MY_125", "sig_NMSSM_bbbb_MX_600_MY_150"]
# tag = "2023Jul5_VR"
# tag = "2023Jul5_SR"
# tag = "2023Dec7_binMYx2_addMX650_10ev_VR"
# globalMaxVal = [0, 0, 0, 0, 0]
tag = "2023Dec7_binMYx2_addMX650_10ev_SR"

ogTag=tag.replace("_VR","")
ogTag=ogTag.replace("_SR","")
locDirTemplate = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}/"
locFileTemplate = "outPlotter_UnrollLocation_massGroup{0}.txt"

years=["2016", "2017", "2018"]
# years=["2016"]
# allfittypes= ["prefit", "fit_b", "fit_s", "prefit"]
allfittypes= ["prefit", "fit_b", "fit_s", "total"]
massMap={}
# setGroup=1
setGroup=0
for year in years:
    locDir=locDirTemplate.format(year, ogTag)
    for i, sig in enumerate(sigs):
        massMap.clear()
        locFile=locDir + locFileTemplate.format(setGroup)
        with open(locFile) as csvfile:
            binMapping = csv.reader(csvfile, delimiter=',')
            for j,mapmX,mapmY in binMapping:
                massMap[int(j)]=(float(mapmX),float(mapmY))
        for k in range(1, len(BinRanges)):
            globalMaxVal=0
            for afittype in allfittypes:
                labels = [afittype, tag, year, setGroup, sig]
                globalMaxVal = makePlot(labels, BinRanges[k-1],BinRanges[k], globalMaxVal, massMap)



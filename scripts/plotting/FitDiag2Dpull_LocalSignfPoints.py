import ROOT
from ROOT import TFile, TH1F, TH2F, TCanvas, gStyle, gPad, gDirectory, TLatex, gROOT, PyConfig, TMath, kBlue, TLine, TPad, TLegend, TGraph, TBox, kThermometer, THStack, TGraphAsymmErrors
from ROOT import kRed
import numpy as np
import re
import os
from VariableDicts import varInfo
import sys
import math
import argparse
import csv

bkgNormPerMassGroupDictionary = {
    "2016" : { "0" : "1.022", "1" :  "1.022", "2" :  "1.018", "3" :  "1.018", "4" :  "1.042", "none" : "1.010"},
    "2017" : { "0" : "1.015", "1" :  "1.015", "2" :  "1.017", "3" :  "1.013", "4" :  "1.019", "none" : "1.010"},
    "2018" : { "0" : "1.046", "1" :  "1.039", "2" :  "1.033", "3" :  "1.024", "4" :  "1.012", "none" : "1.010"},
}

def rootplot_2Dhist(h1, year, odir, tag, descriptionLabel, descriptionLabel2, sig,totalFit,saveName, ofile):
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    gStyle.SetPalette(kThermometer)
    gPad.SetTicks(1,1)
    gPad.SetMargin(0.12,0.16,0.12,0.09) #left,right,bottom,top
    #  p1.SetMargin(0.12,0.05,0.05,0.09) #left,right,bottom,top
    #  p2.SetMargin(0.12,0.05,0.38,0.05) #left,right,bottom,top

    h1.Draw("COLZ1")
    # if(year == "2016"): h1.GetZaxis().SetRangeUser(0., .1)
    # if(year == "2017"): h1.GetZaxis().SetRangeUser(0., .1)
    if("ratio" in tag): h1.GetZaxis().SetRangeUser(0., 2.1)
    # if("pull" in tag): h1.GetZaxis().SetRangeUser(-3.5, 3.5)
    if("pull" in tag): h1.GetZaxis().SetRangeUser(-5., 5.)
    # if("bkg" in tag or "data" in tag or "total" in tag): h1.GetZaxis().SetRangeUser(0.,1500.)
    # if("pull" in descriptionLabel): h1.GetZaxis().SetRangeUser(-8., 8)
    # if("bkg" in tag and args.year == "2016" and int(args.massGroup) <= 1): h1.GetZaxis().SetRangeUser(0., 295.)
    # if("bkg" in tag and args.year == "2016" and int(args.massGroup) == 2): h1.GetZaxis().SetRangeUser(0., 200.)
    # if("bkg" in tag and args.year == "2016" and int(args.massGroup) == 3): h1.GetZaxis().SetRangeUser(0., 190.)
    # if("bkg" in tag and args.year == "2016" and int(args.massGroup) == 4): h1.GetZaxis().SetRangeUser(0., 70.)
    # h1.GetZaxis().SetRangeUser(zmin, zmax)
    if ("pull" in tag): h1.GetZaxis().SetTitle("pull [(data-bkg)/#sigma]")
    else: h1.GetZaxis().SetTitle("Entries/bin/(bin area)")
    h1.GetZaxis().SetTitleOffset(1.3)
    h1.GetXaxis().SetTitle("m_{X} [GeV]")
    h1.GetYaxis().SetTitle("m_{Y} [GeV]")
    CMSlabel = TLatex()
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 30 )
    CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
    plotlabels = TLatex()
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    #  labelText = "mX = %.0f GeV, mY = %.0f GeV"%(mXval,mYval)
    labelText = ""
    if ("VR" in mainTag): labelText = "Validation Region"
    elif ("SR" in mainTag): labelText = "Signal Region"
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    mXval = sig.split("MX_")[1].split("_MY_")[0]
    mYval = sig.split("MX_")[1].split("_MY_")[1]
    plotlabels.DrawLatexNDC(0.2, 0.84,"mX={0},mY={1}".format(mXval, mYval))
    plotlabels.SetTextSize(16)
    plotlabels.SetTextFont(43)
    plotlabels.DrawLatexNDC(0.2, 0.8, "Mass Group {}".format(args.massGroup))
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(16)
    plotlabels.DrawLatexNDC(0.2, 0.76, descriptionLabel)
    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(16)
    plotlabels.DrawLatexNDC(0.2, 0.72, descriptionLabel2)
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    plotlabels.DrawLatexNDC(0.5, 0.93, labelText)
    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(20)
    plotlabels.DrawTextNDC(0.75, 0.93, year)

    fitDir=""
    if("fit_b" in tag):
        fitDir="fit_b"
    if("prefit" in tag):
        fitDir="prefit"
    if("fit_s" in tag):
        fitDir="fit_s"

    odir = "FitDiagnostics/{0}/".format("pulls_updated_localSignfPoints")
    if not os.path.isdir(odir):
        os.mkdir(odir)
    odir = "{0}{1}/".format(odir,mainTag)
    if not os.path.isdir(odir):
        os.mkdir(odir)
    odir = "{0}{1}/".format(odir,sig)
    if not os.path.isdir(odir):
        os.mkdir(odir)
    odir = "{0}{1}/".format(odir,year)
    if not os.path.isdir(odir):
        os.mkdir(odir)
    if (totalFit): odir = "{0}{1}/".format(odir,"total")
    else: odir = "{0}{1}/".format(odir,fitDir)
    if not os.path.isdir(odir):
        os.mkdir(odir)
    # c1.SaveAs("{0}{1}_{2}_{3}.pdf".format(odir, tag, sig, year))
    c1.SaveAs("{0}{1}.pdf".format(odir, saveName))
    # ofile.cd("{0}/{1}".format(sig,year,fitDir))
    # ofile.WriteObject(h1, saveName)
    # c1.SaveAs("FitDiagnostics/pulls/{1}/{0}_{1}.root".format(tag, year))
    # c1.SaveAs("test.pdf")

    del c1
    del h1

def rootplot_3Dhist(h1, year, odir, tag, descriptionLabel, descriptionLabel2, sig,totalFit,saveName, ofile):
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    gStyle.SetPalette(kThermometer)
    gPad.SetTicks(1,1)
    gPad.SetMargin(0.12,0.16,0.12,0.09) #left,right,bottom,top
    #  p1.SetMargin(0.12,0.05,0.05,0.09) #left,right,bottom,top
    #  p2.SetMargin(0.12,0.05,0.38,0.05) #left,right,bottom,top

    h1.Draw("lego2")
    c1.SetTheta(21.18878);
    c1.SetPhi(-49.16531);
    # if(year == "2016"): h1.GetZaxis().SetRangeUser(0., .1)
    # if(year == "2017"): h1.GetZaxis().SetRangeUser(0., .1)
    if("ratio" in tag): h1.GetZaxis().SetRangeUser(0., 2.1)
    # if("pull" in tag): h1.GetZaxis().SetRangeUser(-3.5, 3.5)
    if("pull" in tag): h1.GetZaxis().SetRangeUser(-5., 5.)
    # if("bkg" in tag or "data" in tag or "total" in tag): h1.GetZaxis().SetRangeUser(0.,1500.)
    # if("pull" in descriptionLabel): h1.GetZaxis().SetRangeUser(-8., 8)
    # if("bkg" in tag and args.year == "2016" and int(args.massGroup) <= 1): h1.GetZaxis().SetRangeUser(0., 295.)
    # if("bkg" in tag and args.year == "2016" and int(args.massGroup) == 2): h1.GetZaxis().SetRangeUser(0., 200.)
    # if("bkg" in tag and args.year == "2016" and int(args.massGroup) == 3): h1.GetZaxis().SetRangeUser(0., 190.)
    # if("bkg" in tag and args.year == "2016" and int(args.massGroup) == 4): h1.GetZaxis().SetRangeUser(0., 70.)
    # h1.GetZaxis().SetRangeUser(zmin, zmax)
    if ("pull" in tag): h1.GetZaxis().SetTitle("pull [(data-bkg)/#sigma]")
    else: h1.GetZaxis().SetTitle("Entries/bin/(bin area)")
    h1.GetZaxis().SetTitleOffset(1.5)
    h1.GetXaxis().SetTitle("m_{X} [GeV]")
    h1.GetYaxis().SetTitle("m_{Y} [GeV]")
    h1.GetXaxis().SetTitleOffset(1.5)
    h1.GetYaxis().SetTitleOffset(1.5)
    h1.GetXaxis().SetLabelSize(0.02)
    h1.GetYaxis().SetLabelSize(0.02)
    CMSlabel = TLatex()
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 30 )
    CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
    plotlabels = TLatex()
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    #  labelText = "mX = %.0f GeV, mY = %.0f GeV"%(mXval,mYval)
    labelText = ""
    if ("VR" in mainTag): labelText = "Validation Region"
    elif ("SR" in mainTag): labelText = "Signal Region"
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    mXval = sig.split("MX_")[1].split("_MY_")[0]
    mYval = sig.split("MX_")[1].split("_MY_")[1]
    plotlabels.DrawLatexNDC(0.8, 0.94,"mX={0},mY={1}".format(mXval, mYval))
    plotlabels.SetTextSize(16)
    plotlabels.SetTextFont(43)
    plotlabels.DrawLatexNDC(0.8, 0.9, "Mass Group {}".format(args.massGroup))
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(16)
    plotlabels.DrawLatexNDC(0.8, 0.86, descriptionLabel)
    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(16)
    plotlabels.DrawLatexNDC(0.8, 0.82, descriptionLabel2)
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    plotlabels.DrawLatexNDC(0.46, 0.93, labelText)
    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(20)
    plotlabels.DrawTextNDC(0.65, 0.93, year)

    fitDir=""
    if("fit_b" in tag):
        fitDir="fit_b"
    if("prefit" in tag):
        fitDir="prefit"
    if("fit_s" in tag):
        fitDir="fit_s"

    odir = "FitDiagnostics/{0}/".format("pulls_updated_localSignfPoints")
    if not os.path.isdir(odir):
        os.mkdir(odir)
    odir = "{0}{1}/".format(odir,mainTag)
    if not os.path.isdir(odir):
        os.mkdir(odir)
    odir = "{0}{1}/".format(odir,sig)
    if not os.path.isdir(odir):
        os.mkdir(odir)
    odir = "{0}{1}/".format(odir,year)
    if not os.path.isdir(odir):
        os.mkdir(odir)
    if (totalFit): odir = "{0}{1}/".format(odir,"total")
    else: odir = "{0}{1}/".format(odir,fitDir)
    if not os.path.isdir(odir):
        os.mkdir(odir)
    odir = "{0}{1}/".format(odir,"3D")
    if not os.path.isdir(odir):
        os.mkdir(odir)
    # c1.SaveAs("{0}{1}_{2}_{3}.pdf".format(odir, tag, sig, year))
    c1.SaveAs("{0}{1}_3D.pdf".format(odir, saveName))
    # ofile.cd("{0}/{1}".format(sig,year,fitDir))
    # ofile.WriteObject(h1, saveName)
    # c1.SaveAs("FitDiagnostics/pulls/{1}/{0}_{1}.root".format(tag, year))
    # c1.SaveAs("test.pdf")

    del c1
    del h1

def rootplot_1Dhist(h1, year, odir, tag, descriptionLabel,  sig,totalFit,saveName, ofile):
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title
    gPad.SetTicks(1,1)
    gPad.SetMargin(0.12,0.09,0.12,0.09) #left,right,bottom,top

    h1.Draw("hist")
    h1.GetXaxis().SetTitle("pull [(data-bkg)/#sigma]")
    # h1.GetXaxis().SetRangeUser(-3., 3.)
    h1.GetXaxis().SetRangeUser(-5., 5.)
    h1.GetYaxis().SetRangeUser(0., 40.)
    h1.GetYaxis().SetTitle("Entries/bin/(bin area)")
    CMSlabel = TLatex()
    CMSlabel.SetTextFont(63)
    CMSlabel.SetTextSize( 30 )
    CMSlabel.DrawLatexNDC(0.12, 0.93, "CMS #scale[0.8]{#it{#bf{Work In Progress}}}")
    plotlabels = TLatex()
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    #  labelText = "mX = %.0f GeV, mY = %.0f GeV"%(mXval,mYval)
    labelText = ""
    if ("VR" in mainTag): labelText = "Validation Region"
    elif ("SR" in mainTag): labelText = "Signal Region"
    # else:    labelText = labelText + "Signal Region"
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    mXval = sig.split("MX_")[1].split("_MY_")[0]
    mYval = sig.split("MX_")[1].split("_MY_")[1]
    plotlabels.DrawLatexNDC(0.2, 0.84,"mX={0},mY={1}".format(mXval, mYval))
    plotlabels.SetTextFont(43)
    plotlabels.SetTextSize(16)
    plotlabels.DrawLatexNDC(0.2, 0.8, "Mass Group {}".format(args.massGroup))
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(16)
    plotlabels.DrawLatexNDC(0.2, 0.76, descriptionLabel)

    plotlabels.SetTextFont(43)
    plotlabels.SetTextSize(14)
    plotlabels.DrawTextNDC(0.2, 0.72, "Mean: {:0.4f}".format(h1.GetMean()))
    plotlabels.DrawTextNDC(0.2, 0.68, "Std. Dev.: {:.4f}".format(h1.GetStdDev()))
    plotlabels.SetTextFont(63)
    plotlabels.SetTextSize(20)
    plotlabels.DrawLatexNDC(0.5, 0.93, labelText)
    plotlabels.SetTextFont(53)
    plotlabels.SetTextSize(20)
    plotlabels.DrawTextNDC(0.75, 0.93, year)

    fitDir=""
    if("fit_b" in tag):
        fitDir="fit_b"
    if("prefit" in tag):
        fitDir="prefit"
    if("fit_s" in tag):
        fitDir="fit_s"

    # odir = "FitDiagnostics/{0}/".format("pulls_updated")
    odir = "FitDiagnostics/{0}/".format("pulls_updated_localSignfPoints")
    # cd = ofile.mkdir("{0}".format("FitDiagnostics"))
    if not os.path.isdir(odir):
        os.mkdir(odir)
    # cd = ofile.mkdir("{0}".format(odir))
    odir = "{0}{1}/".format(odir,mainTag)
    if not os.path.isdir(odir):
        os.mkdir(odir)
    # cd = ofile.mkdir("{0}".format(odir))
    odir = "{0}{1}/".format(odir,sig)
    if not os.path.isdir(odir):
        os.mkdir(odir)
    # cd = ofile.mkdir("{0}".format(odir))
    odir = "{0}{1}/".format(odir,year)
    if not os.path.isdir(odir):
        os.mkdir(odir)
    # cd = ofile.mkdir("{0}".format(odir))
    if (totalFit): odir = "{0}{1}/".format(odir,"total")
    else: odir = "{0}{1}/".format(odir,fitDir)
    if not os.path.isdir(odir):
        os.mkdir(odir)
    # cd = ofile.mkdir("{0}".format(odir))
    # c1.SaveAs("{0}{1}_{2}_{3}.pdf".format(odir,tag, sig, year))
    c1.SaveAs("{0}{1}.pdf".format(odir,saveName))
    # ofile.cd("{0}".format(odir))
    # ofile.WriteObject(h1, saveName)
    # ofile.cd("")
    # c1.SaveAs("FitDiagnostics/pulls/{1}/{0}_{1}.root".format(tag, year))
    # c1.SaveAs("test.pdf")

    del c1
    del h1


def makePlotsPerYear(year, pvalFile, labels, inputFile, ofile):
    fittype=labels[0]
    totalFit=False
    if ("total" in fittype):
        totalFit=True
        fittype="fit_s"
    print(fittype)
    tag = labels[1]
    year = labels[2]
    # sig = "sig_NMSSM_bbbb_MX_1200_MY_300"
    massGroup = labels[3]
    sig = labels[4]

    fName = "FitDiagnostics/{0}/{1}/FitDiagnostics_{1}_{2}_id0_sig0.root".format(tag, year, sig)
    print(fName)
    fFit = ROOT.TFile(fName)

    fFit.cd("shapes_{0}/selectionbJets_SignalRegion".format(fittype));
    grDataShape = fFit.Get("shapes_{0}/selectionbJets_SignalRegion/data".format(fittype))
    hBkgShape = fFit.Get("shapes_{0}/selectionbJets_SignalRegion/data_BTagCSV_dataDriven_kinFit".format(fittype))
    hSigShape = fFit.Get("shapes_{0}/selectionbJets_SignalRegion/{1}".format(fittype,sig))
    if(totalFit): hBkgShape = fFit.Get("shapes_{0}/selectionbJets_SignalRegion/total".format(fittype))

    h2dVR_pull = ROOT.TH2D( "h2dVR_pull", "HistVR_pull ", nbins_mX, MXbins, nbins_mY, MYbins );
    h2dVR_data = ROOT.TH2D( "h2dVR_data", "HistVR_data ", nbins_mX, MXbins, nbins_mY, MYbins );
    h2dVR_bkg  = ROOT.TH2D( "h2dVR_bkg", "HistVR_bkg ", nbins_mX, MXbins, nbins_mY, MYbins );
    h2dVR_dataShape = ROOT.TH2D( "h2dVR_dataShape", "HistVR_dataShape ", nbins_mX, MXbins, nbins_mY, MYbins );
    h2dVR_sigShape = ROOT.TH2D( "h2dVR_sigShape", "HistVR_sigShape ", nbins_mX, MXbins, nbins_mY, MYbins );
    h2dVR_bkgShape  = ROOT.TH2D( "h2dVR_bkgShape", "HistVR_bkgShape ", nbins_mX, MXbins, nbins_mY, MYbins );
    h2dVR_ratioShape  = ROOT.TH2D( "h2dVR_ratioShape", "HistVR_ratioShape ", nbins_mX, MXbins, nbins_mY, MYbins );
    h2dVR_pullShape  = ROOT.TH2D( "h2dVR_pullShape", "HistVR_pullShape ", nbins_mX, MXbins, nbins_mY, MYbins );

    inCombine = ROOT.TFile(inputFile)
    inCombine.cd("data_BTagCSV/selectionbJets_SignalRegion");
    hdataIN = inCombine.Get("data_BTagCSV/selectionbJets_SignalRegion/data_BTagCSV_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled");
    inCombine.cd("data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion");
    hbkgIN = inCombine.Get("data_BTagCSV_dataDriven_kinFit/selectionbJets_SignalRegion/data_BTagCSV_dataDriven_kinFit_selectionbJets_SignalRegion_HH_kinFit_m_H2_m_Rebinned_Unrolled");
    h2dVR_INdata = ROOT.TH2D( "h2dVR_INdata", "HistVR_INdata ", nbins_mX, MXbins, nbins_mY, MYbins );
    h2dVR_INbkg = ROOT.TH2D( "h2dVR_INbkg", "HistVR_INbkg ", nbins_mX, MXbins, nbins_mY, MYbins );
    h2dVR_INratio = ROOT.TH2D( "h2dVR_INratio", "HistVR_INratio ", nbins_mX, MXbins, nbins_mY, MYbins );
    # hpullDistribution = ROOT.TH1D( "hpull", "hpull", 50, -2.8, 2.8);
    # hpullDistribution = ROOT.TH1D( "hpull", "hpull", 64, -3.6, 3.6);
    hpullDistribution = ROOT.TH1D( "hpull", "hpull", 90, -5., 5.);

    inputHistsFileName = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}/outPlotter_massGroup{2}.root".format(year, tag, args.massGroup)
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

    pullVal = ROOT.Double(0)
    dataVal = ROOT.Double(0)
    bkgVal = ROOT.Double(0)
    pull_bin_middle = ROOT.Double(0)
    with open(ifile) as csvfile:
        binMapping = csv.reader(csvfile, delimiter=',')
        for j,mapmX,mapmY in binMapping:
            i=int(j)
            dataValIN = hdataIN.GetBinContent(int(i))
            bkgValIN = hbkgIN.GetBinContent(int(i))
            dataShapeVal = grDataShape.Eval(float(i)-0.5)
            errDataShape = grDataShape.GetErrorY(int(i)-1)
            bkgShapeVal = hBkgShape.GetBinContent(int(i))
            sigShapeVal = hSigShape.GetBinContent(int(i))
            if ("fit_" in fittype):
                pull = (dataShapeVal-bkgShapeVal)/math.sqrt(errDataShape**2)
            elif ("prefit" in fittype):
                errBkgShape = hBkgShape.GetBinError(i)
                shapeErr=hShapeUp.GetBinContent(i)-hBkgShape.GetBinContent(i)
                normErr=bkgShapeVal * ( float(bkgNormPerMassGroupDictionary[str(year)][str(args.massGroup)]) - 1 )
                pull = (dataShapeVal-bkgShapeVal)/math.sqrt(errDataShape**2+ errBkgShape**2 +shapeErr**2+normErr**2)
            else:
                print("fit type is not defined")
                sys.exit()


            if ("VR" in tag):
                if (125-20<float(mapmY) and float(mapmY)<125+20): pull = -1000
            # h2dVR_pull.Fill(float(mapmX),float(mapmY), pullVal)
            # h2dVR_data.Fill(float(mapmX),float(mapmY), dataVal)
            # h2dVR_bkg.Fill(float(mapmX),float(mapmY), bkgVal)
            h2dVR_INdata.Fill(float(mapmX),float(mapmY), dataValIN)
            h2dVR_INbkg.Fill(float(mapmX),float(mapmY), bkgValIN)
            h2dVR_INratio.Fill(float(mapmX),float(mapmY), dataValIN/bkgValIN)

            h2dVR_dataShape.Fill(float(mapmX),float(mapmY), dataShapeVal)
            h2dVR_bkgShape.Fill(float(mapmX),float(mapmY), bkgShapeVal)
            h2dVR_sigShape.Fill(float(mapmX),float(mapmY), sigShapeVal)
            h2dVR_pullShape.Fill(float(mapmX),float(mapmY), pull)
            if (pull>-500): hpullDistribution.Fill(pull)

    # divide by bin areas for data and background
    for binx in range(1,h2dVR_bkgShape.GetNbinsX()):
        for biny in range(1,h2dVR_bkgShape.GetNbinsY()):
            h2dVR_bkgShape.SetBinContent(binx,biny,
                                         h2dVR_bkgShape.GetBinContent(binx,biny)
                                         /(h2dVR_bkgShape.GetYaxis().GetBinWidth(biny)
                                           *h2dVR_bkgShape.GetXaxis().GetBinWidth(binx)
                                           )
                                         )
    for binx in range(1,h2dVR_dataShape.GetNbinsX()):
        for biny in range(1,h2dVR_dataShape.GetNbinsY()):
            h2dVR_dataShape.SetBinContent(binx,biny,
                                         h2dVR_dataShape.GetBinContent(binx,biny)
                                         /(h2dVR_dataShape.GetYaxis().GetBinWidth(biny)
                                           *h2dVR_dataShape.GetXaxis().GetBinWidth(binx)
                                           )
                                         )

    for binx in range(1,h2dVR_sigShape.GetNbinsX()):
        for biny in range(1,h2dVR_sigShape.GetNbinsY()):
            h2dVR_sigShape.SetBinContent(binx,biny,
                                         h2dVR_sigShape.GetBinContent(binx,biny)
                                         /(h2dVR_sigShape.GetYaxis().GetBinWidth(biny)
                                           *h2dVR_sigShape.GetXaxis().GetBinWidth(binx)
                                           )
                                         )

    # rootplot_2Dhist(h2dVR_INdata, year, iodir, tag + "_dataIN_massGroup" + args.massGroup, "Input Hist Data", sig)
    # rootplot_2Dhist(h2dVR_INbkg, year, iodir, tag + "_bkgIN_massGroup" + args.massGroup, "Input Hist Bkg", sig)
    # rootplot_2Dhist(h2dVR_INratio, year, iodir, tag + "_ratioIN_massGroup" + args.massGroup, "Input Hists Ratio", sig)
    if ("prefit" in fittype): fittypeLabel = "Pre-fit"
    elif ("fit_b" in fittype): fittypeLabel = "Bkg. Only Fit"
    elif ("fit_s" in fittype):
        if(totalFit): fittypeLabel = "Sig.+Bkg. Fit"
        else: fittypeLabel = "Bkg. of S+B  Fit"

    rootplot_2Dhist(h2dVR_dataShape,
                    year,
                    iodir,
                    tag + "_dataShape_massGroup" + args.massGroup+"_{0}".format(fittype),
                    "{0}".format(fittypeLabel),
                    "Data distribution",
                    sig,
                    totalFit,
                    "aData",
                    ofile
                    )
    rootplot_2Dhist(h2dVR_sigShape,
                    year,
                    iodir,
                    tag + "_sigShape_massGroup" + args.massGroup+"_{0}".format(fittype),
                    "{0}".format(fittypeLabel),
                    "Sig. distribution",
                    sig,
                    totalFit,
                    "cSignal",
                    ofile
                    )
    if(totalFit): rootplot_2Dhist(h2dVR_bkgShape,
                                  year,
                                  iodir,
                                  tag + "_totalFit_massGroup" + args.massGroup+"_{0}".format(fittype),
                                  "{0}".format(fittypeLabel),
                                  "Bkg+Fit distribution",
                                  sig,
                                  totalFit,
                                  "bBkgAndSignal",
                                  ofile
                                  )
    else: rootplot_2Dhist(h2dVR_bkgShape,
                          year,
                          iodir,
                          tag + "_bkgShape_massGroup" + args.massGroup+"_{0}".format(fittype),
                          "{0}".format(fittypeLabel),
                          "Bkg Distribution",
                          sig,
                          totalFit,
                          "bBkg",
                          ofile
                          )
    rootplot_2Dhist(h2dVR_pullShape,
                    year,
                    iodir,
                    tag + "_pullShape_massGroup" + args.massGroup+"_{0}".format(fittype),
                    fittypeLabel,
                    "",
                    sig,
                    totalFit,
                    "dPull",
                    ofile
                    )
    # 3D

    rootplot_3Dhist(h2dVR_dataShape,
                    year,
                    iodir,
                    tag + "_dataShape_massGroup" + args.massGroup+"_{0}".format(fittype),
                    "{0}".format(fittypeLabel),
                    "Data distribution",
                    sig,
                    totalFit,
                    "aData",
                    ofile
                    )
    rootplot_3Dhist(h2dVR_sigShape,
                    year,
                    iodir,
                    tag + "_sigShape_massGroup" + args.massGroup+"_{0}".format(fittype),
                    "{0}".format(fittypeLabel),
                    "Sig. distribution",
                    sig,
                    totalFit,
                    "cSignal",
                    ofile
                    )
    if(totalFit): rootplot_3Dhist(h2dVR_bkgShape,
                                  year,
                                  iodir,
                                  tag + "_totalFit_massGroup" + args.massGroup+"_{0}".format(fittype),
                                  "{0}".format(fittypeLabel),
                                  "Bkg+Fit distribution",
                                  sig,
                                  totalFit,
                                  "bBkgAndSignal",
                                  ofile
                                  )
    else: rootplot_3Dhist(h2dVR_bkgShape,
                          year,
                          iodir,
                          tag + "_bkgShape_massGroup" + args.massGroup+"_{0}".format(fittype),
                          "{0}".format(fittypeLabel),
                          "Bkg Distribution",
                          sig,
                          totalFit,
                          "bBkg",
                          ofile
                          )
    rootplot_3Dhist(h2dVR_pullShape,
                    year,
                    iodir,
                    tag + "_pullShape_massGroup" + args.massGroup+"_{0}".format(fittype),
                    fittypeLabel,
                    "",
                    sig,
                    totalFit,
                    "dPull",
                    ofile
                    )
    rootplot_1Dhist(hpullDistribution,
                    year,
                    iodir,
                    tag + "_pullDist_massGroup" + args.massGroup+"_{0}".format(fittype),
                    fittypeLabel,
                    sig,
                    totalFit,
                    "fPull1D",
                    ofile
                    )
    del h2dVR_INbkg
    del h2dVR_INdata
    del h2dVR_INratio
    del h2dVR_dataShape
    del h2dVR_sigShape
    del h2dVR_bkgShape
    del h2dVR_pullShape

##################################################
gROOT.SetBatch(True)
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--tag'   ,  dest = 'tag'    ,  help = 'production tag'  ,  default = ""  ,  required = True  )
parser.add_argument('--algo'  ,  dest = 'algo'   ,  help = 'production tag'  ,  default = ""  ,  required = False  )
parser.add_argument('--year'  ,  dest = 'year'   ,  help = 'production tag'  ,  default = ""  ,  required = True  )
parser.add_argument('--group'  ,  dest = 'massGroup'   ,  help = 'production tag'  ,  default = ""  ,  required = True  )
parser.add_argument('--zoom'  ,  dest = 'zoom'   ,  help = 'production tag'  ,  default = ""  ,  required = False )

args = parser.parse_args()
# MXbins = np.diff(signalsMX)
# bins
# nbins_mY=69
# nbins_mX=36
nbins_mY=35
nbins_mX=33

## from fillhists after mYx2, before unrolling...
# HH_kinFit_m:H2_m@H2_m     = 36, 51, 62, 70, 78, 86, 94, 102, 110, 122, 140, 156, 172, 188, 204, 228, 260, 292, 324, 356, 388, 444, 508, 572, 636, 700, 764, 892, 1020, 1148, 1276, 1404, 1564, 1820, 2076, 2204
# HH_kinFit_m:H2_m@HH_kinFit_m     = 212, 228, 244, 260, 276, 292, 308, 324, 340, 360, 392, 424, 456, 488, 520, 552, 584, 616, 648, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216, 1296, 1424, 1552, 1680, 1808, 1936, 2064, 2192, 2320

MYbins     = np.array([36, 51, 62, 70, 78, 86, 94, 102, 110, 122, 140, 156, 172, 188, 204, 228, 260, 292, 324, 356, 388, 444, 508, 572, 636, 700, 764, 892, 1020, 1148, 1276, 1404, 1564, 1820, 2076, 2204], dtype='float64')
MXbins     = np.array([212, 228, 244, 260, 276, 292, 308, 324, 340, 360, 392, 424, 456, 488, 520, 552, 584, 616, 648, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216, 1296, 1424, 1552, 1680, 1808, 1936], dtype='float64')
# MYbins = np.array([36, 45, 51, 57, 62, 66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 122, 132, 140, 148, 156, 164, 172, 180, 188, 196, 204, 212, 228, 244, 260, 276, 292, 308, 324, 340, 356, 372, 388, 412, 444, 476, 508, 540, 572, 604, 636, 668, 700, 732, 764, 828, 892, 956, 1020, 1084, 1148, 1212, 1276, 1340, 1404, 1468, 1564, 1692, 1820, 1948, 2076, 2204], dtype='float64')
# MXbins = np.array([212, 228, 244, 260, 276, 292, 308, 324, 340, 360, 392, 424, 456, 488, 520, 552, 584, 616, 648, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216, 1296, 1424, 1552, 1680, 1808, 1936, 2064, 2192, 2320], dtype='float64')

# zmin = 0.
# zmax=1.0
tag=args.tag
# for the save dir
mainTag=args.tag
ogTag=tag.replace("_VR","")
ogTag=ogTag.replace("_SR","")
print(ogTag)
print(tag)

# inputFile = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_2023Jul5_loc_VR/outPlotter_massGroup{1}.root".format(args.year, args.massGroup)
inputFile = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}/outPlotter_massGroup{2}.root".format(args.year, tag, args.massGroup)
# ofile = ROOT.TFile.Open("singleMassPoints_{0}_{1}.root".format(tag, args.year), "RECREATE")
ofile = ""

# iodir = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_2023Jul5_loc/".format(args.year)
iodir = "/uscms/homes/a/agrummer/nobackup/DiHiggs_v2/CMSSW_10_2_5/src/bbbbAnalysis/VarPlots/rootHists/fullSubmission_2022Nov/{0}DataPlots_{1}/".format(args.year, ogTag)
ifile = iodir + "outPlotter_UnrollLocation_massGroup{0}.txt".format(args.massGroup)

sigs = ["sig_NMSSM_bbbb_MX_650_MY_350", "sig_NMSSM_bbbb_MX_700_MY_400"]
# sig= "sig_NMSSM_bbbb_MX_400_MY_125"
# # labels = ["prefit", "2016", "Mass Group 0", sig]
# tag = "2023Jul5_VR"
# # tag = "2023Jul5_SR"
# years=["2016", "2017", "2018"]
# allfittypes= ["fit_b", "fit_s", "prefit"]
# for afittype in allfittypes:
#     for year in years:
#         for i, sig in enumerate(sigs):
#             labels = [afittype, tag, year, "Mass Group {}".format(i), sig]
#             makePlot(labels)
for sig in sigs:
    labels = ["fit_b", tag, args.year, "Mass Group {}".format(args.massGroup), sig]
    makePlotsPerYear("{}".format(args.year), ifile, labels, inputFile, ofile)
    labels = ["prefit", tag, args.year, "Mass Group {}".format(args.massGroup), sig]
    makePlotsPerYear("{}".format(args.year), ifile, labels, inputFile, ofile)
    labels = ["fit_s", tag, args.year, "Mass Group {}".format(args.massGroup), sig]
    makePlotsPerYear("{}".format(args.year), ifile, labels, inputFile, ofile)
    labels = ["total", tag, args.year, "Mass Group {}".format(args.massGroup), sig]
    makePlotsPerYear("{}".format(args.year), ifile, labels, inputFile, ofile)


import numpy 
from ROOT import TFile, TH1F, TCanvas, gROOT, kTRUE, gPad, TLegend, gStyle, kRed, kBlue,TPad, TLatex, TLine, TH2F
import os
import matplotlib
import root_numpy
import pandas
import glob
from root_numpy import root2array
from matplotlib import pyplot as plt
from numpy.lib.recfunctions import stack_arrays
from hep_ml.metrics_utils import ks_2samp_weighted
from scipy import stats
from VariableDicts import varInfo
gROOT.SetBatch(kTRUE)

def Draw1DHistosComparison(original, target, variables, original_weights, norm, outputDirectory, tag):
    #Create folder for plots
    #Normalize or not?
    if norm is True:
      hist_settings = {'bins': 100, 'density': True, 'alpha': 0.5}
    else:
      hist_settings = {'bins': 100, 'density': None, 'alpha': 0.5}
    #Create figure on matplotlib
    matplotlib.rcParams.update({'font.size': 35})
    plt.figure(figsize=[80, 60], dpi=50)
    for id, column in enumerate(variables, 1):
        xlim = numpy.percentile(numpy.hstack([target[column]]), [0.01, 99.99])
        plt.subplot(4, 4, id)
        plt.hist(original[column],label='Bkg. Model', weights=original_weights, range=xlim, **hist_settings)
        plt.hist(target[column],  label='4 btag (Target)', range=xlim, **hist_settings)
        plt.legend(loc='best')
        plt.title(column,fontsize=40)
    plt.savefig("%s/distibutions_%s.png"%(outputDirectory,tag))
    plt.close('all')

def DrawDNNScoreComparison(yhat,y, norm, tag):
    #Normalize or not?
    if norm is True:
      hist_settings = {'bins': 20, 'density': True, 'alpha': 0.5}
    else:
      hist_settings = {'bins': 20, 'density': None, 'alpha': 0.5}
    #Create dataframes
    datayhat= numpy.array(yhat)
    datay= numpy.array(y)
    datatrain= pandas.DataFrame({'DNN':datayhat[:,0]})
    datatrain['Class'] = pandas.DataFrame(datay)  
    datatrain_signal=datatrain[datatrain.Class==1]
    datatrain_background=datatrain[datatrain.Class==0]
    #Create figure on matplotlib
    fig, (ax1, ax2) = plt.subplots(nrows=2)

    matplotlib.rcParams.update({'font.size': 20})
    plt.figure(figsize=(7,7))
    xlim = numpy.percentile(numpy.hstack(datatrain_signal['DNN']), [0.01, 99.99])
    plt.hist(datatrain_signal['DNN'],label='Signal',  range=xlim, **hist_settings)
    plt.hist(datatrain_background['DNN'],  label='Background', range=xlim, **hist_settings)
    plt.legend(loc='best')
    plt.title('DNN output (%s)'%tag,fontsize=20) 
    plt.savefig("myplots/nndistibutions_%s.png"%tag)    

def DrawDNNScore(yhat,y, norm, tag):
    #Normalize or not?
    if norm is True:
      hist_settings = {'bins': 10, 'density': True, 'alpha': 0.5}
    else:
      hist_settings = {'bins': 10, 'density': None, 'alpha': 0.5}
    #Create dataframes
    datayhat= numpy.array(yhat)
    datay= numpy.array(y)
    datatrain= pandas.DataFrame({'DNN':datayhat[:,0]})
    datatrain['Class'] = pandas.DataFrame(datay)  
    datatrain_signal=datatrain[datatrain.Class==1]
    datatrain_background=datatrain[datatrain.Class==0]
    #Create figure on matplotlib
    matplotlib.rcParams.update({'font.size': 20})
    plt.figure(figsize=(7,7))
    xlim = numpy.percentile(numpy.hstack(datatrain_signal['DNN']), [0.01, 99.99])
    plt.hist(datatrain_signal['DNN'],label='Signal',  range=xlim, **hist_settings)
    plt.hist(datatrain_background['DNN'],  label='Background', range=xlim, **hist_settings)
    plt.legend(loc='best')
    plt.title('DNN output (%s)'%tag,fontsize=20) 
    plt.savefig("myplots/nndistibution_%s.png"%tag) 


def CreateDataFrameForPlot(scores,labels):
    datayhat= numpy.array(scores)
    datay= numpy.array(labels)
    data= pandas.DataFrame({'DNN':datayhat[:,0]})
    data['Class'] = pandas.DataFrame(datay)  
    data_signal=data[data.Class==1]
    data_background=data[data.Class==0]
    return data_signal,data_background

def DrawDNNScoreComparison(yhat_train,y_train,yhat_test,y_test, norm, tag):
    #Create dataframes for train and test 
    datatrain_signal,datatrain_background = CreateDataFrameForPlot(yhat_train,y_train)
    datatest_signal,datatest_background   = CreateDataFrameForPlot(yhat_test,y_test)
    #Format
    dnnbin = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]
    ratiobin = [0.025,0.075,0.125,0.175,0.225,0.275,0.325,0.375,0.425,0.475,0.525,0.575,0.625,0.675,0.725,0.775,0.825,0.875,0.925,0.975]
    #KS TEST
    sig_d,sig_p = ks_2samp(datatrain_signal['DNN'], datatest_signal['DNN'])
    bkg_d,bkg_p =ks_2samp(datatrain_background['DNN'], datatest_background['DNN'])
    #Create figure on matplotlib
    matplotlib.rcParams.update({'font.size': 15})
    fig = plt.figure(1, figsize=(15, 15))
    ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)
    ax2 = plt.subplot2grid((3, 1), (2, 0))
    plot1 = ax1.hist(datatrain_signal['DNN'],label='Signal(fitmodel)', range=[0,1], color='blue',  bins=dnnbin, density=True, alpha=0.5)
    plot2 = ax1.hist(datatest_signal['DNN'] ,label='Signal(test)' , range=[0,1], color='darkblue', linewidth=2, histtype="step", bins=dnnbin, density=True, alpha=0.4)
    plot3 = ax1.hist(datatrain_background['DNN'],label='Background(fitmodel)', range=[0,1], color='red',  bins=dnnbin, density=True, alpha=0.5)
    plot4 = ax1.hist(datatest_background['DNN'] ,label='Background(test)' , range=[0,1], color='darkred', linewidth=2, histtype="step", bins=dnnbin, density=True, alpha=0.4)
    plot5 = ax1.text(0.35, 0.01,'P(KS-test) sig(bkg) = %.2f(%.2f)'%(sig_p,bkg_p),fontsize=10)
    ax1.set_ylabel("A. U.",fontsize=15)
    ax1.set_title('DNN output (%s)'%tag,fontsize=15) 
    ax1.legend(loc='upper center')
    plots5 = ax2.bar(ratiobin, height=( (plot2[0]-plot1[0])/plot1[0]), alpha=0.4, edgecolor='darkblue', linewidth=1.5, color='blue',width = 0.05)
    plots6 = ax2.bar(ratiobin, height=( (plot4[0]-plot3[0])/plot3[0]), alpha=0.4, edgecolor='darkred', linewidth=1.5, color='red',width = 0.05)
    ax2.set_ylim([-0.5, 0.5])
    ax2.axhline(y=0,ls='--',c='k',zorder=11,lw=1) 
    ax2.axhline(y=0.2,ls='--',c='k',zorder=11,lw=1) 
    ax2.axhline(y=-0.2,ls='--',c='k',zorder=11,lw=1) 
    ax2.set_ylabel('(Test-fitmodel)/fitmodel',fontsize=15)
    ax2.set_xlabel("DNN",fontsize=20)
    plt.savefig("myplots/nndistibutioncomparison_%s.png"%tag) 


def Draw2DHisto(data,var1,var2,x1,x2,y1,y2,tag):
    plt.figure(figsize=(10,10)) # square canvas
    _ = plt.hist2d(data['%s'%var1], data['%s'%var2], range=[[x1, x2], [y1, y2]], bins=100, cmap='viridis', norm=LogNorm())
    plt.xlabel("%s"%var1, fontsize=20) 
    plt.ylabel("%s"%var2, fontsize=20)
    plt.title("%s"%tag,fontsize=20)
    _ = plt.colorbar() 
    plt.savefig("myplots/mh1mh2plane_%s.png"%tag) 

def rootplot_2samp_ratio(original, target, variables, weights, outputDirectory, tag):
    ofileName = "%s/histograms.root"%(outputDirectory)
    ofile = TFile.Open ( ofileName, "UPDATE")
    for var in variables:
        #### define the histograms
        h1 = TH1F( var+"_model_"+tag, var+"_model_"+tag, varInfo[var]['bins'], varInfo[var]['xlow'], varInfo[var]['xhigh'])
        h2 = TH1F( var+"_target", var+"_target", varInfo[var]['bins'], varInfo[var]['xlow'], varInfo[var]['xhigh'])
        for i, val in enumerate(original[var]):
            h1.Fill(val, weights[i])
        for val2 in target[var]:
            h2.Fill(val2, 1.)
        # h1.Sumw2()
        h2.Sumw2()
        h1.Scale(1./h1.Integral())
        h2.Scale(1./h2.Integral())
        #### define the canvas
        c1 = TCanvas('c1', 'c1',800,600)
        gStyle.SetOptStat(0) # remove the stats box
        gStyle.SetOptTitle(0) # remove the title
        
        #### define the upper and lower pads
        p1 = TPad("p1", "p1", 0., 0.3, 1., 1.0, 0, 0, 0)
        p1.SetMargin(0.12,0.05,0.05,0.05) #left,right,bottom,top
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
        h1.GetXaxis().SetRangeUser(varInfo[var]['xlowRange'],varInfo[var]['xhighRange'])
        h1.GetXaxis().SetLabelSize(0.)
        #yaxis
        h1.GetYaxis().SetTitle(varInfo[var]['YaxisTitle'])
        h1.GetYaxis().SetLabelSize(0.05)
        h1.GetYaxis().SetTitleSize(0.05)
        h1.GetYaxis().SetTitleOffset(1.1)
        h1.GetYaxis().SetTickLength(0.02)
        if h2.GetMaximum()>h1.GetMaximum():
            h1.GetYaxis().SetRangeUser(0,h2.GetMaximum()*1.1)
        
        ### KStest and AD test
        ksval = "KS Test = %.4f"%h1.KolmogorovTest(h2)
        # print("KS test, UO %e"%h1.KolmogorovTest(h2, "UO"))
        ksvalMaxDist= "KS Test, Max Dist. = %.4f"%h1.KolmogorovTest(h2, "M")
        # print("KS test, normalized %e"%h1.KolmogorovTest(h2, "N"))
        ksvalX = "KS Test, pseudoX = %.4f"%h1.KolmogorovTest(h2, "X")
        # print("AD test %e"%h1.AndersonDarlingTest(h2))
        # print("AD test, normalized %e"%h1.AndersonDarlingTest(h2, "T"))
        CMSlabel = TLatex()
        CMSlabel.SetTextSize( 0.08 )
        CMSlabel.DrawTextNDC(0.7, 0.85, "CMS Internal")

        KSlabel = TLatex()
        KSlabel.SetTextFont( 42 )
        KSlabel.SetTextSize( 0.03 )
        KSlabel.DrawTextNDC(0.72, 0.7, ksval)
        KSlabel.DrawTextNDC(0.72, 0.66, ksvalMaxDist)
        KSlabel.DrawTextNDC(0.72, 0.62, ksvalX)
        #### define legend
        leg = TLegend(0.7,0.74,0.95,0.84)
        leg.AddEntry(h1, "3b data (bkg. model)", "l")
        leg.AddEntry(h2, "4b data (target)", "l")
        leg.SetBorderSize(0) # remove the border
        leg.SetLineColor(0)
        leg.SetFillColor(0)
        leg.SetTextSize(0.035)
        leg.SetFillStyle(0) # make the legend background transparent
        leg.Draw()
        
        #### draw the ratio hist in lower pad
        p2.cd()
        h3 = h1.Clone("h3")
        h3.Divide(h2)
        h3.SetMarkerStyle(20) # marker style (20 = filled circle) that can be resized
        h3.SetMarkerSize(0.7)
        h3.SetMarkerColor(1)
        h3.SetLineColor(1)
        h3.Draw("p") # draw as data points
        LineAtOne = TLine(varInfo[var]['xlowRange'],1.,varInfo[var]['xhighRange'],1.) #x1,y1,x2,y2
        LineAtOne.SetLineWidth(2)
        LineAtOne.SetLineStyle(9)
        LineAtOne.Draw()
        h3.GetYaxis().SetRangeUser(0.,2.)
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
        h3.GetYaxis().SetTitle("model / target")

        #### save the histograms and pdf
        h1.Write()
        if (tag is not "weights"): h2.Write()
        # c1.SaveAs("%s/distibutions_%s_%s.png"%(outputDirectory,var,tag))
        c1.SaveAs("%s/distibutions_%s_%s.pdf"%(outputDirectory,var,tag))
        del c1, h1, h2
    ofile.Close()

def rootplot_2Dhist(original, target, weights, var1, var2, outputDirectory,tag):
    ofileName = "%s/histograms.root"%(outputDirectory)
    ofile = TFile.Open ( ofileName, "UPDATE")
    def CreatePlot(h1, datatag,ksval,ksvalMaxDist,ksvalX): 
        c1 = TCanvas('c1', 'c1',800,600)
        gStyle.SetOptStat(0) # remove the stats box
        gStyle.SetOptTitle(0) # remove the title
        gPad.SetTicks(1,1)
        gPad.SetMargin(0.16,0.16,0.16,0.05) #left,right,bottom,top

        h1.Draw("COLZ")
        CMSlabel = TLatex()
        CMSlabel.SetTextSize( 0.06 )
        CMSlabel.DrawTextNDC(0.2, 0.85, "CMS Internal")
        KSlabel = TLatex()
        KSlabel.SetTextFont( 42 )
        KSlabel.SetTextSize( 0.03 )
        KSlabel.DrawTextNDC(0.2, 0.8, ksval)
        KSlabel.DrawTextNDC(0.2, 0.76, ksvalMaxDist)
        KSlabel.DrawTextNDC(0.2, 0.72, ksvalX)
        h1.GetXaxis().SetTitle(varInfo[var1]['XaxisTitle'])
        h1.GetYaxis().SetTitle(varInfo[var2]['XaxisTitle'])
        # h1.GetZaxis().SetTitle(varInfo[var2]['ZaxisTitle'])
        if(datatag is "ratio"): 
            h1.GetZaxis().SetRangeUser(0.,2.1)
            h1.GetZaxis().SetTitle("Ratio [model/target]")
        elif(datatag is "model"):
            h1.GetZaxis().SetTitle("3b data (model) Events")
        elif(datatag is "target"):
            h1.GetZaxis().SetTitle("4b data (target) Events")
        c1.SaveAs("%s/mXvsmY_%s%s.pdf"%(outputDirectory,datatag,tag))
        del c1
    
    h1 = TH2F( 'model_'+tag, 'model_'+tag, varInfo[var1]['bins'], varInfo[var1]['xlow'], varInfo[var1]['xhigh'], varInfo[var2]['bins'], varInfo[var2]['xlow'], varInfo[var2]['xhigh'])
    h2 = TH2F( 'target', 'target', varInfo[var1]['bins'], varInfo[var1]['xlow'], varInfo[var1]['xhigh'], varInfo[var2]['bins'], varInfo[var2]['xlow'], varInfo[var2]['xhigh'])
    for ii, val in enumerate(original[var1]):
        h1.Fill(val,original[var2][ii],weights[ii])
    for ii, val in enumerate(target[var1]):
        h2.Fill(val,target[var2][ii],1.)
    h3=h1.Clone("ratio")
    h3.Divide(h2)
    ksval = "KS Test = %.4f"%h1.KolmogorovTest(h2)
    ksvalMaxDist= "KS Test, Max Dist. = %.4f"%h1.KolmogorovTest(h2, "M")
    ksvalX = "KS Test, pseudoX = %.4f"%h1.KolmogorovTest(h2, "X")

    CreatePlot(h1,"model",ksval,ksvalMaxDist,ksvalX)
    CreatePlot(h2,"target",ksval,ksvalMaxDist,ksvalX)
    CreatePlot(h3,"ratio",ksval,ksvalMaxDist,ksvalX)
    h1.Write()
    h2.Write()
    h3.Write()
    del h1,h2,h3
    ofile.Close()
        
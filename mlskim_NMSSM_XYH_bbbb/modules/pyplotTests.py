import numpy 
import os
from ROOT import TFile, TH1F, TCanvas, gROOT, kTRUE, gPad, TLegend, gStyle, kRed, kBlue,TPad, TLatex, TH2F
import numpy as np
gROOT.SetBatch(kTRUE)
# from rootpy.plotting import Hist, HistStack, Legend, Canvas
# from rootpy.plotting.style import get_style, set_style
# from rootpy.plotting.utils import draw
# # from rootpy.interactive import wait
# import rootpy.plotting.root2matplotlib as rplt
import matplotlib
from matplotlib.ticker import AutoMinorLocator
import root_numpy
import pandas
import glob
from root_numpy import root2array
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from numpy.lib.recfunctions import stack_arrays
from hep_ml.metrics_utils import ks_2samp_weighted
from scipy import stats
import random
from VariableDicts import varInfo

def Draw1DHistosComparison_sep():
    tag='1'
    nums = numpy.array([])
    nums2 = numpy.array([]) 
    mu = 100
    sigma = 50
    mu2 =110
    sigma2 =55
    
    for i in range(10000): 
        temp = random.gauss(mu, sigma) 
        nums = numpy.append(nums, temp)
        temp2 = random.gauss(mu2,sigma2)
        nums2 = numpy.append(nums2, temp2)
    #Create folder for plots
    #Normalize or not?
    norm = True
    if norm is True:
      hist_settings = {'bins': 100, 'density': True}
    else:
      hist_settings = {'bins': 100, 'density': None}
    #Create figure on matplotlib
    matplotlib.rcParams.update({'font.size': 35})
    plt.figure(figsize=[80, 60], dpi=50)
    fig, ax = plt.subplots(2,1,figsize=(7,5), gridspec_kw={'height_ratios': [4, 1]})
    plt.subplots_adjust(
        left  = 0.125,  # the left side of the subplots of the figure
        right = 0.9,    # the right side of the subplots of the figure
        bottom = 0.1,   # the bottom of the subplots of the figure
        top = 0.9,    # the top of the subplots of the figure
        wspace = 0.2,   # the amount of width reserved for blank space between subplots
        hspace = 0.1   # the amount of height reserved for white space between subplots
    )
    ax[0].tick_params(axis='x', which='major', labelsize=0, direction='in',right=True,top=True)
    ax[0].tick_params(axis='x', which='minor', labelsize=0, direction='in',right=True,top=True)
    ax[0].tick_params(axis='y', which='major', labelsize=10, direction='in',right=True,top=True)
    ax[0].tick_params(axis='y', which='minor', labelsize=8, direction='in',right=True,top=True)
    ax[0].xaxis.set_minor_locator(AutoMinorLocator())
    ax[0].yaxis.set_minor_locator(AutoMinorLocator())
    xlim = numpy.percentile(numpy.hstack([nums]), [0.01, 99.99])
    counts0,bins0,patches0 = ax[0].hist(nums, label='Bkg. Model', range=xlim, histtype='step', color='r', **hist_settings)
    counts,bin_edges = numpy.histogram(nums2, range=xlim, **hist_settings)
    th1f = Hist(40, -4, 4, name='my hist', title='Some Data')
    for i in range(25000):
        th1f.Fill(random.gauss(0., 1.))
    rplt.errorbar(th1f, xerr=False, emptybins=False, axes = ax[0])
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2.
    ax[0].errorbar(bin_centres, counts, fmt='o',label='4 btag (Target)',color='b', ms=2)
    legend_elements = [Line2D([0], [0], color='r', lw=2, label='Bkg. Model'),
                       Line2D([0], [0], marker='o', color='w', label='4 btag (Target)',
                            markerfacecolor='b', markersize=5)]
    ax[0].set_xlim([-100.,300.])
    ax[0].legend(handles=legend_elements,loc=1, prop={'size': 8},frameon=False)
    # plt.title(column,fontsize=40)
    # ax[0].set_xlabel("var_name", fontsize=12, position=(1., 0.), va='bottom', ha='right')
    # plt.ylabel("Fraction of Events (val/MeV)", loc='top')
    ax[0].set_ylabel('Fraction of Events (val/MeV)', fontsize=12, position=(0., 1.), va='top', ha='right')
    # ax[0].xaxis.set_label_coords(1., -0.20)
    # ax[0].yaxis.set_label_coords(-0.18, 1.)
    ax[0].yaxis.set_label_coords(-0.12, 1.)
    # for id in range(len(counts)):
        # print(counts0[id],counts[id])
    ratio=numpy.divide(counts0,counts,out=numpy.full_like(counts0,10.,dtype=numpy.double), where=counts!=0)
    # print(len(ratio))
    # print(len(bins0))
    # ax[1].bar(bins0[:-1], ratio)
    ax[1].errorbar(bins0[:-1], ratio, fmt='o',color='k', ms=2)
    ax[1].set_xlim([-100.,300.])
    ax[1].set_ylim([0.,2.])
    ax[1].plot([-100.,300.],[1.,1.])
    ax[1].set_xlabel("var_name", fontsize=12, position=(1., 0.), va='bottom', ha='right')
    ax[1].xaxis.set_label_coords(1., -0.5)
    ax[1].tick_params(axis='both', which='major', labelsize=10, direction='in',right=True,top=True)
    ax[1].tick_params(axis='both', which='minor', labelsize=8, direction='in',right=True,top=True)
    ax[1].xaxis.set_minor_locator(AutoMinorLocator())
    ax[1].yaxis.set_minor_locator(AutoMinorLocator())
    # counts2,bin_edges2 = numpy.histogram(ratio, range=xlim, bins=100)
    # bin_centres2 = (bin_edges2[:-1] + bin_edges2[1:])/2.
    # ax[1].errorbar(bin_centres2[:-1], counts2, fmt='o',color='k', ms=2)
    plt.savefig("pyplottest_%s.pdf"%(tag))
    plt.savefig("pyplottest_%s.png"%(tag))
    plt.close('all')

# Draw1DHistosComparison_sep()

def rootplot_2samp_ratio(numarray1, numarray2, pdict, outputDirectory):
    #### define the histograms
    h1 = TH1F( 'hg1', 'hg1', pdict['bins'], pdict['xlow'], pdict['xhigh'])
    h2 = TH1F( 'hg2', 'hg2', pdict['bins'], pdict['xlow'], pdict['xhigh'])
    for val in numarray1:
        h1.Fill(val)
    for val2 in numarray2:
        h2.Fill(val2)
    h1.Sumw2()
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
    h1.GetXaxis().SetRangeUser(-100.,300.)
    h1.GetXaxis().SetLabelSize(0.)
    #yaxis
    h1.GetYaxis().SetTitle(pdict['YaxisTitle'])
    h1.GetYaxis().SetLabelSize(0.05)
    h1.GetYaxis().SetTitleSize(0.05)
    h1.GetYaxis().SetTitleOffset(1.1)
    h1.GetYaxis().SetTickLength(0.02)
    
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
    h3.GetYaxis().SetRangeUser(0.,2.)
    h3.GetXaxis().SetLabelSize(0.15)
    h3.GetXaxis().SetLabelOffset(0.05)
    h3.GetYaxis().SetLabelSize(0.12)
    h3.GetYaxis().SetNdivisions(503)
    h3.GetXaxis().SetTickLength(0.1)
    h3.GetXaxis().SetTitleSize(.16)
    h3.GetXaxis().SetTitleOffset(1.1)
    h3.GetXaxis().SetTitle(pdict['XaxisTitle'])
    h3.GetYaxis().SetTickLength(0.03)
    h3.GetYaxis().SetTitleSize(.12)
    h3.GetYaxis().SetTitleOffset(0.3)
    h3.GetYaxis().SetTitle("model / target")

    #### save the histogram
    c1.SaveAs(outputDirectory + "pyplot_root_2.png")
    c1.SaveAs(outputDirectory + "pyplot_root_2.pdf")
    
    #end of function

def rootplot_2Dhist(numarray1, numarray2, weights, pdict, pdict2, outputDirectory):
    h1 = TH2F( 'hg1', 'hg1', pdict['bins'], pdict['xlow'], pdict['xhigh'], pdict2['bins'], pdict2['xlow'], pdict2['xhigh'])
    h2 = TH2F( 'hg1', 'hg1', pdict['bins'], pdict['xlow'], pdict['xhigh'], pdict2['bins'], pdict2['xlow'], pdict2['xhigh'])
    for ii, val in enumerate(numarray1):
        h1.Fill(val,numarray2[ii],weights[ii])
    for ii, val in enumerate(numarray1):
        h1.Fill(numarray2[ii],val,1.)
    
    c1 = TCanvas('c1', 'c1',800,600)
    gStyle.SetOptStat(0) # remove the stats box
    gStyle.SetOptTitle(0) # remove the title

    h1.Draw("SCAT")

    c1.SaveAs(outputDirectory+"mXvsmY.pdf")


    # end of function

# Draw1DHistosComparison_root()
tag='1'
nums = numpy.array([])
nums2 = numpy.array([]) 
weights = numpy.array([]) 
mu = 100
sigma = 50
mu2 =110
sigma2 =55
    
for i in range(10000): 
    temp = random.gauss(mu, sigma) 
    nums = numpy.append(nums, temp)
    temp2 = random.gauss(mu2,sigma2)
    nums2 = numpy.append(nums2, temp2)
    weights = numpy.append(weights, 1.)
outputDirectory = "./"
myvarname = "mX"
trainingVariables = ['H1_b1_ptRegressed', 'H1_b2_ptRegressed', 'H2_b1_ptRegressed', 'H2_b2_ptRegressed','H1_pt', 'H2_pt', 'H1_eta', 'H2_eta', 'HH_m', 'H1_bb_DeltaR', 'H2_bb_DeltaR', 'H2_m']

# rootplot_2samp_ratio(nums, nums2, VariableDicts.varInfo['H1_b1_ptRegressed'], outputDirectory)
rootplot_2Dhist(nums,nums2, weights, varInfo['HH_kinFit_m'], varInfo['H2_m'], outputDirectory)
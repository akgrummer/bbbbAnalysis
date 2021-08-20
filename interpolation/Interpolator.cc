#include <algorithm>
#include "RooBinning.h"
#include "RooRealVar.h"
#include "RooArgList.h"
#include "RooDataHist.h"
#include "RooHistPdf.h"
#include "RooAddPdf.h"
#include "RooMomentMorphND.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TROOT.h"
#include "TH1D.h"
#include "TH2F.h"
#include "TGraph2D.h"
#include "TSystem.h"

// g++  -std=c++17 -I `root-config --incdir` -lRooFit -lRooFitCore -o Interpolator Interpolator.cc `root-config --libs` -O3 && ./Interpolator

class InterpolatorHist2D
{
  public:
    InterpolatorHist2D()
    {
        fIntegralInterpolation = std::make_shared<TGraph2D>();
        fIntegralInterpolation->SetNameTitle("IntegralInterpolation", "Integral Interpolation; m_{X} [GeV]; m_{Y} [GeV]");
    }
    ~InterpolatorHist2D(){}

    void addPlot(const TH2F* thePlot, float mX, float mY)
    {
        auto thePoint = std::make_tuple(mX, mY);
        if(fThePlotMap.find(thePoint) != fThePlotMap.end())
        {
            std::string runTimeErrorMessage = std::string(__PRETTY_FUNCTION__) + " Point already exists";
            throw std::runtime_error(runTimeErrorMessage.c_str());
        }
        fThePlotMap[thePoint] = thePlot;

        fIntegralInterpolation->SetPoint(fIntegralInterpolation->GetN(), mX, mY, thePlot->Integral());
    }

    TH2F* getInterpolatedPlot(float mXtargetValue, float mYtargetValue)
    {

        RooArgList variableList;
        RooRealVar mXreco("mXreco", "m_{Xreco}", fThePlotMap.begin()->second->GetXaxis()->GetXmin(), fThePlotMap.begin()->second->GetXaxis()->GetXmax(), "GeV");
        variableList.add(mXreco);
        RooRealVar mYreco("mYreco", "m_{Yreco}", fThePlotMap.begin()->second->GetYaxis()->GetXmin(), fThePlotMap.begin()->second->GetYaxis()->GetXmax(), "GeV");
        variableList.add(mYreco);

        RooArgList mtargetList;
        RooRealVar mXtarget("mXtarget", "mXtarget", fThePlotMap.begin()->second->GetXaxis()->GetXmin(), fThePlotMap.begin()->second->GetXaxis()->GetXmax());
        mXtarget.setVal(mXtargetValue);
        mtargetList.add(mXtarget);
        RooRealVar mYtarget("mYtarget", "mYtarget", fThePlotMap.begin()->second->GetYaxis()->GetXmin(), fThePlotMap.begin()->second->GetYaxis()->GetXmax());
        mYtarget.setVal(mYtargetValue);
        mtargetList.add(mYtarget);

        std::vector<double> mXvector;
        std::vector<double> mYvector;

        for(const auto& thePointAndPlot : fThePlotMap)
        {
            mXvector.push_back(std::get<0>(thePointAndPlot.first));
            mYvector.push_back(std::get<1>(thePointAndPlot.first));
        }

        std::sort( mXvector.begin(), mXvector.end() );
        mXvector.erase( std::unique( mXvector.begin(), mXvector.end() ), mXvector.end() );

        std::sort( mYvector.begin(), mYvector.end() );
        mYvector.erase( std::unique( mYvector.begin(), mYvector.end() ), mYvector.end() );


        RooBinning mXbinning(mXvector.size()-1, mXvector.data());
        RooBinning mYbinning(mYvector.size()-1, mYvector.data());

        RooMomentMorphND::Grid theGrid(mXbinning,mYbinning);

        for(const auto& thePointAndPlot : fThePlotMap)
        {
            //Those has to be pointers otherwise it crashes, Grid and list do not make a copy but they just get a reference :-( :-( :-( !!!
            int mX = std::get<0>(thePointAndPlot.first);
            int mY = std::get<1>(thePointAndPlot.first);
            std::string histName          = "theRooHist_mX_"       + std::to_string(mX) + "_mY_" + std::to_string(mY);
            std::string histPdfName       = "theRooHistPdg_mX_"    + std::to_string(mX) + "_mY_" + std::to_string(mY);
            std::string normalizationName = "theNormalization_mX_" + std::to_string(mX) + "_mY_" + std::to_string(mY);
            std::string pdfName           = "thePfd_mX_"           + std::to_string(mX) + "_mY_" + std::to_string(mY);
            RooDataHist *theRooHist    = new RooDataHist(histName.c_str(), histName.c_str(), variableList, thePointAndPlot.second);
            RooHistPdf  *theRooHistPdg = new RooHistPdf(histPdfName.c_str(), histPdfName.c_str(), variableList, *theRooHist );

            float integral = thePointAndPlot.second->Integral();
            RooRealVar  *theNormalization = new RooRealVar(normalizationName.c_str(), normalizationName.c_str(), 0.5 * integral, 1.5 * integral);
            RooAddPdf   *thePfd           = new RooAddPdf(pdfName.c_str(), pdfName.c_str(), RooArgList(*theRooHistPdg), RooArgList(*theNormalization));
            int mXvectorPosition = find(mXvector.begin(), mXvector.end(), mX) - mXvector.begin();
            int mYvectorPosition = find(mYvector.begin(), mYvector.end(), mY) - mYvector.begin();
            
            std::cout << "mX = " << mX << " (" << mXvectorPosition << ") - mY = " << mY << " (" << mYvectorPosition << ")" << std::endl;
            theGrid.addPdf(*thePfd, mXvectorPosition, mYvectorPosition);
        }

        RooMomentMorphND theRooMomentMorphND("morph", "morph", mtargetList, variableList, theGrid, RooMomentMorphND::Linear);
        theRooMomentMorphND.useHorizontalMorphing(true);

        std::string interpolatedPlotName = "InterlatedPlot_mX_" + std::to_string(mXtargetValue) + "_mY_" + std::to_string(mYtargetValue);
        TH2F* theInterpolatedPlot = static_cast<TH2F*>(fThePlotMap.begin()->second->Clone(interpolatedPlotName.c_str()));
        theInterpolatedPlot->SetTitle(interpolatedPlotName.c_str());
        theInterpolatedPlot->SetDirectory(0);
        theInterpolatedPlot->Reset("ICES");

        float interpolatedIntegral = fIntegralInterpolation->Interpolate(mXtargetValue,mYtargetValue);

        theRooMomentMorphND.fillHistogram(theInterpolatedPlot, variableList);
        theInterpolatedPlot->Scale(interpolatedIntegral/theInterpolatedPlot->Integral());

        return theInterpolatedPlot;
    }

    std::shared_ptr<TGraph2D> getIntegrapInterpolationPlot() {return fIntegralInterpolation;}

  private:
    std::map<std::tuple<float,float>, const TH2F*> fThePlotMap;
    std::shared_ptr<TGraph2D> fIntegralInterpolation;

};


/*std::vector<std::string> signalList = 
    {
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_60.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_70.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_80.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_1000.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_1000.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_1200.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_1000.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_1200.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_1400.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_1000.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_1200.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_1400.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_1600.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1000.txt",
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1200.txt",
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1400.txt",
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1600.txt",
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1800.txt",
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_400.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_400.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_500.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_400.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_500.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_600.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_400.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_500.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_600.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_700.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_90.txt"  
    };
*/


std::pair<int, int> getMxMyFromSample(std::string sampleName)
{
    std::string mxStringStart = "_MX_";
    std::string mxStringEnd   = "_NANOAOD_";
    std::string myStringStart = "_MY_";
    size_t mxStart = sampleName.find(mxStringStart) + mxStringStart.size();
    size_t mxEnd   = sampleName.find(mxStringEnd);
    size_t myStart = sampleName.find(myStringStart) + myStringStart.size();
    size_t myEnd   = sampleName.size();

    std::string mx = sampleName.substr(mxStart, mxEnd-mxStart);
    std::string my = sampleName.substr(myStart, myEnd-myStart);

    return std::make_pair(std::stoi(mx), std::stoi(my));
}

std::string getPlotName(int mX, int mY)
{
    std::string plotName = "sig_NMSSM_bbbb_MX_" + std::to_string(mX) + "_MY_" + std::to_string(mY) + "/selectionbJets_SignalRegion/sig_NMSSM_bbbb_MX_" + std::to_string(mX) + "_MY_" + std::to_string(mY) + "_selectionbJets_SignalRegion_HH_kinFit_m_H2_m";
    return plotName;
}

template<typename Hist>
Hist* getHistogramFromFile(TFile& inputFile, std::string histogramName)
{
    Hist* histogram = (Hist*)inputFile.Get(histogramName.data());
    if(histogram == nullptr)
    {
        std::cout<< "Histogram " << histogramName << " does not exist" << std::endl;
        return nullptr;
    }
    histogram->SetDirectory(0);

    return histogram;
}

class getMassGridPoint
{
  public:
    getMassGridPoint(int year)
    {
        for(const auto & signalName : fSignalList) 
        {
            std::pair<int, int> signalPoint = getMxMyFromSample(signalName);
            fMassXlist.push_back(signalPoint.first );
            fMassYlist.push_back(signalPoint.second);
        }
        
        sort( fMassXlist.begin(), fMassXlist.end() );
        fMassXlist.erase( unique( fMassXlist.begin(), fMassXlist.end() ), fMassXlist.end() );

        sort( fMassYlist.begin(), fMassYlist.end() );
        fMassYlist.erase( unique( fMassYlist.begin(), fMassYlist.end() ), fMassYlist.end() );

        for(const auto mX : fMassXlist)
        {
            for(const auto mY : fMassYlist)
            {
                fMassGridFilledPoints[std::make_pair(mX,mY)] = false;
            }
        }

        for(const auto & signalName : fSignalList) 
        {
            std::pair<int, int> signalPoint = getMxMyFromSample(signalName);
            if(year==2017 && signalPoint.first == 1000 && signalPoint.second == 125) continue;
            fMassGridFilledPoints[signalPoint] = true
        }
    }
    ~getMassGridPoint(){}

    std::vector<std::pair<int, int>> getListOfREferencePoints(int mXtarget, int mYtarget)
    {
        
    }

  private:
    std::vector<std::string> fSignalList = 
    {
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_60.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_70.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_80.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1000_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1100_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_1000.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1200_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_1000.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_1200.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1400_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_1000.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_1200.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_1400.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1600_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_1000.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_1200.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_1400.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_1600.txt",
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_1800_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_100.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1000.txt",
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1200.txt",
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_125.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1400.txt",
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_150.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1600.txt",
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_1800.txt",
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_200.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_250.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_300.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_400.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_500.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_600.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_700.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_800.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_90.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_2000_NANOAOD_v7_Full_MY_900.txt" ,
        "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_300_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_400_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_500_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_400.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_600_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_400.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_500.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_700_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_400.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_500.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_600.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_800_NANOAOD_v7_Full_MY_90.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_100.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_125.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_150.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_200.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_250.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_300.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_400.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_500.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_60.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_600.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_70.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_700.txt"  ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_80.txt"   ,
        "FileList_NMSSM_XYH_bbbb_MX_900_NANOAOD_v7_Full_MY_90.txt"  
    };
    std::map<std::pair<int,int>, bool> fMassGridFilledPoints; 
    std::vector<int> fMassXlist; 
    std::vector<int> fMassYlist; 
};

void TestInterpolation(int year=2016, int plotVersion=21, int mXtestPoint=700, int mYtestPoint=300)
{
    std::string plotInputFileName  = "../DataPlots_fullSubmission_" + std::to_string(year) + "_v" + std::to_string(plotVersion) + "/outPlotter.root";
    TFile plotInputFile(plotInputFileName.data());
    InterpolatorHist2D theInterpolatorHist2D;

    for(const auto &signalName : signalList)
    {
        auto mXmYpair = getMxMyFromSample(signalName);
        int mX = mXmYpair.first ;
        int mY = mXmYpair.second;
        if(mX==mXtestPoint && mY==mYtestPoint) continue;

        float crossSection = 1.;
        if (mX >=  0.)   crossSection = 100.;
        if (mX >=  600.) crossSection = 10.;
        if (mX >= 1600.) crossSection = 1.;
        TH2F* theMassPlot = getHistogramFromFile<TH2F>(plotInputFile,getPlotName(mX,mY));
        theMassPlot->Scale(1./crossSection);
        theInterpolatorHist2D.addPlot(theMassPlot, mX, mY);
    }

    auto theInterpolatedPlot = theInterpolatorHist2D.getInterpolatedPlot(mXtestPoint, mYtestPoint);
    float crossSection = 1.;
    if (mXtestPoint >=  0.)   crossSection = 100.;
    if (mXtestPoint >=  600.) crossSection = 10.;
    if (mXtestPoint >= 1600.) crossSection = 1.;
    theInterpolatedPlot->Scale(crossSection);

    auto theOriginalPlot     = getHistogramFromFile<TH2F>(plotInputFile,getPlotName(mXtestPoint,mYtestPoint));

    plotInputFile.Close();

    float originalIntegral         = theOriginalPlot->Integral();
    float interpolatedIntegral = theInterpolatedPlot->Integral();

    std::cout<<"Original integral     = " << originalIntegral     << std::endl;
    std::cout<<"Interpolated integral = " << interpolatedIntegral << std::endl;
    std::cout<<"Difference            = " << (interpolatedIntegral-originalIntegral)/originalIntegral*100. << "%" << std::endl;

    std::string outputPlotName = "InterpolationTest_" + std::to_string(year) + "_mX_" + std::to_string(mXtestPoint) + "_mY_"  + std::to_string(mYtestPoint) + ".root";
    TFile outputFile(outputPlotName.data(),"RECREATE");

    theInterpolatedPlot->Write();
    theOriginalPlot    ->Write();

    // TMP - BEGIN
    gROOT->SetBatch(true);
    TCanvas c1;
	theInterpolatedPlot->SetMarkerColor(kRed);
    theInterpolatedPlot->Scale(10);
    theInterpolatedPlot->Draw(""   );
    // auto theOriginalPlot1   = getHistogramFromFile<TH2F>(plotInputFile,getPlotName(400,200));
	// theOriginalPlot1   ->SetMarkerColor(kBlue);
    // theOriginalPlot1   ->Scale(10);
    // theOriginalPlot1   ->Draw("same");
    // auto theOriginalPlot2   = getHistogramFromFile<TH2F>(plotInputFile,getPlotName(700,100));
	// theOriginalPlot2   ->SetMarkerColor(kGreen);
    // theOriginalPlot2   ->Scale(10);
    // theOriginalPlot2   ->Draw("same");
    // auto theOriginalPlot3   = getHistogramFromFile<TH2F>(plotInputFile,getPlotName(700,500));
	// theOriginalPlot3   ->SetMarkerColor(kOrange);
    // theOriginalPlot3   ->Scale(10);
    // theOriginalPlot3   ->Draw("same");
    // auto theOriginalPlot4   = getHistogramFromFile<TH2F>(plotInputFile,getPlotName(900,500));
	// theOriginalPlot4   ->SetMarkerColor(kViolet);
    // theOriginalPlot4   ->Scale(10);
    // theOriginalPlot4   ->Draw("same");
    theOriginalPlot->SetMarkerColor(kRed);
    theInterpolatedPlot->Scale(10);
    theInterpolatedPlot->Draw(""   );
	c1.SaveAs("testReal.pdf");
	gROOT->SetBatch(false);
    // TMP - END

    outputFile.Close();

    return;
}

int main()
{
    gSystem->ResetSignal(kSigSegmentationViolation, kTRUE);

    TestInterpolation();
    return 0;
}

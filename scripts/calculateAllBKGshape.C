#include "Riostream.h"
#include "TFile.h"
#include "TH1F.h"

template<typename Hist>
Hist* getHistogramFromFile(TFile& inputFile, std::string histogramName)
{
    Hist* histogram = (Hist*)inputFile.Get(histogramName.c_str());
    if(histogram == nullptr)
    {
        std::cout<< "Histogram " << histogramName << " does not exist" << std::endl;
        exit(EXIT_FAILURE);
    }
    histogram->SetDirectory(0);
    return histogram;
}

std::string getDatasetFolderName(std::string dataset, std::string variation = "")
{
    std::string datasetFolder = dataset + variation;
    return datasetFolder;
}

std::string getRegionFolderName(std::string region)
{
    return region;
}

std::string getDatasetAndRegionFolderName(std::string dataset, std::string region, std::string variation = "")
{
    std::string datasetAndRegionFolder = getDatasetFolderName(dataset, variation) + "/" + getRegionFolderName(region);
    return datasetAndRegionFolder; 
}

std::string getHistogramName(std::string dataset, std::string region, std::string variable, std::string variation = "")
{
    return dataset + variation + "_" + region + "_" + variable;
}

std::string getFullHistName (std::string dataset, std::string region, std::string variable, std::string variation = "")
{
    std::string fullHistogramName = getDatasetFolderName(dataset, variation) + "/" + getRegionFolderName(region) + "/" + getHistogramName(dataset, region, variable, variation);
    return fullHistogramName;
}

void calculateBKGshape(std::string inputFileName)
{
    TFile inputFile(inputFileName.c_str(), "UPDATE");

    std::string dataset          = "data_BTagCSV_dataDriven_kinFit"    ;
    std::string region           = "selectionbJets_SignalRegion"       ;
    std::string variable         = "HH_kinFit_m_H2_m_Rebinned_Unrolled";
    std::string variationUp      = "_up"                               ;
    std::string variationDown    = "_down"                             ;
    std::string newVariationUp   = "_upRefined"                        ;
    std::string newVariationDown = "_downRefined"                      ;

    TH1F* bkgNominal = getHistogramFromFile<TH1F>(inputFile, getFullHistName(dataset, region, variable               ));
    TH1F* bkgUp      = getHistogramFromFile<TH1F>(inputFile, getFullHistName(dataset, region, variable, variationUp  ));
    TH1F* bkgDown    = getHistogramFromFile<TH1F>(inputFile, getFullHistName(dataset, region, variable, variationDown));

    float bkgNominalIntegral = bkgNominal->Integral();
    inputFile.mkdir(getDatasetFolderName(dataset, newVariationUp).c_str());
    inputFile.cd   (getDatasetFolderName(dataset, newVariationUp).c_str());
    inputFile.mkdir(getDatasetAndRegionFolderName(dataset, region, newVariationUp).c_str());
    inputFile.cd   (getDatasetAndRegionFolderName(dataset, region, newVariationUp).c_str());

    std::string bkgUpRefinedName = getHistogramName(dataset, region, variable, newVariationUp);
    TH1F *bkgUpRefined = new TH1F(bkgUpRefinedName.c_str(), bkgUpRefinedName.c_str(), bkgNominal->GetNbinsX(), bkgNominal->GetXaxis()->GetBinLowEdge(1), bkgNominal->GetXaxis()->GetBinUpEdge(bkgNominal->GetNbinsX()));
    for(int nBinX = 1; nBinX<=bkgNominal->GetNbinsX(); ++nBinX)
    {
        if(TMath::Abs(bkgUp->GetBinContent(nBinX)- bkgNominal->GetBinContent(nBinX)) > TMath::Abs(bkgDown->GetBinContent(nBinX)- bkgNominal->GetBinContent(nBinX))){ 
        bkgUpRefined->SetBinContent(nBinX, TMath::Abs(bkgUp->GetBinContent(nBinX)- bkgNominal->GetBinContent(nBinX)) + bkgNominal->GetBinContent(nBinX));
        bkgUpRefined->SetBinError  (nBinX, sqrt(bkgUp->GetBinError(nBinX)*bkgUp->GetBinError(nBinX) + 2*bkgNominal->GetBinError(nBinX)*bkgNominal->GetBinError(nBinX)));
        }
        else{
          bkgUpRefined->SetBinContent(nBinX, TMath::Abs(bkgDown->GetBinContent(nBinX)- bkgNominal->GetBinContent(nBinX)) + bkgNominal->GetBinContent(nBinX) );
          bkgUpRefined->SetBinError  (nBinX, sqrt(bkgDown->GetBinError(nBinX)*bkgDown->GetBinError(nBinX) + 2*bkgNominal->GetBinError(nBinX)*bkgNominal->GetBinError(nBinX)));
        }

        //bkgUpRefined->SetBinContent(nBinX, (bkgUp->GetBinContent(nBinX)+bkgDown->GetBinContent(nBinX))/2.);
        //bkgUpRefined->SetBinError  (nBinX, sqrt(bkgUp->GetBinError(nBinX)*bkgUp->GetBinError(nBinX) + bkgDown->GetBinError(nBinX)*bkgDown->GetBinError(nBinX))/2.);
    }
    //bkgUpRefined->Scale(bkgNominalIntegral/bkgUpRefined->Integral());
    bkgUpRefined->Write();

    inputFile.mkdir(getDatasetFolderName(dataset, newVariationDown).c_str());
    inputFile.cd   (getDatasetFolderName(dataset, newVariationDown).c_str());
    inputFile.mkdir(getDatasetAndRegionFolderName(dataset, region, newVariationDown).c_str());
    inputFile.cd   (getDatasetAndRegionFolderName(dataset, region, newVariationDown).c_str());

    std::string bkgDownRefinedName = getHistogramName(dataset, region, variable, newVariationDown);
    TH1F *bkgDownRefined = new TH1F(bkgDownRefinedName.c_str(), bkgDownRefinedName.c_str(), bkgNominal->GetNbinsX(), bkgNominal->GetXaxis()->GetBinLowEdge(1), bkgNominal->GetXaxis()->GetBinUpEdge(bkgNominal->GetNbinsX()));
    for(int nBinX = 1; nBinX<=bkgNominal->GetNbinsX(); ++nBinX)
    {
        bkgDownRefined->SetBinContent(nBinX, bkgNominal->GetBinContent(nBinX) - (bkgUpRefined->GetBinContent(nBinX) - bkgNominal->GetBinContent(nBinX)));
        bkgDownRefined->SetBinError  (nBinX, bkgUpRefined->GetBinError(nBinX));
    }
    // bkgDownRefined->Scale(bkgNominalIntegral/bkgDownRefined->Integral());
    bkgDownRefined->Write();

    std::cout << getFullHistName(dataset, region, variable                  ) << std::endl;
    std::cout << getFullHistName(dataset, region, variable, newVariationUp  ) << std::endl;
    std::cout << getFullHistName(dataset, region, variable, newVariationDown) << std::endl;
    
}


void calculateAllBKGshape(std::string tag, std::string tagDir = "")
{
    std::vector<int> massesGroupList {0, 1, 2, 3, 4};
    /* std::vector<int> massesGroupList {0}; */
    std::vector<int> yearList        {2016, 2017, 2018};

    for(const auto year : yearList)
    {
        for(const auto massGroup : massesGroupList)
        {
            /* std::string inputFileName = "DataPlots_fullSubmission_" + std::to_string(year) + "_" + tag + "/outPlotter_massGroup" + std::to_string(massGroup) + ".root"; */
            std::string inputFileName = "VarPlots/rootHists/" + tagDir + std::to_string(year) + "DataPlots_" + tag + "/outPlotter_massGroup" + std::to_string(massGroup) + ".root";
            calculateBKGshape(inputFileName);
        }
    }
}


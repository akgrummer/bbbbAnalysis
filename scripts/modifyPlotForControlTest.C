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

void modifyPlotForControlTest(std::string inputFileName)
{
    TFile inputFile(inputFileName.c_str(), "UPDATE");

    std::string dataDataset      = "data_BTagCSV"                          ; //4b data
    std::string bkgDataset       = "data_BTagCSV_dataDriven_kinFit"        ; //3b data reweighted
    std::string signalRegion     = "selectionbJets_SignalRegion"           ;
    std::string validationRegion = "selectionbJets_ControlRegionBlinded";
    std::string variable         = "HH_kinFit_m_H2_m_Rebinned_Unrolled"    ;
    std::string variationUp      = "_up"                                   ;
    std::string variationDown    = "_down"                                 ;
    
    inputFile.cd(getDatasetAndRegionFolderName(dataDataset, signalRegion).c_str());
    gDirectory->Delete((getHistogramName(dataDataset, signalRegion, variable) + ";1").c_str());
    inputFile.cd(getDatasetAndRegionFolderName(bkgDataset, signalRegion).c_str());
    gDirectory->Delete((getHistogramName(bkgDataset, signalRegion, variable) + ";1").c_str());
    // inputFile.cd(getDatasetAndRegionFolderName(bkgDataset, signalRegion, variationUp  ).c_str());
    // gDirectory->Delete((getHistogramName(bkgDataset, signalRegion, variable, variationUp  ) + ";1").c_str());
    // inputFile.cd(getDatasetAndRegionFolderName(bkgDataset, signalRegion, variationDown).c_str());
    // gDirectory->Delete((getHistogramName(bkgDataset, signalRegion, variable, variationDown) + ";1").c_str());


    // inputFile.Delete((getFullHistName(dataDataset, signalRegion, variable) + ";1").c_str());
    // inputFile.Delete((getFullHistName(bkgDataset , signalRegion, variable) + ";1").c_str());
    // inputFile.Delete((getFullHistName(bkgDataset , signalRegion, variable, variationUp  ) + ";1").c_str());
    // inputFile.Delete((getFullHistName(bkgDataset , signalRegion, variable, variationDown) + ";1").c_str());

    TH1F* data       = getHistogramFromFile<TH1F>(inputFile, getFullHistName(dataDataset, validationRegion, variable               ));
    TH1F* bkgNominal = getHistogramFromFile<TH1F>(inputFile, getFullHistName(bkgDataset , validationRegion, variable               ));
    // TH1F* bkgUp      = getHistogramFromFile<TH1F>(inputFile, getFullHistName(bkgDataset , validationRegion, variable, variationUp  ));
    // TH1F* bkgDown    = getHistogramFromFile<TH1F>(inputFile, getFullHistName(bkgDataset , validationRegion, variable, variationDown));

    data      ->SetDirectory(0);
    bkgNominal->SetDirectory(0);
    // bkgUp     ->SetDirectory(0);
    // bkgDown   ->SetDirectory(0);

    data      ->SetName(getHistogramName(dataDataset, signalRegion, variable               ).c_str());
    bkgNominal->SetName(getHistogramName(bkgDataset , signalRegion, variable               ).c_str());
    // bkgUp     ->SetName(getHistogramName(bkgDataset , signalRegion, variable, variationUp  ).c_str());
    // bkgDown   ->SetName(getHistogramName(bkgDataset , signalRegion, variable, variationDown).c_str());

    inputFile.cd(getDatasetAndRegionFolderName(dataDataset, signalRegion).c_str());
    data->Write();
    inputFile.cd(getDatasetAndRegionFolderName(bkgDataset , signalRegion).c_str());
    bkgNominal->Write();
    // inputFile.cd(getDatasetAndRegionFolderName(bkgDataset , signalRegion, variationUp  ).c_str());
    // bkgUp->Write();
    // inputFile.cd(getDatasetAndRegionFolderName(bkgDataset , signalRegion, variationDown).c_str());
    // bkgDown->Write();
}


void modifyAllPlotForControlTest(std::string tag = "NMSSM_XYH_bbbb_dataDrivenStudies_aidan_2021Dec15")
{
    std::vector<int> massesGroupList {0, 1, 2, 3, 4};
    std::vector<int> yearList        {2016, 2017, 2018};

    for(const auto year : yearList)
    {
        for(const auto massGroup : massesGroupList)
        {
            std::string inputFileName = std::to_string(year) + "DataPlots_" + tag + "/outPlotter_massGroup" + std::to_string(massGroup) + ".root";
            modifyPlotForControlTest(inputFileName);
        }
    }
}
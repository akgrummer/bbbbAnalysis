// compile with:
// cd scripts && g++  -std=c++17 -I `root-config --incdir` -o BkgShape_ttbar BkgShape_ttbar.cc `root-config --libs` -O3 ; cd -
void BkgShape_ttbar(TString inputFileName, TString selectionName ){

    // if(argc < 2)
    // {
        // std::cout << "Usage: ./BkgShape_ttbar <infileName> <outfileName> <selection>"
        // return EXIT_FAILURE;
    // }
    
    //input
    // TString inputFileName = argv[1];
    // TString outputFileName = argv[2];
    // TString selectionName = argv[3];
    TString variable = "HH_kinFit_m_H2_m";
    // TString outputFileName = "outputFile.root";

    TFile ifile ( inputFileName, "UPDATE" );
    
    //root directories:
    TString dataDataset = "data_BTagCSV_dataDriven_kinFit";
    TString ttbarDataset = "ttbar";
    TString ttbar3bScaledDataset = "ttbar_3bScaled";
    TString outputDatasetUp = "data_BTagCSV_dataDriven_kinFit_ttbar_up";
    TString outputDatasetDown = "data_BTagCSV_dataDriven_kinFit_ttbar_down";

    //inputHistograms
    TString hDataName = dataDataset + "/" + selectionName + "/" + dataDataset + "_" + selectionName + "_"  + variable;
    TH2F *hData = (TH2F*)ifile.Get(hDataName);
    hData->SetDirectory(0);
    //
    TString hTTBARName = ttbarDataset + "/" + selectionName + "/" + ttbarDataset + "_" + selectionName + "_"  + variable;
    TH2F *hTTBAR = (TH2F*)ifile.Get(hTTBARName);
    hTTBAR->SetDirectory(0);
    //
    TString hTTBARName3bScaled = ttbar3bScaledDataset + "/" + selectionName + "/" + ttbar3bScaledDataset + "_" + selectionName + "_"  + variable;
    TH2F *hTTBAR3bScaled = (TH2F*)ifile.Get(hTTBARName3bScaled);
    hTTBAR3bScaled->SetDirectory(0);

    //output Histograms
    // TFile ofile ( outputFileName, "RECREATE");
    ifile.mkdir(outputDatasetUp + "/" + selectionName );
    ifile.mkdir(outputDatasetDown + "/" + selectionName );
    TString hBkgUpName = outputDatasetUp + "_" + selectionName + "_"  + variable;
    TString hBkgDownName = outputDatasetDown + "_" + selectionName + "_"  + variable;
    TH2F *hBkgUp = (TH2F *)hData->Clone(hBkgUpName);
    TH2F *hBkgDown = (TH2F *)hData->Clone(hBkgDownName);
    hBkgUp->Add(hTTBAR3bScaled);
    hBkgUp->Add(hTTBAR, -1);
    hBkgDown->Add(hTTBAR3bScaled, -1);
    hBkgDown->Add(hTTBAR);

    //write histograms
    ifile.cd( outputDatasetUp + "/" + selectionName );
    hBkgUp->Write(hBkgUp->GetName(), TObject::kOverwrite);
    ifile.cd( outputDatasetDown + "/" + selectionName );
    hBkgDown->Write(hBkgDown->GetName(), TObject::kOverwrite);

    ifile.Close();
}


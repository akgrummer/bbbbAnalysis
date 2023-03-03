import pandas as pd

def CreateDF(filename):
    print(filename)
    #  df = pd.read_csv("CondorJobs/jobsLimits_2022Sep14_Mx300_bJetLoose_depth4_leafs50_3_VR_rmax30_unrollcut/limits_MX_300_MY_60.txt", usecols=[0,1,3,7], names=['Names', 'LimitValStat',  'LimitValSyst',  'LimitValBkgNormOnly'])
    columnNames=["Names", "StatVal", "col2", "SystVal", "col4", "BkgNormOnlyVal"]
    df = pd.read_csv(filename, names=columnNames)
    df = df.drop(['col2', 'col4'], axis=1)
    #  df = pd.read_csv("CondorJobs/jobsLimits_2022Sep14_Mx300_bJetLoose_depth4_leafs50_3_VR_rmax30_unrollcut/limits_MX_300_MY_60.txt", usecols=[0,1,3,5], names=["0", "1", "3", "5"])
    #  df = pd.read_csv("CondorJobs/jobsLimits_2022Sep14_Mx300_bJetLoose_depth4_leafs50_3_VR_rmax30_unrollcut/limits_MX_300_MY_60.txt")
    #  for col in df.columns:
        #  print(col)
    #  df = df.drop
    obs_2016 = 2
    obs_2017 = 9
    obs_2018 = 16
    obs_RunII = 23
    per50_2016 =5
    per50_2017 =12
    per50_2018 =19
    per50_RunII =26
    onesigN_2016 =4
    onesigN_2017 =11
    onesigN_2018 =18
    onesigN_RunII =25
    onesigP_2016 =6
    onesigP_2017 =13
    onesigP_2018 =20
    onesigP_RunII =27

    df2016 = pd.DataFrame([['2016ObsMinusExp', float(df.loc[obs_2016, "StatVal"])-float(df.loc[per50_2016, "StatVal"]),
                                         float(df.loc[obs_2016, "SystVal"])-float(df.loc[per50_2016, "SystVal"]),
                                         float(df.loc[obs_2016, "BkgNormOnlyVal"])-float(df.loc[per50_2016, "BkgNormOnlyVal"]),
                       ]], columns=df.columns)

    df2016 = pd.DataFrame([['2016Sigma', df2016.loc[0, "StatVal"]/(float(df.loc[onesigP_2016, "StatVal"])-float(df.loc[per50_2016, "StatVal"])),
                                         df2016.loc[0, "SystVal"]/(float(df.loc[onesigP_2016, "SystVal"])-float(df.loc[per50_2016, "SystVal"])),
                                         df2016.loc[0, "BkgNormOnlyVal"]/(float(df.loc[onesigP_2016, "BkgNormOnlyVal"])-float(df.loc[per50_2016, "BkgNormOnlyVal"])),
                       ]], columns=df.columns)
    df2016 = pd.DataFrame([['2016sensitivity', float(df.loc[per50_2016, "StatVal"]),
                                         float(df.loc[per50_2016, "SystVal"]),
                                         float(df.loc[per50_2016, "BkgNormOnlyVal"]),
                       ]], columns=df.columns).append(df2016)

    df2017 = pd.DataFrame([['2017ObsMinusExp', float(df.loc[obs_2017, "StatVal"])-float(df.loc[per50_2017, "StatVal"]),
                                         float(df.loc[obs_2017, "SystVal"])-float(df.loc[per50_2017, "SystVal"]),
                                         float(df.loc[obs_2017, "BkgNormOnlyVal"])-float(df.loc[per50_2017, "BkgNormOnlyVal"]),
                       ]], columns=df.columns)

    df2017 = pd.DataFrame([['2017Sigma', df2017.loc[0, "StatVal"]/(float(df.loc[onesigP_2017, "StatVal"])-float(df.loc[per50_2017, "StatVal"])),
                                         df2017.loc[0, "SystVal"]/(float(df.loc[onesigP_2017, "SystVal"])-float(df.loc[per50_2017, "SystVal"])),
                                         df2017.loc[0, "BkgNormOnlyVal"]/(float(df.loc[onesigP_2017, "BkgNormOnlyVal"])-float(df.loc[per50_2017, "BkgNormOnlyVal"])),
                       ]], columns=df.columns)
    df2017 = pd.DataFrame([['2017sensitivity', float(df.loc[per50_2017, "StatVal"]),
                                         float(df.loc[per50_2017, "SystVal"]),
                                         float(df.loc[per50_2017, "BkgNormOnlyVal"]),
                       ]], columns=df.columns).append(df2017)

    df2018 = pd.DataFrame([['2018ObsMinusExp', float(df.loc[obs_2018, "StatVal"])-float(df.loc[per50_2018, "StatVal"]),
                                         float(df.loc[obs_2018, "SystVal"])-float(df.loc[per50_2018, "SystVal"]),
                                         float(df.loc[obs_2018, "BkgNormOnlyVal"])-float(df.loc[per50_2018, "BkgNormOnlyVal"]),
                       ]], columns=df.columns)

    df2018 = pd.DataFrame([['2018Sigma', df2018.loc[0, "StatVal"]/(float(df.loc[onesigP_2018, "StatVal"])-float(df.loc[per50_2018, "StatVal"])),
                                         df2018.loc[0, "SystVal"]/(float(df.loc[onesigP_2018, "SystVal"])-float(df.loc[per50_2018, "SystVal"])),
                                         df2018.loc[0, "BkgNormOnlyVal"]/(float(df.loc[onesigP_2018, "BkgNormOnlyVal"])-float(df.loc[per50_2018, "BkgNormOnlyVal"])),
                       ]], columns=df.columns)
    df2018 = pd.DataFrame([['2018sensitivity', float(df.loc[per50_2018, "StatVal"]),
                                         float(df.loc[per50_2018, "SystVal"]),
                                         float(df.loc[per50_2018, "BkgNormOnlyVal"]),
                       ]], columns=df.columns).append(df2018)

    dfRunII = pd.DataFrame([['RunIIObsMinusExp', float(df.loc[obs_RunII, "StatVal"])-float(df.loc[per50_RunII, "StatVal"]),
                                         float(df.loc[obs_RunII, "SystVal"])-float(df.loc[per50_RunII, "SystVal"]),
                                         float(df.loc[obs_RunII, "BkgNormOnlyVal"])-float(df.loc[per50_RunII, "BkgNormOnlyVal"]),
                       ]], columns=df.columns)

    dfRunII = pd.DataFrame([['RunIISigma', dfRunII.loc[0, "StatVal"]/(float(df.loc[onesigP_RunII, "StatVal"])-float(df.loc[per50_RunII, "StatVal"])),
                                         dfRunII.loc[0, "SystVal"]/(float(df.loc[onesigP_RunII, "SystVal"])-float(df.loc[per50_RunII, "SystVal"])),
                                         dfRunII.loc[0, "BkgNormOnlyVal"]/(float(df.loc[onesigP_RunII, "BkgNormOnlyVal"])-float(df.loc[per50_RunII, "BkgNormOnlyVal"])),
                       ]], columns=df.columns)
    #  dfRunII = pd.DataFrame([['RunIIsensitivity', float(df.loc[per50_RunII, "StatVal"]),
                                         #  float(df.loc[per50_RunII, "SystVal"]),
                                         #  float(df.loc[per50_RunII, "BkgNormOnlyVal"]),
                       #  ]], columns=df.columns).append(dfRunII)
    pd.set_option('display.max_columns', 500)

    dfout = df2016.append(df2017)
    dfout = dfout.append(df2018)
    dfout = dfout.append(dfRunII)
    # print(dfout)
    print(dfRunII)


filenames = [
        "jobsLimits_2022Sep14_Mx300_bJetLoose_3_rmax30_unrollcut", 
        "jobsLimits_2022Sep14_Mx300_bJetLoose_mx280cut_rmax30_unrollcut",
        "jobsLimits_2022Sep14_Mx300_bJetLoose_depth4_leafs50_3_rmax30_unrollcut",
        "jobsLimits_2022Sep14_Mx300_bJetLoose_depth2_leafs50_rmax30_unrollcut",
        "jobsLimits_2022Sep14_Mx300_bJetLoose_3_VR_rmax30_unrollcut", 
        "jobsLimits_2022Sep14_Mx300_bJetLoose_mx280cut_VR_rmax30_unrollcut",
        "jobsLimits_2022Sep14_Mx300_bJetLoose_depth4_leafs50_3_VR_rmax30_unrollcut",
        "jobsLimits_2022Sep14_Mx300_bJetLoose_depth2_leafs50_VR_rmax30_unrollcut"
        ]
massPoints=["/limits_MX_300_MY_60.txt", "/limits_MX_300_MY_150.txt"]

for massPoint in massPoints:
    for filename in filenames:
        CreateDF("CondorJobs/"+filename+massPoint)


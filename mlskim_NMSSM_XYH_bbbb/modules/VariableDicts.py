varInfo = {
    "H1_b1_kinFit_ptRegressed" : {
        # 'bins': 200,
        'bins': 32,
        'xlow': 0,
        'xhigh': 500,
        'xlowRange': -16.,
        'xhighRange': 516.,
        # 'XaxisTitle': "#lambda_{Z} [MeV]"
        'XaxisTitle': "H1_b1_kinFit_ptRegressed [GeV]"
    }, 
    "H1_b2_kinFit_ptRegressed" : {
        # 'bins': 200,
        'bins': 32,
        'xlow': 0,
        'xhigh': 500,
        'xlowRange': -16.,
        'xhighRange': 516.,
        'XaxisTitle': "H1_b2_kinFit_ptRegressed [GeV]"
    }, 
    "H2_b1_ptRegressed" : {
        # 'bins': 200,
        'bins': 32,
        'xlow': 0,
        'xhigh': 500,
        'xlowRange': -16.,
        'xhighRange': 516.,
        'XaxisTitle': "H2_b1_ptRegressed [GeV]"
    }, 
    "H2_b2_ptRegressed" : {
        # 'bins': 200,
        'bins': 32,
        'xlow': 0,
        'xhigh': 500,
        'xlowRange': -16.,
        'xhighRange': 516.,
        'XaxisTitle': "H2_b2_ptRegressed [GeV]"
    }, 
    "H1_kinFit_pt" : {
        # 'bins': 100,
        'bins': 32,
        'xlow': 0,
        'xhigh': 800,
        'xlowRange': -25.,
        'xhighRange': 825.,
        'XaxisTitle': "H1_kinFit_pt [GeV]"
    }, 
    "H2_pt" : {
        # 'bins': 100,
        'bins': 32,
        'xlow': 0,
        'xhigh': 800,
        'xlowRange': -25.,
        'xhighRange': 825.,
        'XaxisTitle': "H2_pt [MeV]"
    }, 
    "H1_kinFit_eta" : {
        # 'bins': 50,
        'bins': 50,
        'xlow': -5,
        'xhigh': 5,
        'xlowRange': -5.2,
        'xhighRange': 5.2,
        'XaxisTitle': "H1_kinFit_eta"
    }, 
    "H2_eta" : {
        # 'bins': 50,
        'bins': 50,
        'xlow': -5,
        'xhigh': 5,
        'xlowRange': -5.2,
        'xhighRange': 5.2,
        'XaxisTitle': "H2_eta"
    }, 
    "HH_kinFit_m" : {
        # 'bins': 100,
        'bins': 50,
        'xlow': 0,
        'xhigh': 2500,
        'xlowRange': -50,
        'xhighRange': 2550,
        'XaxisTitle': "HH_kinFit_m [GeV]",
        'nvbins':  36,
        'vbins': [212, 228, 244, 260, 276, 292, 308, 324, 340, 360, 392, 424, 456, 488, 520, 552, 584, 616, 648, 704, 768, 832, 896, 960, 1024, 1088, 1152, 1216, 1296, 1424, 1552, 1680, 1808, 1936, 2064, 2192, 2320]
    }, 
    "H1_kinFit_bb_DeltaR" : {
        # 'bins': 37,
        'bins': 37,
        'xlow': 0.,
        'xhigh': 3.7,
        'xlowRange': -0.1,
        'xhighRange': 3.8,
        'XaxisTitle': "H1_kinFit_bb_DeltaR"
    }, 
    "H2_bb_DeltaR" : {
        'bins': 30,
        'xlow': 0.,
        'xhigh': 5.4,
        'xlowRange': -0.18,
        'xhighRange': 5.58,
        'XaxisTitle': "H2_bb_DeltaR"
    }, 
    "H2_m" : {
        # 'bins': 100,
        'bins': 50,
        'xlow': 0,
        'xhigh': 1500,
        'xlowRange': -30,
        'xhighRange': 1530,
        'XaxisTitle': "H2_m [GeV]",
        'ZaxisTitle': "Events",
        'nvbins': 69,
        'vbins': [36, 45, 51, 57, 62, 66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 122, 132, 140, 148, 156, 164, 172, 180, 188, 196, 204, 212, 228, 244, 260, 276, 292, 308, 324, 340, 356, 372, 388, 412, 444, 476, 508, 540, 572, 604, 636, 668, 700, 732, 764, 828, 892, 956, 1020, 1084, 1148, 1212, 1276, 1340, 1404, 1468, 1564, 1692, 1820, 1948, 2076, 2204]

    }, 
    "distanceFromDiagonal" : {
        # 'bins': 100,
        # 'xlow': 0,
        # 'xhigh': 1500,
        # 'xlowRange': -15,
        # 'xhighRange': 1515,
        # 'XaxisTitle': "distanceFromDiagonal"
        'bins': 50,
        'xlow': 0,
        'xhigh': 1500,
        'xlowRange': -30.,
        'xhighRange': 1530.,
        'XaxisTitle': "distanceFromDiagonal"
    }
}
varInfo["H1_b1_kinFit_ptRegressed"]['YaxisTitle'] = "Fraction of Events / {val:.2f} GeV".format(val=(varInfo["H1_b1_kinFit_ptRegressed"]['xhigh']-varInfo["H1_b1_kinFit_ptRegressed"]['xlow'])/varInfo["H1_b1_kinFit_ptRegressed"]['bins'])
varInfo["H1_b2_kinFit_ptRegressed"]['YaxisTitle'] = "Fraction of Events / {val:.2f} GeV".format(val=(varInfo["H1_b2_kinFit_ptRegressed"]['xhigh']-varInfo["H1_b2_kinFit_ptRegressed"]['xlow'])/varInfo["H1_b2_kinFit_ptRegressed"]['bins'])
varInfo["H2_b1_ptRegressed"]['YaxisTitle'] = "Fraction of Events / {val:.2f} GeV".format(val=(varInfo["H2_b1_ptRegressed"]['xhigh']-varInfo["H2_b1_ptRegressed"]['xlow'])/varInfo["H2_b1_ptRegressed"]['bins'])
varInfo["H2_b2_ptRegressed"]['YaxisTitle'] = "Fraction of Events / {val:.2f} GeV".format(val=(varInfo["H2_b2_ptRegressed"]['xhigh']-varInfo["H2_b2_ptRegressed"]['xlow'])/varInfo["H2_b2_ptRegressed"]['bins'])
varInfo["H1_kinFit_pt"]['YaxisTitle'] = "Fraction of Events / {val:.2f} GeV".format(val=(varInfo["H1_kinFit_pt"]['xhigh']-varInfo["H1_kinFit_pt"]['xlow'])/varInfo["H1_kinFit_pt"]['bins'])
varInfo["H2_pt"]['YaxisTitle'] = "Fraction of Events / {val:.2f} GeV".format(val=(varInfo["H2_pt"]['xhigh']-varInfo["H2_pt"]['xlow'])/varInfo["H2_pt"]['bins'])
varInfo["H1_kinFit_eta"]['YaxisTitle'] = "Fraction of Events / {val:.2f}".format(val=(varInfo["H1_kinFit_eta"]['xhigh']-varInfo["H1_kinFit_eta"]['xlow'])/varInfo["H1_kinFit_eta"]['bins'])
varInfo["H2_eta"]['YaxisTitle'] = "Fraction of Events / {val:.2f}".format(val=(varInfo["H2_eta"]['xhigh']-varInfo["H2_eta"]['xlow'])/varInfo["H2_eta"]['bins'])
varInfo["HH_kinFit_m"]['YaxisTitle'] = "Fraction of Events / {val:.2f} GeV".format(val=(varInfo["HH_kinFit_m"]['xhigh']-varInfo["HH_kinFit_m"]['xlow'])/varInfo["HH_kinFit_m"]['bins'])
varInfo["H1_kinFit_bb_DeltaR"]['YaxisTitle'] = "Fraction of Events / {val:.2f}".format(val=(varInfo["H1_kinFit_bb_DeltaR"]['xhigh']-varInfo["H1_kinFit_bb_DeltaR"]['xlow'])/varInfo["H1_kinFit_bb_DeltaR"]['bins'])
varInfo["H2_bb_DeltaR"]['YaxisTitle'] = "Fraction of Events / {val:.2f}".format(val=(varInfo["H2_bb_DeltaR"]['xhigh']-varInfo["H2_bb_DeltaR"]['xlow'])/varInfo["H2_bb_DeltaR"]['bins'])
varInfo["H2_m"]['YaxisTitle'] = "Fraction of Events / {val:.2f} GeV".format(val=(varInfo["H2_m"]['xhigh']-varInfo["H2_m"]['xlow'])/varInfo["H2_m"]['bins'])
varInfo["distanceFromDiagonal"]['YaxisTitle'] = "Fraction of Events / {val:.2f}".format(val=(varInfo["distanceFromDiagonal"]['xhigh']-varInfo["distanceFromDiagonal"]['xlow'])/varInfo["distanceFromDiagonal"]['bins'])
# H1_b1_ptRegressed
# H1_b2_ptRegressed
# H2_b1_ptRegressed
# H2_b2_ptRegressed
# H1_pt
# H2_pt
# H1_eta
# H2_eta
# HH_m
# H1_bb_DeltaR
# H2_bb_DeltaR
# H2_m
# H1_b1_kinFit_ptRegressed
# H1_b2_kinFit_ptRegressed
# H2_b1_ptRegressed
# H2_b2_ptRegressed
# H1_kinFit_pt
# H2_pt
# H1_kinFit_eta
# H2_eta
# HH_kinFit_m
# H1_kinFit_bb_DeltaR
# H2_bb_DeltaR
# H2_m
# distanceFromDiagonal
from scipy.stats import norm

pval=0.0056
signif = -norm.ppf(pval)
print("pval: ", pval)
print("signif: {0:.4f}".format(signif))

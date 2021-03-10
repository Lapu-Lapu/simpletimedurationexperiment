from PsychophysicalFunctions import *
from model1 import *

x, n, r, rprop, names = load_data()
xij, nij, rij, xvect, xmean, sbjid, nsubjs = prepare_data(x, n, r)

with model1:
    trace1 = pm.sample(draws=1000, init="advi+adapt_diag", tune=2000)
pm.save_trace(trace1, 'intermediate/trace_model1.tr', overwrite=True)

az.plot_trace(trace1, var_names=["alpha", "beta"], compact=True);
plt.savefig('intermediate/traceplot_model1.png')
plt.close()

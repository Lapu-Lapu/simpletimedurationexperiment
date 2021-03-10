from PsychophysicalFunctions import *
from model2 import *

with model2b:
    s = theano.shared(pm.floatX(1))
    inference = pm.ADVI(cost_part_grad_scale=s)

    # ADVI has nearly converged
    inference.fit(n=20000)

    # It is time to set `s` to zero
    s.set_value(0)
    approx = inference.fit(n=10000)
    trace2b = approx.sample(3000, include_transformed=True)
    elbos1 = -inference.hist

pm.save_trace(trace2b, 'intermediate/model2_init.tr', overwrite=True)
az.plot_trace(trace2b, var_names=["alpha", "beta"], compact=True);
plt.savefig('intermediate/traceplot_model2_init.png')
plt.close()

# with model2b:
    # trace1 = pm.load_trace('intermediate/model2_init.tr')

nchains = 2
cov = np.atleast_1d(pm.trace_cov(trace2b, model=model2b))
start = list(np.random.choice(trace2b, nchains))
for ic in range(nchains):
    start[ic]["zij"] = start[ic]["zij"].astype(int)

potential = quadpotential.QuadPotentialFull(cov)
step = pm.NUTS(potential=potential, model=model2b_, vars=model2b_.free_RVs[:-1])

with model2b_:
    trace2b_ = pm.sample(1000, tune=1000, step=step, start=start, chains=nchains)

az.plot_trace(trace2b_, var_names=["alpha", "beta", "zij"], compact=True);
pm.save_trace(trace2b_, 'intermediate/model2.tr', overwrite=True)
plt.savefig('intermediate/traceplot_model2.png')
plt.close()

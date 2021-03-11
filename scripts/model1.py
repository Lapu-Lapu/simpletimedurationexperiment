from PsychophysicalFunctions import *

x, n, r, rprop, names = load_data()
xij, nij, rij, xvect, xmean, sbjid, nsubjs = prepare_data(x, n, r)

with pm.Model() as model1:
    sigma_a = pm.Uniform("sigma_a", lower=0, upper=500)
    sigma_b = pm.Uniform("sigma_b", lower=0, upper=500)

    mu_a = pm.Normal("mu_a", mu=0, tau=0.001)
    mu_b = pm.Normal("mu_b", mu=0, tau=0.001)

    alpha = pm.Normal("alpha", mu=mu_a, sd=sigma_a, shape=nsubjs)
    beta = pm.Normal("beta", mu=mu_b, sd=sigma_b, shape=nsubjs)

    linerpredi = alpha[sbjid] + beta[sbjid] * (xij - xvect)
    thetaij = pm.Deterministic("thetaij", tlogit(linerpredi))

    rij_ = pm.Binomial("rij", p=thetaij, n=nij, observed=rij)

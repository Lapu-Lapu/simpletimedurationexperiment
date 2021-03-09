from PsychophysicalFunctions import *

x, n, r, rprop, names = load_data()
xij, nij, rij, xvect, xmean, sbjid, nsubjs = prepare_data(x, n, r)

with pm.Model() as model1:
    #sigma_a = pm.Uniform("sigma_a", lower=0, upper=10)
    #sigma_b = pm.Uniform("sigma_b", lower=0, upper=10)
    sigma_a = pm.Uniform("sigma_a", lower=0, upper=0.5)
    sigma_b = pm.Uniform("sigma_b", lower=0, upper=0.5)

#     mu_a = pm.Normal("mu_a", mu=0, tau=0.001)
#     mu_b = pm.Normal("mu_b", mu=0, tau=0.001)
    mu_a = pm.Normal("mu_a", mu=0, tau=0.1000)
    mu_b = pm.Normal("mu_b", mu=0, tau=1000)

    alpha = pm.Normal("alpha", mu=mu_a, sd=sigma_a, shape=nsubjs)
    beta = pm.Normal("beta", mu=mu_b, sd=sigma_b, shape=nsubjs)

    linerpredi = alpha[sbjid] + beta[sbjid] * (xij - xvect)
    thetaij = pm.Deterministic("thetaij", tPhi(linerpredi))
#     thetaij = pm.Deterministic("thetaij", tlogit(linerpredi))

    rij_ = pm.Binomial("rij", p=thetaij, n=nij, observed=rij)
   
    prior_checks = pm.sample_prior_predictive(samples=150)

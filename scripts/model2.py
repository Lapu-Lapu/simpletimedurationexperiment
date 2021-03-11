from PsychophysicalFunctions import *


x, n, r, rprop, names = load_data()
xij, nij, rij, xvect, xmean, sbjid, nsubjs = prepare_data(x, n, r)

with pm.Model() as model2b:
    sigma_a = pm.Uniform("sigma_a", lower=0, upper=500)
    sigma_b = pm.Uniform("sigma_b", lower=0, upper=500)
    mu_a = pm.Normal("mu_a", mu=0, tau=0.001)
    mu_b = pm.Normal("mu_b", mu=0, tau=0.001)
    alpha = pm.Normal("alpha", mu=mu_a, sd=sigma_a, shape=nsubjs)
    beta = pm.Normal("beta", mu=mu_b, sd=sigma_b, shape=nsubjs)

    linerpredi = alpha[sbjid] + beta[sbjid] * (xij - xvect)

    # latent model for contamination
    sigma_p = pm.Uniform("sigma_p", lower=0, upper=3)
    mu_p = pm.Normal("mu_p", mu=0, tau=0.001)

    probitphi = pm.Normal(
        "probitphi", mu=mu_p, sd=sigma_p, shape=nsubjs, testval=np.ones(nsubjs)
    )
    phii = pm.Deterministic("phii", tPhi(probitphi))

    pi_ij = pm.Uniform("pi_ij", lower=0, upper=1, shape=xij.shape)

    # reparameterized so we can use ADVI initialization
    # zij_ = pm.Uniform('zij_',lower=0, upper=1, shape=xij.shape)
    # zij = pm.Deterministic('zij', tt.lt(zij_, phii[sbjid]))

    # rng = tt.shared_randomstreams.RandomStreams()
    # zij_ = rng.binomial(n=1, p=phii[sbjid], size=xij.shape)
    zij_ = pm.theanof.tt_rng().uniform(size=xij.shape)
    zij = pm.Deterministic("zij", tt.lt(zij_, phii[sbjid]))
    # zij = pm.Deterministic('zij', tt.eq(zij_, 0))

    thetaij = pm.Deterministic("thetaij", tt.switch(zij, tlogit(linerpredi), pi_ij))

    rij_ = pm.Binomial("rij", p=thetaij, n=nij, observed=rij)
    # priorsamples_m2 = pm.sample_prior_predictive()

with pm.Model() as model2b_:
    sigma_a = pm.Uniform("sigma_a", lower=0, upper=1000)
    sigma_b = pm.Uniform("sigma_b", lower=0, upper=1000)
    mu_a = pm.Normal("mu_a", mu=0, tau=0.001)
    mu_b = pm.Normal("mu_b", mu=0, tau=0.001)

    alpha = pm.Normal("alpha", mu=mu_a, sd=sigma_a, shape=nsubjs)
    beta = pm.Normal("beta", mu=mu_b, sd=sigma_b, shape=nsubjs)

    linerpredi = alpha[sbjid] + beta[sbjid] * (xij - xvect)

    # latent model for contamination
    sigma_p = pm.Uniform("sigma_p", lower=0, upper=3)
    mu_p = pm.Normal("mu_p", mu=0, tau=0.001)

    probitphi = pm.Normal(
        "probitphi", mu=mu_p, sd=sigma_p, shape=nsubjs, testval=np.ones(nsubjs)
    )
    phii = pm.Deterministic("phii", tPhi(probitphi))

    pi_ij = pm.Uniform("pi_ij", lower=0, upper=1, shape=xij.shape)

    # place holder if zij_ is in the graph in the previous model
    # zij_ = pm.Uniform('zij_',lower=0, upper=1, shape=xij.shape)

    zij = pm.Bernoulli("zij", p=phii[sbjid], shape=xij.shape)
    thetaij = pm.Deterministic(
        "thetaij", tt.switch(tt.eq(zij, 0), tlogit(linerpredi), pi_ij)
    )

    rij_ = pm.Binomial("rij", p=thetaij, n=nij, observed=rij)

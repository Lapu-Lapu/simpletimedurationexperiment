#!/usr/bin/env python
# coding: utf-8

import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc3 as pm
import theano

from matplotlib import gridspec
from pymc3.step_methods.hmc import quadpotential
from scipy import stats
import scipy
from theano import tensor as tt

RANDOM_SEED = 8927
np.random.seed(RANDOM_SEED)
az.style.use("arviz-darkgrid")


def logit(x):
    return 1 / (1 + np.exp(-x))


def invlogit(x):
    return np.log(x / (1 - x))


def Phi(x):
    # probit transform
    return 0.5 + 0.5 * scipy.special.erf(x / np.sqrt(2))

def load_data():
    # x = pd.read_csv("./data/data_x.txt", sep="\t", header=None)
    # n = pd.read_csv("./data/data_n.txt", sep="\t", header=None)
    # r = pd.read_csv("./data/data_r.txt", sep="\t", header=None)
    # rprop = pd.read_csv("./data/data_rprop.txt", sep="\t", header=None)

    x = pd.read_csv("analysis/data_x_c.txt", sep="\t", header=None)
    n = pd.read_csv("analysis/data_n_c.txt", sep="\t", header=None)
    r = pd.read_csv("analysis/data_r_c.txt", sep="\t", header=None)
    rprop = pd.read_csv("analysis/data_rprop_c.txt", sep="\t", header=None)
    with open("analysis/names.txt") as fh:
        names = {i: s[:-1] for i, s in zip(range(len(r)), fh)}
    return x, n, r, rprop, names

if __name__ == '__main__':


    # Data for all 8 subjects, showing the proportion of “long” responses as a function of test interval duration.


    x, n, r, rprop, names = load_data()


    # The psychometric function here is a logistic function with parameters $\alpha_i$ and $\beta_i$:  
    # 
    # $$ \theta_{ij} = \frac{1}{1+\text{exp}\{-[\alpha_{i}+\beta_{i}(x_{ij}-\bar x_{i})]\}}$$  
    # $$\text{or}$$   
    # $$ \text{logit}(\theta_{ij}) = \alpha_{i}+\beta_{i}(x_{ij}-\bar x_{i})$$
    # 
    # ## 12.1 Psychophysical functions
    # 
    # 
    # $$ r_{ij} \sim \text{Binomial}(\theta_{ij},n_{ij})$$
    # $$ \text{logit}(\theta_{ij}) = \alpha_{i}+\beta_{i}(x_{ij}-\bar x_{i})$$
    # $$ \alpha_{i} \sim \text{Gaussian}(\mu_{\alpha},\sigma_{\alpha})$$
    # $$ \beta_{i} \sim \text{Gaussian}(\mu_{\beta},\sigma_{\beta})$$
    # $$ \mu_{\alpha} \sim \text{Gaussian}(0,0.001)$$
    # $$ \mu_{\beta} \sim \text{Gaussian}(0,0.001)$$
    # $$ \sigma_{\alpha} \sim \text{Uniform}(0,1000)$$
    # $$ \sigma_{\beta} \sim \text{Uniform}(0,1000)$$

    import scipy.stats as stats
    from matplotlib.ticker import MaxNLocator

    N = 30
    p = 0.8
    theta = stats.binom(N, p)
    r = np.arange(10, N, dtype=int)
    fig = plt.figure()
    ax = fig.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_title(f'Binomial Distribution (N={N}; $\Theta$={p})')
    ax.set_xlabel('$r_{ij}$')
    ax.set_ylabel('$p(r_{ij})$')
    ax.bar(r, theta.pmf(r))
    plt.savefig('Binomial_Example.png')


    xij_tmp = x.values
    nij_tmp = n.values
    rij_tmp = r.values
    tmp, nstim2 = np.shape(xij_tmp)

    xmeanvect = np.repeat(xmean, nstim2)
    sbjidx = np.repeat(np.arange(nsubjs), nstim2)

    # remove nans
    validmask = np.isnan(xij_tmp.flatten()) == False
    xij2 = xij_tmp.flatten()
    nij2 = nij_tmp.flatten()
    rij2 = rij_tmp.flatten()

    xij = xij2[validmask]
    nij = nij2[validmask]
    rij = rij2[validmask]
    xvect = xmeanvect[validmask]
    sbjid = sbjidx[validmask]


    # Helper function

    def tPhi(x):
        # probit transform
        return 0.5 + 0.5 * pm.math.erf(x / pm.math.sqrt(2))


    def tlogit(x):
        return 1 / (1 + tt.exp(-x))


    def find_nearest(array, value):
        idx = (np.abs(array - value)).argmin()
        return idx


    trace1['mu_a'].mean(), trace1['mu_b'].mean()


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


    fig = plt.figure(figsize=(16, 8))
    fig.text(0.5, -0.02, "Test Interval (ms)", ha="center", fontsize=20)
    fig.text(
        -0.02,
        0.5,
        "Proportion of Long Responses",
        va="center",
        rotation="vertical",
        fontsize=20,
    )
    gs = gridspec.GridSpec(3, 4)

    for ip in np.arange(nsubjs):
        ax = plt.subplot(gs[ip])
        xp = np.array(x.iloc[ip, :])
        yp = np.array(rprop.iloc[ip, :])
        ax.scatter(xp, yp, marker="s", alpha=0.5)

        xl = np.linspace(190, 410, 100)

        # Posterior sample from the trace
        for ips in np.random.randint(0, 50, 100):
    #         param = prior_checks[ips]
    #         yl2 = logit(prior_checks["alpha"][ips][ip] + prior_checks["beta"][ips][ip] * (xl - xmean[ip]))
            yl2 = Phi(prior_checks["alpha"][ips][ip] + prior_checks["beta"][ips][ip] * (xl - xmean[ip]))
            plt.plot(xl, yl2, "k", linewidth=2, alpha=0.05)

        plt.axis([190, 410, -0.1, 1.1])
        plt.yticks((0, 0.5, 0.84, 1))
        plt.title("Subject %s" % (ip + 1))
        plt.title(names[ip])

    plt.tight_layout();


    trace1['alpha'].mean(axis=0)


    trace1['mu_a'].mean()


    prior_checks['alpha'].mean()


    with model1:
        trace1 = pm.sample(draws=1000, init="advi+adapt_diag", tune=2000)

    az.plot_trace(trace1, var_names=["alpha", "beta"], compact=True);


    # get MAP estimate
    tmp = az.summary(trace1, var_names=["alpha", "beta"])
    alphaMAP = tmp["mean"][np.arange(nsubjs)]
    betaMAP = tmp["mean"][np.arange(nsubjs) + nsubjs]


    fig = plt.figure(figsize=(16, 8))
    fig.text(0.5, -0.02, "Test Interval (ms)", ha="center", fontsize=20)
    fig.text(
        -0.02,
        0.5,
        "Proportion of Long Responses",
        va="center",
        rotation="vertical",
        fontsize=20,
    )
    gs = gridspec.GridSpec(3, 4)

    for ip in np.arange(nsubjs):
        ax = plt.subplot(gs[ip])
        xp = np.array(x.iloc[ip, :])
        yp = np.array(rprop.iloc[ip, :])
        ax.scatter(xp, yp, marker="s", alpha=0.5)

        xl = np.linspace(190, 410, 100)
    #     yl = logit(alphaMAP[ip] + betaMAP[ip] * (xl - xmean[ip]))
        yl = Phi(alphaMAP[ip] + betaMAP[ip] * (xl - xmean[ip]))
        x1 = xl[find_nearest(yl, 0.5)]
        x2 = xl[find_nearest(yl, 0.84)]

        plt.plot(xl, yl, "k", linewidth=2)
        plt.plot([x1, x1], [-0.1, 0.5], color="k", linestyle="--", linewidth=1)
        plt.plot([190, x1], [0.5, 0.5], color="k", linestyle="--", linewidth=1)
        plt.plot([x2, x2], [-0.1, 0.84], color="k", linestyle="--", linewidth=1)
        plt.plot([190, x2], [0.84, 0.84], color="k", linestyle="--", linewidth=1)

        plt.axis([190, 410, -0.1, 1.1])
        plt.yticks((0, 0.5, 0.84, 1))
        #plt.title("Subject %s" % (ip + 1))
        plt.title(names[ip])

    plt.tight_layout();


    with model1:
        ppc = pm.sample_posterior_predictive(trace1, samples=5000, var_names=["alpha", "beta"])

    alphaPPC = ppc["alpha"].mean(axis=1)
    betaPPC = ppc["beta"].mean(axis=1)


    # PLOT FOR EXERCISE 12.1.2
    fig = plt.figure(figsize=(16, 8))
    fig.text(0.5, -0.02, "Test Interval (ms)", ha="center", fontsize=20)
    fig.text(
        -0.02,
        0.5,
        "Proportion of Long Responses",
        va="center",
        rotation="vertical",
        fontsize=20,
    )
    gs = gridspec.GridSpec(3, 4)

    ppcsamples = 100

    for ip in np.arange(nsubjs):
        ax = plt.subplot(gs[ip])
        xp = np.array(x.iloc[ip, :])
        yp = np.array(rprop.iloc[ip, :])
        ax.scatter(xp, yp, marker="s", alpha=0.5)

        xl = np.linspace(190, 410, 100)
    #     yl = logit(alphaMAP[ip] + betaMAP[ip] * (xl - xmean[ip]))
        yl = Phi(alphaMAP[ip] + betaMAP[ip] * (xl - xmean[ip]))

        # Posterior sample from the trace
        for ips in np.random.randint(0, 1000, ppcsamples):
            param = trace1[ips]
    #         yl2 = logit(param["alpha"][ip] + param["beta"][ip] * (xl - xmean[ip]))
    #         yl3 = logit(param['mu_a'].mean() + param['mu_b'].mean() * (xl -xmean[ip]))
            yl2 = Phi(param["alpha"][ip] + param["beta"][ip] * (xl - xmean[ip]))
            yl3 = Phi(param['mu_a'].mean() + param['mu_b'].mean() * (xl -xmean[ip]))
            plt.plot(xl, yl2, "k", linewidth=2, alpha=0.05)
            plt.plot(xl, yl3, "y", linewidth=2, alpha=0.05)

        plt.plot(xl, yl, "r", linewidth=2)

        plt.axis([190, 410, -0.1, 1.1])
        plt.yticks((0, 0.5, 0.84, 1))
        plt.title("Subject %s" % (ip + 1))
        plt.title(names[ip])

    plt.tight_layout();


    for ips in np.random.randint(0, 1000, ppcsamples):
        param = trace1[ips]
        yl2 = param["alpha"][ip]


    param['alpha'][np.random.randint(0, 1000, ppcsamples)]


    # PLOT FOR EXERCISE 12.1.4
    fig = plt.figure(figsize=(16, 8))
    fig.text(0.5, -0.02, "JND (ms)", ha="center", fontsize=20)
    fig.text(-0.02, 0.5, "Posterior Density", va="center", rotation="vertical", fontsize=20)
    gs = gridspec.GridSpec(3, 4)

    ppcsamples = 500

    for ip in np.arange(nsubjs):
        ax = plt.subplot(gs[ip])

        xl = np.linspace(190, 410, 200)
        yl = logit(alphaMAP[ip] + betaMAP[ip] * (xl - xmean[ip]))
        x1 = xl[find_nearest(yl, 0.5)]
        x2 = xl[find_nearest(yl, 0.84)]
        jnd1 = x2 - x1

        # Posterior sample
        jndps = []
        for ips in np.random.randint(0, 1000, ppcsamples):
            param = trace1[ips]
            yl2 = logit(param["alpha"][ip] + param["beta"][ip] * (xl - xmean[ip]))
            x1 = xl[find_nearest(yl2, 0.5)]
            x2 = xl[find_nearest(yl2, 0.84)]
            jndps.append(x2 - x1)
        pdfpc = stats.kde.gaussian_kde(jndps)

        x2 = np.linspace(10, 109, 100)
        plt.plot(x2, pdfpc(x2), "k", alpha=0.5)
        plt.fill_between(x2, pdfpc(x2), 0, alpha=0.5, color="k")
        plt.axvline(jnd1, color="r", ls="--", lw=2)

        plt.axis([10, 105, -0.01, 0.125])
        plt.title(names[ip])

        plt.tight_layout();


    # ## 12.2 Psychophysical functions under contamination
    # 
    # Latent-mixture model approach  
    # $$ r_{ij} \sim \text{Binomial}(\theta_{ij},n_{ij})$$
    # 
    # $$   \theta_{ij} \sim
    # \begin{cases}
    # \frac{1}{1+\text{exp}\{-[\alpha_{i}+\beta_{i}(x_{ij}-\bar x_{i})]\}}  & \text{if $z_{ij} = 0$} \\
    # \pi_{ij}  & \text{if $z_{ij} = 1$}
    # \end{cases}  $$
    # 
    # $$ \Phi^{-1}(\phi_{i}) \sim \text{Gaussian}(\mu_{\phi},\sigma_{\phi})$$
    # $$ z_{ij} \sim \text{Bernoulli}(\phi_{i})$$
    # $$ \pi_{ij} \sim \text{Uniform}(0,1)$$
    # $$ \alpha_{i} \sim \text{Gaussian}(\mu_{\alpha},\sigma_{\alpha})$$
    # $$ \beta_{i} \sim \text{Gaussian}(\mu_{\beta},\sigma_{\beta})$$
    # $$ \mu_{\alpha},\mu_{\beta},\mu_{\phi} \sim \text{Gaussian}(0,0.001)$$
    # $$ \sigma_{\alpha},\sigma_{\beta} \sim \text{Uniform}(0,1000)$$
    # $$ \sigma_{\phi} \sim \text{Uniform}(0,3)$$

    with pm.Model() as model2b:
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
        priorsamples_m2 = pm.sample_prior_predictive()


    Phi(priorsamples_m2['phii'].mean(axis=0))


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

    az.plot_trace(trace2b, var_names=["alpha", "beta"], compact=True);


    # Now, let's use the ADVI result from above to initialize our original model without reparameterization of $z_{ij}$

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


    model2b.free_RVs


    model2b_.free_RVs


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


    # Psychophysical functions corresponding to expected posterior parameter values, using the model including a contaminant process, for each of the 8 subjects. Square markers representing data are colored to represent how certain they are to be generated by the psychophysical process (lighter) or the contaminant process (darker).

    trace2 = trace2b_
    # get MAP estimate
    tmp = az.summary(trace2, var_names=["alpha", "beta"])
    tmp2 = az.summary(trace2, var_names=["zij"])

    alphaMAP2 = tmp["mean"][np.arange(nsubjs)]
    betaMAP2 = tmp["mean"][np.arange(nsubjs) + nsubjs]


    # reproduce figure 12.6
    fig = plt.figure(figsize=(16, 8))
    fig.text(0.5, -0.02, "Test Interval (ms)", ha="center", fontsize=20)
    fig.text(
        -0.02,
        0.5,
        "Proportion of Long Responses",
        va="center",
        rotation="vertical",
        fontsize=20,
    )
    gs = gridspec.GridSpec(3, 4)

    for ip in np.arange(nsubjs):
        ax = plt.subplot(gs[ip])
        xp = np.array(x.iloc[ip, :])
        yp = np.array(rprop.iloc[ip, :])
        v1 = np.asarray(tmp2["mean"][sbjid == ip])
        ax.scatter(xp, yp, marker="s", alpha=0.5)

        xl = np.linspace(190, 410, 100)
        yl = logit(alphaMAP2[ip] + betaMAP2[ip] * (xl - xmean[ip]))
        yl2 = logit(alphaMAP[ip] + betaMAP[ip] * (xl - xmean[ip]))
        x1 = xl[find_nearest(yl, 0.5)]
        x2 = xl[find_nearest(yl, 0.84)]

        plt.plot(xl, yl, "k", linewidth=2)
        plt.plot(xl, yl2, "k", linestyle="--", linewidth=2)
        plt.plot([x1, x1], [-0.1, 0.5], color="k", linestyle="--", linewidth=1)
        plt.plot([190, x1], [0.5, 0.5], color="k", linestyle="--", linewidth=1)
        plt.plot([x2, x2], [-0.1, 0.84], color="k", linestyle="--", linewidth=1)
        plt.plot([190, x2], [0.84, 0.84], color="k", linestyle="--", linewidth=1)

        plt.axis([190, 410, -0.1, 1.1])
        plt.yticks((0, 0.5, 0.84, 1))
        #plt.title("Subject %s" % (ip + 1))
        plt.title(names[ip])

    plt.tight_layout();


    # reproduce figure 12.7
    fig = plt.figure(figsize=(16, 8))
    fig.text(0.5, -0.02, "JND (ms)", ha="center", fontsize=20)
    fig.text(-0.02, 0.5, "Posterior Density", va="center", rotation="vertical", fontsize=20)
    gs = gridspec.GridSpec(3, 4)

    ppcsamples = 200

    for ip in np.arange(nsubjs):
        ax = plt.subplot(gs[ip])

        xl = np.linspace(190, 410, 200)

        yl = logit(alphaMAP[ip] + betaMAP[ip] * (xl - xmean[ip]))
        x1 = xl[find_nearest(yl, 0.5)]
        x2 = xl[find_nearest(yl, 0.84)]
        jnd1 = x2 - x1

        yl2 = logit(alphaMAP2[ip] + betaMAP2[ip] * (xl - xmean[ip]))
        x12 = xl[find_nearest(yl2, 0.5)]
        x22 = xl[find_nearest(yl2, 0.84)]
        jnd2 = x22 - x12

        # Posterior sample
        jndps = []
        jndps2 = []
        for ips in np.random.randint(0, 1e3, ppcsamples):
            param = trace1[ips]
            yl2 = logit(param["alpha"][ip] + param["beta"][ip] * (xl - xmean[ip]))
            x1 = xl[find_nearest(yl2, 0.5)]
            x2 = xl[find_nearest(yl2, 0.84)]
            jndps.append(x2 - x1)

            param = trace2[ips]
            yl2 = logit(param["alpha"][ip] + param["beta"][ip] * (xl - xmean[ip]))
            x1 = xl[find_nearest(yl2, 0.5)]
            x2 = xl[find_nearest(yl2, 0.84)]
            jndps2.append(x2 - x1)

        x2 = np.linspace(10, 109, 100)
        pdfpc = stats.kde.gaussian_kde(jndps)
        plt.plot(x2, pdfpc(x2), "k", alpha=0.5)
        plt.fill_between(x2, pdfpc(x2), 0, alpha=0.5, color="k")
        plt.axvline(jnd1, color="r", ls="--", lw=2)

        pdfpc2 = stats.kde.gaussian_kde(jndps2)
        plt.plot(x2, pdfpc2(x2), "k", alpha=0.25)
        plt.fill_between(x2, pdfpc2(x2), 0, alpha=0.25, color="k")
        plt.axvline(jnd2, color="g", ls="-", lw=2)

        plt.axis([10, 105, -0.01, 0.125])
        plt.title("Subject %s" % (ip + 1))
        plt.title(names[ip])

    plt.tight_layout()
    plt.show()


    get_ipython().run_line_magic('load_ext', 'watermark')
    get_ipython().run_line_magic('watermark', '-n -u -v -iv -w')

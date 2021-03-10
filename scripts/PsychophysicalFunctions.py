#!/usr/bin/env python
# coding: utf-8

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['savefig.bbox'] = 'tight'

from math import ceil

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


def tPhi(x):
    # probit transform
    return 0.5 + 0.5 * pm.math.erf(x / pm.math.sqrt(2))


def tlogit(x):
    return 1 / (1 + tt.exp(-x))


def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx


def prepare_data(x, n, r):
    xij_tmp = x.values
    nij_tmp = n.values
    rij_tmp = r.values
    tmp, nstim2 = np.shape(xij_tmp)
    xmean = x.mean(axis=1)
    nsubjs = len(r)

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
    return xij, nij, rij, xvect, xmean, sbjid, nsubjs


if __name__ == '__main__':
    x, n, r, rprop, names = load_data()
    xij, nij, rij, xvect, xmean, sbjid, nsubjs = prepare_data(x, n, r)

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


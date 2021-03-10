from PsychophysicalFunctions import *
from model1 import *

x, n, r, rprop, names = load_data()
xij, nij, rij, xvect, xmean, sbjid, nsubjs = prepare_data(x, n, r)

with model1:
    trace1 = pm.load_trace('intermediate/trace_model1.tr')
    ppc = pm.sample_posterior_predictive(trace1, samples=5000, var_names=["alpha", "beta"])

alphaPPC = ppc["alpha"].mean(axis=1)
betaPPC = ppc["beta"].mean(axis=1)

alphaMAP = trace1['alpha'].mean(axis=0)
betaMAP = trace1['beta'].mean(axis=0)

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
plt.savefig('figures/posterior_jnd.png')
plt.close()

from PsychophysicalFunctions import *
from model2 import *
from model1 import *

x, n, r, rprop, names = load_data()
xij, nij, rij, xvect, xmean, sbjid, nsubjs = prepare_data(x, n, r)

with model1:
    trace1 = pm.load_trace('intermediate/trace_model1.tr')

alphaMAP = trace1['alpha'].mean(axis=0)
betaMAP = trace1['beta'].mean(axis=0)

with model2b_:
    trace2 = pm.load_trace('intermediate/model2.tr')
# get MAP estimate
tmp = az.summary(trace2, var_names=["alpha", "beta"])
tmp2 = az.summary(trace2, var_names=["zij"])

alphaMAP2 = tmp["mean"][np.arange(nsubjs)]
betaMAP2 = tmp["mean"][np.arange(nsubjs) + nsubjs]
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
plt.savefig('figures/model2_jnd.png')
plt.close()

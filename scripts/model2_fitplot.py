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
gs = gridspec.GridSpec(ceil(nsubjs/4), 4)

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
plt.savefig('figures/model2_fit.png')
plt.close()

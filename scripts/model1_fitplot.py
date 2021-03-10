from PsychophysicalFunctions import *
from model1 import *

x, n, r, rprop, names = load_data()
xij, nij, rij, xvect, xmean, sbjid, nsubjs = prepare_data(x, n, r)
with model1:
    trace1 = pm.load_trace('intermediate/trace_model1.tr')
print('here')

# get MAP estimate
# tmp = az.summary(trace1, var_names=["alpha", "beta"])
# alphaMAP = tmp["mean"][np.arange(nsubjs)]
# betaMAP = tmp["mean"][np.arange(nsubjs) + nsubjs]
alphaMAP = trace1['alpha'].mean(axis=0)
betaMAP = trace1['beta'].mean(axis=0)

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
plt.savefig('figures/model1_fit.png')
plt.close()

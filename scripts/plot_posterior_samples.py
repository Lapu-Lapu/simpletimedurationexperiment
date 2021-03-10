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
gs = gridspec.GridSpec(ceil(nsubjs/4), 4)

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
        # plt.plot(xl, yl3, "y", linewidth=2, alpha=0.05) # plot extraindividual posterior

    plt.plot(xl, yl, "r", linewidth=2)

    plt.axis([190, 410, -0.1, 1.1])
    plt.yticks((0, 0.5, 0.84, 1))
    plt.title("Subject %s" % (ip + 1))
    plt.title(names[ip])

plt.tight_layout();
plt.savefig('figures/posterior_samples.png')
plt.close()

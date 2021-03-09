#from PsychophysicalFunctions import *
from model1 import *

x, n, r, rprop, names = load_data()
xij, nij, rij, xvect, xmean, sbjid, nsubjs = prepare_data(x, n, r)

with model1:
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
plt.savefig('figures/model1_prior_checks.png')
plt.close()

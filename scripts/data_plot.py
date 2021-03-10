from PsychophysicalFunctions import *

x, n, r, rprop, names = load_data()
xmean = x.mean(axis=1)
nsubjs = len(r)

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
#fig.suptitle("Proportion of long responses as function of test durations.")
gs = gridspec.GridSpec(ceil(nsubjs/4), 4)

for ip in np.arange(nsubjs):
    ax = plt.subplot(gs[ip])
    xp = np.array(x.iloc[ip, :])
    yp = np.array(rprop.iloc[ip, :])
    ax.scatter(xp, yp, marker="s", alpha=0.5)
    plt.axis([190, 410, -0.1, 1.1])
    plt.yticks((0, 0.5, 0.84, 1))
    #plt.title("Subject %s" % (nsubjs))
    plt.title(names[ip])

plt.tight_layout();
plt.savefig('figures/data_plot.png', bbox_inches='tight')
plt.close()

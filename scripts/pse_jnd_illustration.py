from PsychophysicalFunctions import *

x = np.linspace(-3.75, 3.75, 100)
fig, ax = plt.subplots(figsize=(9, 6))
x1 = invlogit(0.5)
x2 = invlogit(0.84)

plt.plot(x, logit(x), "k", linewidth=2)
plt.plot([x1, x1], [0, 0.5], color="k", linestyle="--", linewidth=1)
plt.plot([-3.75, x1], [0.5, 0.5], color="k", linestyle="--", linewidth=1)
plt.plot([x2, x2], [0, 0.84], color="k", linestyle="--", linewidth=1)
plt.plot([-3.75, x2], [0.84, 0.84], color="k", linestyle="--", linewidth=1)

plt.scatter(x1, 0.5, c="k", s=75)
plt.text(x1 + 0.5, 0.5 - 0.02, "PSE", horizontalalignment="center", fontsize=20)
plt.plot([x1, x2], [0.5 / 2 + 0.06, 0.5 / 2 + 0.06], color="k", linewidth=1)
plt.text((x1 + x2) / 2, 0.5 / 2, "JND", horizontalalignment="center", fontsize=20)

ax.set_xticks(())
ax.set_yticks((0, 0.5, 0.84, 1))
ax.set_yticklabels(("0", "0.5", "0.84", "1"), fontsize=12)
plt.xlim(-3.75, 3.75)
plt.ylim(0, 1)
plt.xlabel("Stimulus Intensity", fontsize=15)
plt.ylabel("Respone Probability", fontsize=15);
plt.savefig('figures/pse_jnd_illustration.png')
plt.close()

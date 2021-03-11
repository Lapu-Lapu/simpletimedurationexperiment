all: talk/210310_leewagenmakers_psych.pdf

illustrations = figures/data_plot.png figures/Binomial_Example.png figures/pse_jnd_illustration.png

model1_plots = figures/model1_fit.png figures/posterior_samples.png figures/posterior_jnd.png
model1: ${model1_plots}

model2_plots = figures/model2_fit.png figures/model2_jnd.png
model2: ${model2_plots}

analysis/data_x_c.txt: analysis/names.txt analysis/files.txt
	python analysis/read_data.py

# talk/210310_leewagenmakers_psych.pdf: talk/210310_leewagenmakers_psych.md figures/*
# talk/210310_leewagenmakers_psych.pdf: talk/210310_leewagenmakers_psych.md ${illustrations} ${model1_plots}
talk/210310_leewagenmakers_psych.pdf: talk/210310_leewagenmakers_psych.md ${illustrations} ${model1_plots} ${model2_plots}
	pandoc -t beamer -s talk/210310_leewagenmakers_psych.md -o talk/210310_leewagenmakers_psych.pdf

figures/data_plot.png: analysis/data_x_c.txt
	python scripts/data_plot.py

figures/Binomial_Example.png:
	python scripts/binomial_plot.py

figures/pse_jnd_illustration.png:
	python scripts/pse_jnd_illustration.py

# Plain Model:

intermediate/trace_model1.tr: scripts/model1.py analysis/data_x_c.txt
	python scripts/model1_inference.py

figures/model1_fit.png: intermediate/trace_model1.tr
	python scripts/model1_fitplot.py

figures/posterior_samples.png: intermediate/trace_model1.tr
	python scripts/plot_posterior_samples.py

figures/posterior_jnd.png: intermediate/trace_model1.tr
	python scripts/plot_posterior_jnd.py

# Contamination Model:

intermediate/traceplot_model2.png: scripts/model2.py analysis/names.txt analysis/files.txt
	python scripts/model2_inference.py

figures/model2_fit.png: intermediate/traceplot_model2.png intermediate/trace_model1.tr
	python scripts/model2_fitplot.py

figures/model2_jnd.png: intermediate/traceplot_model2.png intermediate/trace_model1.tr
	python scripts/model2_jnd.py

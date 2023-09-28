# Simple Time Duration Experiment

Time duration experiment to illustrate inference of psychophysical functions using MCMC (using pymc3).

The experiment is implemented in javascript using jsPsych to get data for the analysis described in "Bayesian Cognitive Modeling" by Lee and Wagenmakers.
The Bayesian Analysis is based on an implementation by junpenglao (https://github.com/junpenglao).

## How to use

A Makefile is provided, run `make all` if all requirements are fullfilled. See below for details.

Get data: available on request.

Write files for pymc notebook:
- `python analysis/read_data.py`

Convert markdown to beamer presentation:
- `pandoc -t beamer -s talk/210310_leewagenmakers_psych.md -o talk/210310_leewagenmakers_psych.pdf`

Use `analysis/names.txt` to specify the data to be processed.

Plot data:
- `python scripts/data_plot.py`

Plot illustrations:
- `python scripts/binomial_plot.py`
- `python scripts/pse_jnd_illustration.py`

Plain Model:
- `python scripts/model1_inference.py`
- `python scripts/model1_fitplot.py`
- `python scripts/plot_posterior_samples.py`
- `python scripts/plot_posterior_jnd.py`

Contamination Model:
- `python scripts/model2_inference.py`
- `python scripts/model2_fitplot.py`
- `python scripts/model2_jnd.py`

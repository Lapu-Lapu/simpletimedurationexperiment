---
title: Psychometric Functions
subtitle: Chapter 12 from Bayesian Cognitive Modeling (Lee, Wagenmakers)
author: Benjamin Knopp
date: 2021/03/10
code-block-font-size: \tiny
...

# What is psychophysics?

## Psychophysics measures sensitivity to stimuli

- Physical Stimulus $\rightarrow$ Psychological Response
- 2-alterative forced choice tasks:
    - In each trial: 
        1. constant duration beep (300ms)
        2. varying duration beep
        3. second beep shorter or longer?
    - if duration is perceived as equal, probability of responses is equal

## Subjective equality and sensitivity

Beep Duration $\rightarrow$ Perceived Duration

PSE
: Point of Subjective Equality

JND
: Just Noticable Difference

![](figures/pse_jnd_illustration.png){width=70%}

## Proportion of “long” responses as a function of test interval duration.

![](figures/data_plot.png)

# Psychophysical Functions

## Psychological model of data generation

::: columns

:::{.column width="60%"}
<!-- \begin{align} -->
<!-- \Theta_{ij} = \frac{1}{1+\exp\left(-(\alpha_i + \beta_i(x_{ij} - \bar x_i))\right)}\nonumber -->
<!-- \end{align} -->

![](figures/model.png){width=100%}
:::

:::{.column width="40%"}
![](figures/Binomial_Example.png){width=100%}

![](figures/pse_jnd_illustration.png){width=100%}
:::
:::

## While my PYMC3 Gently Samples

![](figures/pymc3model.png){width=70%}

## Estimated PSE/JND of subjects

![](figures/model1_fit.png)

## Exercise 12.1.1

What do you think is the function of the thetalim construction
in the WinBUGS script?

![](figures/winbugs.png){width=70%}

## Exercise 12.1.2

The sigmoid curves in Figure 12.4 are single lines derived from
point estimates. How can you visualize the uncertainty in the psychometric
function?

![](figures/model1_fit.png)

## Exercise 12.1.2: Answer

The sigmoid curves in Figure 12.4 are single lines derived from
point estimates. How can you visualize the uncertainty in the psychometric
function?

![](figures/posterior_samples.png)


## Exercise 12.1.3

The figure below shows the PSE for each subject. Compare subject 2
with subject 8. How do they differ in their perception of the intervals?

![](figures/model1_fit.png)

## Exercise 12.1.4

In the plot below we have plotted point estimates for JND.

- Infer posterior distribution for JND!

![](figures/model1_fit.png)

## Exercise 12.1.4: Answer
- Interpret the results: Which subjects are better
at perceiving differences in time, and how certain are your conclusions?

![](figures/posterior_jnd.png)

## Exercise 12.1.5

Are all data points close to the sigmoid curve? How do you think
possible outliers would influence the function, and the inferred JND?

![](figures/posterior_samples.png)

# Psychological functions under contamination

## Psychological model of data generation with contamination

![](figures/contamination_model.png){width=70%}

## Cleaner estimation of PSE/JND

![](figures/model2_fit.png)

## Effect of accounting for contamination on posterior JND

![](figures/model2_jnd.png)

## Exercise 12.2.1

How did the inclusion of the contaminant process change the
inference for the psychophysical functions, and the key JND and PSE properties?

## Summary 

::: columns
::: column
- 2AFC paradigm useful for connecting physical stimuli with psychological processes
- Logistic regression model estimates:
    - Point of Subjective Equality
    - Just Noticable Difference
- Latent variables can be introduced to account for contamination
:::
::: column

- junpenglao provided pymc3 implementation $\rightarrow$ more fun, less stress!

![](figures/junpenglao.png){width=90%}
:::
:::

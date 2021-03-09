---
title: Psychometric Functions
author: Benjamin Knopp
date: 2021/03/10
...

# What is psychophysics?

## Psychophysics

- Physical Stimulus $\rightarrow$ Psychological Response
- Problem: Quantify psychological processes.
- One Solution: 2-alterative forced choice tasks.
    - Example:
        - In each trial: 
        - two beeps, first constant duration, second varying
        - participants have to choose which beep was longer
        - if duration is perceived as equal, probability of responses is equal

## Psychophysics: PSE and JND

Beep Duration $\rightarrow$ Perceived Duration

PSE
: Point of Subjective Equality

JND
: Just Noticable Difference

![](figures/pse_jnd_illustration.png){width=70%}

## Data

Proportion of “long” responses as a function of test interval duration.

![](figures/data_plot.png)

# Psychophysical Functions

## Psychophysical Functions: Model

::: columns

::: column
\begin{align}
\Theta_{ij} = \frac{1}{1+\exp\left(-(\alpha_i + \beta_i(x_{ij} - \bar x_i))\right)}
\end{align}
:::

::: column
![](figures/Binomial_Example.png){width=90%}
:::
:::

![](figures/model.png){width=70%}

## Result: Logistic Regression

![](output_15_0.png)

## Exercise 12.1.1

What do you think is the function of the thetalim construction
in the WinBUGS script?

![](winbugs.png){width=70%}

## Exercise 12.1.1: Answer

![](winbugs.png){width=70%}

## Exercise 12.1.2

The sigmoid curves in Figure 12.4 are single lines derived from
point estimates. How can you visualize the uncertainty in the psychometric
function?

![](output_15_0.png)

## Exercise 12.1.2: Answer

![](output_17_0.png)


## Exercise 12.1.3

The figure below shows the PSE for each subject. Compare subject 2
with subject 8. How do they differ in their perception of the intervals?

![](output_15_0.png)

## Exercise 12.1.4

One of the aims of the analysis is to use the psychometric function
to infer the JND. In Figure 12.4 the JND is indicated by the difference on
the x-axis between the dashed lines corresponding to the 50% and 84% points
on the y-axis. The JNDs from Figure 12.4 are point estimates. Plot posterior
distributions for the JND, and interpret the results. Which subjects are better
at perceiving differences in time, and how certain are your conclusions?

## Exercise 12.1.4: Answer

![png](output_18_0.png)

## Exercise 12.1.5

Look closely at the data points that are used to fit the psychome-
tric functions. Are all of them close to the sigmoid curve? How do you think
possible outliers would influence the function, and the inferred JND?

# Psychophysical Functions with Contamination

## Model

![](contamination_model.png){width=70%}

## Result: Regression

![](output_30_0.png)

## Result: Posterior JND

![](output_31_0.png)

## Exercise 12.2.1

How did the inclusion of the contaminant process change the
inference for the psychophysical functions, and the key JND and PSE properties?

## Summary

- 2AFC paradigm useful for connecting physical stimuli with psychological processes
- Logistic regression model estimates:
    - Point of Subjective Equality
    - Just Noticable Difference
- pymc3 makes Bayesian analysis easy and fun!
- junpenglao provided pymc3 implementation $\rightarrow$ more fun!

![](junpenglao.png){width=30%}

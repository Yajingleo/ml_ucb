## Generalized ML UCB 

### Overview
Generalized ML UCB is based on the learning curve to establish the UCB score. The exploration 
bonus is based on a generalized concentration inequality, which is known as the cumulant 
generating function (CGF) bounds. See https://www.stat.berkeley.edu/~bartlett/courses/2014fall-cs294stat260/lectures/bandit-ucb-notes.pdf

#### ML-UCB model & workflow
1. ML-Model Training
2. Linear curve estimation: Use linear regression on log transformation to estimate MSE convergence order: $S$
3. Calculate UCB scores: A generalized ML-UCB formula is provided in the paper:
   $Prediction(arm)+\sqrt{\frac{\ln(t)^{1/S}}{N_{arm}(t)}}\cdot\sigma(rewards)$
4. Select arm
5. Repeat

#### Workspace Organization
1. paper/: pdf latex
2. colab/: training & simulation results

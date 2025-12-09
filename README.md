Generalized ML UCB 

Generalized ML UCB is based on the learning curve to establish the UCB score. The exploration 
bonus is based on a generalized concentration inequality, which is known as the cumulant 
generating function (CGF) bounds. See https://www.stat.berkeley.edu/~bartlett/courses/2014fall-cs294stat260/lectures/bandit-ucb-notes.pdf

The steps is as follows:
1. Calibrate the learning curve of training loss
2. Use linear regression on log transformation to estimate CGF bounds
3. Then, a generalized ML-UCB formula can be derived.

The workspace is organized as follows:
1. paper/: pdf latex
2. colab/: training & simulation results

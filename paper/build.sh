#!/bin/bash
# This script will work once pdflatex is available
pdflatex ml_ucb.tex
bibtex ml_ucb
pdflatex ml_ucb.tex
pdflatex ml_ucb.tex

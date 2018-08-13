#!/bin/bash
#$ -l h_rt=00:35:30
#$ -j y
#$ -l h_vmem=32g
#$ -cwd
#$ -R y
#$ -o /broad/finucanelab/ktashman/inrich_analyses/simulations/genotypes.1.log
#$ -t 1-22

source /broad/software/scripts/useuse
reuse -q UGER
reuse -q .anaconda-5.0.1

python scripts/fix_genotypes.py --bed-files /broad/finucanelab/ktashman/inrich_analyses/simulations/ukbb/UKB_null_50k_imputed_0 --chromosome ${SGE_TASK_ID}

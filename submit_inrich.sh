#!/bin/bash
#$ -l h_rt=14:59:30
#$ -l h_vmem=32g
#$ -j y
#$ -cwd
#$ -o /broad/finucanelab/ktashman/inrich_analyses/c1.3.out
#$ -m ea
#$ -M ktashman@broadinstitute.org

source /broad/software/scripts/useuse
reuse -q .anaconda-5.0.1

python /broad/finucanelab/ktashman/inrich_analyses/scripts/run_inrich.py --sumstats /broad/finucanelab/sumstats/dense/mental_NEUROTICISM.sumstats.gz --assoc-snps /broad/finucanelab/ktashman/inrich_analyses/run_inrich/mental_NEUROTICISM.assoc_snps --geneset-list /broad/finucanelab/ktashman/inrich_genesets/c1.all.v3.0.entrez.msig.set

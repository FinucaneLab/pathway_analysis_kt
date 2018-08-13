#!/bin/bash
#$ -l h_rt=6:10:30
#$ -j y
#$ -l h_vmem=8g
#$ -cwd
#$ -o /broad/finucanelab/ktashman/inrich_analyses/simulations/download.log


source /broad/software/scripts/useuse
reuse -q .anaconda-5.0.1
reuse -q .python-2.7.14-sqlite3-rtrees
reuse -q .google-cloud-sdk 
gsutil -m cp gs://inrich_analyses/simulations/UKB_null_50k_imputed_0.fam /broad/finucanelab/ktashman/inrich_analyses/simulations/ukbb/


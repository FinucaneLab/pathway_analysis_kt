#!/bin/bash
#$ -l h_rt=3:10:30
#$ -j y
#$ -l h_vmem=16g
#$ -cwd
#$ -R y
#$ -o /broad/finucanelab/ktashman/inrich_analyses/simulations/pipeline.3.log
#$ -t 2-100

source /broad/software/scripts/useuse
reuse -q UGER
reuse -q .anaconda-5.0.1

/broad/software/free/Linux/redhat_6_x86_64/pkgs/anaconda_5.0.1/bin/python /broad/finucanelab/ktashman/inrich_analyses/simulations/scripts/run_null_pipeline.py --json /broad/finucanelab/ktashman/inrich_analyses/simulations/json/simulations_null.json --simulation-number ${SGE_TASK_ID}

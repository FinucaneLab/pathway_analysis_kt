#!/bin/bash
#$ -l h_rt=6:10:30
#$ -j y
#$ -l h_vmem=16g
#$ -cwd
#$ -o /broad/finucanelab/ktashman/inrich_analyses/simulations/pipeline_causal.2.log
#$ -t 1-100

source /broad/software/scripts/useuse
reuse -q .anaconda-5.0.1

/broad/software/free/Linux/redhat_6_x86_64/pkgs/anaconda_5.0.1/bin/python /broad/finucanelab/ktashman/inrich_analyses/simulations/scripts/run_causal_pipeline.py --json /broad/finucanelab/ktashman/inrich_analyses/simulations/json/simulations_causal5_tau100.json --simulation-number ${SGE_TASK_ID} --starting-folder /broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_tau100

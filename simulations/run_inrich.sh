#!/bin/bash
#$ -l h_rt=8:10:30
#$ -j y
#$ -l h_vmem=32g
#$ -cwd
#$ -o /broad/finucanelab/ktashman/inrich_analyses/simulations/inrich.causal.5tau100.log
#$ -R y
#$ -t 1-100

source /broad/software/scripts/useuse
reuse -q .anaconda-5.0.1
reuse -q Python-2.7

json=$1
sim=$((${SGE_TASK_ID}-1))
geno_sim=$(/psych/genetics_data/ktashman/ldsc_work/imprinting/scripts/./json_lookup.sh $json num_genotype_sims)
sumstats_files=$(/psych/genetics_data/ktashman/ldsc_work/imprinting/scripts/./json_lookup.sh $json sumstats_files)sim0_${sim}.sumstats.pruned
assoc_snp_files=$(/psych/genetics_data/ktashman/ldsc_work/imprinting/scripts/./json_lookup.sh $json assoc_snp_files)sim0_${sim}.sumstats.pruned.assoc_snp
full_geneset_list=$(/psych/genetics_data/ktashman/ldsc_work/imprinting/scripts/./json_lookup.sh $json full_geneset_list)
bed_files=$(/psych/genetics_data/ktashman/ldsc_work/imprinting/scripts/./json_lookup.sh $json bed_files)0
inrich_results=$(/psych/genetics_data/ktashman/ldsc_work/imprinting/scripts/./json_lookup.sh $json inrich_results)
intervals=$(/psych/genetics_data/ktashman/ldsc_work/imprinting/scripts/./json_lookup.sh $json intervals)
python /broad/finucanelab/ktashman/inrich_analyses/scripts/run_inrich.py --sumstats $sumstats_files \
                                --assoc-snps $assoc_snp_files \
                                --geneset-list $full_geneset_list \
                                --intervals $intervals \
                                --inrich-results $inrich_results 

python scripts/prep_for_simulations.py --sim-unique-genos 0 \
                                       --bed-files /broad/finucanelab/ktashman/inrich_analyses/simulations/ukbb/UKB_null_50k_imputed_ --h2g .8   --varbeta-path /broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_sparse/varbeta_files_causal/UKB_null_50k_imputed_ \
                                       --pathway /broad/finucanelab/ktashman/inrich_analyses/inrich_LDSC_genesets/inrich.c1.all.v3.0.entrez.msig.ST_IL_13_PATHWAY.GeneSet \
                                       --multiple 100 \
                                       --windowsize 100000 \
                                       --num-sims 1 \
                                       --sim-snps /broad/finucanelab/ktashman/inrich_analyses/simulations/ukbb/sim.snps \
                                       --sparse

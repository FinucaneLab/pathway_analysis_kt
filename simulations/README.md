### This is the simulation framework I've created to assess the statistical validity of my GSE method. This framework uses a mix of modified versions of Ran Cui's code along with custom scripts specific to my project.


#### Step 1:

Run this script once to remove duplicate SNPs and update rsids from the output of Hail 0.1:

```qsub scripts/submit_fix_genotypes.sh```

#### Step 2a:

Make a directory for the newest simulation case you want to run:

Example:

```mkdir causal5_tau100/```

#### Step 2b:

Make a json file modeled as such:

```
{
        "bed_files":"/broad/finucanelab/ktashman/inrich_analyses/simulations/ukbb/UKB_null_50k_imputed_",
        "varbeta_files":"/broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_tau100/varbeta_files_causal/UKB_null_50k_imputed_",
        "varbeta_folder":"/broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_tau100/varbeta_files_causal/",
        "score_folder":"/broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_tau100/score_files_causal/",
        "plink_profile_folder": "/broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_tau100/plink_profile_files_causal/",
        "h2g_file":"/broad/finucanelab/ktashman/inrich_analyses/simulations/h2g_files/h2g",
        "pheno_folder":"/broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_tau100/pheno_files_causal/",
        "qassoc_folder":"/broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_tau100/qassoc_files_causal/",
        "sumstats_files": "/broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_tau100/sumstats_files_causal/",
        "assoc_snp_files":"/broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_tau100/assoc_snp_files_causal/",
        "full_geneset_list":"/broad/finucanelab/ktashman/inrich_genesets/c1.all.v3.0.entrez.msig.set",
        "unique_geneset_list":"/broad/finucanelab/ktashman/inrich_genesets/c1.all.v3.unique",
        "ldsc_files":"/broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_tau100/ldsc_simulations_exclude_causal/",
        "meta_analysis_files":"/broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_tau100/meta_analysis_files_causal/",
        "inrich_results":"/broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_tau100/inrich_simulations_causal/",
        "num_genotype_sims":1,
        "num_sims":100,
        "intervals":"/broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_tau100/intervals_causal/",
        "pathway":"/broad/finucanelab/ktashman/inrich_analyses/inrich_LDSC_genesets/inrich.c1.all.v3.0.entrez.msig.ST_IL_13_PATHWAY.GeneSet",
        "multiple":100,
        "windowsize":100000,
        "sim_snps":"/broad/finucanelab/ktashman/inrich_analyses/simulations/ukbb/sim.snps"
}
```

#### Step 3:

Submit task array to run pipeline that creates varbeta files, the score files,calculates the phenotypes and runs the association/formats results:

```qsub scripts/submit_causal5_pipeline.sh```

This submit file changes each time I want to run a different analysis because I change the python script in it, the json file I'm using and the starting folder.

An example of this script:

```
#!/bin/bash
#$ -l h_rt=6:10:30
#$ -j y
#$ -l h_vmem=16g
#$ -cwd
#$ -o /broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_sparse_tau100/pipeline.log
#$ -t 1-100

source /broad/software/scripts/useuse
reuse -q .anaconda-5.0.1

/broad/software/free/Linux/redhat_6_x86_64/pkgs/anaconda_5.0.1/bin/python 
/broad/finucanelab/ktashman/inrich_analyses/simulations/scripts/run_causal_pipeline.py 
--json /broad/finucanelab/ktashman/inrich_analyses/simulations/json/simulations_causal5_tau100.json 
--simulation-number ${SGE_TASK_ID} 
--starting-folder /broad/finucanelab/ktashman/inrich_analyses/simulations/causal5_tau100
```

Options for pipelines to run:
   * run_null_pipeline.py
   * run_causal_pipeline.py
   * run_causal_sparse_pipeline.py

These scripts call other scripts such as `prep_for_simulations.py`, `sim_pheno.py`, `compute_sumstats.py` and `prune_sumstats.py`

#### Step 4: 

Run the Inrich analysis:

```qsub scripts/run_inrich.sh json/simulations_causal5_tau100.json```

#### Step 5:

Copy the `*.sumstats.pruned` files and the independent genomic intervals from the Inrich analysis to local computer.

#### Step 6:

Submit S-LDSC using dsub, requires making a new task file each time:

```python make_tsv.py --num-sims 100```

**I should really add arguments to this.** 

#### Step 7:

Copy S-LDSC results to cluster, munge results:

```python run_final_step.py --json json/simulations_causal5_tau100.json```

#### Optional:

Look at results using jupyter notebook and the ipynb scripts I have to plot p-value distributions and calculate FDRs.
Quickly realizing I need to add functions to do the plotting/descriptions, have begun adding that to my ipynbs.

#### **Critiques and Solutions** :

1. Having to make a directory each time for a new analysis:
      * **Solution** : Add a flag to pipeline script that checks if the path already exists and if not creates the base folder for the analysis and the rest of the subfolders

2. The json file is clunky and confusing because of the full paths:
      * **Solution** : Create an arg that is the base for the rest of the paths, this way the rest of the paths can just be the flag for the new directory plus the folder name
           - This might remove the need for a lot of the items in this json because once it has the base and the new directory name, the subfolders are the same each analysis

3. Should create one script for null,causal and causal_sparse simulations:
      * **Solution** : This requires adding "sparse" and "pathway" which are flags  for the `prep_for_simulations.py` script to the overall script, not sure what the best way to do this is, perhaps doing a join where it can be either a space or the command you want to add?

4. Should revert to local S-LDSC at some point so that I'm not jumping between the cluster and cloud:
      * **Solution** : just do it. (My priority is quite low on the cluster, might wait until Goosilon is ready)

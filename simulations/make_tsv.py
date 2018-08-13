import pandas as pd
import os
import argparse

def submission_script(num_sims):
    f = open(os.path.join('simulations_50k_causal50.tsv'),'w')
    for sim in range(num_sims):
        f.write("\t".join(['gs://inrich_analyses/ldcts_files/ldscores_sim0_pruned_100.tsv','gs://inrich_analyses/simulations/sumstats/ukbb_50k_causal50/sim0_'+str(sim)+'.sumstats.pruned','sim0_'+str(sim),'gs://singlecellldscore/entrez_control/','gs://inrich_analyses/simulations/exclude_files/ukbb_50k_causal50/sim0_'+str(sim)+'.sumstats.pruned.intervals','gs://inrich_analyses/simulations/simulations_results_exclude/ukbb_50k_causal50/'])+"\n")


def main(args):
    submission_script(args.num_sims)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates gene sets with annotations')
    parser.add_argument("--num-sims", type=int, help="path to unique genesets to run")
    main(parser.parse_args())

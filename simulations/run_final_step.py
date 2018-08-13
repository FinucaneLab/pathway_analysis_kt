import pandas as pd
import argparse
import os
import json
import subprocess

def run_munge(args,i,y):
    cmd="""python ../scripts/munge_results.py --geneset-list {0}
                                --in-path {1}
                                --out-path {2}
                                --inrich-path {3}
                                --ldsc-prefix {4}
				--inrich-prefix {5}""".format(args.unique_geneset_list,args.ldsc_files,
                                                        args.meta_analysis_files,args.inrich_results,
                                                        'sim'+str(i)+'_'+str(y)+'.sumstats.pruned.sim'+str(i)+'_'+str(y),'sim'+str(i)+'_'+str(y)+'.sumstats.pruned')

    p = subprocess.Popen(cmd.split(), shell=False)
    p.communicate()
    p.wait()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', help = 'json file for simulations')


    args = parser.parse_args()
    args_dict = vars(args)
    d = json.load(open(args.json))
    args_dict.update(d)

    for i in range(args.num_genotype_sims):
        for y in range(args.num_sims):
	    run_munge(args,i,y)

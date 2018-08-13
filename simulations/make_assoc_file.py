import pandas as pd
import numpy as np
import argparse
import os

def create_assoc(sumstats,unique_sim,num_sims):
    for sim in range(num_sims,num_sims+1):
        name = 'sim'+str(unique_sim)+'_'+str(sim)+'.sumstats'
        assoc_file = open(name+'.assoc_snp', "w")
        plink = pd.read_csv('/broad/finucanelab/1000G/1000G_EUR_Phase3/plink_files/plink.bim',delim_whitespace=True,names=['chr','SNP','cm','pos','a1','a2'])

def main(args):
    create_assoc(args.sumstats,args.sim_unique_genos,args.num_sims)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create assoc_snp files for inrich analysis')
    parser.add_argument("--sumstats", type=str, help="path to sumstats",required=True)
    parser.add_argument("--sim-unique-genos",type=int,help="The numer of simulations you have with unique genotypes")
    parser.add_argument('--num-sims',type=int)
    main(parser.parse_args())


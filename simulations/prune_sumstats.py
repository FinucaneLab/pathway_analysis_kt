import pandas as pd
import os
import argparse

def prune_ss(plink_files,ss,assoc_snp,sim_unique_genos,sim_num):
    print('Making correctly formatted summary statistics..')
    plink = pd.read_csv(plink_files,delim_whitespace=True,names=['chr','SNP','cm','pos','a1','a2'])
    sumstats = pd.read_csv(ss+'sim'+str(sim_unique_genos)+'_'+str(sim_num)+'.sumstats',delim_whitespace=True,header=0)
    merge = plink.merge(sumstats,how='inner',on='SNP')
    merge[['chr','pos']].to_csv(assoc_snp+'sim'+str(sim_unique_genos)+'_'+str(sim_num)+'.sumstats.pruned.assoc_snp',sep="\t",index=False,header=False)
    merge[['A1','A2','N','P','SNP','Z']].to_csv(ss+'sim'+str(sim_unique_genos)+'_'+str(sim_num)+'.sumstats.pruned',sep="\t",index=False,header=True)


def main(args):
    for sim in range(args.num_sims,args.num_sims+1):
        prune_ss(args.ref_snps,args.sumstats,args.assoc_snp_files,args.sim_unique_genos,sim)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Separate genotype plink files into chromosomes and generate chr specific varbeta files')
    parser.add_argument("--sumstats", type=str, help="path to sumstats",required=True)
    parser.add_argument("--assoc-snp-files", type=str, help="path to assoc snp files",required=True)
    parser.add_argument("--sim-unique-genos",type=int,help="The numer of simulations you have with unique genotypes")
    parser.add_argument('--num-sims',type=int)
    parser.add_argument("--ref-snps",type=str,help="Path to bim file with chr, pos and rsid to get assoc_snp file for inrich",default='/broad/finucanelab/1000G/1000G_EUR_Phase3/plink_files/plink.bim')
    main(parser.parse_args())

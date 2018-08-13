import pandas as pd
from subprocess import Popen,PIPE,call
import numpy as np
import argparse

def compute_ss_onesim(args):
    bed_files = args.bed_files
    pheno_file = args.pheno_file
    out_file = args.out_file
    for i in range(1,23):
        chrom = str(i)
        cmd = ['/home/unix/sripke/plink_src/plink_1.9_newest/plink','--bfile',bed_files+'.'+chrom,
            '--pheno',pheno_file,'--assoc','--allow-no-sex',
            '--out',out_file+'.'+chrom]
        print('executing command '+' '.join(cmd))
        call(' '.join(cmd),shell=True)
    return None

def compute_ss(args):
    bed_files = args.bed_files
    pheno_folder = args.pheno_folder
    out_folder = args.out_folder
    num_sims = args.num_sims
    for i in range(num_sims,num_sims+1):
        which_sim = str(i)
        cmd = ['python','scripts/compute_sumstats.py',
            '--compute-ss-onesim','--bed-files',bed_files,
            '--pheno-file',pheno_folder+'sim'+str(args.sim_unique_genos)+'_'+which_sim+'.phe',
            '--out-file',out_folder+'sim'+str(args.sim_unique_genos)+'_'+which_sim]
        call(' '.join(cmd),shell=True)
    return None

def format_ss_onesim(args):
    qassoc_files = args.qassoc_files
    bim_files = args.bim_files
    out_file = args.out_file
    formated_ss_df = pd.DataFrame(None,columns=['SNP','N','Z','A1','A2'])
    for i in range(1,23):
        chrom = str(i)
        qassoc_df = pd.read_csv(qassoc_files+chrom+'.qassoc',delim_whitespace=True)
        bim_df = pd.read_csv(bim_files+'.'+chrom+'.bim',delim_whitespace=True,header=None)
        bim_df.columns=['CHR','SNP','CM','N','A1','A2']
        chr_ss_df = pd.DataFrame(None,columns=['SNP','N','Z','A1','A2','P'])
        chr_ss_df[['SNP','N','Z','P']] = qassoc_df[['SNP','NMISS','T','P']]
        chr_ss_df[['A1','A2']] = bim_df[['A1','A2']]
        formated_ss_df = pd.concat([formated_ss_df,chr_ss_df])
    formated_ss_df.to_csv(out_file,index=False,sep='\t')
    return None

def format_ss(args):
    num_sims = args.num_sims
    qassoc_folder = args.qassoc_folder
    out_folder = args.out_folder
    bim_files = args.bim_files
    for i in range(num_sims,num_sims+1):
        which_sim = str(i)
        cmd = ['python','scripts/compute_sumstats.py',
            '--format-ss-onesim',
            '--bim-files',bim_files,
            '--out-file',out_folder+'sim'+str(args.sim_unique_genos)+'_'+which_sim+'.sumstats','--qassoc-files',qassoc_folder+'sim'+str(args.sim_unique_genos)+'_'+which_sim+'.']
        call(' '.join(cmd),shell=True)
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--compute-ss',action='store_true')
    parser.add_argument('--bed-files')
    parser.add_argument('--pheno-folder')
    parser.add_argument('--out-folder')
    parser.add_argument('--num-sims',type=int)
    parser.add_argument('--compute-ss-onesim',action='store_true')
    parser.add_argument('--pheno-file')
    parser.add_argument('--out-file')
    parser.add_argument('--sim-unique-genos',type=int)
    parser.add_argument('--format-ss-onesim',action='store_true')
    parser.add_argument('--qassoc-files')
    parser.add_argument('--bim-files')
    parser.add_argument('--format-ss',action='store_true')
    parser.add_argument('--qassoc-folder')
    args = parser.parse_args()

    if args.compute_ss:
        compute_ss(args)
    elif args.compute_ss_onesim:
        compute_ss_onesim(args)
    elif args.format_ss:
        format_ss(args)
    elif args.format_ss_onesim:
        format_ss_onesim(args)

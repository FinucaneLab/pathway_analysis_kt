import pandas as pd
import numpy as np
import os
from subprocess import Popen,PIPE,call
import argparse
import pdb

def make_score_files(args):
    varbeta_files = args.varbeta_files
    num_sims = args.num_sims
    bed_files = args.bed_files
    out_folder = args.out_folder
    for chrom in range(1,23):
        chrom = str(chrom)
        print('generating score files for chrom '+chrom)
        frq_df = pd.read_csv(bed_files+'.'+chrom+'.frq',delim_whitespace=True)
        # since the genotype is not standardized, we scale beta by the std of each SNP
        # the centering step is done when computing phenotype
        sigma = np.sqrt(2*frq_df['MAF']*(1-frq_df['MAF']))
        score_df = frq_df.copy().drop(['A2','MAF','NCHROBS'],1)
        for i in range(num_sims,num_sims+1):
	    print("Simulation number you are on: {0}".format(str(i)))
	    varbeta_df = pd.read_csv(varbeta_files+'_'+str(i)+'.'+chrom+'.varbeta',delim_whitespace=True)
            beta = np.random.normal(0,np.sqrt(varbeta_df['VARBETA']))
            print("length of betas: {0}".format(len(beta)))
	    print("length of sigma: {0}".format(len(sigma)))
	    scaled_beta = beta/sigma
            score_df['beta_scaled'] = scaled_beta
            score_df.drop_duplicates('SNP').to_csv(out_folder+'sim'+str(args.sim_unique_genos)+'_'+str(i)+'.'+chrom+'.score',index=False,sep='\t')
    return None

def get_plink_profiles(args):
    # use plink to compute the product of genotype and scaled beta
    score_folder = args.score_folder
    num_sims = args.num_sims
    out_folder = args.out_folder
    bed_files = args.bed_files
    sim_unique_genos = args.sim_unique_genos
    for which_sim in range(num_sims,num_sims+1):
        cmd = ['python','scripts/sim_pheno.py','--get-profile-onesim',
            '--which-sim',str(which_sim),'--score-folder',score_folder,
            '--out-folder',out_folder,'--bed-files',bed_files,'--sim-unique-genos',str(sim_unique_genos)]
        call(' '.join(cmd),shell=True)
    return None

def get_profile_onesim(args,which_sim,score_folder,out_folder,bed_files):
    print('computing profiles for simulation number '+str(which_sim))
    score_files = score_folder+'sim'+str(args.sim_unique_genos)+'_'+str(which_sim)+'.'
    out_files = out_folder+'sim'+str(args.sim_unique_genos)+'_'+str(which_sim)+'.'
    for chrom in range(1,23):
        chrom = str(chrom)
        cmd = ['/home/unix/sripke/plink_src/plink_1.9_newest/plink','--bfile',bed_files+'.'+chrom,
            '--score',score_files+chrom+'.score','2','sum','center','header',
            '--allow-no-sex',
            '--out',out_files+chrom]
        call(' '.join(cmd),shell=True)
    return None

def compute_pheno(args):
    profile_folder = args.profile_folder
    num_sims = args.num_sims
    h2g_file = args.h2g_file
    out_folder = args.out_folder
    bed_files = args.bed_files
    for which_sim in range(num_sims,num_sims+1):
        cmd = ['python','scripts/sim_pheno.py','--compute-pheno-onesim',
            '--profile-files',profile_folder+'sim'+str(args.sim_unique_genos)+'_'+str(which_sim)+'.',
            '--h2g-file',h2g_file,'--bed-files',bed_files,
            '--out-file',out_folder+'sim'+str(args.sim_unique_genos)+'_'+str(which_sim)+'.phe']
        call(' '.join(cmd),shell=True)
    return None

def compute_pheno_onesim(args):
    # sum all profile files for one simulation into a phenotype file
    # columns: FID, IID, PHENO
    # file extension: .phe
    profile_files = args.profile_files
    h2g_file = args.h2g_file
    out_file = args.out_file
    bed_files = args.bed_files
    fam_df = pd.read_csv(bed_files+'.1.fam',delim_whitespace=True,header=None)
    with open(h2g_file) as f:
        h2g = f.readline()
    h2g = float(h2g)
    # initialize phenotype dataframe
    phe_df = pd.DataFrame(None)
    phe_df['FID'] = fam_df[0]
    phe_df['IID'] = fam_df[1]
    phenotype = np.zeros(len(phe_df))
    for i in range(1,23):
        chrom = str(i)
        profile_df = pd.read_csv(profile_files+chrom+'.profile',delim_whitespace=True)
        phenotype += np.array(profile_df['SCORESUM'])
    phenotype += np.random.normal(0,np.sqrt(1-h2g),len(phe_df))
    phe_df['PHENO'] = phenotype
    phe_df.to_csv(out_file,index=False,sep='\t')
    return None
    

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--make-score-files',action='store_true')
    parser.add_argument('--varbeta-files')
    parser.add_argument('--num-sims',type=int)
    parser.add_argument('--bed-files')
    parser.add_argument('--out-folder')
    parser.add_argument('--get-plink-profiles',action='store_true')
    parser.add_argument('--score-folder')
    parser.add_argument('--get-profile-onesim',action='store_true')
    parser.add_argument('--which-sim',type=int)
    parser.add_argument('--sim-unique-genos',type=int)
    parser.add_argument('--compute-pheno',action='store_true')
    parser.add_argument('--compute-pheno-onesim',action='store_true')
    parser.add_argument('--profile-folder')
    parser.add_argument('--h2g-file')
    parser.add_argument('--profile-files')
    parser.add_argument('--out-file')
    args=parser.parse_args()

    if args.make_score_files:
        make_score_files(args)
    elif args.get_plink_profiles:
        get_plink_profiles(args)
    elif args.compute_pheno:
        compute_pheno(args)
    elif args.get_profile_onesim:
        get_profile_onesim(args,args.which_sim,args.score_folder,args.out_folder,args.bed_files)
    elif args.compute_pheno_onesim:
        compute_pheno_onesim(args)

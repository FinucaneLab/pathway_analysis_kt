from __future__ import division
import pandas as pd
import os
import argparse
import numpy as np
from pybedtools import BedTool
import subprocess

plink = "/home/unix/sripke/plink_src/plink_1.9_newest/plink"

def count_length(plink_files):
    n = 0    
    bimfile = plink_files+'.bim'
    for line in open(bimfile, "r"):
        n += 1
    return n

def make_varbetas(i,varbeta_path,n,chr_plink_file,total,h2g,sim_unique_genos,sim_snps,num_sims):
    print('Making varbeta files for chromsome '+str(i))
    plink_file = pd.read_csv(chr_plink_file+'.bim',delim_whitespace=True,names=['CHR','SNP','CM','POS','A1','A2'])
    all_snps = pd.read_csv(sim_snps,delim_whitespace=True,names=['chr_bp','SNP'])
    all_snps = all_snps.drop_duplicates('SNP')
    for sim in range(num_sims,num_sims+1):
        causal_snps = all_snps.sample(n=int(round(len(all_snps)/100,0)))
        causal = causal_snps.drop('chr_bp',axis=1)
	causal['VARBETA']=h2g/len(causal_snps)
	merge = plink_file.merge(causal,how='left',on='SNP')
	merge = merge.fillna(0)
	merge['VARBETA'].to_csv(varbeta_path+str(sim_unique_genos)+'_'+str(sim)+'.'+str(i)+'.varbeta',sep='\t',index=False,header=True)

def genesets_to_snps(args,chr_plink_file,pathway,gene_coord_file):
    gene_set =pd.read_csv(pathway,names=['ENTREZ'],sep='\t')
    all_genes = pd.read_csv(gene_coord_file, delim_whitespace = True)
    df = pd.merge(gene_set, all_genes, on = 'ENTREZ', how = 'inner')
    df['START'] = np.maximum(0, df['START'] - args.windowsize)
    df['END'] = df['END'] + args.windowsize
    iter_df = [['chr'+(str(x1)).lstrip('chr'), x2, x3] for (x1,x2,x3) in np.array(df[['CHR', 'START', 'END']])]
    genesetbed = BedTool(iter_df).sort().merge()
    df_bim = pd.read_csv(chr_plink_file+ '.bim',delim_whitespace=True, usecols = [0,1,2,3], names = ['CHR','SNP','CM','BP'])
    iter_bim = [['chr'+str(x1), x2, x2] for (x1, x2) in np.array(df_bim[['CHR', 'BP']])]
    bimbed = BedTool(iter_bim).sort()
    annotbed = bimbed.intersect(genesetbed)
    bp = [x.start for x in annotbed]
    df_caus = pd.DataFrame({'BP': bp, 'count':1})
    causal_snps = pd.merge(df_bim, df_caus, how='left', on='BP')
    causal_snps.fillna(0,inplace=True)
    num_causal_snps = sum(causal_snps['count'])
    return annotbed,df_bim,num_causal_snps

def make_varbetas_causal(i,varbeta_path,sim_unique_genos,multiple,tau,annotbed,df_bim,num_sims,chr_plink):
    for sim in range(num_sims,num_sims+1):
        print('Making causal varbeta files')
	bp = [x.start for x in annotbed]
        df_int = pd.DataFrame({'BP': bp, 'VARBETA':multiple*tau})
	df_annot = pd.merge(df_bim, df_int, how='left', on='BP')
        df_annot.fillna(tau, inplace=True)
	df_annot = df_annot.drop_duplicates('SNP')
        df_annot = df_annot[['VARBETA']].to_csv(varbeta_path+str(sim_unique_genos)+'_'+str(sim)+'.'+str(i)+'.varbeta',sep='\t',index=False,header=True)

def make_varbetas_causal_sparse_old(i,varbeta_path,sim_unique_genos,multiple,tau,annotbed,df_bim,num_sims,chr_plink,all_snps):
    all_snps = all_snps.drop_duplicates('SNP')
    for sim in range(num_sims,num_sims+1):
        print('Making causal varbeta files')
        bp = [x.start for x in annotbed]
	causal_snps = all_snps.sample(n=int(round(len(all_snps)/100,0)))
        causal = causal_snps.drop('chr_bp',axis=1)
        causal = causal.merge(df_bim,how='inner',on='SNP')
	causal['VARBETA']=tau
        df_int = pd.DataFrame({'BP': bp, 'VARBETA':multiple*tau})
        df_annot = pd.merge(causal, df_int, how='outer', on='BP')
        df_annot.fillna(0, inplace=True)
        df_annot_full = pd.merge(df_bim,df_annot,how='left',on='BP')
        df_annot_full.fillna(0,inplace=True)
        df_annot_full = df_annot_full.drop_duplicates('SNP_x')
        df_annot_full = df_annot[['VARBETA']].to_csv(varbeta_path+str(sim_unique_genos)+'_'+str(sim)+'.'+str(i)+'.varbeta',sep='\t',index=False,header=True)

def make_varbetas_causal_sparse(i,varbeta_path,sim_unique_genos,multiple,tau,annotbed,df_bim,num_sims,chr_plink,all_snps):
    for sim in range(num_sims,num_sims+1):
        bp = [x.start for x in annotbed]
	df_int = pd.DataFrame({'BP': bp, 'VARBETA':multiple*tau})
	df_annot = pd.merge(df_bim, df_int, how='left', on='BP')
	df_annot.fillna(0,inplace=True)
	causal_snps = df_annot[~(df_annot.VARBETA>0)].sample(n=int(round(len(df_bim)/100,0)))
	df_annot.loc[df_annot.SNP.isin(causal_snps.SNP),'VARBETA']=tau
        df_annot = df_annot.drop_duplicates('SNP')
	df_annot[['VARBETA']].to_csv(varbeta_path+str(sim_unique_genos)+'_'+str(sim)+'.'+str(i)+'.varbeta',sep='\t',index=False,header=True)
    

def main(args):
    len_geneset=0
    all_snps = pd.read_csv(args.sim_snps,delim_whitespace=True,names=['chr_bp','SNP'])
    total=len(all_snps)
    if args.pathway is not None:
        for i in xrange(1,23):
            chr_plink = args.bed_files+"."+str(i)
            annotbed,df_bim,num_causal_snps=genesets_to_snps(args,chr_plink,args.pathway,args.gene_coord_file)
            len_geneset+=num_causal_snps
        if args.sparse:
            causal_snps_sparse = all_snps.sample(n=int(round(len(all_snps)/100,0)))
            num_sparse = len(causal_snps_sparse)
            tau=args.h2g/(num_sparse+args.multiple*(len_geneset))
            print("The number of sparse snps that get tau is {0}".format(num_sparse))
	    print("The length of geneset is {0}".format(len_geneset))
	    print("Tau is: {0}".format(tau))
	else:
            tau=args.h2g/((total-len_geneset)+args.multiple*(len_geneset))
	for i in xrange(1,23):
	    chr_plink = args.bed_files+"."+str(i)
	    annotbed,df_bim,nums=genesets_to_snps(args,chr_plink,args.pathway,args.gene_coord_file)
            if args.sparse:
                make_varbetas_causal_sparse(i,args.varbeta_path,args.sim_unique_genos,args.multiple,tau,annotbed,df_bim,args.num_sims,chr_plink,all_snps)
            else:
                make_varbetas_causal(i,args.varbeta_path,args.sim_unique_genos,args.multiple,tau,annotbed,df_bim,args.num_sims,chr_plink)
    else:
        for i in xrange(1,23):
	    print("Generating varbeta files...")
	    chr_plink = args.bed_files+"."+str(i)
            n = count_length(chr_plink)
            make_varbetas(i,args.varbeta_path,n,chr_plink,total,args.h2g,args.sim_unique_genos,args.sim_snps,args.num_sims)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Separate genotype plink files into chromosomes and generate chr specific varbeta files')
    parser.add_argument("--bed-files", type=str, help="path to plink files, dont include .bim .bed or .fam ending",required=True)
    parser.add_argument("--sim-snps",type=str,help="File with list of all snps in bim")
    parser.add_argument("--varbeta-path",type=str,help="Path to varbeta files")
    parser.add_argument("--h2g",type=float,help="The heritability of the simulated phenotype")
    parser.add_argument("--sim-unique-genos",type=int,help="The numer of simulations you have with unique genotypes")
    parser.add_argument("--multiple",type=int,help="The multiple of causal snp varbetas vs non causal snps")
    parser.add_argument("--gene-coord-file",type=str,help="Path to map file for your genes, default is entrez map",default="/broad/finucanelab/ktashman/inrich_genesets/ENTREZ_gene_annot.txt")
    parser.add_argument("--pathway",type=str,help="Path to geneset to test for enrichment")
    parser.add_argument("--windowsize",type=int,help="Windowsize around each gene to determine which snps are in that gene")
    parser.add_argument("--num-sims",type=int,help="Number of simulations based on one set of genotypes")
    parser.add_argument("--sparse",help="Type of simulation to run for causal geneset",action='store_true')
    main(parser.parse_args())


    

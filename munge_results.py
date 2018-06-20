from __future__ import division
import pandas as pd
import numpy as np
import scipy
from scipy import stats
import argparse
import math
import os
import argparse
import subprocess

def read_results(input_file):
    x = pd.read_csv(input_file,delim_whitespace=True)
    return x
        
def count(anyfile):
    n = 0    
    for line in open(anyfile, "r"):
        n += 1
    return n

def fdr(p):
    p.sort()
    c = np.arange(1,len(p)+1)*0.05/len(p)
    cutoff_fdr = 0
    for i in range(len(p)):
        if p[i] < c[i]:
            cutoff_fdr = p[i]
    return cutoff_fdr

def munge_ldsc(genesets,in_path,out_path,x):
    out = open(os.path.join(out_path,x+'.exclude.results_munged'),'w')
    results = []
    names = []
    descrip = []
    genesets_list = open(genesets,'r')
    for g in genesets_list:
        name = g.split()[0]
	#name,d = g.split()
	res = read_results(os.path.join(in_path,x+'.inrich.exclude.c1.all.v3.0.entrez.msig.'+name+'.ldsc.cell_type_results.txt'))
	results.append(res)
	names.append(name)
	#descrip.append(d)
    results_all= pd.concat(results,axis=0).reset_index(drop=True)    
    names_all = pd.DataFrame(names,columns=['GS']).reset_index(drop=True)
    #descrip_all  = pd.DataFrame(descrip,columns=['descrip']).reset_index(drop=True)
    all = [names_all,results_all]
    #all = [names_all,results_all,descrip_all]
    full = pd.concat(all,axis=1)
    full.to_csv(os.path.join(out_path,x+'exclude.results_munged'),sep='\t',index=False)
    return full

def munge_ldsc_full(genesets,in_path,out_path,x):
    out = open(os.path.join(out_path,x+'.exclude.results_munged'),'w')
    results = []
    names = []
    descrip = []
    genesets_list = open(genesets,'r')
    for g in genesets_list:
        name = g.split()[0]
        #name,d = g.split()
        res = read_results(os.path.join(in_path,x+'.inrich.c1.all.v3.0.entrez.msig.'+name+'.ldsc.cell_type_results.txt'))
        results.append(res)
        names.append(name)
        #descrip.append(d)
    results_all= pd.concat(results,axis=0).reset_index(drop=True)
    names_all = pd.DataFrame(names,columns=['GS']).reset_index(drop=True)
    #descrip_all  = pd.DataFrame(descrip,columns=['descrip']).reset_index(drop=True)
    all = [names_all,results_all]
    #all = [names_all,results_all,descrip_all]
    full = pd.concat(all,axis=1)
    full.to_csv(os.path.join(out_path,x+'exclude.results_munged'),sep='\t',index=False)
    return full    

def munge_inrich(inrich_results,geneset_list,x):
    length = count(geneset_list)
    print(length)
    out = os.path.join(inrich_results,x+'exclude.munged')
    x = x.strip('.UKB_460K')
    filepath = os.path.join(inrich_results,x+'c1.all.v3.0.entrez.msig.set.out.inrich')
    command="/broad/finucanelab/ktashman/inrich_analyses/scripts/grep.sh {0} {1} {2}".format(length,filepath,out)
    p = subprocess.Popen(command.split(), shell=False)
    p.communicate()
    p.wait()
    out_inrich = pd.read_csv(out,sep='\t',header=0)
    out_inrich['GS'] = out_inrich.apply(lambda x: x['TARGET'].split()[0],axis=1)
    return out_inrich
    
def main(args):
    phens = args.phenotypes.split(',')
    for x in phens:    
        out_ldsc = munge_ldsc(args.geneset_list,args.in_path,args.out_path,x)
        out_inrich = munge_inrich(args.inrich_path,args.geneset_list,x)
	out_ldsc_full = munge_ldsc_full(args.geneset_list,args.in_path_full,args.in_path_full,x)
	out_ldsc_full = out_ldsc_full.rename(columns={'L2_0':'L2_full','Coefficient_P_value':'Coefficient_P_value_full'})
	merged = out_ldsc.merge(out_inrich,how='inner',on='GS')
	merged = merged.merge(out_ldsc_full,how='inner',on='GS')
        merged['chisq'] = merged.apply(lambda x: -2*(math.log(x.Coefficient_P_value) + math.log(x.P)),axis=1)
        merged['meta_pval'] = scipy.stats.chi2.sf(merged.chisq.values,4)
	merged = merged.sort_values(by=['meta_pval'])
	cutoff_meta = fdr(merged.meta_pval.values)*1.00001
        print(cutoff_meta)
	cutoff_LDSC = fdr(merged.Coefficient_P_value_full.values)*1.00001
	print(cutoff_LDSC)
	cutoff_INRICH = fdr(merged.P.values)*1.00001
	print(cutoff_INRICH)
	merged['pass_INRICH']=False
	merged['pass_meta']=False
        merged['pass_LDSC']=False
	merged['pass_meta'][merged.meta_pval<cutoff_meta]=True
	merged['pass_LDSC'][merged.Coefficient_P_value_full<cutoff_LDSC]=True
        merged['pass_INRICH'][merged.P<cutoff_INRICH]=True
	merged = merged.rename(columns={'T_TARG':'SIZE'})
        merged[['GS','SIZE','chisq','meta_pval','pass_meta','pass_LDSC','pass_INRICH']].to_csv(os.path.join(args.out_path,x+'.exclude.meta.txt'),sep="\t",index=False,header=True) 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates gene sets with annotations')
    parser.add_argument("--geneset-list", type=str, help="path to list of unique genesets", required=True)
    parser.add_argument("--in-path", type=str, help="path to results files")
    parser.add_argument("--in-path-full", type=str, help="path to results files full regression")
    parser.add_argument("--out-path", type=str, help="where to put munged results files")
    parser.add_argument("--inrich-path", type=str, help="path to inrich results for all phenotypes in your lis")
    parser.add_argument("--phenotypes", type=str, help="comma separated list of phenotypes that are the prefix in your ldsc and inrich results") 
    main(parser.parse_args())                    

        



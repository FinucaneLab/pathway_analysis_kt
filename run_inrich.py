import os
import time
import pandas
import subprocess
import argparse

def plink_clump(bfile,sumstats,gene_range):
    out_clumped = os.path.basename(sumstats).strip('.gz')
    command = """/home/unix/sripke/plink_src/plink_1.9_newest/plink 
               --noweb --bfile {0} 
               --clump {1} 
               --clump-p1 5e-8 
               --clump-p2 .05 
               --clump-r2 .5 
               --clump-range {2} 
               --clump-range-border 20 
               --out {3}""".format(bfile,sumstats,gene_range,out_clumped)
    p = subprocess.Popen(command.split(), shell=False)
    p.communicate()
    p.wait()
    return out_clumped 

def get_intervals(clumped_ranges):
    out_intervals  = clumped_ranges+'.intervals'
    command="/broad/finucanelab/ktashman/inrich_analyses/scripts/gawk.sh {0} {1}".format(clumped_ranges+'.clumped.ranges',out_intervals)
    p = subprocess.Popen(command.split(), shell=False)
    p.communicate()
    p.wait()
    return out_intervals

def run_inrich(intervals,sumstats_snps,genesets,sumstats):
    basename = os.path.basename(sumstats).strip('.gz')+os.path.basename(genesets)
    command="""/broad/finucanelab/ktashman/pathway_analysis/inrich 
             -a {0}  
  	     -m {1} 
  	     -g /broad/finucanelab/ktashman/inrich_genesets/entrez_gene.hg19.map 
             -t {2} 
  	     -w 20 
  	     -c
	     -r 10000 
  	     -q 2000 
  	     -p .1 
	     -o {3}""".format(intervals,sumstats_snps,genesets,basename)
    p = subprocess.Popen(command.split(), shell=False)
    p.communicate()
    p.wait()


def main(args):
    out_clumped = plink_clump(args.ref_bim,args.sumstats,args.gene_range)
    #while not os.path.exists(out_clumped):
    #    time.sleep(300) 
    out_intervals = get_intervals(out_clumped)
    #while not os.path.exists(out_intervals):
    #    time.sleep(200)
    run_inrich(out_intervals,args.assoc_snps,args.geneset_list,args.sumstats)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run inrich analysis start to finish for a phenotype')
    parser.add_argument("--sumstats", type=str, help="path to summary stats for clumping",required=True)
    parser.add_argument("--assoc-snps",help="str",default="File with CHR BP and no header for snps from association study",required=True)
    parser.add_argument("--geneset-list",help="str",default="List of genesets to run the analysis on e.g. kegg.set",required=True)
    parser.add_argument("--ref-bim", type=str, help="path to reference bim files for clumping",default="/broad/finucanelab/1000G/1000G_EUR_Phase3/plink_files/plink")
    parser.add_argument("--gene-range", type=str, help="which intervals to clump over",default="/broad/finucanelab/ktashman/inrich_genesets/ENTREZ_clump.txt")
    main(parser.parse_args())
    

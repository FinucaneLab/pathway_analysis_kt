import pandas as pd
import os
import argparse

plink = "/home/unix/sripke/plink_src/plink_1.9_newest/plink"
def split_chr(plink_files,chromosome):
    newbfile=plink_files + '.' + str(chromosome)
    command="{0} --bfile {1} --chr {2} --make-bed --out {3}\n".format(plink, plink_files, str(chromosome),newbfile)
    os.system(command)
    command="{0} --bfile {1} --update-name {2} --make-bed --out {1}\n".format(plink,newbfile,"/broad/finucanelab/ktashman/inrich_analyses/simulations/ukbb/sim.snps")
    os.system(command)
    command="{0} --bfile {1} --exclude {2} --make-bed --out {1}\n".format(plink,newbfile,"/broad/finucanelab/ktashman/inrich_analyses/simulations/ukbb/duplicate_rsids_UKB_50k_null.snps")
    os.system(command)
    command="{0} --bfile {1} --list-duplicate-vars suppress-first --out {2}\n".format(plink,newbfile,newbfile+'.duplicates')
    os.system(command)
    command="{0} --bfile {1} --exclude {2} --make-bed --out {3}\n".format(plink,newbfile,newbfile+'.duplicates.dupvar',newbfile)
    os.system(command)
def frq_file(plink_files):
    command="{0} --bfile {1} --freq --out {2}\n".format(plink, plink_files ,plink_files)
    os.system(command)

def main(args):
    split_chr(args.bed_files,args.chromosome)
    chr_plink = args.bed_files+"."+str(args.chromosome)
    frq_file(chr_plink)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Separate genotype plink files into chromosomes and generate chr specific varbeta files')
    parser.add_argument("--bed-files", type=str, help="path to plink files, dont include .bim .bed or .fam ending",required=True)
    parser.add_argument("--chromosome",type=str,help="Chromosome number you are doing")
    main(parser.parse_args())


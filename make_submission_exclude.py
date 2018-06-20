import pandas as pd
import os
import argparse

def submission_script(genesets,outpath):
    out = "c1.all.v3.0.entrez.msig"
    f = open(os.path.join(outpath,'inrich_c1_exclude_submit_bigbaseline.tsv'),'w')
    for geneset in open(genesets,'r'):
        f.write("\t".join(['gs://inrich_analyses/inrich_ldscores/inrich.'+out+'.'+geneset.strip()+'.*','gs://singlecellldscore/PASS/UKB_460K.disease_ASTHMA_DIAGNOSED.sumstats','inrich.exclude.'+out+'.'+geneset.strip(),'gs://singlecellldscore/entrez_control/','ENTREZ','gs://inrich_analyses/ENTREZ_gene_annot.txt','gs://inrich_analyses/exclude_files/UKB_460K.disease_ASTHMA_DIAGNOSED.exclude','gs://inrich_analyses/inrich_results_exclude/'])+"\n")


def main(args):
    submission_script(args.unique_genesets,args.out_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates gene sets with annotations')
    parser.add_argument("--unique-genesets", type=str, help="path to unique genesets to run")
    parser.add_argument("--out-path", type=str, help="where to put submission script,without /")
    main(parser.parse_args())

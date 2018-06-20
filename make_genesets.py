import pandas as pd
import argparse
import os

def read_unique_genesets(genesets_unique,full_genesets,reference,out_path):
   # import pdb;pdb.set_trace()
	full_gs = pd.read_csv(full_genesets,sep=' ',names=['ID','GS','DESCRIP'])
	ref = pd.read_csv(reference, sep=' ',names=['CHR','START','END','ID','GENE','DESCRIP'])
	out = os.path.basename(full_genesets).strip('.set')
	submit_file = os.path.join(out_path,'submit_'+out+'.tsv')
	f = open(submit_file,'w')
	for geneset in open(genesets_unique,'r'):
		geneset = geneset.replace('\n','')
		name = geneset
		ids = full_gs[full_gs.GS==geneset].ID.tolist()
		genes = ref[ref.ID.isin(ids)].GENE
		path = os.path.join(out_path,'inrich.'+out+'.'+name+'.GeneSet')
		if len(genes)>0:
			genes.to_csv(path,sep='\n',header=False,index=False)
			f.write("\t".join(['gs://inrich_analyses/inrich_genesets/inrich.'+out+'.'+name+'.GeneSet','gs://singlecellldscore/pysch_sumstats/scz_summary_stats.sumstats.gz,gs://singlecellldscore/PASS/UKB_460K.mental_NEUROTICISM.sumstats,gs://singlecellldscore/PASS/UKB_460K.disease_ASTHMA_DIAGNOSED.sumstats','inrich.'+out+'.'+name,'gs://singlecellldscore/entrez_control/','ENTREZ','gs://inrich_analyses/ENTREZ_gene_annot.txt','gs://inrich_analyses/inrich_ldscores/','gs://inrich_analyses/inrich_results/'])+"\n")

def main(args):
    read_unique_genesets(args.unique_genesets,args.full_genesets,args.reference,args.out_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Creates gene sets with annotations')
    parser.add_argument("--unique-genesets", type=str, help="path to list of unique genesets", required=True)
    parser.add_argument("--full-genesets", type=str, help="path to full geneset file")
    parser.add_argument("--out-path", type=str, help="where to put GeneSet files, exclude /")
    parser.add_argument("--reference",help="Create gene sets for binary annotations",required=False,default='/broad/finucanelab/ktashman/inrich_genesets/entrez_gene.hg19.map')
    main(parser.parse_args())

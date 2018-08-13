import pandas as pd
final=pd.DataFrame(columns=['ID','GS'])
map = pd.read_csv('/broad/finucanelab/ktashman/inrich_genesets/entrez_gene.hg19.map',delim_whitespace=True,names=['CHR','START','END','ID','GENE','DESCRIP'])
all_geneset = ['simulations.5.GeneSet','simulations.50.GeneSet','simulations.500.GeneSet']
for geneset in all_geneset:
    df=pd.DataFrame()
    GS = pd.read_csv('/broad/finucanelab/ktashman/inrich_analyses/simulations/causal_genesets/'+geneset,delim_whitespace=True,names=['GENE'])
    merge = map.merge(GS,how='inner',on='GENE')
    df['ID']=merge['ID']
    df['GS']=geneset
    final = final.append(df)
final.to_csv('/broad/finucanelab/ktashman/inrich_analyses/simulations/causal_genesets/simulations.5_50_500.set',sep='\t',index=False,header=False)    
    

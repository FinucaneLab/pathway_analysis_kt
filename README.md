Step 1:

Run make_genesets.py by inputting a unique list of genesets
to both make the geneset files for LDSC and the submit.tsv file
for dsub.

```
python make_genesets.py \
       --unique-genesets /broad/finucanelab/ktashman/inrich_genesets/kegg.unique.descrip \
       --full-genesets /broad/finucanelab/ktashman/inrich_genesets/kegg.set \
       --out-path /broad/finucanelab/ktashman/inrich_analyses/inrich_LDSC_genesets \

```

Step 2:

Copy the genesets from that folder to your local machine and upload them
to the bucket and folder as specified in your make_genesets.py script

Step 3:

Copy the submit.tsv file to local machine and run the dsub command script

Step 4:

While the LDSC pipeline is running, run the inrich analyses using run_inrich.py

```
python run_inrich.py \
       --sumstats /broad/finucanelab/ktashman/inrich_analyses/sumstats/scz_summary_stats.sumstats \
       --assoc_snps /broad/finucanelab/ktashman/inrich_analyses/sumstats/scz_summary_stats.assoc_snps \
       --geneset-list /broad/finucanelab/ktashman/inrich_genesets/kegg.set
```

Step 5:

When your LDSC results are done, copy them to local machine and copy to server.
Upload these to a folder that contains all of your genesets.
Run munge_results.py to munge the inrich and the LDSC results and produce 
comined p-value results.

```
python munge_results.py \
       --geneset-list /broad/finucanelab/ktashman/inrich_genesets/kegg.unique.descrip \
       --in-path /broad/finucanelab/ktashman/inrich_analyses/inrich_results \
       --out-path /broad/finucanelab/ktashman/inrich_analyses/inrich_results \
       --inrich-path /broad/finucanelab/ktashman/inrich_analyses/sumstats/ \
       --phenotypes scz_summary_stats.sumstats
```       

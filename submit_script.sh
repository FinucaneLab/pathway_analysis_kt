dsub \
    --provider google \
    --project LDScore-Data \
    --zones "us-central1-*" \
    --min-ram 10 \
    --logging gs://kt_inrich/logging/ \
    --disk-size 100 \
    --image gcr.io/ldscore-data/ldscore \
    --tasks submit_kegg.tsv \
    --script run_pipeline.py

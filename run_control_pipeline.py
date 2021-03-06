#!/usr/bin/env python

import subprocess
import os


GENE_LIST = os.environ['GENE_LIST']
PREFIX = os.environ['PREFIX']
GENE_COL_NAME = os.environ['GENE_COL_NAME']
OUT_LDSCORES = os.environ['OUT_LDSCORES']
MAP_FILE = os.environ['MAP_FILE']

subprocess.call(['/home/sc_enrichement/sc_enrichement-master/main.py',
                    '--main-annot',GENE_LIST,
                    '--ldscores-prefix',PREFIX,
                    '--gene-anno-pos-file',MAP_FILE,
                    '--gene-col-name',GENE_COL_NAME,
                    '--export_ldscore_path',OUT_LDSCORES,
                    '--windowsize','10000',
                    '--verbose'])

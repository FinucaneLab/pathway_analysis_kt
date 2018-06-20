#!/usr/bin/env python

import subprocess
import os


GENE_LIST = os.environ['GENE_LIST']
SUMSTATS = os.environ['SUMSTATS']
PREFIX = os.environ['PREFIX']
CONDITION_ANNOT = os.environ['CONDITION_ANNOT']
GENE_COL_NAME = os.environ['GENE_COL_NAME']
OUT_LDSCORES = os.environ['OUT_LDSCORES']
OUT = os.environ['OUT']
MAP_FILE = os.environ['MAP_FILE']

subprocess.call(['/home/sc_enrichement/sc_enrichement-master/main.py',
                    '--main-annot',GENE_LIST,
                    '--summary-stats-files',SUMSTATS,
                    '--ldscores-prefix',PREFIX,
                    '--out',OUT,
                    '--condition-annot',COND_ANNOT,
		    '--gene-anno-pos-file',MAP_FILE,
		    '--gene-col-name',GENE_COL_NAME,
                    '--export_ldscore_path',OUT_LDSCORES,
                    '--windowsize','10000',
                    '--verbose'])

#!/bin/bash
len=$1
in=$2
out=$3
grep -A $len  PCORR $2 > $3

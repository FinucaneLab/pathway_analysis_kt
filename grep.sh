#!/bin/bash
len=$1
in=$2
out=$3
chars=$4
grep -A $len  $chars $in > $out

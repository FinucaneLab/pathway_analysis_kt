#!/bin/bash
in=$1
out=$2
gawk ' NR>1 { print $1 "." substr($5, index($5,":")+1) } ' \
            $in | gawk -F. ' {print $1,$2,$4 }' > $out

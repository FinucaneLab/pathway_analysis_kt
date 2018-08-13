for ((i=0;i<=99;i++))
do
    grep True sim0_$i.sumstats.pruned.sim0_$i.exclude.meta.txt    
    echo $i
done

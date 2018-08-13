import pandas as pd
import argparse
import os
import json
import subprocess

def run_pipeline(args,i):
    cmd="""python scripts/prep_for_simulations.py --sim-unique-genos {0} 
   						--bed-files {1} 
   						--h2g .8  
						--varbeta-path {2}
						--sim-snps {3}
						--num-sims {4} """.format(str(i),args.bed_files+str(i),args.varbeta_files,args.sim_snps,str(int(args.simulation_number)-1))
    p = subprocess.Popen(cmd.split(), shell=False)
    p.communicate() 
    p.wait()

    cmd="""python scripts/sim_pheno.py --sim-unique-genos {0} 
    				--make-score-files 
				--varbeta-files {1} 
				--num-sims {4}
    				--bed-files {2} 
				--out-folder {3}""".format(str(i),args.varbeta_files+str(i),args.bed_files+str(i),args.score_folder,str(int(args.simulation_number)-1))
    p = subprocess.Popen(cmd.split(), shell=False)
    p.communicate() 
    p.wait()
 
    cmd="""python scripts/sim_pheno.py --sim-unique-genos {0}
    				--get-plink-profiles
				--score-folder {1}
				--num-sims {4} 
				--out-folder {2}
				--bed-files {3}""".format(str(i),args.score_folder,args.plink_profile_folder,args.bed_files+str(i),str(int(args.simulation_number)-1))
    p = subprocess.Popen(cmd.split(), shell=False)
    p.communicate() 
    p.wait()

    cmd="""python scripts/sim_pheno.py --num-sims {5}
    				--sim-unique-genos {0}
				--bed-files {1}
    				--profile-folder {2}
				--h2g-file {3}
				--out-folder {4} 
				--compute-pheno""".format(str(i),args.bed_files+str(i),args.plink_profile_folder,args.h2g_file,args.pheno_folder,str(int(args.simulation_number)-1))
    p = subprocess.Popen(cmd.split(), shell=False)
    p.communicate()
    p.wait()
 
    cmd="""python scripts/compute_sumstats.py --num-sims {4}
    				--sim-unique-genos {0}
				--pheno-folder {1}
    				--out-folder {2}
				--bed-files {3}
				--compute-ss""".format(str(i),args.pheno_folder,args.qassoc_folder,args.bed_files+str(i),str(int(args.simulation_number)-1))
    p = subprocess.Popen(cmd.split(), shell=False)
    p.communicate()
    p.wait()
    
    cmd="""python scripts/compute_sumstats.py --format-ss
    					--sim-unique-genos {0}
					--qassoc-folder {1}
    					--bim-files {2} 
					--num-sims {4}
					--out-folder {3}""".format(str(i),args.qassoc_folder,args.bed_files+str(i),args.sumstats_files,str(int(args.simulation_number)-1))
    p = subprocess.Popen(cmd.split(), shell=False)
    p.communicate()
    p.wait()
    
    cmd="""python scripts/prune_sumstats.py --sumstats {0} 
    					--assoc-snp-files {1} 
    					--sim-unique-genos {2} 
					--num-sims {3} """.format(args.sumstats_files,args.assoc_snp_files,str(i),str(int(args.simulation_number)-1))
    p = subprocess.Popen(cmd.split(), shell=False)
    p.communicate()
    p.wait()
    
    cmd="""qsub scripts/run_inrich.sh {0} {1}""".format(args.json,str(int(args.simulation_number)-1))
    
    p = subprocess.Popen(cmd.split(), shell=False)
    p.communicate()
    p.wait()
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', help = 'json file for simulations')
    parser.add_argument('--simulation-number',help="The number of the simulation you're on")

    args = parser.parse_args()
    args_dict = vars(args)
    d = json.load(open(args.json))
    args_dict.update(d)

    for i in range(args.num_genotype_sims):
        run_pipeline(args,i)

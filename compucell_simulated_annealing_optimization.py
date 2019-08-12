from modules.compucell import compucell
from modules.compucell import cellular_automata
from modules.optimization.simulated_annealing import helpers as sao
from modules.optimization.hill_climb import helpers as hco #I just need to use the getNeighbors function.
from modules.utility import optimization as o
from modules.utility import settings as settings_system
import numpy as np
import os
import random
import time
import datetime
import sys
import json

settings_files = [
    'globalDefaults.json',
    'modules\\utility\\optimizationDefaults.json',
    'modules\\optimization\\simulated_annealing\\defaults.json'
]

all_settings = settings_system.settings(settings_files)
all_settings = settings_system.parseCommandLine(sys.argv, all_settings)
settings = o.settings = sao.settings = all_settings.settings

print("Settings: ", settings)

def main():
    current_phenotype = (cellular_automata.randomSetup(settings['INPUT_SPACE_SIZE'], settings['FUNCTION_SPACE_SIZE']), o.generateRulesetString(512))
    log = {
        'bests': []
    }
    for k in range(settings['K_MAX']):
        print(f"[MAIN] RUN {k}")
        start_time = time.time()
        T = sao.temperature(settings['K_MAX']/(k+1))
        new_phenotype = random.choice(hco.getNeighbors(current_phenotype))

        s = o.performanceEvalulation([current_phenotype])[0][0]
        s_new = o.performanceEvalulation([new_phenotype])[0][0]
        if sao.P(sao.E(s), sao.E(s_new), T) >= random.random():
            print("Moved.")
            current_phenotype = new_phenotype
            score = s_new
        else:
            print("Constant.")
            score = s
        print(f"[MAIN] Score: {score}")
        #log['bests'].append(score)
        end_time = time.time()        
        print(f"[MAIN] Run {k} took {end_time - start_time} seconds.")
    
    final_score = o.performanceEvalulation([current_phenotype])[0][0]
    final_phenotype = (current_phenotype[0].tolist(), current_phenotype[1])

    print("ALRIGHT, WE'RE DONE HERE.")
    print(f"Max: {final_score}")
    print(f"Function Body: {final_phenotype[0]}")
    print(f"RuleString: {final_phenotype[1]}")

    final_ranked_phenotype = (final_score, final_phenotype)

    o.recordAll(final_ranked_phenotype, log)

main()
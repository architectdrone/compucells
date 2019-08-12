from modules.compucell import compucell
from modules.compucell import cellular_automata
from modules.optimization.genetic import helpers as go
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
    'modules\\optimization\\genetic\\defaults.json'
]

all_settings = settings_system.settings(settings_files)
all_settings = settings_system.parseCommandLine(sys.argv, all_settings)
settings = o.settings = go.settings = all_settings.settings

print("Settings: ", settings)

def main():
    current_generation = o.generateInitialBatch()
    for i in range(settings['RUNS']):
        print(f"[MAIN] RUN {i}")
        start_time = time.time()
        evaluated_batch = o.performanceEvalulation(current_generation)
        go.histogram(evaluated_batch)
        selected = go.selection(evaluated_batch)
        if go.log["bests"][-1] >= settings['PERFORMANCE_THRESHOLD']:
            break
        current_generation = go.reproduction(selected)
        end_time = time.time()
        print(f"[MAIN] Run {i} took {end_time - start_time} seconds.")
    
    scores = o.performanceEvalulation(current_generation)
    sorted_scores = sorted(scores, key=lambda t: t[0])
    print("ALRIGHT, WE'RE DONE HERE.")
    print(f"Max: {sorted_scores[-1][0]}")
    print(f"Function Body: {sorted_scores[-1][1][0]}")
    print(f"RuleString: {sorted_scores[-1][1][1]}")

    final_score = sorted_scores[-1][0]
    final_phenotype = {
        'function_space': sorted_scores[-1][1][0].tolist(),
        'rule_string': sorted_scores[-1][1][1]
    }
    final_ranked_phenotype = (final_score, final_phenotype)

    o.recordAll(final_ranked_phenotype, go.log)

main()
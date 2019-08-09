from modules.compucell import compucell
from modules.compucell import cellular_automata
from modules.optimization.genetic import helpers as go
from modules.optimization.genetic import settings
from modules.utility import optimization as o
from modules.utility import settings as new_settings
import numpy as np
import random
import time
import sys
import json

settings_files = [
    'modules\\utility\\optimizationDefaults.json',
    'modules\\optimization\\genetic\\defaults.json'
]

all_settings = new_settings.settings(settings_files)
all_settings = new_settings.parseCommandLine(sys.argv, all_settings)

o.settings = go.settings = all_settings.settings

print("Settings: ", all_settings.settings)

def main():
    current_generation = o.generateInitialBatch()
    for i in range(settings.RUNS):
        print(f"[MAIN] RUN {i}")
        start_time = time.time()
        selected = go.selection(o.performanceEvalulation(current_generation))
        current_generation = go.reproduction(selected)
        end_time = time.time()
        print(f"[MAIN] Run {i} took {end_time - start_time} seconds.")
    scores = o.performanceEvalulation(current_generation)
    sorted_scores = sorted(scores, key=lambda t: t[0])
    print("ALRIGHT, WE'RE DONE HERE.")
    print(f"Max: {sorted_scores[-1][0]}")
    print(f"Function Body: {sorted_scores[-1][1][0]}")
    print(f"RuleString: {sorted_scores[-1][1][1]}")

    go.log['function'] = sorted_scores[-1][1][0].tolist()
    go.log['rs'] = sorted_scores[-1][1][1]
    f = open(f"run_info//{go.log['start_time']}.txt","w")
    json.dump(go.log, f)
    f.close()

main()
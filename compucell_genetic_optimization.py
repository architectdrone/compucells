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
settings = go.log['settings'] = o.settings = go.settings = all_settings.settings

print("Settings: ", settings)

def main():
    current_generation = o.generateInitialBatch()
    for i in range(settings['RUNS']):
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

    go.log['final'] = sorted_scores[-1][0]
    go.log['function'] = sorted_scores[-1][1][0].tolist()
    go.log['rs'] = sorted_scores[-1][1][1]
    
    file_location = settings['LOG_ROOT_FOLDER']+"//"+settings['LOG_SPECIFIC_FOLDER']
    #Create directory if it doesn't already exist
    try:
        os.makedirs(file_location)
    except FileExistsError:
        # directory already exists
        pass
    file_name = str(datetime.datetime.today()).replace(" ","_").replace(":","-")[:-7]
    f = open(f"{file_location}//{file_name}.json","w")
    json.dump(go.log, f)
    f.close()

main()
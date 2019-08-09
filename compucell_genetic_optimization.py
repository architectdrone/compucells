from modules.compucell import compucell
from modules.compucell import cellular_automata

from modules.optimization.genetic import helpers as go
from modules.optimization.genetic import settings
from modules.utility import optimization as o

import numpy as np
import random
import time
import json

o.settings = {
    'FUNCTION_NAME': settings.FUNCTION_NAME,
    'CC_PER_BATCH': settings.CC_PER_BATCH,
    'FUNCTION_SPACE_SIZE': settings.FUNCTION_SPACE_SIZE,
    'ITERATIONS': settings.ITERATIONS,
    'RUNS': settings.RUNS,
    'PERFORMANCE_THRESHOLD': settings.PERFORMANCE_THRESHOLD,
    'INPUT_SPACE_SIZE': settings.INPUT_SPACE_SIZE,
    'MUTATION_CHANCE': settings.MUTATION_CHANCE,
}

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
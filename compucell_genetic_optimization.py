from modules.compucell import compucell
from modules.compucell import cellular_automata

from modules.optimization.genetic import helpers as go
from modules.optimization.genetic import settings

import numpy as np
import random
import time
import json


def main():
    current_generation = go.generateInitialBatch()
    for i in range(settings.RUNS):
        print(f"[MAIN] RUN {i}")
        start_time = time.time()
        selected = go.selection(current_generation)
        current_generation = go.reproduction(selected)
        end_time = time.time()
        print(f"[MAIN] Run {i} took {end_time - start_time} seconds.")
    scores = go.performanceEvalulation(current_generation)
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
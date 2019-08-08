import compucell as cc
import cellular_automata as ca
import cgo_helpers as cgo
import numpy as np
import random
import time
import json
import cgo_settings

def main():
    current_generation = cgo.generateInitialBatch()
    for i in range(cgo_settings.RUNS):
        print(f"[MAIN] RUN {i}")
        start_time = time.time()
        selected = cgo.selection(current_generation)
        current_generation = cgo.reproduction(selected)
        end_time = time.time()
        print(f"[MAIN] Run {i} took {end_time - start_time} seconds.")
    scores = cgo.performanceEvalulation(current_generation)
    sorted_scores = sorted(scores, key=lambda t: t[0])
    print("ALRIGHT, WE'RE DONE HERE.")
    print(f"Max: {sorted_scores[-1][0]}")
    print(f"Function Body: {sorted_scores[-1][1][0]}")
    print(f"RuleString: {sorted_scores[-1][1][1]}")

    cgo.log['function'] = sorted_scores[-1][1][0].tolist()
    cgo.log['rs'] = sorted_scores[-1][1][1]
    f = open(f"run_info//{cgo.log['start_time']}.txt","w")
    json.dump(cgo.log, f)
    f.close()

main()
from modules.utility import settings as settings_system
from modules.utility import optimization as o
from modules.optimization.hill_climb import helpers as hco
import sys
import time
import json
import os
import datetime
import numpy as np

settings_files = [
    'globalDefaults.json',
    'modules\\utility\\optimizationDefaults.json',
    'modules\\optimization\\hill_climb\\defaults.json'
]

all_settings = settings_system.settings(settings_files)
all_settings = settings_system.parseCommandLine(sys.argv, all_settings)
settings = o.settings = hco.settings = all_settings.settings

print("Settings: ", settings)

def main():
    if 'STARTING_RULESET' in settings and 'STARTING_FUNCTION_SPACE' in settings:
        print("Using predefined starting point!")
        starting_ruleset = settings['STARTING_RULESET']
        starting_function_space = np.asarray(eval(settings['STARTING_FUNCTION_SPACE']))
        current_generation = [(starting_function_space, starting_ruleset)]
    else:
        current_generation = o.generateInitialBatch()

    highest_scoring_optima = () #PHENOTYPE. Optima with highest score
    highest_scoring_optima_score = 0 #The score of the highest scoring optima
    run_number = 0
    internal_log = {'bests' : []}
    while highest_scoring_optima_score < 1.0 and len(current_generation) != 0:
        print(f"[MAIN] RUN {run_number}")
        start_time = time.time()

        optimas = [(highest_scoring_optima_score, highest_scoring_optima)] #RANKED BATCH. A list of all optimas found (within the last generation)
        non_optimas = [] #BATCH. A list of all phenotypes that have not yet been shown to be optimas.
        gain = 0 #Number of phenotypes gained in the last generation. For tracking
        loss = 0 #Number of phenotypes lost   in the last generation. For tracking
        for index, a in enumerate(current_generation):
            current_score = o.performanceEvalulation([a])[0][0]
            print(f" Member {index}. Current Score: {current_score}. Evaluating Neighbors... ", end="")
            neighbors_ranked = o.performanceEvalulation(hco.getNeighbors(a))
            print("Done. Determining High Scorers... ", end="")
            neighbors_high_score = 0
            neighbors_high_scorers = [] #BATCH
            #Get high scores, and phenotypes who score highly
            for ranked_phenotype in neighbors_ranked:
                if ranked_phenotype[0] > neighbors_high_score:
                    neighbors_high_score = ranked_phenotype[0]
                    neighbors_high_scorers = [ranked_phenotype[1]]
                elif ranked_phenotype[0] == neighbors_high_score:
                    neighbors_high_scorers.append(ranked_phenotype[1])
            
            print(f"Done. Next Neighbor: {neighbors_high_score}. Number of Neighbors: {len(neighbors_high_scorers)}. Conclusion about member {index}: ", end="")
            if current_score >= neighbors_high_score:
                print(f"Optima.")
                optimas.append((current_score, a))
                loss+=1
            else:
                print("Not Optima.")
                for phenotype in neighbors_high_scorers:
                    non_optimas.append(phenotype)
                    gain+=1
                gain-=1 #So that it only counts new additions.
        
        #Find new top optima.
        for ranked_phenotype in optimas:
            if highest_scoring_optima_score <= ranked_phenotype[0]:
                highest_scoring_optima_score = ranked_phenotype[0]
                highest_scoring_optima = ranked_phenotype[1]
        
        current_generation = non_optimas
        internal_log['bests'].append(highest_scoring_optima_score)
        end_time = time.time()
        print(f"[MAIN] Top: {highest_scoring_optima_score} Phenotype: {highest_scoring_optima}")
        print(f"[MAIN] Gain: {gain} Loss: {loss} New Population: {len(current_generation)}")
        print(f"[MAIN] Run {run_number} took {end_time - start_time} seconds.")
        run_number+=1
    
    print("ALRIGHT, WE'RE DONE HERE.")
    print(f"Max: {highest_scoring_optima_score}")
    print(f"Function Body: {highest_scoring_optima[0]}")
    print(f"RuleString: {highest_scoring_optima[1]}")

    log = {'optimizer': 'genetic', 'information': internal_log}
    log['final_score'] = highest_scoring_optima_score
    log['phenotype'] = {
        'function_space': highest_scoring_optima[0].tolist(),
        'rule_string': highest_scoring_optima[1]
    }
    log['settings'] = settings
    
    file_location = settings['LOG_ROOT_FOLDER']+"//"+settings['LOG_SPECIFIC_FOLDER']
    #Create directory if it doesn't already exist
    try:
        os.makedirs(file_location)
    except FileExistsError:
        # directory already exists
        pass
    file_name = str(datetime.datetime.today()).replace(" ","_").replace(":","-")[:-7]
    f = open(f"{file_location}//{file_name}.json","w")
    json.dump(log, f)
    f.close()

main()

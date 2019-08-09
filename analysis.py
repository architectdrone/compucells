from modules.compucell import compucell
from modules.utility import cruncher
from modules.optimization.genetic import helpers as cgo_helpers
from modules.optimization.genetic import settings as cgo_settings
import sys
import json
import numpy as np

file_name = input("> ") if len(sys.argv) < 2 else sys.argv[1]
to_investigate = open(file_name, 'r')
data = json.load(to_investigate)
to_investigate.close()

function_space = np.asarray(data['function'])
ruleset_helper = cgo_helpers.functionProxy(data['rs'])
ruleset = ruleset_helper.ruleset

my_compucell = compucell.compucell(function_space, cgo_settings.ITERATIONS, ruleset)
my_evaluator = compucell.compucellEvaluator(cgo_helpers.evaluationFunction)

selection = ""
if len(sys.argv) >= 3:
    selection = sys.argv[2]
else:
    print("WELCOME!")
    print("Please make a selection.")
    print("""
    csa - Cross Sectional Analysis. Run a full analysis to rank the performance of the compucell across all inputs.
    id - In Depth Analysis. Observe the motion of a single compucell solving a problem.
    """)
    selection = input("> ")

if selection == 'csa':
    print("CROSS SECTIONAL ANALYSIS")
    print("(Using the function defined in cgo_helpers (evaluationFunction))")

    result = my_evaluator.evaluate(my_compucell, verbose=True)
    print(f"RESULT = {result}")
elif selection == 'id':
    print("IN-DEPTH ANALYSIS")

    to_watch = 0
    if len(sys.argv) >= 4:
        to_watch = int(sys.argv[3])
    else:
        to_watch = int(input('Watch what?\n> '))
    
    my_compucell.cellular_automata.verbose = True
    
    targets = []
    for i in range(cgo_settings.INPUT_SPACE_SIZE):
        bit_array = cgo_helpers.evaluationFunction(compucell.intToOneDBitArray(to_watch, 4))
        if bit_array[i] == 1:
            targets.append((i, cgo_settings.FUNCTION_SPACE_SIZE))
    my_compucell.cellular_automata.targets = targets
    my_compucell.execute(compucell.intToOneDBitArray(to_watch, cgo_settings.INPUT_SPACE_SIZE))

elif selection == 'rss':
    print("RULESET SIMPLIFICATION")
    on_indexes = [i for i in range(512) if data['rs'][i] == '1']
    on_indexes_binary = []
    for i in on_indexes:
        bit_array = compucell.intToOneDBitArray(i, 9)
        bit_list  = [str(item) for sublist in bit_array.tolist() for item in sublist]
        bit_string= ''.join(bit_list)
        on_indexes_binary.append(bit_string)

    crunched = cruncher.superCrunch(on_indexes_binary)
    for i in crunched:
        print(f"{i[0]}{i[1]}{i[2]}")
        print(f"{i[3]}{i[4]}{i[5]}")
        print(f"{i[6]}{i[7]}{i[8]}")
        print("")

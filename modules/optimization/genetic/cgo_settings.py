FUNCTION_NAME = "ADD1"
CC_PER_BATCH = 2000 #Number of compucells per batch
FUNCTION_SPACE_SIZE = 3 #Number of columns in the function space
ITERATIONS = FUNCTION_SPACE_SIZE
RUNS = 30 #Number of times to run the simulation
PERFORMANCE_THRESHOLD = 0.95 #If a compucell performs better than this threshold, stop the simulation and return
INPUT_SPACE_SIZE = 4
MUTATION_CHANCE = 30/((FUNCTION_SPACE_SIZE*INPUT_SPACE_SIZE)+512)#30 -> 80%

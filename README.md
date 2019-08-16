# Welcome to Owen's Compucell "Lab"!

## What is a compucell?

A compucell is a cellular automata plane, with a set of rules and initial state such that data that is passed in as an input (along one edge of the plane) is transformed into an output (along the other side of the plane) after a set number of iterations.

## What is the compucell hypothesis?

The compucell hypothesis is: Any deterministic function can be represented perfectly as a compucell if a correct shape and number of iterations is chosen.

## Has it been proven?

No, of course not. That's why it is a hypothesis.

## What is interesting about the compucell hypothesis?

Syncronization with simple, shared rules. An individual cell can only see itself and it's neighbors, and has no concept of location, but must work together with other cells to produce a solution.

## What is in this repo?

Primarily, three things:

1. Tools for running compucells.

2. Tools for finding compucells that match constraints. (optimization)

3. Tools for analyzing compucells.

## What are the differences between the optimizers? Which one is best?

Genetic - This one is awesome. It is fast and you get to watch a species of compucells rise up like you are some kind of eldrich god. However, it tends to get stuck on optima.

Hill Climb - This is pretty reliable, but takes forever, because when there are multiple most positive gradients, it takes all of them, which means that the number of tests multiplies.

Simulated Annealing - It doesn't work.


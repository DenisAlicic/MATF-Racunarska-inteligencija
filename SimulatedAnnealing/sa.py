# Algoritam simuliranog kaljenja za prost lokacijski problem
# Svakom korisniku dodeliti tacno jedan resurs tako da ukupna cena dodeljivanja bude minimalna.
# Date su cene dodeljivanja svakog resursa svakom korisniku kao i cene uspostavljanja svakog od resursa.
import random
import argparse

def readInput(fileName):
    with open(fileName,'r') as f:
        nbUsers, nbResources = [int(i) for i in f.readline().split()]
        cost = [[int(j) for j in f.readline().split()] for i in range(nbUsers)]
        fixedCost = [int(i) for i in f.readline().split()]
        return nbUsers, nbResources, cost, fixedCost

def isFeasible(solution):
    return any(solution)

def initialize(nbResources, probability):
    solution = []
    for _ in range(nbResources):
        solution.append(random.random() < probability)
    if not isFeasible(solution):
        solution[random.randrange(nbResources)] = True
    return solution

def invert(nbResources, solution):
    j = random.randrange(nbResources)
    solution[j] = not solution[j]
    if isFeasible(solution):
        return j
    else:
        solution[j] = not solution[j]
        return -1

def solutionValue(nbUsers, nbResources, cost, fixedCost, solution):
    value = 0.0
    used = [False]*nbResources
    for i in range(nbUsers):
        minCost = float('inf')
        jUsed = -1
        for j in range(nbResources):
            if solution[j] and cost[i][j] < minCost:
                minCost = cost[i][j]
                jUsed = j
        value += minCost
        used[jUsed] = True
    for j in range(nbResources):
        if used[j]:
            value += fixedCost[j]
    solution[:] = used
    return value

def restore(j, solution):
    solution[j] = not solution[j]

def simulateAnnealing(nbUsers, nbResources, cost, fixedCost, maxIter, probability):
    solution = initialize(nbResources, probability)
    bestSolution = [i for i in solution]
    currValue = solutionValue(nbUsers, nbResources, cost, fixedCost, solution)
    bestValue = currValue
    i = 0
    while i < maxIter:
        j = invert(nbResources, solution)
        if j < 0:
            continue
        newValue = solutionValue(nbUsers, nbResources, cost, fixedCost, solution)
        if newValue < currValue:
            currValue = newValue
        else:
           p = 1.0 / (i+1)**0.5
           q = random.uniform(0, 1)
           if q < p:
               currValue = newValue
           else:
               restore(j, solution)
        if currValue < bestValue:
            bestValue = currValue
            bestSolution = solution[:]
        i += 1
    return bestValue

def main():
    parser = argparse.ArgumentParser(
        prog=__file__,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i',
        '--input_path',
        help='Path to .txt file contains matrices',
        required=True
    )
    parser.add_argument(
        '-iter',
        '--max_iter',
        help='Maximum iterations',
        required=True
    )
    args = parser.parse_args()

    nbUsers, nbResources, cost, fixedCost = readInput(args.input_path)
    print(simulateAnnealing(nbUsers, nbResources, cost, fixedCost, int(args.max_iter), 0.75))


if __name__ == "__main__":
    main()

import random
import argparse

class Individual:
    def __init__(self, nbUsers, nbResources, cost, fixedCost):
        self.code = []
        self.nbUsers = nbUsers
        self.nbResources = nbResources
        self.cost = cost
        self.fixedCost = fixedCost
        for i in range(nbResources):
            self.code.append(random.uniform(0,1) < 0.25)
        self.correctNonFeasible(nbResources)
        self.fitness = self.fitnessFunction()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def correctNonFeasible(self, nbResources):
        if any(self.code):
            return
        index = random.randrange(nbResources)
        self.code[index] = True

    def fitnessFunction(self):
        value = 0.0
        used = [False]*self.nbResources
        for i in range(self.nbUsers):
            min = float('inf')
            jUsed = -1
            for j in range(self.nbResources):
                if self.code[j] and self.cost[i][j] < min:
                    min = self.cost[i][j]
                    jUsed = j
            value += min
            used[jUsed] = True
        self.code = used
        for j in range(self.nbResources):
            if self.code[j]:
                value += self.fixedCost[j]
        return value

def readInput(fileName):
    with open(fileName,'r') as f:
        nbUsers, nbResources = [int(i) for i in f.readline().split()]
        cost = [[int(j) for j in f.readline().split()] for i in range(nbUsers)]
        fixedCost = [int(i) for i in f.readline().split()]
        return nbUsers, nbResources, cost, fixedCost

def selection(population, num):
    min = float('inf')
    index = -1
    for i in range(num):
        k = random.randrange(len(population))
        if population[k].fitness < min:
            min = population[k].fitness
            index = k
    return population[index]

def crossover(nbResources, p1, p2, c1, c2):
    index = random.randrange(nbResources)
    for i in range(index):
        c1.code[i] = p1.code[i]
        c2.code[i] = p2.code[i]
    for i in range(index, nbResources):
        c1.code[i] = p2.code[i]
        c2.code[i] = c1.code[i]
    c1.fitness = c1.fitnessFunction()
    c2.fitness = c2.fitnessFunction()
    return

def mutation(population, num, prob, nbResources):
    for i in range(num):
        index = random.randrange(len(population))
        if random.uniform(0,1) < prob:
            index2 = random.randrange(nbResources)
            population[index].code[index2] = not population[index].code[index2]
            population[index].fitness = population[index].fitnessFunction()


def ea(nbUsers, nbResources, cost, fixedCost, tournamentSize, mutationSize, mutationRate, populationSize, maxIter, eliteSize):
    population = []
    for i in range(populationSize):
        population.append(Individual(nbUsers, nbResources, cost, fixedCost))
    for i in range(maxIter):
        population.sort()
        if i % 100 == 0:
            print("Iteration: {}\nBest solution: {}".format(i, population[0].fitness))
        newPopulation = []
        for i in range(eliteSize):
            newPopulation.append(population[i])
        for i in range(eliteSize, populationSize, 2):
            p1 = selection(population, tournamentSize)
            p2 = selection(population, tournamentSize)
            c1 = Individual(nbUsers, nbResources, cost, fixedCost)
            c2 = Individual(nbUsers, nbResources, cost, fixedCost)
            crossover(nbResources, p1, p2 ,c1, c2)
            newPopulation.append(c1)
            newPopulation.append(c2)
        mutation(newPopulation, mutationSize, mutationRate, nbResources)
        population = newPopulation
    print("Solution: ", min(population).fitness)



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
        '-mr',
        '--mutation_rate',
        help='Probability of mutation',
        required=True,
        type=float
    )
    parser.add_argument(
        '-es',
        '--elite_size',
        help='Number of best individuals to save',
        required=True,
        type=int
    )
    parser.add_argument(
        '-ms',
        '--mutation_size',
        help='Number of possible Individuals for mutation',
        required=True,
        type=int
    )
    parser.add_argument(
        '-ts',
        '--tournament_size',
        help='Number of Individuals for tournament',
        required=True,
        type=int
    )
    parser.add_argument(
        '-max',
        '--max_iter',
        help='Number of iterations',
        required=True,
        type=int
    )
    parser.add_argument(
        '-ps',
        '--population_size',
        help='Number of Individuals in one population',
        required=True,
        type=int
    )
    args = parser.parse_args()

    nbUsers, nbResources, cost, fixedCost = readInput(args.input_path)
    ea(nbUsers, nbResources, cost, fixedCost, args.tournament_size, args.mutation_size, args.mutation_rate, args.population_size, args.max_iter, args.elite_size)
if __name__ == "__main__":
    main()

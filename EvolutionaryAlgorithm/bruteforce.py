# Algoritam grube sile za resavanje prostog lokacijskog problema
# Pronalazi sve mogucnosti i vraca egzaktno resenje.
# Koristan za poredjenje genetskog algoritma i algoritma simuliranog kaljenja 
# na malim instancama.
# Vremenska slozenost je eksponencijalna (NP tezak problem)
import sys
sys.path.append("../SimulatedAnnealing")
from sa import readInput, solutionValue, isFeasible
import argparse

min = float('inf')

def bestValue(i, nbUsers, nbResources, cost, fixedCost, solution):
    global min
    if i == nbResources:
        if not isFeasible(solution):
            return
        value = solutionValue(nbUsers, nbResources, cost, fixedCost, solution)
        if value < min:
            min = value
        return
    solution[i] = True
    bestValue(i+1, nbUsers, nbResources, cost, fixedCost, solution)
    solution[i] = False
    bestValue(i+1, nbUsers, nbResources, cost, fixedCost, solution)
def main():
    parser = argparse.ArgumentParser(
        prog=__file__,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i',
        '--input_path',
        help='Path to .txt file contains matrices',
        required=True
    )
    args = parser.parse_args()
    global min
    nbUsers, nbResources, cost, fixedCost = readInput(args.input_path)
    solution = [None] * nbResources
    bestValue(0, nbUsers, nbResources, cost, fixedCost, solution)
    print(min)


if __name__ == "__main__":
    main()

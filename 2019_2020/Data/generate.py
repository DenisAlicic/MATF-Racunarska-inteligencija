# Code for random making uncapacitated facility location problem examples
import random
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog=__file__,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-o',
        '--output_path',
        help='Path to .txt file contains matrices',
        required=True
    )
    parser.add_argument(
        '-resources',
        '--nb_resources',
        help='Number of resources',
        required=True
    )
    parser.add_argument(
        '-users',
        '--nb_users',
        help='Number of users',
        required=True
    )
    args = parser.parse_args()

    nbResources = int(args.nb_resources)
    nbUsers = int(args.nb_users)
    matrix = [[random.randint(1,21) for _ in range(nbResources)] for _ in range(nbUsers)]
    fixedCost = [random.randint(1,31) for _ in range(nbResources)]
    with open(args.output_path, 'w') as f:
        f.write(str(nbUsers) + " ")
        f.write(str(nbResources) + "\n")
        for i in range(nbUsers):
            for j in range(nbResources):
                f.write(str(matrix[i][j]) + " ")
            f.write("\n")
        for cost in fixedCost:
            f.write(str(cost) + " ")

if __name__ == "__main__":
    main()

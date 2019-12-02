# Problem rasporednjivanja n dama na sahovsku tablu
# dimenzija n x n koriscenjem branch and bound familije algoritama

import numpy as np


def printSolution(board):
    n = board.shape[0]
    for i in range(n):
        for j in range(n):
            print(board[i][j], end=' ')
        print()

def isFree(r, c, rowCheck, d1Check, d2Check):
    n = rowCheck.shape[0]
    if rowCheck[r] or d1Check[r+c] or d2Check[r-c+n-1]:
        return False
    return True

def bnb(board, c, rowCheck, d1Check, d2Check):
    n = board.shape[0]
    if c >= n:
        return True
    for r in range(n):
        if isFree(r, c, rowCheck, d1Check, d2Check):
            board[r][c] = 'Q'
            rowCheck[r] = True
            d1Check[r+c] = True
            d2Check[r-c+n-1] = True
            if bnb(board, c+1, rowCheck, d1Check, d2Check):
                return True
            board[r][c] = '.'
            rowCheck[r] = False
            d1Check[r+c] = False
            d2Check[r-c+n-1] = False
    return False
def solve(n):
    board = np.full((n, n), '.', dtype=str)
    rowCheck = np.full(n, False)
    d1Check = np.full(2*n-1, False)
    d2Check = np.full(2*n-1, False)
    if not bnb(board, 0, rowCheck, d1Check, d2Check):
        print("Nema resenja")
        return False
    printSolution(board)
    return True
def main():
    solve(8)
if __name__ == "__main__":
    main()
